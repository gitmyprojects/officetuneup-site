// Request form: sends the form to /api/intake as JSON and shows the result.
(function () {
  'use strict';
  var form = document.getElementById('intake-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var button = form.querySelector('button[type="submit"]');
  var startedAt = Date.now(); // used by the server's time check

  function showErrors(errors) {
    var first = null;
    form.querySelectorAll('.field-error').forEach(function (el) { el.hidden = true; el.textContent = ''; });
    form.querySelectorAll('[aria-invalid]').forEach(function (el) { el.removeAttribute('aria-invalid'); });
    Object.keys(errors || {}).forEach(function (name) {
      var msg = document.getElementById('e-' + name);
      var input = form.elements[name];
      if (msg) { msg.textContent = errors[name]; msg.hidden = false; }
      if (input && input.setAttribute) {
        input.setAttribute('aria-invalid', 'true');
        if (!first) first = input;
      }
    });
    if (first && first.focus) first.focus();
  }

  function localCheck(data) {
    var errors = {};
    if (!data.name) errors.name = 'This field is required.';
    if (!data.email) errors.email = 'This field is required.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email)) errors.email = 'Please enter a valid email address.';
    if (!data.message) errors.message = 'This field is required.';
    return errors;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var fd = new FormData(form);
    var data = {};
    ['name', 'business', 'email', 'phone', 'officeSize', 'tools', 'message', 'interest', 'website'].forEach(function (k) {
      data[k] = String(fd.get(k) || '').trim();
    });
    data.startedAt = startedAt;

    var errors = localCheck(data);
    if (Object.keys(errors).length) { showErrors(errors); status.textContent = 'Please check the highlighted fields.'; return; }
    showErrors({});

    button.disabled = true;
    status.textContent = 'Sending...';
    fetch('/api/intake', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      credentials: 'same-origin'
    })
      .then(function (res) {
        return res.json().catch(function () { return { ok: false }; }).then(function (body) { return { res: res, body: body }; });
      })
      .then(function (r) {
        if (r.res.ok && r.body.ok) {
          form.reset();
          status.textContent = "Thanks, your request was sent. I'll reply within 2 business days.";
        } else if (r.body.errors) {
          showErrors(r.body.errors);
          status.textContent = 'Please check the highlighted fields.';
        } else {
          status.textContent = 'Something went wrong. Please try again later.';
        }
      })
      .catch(function () { status.textContent = 'Something went wrong. Please check your connection and try again.'; })
      .finally(function () { button.disabled = false; });
  });
})();
