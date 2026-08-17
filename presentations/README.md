# Noli Data Engineer interview presentations

Two PowerPoint decks for the business case:

1. **Section 1 — Architectural solution** (15 min)  
   Trusted multi-channel attribution (Meta, Google Ads, Email) from ingestion to BI.
2. **Section 2 — Business solution** (15 min)  
   Self-service finance platform on the same architecture: one net-revenue definition, fast dashboards.

Stack (JD-aligned, not single-vendor): **Fivetran · Databricks / Delta · Unity Catalog · Snowflake · dbt · Airflow · Power BI**, plus a **restricted hash / PII store**.

## Output

After `python3 build_all.py`:

- `output/Noli_Section1_Attribution_Architecture.pptx`
- `output/Noli_Section2_SelfService_Revenue_Platform.pptx`

Speaker notes are embedded on every slide. See `SPEAKER_GUIDE.md` for timing and likely questions.

## Rebuild

```bash
pip install python-pptx
python3 build_all.py
```
