// Checks and cleans an intake submission. No Azure dependencies, so it can be unit tested.
'use strict';

const MAX_BODY_BYTES = 10 * 1024;   // whole request; the form itself is well under 5 KB
const MIN_FILL_MS = 3000;           // a person can't fill the form in under 3 seconds
const MAX_FILL_MS = 24 * 60 * 60 * 1000;

const INTERESTS = ['tune-up-check', 'quick-fix', 'not-sure'];
const OFFICE_SIZES = ['1-5', '6-15', '16-50', '51+', ''];

// [field, required, max length]
const TEXT_FIELDS = [
  ['name', true, 100],
  ['business', false, 150],
  ['email', true, 200],
  ['phone', false, 40],
  ['tools', false, 500],
  ['message', true, 3000],
];

// Remove control characters (keep line breaks and tabs in the message) and trim.
function clean(value, multiline) {
  if (typeof value !== 'string') return '';
  const pattern = multiline ? /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g;
  return value.replace(pattern, '').trim();
}

const EMAIL = /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[^\s@<>()",;:]{2,}$/;

// Returns { spam: true } for bot-looking submissions (caller pretends success),
// { errors: {...} } for invalid input, or { data: {...} } for a clean submission.
function checkSubmission(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return { errors: { form: 'The form data could not be read.' } };
  }

  // Honeypot: a hidden field people never see. Anything in it means a bot.
  // Named "hp_extra" so browser autofill and password managers don't recognize it.
  for (const name of ['hp_extra', 'website']) {
    if (typeof body[name] === 'string' && body[name].trim() !== '') return { spam: true };
  }

  // Time check: how long the visitor spent on the page, measured in their browser.
  // Uses elapsed time, not clock times, so a wrong clock on the visitor's computer can't trip it.
  const elapsed = Number(body.elapsedMs);
  if (!Number.isFinite(elapsed) || elapsed < MIN_FILL_MS || elapsed > MAX_FILL_MS) {
    return { spam: true };
  }

  const data = {};
  const errors = {};
  for (const [field, required, max] of TEXT_FIELDS) {
    const value = clean(body[field], field === 'message' || field === 'tools');
    if (required && !value) errors[field] = 'This field is required.';
    else if (value.length > max) errors[field] = `Please keep this under ${max} characters.`;
    data[field] = value;
  }
  if (data.email && !errors.email && !EMAIL.test(data.email)) {
    errors.email = 'Please enter a valid email address.';
  }

  const interest = clean(body.interest, false);
  if (!INTERESTS.includes(interest)) errors.interest = 'Please choose an option.';
  data.interest = interest;

  const officeSize = clean(body.officeSize, false);
  if (!OFFICE_SIZES.includes(officeSize)) errors.officeSize = 'Please choose an option.';
  data.officeSize = officeSize;

  return Object.keys(errors).length ? { errors } : { data };
}

module.exports = { checkSubmission, MAX_BODY_BYTES, MIN_FILL_MS };
