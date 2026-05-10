PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    unified_social_credit_code TEXT UNIQUE,
    established_on TEXT,
    region_province TEXT,
    region_city TEXT,
    industry_category TEXT,
    subindustry TEXT,
    is_tech_sme INTEGER NOT NULL DEFAULT 1,
    enterprise_scale TEXT,
    operating_status TEXT,
    registered_capital_cny REAL,
    paid_in_capital_cny REAL,
    website TEXT,
    overview TEXT,
    risk_tier TEXT,
    shell_type TEXT DEFAULT 'demo_realistic',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_code TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    gender TEXT,
    birth_year INTEGER,
    education_level TEXT,
    marital_status TEXT,
    hukou_location TEXT,
    residence_city TEXT,
    mobile_masked TEXT,
    id_number_masked TEXT,
    risk_note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE company_person_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    role_type TEXT NOT NULL,
    title TEXT,
    equity_ratio REAL,
    voting_ratio REAL,
    is_actual_controller INTEGER NOT NULL DEFAULT 0,
    is_guarantor INTEGER NOT NULL DEFAULT 0,
    joined_on TEXT,
    left_on TEXT,
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
);

CREATE TABLE related_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    related_company_name TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    control_path TEXT,
    risk_flag INTEGER NOT NULL DEFAULT 0,
    unified_social_credit_code TEXT,
    industry_category TEXT,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE company_profile_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER,
    attribute_group TEXT NOT NULL,
    label TEXT NOT NULL,
    value_text TEXT,
    source_ref TEXT,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE SET NULL
);

CREATE TABLE due_diligence_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_no TEXT NOT NULL UNIQUE,
    company_id INTEGER NOT NULL,
    case_name TEXT NOT NULL,
    application_date TEXT NOT NULL,
    product_type TEXT NOT NULL,
    requested_amount_cny REAL NOT NULL,
    requested_term_months INTEGER NOT NULL,
    current_stage TEXT NOT NULL,
    decision_status TEXT NOT NULL,
    case_owner TEXT,
    summary TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE loan_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    requested_amount_cny REAL NOT NULL,
    approved_amount_cny REAL,
    loan_purpose TEXT,
    primary_repayment_source TEXT,
    secondary_repayment_source TEXT,
    repayment_method TEXT,
    guarantee_mode TEXT,
    annual_rate_min REAL,
    annual_rate_max REAL,
    tenor_months INTEGER,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE guarantees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    guarantee_type TEXT NOT NULL,
    provider_company_id INTEGER,
    provider_person_id INTEGER,
    asset_name TEXT,
    asset_category TEXT,
    appraised_value_cny REAL,
    pledge_rate REAL,
    lien_status TEXT,
    guarantee_status TEXT,
    notes TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_company_id) REFERENCES companies(id),
    FOREIGN KEY (provider_person_id) REFERENCES persons(id)
);

CREATE TABLE source_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL,
    authority_level TEXT,
    access_mode TEXT,
    description TEXT,
    base_url TEXT,
    default_reliability REAL
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER,
    person_id INTEGER,
    source_id INTEGER,
    document_type TEXT NOT NULL,
    title TEXT NOT NULL,
    source_label TEXT,
    file_uri TEXT,
    external_url TEXT,
    page_count INTEGER,
    uploaded_at TEXT,
    document_date TEXT,
    is_ocr_processed INTEGER NOT NULL DEFAULT 0,
    checksum TEXT,
    summary TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (source_id) REFERENCES source_registry(id)
);

CREATE TABLE document_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    page_no INTEGER NOT NULL,
    image_uri TEXT,
    ocr_text TEXT,
    layout_summary TEXT,
    extracted_json TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE TABLE evidence_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    source_id INTEGER,
    document_id INTEGER,
    page_id INTEGER,
    target_type TEXT NOT NULL,
    target_id INTEGER NOT NULL,
    evidence_kind TEXT NOT NULL,
    excerpt TEXT,
    evidence_uri TEXT,
    confidence REAL,
    notes TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES source_registry(id),
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (page_id) REFERENCES document_pages(id)
);

CREATE TABLE financial_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_code TEXT NOT NULL,
    period_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_month INTEGER,
    is_latest INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE financial_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    metric_code TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_category TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL DEFAULT 'CNY',
    currency TEXT DEFAULT 'CNY',
    source_type TEXT,
    source_ref TEXT,
    is_estimated INTEGER NOT NULL DEFAULT 0,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE financial_statement_line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    statement_type TEXT NOT NULL,
    line_code TEXT NOT NULL,
    line_name TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL DEFAULT 'CNY',
    source_document_id INTEGER,
    source_page_no INTEGER,
    source_ref TEXT,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE,
    FOREIGN KEY (source_document_id) REFERENCES documents(id)
);

CREATE TABLE financial_reconciliation_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    check_code TEXT NOT NULL,
    check_name TEXT NOT NULL,
    statement_scope TEXT NOT NULL,
    lhs_label TEXT NOT NULL,
    lhs_value REAL NOT NULL,
    rhs_label TEXT NOT NULL,
    rhs_value REAL NOT NULL,
    variance_value REAL NOT NULL,
    variance_ratio REAL,
    threshold_value REAL,
    status TEXT NOT NULL,
    interpretation TEXT,
    linked_finding_id INTEGER,
    source_document_id INTEGER,
    source_page_no INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_finding_id) REFERENCES validation_findings(id),
    FOREIGN KEY (source_document_id) REFERENCES documents(id)
);

CREATE TABLE bank_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    account_name TEXT NOT NULL,
    bank_name TEXT NOT NULL,
    account_masked TEXT NOT NULL,
    account_type TEXT NOT NULL,
    is_primary INTEGER NOT NULL DEFAULT 0,
    opened_on TEXT,
    status TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE bank_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    txn_date TEXT NOT NULL,
    txn_direction TEXT NOT NULL,
    counterparty_name TEXT,
    counterparty_account_masked TEXT,
    amount_cny REAL NOT NULL,
    balance_after_cny REAL,
    txn_summary TEXT,
    linked_contract_id INTEGER,
    linked_invoice_id INTEGER,
    source_ref TEXT,
    FOREIGN KEY (account_id) REFERENCES bank_accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE tax_filings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    filing_type TEXT NOT NULL,
    declared_revenue_cny REAL,
    output_tax_cny REAL,
    input_tax_cny REAL,
    tax_burden_ratio REAL,
    filing_status TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE bank_settlement_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    inflow_total_cny REAL,
    outflow_total_cny REAL,
    net_flow_cny REAL,
    average_daily_balance_cny REAL,
    top_inflow_counterparty TEXT,
    top_inflow_amount_cny REAL,
    top_outflow_counterparty TEXT,
    top_outflow_amount_cny REAL,
    transaction_count INTEGER,
    large_transaction_count INTEGER,
    abnormal_fluctuation_flag INTEGER NOT NULL DEFAULT 0,
    summary_note TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE tax_invoice_consistency_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    declared_revenue_cny REAL,
    invoiced_amount_cny REAL,
    bank_receipts_cny REAL,
    output_tax_cny REAL,
    input_tax_cny REAL,
    invoice_count INTEGER,
    revenue_invoice_gap_cny REAL,
    invoice_receipt_gap_cny REAL,
    gap_ratio REAL,
    status TEXT NOT NULL,
    check_note TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE payment_channel_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    channel_name TEXT NOT NULL,
    gross_receipts_cny REAL,
    refund_amount_cny REAL,
    transaction_count INTEGER,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE social_security_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    insured_headcount INTEGER,
    month_change INTEGER,
    average_base_cny REAL,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE utility_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    utility_type TEXT NOT NULL,
    consumption_value REAL,
    unit TEXT NOT NULL,
    yoy_change_pct REAL,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE logistics_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    shipment_count INTEGER,
    shipment_weight_kg REAL,
    freight_cost_cny REAL,
    return_rate_pct REAL,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE receivables_payables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    record_type TEXT NOT NULL,
    balance_cny REAL,
    overdue_over_90d_cny REAL,
    top5_ratio_pct REAL,
    average_days REAL,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE related_party_transaction_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER,
    related_party_name TEXT NOT NULL,
    relation_type TEXT,
    transaction_type TEXT NOT NULL,
    transaction_amount_cny REAL,
    revenue_or_cost_ratio REAL,
    settlement_method TEXT,
    pricing_comment TEXT,
    risk_level TEXT,
    source_ref TEXT,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE SET NULL
);

CREATE TABLE credit_history_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    subject_type TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    linked_person_id INTEGER,
    credit_channel TEXT,
    account_count INTEGER,
    outstanding_balance_cny REAL,
    overdue_count INTEGER,
    max_overdue_bucket TEXT,
    hard_inquiry_3m INTEGER,
    hard_inquiry_6m INTEGER,
    external_guarantee_exposure_cny REAL,
    credit_assessment TEXT,
    summary_note TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_person_id) REFERENCES persons(id) ON DELETE SET NULL
);

CREATE TABLE counterparties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    counterparty_name TEXT NOT NULL,
    counterparty_type TEXT NOT NULL,
    industry TEXT,
    city TEXT,
    relationship_tenor_months INTEGER,
    concentration_rank INTEGER,
    risk_note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    counterparty_id INTEGER NOT NULL,
    contract_no TEXT NOT NULL,
    contract_type TEXT NOT NULL,
    sign_date TEXT NOT NULL,
    amount_cny REAL NOT NULL,
    payment_terms TEXT,
    delivery_terms TEXT,
    performance_status TEXT,
    source_document_id INTEGER,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (counterparty_id) REFERENCES counterparties(id),
    FOREIGN KEY (source_document_id) REFERENCES documents(id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    contract_id INTEGER NOT NULL,
    order_no TEXT NOT NULL,
    order_date TEXT NOT NULL,
    order_amount_cny REAL NOT NULL,
    delivery_due_date TEXT,
    collection_milestones TEXT,
    performance_status TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    contract_id INTEGER,
    counterparty_id INTEGER,
    invoice_no TEXT NOT NULL,
    invoice_type TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    amount_cny REAL NOT NULL,
    tax_rate_pct REAL,
    buyer_name TEXT,
    seller_name TEXT,
    note TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (counterparty_id) REFERENCES counterparties(id)
);

CREATE TABLE contract_cash_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    contract_id INTEGER,
    order_id INTEGER,
    invoice_id INTEGER,
    bank_transaction_id INTEGER,
    receivable_record_id INTEGER,
    link_type TEXT NOT NULL,
    linked_amount_cny REAL,
    confidence REAL,
    note TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (bank_transaction_id) REFERENCES bank_transactions(id),
    FOREIGN KEY (receivable_record_id) REFERENCES receivables_payables(id)
);

CREATE TABLE ip_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    asset_type TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    registration_no TEXT,
    ownership_holder TEXT,
    grant_date TEXT,
    expiry_date TEXT,
    status TEXT,
    pledged_flag INTEGER NOT NULL DEFAULT 0,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE innovation_qualifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    qualification_name TEXT NOT NULL,
    issuing_authority TEXT,
    valid_from TEXT,
    valid_to TEXT,
    status TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE rd_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    project_name TEXT NOT NULL,
    stage TEXT,
    owner_person_id INTEGER,
    budget_cny REAL,
    spent_cny REAL,
    expected_commercialization_date TEXT,
    summary TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (owner_person_id) REFERENCES persons(id)
);

CREATE TABLE rd_team_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    period_id INTEGER NOT NULL,
    rd_headcount INTEGER,
    masters_or_above INTEGER,
    rd_ratio_pct REAL,
    annualized_rd_spend_cny REAL,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (period_id) REFERENCES financial_periods(id) ON DELETE CASCADE
);

CREATE TABLE intangible_asset_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    note_type TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    pledge_status TEXT,
    dispute_status TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE public_risk_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    event_date TEXT,
    counterparty_name TEXT,
    title TEXT NOT NULL,
    summary TEXT,
    public_source_name TEXT,
    public_url TEXT,
    source_ref TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE shareholding_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    case_id INTEGER NOT NULL,
    change_date TEXT NOT NULL,
    change_type TEXT NOT NULL,
    before_snapshot TEXT,
    after_snapshot TEXT,
    declared_reason TEXT,
    risk_comment TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE
);

CREATE TABLE industry_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subindustry TEXT NOT NULL UNIQUE,
    industry_category TEXT NOT NULL,
    policy_direction TEXT,
    lifecycle_stage TEXT,
    benchmark_note TEXT,
    update_cycle TEXT
);

CREATE TABLE industry_benchmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_profile_id INTEGER NOT NULL,
    metric_code TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    benchmark_value REAL,
    unit TEXT,
    percentile_25 REAL,
    percentile_50 REAL,
    percentile_75 REAL,
    note TEXT,
    FOREIGN KEY (industry_profile_id) REFERENCES industry_profiles(id) ON DELETE CASCADE
);

CREATE TABLE peer_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    benchmark_id INTEGER NOT NULL,
    company_value REAL,
    variance_pct REAL,
    percentile_bucket TEXT,
    narrative TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (benchmark_id) REFERENCES industry_benchmarks(id) ON DELETE CASCADE
);

CREATE TABLE validation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_code TEXT NOT NULL UNIQUE,
    rule_name TEXT NOT NULL,
    dimension TEXT NOT NULL,
    severity_default TEXT NOT NULL,
    rule_logic TEXT NOT NULL,
    manual_review_required INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE validation_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    rule_id INTEGER NOT NULL,
    severity TEXT NOT NULL,
    finding_title TEXT NOT NULL,
    finding_summary TEXT NOT NULL,
    impact_summary TEXT,
    confidence REAL,
    status TEXT,
    requires_manual_review INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (rule_id) REFERENCES validation_rules(id)
);

CREATE TABLE risk_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    tag_code TEXT NOT NULL,
    tag_name TEXT NOT NULL,
    dimension TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE case_risk_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    score_dimension TEXT NOT NULL,
    score_value REAL NOT NULL,
    score_band TEXT NOT NULL,
    rationale TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE report_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    section_code TEXT NOT NULL,
    section_title TEXT NOT NULL,
    content TEXT NOT NULL,
    confidence REAL,
    display_order INTEGER NOT NULL,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE credit_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL UNIQUE,
    company_id INTEGER NOT NULL,
    recommendation_status TEXT NOT NULL,
    suggested_amount_cny REAL,
    suggested_term_months INTEGER,
    suggested_rate_min REAL,
    suggested_rate_max REAL,
    guarantee_requirement TEXT,
    supplemental_requirements TEXT,
    rejection_reason TEXT,
    note TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE device_risk_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    device_fingerprint TEXT,
    ip_address TEXT,
    gps_city TEXT,
    risk_level TEXT,
    event_time TEXT,
    note TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE field_visit_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    visit_date TEXT,
    visitor_name TEXT,
    status TEXT,
    checklist_json TEXT,
    findings_summary TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE post_loan_monitoring_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    monitor_date TEXT,
    event_type TEXT,
    severity TEXT,
    summary TEXT,
    FOREIGN KEY (case_id) REFERENCES due_diligence_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE INDEX idx_cases_company ON due_diligence_cases(company_id);
CREATE INDEX idx_roles_company_person ON company_person_roles(company_id, person_id);
CREATE INDEX idx_profile_attrs_company_group ON company_profile_attributes(company_id, attribute_group);
CREATE INDEX idx_docs_case ON documents(case_id);
CREATE INDEX idx_doc_pages_document ON document_pages(document_id);
CREATE INDEX idx_periods_company_case ON financial_periods(company_id, case_id);
CREATE INDEX idx_fin_metrics_period_code ON financial_metrics(period_id, metric_code);
CREATE INDEX idx_stmt_line_period_type ON financial_statement_line_items(period_id, statement_type, line_code);
CREATE INDEX idx_recon_case_period ON financial_reconciliation_checks(case_id, period_id, status);
CREATE INDEX idx_bank_txn_case_date ON bank_transactions(case_id, txn_date);
CREATE INDEX idx_bank_summary_case_period ON bank_settlement_summaries(case_id, period_id);
CREATE INDEX idx_tax_company_period ON tax_filings(company_id, period_id);
CREATE INDEX idx_tax_invoice_check_case_period ON tax_invoice_consistency_checks(case_id, period_id, status);
CREATE INDEX idx_contracts_case ON contracts(case_id);
CREATE INDEX idx_related_party_case_period ON related_party_transaction_summaries(case_id, period_id);
CREATE INDEX idx_credit_history_case_subject ON credit_history_summaries(case_id, subject_type);
CREATE INDEX idx_invoices_case ON invoices(case_id);
CREATE INDEX idx_public_risk_case ON public_risk_events(case_id, severity);
CREATE INDEX idx_findings_case ON validation_findings(case_id, severity);
CREATE INDEX idx_scores_case_dim ON case_risk_scores(case_id, score_dimension);
