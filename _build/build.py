# Generates the site's pages with a shared header/footer.
# Usage (from the repo root): python3 _build/build.py
# Edit content here, run it, and commit the regenerated .html files.
# This folder is blocked from being served by staticwebapp.config.json.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)

MARK = '''<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">
        <rect width="40" height="40" rx="9" fill="#1c3557"/>
        <path d="M9 26a11 11 0 0 1 22 0" fill="none" stroke="#8fb5e0" stroke-width="3" stroke-linecap="round"/>
        <path d="M20 26l7-8" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
        <circle cx="20" cy="26" r="3" fill="#ffffff"/>
      </svg>'''

NAV = [("index.html","Home"),("services.html","Services"),("case-studies.html","Case Studies"),("about.html","About"),("contact.html","Contact")]

def page(fname, title, desc, body, current=None, scripts=""):
    links = "\n".join(
        f'          <li><a href="/{h if h!="index.html" else ""}"{" aria-current=\"page\"" if h==current else ""}>{l}</a></li>'
        for h,l in NAV)
    full_title = "Office Tune-Up Consulting" if title is None else f"{title} | Office Tune-Up Consulting"
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Remove noindex at go-live (name not yet formally checked) -->
  <meta name="robots" content="noindex, nofollow">
  <title>{full_title}</title>
  <meta name="description" content="{desc}">
  <link rel="stylesheet" href="/css/site.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/">
      {MARK}
        <span class="brand-text">
          <span class="brand-name">Office Tune-Up Consulting</span>
          <span class="brand-tagline">Fewer steps. Smoother office. Room to grow.</span>
        </span>
      </a>
      <nav class="site-nav" aria-label="Main">
        <ul>
{links}
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <p>&copy; 2026 Office Tune-Up Consulting &middot; Washington state</p>
      <p><a href="/contact.html">Start with a free Tune-Up Check</a></p>
    </div>
  </footer>
{scripts}</body>
</html>
'''
    with open(os.path.join(out, fname), "w") as f:
        f.write(html)

CTA = '''    <section>
      <div class="wrap">
        <div class="callout">
          <h2>Not sure where to start?</h2>
          <p>A free Tune-Up Check takes about an hour. You'll get a one-page summary of what's slowing your office down and a fixed-price plan to fix it. No obligation.</p>
          <div class="btn-row">
            <a class="btn btn-primary" href="/contact.html">Book a free Tune-Up Check</a>
          </div>
        </div>
      </div>
    </section>'''

ICON = {
 "mail": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "doc": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h4"/></svg>',
 "copy": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/></svg>',
 "bell": '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8"/><path d="M10 20a2 2 0 0 0 4 0"/></svg>',
}

# ---------------- Home ----------------
home = f'''    <section class="hero">
      <div class="wrap">
        <h1>Less chasing. More doing.</h1>
        <p class="tagline">Fewer steps. Smoother office. Room to grow.</p>
        <p class="lead">Office Tune-Up Consulting helps small and mid-sized businesses fix the everyday processes that slow an office down, using the tools you already pay for.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="/contact.html">Book a free Tune-Up Check</a>
          <a class="btn btn-secondary" href="/services.html">See services</a>
        </div>
      </div>
    </section>

    <section class="section-white">
      <div class="wrap">
        <p class="eyebrow">Sound familiar?</p>
        <h2>Where offices lose time</h2>
        <div class="grid">
          <div class="card">{ICON["mail"]}<h3>Chasing approvals</h3><p>Requests sit in someone's inbox, and nobody knows who has the ball.</p></div>
          <div class="card">{ICON["doc"]}<h3>Hunting for documents</h3><p>Three copies of the same file, and no one is sure which is the latest.</p></div>
          <div class="card">{ICON["copy"]}<h3>Typing it in again</h3><p>The same information goes into an email, a spreadsheet and another system.</p></div>
          <div class="card">{ICON["bell"]}<h3>Finding out too late</h3><p>Problems surface after the deadline instead of when they could still be fixed.</p></div>
        </div>
        <p style="margin-top:1.5em">The fix starts with the process. Then your tools do the work.</p>
      </div>
    </section>

    <section>
      <div class="wrap">
        <p class="eyebrow">How it works</p>
        <h2>A tune-up, start to finish</h2>
        <ol class="steps">
          <li><strong>Free Tune-Up Check</strong>A short call and a walkthrough of how your office actually works.</li>
          <li><strong>Fixed-price plan</strong>A one-page summary and a quote that lists exactly what's included.</li>
          <li><strong>The tune-up</strong>Clearer processes, approval routing, organized documents, alerts and simple dashboards.</li>
          <li><strong>Handoff</strong>A hands-on walkthrough and plain-language notes, so your team owns it.</li>
        </ol>
      </div>
    </section>

    <section class="section-white">
      <div class="wrap">
        <div class="grid grid-2">
          <div class="card">
            <span class="tag">One problem</span>
            <h3>Quick Fix</h3>
            <p>The low-cost way to start. One clearly defined file, like a Word template, a tracker spreadsheet or an org chart, for a flat fee.</p>
            <p><a href="/services.html#quick-fix">About Quick Fix</a></p>
          </div>
          <div class="card">
            <span class="tag green">Whole office &middot; Free</span>
            <h3>Tune-Up Check</h3>
            <p>About an hour to find what's slowing your office down, ending with a one-page summary and a fixed-price quote.</p>
            <p><a href="/services.html#tune-up-check">About the Tune-Up Check</a></p>
          </div>
        </div>
        <div class="note" style="margin-top:24px">
          <p><strong>No upselling.</strong> I start with what you already pay for and recommend upgrades only when they clearly pay for themselves. If I'd earn anything from a recommendation, you'll know up front.</p>
        </div>
      </div>
    </section>

{CTA}'''
page("index.html", None, "Office Tune-Up Consulting helps small and mid-sized businesses run more efficiently using the tools they already pay for.", home, "index.html")

# ---------------- Services ----------------
services = f'''    <div class="page-title">
      <div class="wrap">
        <h1>Services</h1>
        <p class="lead">Fixed prices, clear scope, and plain language throughout.</p>
      </div>
    </div>

    <section class="section-white">
      <div class="wrap prose">
        <p>Office Tune-Up Consulting helps small and mid-sized businesses run more efficiently, grow without chaos, and keep everyone accountable. If your team is chasing approvals by email, hunting for the latest version of a document, typing the same information into three places, or finding out about problems too late, the fix starts with the process. Then your tools do the work.</p>
        <p>I start with what you already pay for and recommend upgrades only when they clearly pay for themselves, and if I'd earn anything from a recommendation, you'll know up front. Microsoft 365 and Dynamics 365 are my specialty.</p>
        <p>A typical tune-up begins with a short look at how your office actually works, followed by a fixed-price plan: clearer processes, approval routing, organized document storage, automatic alerts and reminders, and simple dashboards that show who's doing what. When it's done, your team gets a hands-on walkthrough and plain-language notes, and an optional ongoing maintenance plan keeps things running smoothly as you grow.</p>
      </div>
    </section>

    <section>
      <div class="wrap">
        <h2>Ways to work together</h2>
        <p class="lead">Two ways to start: a Quick Fix for one problem, or a free Tune-Up Check for the whole office.</p>
        <div class="grid grid-2" style="margin-top:24px">

          <article class="card package" id="quick-fix">
            <span class="tag">Start small</span>
            <h3>Quick Fix</h3>
            <p class="meta">Flat fee &middot; one problem</p>
            <p>One clearly defined file, built in a few hours, with no access needed to your accounts. The low-cost way to start.</p>
            <h4>Good for</h4>
            <ul>
              <li>Word templates: letterhead, proposals, invoices</li>
              <li>Spreadsheets: trackers, budgets, schedules</li>
              <li>Org charts</li>
            </ul>
            <h4>Included</h4>
            <ul>
              <li>The finished file and short how-to notes</li>
              <li>14 days to correct anything not working as agreed</li>
            </ul>
            <h4>How it works</h4>
            <p>You send what's needed (your logo, examples, the fields you want). I confirm it fits a Quick Fix before you commit. If it's bigger, I'll suggest a Tune-Up Check or a quote instead.</p>
          </article>

          <article class="card package free" id="tune-up-check">
            <span class="tag green">Free</span>
            <h3>Tune-Up Check</h3>
            <p class="meta">About 1 hour &middot; no obligation</p>
            <p>A short look at how your office actually works.</p>
            <h4>What happens</h4>
            <ul>
              <li>A 15-minute call about the systems you use and where time gets lost</li>
              <li>A walkthrough of up to 45 minutes: your departments, your people and where communication breaks down</li>
              <li>On-site within a 30-minute drive of Vancouver, WA; remote everywhere else</li>
            </ul>
            <h4>You get</h4>
            <ul>
              <li>A one-page summary of what I found</li>
              <li>A fixed-price quote that lists its assumptions, so you know exactly what's covered</li>
            </ul>
          </article>

          <article class="card package" id="office-tune-up">
            <span class="tag">Most complete</span>
            <h3>Office Tune-Up</h3>
            <p class="meta">Fixed price &middot; quoted after your Check</p>
            <p>Up to three process improvements, typically one per department. A process that crosses departments counts as one.</p>
            <h4>Can include</h4>
            <ul>
              <li>Approval routing</li>
              <li>Organized document storage</li>
              <li>Automatic alerts and reminders</li>
              <li>Simple dashboards that show who's doing what</li>
            </ul>
            <h4>Included</h4>
            <ul>
              <li>A hands-on walkthrough and plain-language notes</li>
              <li>30 days to fix anything not working as agreed</li>
            </ul>
            <h4>Not included</h4>
            <ul>
              <li>License costs (you pay Microsoft directly)</li>
              <li>Large data migrations or work in non-Microsoft tools</li>
              <li>Additional departments or processes (quoted separately)</li>
            </ul>
          </article>

          <article class="card package" id="ongoing-maintenance">
            <span class="tag">Optional</span>
            <h3>Ongoing Maintenance</h3>
            <p class="meta">Monthly</p>
            <p>Keeps things running smoothly as your business grows.</p>
            <h4>Included</h4>
            <ul>
              <li>A set number of hours each month for small changes and fixes</li>
              <li>A monthly check-in</li>
              <li>Keeping your automations and apps healthy</li>
              <li>Replies within 2 business days</li>
            </ul>
            <p style="margin-top:1em">Not an emergency or same-day support service.</p>
          </article>

        </div>
      </div>
    </section>

{CTA}'''
page("services.html", "Services", "Quick Fix, free Tune-Up Check, Office Tune-Up and Ongoing Maintenance: fixed prices and clear scope.", services, "services.html")

exec(open(os.path.join(HERE, 'cases.py')).read())

# ---------------- About ----------------
about = f'''    <div class="page-title">
      <div class="wrap">
        <h1>About</h1>
        <p class="lead">Process help first. Microsoft 365 and Dynamics 365 are the specialty, not the limit.</p>
      </div>
    </div>

    <section class="section-white">
      <div class="wrap prose">
        <h2>Hi, I'm Neil.</h2>
        <p>I spent 10 years in construction accounting and have done bookkeeping for other kinds of businesses too, so I know the office side of a business from the inside: the receipts, the job costs, the approvals that stall and the reports that take all afternoon.</p>
        <p>Today I'm a Power Platform developer based in Washington state. I build the systems that replace email chains, spreadsheets and retyping with processes that run on their own: approval routing, document control, automatic alerts and dashboards that show where things stand.</p>
        <p>Office Tune-Up Consulting brings that work to small and mid-sized businesses. I work with office managers and owners, not just IT, so everything comes in plain language and your team gets notes they can actually use.</p>

        <h2>What I believe</h2>
        <ul>
          <li><strong>Process before tools.</strong> Automating a confusing process just makes the confusion faster.</li>
          <li><strong>Use what you already have.</strong> Most offices already pay for more than they use.</li>
          <li><strong>No surprises.</strong> Fixed prices, written assumptions, and any income from a recommendation disclosed up front.</li>
          <li><strong>You own it.</strong> Every project ends with a walkthrough and plain-language notes.</li>
        </ul>

        <h2>What I work with</h2>
        <ul>
          <li><strong>Everyday Microsoft 365 apps:</strong> Word, Excel, Outlook, Teams, SharePoint and OneDrive</li>
          <li><strong>Automation, apps and reporting:</strong> Power Apps, Power Automate, Dataverse, Power BI and Azure Functions</li>
          <li><strong>Business systems:</strong> Dynamics 365, including Sales and Business Central</li>
        </ul>
        <p>Process advice applies to any tool; the hands-on building is in Microsoft 365 and Dynamics 365.</p>
      </div>
    </section>

{CTA}'''
page("about.html", "About", "About Office Tune-Up Consulting and its approach: process first, plain language, no surprises.", about, "about.html")

# ---------------- Contact ----------------
contact = '''    <div class="page-title">
      <div class="wrap">
        <h1>Contact</h1>
        <p class="lead">Start with a free Tune-Up Check or ask about a Quick Fix.</p>
      </div>
    </div>

    <section class="section-white">
      <div class="wrap prose">
        <div class="note">
          <p><strong>The request form is coming soon.</strong> Check back shortly.</p>
        </div>
        <h2 style="margin-top:1.5em">What the request will ask</h2>
        <ul>
          <li>Your name, business and how to reach you</li>
          <li>Roughly how many people work in your office</li>
          <li>The tools you use today (for example Microsoft 365, Dynamics 365, spreadsheets)</li>
          <li>What's slowing your office down, in your own words</li>
          <li>Whether you're interested in a Quick Fix or a free Tune-Up Check</li>
        </ul>
        <p>I reply within 2 business days.</p>
      </div>
    </section>'''
page("contact.html", "Contact", "Request a free Tune-Up Check or a Quick Fix from Office Tune-Up Consulting.", contact, "contact.html")

# ---------------- Intake form test page ----------------
# Locked to the "owner" role in staticwebapp.config.json until go-live.
# At go-live this form moves onto contact.html and the role locks come off.
intake_test = '''    <div class="page-title">
      <div class="wrap">
        <h1>Request a free Tune-Up Check</h1>
        <p class="lead">Test version of the request form. Only signed-in owners can see this page.</p>
      </div>
    </div>

    <section class="section-white">
      <div class="wrap prose">
        <form id="intake-form" class="intake-form" novalidate>
          <div class="field">
            <label for="f-name">Your name <span class="req">(required)</span></label>
            <input id="f-name" name="name" type="text" autocomplete="name" maxlength="100" required>
            <p class="field-error" id="e-name" hidden></p>
          </div>
          <div class="field">
            <label for="f-business">Business name</label>
            <input id="f-business" name="business" type="text" autocomplete="organization" maxlength="150">
            <p class="field-error" id="e-business" hidden></p>
          </div>
          <div class="field">
            <label for="f-email">Email <span class="req">(required)</span></label>
            <input id="f-email" name="email" type="email" autocomplete="email" maxlength="200" required>
            <p class="field-error" id="e-email" hidden></p>
          </div>
          <div class="field">
            <label for="f-phone">Phone</label>
            <input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40">
            <p class="field-error" id="e-phone" hidden></p>
          </div>
          <div class="field">
            <label for="f-size">How many people work in your office?</label>
            <select id="f-size" name="officeSize">
              <option value="">Choose one</option>
              <option value="1-5">1 to 5</option>
              <option value="6-15">6 to 15</option>
              <option value="16-50">16 to 50</option>
              <option value="51+">More than 50</option>
            </select>
            <p class="field-error" id="e-officeSize" hidden></p>
          </div>
          <div class="field">
            <label for="f-tools">Tools you use today</label>
            <input id="f-tools" name="tools" type="text" maxlength="500" placeholder="For example Microsoft 365, Dynamics 365, spreadsheets">
            <p class="field-error" id="e-tools" hidden></p>
          </div>
          <div class="field">
            <label for="f-message">What's slowing your office down? <span class="req">(required)</span></label>
            <textarea id="f-message" name="message" rows="6" maxlength="3000" required></textarea>
            <p class="field-error" id="e-message" hidden></p>
          </div>
          <fieldset class="field">
            <legend>What are you interested in? <span class="req">(required)</span></legend>
            <label class="choice"><input type="radio" name="interest" value="tune-up-check" checked> A free Tune-Up Check (whole office)</label>
            <label class="choice"><input type="radio" name="interest" value="quick-fix"> A Quick Fix (one problem)</label>
            <label class="choice"><input type="radio" name="interest" value="not-sure"> Not sure yet</label>
            <p class="field-error" id="e-interest" hidden></p>
          </fieldset>
          <div class="hp" aria-hidden="true">
            <label for="f-website">Leave this empty</label>
            <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off">
          </div>
          <button class="btn btn-primary" type="submit">Send request</button>
          <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>'''
page("intake-test.html", "Request form (test)", "Request form test page.", intake_test, None,
     '  <script src="/js/intake.js" defer></script>\n')

# ---------------- 404 ----------------
nf = '''    <section>
      <div class="wrap prose">
        <h1>That page isn't here</h1>
        <p class="lead">The link may be old or mistyped.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="/">Go to the home page</a>
          <a class="btn btn-secondary" href="/services.html">See services</a>
        </div>
      </div>
    </section>'''
page("404.html", "Page not found", "Page not found.", nf)
