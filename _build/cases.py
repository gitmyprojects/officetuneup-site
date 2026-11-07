# Case studies: index page + one page per written case study.
# exec'd from build.py (uses page(), CTA and `out` from there).
import os

GROUPS = [
 ("approvals-stuck", "Approvals stall and steps get skipped"),
 ("documents", "Documents are hard to find"),
 ("double-entry", "Typing the same thing twice"),
 ("field", "Paperwork in the field"),
 ("too-late", "Finding out too late"),
]

TOOLS = ["Power Apps", "Power Automate", "Power BI", "SharePoint", "Dynamics 365", "Azure"]

# slug, group, kind (real/demo), card title (owner's words), one-line summary, tools, has_page
CARDS = [
 ("approvals", "approvals-stuck", "demo", "Approvals sit in someone's inbox",
  "Requests route themselves to the right approver, and every decision is recorded.", ["SharePoint", "Power Automate"], True),
 ("equipment-retirement", "approvals-stuck", "real", "Equipment gets retired without anyone signing off",
  "A retirement request now waits for approval, and the requester hears back in Teams.", ["Power Automate"], False),
 ("skipped-steps", "approvals-stuck", "demo", "People skip steps in the process",
  "The rules are enforced automatically, and someone is alerted if the check ever fails.", ["SharePoint", "Power Automate"], False),
 ("sales-process", "approvals-stuck", "real", "Every salesperson runs deals their own way",
  "A guided sales path collects the right information at each stage before a deal moves on.", ["Dynamics 365", "Power Automate"], False),

 ("documents", "documents", "demo", "Staff use outdated procedures",
  "One library where everyone sees only the current approved version.", ["SharePoint"], True),
 ("employee-documents", "documents", "real", "Employees can't find the latest policy or form",
  "Announcements, policies, benefits and forms in one place on every employee's phone.", ["Power Apps", "SharePoint"], False),
 ("intranet", "documents", "demo", "Company news gets lost in email",
  "One home page for news, announcements, key dates and live plant status.", ["SharePoint"], False),

 ("contracts", "double-entry", "real", "Contracts go out with mistakes",
  "Contracts built in one click from the sales record, from an approved template.", ["Dynamics 365", "Power Automate"], True),
 ("deal-won", "double-entry", "real", "Winning a deal means setting it up in several systems",
  "Marking a deal as won sets up the customer and job, notifies the team and creates shared folders.", ["Power Automate", "Dynamics 365"], False),
 ("receipts", "double-entry", "real", "Receipts arrive missing the job they belong to",
  "Receipts submitted from a phone, already coded to the job and task.", ["Power Apps"], True),

 ("vehicle-inspections", "field", "real", "Vehicle inspections are still on paper",
  "Inspections on a phone, with problems sent straight to maintenance.", ["Power Apps", "Power Automate"], True),
 ("upcoming-work", "field", "real", "Crews don't know what's coming up next",
  "Field and production crews see recent, current and upcoming jobs on their phones.", ["Power Apps"], False),

 ("production-status", "too-late", "real", "Purchasing and production aren't on the same page",
  "One board for job status, with purchasing notes next to the job they affect.", ["Power BI", "SharePoint"], True),
 ("permits", "too-late", "real", "Permits stall and nobody notices",
  "A scorecard that shows how many jobs sit at each permitting stage.", ["Power BI"], True),
 ("labor-hours", "too-late", "real", "I can't see where the labor hours went",
  "Labor hours by job and task, for any date range, without a spreadsheet.", ["Power BI", "Dynamics 365"], True),
 ("fuel-tax", "too-late", "real", "Fuel tax reporting is a scramble",
  "Trip logs turn into miles and gallons by state, with problem entries flagged.", ["Power BI", "Power Apps"], False),
 ("milestones", "too-late", "real", "Reviews and birthdays get forgotten",
  "Managers are reminded of birthdays, annual reviews and new-hire reviews, with the right form.", ["Power Automate", "SharePoint"], False),
 ("website-requests", "too-late", "own", "Website inquiries sit unnoticed",
  "Requests from the website are saved automatically, and an email alert goes out right away.", ["Azure"], True),
 ("change-dashboard", "too-late", "demo", "Leadership can't see where changes stand",
  "One page shows every change request, how fast approvals move and whether the rules held.", ["Power BI"], False),
]

# Full write-ups
PAGES = {
 "website-requests": dict(
  subtitle="This website's own request form",
  situation=["Office Tune-Up Consulting needed a way for business owners to ask for a free Tune-Up Check from this website.",
             "Many small business websites simply list an email address. That address soon collects spam, and a real request can sit unnoticed in a busy inbox."],
  changed=["The Contact page has a short request form. Each request is checked, saved in a secure database, and an email alert goes out with the details. Hitting Reply on the alert answers the person who asked.",
           "Spam is filtered out quietly, without making visitors solve a puzzle. The whole setup runs on Microsoft Azure's free tiers, so it costs nothing at this size."],
  before=["Email address posted on the site", "Spam and real requests mixed together", "A request gets missed"],
  after=["Visitor fills in the request form", "Request checked and saved", "Email alert with the details", "Reply straight from the alert"],
  figs=[],
  team=["No request depends on someone happening to notice an email.",
        "Every request is kept in one place, with when it arrived and its status.",
        "Replying takes one click from the alert."],
  built="Azure Static Web Apps, Azure Functions, Azure Cosmos DB, Azure Communication Services"),

 "contracts": dict(
  subtitle="Contracts built from the sales record, not by hand",
  situation=["Customer contracts started from a master Word document. Staff copied it, typed in the customer and job details, and edited the terms as they went. Word's track changes showed some edits, but not all of them were captured, and anyone with access to the master could change it.",
             "Mistakes surfaced only when a customer noticed them."],
  changed=["A Generate PDF Document button now sits on the sales record. One click pulls the customer, address, job site and project details already entered there and fills them into an approved contract template.",
           "The right contract package is chosen automatically by the state the project is in (Oregon or Washington), and the finished contract arrives as a PDF, ready to send."],
  before=["Copy the master Word file", "Type in customer and job details", "Edit the terms by hand", "Customer spots the mistake"],
  after=["Details entered once in the sales record", "Click Generate PDF Document", "Correct state's contract filled in", "PDF ready to send"],
  figs=[("contract-button.webp", 660, 56, "Sales record toolbar with the Generate PDF Document button highlighted", "The one-click button on the sales record."),
        ("contract-pdf.webp", 900, 679, "First page of a generated construction agreement with customer and site details filled in, identifying details blurred", "A generated contract with the customer and site details filled in automatically. Company and customer details are blurred.")],
  team=["Details are entered once, in the sales record, instead of being retyped into each contract.",
        "Every contract starts from the same approved wording. Changing the terms means deliberately updating the template, not editing a copy.",
        "Nobody has to remember which state's version to use."],
  built="Dynamics 365 Sales, Power Automate, Word templates"),

 "production-status": dict(
  subtitle="One production board for purchasing and the shop",
  situation=["Job status lived in the company's main business system, while the production team tracked actual start and finish dates in a separate list. Seeing where a job stood meant checking both.",
             "When purchasing learned that a material delivery would be late, there was no set place to tell production."],
  changed=["It started as a verbal request. I designed and built a single board that combines both sources: one line per job, showing whether it's finished, on the floor or not started, with running totals for the year and quarter.",
           "A notes column gives purchasing one place to flag anything that could slow production, such as a late material delivery, right next to the job it affects."],
  before=["Check job status in the main system", "Check dates in the production list", "Late materials mentioned in passing"],
  after=["One board, one line per job", "Purchasing adds a note to the job", "Production sees it beside the job"],
  figs=[("production-board.webp", 961, 422, "Production board listing jobs with description, purchasing notes, status, actual start and end dates, and totals; job numbers, customers and totals blurred", "One line per job, with status, dates and purchasing notes together. Job numbers, customers and totals are blurred.")],
  team=["Purchasing and production management look at the same list instead of two.",
        "Possible delays are written down where production will see them, instead of passed along in conversation.",
        "Job status can be read at a glance."],
  built="Power BI, SharePoint, the company's existing business system"),

 "approvals": dict(
  subtitle="Approvals that route themselves",
  situation=["At Lumen Photonics, every change to how the business runs needs sign-off from the person who owns that process. Changes that affect the financials also need a review from the controller.",
             "Done by email, nobody can easily tell who has a request, who approved it, or whether the right people were asked at all."],
  changed=["Submitting a request now sends it to the right approver automatically, based on their role rather than a name written into the setup. Financial changes go on to the controller.",
           "One person can't approve their own request or approve it twice; if that would happen, it goes to their manager instead. Every decision is recorded with who made it, and the outcome is written back to the request."],
  before=["Email the request", "Wait and follow up", "Search the inbox for who approved"],
  after=["Submit the request", "Sent to the process owner", "Financial review if needed", "Decision recorded on the request"],
  figs=[("approval-email.webp", 645, 414, "Approval email for a financial review with the request details, a link to the request, and Approve and Reject buttons", "The approver gets everything needed to decide, with Approve and Reject right in the email."),
        ("approval-history.webp", 943, 349, "Version history of a request showing each step from submission through process owner and financial approval", "Every step is recorded: who submitted, who approved and when.")],
  team=["Requesters can see where their request stands without asking.",
        "When someone changes roles, approvals follow the role. Nothing has to be rebuilt.",
        "There's a clear record of every approval if an auditor asks."],
  built="SharePoint, Power Automate, Microsoft 365 groups"),

 "documents": dict(
  subtitle="One home for every procedure",
  situation=["At Lumen Photonics, the problem came from a quality audit: an operator followed an outdated work instruction because an old copy was still sitting on a shared drive.",
             "Procedures lived in several places, in several versions, with no clear owner."],
  changed=["Procedures and work instructions now live in one library. Each document must have an owner, a department and a next review date before it can be saved.",
           "Drafts stay hidden while they're being revised. Everyone else only ever sees the current approved version, and every past version is kept along with who approved it."],
  before=["Copies on several shared drives", "Which one is current?", "The old version gets used"],
  after=["One library for every procedure", "Drafts hidden until approved", "Everyone sees the current version", "Reviewed once a year"],
  figs=[("doc-new-menu.webp", 656, 427, "New menu in the library offering only Procedure and Work Instruction", "Authors can only create the two kinds of controlled document."),
        ("doc-draft.webp", 1010, 243, "Version history showing version 0.1 with approval status Draft", "A draft stays at version 0.1, visible only to its author and approvers, until it's approved.")],
  team=["Staff find the current version in one place, every time.",
        "Authors can revise a document without confusing anyone.",
        "Every document comes up for review once a year instead of going stale."],
  built="SharePoint"),

 "receipts": dict(
  subtitle="Receipts submitted from a phone, already coded to the job",
  situation=["Employees bought tools and materials for jobs and turned in the receipts later. Accounts payable then had to work out what each purchase was for and which job and task it belonged to before it could be posted."],
  changed=["Employees now submit receipts from the company app on their phone. The first question is whether the purchase is for a job. If it is, the job and task are required, along with a short description.",
           "The app won't send a submission without the receipt attached. Accounts payable receives an email with the receipt, the employee's name, and the job, task and purchase type in the subject line. When someone from Field Service submits a receipt, their project manager is copied automatically."],
  before=["Paper receipt in a pocket", "Handed to the office later", "Accounts payable asks what it was for"],
  after=["Photo submitted from the app", "Job and task picked on the spot", "Accounts payable gets it ready to post"],
  figs=[],
  pair=[("receipt-home.webp", 315, 570, "Company app home screen with the Submit Receipt tile highlighted"),
        ("receipt-form.webp", 315, 572, "Job-related receipt form with job, task, description and attachment fields")],
  pair_caption="The Submit Receipt tile on the app's home screen, and the job-related receipt form. The company logo is blurred.",
  team=["Accounts payable gets what it needs to post the cost the first time.",
        "Job costs are cleaner because every job purchase arrives already coded.",
        "Project managers see their crews' purchases as they happen."],
  built="Power Apps, Outlook"),

 "vehicle-inspections": dict(
  subtitle="Inspections on a phone, with problems sent straight to maintenance",
  situation=["Paper inspection checklists are easy to half-finish, and a problem written on one doesn't reach maintenance until someone hands the sheet in."],
  changed=["Drivers pick their vehicle from the company's vehicle list in the app, and that vehicle's checklist loads. Each item is marked satisfactory, unsatisfactory or not applicable, with a shortcut to mark everything satisfactory and adjust from there.",
           "The inspection can't be submitted until every item is marked, every problem has a note, and the driver has signed. If anything is marked unsatisfactory, a work order listing those items is created automatically, and the maintenance technician is notified in Teams."],
  before=["Paper checklist in the truck", "Problem noted, maybe", "Maintenance finds out later"],
  after=["Checklist on the phone", "A note required for every problem", "Work order sent to maintenance"],
  figs=[],
  team=["Every submitted inspection is complete and signed.",
        "Maintenance hears about a problem as soon as the inspection is submitted, with the details already written down.",
        "There's a record of every inspection for every vehicle."],
  built="Power Apps, Power Automate, Teams"),

 "permits": dict(
  subtitle="A permit scorecard that shows where every job is stuck",
  situation=["Before a modular home can be built, the job has to be permitted. Permitting moves through several stages, and some of them are spent waiting on someone else.",
             "Without a summary, it was hard to see how many jobs were sitting in each stage, or which ones needed a follow-up."],
  changed=["A scorecard counts the jobs in every permitting stage across the top of the page, from new permit through review to pre-issuance. A large number in a waiting stage shows exactly where follow-up is needed.",
           "The same page shows the jobs and modules permitted so far this year. It can be filtered by permit technician, month and quarter, each technician has a page of their own jobs, and further pages show upcoming completion dates and how this year compares with past years."],
  before=["Status kept in each job record", "Ask around to find stuck jobs", "Delays noticed late"],
  after=["Counts by stage on one page", "Waiting stages stand out", "Follow up before it slips"],
  figs=[("permit-scorecard.webp", 968, 348, "Permit scorecard with counts of jobs at each permitting stage above a list of permitted jobs and filters for technician, month and quarter; job numbers, customers and staff blurred", "Counts by permitting stage across the top. Job numbers, customers and staff names are blurred.")],
  team=["Managers see the bottleneck at a glance.",
        "Each permit technician has their own list of jobs to work.",
        "This year's permitting can be compared with past years."],
  built="Power BI"),

 "labor-hours": dict(
  subtitle="Labor hours by job and task, for any date range",
  situation=["Every payroll hour was posted to a job and task in the accounting system. Answering simple questions, like which jobs used the most labor or which tasks take the longest, still meant exporting data and building a spreadsheet."],
  changed=["A report answers four questions, one per page: how many hours went to each job, where one job's hours went by task, which tasks take the most labor across all jobs, and how the same task compares from one job to another. Any date range or payroll week can be selected.",
           "A short guide page explains that hours appear on the day payroll posts, so a midweek spike isn't mistaken for a busy day, and shows how to drill into the rows behind any bar and export them to Excel."],
  before=["Export payroll postings", "Build a spreadsheet", "Answer one question"],
  after=["Pick a date range or a job", "See hours by job and task", "Drill in or export to Excel"],
  figs=[("labor-hours.webp", 974, 586, "Bar chart of total labor hours by job with a posting-date range selector; job numbers and customers blurred", "Hours by job for the selected dates. Job numbers and customers are blurred.")],
  team=["Project managers and accounting see where the hours went without building a spreadsheet.",
        "Real hours by task are there to check the next estimate against.",
        "A plain-language guide means people use the report correctly."],
  built="Power BI, Dynamics 365 Business Central"),
}

CARDS = [c[:6] + (True,) for c in CARDS]

KIND_LABEL = {"real": "Real-world project", "demo": "Demo company", "own": "My own business"}
KIND_CLASS = {"real": "tag", "demo": "tag green", "own": "tag"}
card_by_slug = {c[0]: c for c in CARDS}
exec(open(os.path.join(HERE, 'pages2.py')).read())

TOOL_CLASS = {"Power Apps": "t-pp", "Power Automate": "t-pp", "Power BI": "t-bi", "SharePoint": "t-sp", "Dynamics 365": "t-d365", "Azure": "t-az"}
def _tags(tools):
    return "".join(f'<li class="{TOOL_CLASS[x]}">{x}</li>' for x in tools)

def _flow(label, steps, cls):
    items = "".join(f'<li>{s}</li>' for s in steps)
    return f'<div class="flow {cls}"><p class="flow-label">{label}</p><ol class="flow-steps">{items}</ol></div>'

# ---------- index ----------
chips = "\n".join(f'            <button type="button" class="chip {TOOL_CLASS[x]}" data-tool="{x}" aria-pressed="false">{x}</button>' for x in TOOLS)
gchips = "\n".join(f'            <button type="button" class="chip" data-group="{gid}" aria-pressed="false">{gname}</button>' for gid, gname in GROUPS)
sections = []
for gid, gname in GROUPS:
    cards = []
    for slug, g, kind, title, summary, tools, has_page in CARDS:
        if g != gid: continue
        inner = (f'<span class="{KIND_CLASS[kind]}">{KIND_LABEL[kind]}</span>'
                 f'<h3>{title}</h3><p>{summary}</p>'
                 f'<ul class="tool-tags" aria-label="Tools used">{_tags(tools)}</ul>')
        if has_page:
            cards.append(f'          <a class="card case-card case-link" href="/case-studies/{slug}.html" data-tools="{"|".join(tools)}">{inner}<span class="read-more">Read the case study</span></a>')
        else:
            cards.append(f'          <div class="card case-card" data-tools="{"|".join(tools)}">{inner}<span class="soon">Write-up coming soon</span></div>')
    sections.append(f'''      <div class="case-group" id="{gid}">
        <h2>{gname}</h2>
        <div class="grid grid-2">
{chr(10).join(cards)}
        </div>
      </div>''')

index_body = f'''    <div class="page-title">
      <div class="wrap">
        <h1>Case Studies</h1>
        <p class="lead">Find the problem that sounds like your office, and see how it was solved.</p>
      </div>
    </div>

    <section class="section-white">
      <div class="wrap">
        <div class="note">
          <p><strong>Real-world projects</strong> were built for, and used at, a working business. <strong>Demo company</strong> projects were built in Lumen Photonics, a sample manufacturer I created in Microsoft 365 to show a complete system end to end. <strong>My own business</strong> projects run Office Tune-Up Consulting itself. Company names, customers and figures are left out or blurred.</p>
        </div>
        <div class="filter" role="group" aria-labelledby="filter-group-label">
          <p id="filter-group-label" class="filter-label">Filter by problem</p>
          <div class="chips">
            <button type="button" class="chip" data-group="all" aria-pressed="true">All problems</button>
{gchips}
          </div>
        </div>
        <div class="filter" role="group" aria-labelledby="filter-tool-label">
          <p id="filter-tool-label" class="filter-label">Filter by tool</p>
          <div class="chips">
            <button type="button" class="chip" data-tool="all" aria-pressed="true">All tools</button>
{chips}
          </div>
        </div>
      </div>
    </section>

    <section class="case-groups">
      <div class="wrap">
{chr(10).join(sections)}
        <p class="no-results" hidden>No case studies match both filters yet. Try another tool or problem.</p>
      </div>
    </section>

{CTA}

  <script>
    (function () {{
      var state = {{ tool: 'all', group: 'all' }};
      var toolChips = document.querySelectorAll('.chip[data-tool]');
      var groupChips = document.querySelectorAll('.chip[data-group]');
      var groups = document.querySelectorAll('.case-group');
      var empty = document.querySelector('.no-results');
      function apply() {{
        toolChips.forEach(function (c) {{ c.setAttribute('aria-pressed', c.dataset.tool === state.tool ? 'true' : 'false'); }});
        groupChips.forEach(function (c) {{ c.setAttribute('aria-pressed', c.dataset.group === state.group ? 'true' : 'false'); }});
        var any = false;
        groups.forEach(function (g) {{
          var groupOk = state.group === 'all' || g.id === state.group;
          var shown = 0;
          g.querySelectorAll('.case-card').forEach(function (card) {{
            var toolOk = state.tool === 'all' || card.dataset.tools.split('|').indexOf(state.tool) !== -1;
            card.hidden = !(groupOk && toolOk);
            if (!card.hidden) shown++;
          }});
          g.hidden = shown === 0;
          if (shown) any = true;
        }});
        empty.hidden = any;
      }}
      toolChips.forEach(function (c) {{ c.addEventListener('click', function () {{ state.tool = c.dataset.tool; apply(); }}); }});
      groupChips.forEach(function (c) {{ c.addEventListener('click', function () {{ state.group = c.dataset.group; apply(); }}); }});
    }})();
  </script>'''
# The script must sit inside <main>; page() puts body inside <main>, which is fine.
page("case-studies.html", "Case Studies", "Office problems and how they were solved: approvals, documents, double entry, field paperwork and late surprises.", index_body, "case-studies.html")

# ---------- individual pages ----------
os.makedirs(os.path.join(out, "case-studies"), exist_ok=True)
for slug, d in PAGES.items():
    _, g, kind, title, summary, tools, _ = card_by_slug[slug]
    gname = dict(GROUPS)[g]
    paras = lambda xs: "\n".join(f"          <p>{x}</p>" for x in xs)
    lis = "\n".join(f"            <li>{x}</li>" for x in d["team"])
    figs = "\n".join(
        f'          <figure class="shot"><img src="/images/case-studies/{s}" width="{w}" height="{h}" alt="{a}" loading="lazy"><figcaption>{c}</figcaption></figure>'
        for s, w, h, a, c in d.get("figs", []))
    if d.get("pair"):
        imgs = "".join(f'<img src="/images/case-studies/{s}" width="{w}" height="{h}" alt="{a}" loading="lazy">' for s, w, h, a in d["pair"])
        figs += f'\n          <figure class="shot shot-pair"><div class="pair">{imgs}</div><figcaption>{d["pair_caption"]}</figcaption></figure>'
    body = f'''    <div class="page-title">
      <div class="wrap case-wrap">
        <p class="crumb"><a href="/case-studies.html">All case studies</a> &rsaquo; {gname}</p>
        <span class="{KIND_CLASS[kind]}">{KIND_LABEL[kind]}</span>
        <h1>{title}</h1>
        <p class="lead">{d["subtitle"]}</p>
      </div>
    </div>

    <section class="section-white">
      <div class="wrap case-wrap">
        <article class="case-page">
          <h2>The situation</h2>
{paras(d["situation"])}
          <h2>What changed</h2>
{paras(d["changed"])}
          <div class="flows">{_flow("Before", d["before"], "flow-before")}{_flow("After", d["after"], "flow-after")}</div>
{figs}
          <h2>What it meant for the team</h2>
          <ul>
{lis}
          </ul>
          <p class="case-tools"><strong>Built with:</strong> {d["built"]}</p>
          <p><a href="/case-studies.html">&larr; Back to all case studies</a></p>
        </article>
      </div>
    </section>

{CTA}'''
    page(f"case-studies/{slug}.html", title, f"{title}: {summary}", body, "case-studies.html")
