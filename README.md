# 风险感知与分析平台

面向银行公司客户授信尽调场景的风险感知与分析 Demo 平台。项目包含前端交互页面、Python 后端 API、SQLite 示例数据库、知识库材料、尽调报告生成/预审流程，以及 DeepSeek AI 调用能力。

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: enable AI report generation and review.
cp .env.example .env
# Fill DEEPSEEK_API_KEY in .env, or export it in your shell.
export DEEPSEEK_API_KEY=your_api_key

python due_diligence_assistant_demo/server.py
```

Open `http://127.0.0.1:8765`.

## AI Configuration

The backend reads the DeepSeek key from:

1. `DEEPSEEK_API_KEY` environment variable
2. `due_diligence_assistant_demo/.local_config.json` for local-only development

Do not commit local secrets. `.local_config.json` and `.env` are ignored by git. In Zeabur, configure `DEEPSEEK_API_KEY` in the service environment variables.

## Zeabur Deployment

This repository includes both `Dockerfile` and `Procfile` deployment entries. For Zeabur, create a new service from this GitHub repository and set:

- Runtime: Dockerfile is preferred
- Environment variables:
  - `DEEPSEEK_API_KEY`: your DeepSeek API key
  - `PORT`: Zeabur normally injects this automatically
  - `HOST=0.0.0.0`

The server listens on `PORT` when present, otherwise falls back to `8765`.

## Project Contents

This workspace now contains a SQLite demo database for a bank-facing SME due diligence platform.
It also now includes a second sample lane for listed-company public-data analysis imported from the local AkShare-backed cache in `/Users/hanshuting/Desktop/智能尽调引擎/data/finance_cache.sqlite3`.

## Files

- `database/schema.sql`
  - Full schema for the first-pass due diligence demo database.
- `scripts/build_demo_db.py`
  - Rebuilds the SQLite database and seeds five sample tech-SME cases.
- `scripts/export_demo_views.py`
  - Exports analyst-friendly CSV views, workbook input data, and per-company source folders.
- `scripts/build_demo_workbook.mjs`
  - Builds the Excel workbook used for manual review.
- `database/sme_due_diligence_demo.db`
  - Generated SQLite database file.
- `artifacts/company_files/`
  - Per-company source files such as contracts, bank transactions, tax summaries, and profile notes.
- `artifacts/csv/`
  - Flat CSV exports aligned to the database.
- `outputs/sme_due_diligence_demo/sme_due_diligence_demo.xlsx`
  - Excel workbook for reviewing the same seeded data outside SQLite.
- `due_diligence_assistant_demo/`
  - Frontend assets and Python API server for the interactive platform.

## Included Demo Coverage

The seeded dataset covers:

- 5 tech-SME borrower companies
- 5 listed-company public-data samples imported from the local AkShare cache
- company and person relationship modeling
- flexible company profile attributes for public profile fields and later manual enrichment
- 1 due diligence case per company
- uploaded documents, page-level OCR placeholders, and evidence references
- monthly financial, tax, bank, social security, utility, logistics, and receivable summaries
- annual financial-reporting detail for 2023-2025, including balance sheet, income statement, and cash flow statement lines
- financial reconciliation checks for balance sheet tie-out, gross profit bridge, capex vs fixed assets, cash roll-forward, and profit-to-cash conversion
- counterparties, contracts, orders, invoices, and contract-to-cash links
- IP, qualification, and R&D project records
- public risk events, peer comparisons, validation findings, risk tags, scores, report sections, and credit recommendations
- extension placeholders for anti-fraud, field visit, and post-loan monitoring

## Rebuild

```bash
python3 scripts/build_demo_db.py
python3 scripts/export_demo_views.py
node scripts/build_demo_workbook.mjs
```

## Sample Query Ideas

```sql
-- Borrower list
SELECT company_code, name, subindustry, risk_tier
FROM companies
ORDER BY company_code;

-- Validation findings for the main showcase case
SELECT c.case_no, vf.severity, vr.rule_name, vf.finding_title
FROM validation_findings vf
JOIN validation_rules vr ON vr.id = vf.rule_id
JOIN due_diligence_cases c ON c.id = vf.case_id
WHERE c.case_no = 'DD-2026-001'
ORDER BY vf.severity DESC;

-- Report sections with confidence
SELECT c.case_no, rs.section_title, rs.confidence
FROM report_sections rs
JOIN due_diligence_cases c ON c.id = rs.case_id
ORDER BY c.case_no, rs.display_order;
```

## Notes

- The current five borrower companies are realistic demo shells with synthetic internal operating data.
- The listed-company sample set currently uses real public financials and cached public profile fields where available; missing profile fields remain as placeholders for later manual enrichment.
- Replace seeded company shells, document paths, and public evidence references as you collect real screenshots and borrower materials.
- The schema is designed to migrate cleanly to PostgreSQL later if needed.
- The workbook, CSV views, and source folders are intentionally aligned so analysts can inspect the same demo content without querying SQLite directly.
