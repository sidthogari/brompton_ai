"""Section 1 — Architectural solution for trusted multi-channel attribution."""

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from pathlib import Path

from theme import (
    CARD,
    CLAY,
    CLAY_DEEP,
    CREAM,
    DANGER,
    FONT,
    FONT_LIGHT,
    GOLD,
    INK,
    INK_SOFT,
    LINE,
    MUTED,
    NAVY,
    OK,
    PAPER,
    SAGE,
    SAGE_DEEP,
    SLIDE_H,
    SLIDE_W,
    WHITE,
    add_para,
    add_textbox,
    blank_slide,
    bullet_card,
    card,
    content_chrome,
    fill_shape,
    pill,
    poster_slide,
    rect,
    rrect,
    set_cell,
    set_notes,
    style_table,
    title_block,
)

TOTAL = 18
DIAGRAMS = Path(__file__).resolve().parent / "output" / "diagrams"
SECTION = "Section 1  ·  Architecture"


def _prs():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def slide_title(prs):
    s = blank_slide(prs)
    rect(s, 0, 0, Inches(0.18), SLIDE_H, CLAY)
    rect(s, 0, Inches(6.85), SLIDE_W, Inches(0.65), INK)
    add_textbox(s, Inches(0.7), Inches(1.35), Inches(11.8), Inches(0.35),
                "NOLI  ·  DATA ENGINEER BUSINESS CASE  ·  SECTION 1",
                size=13, bold=True, color=CLAY)
    add_textbox(s, Inches(0.7), Inches(1.85), Inches(12), Inches(1.6),
                "A trusted attribution\narchitecture",
                size=40, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(3.7), Inches(11.5), Inches(1.1),
                "End-to-end design from paid and owned channels to a single,\n"
                "governed number — using a multi-tool stack, not a single vendor.",
                size=18, color=INK_SOFT, font=FONT_LIGHT)
    add_textbox(s, Inches(0.7), Inches(5.15), Inches(11.5), Inches(0.7),
                "Audience: Senior Data Engineer  ·  Principal Engineer     15 minutes\n"
                "Stack: Fivetran · Databricks / Delta · Unity Catalog · Snowflake · dbt · Airflow · Power BI",
                size=14, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(6.98), Inches(12), Inches(0.4),
                "Sidhartha Thogari   ·   Data Engineer interview",
                size=13, color=WHITE)
    set_notes(s,
        "Open by framing the outcome, not the tools: marketing cannot reconcile Meta, Google Ads, "
        "and Email because we do not have one grain, one identity, one attribution model, or one "
        "place where business logic lives.\n\n"
        "Tell them you will not pitch a single-vendor lakehouse. Noli's JD and Azure estate point "
        "to a modern data stack. Each tool has a job. The risk is overlap — Fivetran transforms, "
        "dbt models, Databricks notebooks, and Power BI measures all inventing 'revenue' or "
        "'attributed orders' differently.\n\n"
        "Promise: by the end they will see ingestion → model → QA → BI, where logic sits, how we "
        "scale to TBs/day, and the honest downsides of the stack.\n\nTime: 30 seconds.")


def slide_agenda(prs):
    s = blank_slide(prs)
    content_chrome(s, "How we will use 15 minutes", 2, TOTAL, SECTION)
    title_block(s, "The brief, answered in order")
    items = [
        ("01", "Diagnose", "Why Meta, Google Ads and Email cannot agree — grain, identity, windows, UTMs, vendor claim."),
        ("02", "Architecture", "ELT path from sources to Power BI. Medallion + a restricted hash / PII store."),
        ("03", "Stack trade-offs", "Fivetran, Databricks, Delta / Unity Catalog, Snowflake, dbt, Airflow, Power BI — why and downside."),
        ("04", "Model & logic", "Canonical attribution model. Logic in the warehouse, never in the BI tool."),
        ("05", "Trust at scale", "Contracts, tests, freshness, reconciliation. Incremental design for TBs/day."),
    ]
    for i, (n, t, b) in enumerate(items):
        top = Inches(1.35 + i * 1.05)
        rrect(s, Inches(0.45), top, Inches(12.4), Inches(0.95), CARD, LINE, 1.0, 0.06)
        rrect(s, Inches(0.62), top + Inches(0.22), Inches(0.7), Inches(0.5), CLAY, adj=0.15)
        add_textbox(s, Inches(0.62), top + Inches(0.28), Inches(0.7), Inches(0.4),
                    n, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(s, Inches(1.55), top + Inches(0.16), Inches(10.9), Inches(0.32),
                    t, size=16, bold=True, color=INK)
        add_textbox(s, Inches(1.55), top + Inches(0.48), Inches(10.9), Inches(0.38),
                    b, size=13, color=INK_SOFT)
    set_notes(s,
        "Do not linger. This is a map so the Principal can interrupt later without you losing the thread.\n\n"
        "Call out that Section 2 reuses this architecture for finance self-service — we are not "
        "designing two platforms.\n\nTime: 45 seconds.")


def slide_problem(prs):
    s = blank_slide(prs)
    content_chrome(s, "Problem statement", 3, TOTAL, SECTION)
    title_block(s, "Marketing does not have a number. It has three stories.",
                "Inconsistent attribution across Meta, Google Ads and Email. UTMs on URLs are missing or malformed.")
    pains = [
        ("Vendor-claimed conversions", "Meta and Google both take credit for the same order. Email tools report 'revenue' on last click to a newsletter."),
        ("Broken campaign contract", "utm_source = fb / Facebook / meta / ig / paid_social. Same campaign, four keys. Sometimes no UTM at all."),
        ("Unstable grain", "One report is sessions. One is users. One is orders. One is clicks. None are labelled."),
        ("Logic in the last mile", "Analysts fix mismatches in Power BI or Excel. Tomorrow the patch is a different number."),
    ]
    for i, (t, b) in enumerate(pains):
        col = i % 2
        row = i // 2
        card(s, Inches(0.45 + col * 6.4), Inches(1.85 + row * 2.15), Inches(6.2), Inches(2.0),
             t, b, accent=CLAY if i < 2 else GOLD, title_size=15, body_size=13)
    set_notes(s,
        "Read the problem the way a Principal would: this is not a connector outage. It is a "
        "semantics and contract failure.\n\n"
        "Noli-specific colour: paid social and email drive a beauty marketplace with quizzes, "
        "face-scan diagnostics and first-party profiles. Identity is messy (anonymous scan → "
        "account → order). Skin and email data are GDPR-sensitive — we cannot 'just join on email' "
        "in a BI dataset.\n\n"
        "The data team getting 'why doesn't this match' tickets is the symptom of no canonical "
        "fct_attribution and no reconciliation to vendor exports.\n\nTime: 1 minute.")


def slide_root_causes(prs):
    s = blank_slide(prs)
    content_chrome(s, "Engineering diagnosis", 4, TOTAL, SECTION)
    title_block(s, "Five reasons the numbers diverge — before we pick tools")
    rows = [
        ("Identity", "Cookie, email, customer_id, device. Logged-out quiz vs logged-in checkout. No stitch → double count or drop."),
        ("Attribution window & model", "1-day click vs 7-day click vs 28-day view. Last-click vs linear vs platform data-driven. Must be explicit columns, not opinions."),
        ("Event vs commercial grain", "Clicks and sessions are not orders. Refunds, cancellations and partial returns change 'attributed revenue' after the fact."),
        ("UTM + landing hygiene", "Missing, mixed case, aliases, leftover internal params. Paid landing pages without a tagging standard."),
        ("Two sources of truth", "Platform UI (Meta Ads Manager) vs warehouse. If we hide the vendor number, trust dies. If we mix it into the KPI, trust dies."),
    ]
    for i, (t, b) in enumerate(rows):
        top = Inches(1.32 + i * 1.08)
        rrect(s, Inches(0.45), top, Inches(12.4), Inches(0.98), CARD, LINE, 1.0, 0.05)
        rrect(s, Inches(0.62), top + Inches(0.24), Inches(2.35), Inches(0.5), PAPER, adj=0.2)
        add_textbox(s, Inches(0.62), top + Inches(0.30), Inches(2.35), Inches(0.4),
                    t, size=13, bold=True, color=CLAY_DEEP, align=PP_ALIGN.CENTER)
        add_textbox(s, Inches(3.15), top + Inches(0.22), Inches(9.4), Inches(0.6),
                    b, size=13, color=INK_SOFT)
    set_notes(s,
        "This is the slide that shows you think like a Senior DE. Tools do not fix a last-click "
        "dashboard compared to Meta's 7-day click / 1-day view default.\n\n"
        "Principle: publish multiple models side by side (last_click, first_click, linear, "
        "position_based) and a separate vendor_claimed fact for reconciliation. Default executive "
        "KPI is last non-direct click, 7-day, order grain, net of refunds — written down.\n\n"
        "If asked 'which model is right?': there is no right model. There is a signed-off default "
        "and transparent alternatives.\n\nTime: 1.5 minutes.")


def slide_principles(prs):
    s = blank_slide(prs)
    content_chrome(s, "Design principles", 5, TOTAL, SECTION)
    title_block(s, "How I would improve trust — before drawing boxes")
    items = [
        ("ELT, not ETL soup", "Land immutable raw payloads. Transform in the warehouse with tested SQL. Hash PII on the way in so raw email is not a free-for-all."),
        ("One grain, many models", "Order-level attribution is the commercial grain. Touchpoints stay at event grain. Models are columns or a model_name key — not competing dashboards."),
        ("Logic lives once", "dbt (and a thin Python layer for hashing / identity). Not Fivetran pre-build transforms. Not Power BI measures that redefine net revenue."),
        ("Contract the tags", "Campaign naming + UTM dictionary + validation at the edge. Warehouse maps aliases; marketing owns the standard."),
        ("Reconcile, don't hide", "Vendor-claimed vs canonical. Freshness, volume, null-UTM rate. Tickets become dashboards."),
        ("Privacy by construction", "Hashed keys in Gold. Restricted mapping store. Consent flags. RTBF. Clean-room-ready shares for partners."),
    ]
    for i, (t, b) in enumerate(items):
        col = i % 3
        row = i // 3
        card(s, Inches(0.45 + col * 4.25), Inches(1.4 + row * 2.55), Inches(4.1), Inches(2.4),
             t, b, accent=SAGE if i % 2 else CLAY, title_size=14, body_size=12)
    set_notes(s,
        "These six principles are the 'why' behind every tool choice on the next slides.\n\n"
        "If challenged on ELT: classic ETL would clean UTMs in ADF/Fivetran and lose the raw "
        "evidence when marketing asks 'what did Meta actually send?'. We keep Bronze raw.\n\n"
        "Exception to pure ELT: irreversible hash of email/phone as early as possible, pepper "
        "from Key Vault, mapping table locked down. That is privacy-preserving ingest — still ELT "
        "for business logic.\n\nTime: 1 minute.")


def slide_architecture(prs):
    s = blank_slide(prs)
    content_chrome(s, "End-to-end architecture", 6, TOTAL, SECTION)
    title_block(s, "Sources  →  ingest  →  lakehouse / warehouse  →  governed Gold  →  BI",
                "Azure. Multi-tool. Airflow is the conductor — not a second transformation engine.")

    # Column headers
    cols = [
        (0.40, 2.05, "Sources", CLAY),
        (2.55, 2.35, "Ingest", GOLD),
        (5.00, 3.55, "Process & model", SAGE),
        (8.65, 2.15, "Serve", NAVY),
        (10.90, 2.05, "Consume", CLAY_DEEP),
    ]
    for x, w, name, col in cols:
        add_textbox(s, Inches(x), Inches(1.28), Inches(w), Inches(0.28),
                    name.upper(), size=11, bold=True, color=col, align=PP_ALIGN.CENTER)

    def box(x, y, w, h, title, lines, fill=CARD, accent=INK):
        rrect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, LINE, 1.0, 0.08)
        add_textbox(s, Inches(x + 0.08), Inches(y + 0.06), Inches(w - 0.14), Inches(0.26),
                    title, size=11, bold=True, color=accent)
        add_textbox(s, Inches(x + 0.08), Inches(y + 0.30), Inches(w - 0.14), Inches(h - 0.36),
                    lines, size=10, color=INK_SOFT)

    box(0.40, 1.60, 2.05, 1.15, "Paid", "Meta Ads\nGoogle Ads", PAPER, CLAY)
    box(0.40, 2.85, 2.05, 1.15, "Owned", "Email / CRM\n(Klaviyo etc.)", PAPER, CLAY)
    box(0.40, 4.10, 2.05, 1.35, "Site & commerce", "GA4 / pixel\nOrders, refunds\nConsent / CMP", PAPER, CLAY)

    box(2.55, 1.60, 2.35, 1.55, "Fivetran", "Managed SaaS CDC\nMeta, Google, email,\ncommerce, GA4 export", CARD, GOLD)
    box(2.55, 3.25, 2.35, 1.15, "Events / files", "Auto Loader / APIs\nfor pixel + exceptions", CARD, GOLD)
    box(2.55, 4.50, 2.35, 0.95, "Airflow", "Sync → hash → dbt\n→ tests → refresh", CARD, GOLD)

    box(5.00, 1.60, 3.55, 1.35, "Bronze  ·  Delta / Snowflake RAW", "Immutable JSON/tables  ·  schema evolution\nAudit cols  ·  Fivetran metadata", CARD, SAGE)
    box(5.00, 3.05, 3.55, 1.20, "Silver  ·  dbt + Databricks Python", "UTM map  ·  identity stitch\nHash PII  ·  SCD2 campaigns", CARD, SAGE)
    box(5.00, 4.35, 3.55, 1.10, "Gold  ·  dbt marts", "fct_touchpoint  ·  fct_order\nfct_attribution  ·  dim_*", CARD, SAGE)

    box(8.65, 1.60, 2.15, 1.45, "Snowflake", "Serving + shares\nClean rooms", CARD, NAVY)
    box(8.65, 3.15, 2.15, 1.20, "Unity Catalog\n+ Snowflake RBAC", "Lineage, masks\nRow filters", CARD, NAVY)
    box(8.65, 4.45, 2.15, 1.00, "PII vault", "Hash map\nDE-only", CARD, DANGER)

    box(10.90, 1.60, 2.05, 1.20, "Power BI", "Certified\nsemantic model", CARD, CLAY_DEEP)
    box(10.90, 2.90, 2.05, 1.15, "dbt docs", "Metrics &\nexposures", CARD, CLAY_DEEP)
    box(10.90, 4.15, 2.05, 1.30, "AI / ML", "Feature tables\nGenie / models", CARD, CLAY_DEEP)

    add_textbox(s, Inches(0.45), Inches(5.65), Inches(12.4), Inches(0.55),
                "Across the top: Entra ID · Key Vault (hash pepper) · Unity Catalog + Snowflake policies · Airflow SLAs · cost/freshness alerts. Reverse ETL later — after identity is clean.",
                size=12, color=INK_SOFT)
    set_notes(s,
        "Walk left to right in 90 seconds.\n\n"
        "Fivetran lands paid/owned/commerce. Databricks + Delta for heavy Python (UTM parse, "
        "identity graph, hashing) and TB-scale semi-structured. dbt is the modelling contract on "
        "Snowflake (and/or Databricks SQL). Airflow sequences Fivetran, Databricks jobs, dbt, "
        "tests, Power BI refresh.\n\n"
        "If they are Snowflake-only today: Bronze can be Snowflake RAW, Python via Snowpark or a "
        "thin Databricks job. If they are lakehouse-first: Databricks SQL serves Gold. The model "
        "does not change.\n\n"
        "Call out the red PII vault — we keep hashing. Gold never carries raw email.\n\n"
        "Clean rooms sit on Snowflake or Databricks Clean Rooms — matches the JD example project.\n\n"
        "Time: 2 minutes.")


def slide_platform_poster(prs):
    poster_slide(
        prs,
        DIAGRAMS / "noli_platform_architecture.png",
        "This is the Brompton-style poster. Spend 90 seconds walking left to right.\n\n"
        "Top bar = platform services. Sources → Fivetran/events → medallion + hash vault → "
        "Snowflake serve → Power BI/Excel. Right rail is how we operate it.\n\n"
        "Point at the red PII vault. Point at Gold as the only place Power BI is allowed.\n\n"
        "If they say 'this looks like Brompton': same craft (medallion, hash, RTBF, Unity Catalog), "
        "fitted to Noli's JD stack — Fivetran, dbt, Snowflake, Airflow — not a Databricks-only copy.\n\n"
        "Time: 1.5 minutes. If short on time, this slide replaces the previous box diagram.",
    )


def slide_medallion_poster(prs):
    poster_slide(
        prs,
        DIAGRAMS / "noli_medallion_logic.png",
        "Five columns: Bronze, hash gate, Silver, Gold, PII vault. Then the lane rules.\n\n"
        "The footer line is the soundbite: money/credit → dbt. Visual → Power BI. "
        "Identifier → hash/consent.\n\nTime: 1 minute.",
    )


def slide_stack(prs):
    s = blank_slide(prs)
    content_chrome(s, "Why this stack — and why not one platform", 9, TOTAL, SECTION)
    title_block(s, "Technology  ·  Why  ·  Downside",
                "I would not rip-and-replace Noli's modern data stack. I would stop tools from overlapping.")

    headers = ["Technology", "Why it earns a place", "Downside I would manage"]
    rows = [
        ["Fivetran", "Managed, reliable connectors for Meta, Google Ads, email, GA4, commerce. Fast time-to-Bronze. Ops-light incremental sync.", "Cost at volume. Vendor dependency. Weak as a transform layer — keep it extract + load."],
        ["Databricks", "Python/Spark for UTM parsing, identity, PII hashing, TB-scale semi-structured, ML feature tables for AI enablement.", "Needs engineering and tuning. Job-cluster cost if left on. Do not re-implement dbt models in notebooks."],
        ["Delta + Unity Catalog", "ACID, time travel, schema evolution, lineage, RBAC, column masks. Auditability when attribution is challenged.", "Platform complexity. Governance only works if we actually register tables and stop ad-hoc personal schemas."],
        ["Snowflake", "JD-aligned serving warehouse. BI-friendly, sharing and clean rooms with brands / L'Oréal-class partners.", "Another compute bill if we also run Databricks. Decide a system of record for Gold — I pick Snowflake for finance & marketing KPIs."],
        ["dbt", "SQL models, tests, docs, contracts, exposures. The only place 'attributed_revenue' is defined.", "Overlap if Fivetran transformations or Power BI DAX duplicate the same logic. Discipline required."],
        ["Airflow", "Cross-platform orchestration: Fivetran sync → hash job → dbt → quality gates → Power BI refresh. Sensors and retries.", "Operational overhead. Treat DAGs as product: SLAs, alerts, no hidden cron on the side."],
        ["Power BI", "How the business already consumes. Import/DirectQuery on Gold only. Analyze in Excel on the certified model.", "Logic duplication if measures redefine net revenue or last-click. Dashboards are views, not the model."],
    ]

    table = s.shapes.add_table(8, 3, Inches(0.4), Inches(1.38), Inches(12.5), Inches(5.55)).table
    table.columns[0].width = Inches(2.15)
    table.columns[1].width = Inches(5.25)
    table.columns[2].width = Inches(5.10)
    for c, h in enumerate(headers):
        set_cell(table, 0, c, h, bold=True)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            set_cell(table, r, c, val, bold=(c == 0))
    style_table(table)
    # Bold first column after style
    for r in range(1, 8):
        cell = table.cell(r, 0)
        for p in cell.text_frame.paragraphs:
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = CLAY_DEEP
    set_notes(s,
        "This is the slide they asked for. Spend time here.\n\n"
        "Narrative: Fivetran = ingest. Databricks = hard Python + scale. Delta/UC = reliability "
        "and governance. Snowflake = serve + clean rooms. dbt = meaning. Airflow = time. "
        "Power BI = consumption.\n\n"
        "The failure mode is duplication: Fivetran transform + dbt + notebook + DAX = four "
        "definitions of revenue.\n\n"
        "If they ask 'why both Snowflake and Databricks?': I would not stand up both greenfield "
        "without a reason. Noli JD lists Snowflake; Azure + AI work lists Databricks-class "
        "processing. My rule: one Gold system of record (Snowflake). Databricks is justified for "
        "hashing, identity, streaming-ish events, and AI feature tables — not a second mart.\n\n"
        "If they are Databricks-only, Unity Catalog + Databricks SQL replaces Snowflake serving; "
        "clean rooms become Databricks Clean Rooms. Principles stay.\n\nTime: 2.5 minutes.")


def slide_no_overlap(prs):
    s = blank_slide(prs)
    content_chrome(s, "Guardrails so the stack does not fight itself", 10, TOTAL, SECTION)
    title_block(s, "Each tool has a lane. Crossing lanes is how trust dies.")

    lanes = [
        (CLAY, "Fivetran", "Does", "Extract + load, schema drift handling, incremental cursors.",
         "Does not", "Business rules, UTM meaning, attribution, net revenue."),
        (GOLD, "Databricks", "Does", "Hash, identity graph, ugly JSON, heavy Python, feature tables.",
         "Does not", "Certified finance/marketing marts that analysts query."),
        (SAGE, "dbt", "Does", "Silver/Gold SQL, tests, docs, metric names, SCD2, incremental models.",
         "Does not", "Orchestrate Fivetran or replace Airflow SLAs."),
        (NAVY, "Airflow", "Does", "Order of operations, retries, sensors, freshness SLAs, paging.",
         "Does not", "Contain SELECT logic that belongs in dbt."),
        (CLAY_DEEP, "Power BI", "Does", "Visuals, RLS, certified dataset, Excel live connection.",
         "Does not", "Join raw Fivetran tables or invent attribution windows."),
        (DANGER, "PII / hash", "Does", "Peppered hash, mapping table, RTBF, secure views.",
         "Does not", "Live in Gold facts or get exported to Excel."),
    ]
    for i, (col, name, a, ad, b, bd) in enumerate(lanes):
        x = 0.4 + (i % 3) * 4.3
        y = 1.38 + (i // 3) * 2.7
        rrect(s, Inches(x), Inches(y), Inches(4.15), Inches(2.52), CARD, LINE, 1.0, 0.06)
        rect(s, Inches(x), Inches(y), Inches(4.15), Inches(0.42), col)
        add_textbox(s, Inches(x + 0.15), Inches(y + 0.06), Inches(3.85), Inches(0.32),
                    name, size=14, bold=True, color=WHITE)
        add_textbox(s, Inches(x + 0.15), Inches(y + 0.52), Inches(3.85), Inches(0.24),
                    a.upper(), size=10, bold=True, color=OK)
        add_textbox(s, Inches(x + 0.15), Inches(y + 0.74), Inches(3.85), Inches(0.7),
                    ad, size=12, color=INK_SOFT)
        add_textbox(s, Inches(x + 0.15), Inches(y + 1.42), Inches(3.85), Inches(0.24),
                    b.upper(), size=10, bold=True, color=DANGER)
        add_textbox(s, Inches(x + 0.15), Inches(y + 1.64), Inches(3.85), Inches(0.7),
                    bd, size=12, color=INK_SOFT)
    set_notes(s,
        "This is how you answer 'isn't this too many tools?' — yes, if they overlap. No, if each "
        "has a hard boundary.\n\n"
        "dbt on Databricks SQL or dbt on Snowflake — pick one adapter for Gold. I would not run "
        "two parallel dbt projects for the same mart.\n\nTime: 1 minute.")


def slide_elt(prs):
    s = blank_slide(prs)
    content_chrome(s, "ETL vs ELT  ·  where logic lives", 11, TOTAL, SECTION)
    title_block(s, "ELT for meaning. A thin 'E-hash-L' for privacy.")

    # Two columns
    rrect(s, Inches(0.45), Inches(1.4), Inches(6.2), Inches(3.55), CARD, LINE, 1.0, 0.05)
    add_textbox(s, Inches(0.7), Inches(1.55), Inches(5.8), Inches(0.35),
                "What I would not do  ·  ETL-heavy", size=16, bold=True, color=DANGER)
    bullets = [
        "Clean UTMs inside Fivetran or ADF and drop the raw payload.",
        "Apply last-click in the ingestion job — you cannot replay a new model.",
        "Join orders to ad spend in Power BI on raw tables.",
        "Hash in a BI calculated column (or not at all).",
        "Let each dashboard pick its own attribution window.",
    ]
    box = s.shapes.add_textbox(Inches(0.7), Inches(2.05), Inches(5.7), Inches(2.7))
    tf = box.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        run = p.add_run()
        run.text = "–  " + b
        from theme import _set_run
        _set_run(run, 13, False, INK_SOFT, FONT)

    rrect(s, Inches(6.85), Inches(1.4), Inches(6.05), Inches(3.55), CARD, LINE, 1.0, 0.05)
    add_textbox(s, Inches(7.1), Inches(1.55), Inches(5.6), Inches(0.35),
                "What I would do  ·  ELT + hash", size=16, bold=True, color=OK)
    bullets2 = [
        "Bronze = exact source extract (plus Fivetran metadata).",
        "Hash email/phone in a locked Databricks job before wide access.",
        "Silver = parse, alias map, identity, SCD2, quality flags.",
        "Gold = facts/dims + attribution models as data, not DAX.",
        "Power BI = thin measures (sum, distinct count) on Gold.",
    ]
    box = s.shapes.add_textbox(Inches(7.1), Inches(2.05), Inches(5.55), Inches(2.7))
    tf = box.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets2):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        run = p.add_run()
        run.text = "–  " + b
        _set_run(run, 13, False, INK_SOFT, FONT)

    rrect(s, Inches(0.45), Inches(5.1), Inches(12.45), Inches(1.85), PAPER, LINE, 1.0, 0.05)
    add_textbox(s, Inches(0.7), Inches(5.22), Inches(12), Inches(0.3),
                "Decision rule I would defend in the room", size=14, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(5.55), Inches(12), Inches(1.2),
                "If a rule changes how money or credit is calculated, it belongs in dbt with a test and an owner.\n"
                "If a rule is visual (colour, chart grain), it belongs in Power BI.\n"
                "If a rule is 'can we store this identifier at all?', it belongs in the hash / consent path — not in a mart PR.",
                size=14, color=INK_SOFT)
    set_notes(s,
        "Senior/Principal bait: 'why not transform in Fivetran to keep dbt thin?' Because we lose "
        "replay, tests, and lineage. Fivetran transformations are fine for tiny type casts, not "
        "attribution.\n\n"
        "'Why not dbt Python everywhere?' Because SQL models are reviewable by analytics engineers "
        "and documented. Python is for hashing, fuzzy identity, and nested payloads.\n\n"
        "Time: 1.5 minutes.")


def slide_ingestion(prs):
    s = blank_slide(prs)
    content_chrome(s, "Ingestion and the UTM contract", 12, TOTAL, SECTION)
    title_block(s, "Stabilise the pipeline at the edge — then map what you cannot block")

    bullet_card(s, Inches(0.45), Inches(1.4), Inches(6.2), Inches(3.35),
                "Ingestion design",
                [
                    "Fivetran for Meta, Google Ads, email, commerce, GA4 BigQuery export if present.",
                    "Incremental / CDC. No nightly full dumps as the default.",
                    "Landing: RAW schema, Fivetran naming, _fivetran_synced, _fivetran_deleted.",
                    "Pixel / webhooks / messy files: Databricks Auto Loader or a small API job.",
                    "Airflow sensor: do not run dbt until sync freshness clears the SLA.",
                    "Backfills are first-class DAGs, not a laptop notebook.",
                ], CLAY)
    bullet_card(s, Inches(6.85), Inches(1.4), Inches(6.05), Inches(3.35),
                "Campaign tagging contract",
                [
                    "Written standard: utm_source / medium / campaign / content / term.",
                    "Allowed values + aliases table (fb → meta, ig → meta, paid-social → paid_social).",
                    "CI-ish check: weekly invalid-UTM report to marketing, not only engineering.",
                    "Paid landing URLs generated from a tool, not typed in Ads Manager.",
                    "Missing UTM → channel = 'unspecified', never silently 'direct'.",
                    "Internal traffic and staff orders flagged, not deleted.",
                ], GOLD)

    rrect(s, Inches(0.45), Inches(4.9), Inches(12.45), Inches(2.05), CARD, LINE, 1.0, 0.05)
    add_textbox(s, Inches(0.7), Inches(5.05), Inches(12), Inches(0.3),
                "Silver normalisation (dbt) — example grain of the contract", size=14, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(5.4), Inches(12), Inches(1.35),
                "utm_source_raw → utm_source_norm  ·  channel_group (paid_social / paid_search / email / organic / direct / unspecified)\n"
                "campaign_key = hash(source_norm, campaign_norm, account_id)  ·  dim_campaign SCD2 for name changes\n"
                "is_valid_utm  ·  is_internal  ·  consent_analytics  ·  event_ts_utc (one timezone, always)\n"
                "Semi-structured: VARIANT/JSON parsed to typed columns; unknown keys kept in a payload map for replay.",
                size=13, color=INK_SOFT)
    set_notes(s,
        "Stabilising the pipeline is half engineering, half operating model with marketing.\n\n"
        "You cannot regex your way out of five teams naming campaigns differently. The alias "
        "table is a product. The unspecified bucket is visible on the exec dashboard so tagging "
        "debt has a number.\n\n"
        "GA4: prefer BigQuery export via Fivetran or native, not UI-sampled reports.\n\n"
        "Meta/Google spend lands at campaign/ad-set grain; clicks/impressions must not be inner-"
        "joined to orders without a date spine or you will drop zero-conversion spend.\n\n"
        "Time: 1.5 minutes.")


def slide_model(prs):
    s = blank_slide(prs)
    content_chrome(s, "Data modelling", 13, TOTAL, SECTION)
    title_block(s, "Commercial grain is the order. Credit is a table, not a vibe.")

    # Facts / dims
    models = [
        ("dim_date", "Standard date role-playing: order_date, click_date, refund_date."),
        ("dim_channel", "Paid social, paid search, email, organic, direct, unspecified, internal."),
        ("dim_campaign", "SCD2. Natural key from platform IDs + normalised UTM campaign."),
        ("dim_customer", "Hashed customer_sk only. No email. Consent flags as attributes."),
        ("fct_touchpoint", "One row per impression/click/email-event. Timestamp, campaign_sk, customer_sk, session_id."),
        ("fct_order", "One row per order. Gross, discount, tax, shipping, net, status, refunded_at."),
        ("fct_attribution", "order_id × model_name. channel_sk, campaign_sk, attributed_revenue, attributed_weight."),
        ("fct_vendor_claimed", "What Meta/Google/Email reported. For reconciliation only — never mixed into the KPI."),
    ]
    for i, (n, b) in enumerate(models):
        col = i % 4
        row = i // 4
        x = 0.45 + col * 3.2
        y = 1.38 + row * 2.15
        rrect(s, Inches(x), Inches(y), Inches(3.05), Inches(2.0), CARD, LINE, 1.0, 0.07)
        rect(s, Inches(x), Inches(y), Inches(3.05), Inches(0.08), SAGE if "fct" in n else CLAY)
        add_textbox(s, Inches(x + 0.12), Inches(y + 0.18), Inches(2.8), Inches(0.4),
                    n, size=13, bold=True, color=CLAY_DEEP if "fct" in n else INK)
        add_textbox(s, Inches(x + 0.12), Inches(y + 0.6), Inches(2.8), Inches(1.25),
                    b, size=12, color=INK_SOFT)
    set_notes(s,
        "Walk fct_attribution: this is how we stop dashboard wars. model_name in "
        "{last_non_direct_click, first_click, linear, position_based}. Default filter in the "
        "certified dataset is last_non_direct_click, 7-day lookback, net revenue after refunds.\n\n"
        "Weight sums to 1 per order per model so we can prove conservation: "
        "sum(attributed_revenue) = sum(order net) for that model.\n\n"
        "Identity: probabilistic stitch is a later phase. Phase 1 is deterministic (customer_id, "
        "hashed email, order email). Do not oversell a graph on day one.\n\n"
        "Spend: fct_ad_spend daily by campaign so ROAS = attributed_revenue / spend, same grain.\n\n"
        "Time: 1.5 minutes.")


def slide_privacy(prs):
    s = blank_slide(prs)
    content_chrome(s, "Privacy, hashing, GDPR, clean rooms", 14, TOTAL, SECTION)
    title_block(s, "Keep the hash. Gold never sees raw email.")

    cards = [
        (CLAY, "How we hash",
         "SHA-256(normalised_identifier + pepper). Pepper in Azure Key Vault, not in git. Normalise email (trim, lower) before hash so 'A@B' and 'a@b' collide correctly. Phone in E.164."),
        (SAGE, "PII store",
         "Restricted schema: map_hash (raw → hash), access DE + DPO only. Unity Catalog / Snowflake masks. Secure views for analytics. No SELECT * grants on Bronze PII columns."),
        (NAVY, "RTBF & consent",
         "Right to be forgotten: delete/suppress mapping + tombstone hash in facts (keep financial history aggregated). Consent from CMP joined before activation or detailed profiling. Special-category risk: skin/quiz data stays out of marketing marts."),
        (GOLD, "Clean rooms",
         "JD project. Share hashed or aggregated keys with brand partners — not emails. Snowflake clean rooms or Databricks Clean Rooms. Purpose limitation in the share contract. Audit every query."),
    ]
    for i, (col, t, b) in enumerate(cards):
        card(s, Inches(0.45 + (i % 2) * 6.4), Inches(1.4 + (i // 2) * 2.55),
             Inches(6.2), Inches(2.4), t, b, accent=col, title_size=16, body_size=13)
    set_notes(s,
        "Noli collects face scans, quizzes, emails. Treat this as privacy-first, not a bolt-on.\n\n"
        "Be precise: hashing is not anonymisation if the mapping table exists — it is "
        "pseudonymisation (GDPR). That is fine if the map is locked and we document it.\n\n"
        "Do not claim 'encrypted PII in Bronze' unless we actually encrypt columns. I hash for "
        "join keys and restrict raw columns. Encryption at rest is platform default (ADLS/Snowflake).\n\n"
        "Clean room: this is how you mention L'Oréal/partner sharing without sounding reckless.\n\n"
        "Time: 1 minute.")


def slide_quality(prs):
    s = blank_slide(prs)
    content_chrome(s, "Quality assurance", 15, TOTAL, SECTION)
    title_block(s, "Trust is a pipeline with gates — not a Slack thread")

    layers = [
        ("Contract tests", "dbt",
         "unique + not_null on order_id, touchpoint_id\nrelationships to dims\naccepted_values on channel_group, model_name\nconservation: attr revenue = net revenue per model"),
        ("Freshness & volume", "Airflow + dbt source freshness",
         "Fivetran synced_at vs SLA (e.g. Meta < 2h)\nRow-count z-score vs 14-day baseline\nZero-row is a fail, not a green empty table"),
        ("Semantic QA", "Recon mart",
         "Vendor claimed vs canonical (tolerance band)\nUnspecified UTM %\nRefund lag: attributed revenue restated\nDirect-share of last-click (sanity)"),
        ("Observability", "Alerts",
         "Pager on SLA miss and conservation break\nDashboard: pipeline, DBU/credit, queue time\ndbt exposures so a failed model emails the dashboard owner"),
    ]
    for i, (t, tag, b) in enumerate(layers):
        x = 0.45 + i * 3.2
        rrect(s, Inches(x), Inches(1.4), Inches(3.05), Inches(4.0), CARD, LINE, 1.0, 0.06)
        rect(s, Inches(x), Inches(1.4), Inches(3.05), Inches(0.1), CLAY if i % 2 == 0 else SAGE)
        add_textbox(s, Inches(x + 0.15), Inches(1.6), Inches(2.75), Inches(0.55),
                    t, size=15, bold=True, color=INK)
        pill(s, Inches(x + 0.15), Inches(2.2), Inches(2.75), Inches(0.32), tag, PAPER, CLAY_DEEP, 10)
        add_textbox(s, Inches(x + 0.15), Inches(2.7), Inches(2.75), Inches(2.5),
                    b, size=12, color=INK_SOFT)
    set_notes(s,
        "Principal-level: tests that only check not_null are table stakes. The interesting test is "
        "conservation of revenue across attribution weights, and reconciling vendor claimed vs us.\n\n"
        "Schema drift: Fivetran will add columns. dbt sources should not SELECT *. Bronze can "
        "evolve; Silver is typed.\n\n"
        "I would rather fail the Gold refresh and serve yesterday's certified numbers than publish "
        "a broken attribution table. Airflow short-circuit.\n\n"
        "Time: 1.5 minutes.")


def slide_scale(prs):
    s = blank_slide(prs)
    content_chrome(s, "Scaling to TBs per day", 16, TOTAL, SECTION)
    title_block(s, "TBs/day is an incremental design problem, not a bigger cluster")

    items = [
        ("Partition / cluster", "Event and order tables clustered on event_date (and channel where it pays). Never let Power BI scan Bronze."),
        ("Incremental everything", "Fivetran cursors. dbt incremental + unique_key. Databricks Auto Loader checkpoints. No full rebuild of touchpoints."),
        ("Separate compute", "Transform warehouse/job cluster ≠ BI warehouse. Finance refresh cannot queue behind a 4TB backfill."),
        ("Semi-structured discipline", "Parse once in Silver. Gold is typed. Keep raw VARIANT only in Bronze for replay."),
        ("Photon / result cache", "Databricks Photon or Snowflake result cache + clustering for the certified mart. Pre-aggregate daily ROAS."),
        ("Cost guardrails", "Auto-suspend. Airflow pool limits. Budget alerts on Fivetran MAR and warehouse credits/DBUs. Prune Fivetran tables we do not model."),
    ]
    for i, (t, b) in enumerate(items):
        col = i % 3
        row = i // 3
        card(s, Inches(0.45 + col * 4.25), Inches(1.4 + row * 2.55), Inches(4.1), Inches(2.4),
             t, b, accent=SAGE if row else CLAY, title_size=15, body_size=13)
    set_notes(s,
        "Noli may not be at TBs/day yet. Design as if clickstream + GA4 + ad insights will get "
        "there. Show you can scale without premature Kafka-everywhere.\n\n"
        "If they push streaming: marketing attribution is rarely sub-minute. Hourly or "
        "micro-batch is enough. Streaming is justified for onsite tracking quality (JD: traffic "
        "analysis), not for finance-grade attribution.\n\n"
        "Backfill strategy: replay Bronze through the same dbt models with a date window. Time "
        "travel on Delta/Snowflake to debug.\n\n"
        "Time: 1 minute.")


def slide_plan(prs):
    s = blank_slide(prs)
    content_chrome(s, "90-day plan and success", 17, TOTAL, SECTION)
    title_block(s, "Ship trust in slices — do not boil the lake")

    phases = [
        ("Days 1–30  ·  Stabilise", CLAY,
         "Inventory current dashboards and definitions.\n"
         "Fivetran → RAW for Meta, Google, email, orders.\n"
         "UTM alias table + unspecified KPI.\n"
         "Hash path + PII grants locked.\n"
         "Stop new Power BI models on raw tables."),
        ("Days 31–60  ·  Canonical model", SAGE,
         "dbt Silver/Gold: orders, touchpoints, last-click v1.\n"
         "Conservation tests + freshness SLAs.\n"
         "Certified Power BI dataset, one default model.\n"
         "Vendor-claimed recon dashboard.\n"
         "Airflow DAG replaces hidden refresh jobs."),
        ("Days 61–90  ·  Scale & share", NAVY,
         "Add linear / position-based models.\n"
         "Daily spend + ROAS mart.\n"
         "Identity v1 (deterministic only).\n"
         "Clean-room pattern for one partner.\n"
         "Runbook, dbt docs, on-call."),
    ]
    for i, (t, col, b) in enumerate(phases):
        x = 0.45 + i * 4.25
        rrect(s, Inches(x), Inches(1.4), Inches(4.1), Inches(3.55), CARD, LINE, 1.0, 0.06)
        rect(s, Inches(x), Inches(1.4), Inches(4.1), Inches(0.5), col)
        add_textbox(s, Inches(x + 0.15), Inches(1.5), Inches(3.8), Inches(0.35),
                    t, size=14, bold=True, color=WHITE)
        add_textbox(s, Inches(x + 0.2), Inches(2.1), Inches(3.7), Inches(2.65),
                    b, size=13, color=INK_SOFT)

    rrect(s, Inches(0.45), Inches(5.1), Inches(12.45), Inches(1.85), PAPER, LINE, 1.0, 0.05)
    add_textbox(s, Inches(0.7), Inches(5.22), Inches(12), Inches(0.3),
                "How I would know it worked", size=14, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(5.55), Inches(12), Inches(1.2),
                "–  'Why doesn't this match?' tickets down ≥ 70% after the certified dataset is the only marketing source.\n"
                "–  Unspecified UTM share falling; conservation test green for 14 consecutive days.\n"
                "–  Vendor vs canonical variance explained (window/model), not ignored.\n"
                "–  p95 of the attribution dashboard < 5s (Section 2 will push finance below 3s).",
                size=13, color=INK_SOFT)
    set_notes(s,
        "Pragmatism vs scalability — the JD working style. Week 1 is inventory and stopping the "
        "bleeding (raw in BI), not a 12-month target architecture tour.\n\n"
        "Offer to partner with the Data Product Manager on the default attribution definition — "
        "engineering should not pick last-click in a vacuum.\n\n"
        "Time: 1 minute.")


def slide_close(prs):
    s = blank_slide(prs)
    content_chrome(s, "Close", 18, TOTAL, SECTION)
    title_block(s, "What I want you to remember")

    recs = [
        ("01", "Multi-tool on purpose", "Fivetran ingest, Databricks for hard Python and scale, Snowflake to serve and share, dbt for meaning, Airflow for time, Power BI for views."),
        ("02", "Logic once", "Attribution and revenue are warehouse models with tests. BI does not get a vote on the formula."),
        ("03", "Hash and recon", "Pseudonymous Gold, locked map, RTBF. Vendor numbers sit beside ours — we explain the delta."),
    ]
    for i, (n, t, b) in enumerate(recs):
        rrect(s, Inches(0.45), Inches(1.4 + i * 1.35), Inches(12.4), Inches(1.22), CARD, LINE, 1.0, 0.06)
        rrect(s, Inches(0.65), Inches(1.62 + i * 1.35), Inches(0.7), Inches(0.75), CLAY, adj=0.15)
        add_textbox(s, Inches(0.65), Inches(1.78 + i * 1.35), Inches(0.7), Inches(0.45),
                    n, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(s, Inches(1.55), Inches(1.55 + i * 1.35), Inches(11), Inches(0.35),
                    t, size=16, bold=True, color=INK)
        add_textbox(s, Inches(1.55), Inches(1.95 + i * 1.35), Inches(11), Inches(0.5),
                    b, size=14, color=INK_SOFT)

    add_textbox(s, Inches(0.45), Inches(5.55), Inches(12.4), Inches(1.4),
                "Next: Section 2 — the same platform, made self-serve for finance.\n"
                "Trusted net revenue, fast dashboards, and an end to Excel-as-a-warehouse.",
                size=16, color=INK_SOFT, font=FONT_LIGHT)
    set_notes(s,
        "Stop. Smile. Invite questions on stack downsides, identity, or why Snowflake + Databricks.\n\n"
        "If time is short, skip nothing before the stack table and the model slide — those are the "
        "assessment.\n\nTime: 30 seconds.")


def build(path):
    prs = _prs()
    slide_title(prs)
    slide_agenda(prs)
    slide_problem(prs)
    slide_root_causes(prs)
    slide_principles(prs)
    slide_architecture(prs)
    slide_platform_poster(prs)
    slide_medallion_poster(prs)
    slide_stack(prs)
    slide_no_overlap(prs)
    slide_elt(prs)
    slide_ingestion(prs)
    slide_model(prs)
    slide_privacy(prs)
    slide_quality(prs)
    slide_scale(prs)
    slide_plan(prs)
    slide_close(prs)
    prs.save(path)
    return path
