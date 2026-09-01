# RevenueRadar

**Enterprise Revenue Leakage & Margin Intelligence Platform**

RevenueRadar turns retail order, price-list, returns, and customer-master data into a governed view of revenue leakage and margin risk. It is designed for CFO, Sales Operations, and Finance Controller decisions—not just dashboarding.

## What it answers
- Which orders are priced below list or use an unapproved discount?
- Which customers, products, and regions are eroding margin?
- How much leakage is likely recoverable, and what is driving it?
- Do source, curated, and reporting revenue totals reconcile?

## Architecture
```text
Synthetic raw CSVs → validation & standardisation → curated revenue mart → SQL KPI views
          ↓                                                   ↓
  quality/reconciliation report                         leakage scoring
                                                          ↓
                                             executive web dashboard / Power BI model
```

## Quick start
```bash
python3 src/generate_data.py
python3 src/pipeline.py
python3 -m unittest discover -s tests
cd web && python3 -m http.server 8080
```
Open `http://localhost:8080` to explore the dashboard. No database is required for the sample; `sql/` contains PostgreSQL-ready analytics views.

## KPIs
Net revenue, gross margin %, leakage value, price variance, return rate, and unreconciled transaction count. Definitions and calculation rules are in [docs/kpi_catalog.md](docs/kpi_catalog.md).

## Portfolio impact
- Built a reproducible revenue-reconciliation pipeline with validation controls and a transparent recoverable-leakage score.
- Designed governed KPI logic and an executive decision dashboard for pricing, discount, return, and margin exceptions.

## Limitations
The data is deliberately synthetic and scores are transparent rules, not causal proof. Production deployment should connect approved source systems, enforce row-level access, and calibrate thresholds with Finance.

