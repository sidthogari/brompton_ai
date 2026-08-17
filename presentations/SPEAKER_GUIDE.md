# Noli Data Engineer business case — speaker guide

Two 15-minute presentations for a Senior Data Engineer and a Principal Engineer.

Send both `.pptx` files at least one full working day before the interview.

Open **View → Notes** while rehearsing. Every slide has a spoken script.

## How to use the 15 minutes

The brief’s “12 mins per slide” is almost certainly a typo for **1–2 minutes per slide**. These decks are sized for that.

| | Section 1 | Section 2 |
|---|---|---|
| Slides | 16 | 15 |
| Must-hit | 3 problem, 6 architecture, 7 stack table, 9 ELT, 11 model, 12 hash, 13 QA | 3 definition table, 5 model, 6 formula, 7 performance, 8 self-serve, 12 success |
| If they interrupt | Jump to the stack table or the model. Do not restart. |

Do **not** teach SQL. Do **not** walk every box. State the decision, the trade-off, and where you would start on Monday.

## The story that ties both sections

1. Marketing and finance are arguing with **raw tables and last-mile logic**.
2. You will not pick one vendor. You will give each tool a **lane**.
3. **Meaning lives in dbt Gold.** Fivetran loads. Databricks hashes and processes ugly data. Snowflake serves and shares. Airflow runs the clock. Power BI and Excel **consume**.
4. **Hash stays.** Gold never carries raw email. Clean rooms share keys or aggregates.
5. Section 2 is the same spine: **one `net_revenue`**, a day-level mart so the dashboard is fast, Excel on the certified model only.

## Stack one-liner (memorise this)

> Fivetran ingest, Databricks for hard Python and scale, Delta / Unity Catalog for ACID and governance, Snowflake to serve and clean-room share, dbt for meaning, Airflow for time, Power BI for views.

If they are **Snowflake-only**: Bronze can be `RAW`, Python via Snowpark or a thin Databricks job, Gold still dbt-on-Snowflake.

If they are **Databricks-only**: Databricks SQL serves Gold; clean rooms become Databricks Clean Rooms. The model does not change.

**Do not run two Gold marts.** That is the downside of a multi-tool stack.

## Section 1 — suggested clock

| Min | Slide | Say this, then stop |
|-----|--------|---------------------|
| 0:00 | Title | Outcome first: one grain, one identity, one default model, one place for logic. |
| 0:30 | Agenda | Five beats. Section 2 reuses this platform. |
| 1:15 | Problem | Three stories, not one number. UTMs are a contract failure. |
| 2:15 | Root causes | Identity, window/model, grain, UTMs, vendor vs canonical. |
| 3:30 | Principles | ELT + early hash. Logic once. Reconcile, don’t hide. |
| 4:30 | Architecture | Left to right in 90 seconds. Point at the PII vault. |
| 6:30 | **Stack table** | Why / downside for each tool. This is the assessment slide. |
| 9:00 | Lanes | Crossing lanes is how trust dies. |
| 10:00 | ELT | Raw evidence stays. Hash is the only transform at the door. |
| 11:00 | Ingest + UTM | Fivetran + alias table + `unspecified`, never silent direct. |
| 12:00 | Model | `fct_attribution` = order × model. Conservation test. |
| 13:00 | Hash / GDPR | Pseudonymisation, RTBF, clean rooms. |
| 13:45 | QA | Conservation + vendor recon, not just `not_null`. |
| 14:15 | Scale / plan | Incremental, separate compute. 90 days in slices. |
| 14:45 | Close | Three memories. Invite questions. |

## Section 2 — suggested clock

| Min | Slide | Say this, then stop |
|-----|--------|---------------------|
| 0:00 | Title | Same architecture. Finance product on Gold. |
| 0:30 | Problem | Slow + unexplained + Excel shadow warehouse. |
| 1:30 | Definition table | You do not sign off net revenue alone. Show the draft rule. |
| 3:00 | Architecture delta | Joins move left. Ban BI on RAW. |
| 4:30 | Model | Line grain for truth, day grain for speed. |
| 6:00 | Formula | One column, metric layer, thin DAX, live Excel. |
| 7:30 | Performance | 10–15s is raw DirectQuery. Import on `agg_finance_day`. |
| 9:00 | Self-serve | Catalogue + certified dataset + metric SLA. |
| 10:30 | Governance / ops | Guardrails, dual-run on formula changes, small-team roles. |
| 11:30 | Reverse ETL | JD skill. Not first. Don’t activate junk. |
| 12:30 | Success + 90 days | p95 < 3s, tickets −70%, 100% of close packs certified. |
| 14:00 | Risks + close | Say no to a second warehouse and to AI on RAW. |

## Likely questions (have a one-sentence answer)

**Why both Snowflake and Databricks?**  
Serving SoR is Snowflake (JD + clean rooms). Databricks is for hashing, identity, semi-structured volume, and AI feature tables — not a second mart.

**Why not transform in Fivetran?**  
You lose replay, tests, and lineage. Connectors extract. dbt means.

**Which attribution model is correct?**  
None. A signed-off default (last non-direct click, 7-day, net of refunds) plus alternatives as data. Vendor UI is a recon table, not the KPI.

**Is hashing anonymisation?**  
No. It is pseudonymisation if a mapping table exists. That is why the map is DE/DPO-only.

**Why Airflow if Databricks Workflows / dbt Cloud exist?**  
Airflow earns its place as the **cross-platform** clock (Fivetran → jobs → dbt → BI). If Noli already standardised on one orchestrator, use that — don’t add Airflow for sport.

**Power BI Import vs DirectQuery?**  
Import (or composite) on the day mart for the exec pack. DirectQuery on RAW is the current failure mode.

**How do you scale to TBs/day?**  
Incremental cursors, cluster on date, parse JSON once, separate BI compute, no Bronze scans from dashboards.

**What do you do on Monday?**  
Definition workshop (Finance + DPM) and remove RAW from the finance workspace. Then Fivetran → hash → `fct_order` conservation test.

## What not to say

- Do not pitch Brompton as the design. Pitch Noli’s stack; use Brompton as evidence you have shipped lakehouse, hashing, and GDPR.
- Do not claim a 12-month target architecture as week-one work.
- Do not invent Noli’s current warehouse if they correct you. The **lanes** still apply.
- Do not dump a Kafka/streaming story for finance-grade attribution. Hourly is enough. Streaming is for onsite tracking quality if they ask about the traffic-analysis project.

## Files

- `output/Noli_Section1_Attribution_Architecture.pptx`
- `output/Noli_Section2_SelfService_Revenue_Platform.pptx`

Regenerate after edits:

```bash
cd presentations && python3 build_all.py
```
