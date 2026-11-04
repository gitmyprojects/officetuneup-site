// POST /api/intake — saves a contact request to Cosmos DB and emails an alert.
// Settings (Static Web App > Environment variables; never in the repo):
//   COSMOS_CONNECTION_STRING   required
//   COSMOS_DATABASE            optional, default "intake"
//   COSMOS_CONTAINER           optional, default "requests"
//   ACS_CONNECTION_STRING      optional until the email alert is set up
//   ACS_SENDER                 e.g. DoNotReply@<guid>.azurecomm.net
//   ALERT_TO                   address that receives the alerts
'use strict';

const { app } = require('@azure/functions');
const { randomUUID } = require('node:crypto');
const { checkSubmission, MAX_BODY_BYTES } = require('../validate');

let container; // reused between calls while the function stays warm
function getContainer() {
  if (!container) {
    const { CosmosClient } = require('@azure/cosmos');
    const client = new CosmosClient(process.env.COSMOS_CONNECTION_STRING);
    container = client
      .database(process.env.COSMOS_DATABASE || 'intake')
      .container(process.env.COSMOS_CONTAINER || 'requests');
  }
  return container;
}

let emailClient;
async function sendAlert(doc, context) {
  const { ACS_CONNECTION_STRING, ACS_SENDER, ALERT_TO } = process.env;
  if (!ACS_CONNECTION_STRING || !ACS_SENDER || !ALERT_TO) {
    context.log('Email alert skipped: ACS settings not configured yet.');
    return;
  }
  if (!emailClient) {
    const { EmailClient } = require('@azure/communication-email');
    emailClient = new EmailClient(ACS_CONNECTION_STRING);
  }
  const labels = { 'tune-up-check': 'Free Tune-Up Check', 'quick-fix': 'Quick Fix', 'not-sure': 'Not sure yet' };
  const lines = [
    `New request received ${doc.createdAt}`,
    '',
    `Name:        ${doc.name}`,
    `Business:    ${doc.business || '-'}`,
    `Email:       ${doc.email}`,
    `Phone:       ${doc.phone || '-'}`,
    `Office size: ${doc.officeSize || '-'}`,
    `Interested:  ${labels[doc.interest] || doc.interest}`,
    `Tools:       ${doc.tools || '-'}`,
    '',
    'What is slowing the office down:',
    doc.message,
    '',
    `Request id: ${doc.id}`,
  ];
  // Start the send; don't wait for final delivery status (that can take a while).
  await emailClient.beginSend({
    senderAddress: ACS_SENDER,
    recipients: { to: [{ address: ALERT_TO }] },
    replyTo: [{ address: doc.email, displayName: doc.name }],
    content: {
      subject: `New intake request: ${doc.name}`.slice(0, 150),
      plainText: lines.join('\n'),
    },
  });
}

function reply(status, body) {
  return { status, jsonBody: body, headers: { 'Cache-Control': 'no-store' } };
}

app.http('intake', {
  methods: ['POST'],
  authLevel: 'anonymous', // access is controlled by staticwebapp.config.json routes
  route: 'intake',
  handler: async (request, context) => {
    const declared = Number(request.headers.get('content-length') || 0);
    if (declared > MAX_BODY_BYTES) return reply(413, { ok: false, error: 'Request too large.' });

    const type = request.headers.get('content-type') || '';
    if (!type.toLowerCase().startsWith('application/json')) {
      return reply(415, { ok: false, error: 'Expected JSON.' });
    }

    const text = await request.text();
    if (Buffer.byteLength(text, 'utf8') > MAX_BODY_BYTES) {
      return reply(413, { ok: false, error: 'Request too large.' });
    }

    let body;
    try { body = JSON.parse(text); } catch { return reply(400, { ok: false, error: 'The form data could not be read.' }); }

    const result = checkSubmission(body);
    if (result.spam) {
      context.log('Submission dropped by spam checks.');
      return reply(200, { ok: true }); // look successful so bots learn nothing
    }
    if (result.errors) return reply(400, { ok: false, errors: result.errors });

    const doc = {
      id: randomUUID(),
      createdAt: new Date().toISOString(),
      status: 'new',
      source: 'site-form',
      ...result.data,
    };

    try {
      await getContainer().items.create(doc);
    } catch (err) {
      context.error('Saving the request failed:', err.code || err.message);
      return reply(500, { ok: false, error: 'Something went wrong. Please try again later.' });
    }

    try {
      await sendAlert(doc, context);
    } catch (err) {
      // The request is already saved, so don't fail the visitor over the alert.
      context.error('Email alert failed:', err.code || err.message);
    }

    return reply(200, { ok: true });
  },
});
