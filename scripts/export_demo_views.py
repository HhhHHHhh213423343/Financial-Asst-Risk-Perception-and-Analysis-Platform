#!/usr/bin/env python3
import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "sme_due_diligence_demo.db"
ARTIFACTS_DIR = ROOT / "artifacts"
CSV_DIR = ARTIFACTS_DIR / "csv"
COMPANY_FILES_DIR = ARTIFACTS_DIR / "company_files"
WORKBOOK_DATA_PATH = ARTIFACTS_DIR / "workbook_data.json"


EXPORTS = {
    "companies": """
        SELECT company_code, name, unified_social_credit_code, region_province, region_city,
               industry_category, subindustry, enterprise_scale, operating_status, risk_tier,
               registered_capital_cny, paid_in_capital_cny, overview
        FROM companies
        ORDER BY company_code
    """,
    "core_people": """
        SELECT c.company_code, c.name AS company_name, p.person_code, p.full_name, r.role_type,
               r.title, r.equity_ratio, r.voting_ratio, r.is_actual_controller, r.is_guarantor,
               p.education_level, p.birth_year
        FROM company_person_roles r
        JOIN companies c ON c.id = r.company_id
        JOIN persons p ON p.id = r.person_id
        ORDER BY c.company_code, r.role_type, p.full_name
    """,
    "company_profile_attributes": """
        SELECT c.company_code, a.attribute_group, a.label, a.value_text, a.source_ref, a.note
        FROM company_profile_attributes a
        JOIN companies c ON c.id = a.company_id
        ORDER BY c.company_code, a.attribute_group, a.label
    """,
    "related_companies": """
        SELECT c.company_code, r.related_company_name, r.relation_type, r.risk_flag, r.control_path, r.note
        FROM related_companies r
        JOIN companies c ON c.id = r.company_id
        ORDER BY c.company_code, r.relation_type, r.related_company_name
    """,
    "cases": """
        SELECT c.company_code, d.case_no, d.case_name, d.application_date, d.product_type,
               d.requested_amount_cny, d.requested_term_months, d.current_stage, d.decision_status,
               l.approved_amount_cny, l.loan_purpose, l.primary_repayment_source, l.guarantee_mode
        FROM due_diligence_cases d
        JOIN companies c ON c.id = d.company_id
        LEFT JOIN loan_applications l ON l.case_id = d.id
        ORDER BY d.case_no
    """,
    "financial_summary": """
        SELECT c.company_code, fp.period_code, fm.metric_code, fm.metric_name, fm.value, fm.unit
        FROM financial_metrics fm
        JOIN companies c ON c.id = fm.company_id
        JOIN financial_periods fp ON fp.id = fm.period_id
        WHERE fp.period_type = 'monthly'
          AND fm.metric_code IN ('revenue','gross_profit','net_profit','accounts_receivable','operating_cash_flow')
        ORDER BY c.company_code, fp.period_code, fm.metric_code
    """,
    "annual_financial_metrics": """
        SELECT c.company_code, fp.period_code, fm.metric_code, fm.metric_name, fm.metric_category, fm.value, fm.unit
        FROM financial_metrics fm
        JOIN companies c ON c.id = fm.company_id
        JOIN financial_periods fp ON fp.id = fm.period_id
        WHERE fp.period_type = 'annual'
        ORDER BY c.company_code, fp.period_code, fm.metric_category, fm.metric_code
    """,
    "financial_statement_lines": """
        SELECT c.company_code, fp.period_code, fsl.statement_type, fsl.display_order, fsl.line_code,
               fsl.line_name, fsl.value, fsl.unit, fsl.source_page_no
        FROM financial_statement_line_items fsl
        JOIN companies c ON c.id = fsl.company_id
        JOIN financial_periods fp ON fp.id = fsl.period_id
        ORDER BY c.company_code, fp.period_code, fsl.statement_type, fsl.display_order
    """,
    "financial_reconciliation_checks": """
        SELECT c.company_code, fp.period_code, frc.check_code, frc.check_name, frc.statement_scope,
               frc.lhs_label, frc.lhs_value, frc.rhs_label, frc.rhs_value, frc.variance_value,
               frc.variance_ratio, frc.status, frc.interpretation
        FROM financial_reconciliation_checks frc
        JOIN companies c ON c.id = frc.company_id
        JOIN financial_periods fp ON fp.id = frc.period_id
        ORDER BY c.company_code, fp.period_code, frc.check_code
    """,
    "bank_settlement_summaries": """
        SELECT c.company_code, fp.period_code, b.inflow_total_cny, b.outflow_total_cny, b.net_flow_cny,
               b.average_daily_balance_cny, b.top_inflow_counterparty, b.top_outflow_counterparty,
               b.transaction_count, b.large_transaction_count, b.abnormal_fluctuation_flag, b.summary_note
        FROM bank_settlement_summaries b
        JOIN companies c ON c.id = b.company_id
        JOIN financial_periods fp ON fp.id = b.period_id
        ORDER BY c.company_code, fp.period_code
    """,
    "tax_invoice_consistency_checks": """
        SELECT c.company_code, fp.period_code, t.declared_revenue_cny, t.invoiced_amount_cny, t.bank_receipts_cny,
               t.output_tax_cny, t.input_tax_cny, t.invoice_count, t.revenue_invoice_gap_cny,
               t.invoice_receipt_gap_cny, t.gap_ratio, t.status, t.check_note
        FROM tax_invoice_consistency_checks t
        JOIN companies c ON c.id = t.company_id
        JOIN financial_periods fp ON fp.id = t.period_id
        ORDER BY c.company_code, fp.period_code
    """,
    "related_party_transaction_summaries": """
        SELECT c.company_code, COALESCE(fp.period_code, '') AS period_code, r.related_party_name, r.relation_type,
               r.transaction_type, r.transaction_amount_cny, r.revenue_or_cost_ratio, r.settlement_method,
               r.pricing_comment, r.risk_level, r.note
        FROM related_party_transaction_summaries r
        JOIN companies c ON c.id = r.company_id
        LEFT JOIN financial_periods fp ON fp.id = r.period_id
        ORDER BY c.company_code, period_code, r.related_party_name
    """,
    "credit_history_summaries": """
        SELECT c.company_code, h.subject_type, h.subject_name, h.credit_channel, h.account_count,
               h.outstanding_balance_cny, h.overdue_count, h.max_overdue_bucket, h.hard_inquiry_3m,
               h.hard_inquiry_6m, h.external_guarantee_exposure_cny, h.credit_assessment, h.summary_note
        FROM credit_history_summaries h
        JOIN companies c ON c.id = h.company_id
        ORDER BY c.company_code, h.subject_type, h.subject_name
    """,
    "tax_filings": """
        SELECT c.company_code, fp.period_code, t.filing_type, t.declared_revenue_cny,
               t.output_tax_cny, t.input_tax_cny, t.tax_burden_ratio, t.filing_status
        FROM tax_filings t
        JOIN companies c ON c.id = t.company_id
        JOIN financial_periods fp ON fp.id = t.period_id
        ORDER BY c.company_code, fp.period_code
    """,
    "bank_transactions": """
        SELECT c.company_code, d.case_no, b.txn_date, b.txn_direction, b.counterparty_name,
               b.amount_cny, b.balance_after_cny, b.txn_summary
        FROM bank_transactions b
        JOIN due_diligence_cases d ON d.id = b.case_id
        JOIN companies c ON c.id = d.company_id
        ORDER BY c.company_code, b.txn_date
    """,
    "contracts": """
        SELECT c.company_code, ct.contract_no, ct.contract_type, cp.counterparty_name,
               ct.sign_date, ct.amount_cny, ct.payment_terms, ct.performance_status
        FROM contracts ct
        JOIN companies c ON c.id = ct.company_id
        JOIN counterparties cp ON cp.id = ct.counterparty_id
        ORDER BY c.company_code, ct.contract_no
    """,
    "orders": """
        SELECT c.company_code, o.order_no, ct.contract_no, o.order_date, o.order_amount_cny,
               o.delivery_due_date, o.collection_milestones, o.performance_status
        FROM orders o
        JOIN contracts ct ON ct.id = o.contract_id
        JOIN companies c ON c.id = o.company_id
        ORDER BY c.company_code, o.order_no
    """,
    "invoices": """
        SELECT c.company_code, i.invoice_no, ct.contract_no, i.issue_date, i.amount_cny,
               i.tax_rate_pct, i.invoice_type, cp.counterparty_name
        FROM invoices i
        LEFT JOIN contracts ct ON ct.id = i.contract_id
        LEFT JOIN counterparties cp ON cp.id = i.counterparty_id
        JOIN companies c ON c.id = i.company_id
        ORDER BY c.company_code, i.invoice_no
    """,
    "innovation": """
        SELECT c.company_code, i.asset_type, i.asset_name, i.registration_no, i.status,
               q.qualification_name, q.valid_to
        FROM companies c
        LEFT JOIN ip_assets i ON i.company_id = c.id
        LEFT JOIN innovation_qualifications q ON q.company_id = c.id
        ORDER BY c.company_code, i.asset_name, q.qualification_name
    """,
    "public_risks": """
        SELECT c.company_code, p.event_type, p.severity, p.event_date, p.title, p.summary
        FROM public_risk_events p
        JOIN companies c ON c.id = p.company_id
        ORDER BY c.company_code, p.event_date
    """,
    "validation_findings": """
        SELECT c.company_code, d.case_no, vr.rule_name, vf.severity, vf.finding_title,
               vf.finding_summary, vf.impact_summary, vf.confidence, vf.status
        FROM validation_findings vf
        JOIN validation_rules vr ON vr.id = vf.rule_id
        JOIN due_diligence_cases d ON d.id = vf.case_id
        JOIN companies c ON c.id = vf.company_id
        ORDER BY c.company_code, vf.severity DESC, vr.rule_name
    """,
    "credit_recommendations": """
        SELECT c.company_code, d.case_no, cr.recommendation_status, cr.suggested_amount_cny,
               cr.suggested_term_months, cr.suggested_rate_min, cr.suggested_rate_max,
               cr.guarantee_requirement, cr.supplemental_requirements, cr.note
        FROM credit_recommendations cr
        JOIN due_diligence_cases d ON d.id = cr.case_id
        JOIN companies c ON c.id = cr.company_id
        ORDER BY c.company_code
    """,
    "document_index": """
        SELECT c.company_code, d.case_no, doc.document_type, doc.title, doc.file_uri, doc.external_url, doc.page_count,
               doc.source_label, doc.summary
        FROM documents doc
        JOIN due_diligence_cases d ON d.id = doc.case_id
        JOIN companies c ON c.id = d.company_id
        ORDER BY c.company_code, doc.document_type
    """,
}


def rows_to_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fetch_dicts(conn, sql, params=()):
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, params)
    return [dict(row) for row in cur.fetchall()]


def build_company_files(conn, company_row):
    company_code = company_row["company_code"]
    company_dir = COMPANY_FILES_DIR / company_code
    company_dir.mkdir(parents=True, exist_ok=True)

    company_id = company_row["id"]
    case_row = fetch_dicts(
        conn,
        """
        SELECT d.id, d.case_no, d.case_name, d.application_date, d.current_stage, d.decision_status,
               d.requested_amount_cny, d.requested_term_months, l.loan_purpose,
               l.primary_repayment_source, l.secondary_repayment_source,
               cr.recommendation_status, cr.suggested_amount_cny, cr.note
        FROM due_diligence_cases d
        LEFT JOIN loan_applications l ON l.case_id = d.id
        LEFT JOIN credit_recommendations cr ON cr.case_id = d.id
        WHERE d.company_id = ?
        """,
        (company_id,),
    )[0]
    case_id = case_row["id"]

    people = fetch_dicts(
        conn,
        """
        SELECT p.full_name, r.role_type, r.title, r.equity_ratio, r.is_actual_controller, r.is_guarantor,
               p.education_level, p.birth_year
        FROM company_person_roles r
        JOIN persons p ON p.id = r.person_id
        WHERE r.company_id = ?
        ORDER BY r.is_actual_controller DESC, r.role_type, p.full_name
        """,
        (company_id,),
    )
    profile_attributes = fetch_dicts(
        conn,
        """
        SELECT attribute_group, label, value_text, source_ref, note
        FROM company_profile_attributes
        WHERE company_id = ?
        ORDER BY attribute_group, label
        """,
        (company_id,),
    )
    related_companies = fetch_dicts(
        conn,
        """
        SELECT related_company_name, relation_type, risk_flag, control_path, note
        FROM related_companies
        WHERE company_id = ?
        ORDER BY relation_type, related_company_name
        """,
        (company_id,),
    )
    financials = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, fm.metric_code, fm.metric_name, fm.value, fm.unit
        FROM financial_metrics fm
        JOIN financial_periods fp ON fp.id = fm.period_id
        WHERE fm.company_id = ? AND fp.period_type = 'monthly'
        ORDER BY fp.period_code, fm.metric_code
        """,
        (company_id,),
    )
    annual_financial_metrics = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, fm.metric_code, fm.metric_name, fm.metric_category, fm.value, fm.unit
        FROM financial_metrics fm
        JOIN financial_periods fp ON fp.id = fm.period_id
        WHERE fm.company_id = ? AND fp.period_type = 'annual'
        ORDER BY fp.period_code, fm.metric_category, fm.metric_code
        """,
        (company_id,),
    )
    financial_statement_lines = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, statement_type, display_order, line_code, line_name, value, unit, source_page_no
        FROM financial_statement_line_items f
        JOIN financial_periods fp ON fp.id = f.period_id
        WHERE f.company_id = ?
        ORDER BY fp.period_code, statement_type, display_order
        """,
        (company_id,),
    )
    reconciliation_checks = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, check_code, check_name, statement_scope, lhs_label, lhs_value,
               rhs_label, rhs_value, variance_value, variance_ratio, status, interpretation
        FROM financial_reconciliation_checks f
        JOIN financial_periods fp ON fp.id = f.period_id
        WHERE f.company_id = ?
        ORDER BY fp.period_code, check_code
        """,
        (company_id,),
    )
    settlement_summaries = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, inflow_total_cny, outflow_total_cny, net_flow_cny, average_daily_balance_cny,
               top_inflow_counterparty, top_outflow_counterparty, transaction_count, large_transaction_count,
               abnormal_fluctuation_flag, summary_note
        FROM bank_settlement_summaries b
        JOIN financial_periods fp ON fp.id = b.period_id
        WHERE b.company_id = ?
        ORDER BY fp.period_code
        """,
        (company_id,),
    )
    tax_invoice_checks = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, declared_revenue_cny, invoiced_amount_cny, bank_receipts_cny, output_tax_cny,
               input_tax_cny, invoice_count, revenue_invoice_gap_cny, invoice_receipt_gap_cny, gap_ratio, status, check_note
        FROM tax_invoice_consistency_checks t
        JOIN financial_periods fp ON fp.id = t.period_id
        WHERE t.company_id = ?
        ORDER BY fp.period_code
        """,
        (company_id,),
    )
    related_party_transactions = fetch_dicts(
        conn,
        """
        SELECT COALESCE(fp.period_code, '') AS period_code, related_party_name, relation_type, transaction_type,
               transaction_amount_cny, revenue_or_cost_ratio, settlement_method, pricing_comment, risk_level, note
        FROM related_party_transaction_summaries r
        LEFT JOIN financial_periods fp ON fp.id = r.period_id
        WHERE r.company_id = ?
        ORDER BY period_code, related_party_name
        """,
        (company_id,),
    )
    credit_history_summaries = fetch_dicts(
        conn,
        """
        SELECT subject_type, subject_name, credit_channel, account_count, outstanding_balance_cny, overdue_count,
               max_overdue_bucket, hard_inquiry_3m, hard_inquiry_6m, external_guarantee_exposure_cny,
               credit_assessment, summary_note
        FROM credit_history_summaries
        WHERE company_id = ?
        ORDER BY subject_type, subject_name
        """,
        (company_id,),
    )
    taxes = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, filing_type, declared_revenue_cny, output_tax_cny, input_tax_cny,
               tax_burden_ratio, filing_status
        FROM tax_filings t
        JOIN financial_periods fp ON fp.id = t.period_id
        WHERE t.company_id = ?
        ORDER BY fp.period_code
        """,
        (company_id,),
    )
    bank_transactions = fetch_dicts(
        conn,
        """
        SELECT txn_date, txn_direction, counterparty_name, amount_cny, balance_after_cny, txn_summary
        FROM bank_transactions
        WHERE case_id = ?
        ORDER BY txn_date
        """,
        (case_id,),
    )
    contracts = fetch_dicts(
        conn,
        """
        SELECT ct.contract_no, cp.counterparty_name, ct.sign_date, ct.amount_cny,
               ct.payment_terms, ct.performance_status
        FROM contracts ct
        JOIN counterparties cp ON cp.id = ct.counterparty_id
        WHERE ct.company_id = ?
        ORDER BY ct.contract_no
        """,
        (company_id,),
    )
    orders = fetch_dicts(
        conn,
        """
        SELECT o.order_no, ct.contract_no, o.order_date, o.order_amount_cny,
               o.delivery_due_date, o.collection_milestones, o.performance_status
        FROM orders o
        JOIN contracts ct ON ct.id = o.contract_id
        WHERE o.company_id = ?
        ORDER BY o.order_no
        """,
        (company_id,),
    )
    invoices = fetch_dicts(
        conn,
        """
        SELECT invoice_no, issue_date, amount_cny, tax_rate_pct, invoice_type, buyer_name, seller_name
        FROM invoices
        WHERE company_id = ?
        ORDER BY invoice_no
        """,
        (company_id,),
    )
    innovation = fetch_dicts(
        conn,
        """
        SELECT asset_type, asset_name, registration_no, status, grant_date, expiry_date
        FROM ip_assets
        WHERE company_id = ?
        ORDER BY asset_name
        """,
        (company_id,),
    )
    findings = fetch_dicts(
        conn,
        """
        SELECT vr.rule_name, vf.severity, vf.finding_title, vf.finding_summary, vf.impact_summary, vf.confidence
        FROM validation_findings vf
        JOIN validation_rules vr ON vr.id = vf.rule_id
        WHERE vf.company_id = ?
        ORDER BY vf.severity DESC, vr.rule_name
        """,
        (company_id,),
    )
    risks = fetch_dicts(
        conn,
        """
        SELECT event_date, event_type, severity, title, summary
        FROM public_risk_events
        WHERE company_id = ?
        ORDER BY event_date
        """,
        (company_id,),
    )
    annual_report_docs = fetch_dicts(
        conn,
        """
        SELECT title, document_date, external_url, summary
        FROM documents
        WHERE case_id = ? AND document_type = 'annual_report_notice'
        ORDER BY document_date DESC, id DESC
        """,
        (case_id,),
    )
    utility = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, utility_type, consumption_value, unit, yoy_change_pct
        FROM utility_metrics u
        JOIN financial_periods fp ON fp.id = u.period_id
        WHERE u.company_id = ?
        ORDER BY fp.period_code, utility_type
        """,
        (company_id,),
    )
    social = fetch_dicts(
        conn,
        """
        SELECT fp.period_code, insured_headcount, month_change, average_base_cny
        FROM social_security_metrics s
        JOIN financial_periods fp ON fp.id = s.period_id
        WHERE s.company_id = ?
        ORDER BY fp.period_code
        """,
        (company_id,),
    )

    files = {
        "enterprise_profile.md": (
            "# Enterprise Profile\n\n"
            f"- Company: {company_row['name']}\n"
            f"- Company code: {company_code}\n"
            f"- Unified social credit code: {company_row['unified_social_credit_code']}\n"
            f"- Region: {company_row['region_province']} / {company_row['region_city']}\n"
            f"- Industry: {company_row['industry_category']} / {company_row['subindustry']}\n"
            f"- Scale: {company_row['enterprise_scale']}\n"
            f"- Status: {company_row['operating_status']}\n"
            f"- Risk tier: {company_row['risk_tier']}\n"
            f"- Overview: {company_row['overview']}\n\n"
            "## Case Snapshot\n\n"
            f"- Case no: {case_row['case_no']}\n"
            f"- Requested amount: {case_row['requested_amount_cny']}\n"
            f"- Requested term: {case_row['requested_term_months']} months\n"
            f"- Current stage: {case_row['current_stage']}\n"
            f"- Recommendation status: {case_row['recommendation_status']}\n"
        ),
        "governance_summary.md": (
            "# Governance Summary\n\n"
            + "\n".join(
                [
                    f"- {person['full_name']} | {person['role_type']} | {person['title']} | equity {person['equity_ratio']}"
                    for person in people
                ]
            )
        ),
        "industry_insights.md": (
            "# Industry Insights\n\n"
            + (
                "\n".join(
                    [
                        f"- {item['label']} | {item['value_text']}"
                        for item in profile_attributes
                        if item["attribute_group"] == "industry_insight"
                    ]
                )
                or "- No industry insight cards."
            )
        ),
        "annual_financial_overview.md": (
            "# Annual Financial Statement Overview\n\n"
            + "\n".join(
                [
                    f"- {row['period_code']} | {row['metric_name']} | {row['value']} {row['unit']}"
                    for row in annual_financial_metrics
                    if row["metric_code"] in {"revenue", "net_profit", "operating_cash_flow", "capital_expenditure"}
                ]
            )
        ),
        "public_risks.md": (
            "# Public Risks\n\n"
            + ("\n".join([f"- {r['event_date']} | {r['severity']} | {r['title']} | {r['summary']}" for r in risks]) or "- No public risk items.")
        ),
        "annual_reports.md": (
            "# Annual Report Links\n\n"
            + (
                "\n".join(
                    [
                        f"- {doc['document_date']} | {doc['title']} | {doc['external_url'] or 'No URL cached'}"
                        for doc in annual_report_docs
                    ]
                )
                or "- No annual report links cached."
            )
        ),
        "report_summary.md": (
            "# Validation Findings\n\n"
            + "\n".join(
                [
                    f"- {f['severity']} | {f['rule_name']} | {f['finding_title']} | confidence {f['confidence']}"
                    for f in findings
                ]
            )
            + f"\n\n## Recommendation\n\n- Status: {case_row['recommendation_status']}\n- Suggested amount: {case_row['suggested_amount_cny']}\n- Note: {case_row['note']}\n"
        ),
    }

    for name, text in files.items():
        (company_dir / name).write_text(text, encoding="utf-8")

    csv_payloads = {
        "company_profile_attributes.csv": profile_attributes,
        "related_companies.csv": related_companies,
        "core_people.csv": people,
        "financial_monthly.csv": financials,
        "annual_financial_metrics.csv": annual_financial_metrics,
        "financial_statement_lines.csv": financial_statement_lines,
        "financial_reconciliation_checks.csv": reconciliation_checks,
        "bank_settlement_summaries.csv": settlement_summaries,
        "tax_invoice_consistency_checks.csv": tax_invoice_checks,
        "related_party_transaction_summaries.csv": related_party_transactions,
        "credit_history_summaries.csv": credit_history_summaries,
        "tax_filings.csv": taxes,
        "bank_transactions.csv": bank_transactions,
        "contracts.csv": contracts,
        "orders.csv": orders,
        "invoices.csv": invoices,
        "innovation_assets.csv": innovation,
        "utility_metrics.csv": utility,
        "social_security.csv": social,
        "validation_findings.csv": findings,
    }
    for filename, rows in csv_payloads.items():
        rows_to_csv(company_dir / filename, rows)

    doc_map = {
        "business_license": company_dir / "enterprise_profile.md",
        "articles": company_dir / "governance_summary.md",
        "public_profile": company_dir / "company_profile_attributes.csv",
        "financial_pack": company_dir / "financial_monthly.csv",
        "annual_financial_statements": company_dir / "financial_statement_lines.csv",
        "bank_statement": company_dir / "bank_transactions.csv",
        "tax_summary": company_dir / "tax_filings.csv",
        "core_contract": company_dir / "contracts.csv",
        "ip_pack": company_dir / "innovation_assets.csv",
        "public_risk": company_dir / "public_risks.md",
        "annual_report_notice": company_dir / "annual_reports.md",
        "industry_insights": company_dir / "industry_insights.md",
        "utility_report": company_dir / "utility_metrics.csv",
        "social_security": company_dir / "social_security.csv",
    }

    docs = fetch_dicts(
        conn,
        "SELECT id, document_type, title, page_count FROM documents WHERE case_id = ? ORDER BY id",
        (case_id,),
    )
    for doc in docs:
        path = doc_map.get(doc["document_type"], company_dir / "enterprise_profile.md")
        conn.execute("UPDATE documents SET file_uri = ? WHERE id = ?", (str(path), doc["id"]))
        pages = fetch_dicts(conn, "SELECT id, page_no FROM document_pages WHERE document_id = ? ORDER BY page_no", (doc["id"],))
        for page in pages:
            anchor = f"{path}#page-{page['page_no']}"
            conn.execute("UPDATE document_pages SET image_uri = ? WHERE id = ?", (anchor, page["id"]))
            conn.execute("UPDATE evidence_refs SET evidence_uri = ? WHERE page_id = ?", (anchor, page["id"]))


def write_exports(conn):
    workbook_data = {"sheets": []}
    for name, sql in EXPORTS.items():
        rows = fetch_dicts(conn, sql)
        rows_to_csv(CSV_DIR / f"{name}.csv", rows)
        workbook_data["sheets"].append(
            {
                "name": name,
                "headers": list(rows[0].keys()) if rows else [],
                "rows": [[row.get(header) for header in rows[0].keys()] for row in rows] if rows else [],
            }
        )
    counts = {}
    for table in [
        "companies",
        "persons",
        "company_profile_attributes",
        "due_diligence_cases",
        "documents",
        "financial_metrics",
        "financial_statement_line_items",
        "financial_reconciliation_checks",
        "bank_settlement_summaries",
        "tax_invoice_consistency_checks",
        "related_party_transaction_summaries",
        "credit_history_summaries",
        "bank_transactions",
        "contracts",
        "public_risk_events",
        "validation_findings",
    ]:
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    workbook_data["summary"] = counts
    WORKBOOK_DATA_PATH.write_text(json.dumps(workbook_data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    companies = fetch_dicts(conn, "SELECT * FROM companies ORDER BY company_code")
    for company in companies:
        build_company_files(conn, company)
    write_exports(conn)
    conn.commit()
    conn.close()
    print(f"Exported CSVs, workbook data, and company files under {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
