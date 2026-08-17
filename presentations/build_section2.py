"""Section 2 — Self-service trusted revenue platform on the Section 1 architecture."""

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from theme import (
    CARD,
    CLAY,
    CLAY_DEEP,
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
    SLIDE_H,
    SLIDE_W,
    WHITE,
    add_textbox,
    blank_slide,
    bullet_card,
    card,
    content_chrome,
    pill,
    rect,
    rrect,
    set_cell,
    set_notes,
    style_table,
    title_block,
    _set_run,
)

TOTAL = 15
SECTION = "Section 2  ·  Business solution"


def _prs():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def slide_title(prs):
    s = blank_slide(prs)
    rect(s, 0, 0, Inches(0.18), SLIDE_H, SAGE)
    rect(s, 0, Inches(6.85), SLIDE_W, Inches(0.65), INK)
    add_textbox(s, Inches(0.7), Inches(1.35), Inches(11.8), Inches(0.35),
                "NOLI  ·  DATA ENGINEER BUSINESS CASE  ·  SECTION 2",
                size=13, bold=True, color=SAGE)
    add_textbox(s, Inches(0.7), Inches(1.85), Inches(12), Inches(1.6),
                "A self-service revenue\nplatform finance can trust",
                size=40, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(3.7), Inches(11.5), Inches(1.1),
                "Same architecture as Section 1. Different product: one definition of net revenue,\n"
                "fast dashboards, and Excel that cannot invent a second warehouse.",
                size=18, color=INK_SOFT, font=FONT_LIGHT)
    add_textbox(s, Inches(0.7), Inches(5.15), Inches(11.5), Inches(0.7),
                "Audience: Senior Data Engineer  ·  Principal Engineer     15 minutes\n"
                "Built on: Fivetran · Databricks · Delta / Unity Catalog · Snowflake · dbt · Airflow · Power BI",
                size=14, color=MUTED)
    add_textbox(s, Inches(0.7), Inches(6.98), Inches(12), Inches(0.4),
                "Sidhartha Thogari   ·   Data Engineer interview",
                size=13, color=WHITE)
    set_notes(s,
        "Bridge from Section 1: we already have a place for logic (dbt Gold) and a hash path. "
        "Finance pain is different — speed, explainability, and inconsistent definitions — but "
        "the anti-pattern is the same: raw tables + joins in Power BI + Excel copies.\n\n"
        "Noli context: marketplace GMV, discounts, GWPs, refunds, brand-funded promos. 'Net "
        "revenue' is a product decision, not a SQL preference.\n\n"
        "Time: 30 seconds.")


def slide_problem(prs):
    s = blank_slide(prs)
    content_chrome(s, "Problem statement", 2, TOTAL, SECTION)
    title_block(s, "Leadership wants to trust the numbers. The dashboard cannot explain itself.",
                "Finance reports sales, refunds and discount impact from raw tables. Joins live in Power BI. 10–15s loads. Excel is the real BI tool.")

    pains = [
        ("Definition drift", "Net revenue, GMV, discount rate and 'refunds' mean different things in three reports and a close spreadsheet."),
        ("Wrong grain in BI", "Raw Fivetran orders ⋈ refunds ⋈ discounts in DAX. Every new analyst re-discovers fan-out bugs."),
        ("Latency as a trust issue", "10–15s feels broken. People export and do not come back. Shadow numbers win."),
        ("No owner, little capacity", "Pressure to 'just make it right' with a small data team. Self-serve must reduce interrupt load, not add a ticket queue."),
    ]
    for i, (t, b) in enumerate(pains):
        card(s, Inches(0.45 + (i % 2) * 6.4), Inches(1.85 + (i // 2) * 2.15),
             Inches(6.2), Inches(2.0), t, b, accent=SAGE if i % 2 else CLAY, title_size=16, body_size=13)
    set_notes(s,
        "Name the real risk: month-end close and board packs using a number that marketing "
        "attribution (Section 1) cannot reconcile to. If finance net revenue ≠ sum of attributed "
        "net revenue under the default model, we failed both sections.\n\n"
        "Excel is not the enemy. Uncertified Excel on raw extracts is.\n\nTime: 1 minute.")


def slide_inconsistent_logic(prs):
    s = blank_slide(prs)
    content_chrome(s, "Inconsistent business logic", 3, TOTAL, SECTION)
    title_block(s, "Everyone can write a measure. That is the bug.")

    headers = ["Metric", "How it fragments today", "Canonical rule (draft — Product + Finance sign-off)"]
    rows = [
        ["Gross sales / GMV", "With vs without tax; with vs without shipping; cancelled orders included.", "Sum of fulfilled order lines, ex-VAT, before discounts, excluding cancelled / test / staff."],
        ["Discounts", "Promo code only vs GWP vs employee vs shipping. Stacking unclear.", "All commercial reductions at line grain, typed (code, automatic, GWP, staff). GWP is a discount type, not free revenue."],
        ["Refunds / returns", "Partial refunds missed. Timing: order date vs refund date.", "fct_refund at refund_date; net revenue restated for order_date and available as refund-period view."],
        ["Net revenue", "GMV − discounts; or − refunds; or − both; or 'what Shopify said'.", "GMV − discounts − refunds − chargebacks. Shipping collected is not net revenue unless Finance says so."],
        ["AOV / discount rate", "Numerator and denominator from different filters.", "Same order set. discount_rate = discounts / GMV. AOV = net / order_count."],
    ]
    table = s.shapes.add_table(6, 3, Inches(0.4), Inches(1.4), Inches(12.5), Inches(5.5)).table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(5.15)
    table.columns[2].width = Inches(5.15)
    for c, h in enumerate(headers):
        set_cell(table, 0, c, h, True)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            set_cell(table, r, c, val, bold=(c == 0))
    style_table(table)
    for r in range(1, 6):
        for p in table.cell(r, 0).text_frame.paragraphs:
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = CLAY_DEEP
    set_notes(s,
        "Do not pretend you can sign off net revenue in the interview. Show the decision table "
        "and say the Data Product Manager + Finance own the words; engineering owns the "
        "implementation, tests, and that every tool reads the same column.\n\n"
        "Noli specifics to mention if asked: gift-with-purchase, brand-funded markdowns, "
        "marketplace vs 1P if they expand, multi-currency later. Start GBP, one entity.\n\n"
        "VAT: UK beauty retail almost always needs ex-VAT for commercial dashboards and a tax "
        "column for finance. Never bury VAT inside 'sales'.\n\nTime: 1.5 minutes.")


def slide_architecture_delta(prs):
    s = blank_slide(prs)
    content_chrome(s, "What changes on the Section 1 architecture", 4, TOTAL, SECTION)
    title_block(s, "We do not build a second platform. We add a finance product on Gold.")

    items = [
        ("Keep", SAGE,
         "Fivetran RAW, hash vault, Airflow, Unity Catalog / Snowflake RBAC, dbt project, certified Power BI pattern."),
        ("Add", CLAY,
         "Finance mart: fct_order_line, fct_refund, fct_discount, daily snapshot, metric layer. Semantic model. Analyze in Excel."),
        ("Change", GOLD,
         "Ban BI on RAW. Split compute: dbt transform vs BI warehouse. Pre-aggregates for the exec pack. Metric tests."),
        ("Defer", NAVY,
         "Reverse ETL of 'VIP revenue' into CRM until identity + consent are clean. Real-time finance. A second BI tool."),
    ]
    for i, (t, col, b) in enumerate(items):
        rrect(s, Inches(0.45 + i * 3.2), Inches(1.4), Inches(3.05), Inches(3.35), CARD, LINE, 1.0, 0.06)
        rect(s, Inches(0.45 + i * 3.2), Inches(1.4), Inches(3.05), Inches(0.5), col)
        add_textbox(s, Inches(0.6 + i * 3.2), Inches(1.5), Inches(2.75), Inches(0.35),
                    t, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        add_textbox(s, Inches(0.65 + i * 3.2), Inches(2.1), Inches(2.7), Inches(2.45),
                    b, size=13, color=INK_SOFT)

    rrect(s, Inches(0.45), Inches(4.95), Inches(12.45), Inches(1.95), PAPER, LINE, 1.0, 0.05)
    add_textbox(s, Inches(0.7), Inches(5.1), Inches(12), Inches(0.3),
                "The join moves left", size=15, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(5.5), Inches(12), Inches(1.2),
                "Today: Power BI scans raw tables and joins them per visual.\n"
                "Target: dbt incremental models produce a star schema + a daily finance agg. Power BI Import mode on that agg (and DirectQuery only if we must).\n"
                "Attribution (Section 1) reads the same fct_order.net_revenue. One economic spine.",
                size=14, color=INK_SOFT)
    set_notes(s,
        "This answers 'changes needed to the architecture/data model'. Emphasise reuse.\n\n"
        "If they ask about Databricks SQL vs Snowflake for this mart: serving finance KPIs is "
        "Snowflake (or Databricks SQL if that is the SoR). Not both.\n\nTime: 1.5 minutes.")


def slide_model(prs):
    s = blank_slide(prs)
    content_chrome(s, "Finance data model", 5, TOTAL, SECTION)
    title_block(s, "Line grain for truth. Day grain for speed. Metrics for language.")

    models = [
        ("fct_order_line", "SKU, brand, category, qty, gmv, discount, net, tax, shipping share. The atomic commercial fact."),
        ("fct_order", "Header rollup of the same rules. Status, customer_sk (hashed), channel of order — not attribution credit."),
        ("fct_discount", "One row per discount application. Type, code, funded_by (Noli vs brand)."),
        ("fct_refund", "Partial/full, reason, refund_ts, original_order_id, amount. Restates net."),
        ("agg_finance_day", "date × brand × channel × discount_type. Pre-summed for the 3-second dashboard."),
        ("metric_* / semantic", "dbt metrics or a thin semantic layer: net_revenue, gmv, discount_rate, refund_rate, aov."),
        ("dim_product", "Brand, hero category, margin class if we have it. SCD2 for price changes if needed."),
        ("dim_customer", "Same hashed key as attribution. No PII. Cohort month. Consent flags."),
    ]
    for i, (n, b) in enumerate(models):
        col = i % 4
        row = i // 4
        x = 0.45 + col * 3.2
        y = 1.38 + row * 2.55
        rrect(s, Inches(x), Inches(y), Inches(3.05), Inches(2.4), CARD, LINE, 1.0, 0.07)
        add_textbox(s, Inches(x + 0.14), Inches(y + 0.16), Inches(2.78), Inches(0.55),
                    n, size=13, bold=True, color=CLAY_DEEP)
        add_textbox(s, Inches(x + 0.14), Inches(y + 0.72), Inches(2.78), Inches(1.5),
                    b, size=12, color=INK_SOFT)
    set_notes(s,
        "Why line grain: discount impact and brand mix cannot be explained at header grain.\n\n"
        "Why day agg: exec dashboard should not sum 10M lines on every slicer click.\n\n"
        "Channel on the order is 'how they bought' (web, app). Attribution channel is 'who gets "
        "credit'. Do not collapse those in one column — that is how Section 1 and 2 start fighting.\n\n"
        "Time: 1.5 minutes.")


def slide_semantic(prs):
    s = blank_slide(prs)
    content_chrome(s, "Where net revenue is applied", 6, TOTAL, SECTION)
    title_block(s, "One formula, three interfaces — warehouse, BI, Excel")

    # Formula banner
    rrect(s, Inches(0.45), Inches(1.38), Inches(12.45), Inches(1.15), INK, adj=0.05)
    add_textbox(s, Inches(0.7), Inches(1.5), Inches(12), Inches(0.3),
                "Draft metric  ·  owned by Finance + Data Product  ·  implemented in dbt",
                size=12, bold=True, color=GOLD)
    add_textbox(s, Inches(0.7), Inches(1.82), Inches(12), Inches(0.5),
                "net_revenue  =  gmv  −  discounts  −  refunds  −  chargebacks     (ex-VAT, GBP, exclude test/staff/cancelled)",
                size=18, bold=True, color=WHITE)

    places = [
        ("dbt model + test", "Column net_revenue on fct_order_line and fct_order. Test: header = sum(lines). Test: refunds cannot exceed original net."),
        ("Metric layer", "Named metric with dimensions (date, brand, channel, discount_type). Versioned in git. Shown in dbt docs."),
        ("Power BI dataset", "Thin measures: SUM(net_revenue). No rewrite of the formula. Display folders and descriptions from the catalogue."),
        ("Excel", "Analyze in Excel / live connection to the certified dataset. Pivot only. If they need a new metric, it is a dbt PR — not a new column in a CSV."),
    ]
    for i, (t, b) in enumerate(places):
        card(s, Inches(0.45 + (i % 2) * 6.4), Inches(2.7 + (i // 2) * 1.95),
             Inches(6.2), Inches(1.82), t, b, accent=SAGE if i % 2 else CLAY, title_size=15, body_size=13)
    set_notes(s,
        "This is the heart of 'how business logic is applied inconsistently' and how we fix it.\n\n"
        "If they have MetricFlow / dbt Semantic Layer / Power BI calculation groups — great, use "
        "them. If not, a well-named Gold column plus a one-page metric catalogue is enough for a "
        "startup. Do not sell a 6-month semantic-layer programme.\n\n"
        "Time: 1.5 minutes.")


def slide_performance(prs):
    s = blank_slide(prs)
    content_chrome(s, "Why it is slow — and how we get under 3 seconds", 7, TOTAL, SECTION)
    title_block(s, "10–15 seconds is a modelling problem wearing a BI costume")

    headers = ["Today", "Why it hurts", "Change"]
    rows = [
        ["DirectQuery / live on raw Fivetran tables", "Wide JSON-ish tables, no cluster key the BI query hits, joins per visual.", "Import (or composite) on agg_finance_day + a few dims. RAW hidden."],
        ["Joins in the model for every refund", "Fan-out, duplicate GMV, unpredictable totals.", "Pre-joined facts in dbt. BI relates on surrogate keys only."],
        ["No incremental mart", "Every refresh rebuilds history. Warehouse and dataset fight.", "Incremental dbt + incremental Power BI refresh on date."],
        ["One warehouse for everything", "A backfill evicts the cache; finance waits.", "Dedicated BI warehouse/SQL endpoint, auto-resume, small."],
        ["Too many visuals, too many slicers", "Each slicer = another scan.", "Exec pack: 6 visuals, date + brand + channel. Detail page optional."],
        ["Wide text columns in memory", "Import mode bloated; refresh fails.", "Mart is typed, hashed IDs, no PII, no raw payloads."],
    ]
    table = s.shapes.add_table(7, 3, Inches(0.4), Inches(1.38), Inches(12.5), Inches(5.55)).table
    table.columns[0].width = Inches(3.6)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.4)
    for c, h in enumerate(headers):
        set_cell(table, 0, c, h, True)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            set_cell(table, r, c, val)
    style_table(table)
    set_notes(s,
        "Be concrete. 10–15s on a finance dashboard is almost always raw-table DirectQuery plus "
        "DAX joins.\n\n"
        "Target: p95 < 3s for the exec view; < 8s for a line-level drill page.\n\n"
        "Snowflake: clustering on order_date, search optimization if needed, result cache.\n"
        "Databricks SQL: Photon, clustering, warehouse sizing, query profile.\n\n"
        "I would measure before/after with the Power BI performance analyzer and warehouse query "
        "history — not vibes.\n\nTime: 1.5 minutes.")


def slide_self_serve(prs):
    s = blank_slide(prs)
    content_chrome(s, "Ease of use for analysts", 8, TOTAL, SECTION)
    title_block(s, "Self-serve is a product: certified data, a catalogue, and a paved road")

    items = [
        (CLAY, "Find",
         "dbt docs + exposures. A one-page metric catalogue (name, grain, owner, last certified). Power BI endorsed dataset only in the finance workspace."),
        (SAGE, "Explore",
         "Shared semantic model: date, brand, channel, discount type. Analysts build reports from the dataset — they do not get warehouse keys on day one."),
        (GOLD, "Excel, safely",
         "Analyze in Excel / live pivot on the certified model. Monthly close can still be a workbook — it cannot be a private extract of RAW."),
        (NAVY, "Ask for more",
         "New metric = issue → dbt PR → test → release notes. SLA: trivial metric 2–3 days, not a 6-week project. Data Product Manager prioritises."),
        (CLAY_DEEP, "Understand",
         "Every official visual has a hover: definition + as-of timestamp + default filters. Lineage link to the dbt model. No mystery tiles."),
        (DANGER, "Don't",
         "A second unofficial dataset 'just for this deck'. Personal gateways. Copy-paste of net revenue DAX. Sharing RAW via Teams."),
    ]
    for i, (col, t, b) in enumerate(items):
        card(s, Inches(0.45 + (i % 3) * 4.25), Inches(1.4 + (i // 3) * 2.55),
             Inches(4.1), Inches(2.4), t, b, accent=col, title_size=16, body_size=13)
    set_notes(s,
        "Self-serve fails when engineering dumps 200 tables into a workspace and calls it "
        "enablement.\n\n"
        "Paved road: 1 endorsed dataset, 1 catalogue, 1 request path. Dirt road (warehouse access) "
        "exists for the Data Tech Lead and a couple of power users — logged, not default.\n\n"
        "Genie / AI/BI: useful later on Gold, dangerous on RAW. Same rule as humans.\n\n"
        "Time: 1.5 minutes.")


def slide_governance(prs):
    s = blank_slide(prs)
    content_chrome(s, "Governance that still feels easy", 9, TOTAL, SECTION)
    title_block(s, "Guardrails, not gatekeeping")

    bullet_card(s, Inches(0.45), Inches(1.4), Inches(6.2), Inches(5.4),
                "Access & privacy",
                [
                    "Entra groups: finance_read, marketing_read, de_admin.",
                    "Row-level: not required for UK-only start; ready for region later.",
                    "Column-level: no email, phone, scan IDs in the finance dataset.",
                    "Same hash keys as Section 1 — finance can cohort, not identify.",
                    "Unity Catalog + Snowflake grants versioned (Terraform or GRANT models).",
                    "Workspace endorsement: only 'Certified — Finance' is used in exec packs.",
                    "Audit: who refreshed, who exported. Exports of line-level get a warning.",
                ], SAGE)
    bullet_card(s, Inches(6.85), Inches(1.4), Inches(6.05), Inches(5.4),
                "Change control",
                [
                    "Metric changes are PRs with Finance as reviewer.",
                    "Breaking change (net revenue formula) = versioned metric + dual-run.",
                    "dbt CI on PRs: tests must pass before merge.",
                    "Airflow blocks Power BI refresh if conservation tests fail — we serve last-good.",
                    "Release note in Teams/Slack: what changed, who signed it.",
                    "Quarterly: kill unused datasets (Power BI lineage + dbt exposures).",
                    "Cost: BI warehouse budget; no 24/7 XL cluster for a daily pack.",
                ], CLAY)
    set_notes(s,
        "Principal prompt: how do we move fast with a small team? Certified path is fast because "
        "it is narrow. Exceptions are explicit.\n\n"
        "Dual-run when changing net revenue: publish net_revenue_v2 alongside v1 for one close, "
        "then switch the default measure.\n\nTime: 1 minute.")


def slide_operating(prs):
    s = blank_slide(prs)
    content_chrome(s, "Operating model with a small data team", 10, TOTAL, SECTION)
    title_block(s, "Proactive reliability — the JD — without a 20-person platform group")

    rows = [
        ("Data Product Manager", "Priority, definition workshops, 'this is the number we will defend'."),
        ("Data Tech Lead", "Standards, stack boundaries, review of dbt contracts and Airflow SLAs."),
        ("Data Engineer (this role)", "Pipelines, tests, marts, performance, hash/RTBF, on-call for freshness."),
        ("Finance / Marketing", "Sign definitions. Stop screenshots of Ads Manager as source of truth."),
        ("AI / ML stakeholders", "Read feature tables from Gold, not from finance Excel. Same spine."),
    ]
    for i, (t, b) in enumerate(rows):
        rrect(s, Inches(0.45), Inches(1.38 + i * 1.0), Inches(12.4), Inches(0.9), CARD, LINE, 1.0, 0.08)
        rrect(s, Inches(0.62), Inches(1.55 + i * 1.0), Inches(3.1), Inches(0.55), PAPER, adj=0.2)
        add_textbox(s, Inches(0.7), Inches(1.62 + i * 1.0), Inches(2.95), Inches(0.42),
                    t, size=13, bold=True, color=CLAY_DEEP, align=PP_ALIGN.CENTER)
        add_textbox(s, Inches(3.95), Inches(1.58 + i * 1.0), Inches(8.6), Inches(0.55),
                    b, size=14, color=INK_SOFT)
    set_notes(s,
        "Show you will work with the DPM and Tech Lead, not hero-build a private stack.\n\n"
        "AI enablement from the JD: model-ready data is this Gold spine plus documented grains — "
        "not a separate 'AI dump'.\n\nTime: 1 minute.")


def slide_reverse_etl(prs):
    s = blank_slide(prs)
    content_chrome(s, "Activation — when, not first", 11, TOTAL, SECTION)
    title_block(s, "Reverse ETL is in the JD. I would not start there.")

    card(s, Inches(0.45), Inches(1.4), Inches(6.2), Inches(2.5),
         "Later",
         "Push LTV, predicted churn, or 'high discount reliance' to CRM / email — from certified Gold, hashed identity, consent-checked. Tool: existing reverse ETL or a thin job. Same Airflow DAG family.",
         accent=SAGE, title_size=16, body_size=14)
    card(s, Inches(6.85), Inches(1.4), Inches(6.05), Inches(2.5),
         "Not now",
         "Syncing raw emails or half-correct revenue into Klaviyo will industrialise the inconsistency we are here to kill. Activation without a metric layer is how ops and finance diverge forever.",
         accent=CLAY, title_size=16, body_size=14)

    rrect(s, Inches(0.45), Inches(4.1), Inches(12.45), Inches(2.85), CARD, LINE, 1.0, 0.05)
    add_textbox(s, Inches(0.7), Inches(4.25), Inches(12), Inches(0.35),
                "Fit to Noli example projects", size=16, bold=True, color=INK)
    add_textbox(s, Inches(0.7), Inches(4.7), Inches(12), Inches(2.0),
                "Traffic analysis  —  onsite tracking quality feeds the same UTM + identity spine; finance does not wait on it.\n"
                "Business data availability  —  this mart is the deliverable.\n"
                "Clean room  —  share brand-level sell-out / campaign performance, not customer lists.\n"
                "AI enablement  —  feature tables (discount sensitivity, repeat purchase) built on fct_order_line, not on a dashboard extract.",
                size=14, color=INK_SOFT)
    set_notes(s,
        "Shows judgement. JD lists reverse ETL as a nice-to-have skill, not the first milestone.\n\n"
        "Time: 1 minute.")


def slide_success(prs):
    s = blank_slide(prs)
    content_chrome(s, "How we measure success", 12, TOTAL, SECTION)
    title_block(s, "If we cannot measure it, it is a rebrand of the same mess")

    kpis = [
        ("< 3s", "p95 load, exec revenue view"),
        ("≥ 70%", "drop in 'numbers don't match' tickets"),
        ("100%", "board / close packs on certified dataset"),
        ("0", "Power BI models still bound to RAW"),
        ("14d", "conservation + freshness tests green"),
        ("≤ 3d", "time-to-ship a trivial new metric"),
    ]
    for i, (n, b) in enumerate(kpis):
        x = 0.45 + (i % 3) * 4.25
        y = 1.4 + (i // 3) * 2.15
        rrect(s, Inches(x), Inches(y), Inches(4.1), Inches(2.0), CARD, LINE, 1.0, 0.07)
        add_textbox(s, Inches(x + 0.2), Inches(y + 0.25), Inches(3.7), Inches(0.7),
                    n, size=28, bold=True, color=CLAY)
        add_textbox(s, Inches(x + 0.2), Inches(y + 1.05), Inches(3.7), Inches(0.7),
                    b, size=14, color=INK_SOFT)

    set_notes(s,
        "These are leading indicators the Principal can hold you to.\n\n"
        "Also track: % of analyst hours on paved road vs dirt road; Fivetran + warehouse cost vs "
        "baseline; Excel workbooks still on RAW (Power BI admin + sharing audit).\n\n"
        "Qualitative: Finance will present the dashboard in the leadership meeting without a "
        "disclaimer slide.\n\nTime: 1 minute.")


def slide_plan(prs):
    s = blank_slide(prs)
    content_chrome(s, "90-day plan", 13, TOTAL, SECTION)
    title_block(s, "Sequence: stop the bleeding, certify one number, then open self-serve")

    phases = [
        ("Days 1–30", CLAY, "Define & protect",
         "Workshop net revenue with Finance + DPM.\n"
         "Hide RAW from the finance workspace.\n"
         "Ship fct_order_line + header conservation test.\n"
         "Performance baseline (analyzer + query history).\n"
         "Last-good refresh policy in Airflow."),
        ("Days 31–60", SAGE, "Make it fast and official",
         "agg_finance_day + Import-mode certified dataset.\n"
         "Exec dashboard v1: sales, refunds, discount impact.\n"
         "Analyze in Excel on that dataset only.\n"
         "Metric catalogue (one page is enough).\n"
         "p95 under 3s or we keep cutting the model."),
        ("Days 61–90", NAVY, "Self-serve without chaos",
         "Analyst workspace on the certified model.\n"
         "Request SLA for new metrics.\n"
         "Kill or quarantine unofficial reports.\n"
         "Hook attribution net to finance net (recon).\n"
         "Write the runbook; measure ticket drop."),
    ]
    for i, (when, col, title, body) in enumerate(phases):
        x = 0.45 + i * 4.25
        rrect(s, Inches(x), Inches(1.4), Inches(4.1), Inches(5.4), CARD, LINE, 1.0, 0.06)
        rect(s, Inches(x), Inches(1.4), Inches(4.1), Inches(0.85), col)
        add_textbox(s, Inches(x + 0.18), Inches(1.48), Inches(3.75), Inches(0.3),
                    when, size=12, bold=True, color=WHITE)
        add_textbox(s, Inches(x + 0.18), Inches(1.78), Inches(3.75), Inches(0.35),
                    title, size=16, bold=True, color=WHITE)
        add_textbox(s, Inches(x + 0.2), Inches(2.45), Inches(3.7), Inches(4.1),
                    body, size=14, color=INK_SOFT)
    set_notes(s,
        "Align with Section 1 timeline: same first 30 days (RAW + hash + stop BI on raw). Finance "
        "mart and attribution mart can land in parallel if we share fct_order.\n\n"
        "Time: 1 minute.")


def slide_risks(prs):
    s = blank_slide(prs)
    content_chrome(s, "Risks and what I would refuse to do", 14, TOTAL, SECTION)
    title_block(s, "Downsides, said out loud")

    items = [
        ("dbt + Power BI overlap", "If someone 'quickly' rebuilds net revenue in DAX, we are back to day zero. Mitigation: dataset permissions + review of published measures."),
        ("Two warehouses", "Snowflake + Databricks without a Gold SoR doubles cost and definitions. Mitigation: one serving layer for finance."),
        ("Fivetran bill", "Finance wants every connector 'just in case'. Mitigation: model-driven connectors; pause unused MAR."),
        ("Over-modelling", "A 40-dim Kimball cathedral delays the close. Mitigation: line fact + 5 dims, then grow."),
        ("AI on junk", "Genie/Chat on RAW will sound confident and be wrong. Mitigation: AI only on certified Gold."),
        ("People", "Self-serve fails if Finance never attends the definition workshop. Mitigation: DPM-owned decision log."),
    ]
    for i, (t, b) in enumerate(items):
        card(s, Inches(0.45 + (i % 3) * 4.25), Inches(1.4 + (i // 3) * 2.55),
             Inches(4.1), Inches(2.4), t, b, accent=DANGER if i % 2 else GOLD, title_size=14, body_size=13)
    set_notes(s,
        "Principals hire people who can say no. The 'refuse' list is as important as the architecture.\n\n"
        "Time: 1 minute.")


def slide_close(prs):
    s = blank_slide(prs)
    content_chrome(s, "Close", 15, TOTAL, SECTION)
    title_block(s, "The platform in one sentence")

    rrect(s, Inches(0.45), Inches(1.45), Inches(12.45), Inches(1.7), INK, adj=0.05)
    add_textbox(s, Inches(0.75), Inches(1.7), Inches(11.9), Inches(1.25),
                "Ingest with Fivetran, process the hard things in Databricks, govern with Delta / Unity Catalog,\n"
                "serve from Snowflake, define meaning in dbt, run the clock with Airflow, and let Power BI\n"
                "and Excel consume — never redefine — a hashed, tested Gold model.",
                size=16, color=WHITE)

    recs = [
        ("Trust", "One net revenue. Conservation tests. Last-good publish."),
        ("Speed", "Day-level mart. Import mode. Separate BI compute."),
        ("Ease", "Certified dataset, catalogue, Excel live, metric SLA."),
    ]
    for i, (t, b) in enumerate(recs):
        rrect(s, Inches(0.45 + i * 4.25), Inches(3.4), Inches(4.1), Inches(1.7), CARD, LINE, 1.0, 0.07)
        add_textbox(s, Inches(0.65 + i * 4.25), Inches(3.55), Inches(3.7), Inches(0.4),
                    t, size=16, bold=True, color=CLAY)
        add_textbox(s, Inches(0.65 + i * 4.25), Inches(4.05), Inches(3.7), Inches(0.85),
                    b, size=14, color=INK_SOFT)

    add_textbox(s, Inches(0.45), Inches(5.35), Inches(12.4), Inches(1.5),
                "I would start Monday with the definition workshop and turning off RAW access in the finance workspace.\n"
                "Everything else is implementation.",
                size=16, color=INK_SOFT, font=FONT_LIGHT)
    set_notes(s,
        "Close on pragmatism. Invite questions on the formula, Power BI mode, or how this maps "
        "to their current Snowflake/dbt setup.\n\n"
        "If they ask about Brompton/Databricks depth: you have done lakehouse + GDPR hashing in "
        "production; you are explicitly fitting that craft to Noli's stack rather than importing "
        "a vendor religion.\n\nTime: 45 seconds.")


def build(path):
    prs = _prs()
    slide_title(prs)
    slide_problem(prs)
    slide_inconsistent_logic(prs)
    slide_architecture_delta(prs)
    slide_model(prs)
    slide_semantic(prs)
    slide_performance(prs)
    slide_self_serve(prs)
    slide_governance(prs)
    slide_operating(prs)
    slide_reverse_etl(prs)
    slide_success(prs)
    slide_plan(prs)
    slide_risks(prs)
    slide_close(prs)
    prs.save(path)
    return path
