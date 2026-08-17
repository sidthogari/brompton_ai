"""Brompton-style architecture posters for the Noli interview decks."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "output" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 3200, 1800

CREAM = (250, 246, 240)
PAPER = (243, 236, 227)
CARD = (255, 252, 248)
INK = (28, 25, 23)
INK2 = (58, 52, 48)
MUTED = (122, 113, 104)
LINE = (228, 216, 200)
CLAY = (176, 92, 69)
CLAY_D = (140, 67, 48)
SAGE = (95, 117, 98)
SAGE_D = (62, 84, 69)
GOLD = (184, 149, 106)
NAVY = (44, 58, 71)
WHITE = (255, 255, 255)
PII = (163, 69, 58)
OK = (62, 107, 82)

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
LIB = Path("/usr/share/fonts/truetype/liberation")


def font(name, size):
    mapping = {
        "reg": FONT_DIR / "Inter-Regular.ttf",
        "med": FONT_DIR / "Inter-Medium.ttf",
        "sb": FONT_DIR / "Inter-SemiBold.ttf",
        "bd": FONT_DIR / "Inter-Bold.ttf",
    }
    path = mapping.get(name, mapping["reg"])
    if not path.exists():
        path = LIB / ("LiberationSans-Bold.ttf" if name in ("sb", "bd") else "LiberationSans-Regular.ttf")
    return ImageFont.truetype(str(path), size)


def rr(draw, box, fill, radius=16, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="lt"):
    if "\n" in s:
        x, y = xy
        lines = s.split("\n")
        ascent = fnt.size + 4
        if anchor == "mm":
            total_h = ascent * len(lines)
            y = y - total_h / 2 + fnt.size / 2
            for i, line in enumerate(lines):
                draw.text((x, y + i * ascent), line, font=fnt, fill=fill, anchor="mt")
        else:
            for i, line in enumerate(lines):
                draw.text((x, y + i * ascent), line, font=fnt, fill=fill, anchor="lt")
        return
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def card(draw, x, y, w, h, title, lines, accent=CLAY, title_size=22, body_size=18, radius=14):
    rr(draw, (x, y, x + w, y + h), CARD, radius=radius, outline=LINE, width=2)
    draw.rectangle((x, y, x + 10, y + h), fill=accent)
    f_title = font("sb", title_size)
    f_body = font("reg", body_size)
    text(draw, (x + 22, y + 12), title, f_title, INK)
    ty = y + 44
    for line in lines:
        text(draw, (x + 22, ty), line, f_body, INK2)
        ty += body_size + 6
    return (x, y, x + w, y + h)


def pill(draw, x, y, w, h, label, fill=CLAY, fg=WHITE, size=16):
    rr(draw, (x, y, x + w, y + h), fill, radius=h // 2)
    text(draw, (x + w / 2, y + h / 2), label, font("sb", size), fg, "mm")


def header_bar(draw, title, subtitle, kicker):
    draw.rectangle((0, 0, W, 148), fill=INK)
    draw.rectangle((0, 0, 18, 148), fill=CLAY)
    text(draw, (40, 28), kicker, font("sb", 20), GOLD)
    text(draw, (40, 62), title, font("bd", 42), WHITE)
    text(draw, (40, 114), subtitle, font("reg", 20), (220, 210, 198))


def ops_bar(draw, y, items):
    n = len(items)
    gap = 14
    x0, x1 = 36, W - 36
    tw = x1 - x0
    cw = (tw - gap * (n - 1)) / n
    for i, (label, sub, col) in enumerate(items):
        x = x0 + i * (cw + gap)
        rr(draw, (x, y, x + cw, y + 70), CARD, 12, LINE, 2)
        draw.rectangle((x, y, x + cw, y + 8), fill=col)
        text(draw, (x + 16, y + 20), label, font("sb", 18), INK)
        text(draw, (x + 16, y + 44), sub, font("reg", 14), MUTED)


def footer_domains(draw, y, domains):
    n = len(domains)
    gap = 12
    x0, x1 = 36, W - 36
    cw = (x1 - x0 - gap * (n - 1)) / n
    for i, (name, bits, col) in enumerate(domains):
        x = x0 + i * (cw + gap)
        rr(draw, (x, y, x + cw, y + 118), CARD, 12, LINE, 2)
        draw.rectangle((x, y, x + cw, y + 8), fill=col)
        text(draw, (x + 14, y + 20), name, font("sb", 18), INK)
        text(draw, (x + 14, y + 48), bits, font("reg", 15), INK2)


def draw_platform():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    header_bar(
        d,
        "NOLI  ·  Trusted Attribution & Revenue Platform",
        "Multi-tool modern data stack   ·   Azure   ·   Not a single-vendor lakehouse",
        "DATA ENGINEER BUSINESS CASE   ·   SECTION 1  ARCHITECTURE",
    )
    ops_bar(
        d,
        168,
        [
            ("Azure Entra ID", "RBAC · groups · SSO", NAVY),
            ("Unity Catalog", "Lineage · masks · grants", SAGE),
            ("Azure Key Vault", "Hash pepper · secrets", CLAY),
            ("dbt + Git", "Models · tests · docs", GOLD),
            ("Airflow", "Cross-platform clock", CLAY_D),
            ("Monitoring", "SLA · freshness · cost", SAGE_D),
        ],
    )

    # Column titles
    cols = [
        (36, 430, "1  SOURCES"),
        (486, 430, "2  INGEST"),
        (936, 980, "3  LAKEHOUSE  /  WAREHOUSE"),
        (1936, 430, "4  SERVE"),
        (2386, 380, "5  CONSUME"),
        (2786, 378, "GOVERN"),
    ]
    for x, w, name in cols:
        text(d, (x, 258), name, font("sb", 18), CLAY)

    # Sources
    card(d, 36, 288, 430, 150, "Paid media", ["Meta Ads  ·  spend, clicks, claimed conv.", "Google Ads  ·  campaigns, keywords"], CLAY)
    card(d, 36, 452, 430, 150, "Owned / CRM", ["Email  ·  Klaviyo (or equiv.) sends & clicks", "Customer / account events"], GOLD)
    card(d, 36, 616, 430, 196, "Site & commerce", ["GA4 / pixel  ·  sessions, UTMs, consent", "Orders, refunds, discounts, GWP", "CMP  ·  analytics & marketing flags"], SAGE)
    card(d, 36, 826, 430, 150, "Partners (later)", ["Brand / L'Oréal clean-room shares", "Hashed or aggregated keys only"], NAVY)

    # Ingest
    card(d, 486, 288, 430, 196, "Fivetran", ["Managed connectors + CDC", "Meta, Google, email, commerce, GA4", "Land RAW  ·  no business logic here"], GOLD)
    card(d, 486, 498, 430, 150, "Events / files", ["Databricks Auto Loader / APIs", "Pixel payloads, exceptions, backfills"], SAGE)
    card(d, 486, 662, 430, 170, "Airflow DAG", ["Sensor: Fivetran freshness SLA", "Then hash → dbt → tests → BI refresh", "Retries, paging, last-good publish"], CLAY)
    card(d, 486, 846, 430, 130, "Contract at the edge", ["UTM standard + alias table", "Missing UTM = unspecified, not direct"], CLAY_D)

    # Center medallion
    rr(d, (936, 288, 1916, 976), PAPER, 20, LINE, 2)
    text(d, (956, 304), "MEDALLION ON DELTA  +  SNOWFLAKE SERVING", font("sb", 20), SAGE_D)
    text(d, (956, 334), "Azure Data Lake  ·  ACID  ·  time travel  ·  schema evolution", font("reg", 16), MUTED)

    card(d, 956, 368, 940, 130, "Bronze  ·  RAW  (Delta / Snowflake RAW)", ["Immutable source extract  ·  VARIANT/JSON kept  ·  Fivetran metadata  ·  audit columns", "Schema drift allowed here  ·  never queried by Power BI"], NAVY, 20, 17)
    card(d, 956, 512, 940, 148, "Silver  ·  dbt SQL  +  Databricks Python", ["UTM parse & alias map  ·  identity stitch (deterministic v1)  ·  SCD2 campaigns", "PII hashed before wide access  ·  typed columns  ·  quality flags"], SAGE, 20, 17)
    card(d, 956, 674, 940, 148, "Gold  ·  dbt marts  (system of record)", ["fct_touchpoint  ·  fct_order  ·  fct_attribution (order × model)", "fct_vendor_claimed for recon  ·  dim_channel / campaign / customer_sk", "Default KPI: last non-direct click, 7-day, net of refunds"], GOLD, 20, 17)
    card(d, 956, 836, 940, 120, "PII / hash vault  ·  DE + DPO only", ["SHA-256(normalised id + Key Vault pepper)  ·  mapping table  ·  secure views  ·  RTBF", "Gold never stores raw email  ·  clean-room ready keys"], PII, 20, 17)

    # Serve
    card(d, 1936, 288, 430, 150, "Snowflake", ["Serving SoR for KPIs", "Shares + clean rooms"], NAVY)
    card(d, 1936, 452, 430, 150, "Unity Catalog + RBAC", ["Masks, row filters, lineage", "No personal schemas in prod"], SAGE)
    card(d, 1936, 616, 430, 150, "Certified semantic model", ["Power BI dataset on Gold only", "Thin measures  ·  no RAW joins"], GOLD)
    card(d, 1936, 780, 430, 196, "Activation (later)", ["Reverse ETL from certified Gold", "Consent-checked  ·  hashed identity", "Not from RAW or Excel"], CLAY)

    # Consume
    card(d, 2386, 288, 380, 130, "Power BI", ["Exec + analyst reports", "Import on day mart"], CLAY)
    card(d, 2386, 432, 380, 118, "Excel", ["Analyze in Excel live", "No RAW CSV warehouse"], GOLD)
    card(d, 2386, 564, 380, 118, "dbt docs", ["Metric catalogue", "Exposures / owners"], SAGE)
    card(d, 2386, 696, 380, 130, "AI / ML", ["Feature tables on Gold", "Genie only on certified data"], NAVY)
    card(d, 2386, 840, 380, 136, "Users", ["Marketing  ·  Finance", "DPM  ·  Tech Lead  ·  DS"], CLAY_D)

    # Govern rail
    card(d, 2786, 288, 378, 150, "Security", ["Entra groups", "Column/row policies", "Dynamic masking"], NAVY)
    card(d, 2786, 452, 378, 150, "Data quality", ["dbt tests + conservation", "Freshness / volume", "Vendor vs canonical"], SAGE)
    card(d, 2786, 616, 378, 150, "Lineage", ["Source → Gold → dashboard", "Impact analysis"], GOLD)
    card(d, 2786, 780, 378, 196, "Cost & ops", ["Fivetran MAR review", "Separate BI compute", "Budget alerts", "Auto-suspend clusters"], CLAY)

    # Value bar
    rr(d, (36, 1000, 3164, 1088), INK, 14)
    text(d, (56, 1024), "BUSINESS VALUE", font("sb", 16), GOLD)
    values = [
        "Single source of truth",
        "Trusted / governed data",
        "Explainable attribution",
        "GDPR + RTBF built in",
        "Clean-room ready",
        "AI-ready Gold",
        "Fast finance packs",
    ]
    for i, v in enumerate(values):
        pill(d, 56 + i * 440, 1050, 420, 28, v, (58, 48, 42), WHITE, 15)

    footer_domains(
        d,
        1112,
        [
            ("Marketing", "Attribution  ·  ROAS  ·  UTM hygiene\nVendor recon  ·  campaign SCD2", CLAY),
            ("Traffic / site", "GA4 freshness  ·  tracking accuracy\nConsent-aware events", GOLD),
            ("Finance", "Net revenue  ·  discounts  ·  refunds\nSame fct_order spine", SAGE),
            ("Customer", "Hashed SCV  ·  no raw email in marts\nDeterministic stitch v1", NAVY),
            ("Partners", "Clean rooms  ·  brand shares\nPurpose-limited queries", CLAY_D),
            ("AI enablement", "Model-ready features on Gold\nNot on dashboard extracts", SAGE_D),
        ],
    )

    text(
        d,
        (36, 1748),
        "Noli Data Engineer business case   ·   Fivetran · Databricks / Delta · Unity Catalog · Snowflake · dbt · Airflow · Power BI   ·   Hash / PII vault retained",
        font("reg", 18),
        MUTED,
    )
    img.save(OUT / "noli_platform_architecture.png", "PNG", optimize=True)
    return OUT / "noli_platform_architecture.png"


def draw_medallion():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    header_bar(
        d,
        "How data is refined  ·  Medallion, hash, and where logic lives",
        "ELT for meaning   ·   E-hash-L for privacy   ·   BI never redefines the formula",
        "SECTION 1  ·  DETAIL  ·  LAYERS AND CONTRACTS",
    )

    layers = [
        (CLAY, "BRONZE  ·  RAW", "Land, do not interpret",
         ["Fivetran + Auto Loader extracts", "Immutable JSON / tables + _fivetran_*", "Schema evolution allowed", "Evidence when marketing asks “what did Meta send?”", "No Power BI, no Excel, no Genie"]),
        (GOLD, "HASH GATE", "Privacy-preserving ingest",
         ["Normalise email / phone first", "SHA-256 + Key Vault pepper", "Mapping table in locked schema", "Pseudonymisation (not anonymisation)", "RTBF deletes/suppresses the map"]),
        (SAGE, "SILVER", "Clean, conform, stitch",
         ["UTM alias dictionary", "channel_group + is_valid_utm", "Deterministic identity v1", "SCD2 dim_campaign", "Typed columns; payload kept in Bronze"]),
        (NAVY, "GOLD", "Commercial grain = order",
         ["fct_order + fct_touchpoint", "fct_attribution (order × model)", "fct_vendor_claimed (recon only)", "Conservation test: attr $ = net $", "Default model signed off with DPM"]),
        (PII, "PII VAULT", "DE + DPO only",
         ["map_hash raw → hash", "Secure views for analytics", "No SELECT * on Bronze PII", "Skin / quiz data stays out of marts", "Clean-room keys, not emails"]),
    ]
    for i, (col, title, sub, bullets) in enumerate(layers):
        x = 36 + i * 632
        rr(d, (x, 188, x + 612, 980), CARD, 18, LINE, 2)
        rr(d, (x, 188, x + 612, 280), col, 18)
        # square off bottom of header
        d.rectangle((x, 250, x + 612, 280), fill=col)
        text(d, (x + 24, 208), title, font("bd", 24), WHITE)
        text(d, (x + 24, 244), sub, font("reg", 16), (255, 236, 228))
        ty = 312
        for b in bullets:
            rr(d, (x + 24, ty, x + 588, ty + 108), PAPER, 12)
            text(d, (x + 44, ty + 38), b, font("reg", 20), INK2)
            ty += 124

    # Bottom rule strip
    rr(d, (36, 1016, 3164, 1680), PAPER, 18, LINE, 2)
    text(d, (64, 1044), "DECISION RULES I WOULD DEFEND", font("sb", 22), INK)
    rules = [
        ("Fivetran", "Extract + load only. No last-click, no net revenue."),
        ("Databricks", "Ugly JSON, identity, hash, TB-scale, feature tables — not the certified mart."),
        ("dbt", "The only place attributed_revenue and net_revenue are defined and tested."),
        ("Airflow", "Order of operations and SLAs. No hidden SELECT in the DAG."),
        ("Snowflake", "Serving system of record + clean rooms. One Gold, not two."),
        ("Power BI / Excel", "Thin visuals on certified Gold. Joins and formulas already happened."),
    ]
    for i, (t, b) in enumerate(rules):
        col = i % 3
        row = i // 3
        x = 64 + col * 1030
        y = 1100 + row * 260
        rr(d, (x, y, x + 1000, y + 230), CARD, 14, LINE, 2)
        draw_rect = d
        draw_rect.rectangle((x, y, x + 12, y + 230), fill=CLAY if row == 0 else SAGE)
        text(d, (x + 36, y + 28), t, font("sb", 24), CLAY_D if row == 0 else SAGE_D)
        # wrap body
        f = font("reg", 20)
        lines = wrap(d, b, f, 920)
        ty = y + 80
        for line in lines:
            text(d, (x + 36, ty), line, f, INK2)
            ty += 32

    text(d, (36, 1748), "If a rule changes money or credit → dbt.  If it is visual → Power BI.  If it is “may we store this identifier?” → hash / consent path.", font("reg", 18), MUTED)
    img.save(OUT / "noli_medallion_logic.png", "PNG", optimize=True)
    return OUT / "noli_medallion_logic.png"


def draw_finance():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    header_bar(
        d,
        "NOLI  ·  Self-service finance platform on the same architecture",
        "One net_revenue  ·  line grain for truth  ·  day grain for speed  ·  Excel cannot invent a second warehouse",
        "DATA ENGINEER BUSINESS CASE   ·   SECTION 2  BUSINESS SOLUTION",
    )
    ops_bar(
        d,
        168,
        [
            ("Same ingest", "Fivetran RAW already landing", GOLD),
            ("Same hash vault", "Hashed customer_sk only", PII),
            ("Same Airflow", "Last-good if tests fail", CLAY),
            ("New finance mart", "dbt Gold product", SAGE),
            ("Certified dataset", "Power BI + live Excel", NAVY),
            ("Metric catalogue", "Owner + definition + as-of", GOLD),
        ],
    )

    text(d, (36, 258), "TODAY  ·  THE FAILURE MODE", font("sb", 18), PII)
    text(d, (1090, 258), "TARGET  ·  FINANCE PRODUCT ON GOLD", font("sb", 18), SAGE_D)
    text(d, (2386, 258), "HOW ANALYSTS WORK", font("sb", 18), CLAY)

    card(d, 36, 288, 1020, 140, "Raw tables in Power BI", ["Fivetran orders ⋈ refunds ⋈ discounts in DAX", "Fan-out, 10–15s loads, three definitions of net revenue"], PII, 22, 18)
    card(d, 36, 444, 1020, 140, "Excel as a warehouse", ["Exports drift from the dashboard", "Close pack cannot be explained"], CLAY, 22, 18)
    card(d, 36, 600, 1020, 140, "No owner of the formula", ["Leadership pressure, small data team", "Every analyst “fixes” it locally"], GOLD, 22, 18)
    card(d, 36, 756, 1020, 220, "What we stop", ["New datasets on RAW", "DAX that rewrites net revenue", "Silent VAT / GWP / staff orders", "Genie or AI on uncertified tables"], NAVY, 22, 18)

    # Target center
    rr(d, (1090, 288, 2350, 976), PAPER, 18, LINE, 2)
    text(d, (1110, 308), "SAME SPINE AS SECTION 1", font("sb", 16), MUTED)
    card(d, 1110, 348, 1220, 120, "fct_order_line", ["Atomic commercial fact  ·  SKU, brand, GMV, discount, net, tax  ·  header = sum(lines) test"], SAGE, 20, 18)
    card(d, 1110, 484, 600, 150, "fct_discount", ["Type: code / auto / GWP / staff", "funded_by: Noli vs brand"], GOLD, 20, 17)
    card(d, 1730, 484, 600, 150, "fct_refund", ["Partial/full  ·  refund_date", "Restates net on order_date too"], CLAY, 20, 17)
    card(d, 1110, 650, 1220, 120, "agg_finance_day", ["date × brand × channel × discount_type  ·  pre-summed for p95 < 3s exec view"], NAVY, 20, 18)
    card(d, 1110, 786, 1220, 168, "net_revenue  =  gmv − discounts − refunds − chargebacks", ["ex-VAT, GBP  ·  exclude test / staff / cancelled  ·  Finance + DPM sign the words", "Implemented once in dbt  ·  Power BI is SUM(net_revenue)  ·  Excel live on the same dataset"], PII, 20, 17)

    card(d, 2386, 288, 778, 150, "Find", ["Endorsed “Certified — Finance” dataset", "One-page metric catalogue"], SAGE)
    card(d, 2386, 452, 778, 150, "Explore", ["Date, brand, channel, discount type", "No warehouse keys on day one"], GOLD)
    card(d, 2386, 616, 778, 150, "Ask for more", ["New metric = dbt PR, not a CSV column", "Trivial metric SLA: 2–3 days"], CLAY)
    card(d, 2386, 780, 778, 196, "Understand", ["Hover: definition + as-of time", "Lineage to the dbt model", "Last-good if conservation fails"], NAVY)

    rr(d, (36, 1000, 3164, 1088), INK, 14)
    text(d, (56, 1024), "SUCCESS", font("sb", 16), GOLD)
    for i, v in enumerate(["p95 < 3s exec view", "Tickets −70%", "100% close packs certified", "0 RAW-bound finance models", "14d tests green", "≤ 3d new metric", "Attribution $ = finance $"]):
        pill(d, 56 + i * 440, 1050, 420, 28, v, (58, 48, 42), WHITE, 15)

    footer_domains(
        d,
        1112,
        [
            ("Keep from S1", "Fivetran, hash vault, Airflow,\nUnity Catalog, dbt project", SAGE),
            ("Add", "Finance mart, day agg,\nsemantic model, Excel live", CLAY),
            ("Change", "Ban BI on RAW  ·  split compute\nPre-aggregates for the pack", GOLD),
            ("Defer", "Reverse ETL  ·  real-time finance\nSecond BI tool", NAVY),
            ("Privacy", "No email in the dataset\nSame hashed customer_sk", PII),
            ("AI / JD projects", "Features from fct_order_line\nClean room = brand sell-out", SAGE_D),
        ],
    )
    text(d, (36, 1748), "Section 2 does not build a second platform. The join moves left. Meaning stays in dbt. Power BI and Excel only consume.", font("reg", 18), MUTED)
    img.save(OUT / "noli_finance_architecture.png", "PNG", optimize=True)
    return OUT / "noli_finance_architecture.png"


def main():
    paths = [draw_platform(), draw_medallion(), draw_finance()]
    for p in paths:
        print(p, p.stat().st_size)


if __name__ == "__main__":
    main()
