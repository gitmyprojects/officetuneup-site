'use strict';
const test = require('node:test');
const assert = require('node:assert');
const { checkSubmission } = require('../src/validate');

const NOW = 1_800_000_000_000;
const good = () => ({
  name: 'Pat Example', business: 'Example Builders', email: 'pat@example.com', phone: '',
  officeSize: '6-15', tools: 'Microsoft 365, spreadsheets', interest: 'tune-up-check',
  message: 'Approvals get lost in email.', hp_extra: '', elapsedMs: 60_000,
});

test('accepts a clean submission', () => {
  const r = checkSubmission(good(), NOW);
  assert.ok(r.data);
  assert.equal(r.data.email, 'pat@example.com');
});

test('honeypot filled is treated as spam (new and old field names)', () => {
  assert.deepEqual(checkSubmission({ ...good(), hp_extra: 'http://spam' }, NOW), { spam: true });
  assert.deepEqual(checkSubmission({ ...good(), website: 'http://spam' }, NOW), { spam: true });
});

test('too fast, too slow or missing elapsed time is spam', () => {
  assert.ok(checkSubmission({ ...good(), elapsedMs: 500 }, NOW).spam);
  assert.ok(checkSubmission({ ...good(), elapsedMs: 2 * 24 * 60 * 60 * 1000 }, NOW).spam);
  assert.ok(checkSubmission({ ...good(), elapsedMs: undefined }, NOW).spam);
  assert.ok(checkSubmission({ ...good(), elapsedMs: 'abc' }, NOW).spam);
});

test('missing required fields are reported', () => {
  const r = checkSubmission({ ...good(), name: ' ', message: '' }, NOW);
  assert.ok(r.errors.name && r.errors.message);
});

test('bad email, long message and unknown option are rejected', () => {
  const r = checkSubmission({ ...good(), email: 'nope', message: 'x'.repeat(3001), interest: 'free stuff' }, NOW);
  assert.ok(r.errors.email && r.errors.message && r.errors.interest);
});

test('control characters are stripped', () => {
  const r = checkSubmission({ ...good(), name: 'Pat\u0000 Example\u0007' }, NOW);
  assert.equal(r.data.name, 'Pat Example');
});

test('non-object body is rejected', () => {
  assert.ok(checkSubmission([1, 2], NOW).errors);
  assert.ok(checkSubmission(null, NOW).errors);
});
