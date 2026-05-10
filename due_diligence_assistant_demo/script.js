const API_BASE = "";

const topSections = [
  { id: "risk-view", title: "风险洞察", summary: "围绕客户全景数据形成风险专题洞察。" },
  { id: "process-engine", title: "全流程引擎", summary: "围绕授信流程节点组织尽调、评级、方案、合同与贷后。" },
  { id: "knowledge-base", title: "知识库", summary: "沉淀法律法规、行内制度和专家经验文件。" },
  { id: "system-admin", title: "系统管理", summary: "管理用户、权限、菜单与操作日志。" },
];

const sidebarItems = {
  "risk-view": [
    { id: "basic-info", title: "基本信息" },
    { id: "operation-info", title: "经营情况" },
    { id: "shareholder-related", title: "股东及关联方" },
    { id: "financial-status", title: "财务状况" },
    { id: "external-industry", title: "外部环境与行业" },
    { id: "guarantor-info", title: "担保人信息" },
    { id: "collateral-info", title: "抵质押物" },
    { id: "other-risk", title: "其他" },
  ],
  "process-engine": [
    { id: "due-diligence", title: "尽职调查" },
    { id: "credit-rating", title: "信用评级" },
    { id: "credit-plan", title: "授信方案" },
    { id: "investigation-report", title: "授信调查报告" },
    { id: "contract-loan", title: "合同与放款" },
    { id: "post-loan", title: "贷后管理" },
  ],
  "knowledge-base": [
    { id: "laws", title: "法律法规" },
    { id: "policies", title: "行内制度" },
    { id: "experience", title: "专家经验" },
  ],
  "system-admin": [
    { id: "users", title: "用户管理" },
    { id: "roles", title: "角色管理" },
    { id: "permissions", title: "权限管理" },
    { id: "menus", title: "菜单配置" },
    { id: "knowledge-permissions", title: "知识库权限" },
    { id: "logs", title: "操作日志" },
  ],
};

const dueDiligenceTabs = [
  { id: "report-generate", title: "尽调报告生成" },
  { id: "report-review", title: "报告预审" },
];

const customerSections = [
  { id: "basic", title: "基本信息" },
  { id: "operation", title: "经营情况" },
  { id: "financial", title: "财务情况" },
  { id: "industry", title: "行业与外部环境信息" },
  { id: "collateral", title: "抵质押物" },
  { id: "other", title: "其他" },
];

const materialBucketDescriptions = {
  application: ["授信申请书", "融资用途说明", "用款计划"],
  financial: ["财务报表", "银行流水", "纳税/发票材料", "销售合同/订单/回款材料"],
  governance: ["营业执照", "公司章程", "股东结构材料", "法人/实控人材料"],
  collateral: ["担保承诺", "抵押物权属材料", "评估报告", "质押清单"],
  external: ["行业研究", "舆情/处罚/涉诉材料", "外部数据平台截图或报告"],
  "manager-notes": ["现场尽调记录", "电话访谈纪要", "特殊风险说明", "其他补充备注"],
};

const reportDataSourceGroups = [
  {
    id: "customer-base",
    title: "客户与案例基础",
    description: "主体、案例、人员和企业画像基础数据。",
    items: [
      { id: "company", label: "企业主体信息" },
      { id: "case_info", label: "案例与授信申请信息" },
      { id: "people", label: "核心人员与角色信息" },
      { id: "profile_attributes", label: "补充画像属性" },
    ],
  },
  {
    id: "operation-flow",
    title: "经营与交易闭环",
    description: "主营经营、合同订单、开票和回款链路。",
    items: [
      { id: "contracts", label: "合同数据" },
      { id: "orders", label: "订单数据" },
      { id: "invoices", label: "发票数据" },
      { id: "bank_summaries", label: "银行摘要与回款" },
      { id: "related_transactions", label: "关联交易摘要" },
    ],
  },
  {
    id: "financial-check",
    title: "财务与核验",
    description: "财务指标、勾稽核验、税票和征信摘要。",
    items: [
      { id: "latest_metrics", label: "最新核心财务指标" },
      { id: "recent_metric_history", label: "近年财务趋势" },
      { id: "reconciliation_checks", label: "勾稽检查结果" },
      { id: "tax_invoice_checks", label: "税票一致性核验" },
      { id: "tax_filings", label: "纳税申报摘要" },
      { id: "credit_history", label: "信用历史摘要" },
    ],
  },
  {
    id: "external-governance",
    title: "外部环境与治理",
    description: "股权治理、行业外部环境、同业和公开风险。",
    items: [
      { id: "related_companies", label: "关联公司关系" },
      { id: "shareholding_changes", label: "股权变更记录" },
      { id: "industry_profile", label: "行业画像" },
      { id: "peer_comparisons", label: "同业比较" },
      { id: "public_risks", label: "公开风险事件" },
      { id: "public_info_enrichment", label: "公开信息补全层" },
    ],
  },
  {
    id: "guarantee-support",
    title: "担保与补件",
    description: "担保缓释、补件资料和风险建议。",
    items: [
      { id: "guarantees", label: "担保与抵质押信息" },
      { id: "due_diligence_materials", label: "尽调补充材料" },
      { id: "validation_findings", label: "核验发现" },
      { id: "recommendation", label: "授信建议与缓释要求" },
    ],
  },
];

const processPlaceholderMap = {
  "credit-rating": {
    title: "信用评级",
    metrics: ["评级要素", "评级结果", "评级说明"],
    cards: ["财务指标评分", "行业景气度评分", "行为与合规评分", "最终评级与敏感项说明"],
  },
  "credit-plan": {
    title: "授信方案",
    metrics: ["授信额度", "产品结构", "缓释措施"],
    cards: ["额度与期限设计", "产品与用途匹配", "第一/第二还款来源", "担保与抵质押配置"],
  },
  "investigation-report": {
    title: "授信调查报告",
    metrics: ["报告结构", "引用材料", "调查结论"],
    cards: ["调查报告草案", "引用材料汇总", "调查意见校验", "上报版结论摘要"],
  },
  "contract-loan": {
    title: "合同与放款",
    metrics: ["合同包", "条件落实", "放款校验"],
    cards: ["合同签署资料", "放款前条件清单", "受托支付/资金流向校验", "台账登记与放款结果"],
  },
  "post-loan": {
    title: "贷后管理",
    metrics: ["贷后监测", "预警事件", "整改跟踪"],
    cards: ["经营与财务监测", "风险预警时间线", "整改闭环记录", "贷后检查计划"],
  },
};

const statusPalette = {
  stable: { label: "稳定", className: "status-stable" },
  watch: { label: "关注", className: "status-watch" },
  pressure: { label: "高风险", className: "status-pressure" },
  open: { label: "已开放", className: "status-stable" },
  placeholder: { label: "框架中", className: "status-blue" },
  processing: { label: "生成中", className: "status-blue" },
  generated: { label: "已生成", className: "status-stable" },
  reviewed: { label: "已预审", className: "status-blue" },
  pending: { label: "待预审", className: "status-watch" },
  draft: { label: "草稿", className: "status-watch" },
};

const localizedPhrases = {
  "Builds high-precision industrial sensors for battery and equipment clients.": "面向电池及装备客户提供高精度工业传感器。",
  "Industrial Sensors": "工业传感器",
  "Tech Manufacturing": "科技制造",
  "Leverage remains elevated for public-company sample": "公开资料样本显示杠杆水平仍然偏高",
  "Balance sheet equation": "资产负债平衡关系",
  "Revenue minus COGS equals gross profit": "营业收入减营业成本等于毛利",
  "Capex versus fixed asset roll-forward": "资本开支与固定资产滚动勾稽",
  "Cash roll-forward": "现金滚动勾稽",
  "Net profit to operating cash conversion": "净利润向经营现金流转化",
  "Listed balance sheet equation": "上市公司资产负债平衡关系",
  "Public balance-sheet totals should tie out.": "公开口径下总资产、总负债与权益关系应保持勾稽一致。",
  "Gross margin consistency": "毛利率一致性核验",
  "A loose bridge between disclosed gross margin and revenue-cost spread.": "披露毛利率与收入成本差额之间需要保持可解释的一致关系。",
  "Net cash flow bridge": "净现金流勾稽",
  "Net cash flow should broadly reconcile to the three cash flow sections.": "净现金流应与经营、投资、筹资三部分现金流总体勾稽。",
  "Profit to operating cash conversion": "利润向经营现金流转化",
  "Cash conversion below 0.8x or negative should trigger follow-up.": "当利润转现金能力低于 0.8 倍或为负时，应触发后续跟踪。",
  "Collections from top industrial clients": "头部工业客户回款",
  "Supported in domestic substitution and industrial upgrade.": "受益于国产替代与产业升级政策支持。",
  "Capital intensive with high customer verification requirements.": "资本投入相对较高，客户验收与核验要求严格。",
  "Former sales manager labor dispute": "原销售经理劳动争议",
  "Tax bureau requested supplementary filing explanation": "税务机关要求补充申报说明",
  "Controller dilution is acceptable but points to capital pressure.": "实控人股权被稀释尚可接受，但反映出一定资本压力。",
  "Shares controller family links and short-term advances.": "与实控人家庭存在关联，并发生过短期资金往来。",
  "Pricing and settlement need supplementary explanation": "定价与结算安排仍需补充说明。",
  "Monthly settlement summary derived from seeded bank statement behavior.": "根据示例银行流水行为提炼的月度结算摘要。",
  "Revenue, invoice, and bank receipt consistency summary for demo tax dimension.": "收入、发票与银行回款一致性核验摘要。",
  "Total assets should equal liabilities plus equity.": "总资产应与负债及所有者权益合计一致。",
  "Gross profit should bridge cleanly from revenue and cost.": "营业收入与营业成本勾稽后应能准确推导毛利。",
  "High variance suggests capex or fixed asset roll-forward needs manual support.": "波动较大，说明资本开支或固定资产滚动关系仍需人工补证。",
  "Cash flow statement roll-forward should fully tie.": "现金流量表滚动关系应完整勾稽。",
  "Large gaps between profit and operating cash need working-capital explanation.": "利润与经营现金流偏离较大，需要结合营运资本变化解释。",
  "If used in credit workflow, supplement shareholder, legal representative, and exposure structure from external enterprise data providers.":
    "如用于授信流程，建议补充股东、法定代表人及授信敞口结构等外部企业信息。",
};

const localizedTokens = {
  medium_high: "中高风险",
  medium: "中风险",
  high: "高风险",
  listed_company_public_pack: "上市公司公开资料包",
  listed: "上市公司",
  "Not applicable": "暂不适用",
  pass: "通过",
  fail: "未通过",
  warn: "预警",
  active: "正常经营",
  listed_active: "正常上市经营",
  small: "小型企业",
  medium_enterprise: "中型企业",
  micro_enterprise_credit: "小微企业授信",
  public_pack_analysis: "公开资料分析",
  CEO: "首席执行官",
  CTO: "首席技术官",
  Tech: "科技",
  Manufacturing: "制造",
  Industrial: "工业",
  Sensors: "传感器",
  Guangdong: "广东",
  Shenzhen: "深圳",
  growth: "成长期",
  affiliate_supplier: "关联供应商",
  legal_representative: "法定代表人",
  finance_controller: "财务负责人",
  core_executive: "核心高管",
  guarantor: "担保人",
  equity_transfer: "股权转让",
  purchase: "采购",
  submitted: "已申报",
  VAT_summary: "增值税申报摘要",
  controller_joint_guarantee: "实控人连带保证",
  monthly_interest_bullet_principal: "按月付息、到期还本",
  admin_notice: "行政提示",
  labour_dispute: "劳动争议",
  low: "低",
  none: "无",
};

const state = {
  topSectionId: "risk-view",
  activeSidebarBySection: {
    "risk-view": "basic-info",
    "process-engine": "due-diligence",
    "knowledge-base": "laws",
    "system-admin": "users",
  },
  riskViewCompanyCode: null,
  processEngineCompanyCode: null,
  riskSearchKeyword: "",
  processSearchKeyword: "",
  knowledgeSearchKeyword: "",
  riskRecentCodes: [],
  processRecentCodes: [],
  dueDiligenceTabId: "report-generate",
  customerSectionId: "basic",
  reportVersionId: null,
  previewOpen: false,
  previewSectionId: null,
  pendingDataSourceSelection: [],
  riskCompletionMode: null,
  riskCompletionMenuOpen: false,
  completionModalOpen: false,
  completionModalType: null,
  completionModalField: null,
  riskCompletionUploads: {},
  riskManualEdits: {},
  riskManualDirtyFields: {},
  activeEditableField: null,
  riskCompletionSnapshot: null,
  pendingKnowledgeSelection: [],
  pendingKnowledgeVersionId: null,
  reportEditorText: "",
  reviewEditorText: "",
  companies: [],
  meta: null,
  knowledgeBase: null,
  systemAdmin: null,
  companyDetailCache: {},
  isGeneratingVersion: false,
  isRunningReview: false,
};

const topbarNavEl = document.getElementById("topbar-nav");
const sidebarContextEl = document.getElementById("sidebar-context");
const sidebarNavEl = document.getElementById("sidebar-nav");
const sidebarNoteEl = document.getElementById("sidebar-note");
const toolbarAreaEl = document.getElementById("toolbar-area");
const contentAreaEl = document.getElementById("content-area");
const previewOverlayEl = document.getElementById("preview-overlay");
const previewTitleEl = document.getElementById("preview-title");
const previewOutlineEl = document.getElementById("preview-outline");
const previewArticleEl = document.getElementById("preview-article");
const completionModalEl = document.getElementById("completion-modal");
const completionModalTitleEl = document.getElementById("completion-modal-title");
const completionModalBodyEl = document.getElementById("completion-modal-body");

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function fetchJson(url, options = {}) {
  return fetch(`${API_BASE}${url}`, options).then(async (response) => {
    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || `Request failed: ${response.status}`);
    }
    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) return null;
    return response.json();
  });
}

async function uploadFile(url, file) {
  const formData = new FormData();
  formData.append("file", file);
  return fetchJson(url, { method: "POST", body: formData });
}

function postJson(url, payload) {
  return fetchJson(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

function createStatusPill(key) {
  const item = statusPalette[key] || { label: key, className: "status-blue" };
  return `<span class="status-pill ${item.className}">${item.label}</span>`;
}

function compactText(value, fallback = "—") {
  if (!value) return fallback;
  return localizeText(String(value));
}

function localizeText(value) {
  let text = String(value ?? "");
  Object.entries(localizedPhrases).forEach(([source, target]) => {
    text = text.replaceAll(source, target);
  });
  Object.entries(localizedTokens).forEach(([source, target]) => {
    const escaped = source.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    text = text.replace(new RegExp(`\\b${escaped}\\b`, "g"), target);
  });
  return text;
}

function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  const num = Number(value);
  if (Math.abs(num) >= 100000000) return `${(num / 100000000).toFixed(2)} 亿元`;
  if (Math.abs(num) >= 10000) return `${(num / 10000).toFixed(2)} 万元`;
  return `${num.toLocaleString("zh-CN", { maximumFractionDigits: 2 })} 元`;
}

function formatPercent(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  return `${(Number(value) * 100).toFixed(2)}%`;
}

function formatRiskTier(value) {
  const mapping = {
    stable: "低风险",
    low: "低风险",
    medium: "中风险",
    medium_high: "中高风险",
    watch: "重点关注",
    high: "高风险",
    pressure: "高风险",
  };
  return mapping[String(value || "").toLowerCase()] || compactText(value, "未分层");
}

function formatRecommendationStatus(value) {
  const mapping = {
    public_pack_only: "仅公开资料模式",
    approve: "建议通过",
    review_required: "需人工复核",
    reject: "建议拒绝",
  };
  return mapping[String(value || "").toLowerCase()] || compactText(value, "—");
}

function toNumber(value) {
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
}

function formatNumber(value, digits = 2) {
  const num = toNumber(value);
  if (num === null) return "—";
  return num.toLocaleString("zh-CN", { minimumFractionDigits: 0, maximumFractionDigits: digits });
}

function formatMultiple(value) {
  const num = toNumber(value);
  if (num === null) return "—";
  return `${num.toFixed(2)} 倍`;
}

function formatPeriodLabel(periodCode) {
  const text = String(periodCode || "");
  if (!text) return "—";
  if (text.endsWith("FY")) return `${text.slice(0, 4)}年`;
  const annualDateMatched = text.match(/^(\d{4})1231$/);
  if (annualDateMatched) return `${annualDateMatched[1]}年`;
  const matched = text.match(/^(\d{4})-(\d{2})$/);
  if (matched) return `${matched[1]}年${matched[2]}月`;
  const fullDateMatched = text.match(/^(\d{4})(\d{2})(\d{2})$/);
  if (fullDateMatched) return `${fullDateMatched[1]}-${fullDateMatched[2]}-${fullDateMatched[3]}`;
  return text;
}

function getMetricMap(detail) {
  return Object.fromEntries((detail.latest_metrics || []).map((item) => [item.metric_code, item.value]));
}

function getAnnualSeries(detail, metricCode) {
  const series = (detail.recent_metric_history || [])
    .filter((item) => item.metric_code === metricCode && (String(item.period_code || "").endsWith("FY") || /^\d{4}1231$/.test(String(item.period_code || ""))))
    .map((item) => ({ period: item.period_code, value: toNumber(item.value) ?? 0 }))
    .sort((a, b) => String(a.period).localeCompare(String(b.period)));
  return series;
}

function computeChangeRatio(current, previous) {
  const currentNum = toNumber(current);
  const previousNum = toNumber(previous);
  if (currentNum === null || previousNum === null || previousNum === 0) return null;
  return (currentNum - previousNum) / Math.abs(previousNum);
}

function getTrendLabel(changeRatio) {
  const value = toNumber(changeRatio);
  if (value === null) return "待观察";
  if (Math.abs(value) < 0.03) return "基本稳定";
  return value > 0 ? "上升" : "下降";
}

function getToneLabel(tone) {
  if (tone === "stable") return "稳健";
  if (tone === "watch") return "关注";
  return "承压";
}

function getToneByStatus(status) {
  const value = String(status || "").toLowerCase();
  if (!value) return "watch";
  if (value === "pass") return "stable";
  if (value === "warn") return "watch";
  return "pressure";
}

function renderToneBadge(label, tone) {
  return `<span class="analysis-badge analysis-badge-${tone}">${escapeHtml(label)}</span>`;
}

function dedupeBy(items, getKey) {
  const seen = new Set();
  return items.filter((item) => {
    const key = getKey(item);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function getReceivableSnapshot(detail, recordType) {
  return (detail.receivables || []).find((item) => item.record_type === recordType) || null;
}

function buildFinancialSummary(detail) {
  const metrics = getMetricMap(detail);
  const revenueSeries = getAnnualSeries(detail, "revenue");
  const profitSeries = getAnnualSeries(detail, "net_profit");
  const revenueChange = computeChangeRatio(revenueSeries.at(-1)?.value, revenueSeries.at(-2)?.value);
  const profitChange = computeChangeRatio(profitSeries.at(-1)?.value, profitSeries.at(-2)?.value);
  const leverage = toNumber(metrics.asset_liability_ratio) ?? ((toNumber(metrics.total_assets) && toNumber(metrics.total_liabilities))
    ? toNumber(metrics.total_liabilities) / toNumber(metrics.total_assets)
    : null);
  const grossMargin = toNumber(metrics.gross_margin_pct) ?? ((toNumber(metrics.revenue) && toNumber(metrics.gross_profit))
    ? toNumber(metrics.gross_profit) / toNumber(metrics.revenue)
    : null);
  const cashFlowMargin = toNumber(metrics.operating_cash_flow_margin_pct) ?? ((toNumber(metrics.revenue) && toNumber(metrics.operating_cash_flow))
    ? toNumber(metrics.operating_cash_flow) / toNumber(metrics.revenue)
    : null);
  const receivable = getReceivableSnapshot(detail, "accounts_receivable");
  const bankSummary = detail.bank_summaries?.[0] || null;

  const dimensionCards = [
    {
      title: "偿债及杠杆",
      tone: leverage !== null && leverage <= 0.55 ? "stable" : leverage !== null && leverage <= 0.68 ? "watch" : "pressure",
      metrics: [
        { label: "资产负债率", value: formatPercent(leverage) },
        { label: "总负债", value: formatCurrency(metrics.total_liabilities) },
        { label: "经营现金流", value: formatCurrency(metrics.operating_cash_flow) },
      ],
      summary: leverage !== null && leverage <= 0.55 ? "整体杠杆仍在可接受区间，可重点跟踪债务结构与短债安排。" : "负债压力偏高，建议结合现金流与授信期限审慎判断承接能力。",
    },
    {
      title: "盈利能力",
      tone: grossMargin !== null && grossMargin >= 0.28 && toNumber(metrics.net_profit) > 0 ? "stable" : grossMargin !== null && grossMargin >= 0.2 ? "watch" : "pressure",
      metrics: [
        { label: "营业收入", value: formatCurrency(metrics.revenue) },
        { label: "净利润", value: formatCurrency(metrics.net_profit) },
        { label: "毛利率", value: formatPercent(grossMargin) },
      ],
      summary: toNumber(metrics.net_profit) > 0 ? "利润仍为正，但要继续确认利润增长是否真实转化为可回收现金。" : "利润表现偏弱，应优先关注毛利、费用和一次性收益的影响。",
    },
    {
      title: "营运能力",
      tone: receivable?.average_days && receivable.average_days <= 75 ? "stable" : receivable?.average_days && receivable.average_days <= 90 ? "watch" : "pressure",
      metrics: [
        { label: "应收账款", value: formatCurrency(metrics.accounts_receivable) },
        { label: "应收周转天数", value: receivable?.average_days ? `${formatNumber(receivable.average_days)} 天` : "—" },
        { label: "前五客户集中度", value: receivable?.top5_ratio_pct ? formatPercent(receivable.top5_ratio_pct) : "—" },
      ],
      summary: "回款链路是营运判断核心，建议联动合同、订单、发票和银行回款节奏一起看。",
    },
    {
      title: "规模",
      tone: toNumber(metrics.total_assets) >= 12000000 ? "stable" : "watch",
      metrics: [
        { label: "总资产", value: formatCurrency(metrics.total_assets) },
        { label: "固定资产", value: formatCurrency(metrics.fixed_assets) },
        { label: "资本开支", value: formatCurrency(metrics.capital_expenditure) },
      ],
      summary: "资产规模与产线投入已经形成一定底盘，后续重点看扩产是否继续沉淀为收入与现金。",
    },
    {
      title: "流动性",
      tone: cashFlowMargin !== null && cashFlowMargin >= 0.04 ? "stable" : cashFlowMargin !== null && cashFlowMargin >= 0 ? "watch" : "pressure",
      metrics: [
        { label: "经营现金流率", value: formatPercent(cashFlowMargin) },
        { label: "日均余额", value: formatCurrency(bankSummary?.average_daily_balance_cny) },
        { label: "月度净流量", value: formatCurrency(bankSummary?.net_flow_cny) },
      ],
      summary: cashFlowMargin !== null && cashFlowMargin >= 0 ? "现金流尚能覆盖经营需要，但仍需核验利润与回款转化质量。" : "流动性承压，应优先解释回款、备货和付款节奏的错配原因。",
    },
    {
      title: "成长性",
      tone: (revenueChange ?? -1) >= 0.08 && (profitChange ?? -1) >= 0.05 ? "stable" : (revenueChange ?? -1) >= 0 ? "watch" : "pressure",
      metrics: [
        { label: "收入同比", value: revenueChange === null ? "—" : formatPercent(revenueChange) },
        { label: "利润同比", value: profitChange === null ? "—" : formatPercent(profitChange) },
        { label: "收入趋势", value: getTrendLabel(revenueChange) },
      ],
      summary: revenueChange !== null && revenueChange > 0 ? "收入呈增长态势，但仍要确认增长质量与利润兑现程度是否同步。" : "增长动能偏弱，建议结合订单储备与客户结构继续判断可持续性。",
    },
  ];

  const highlightedChecks = dedupeBy(detail.reconciliation_checks || [], (item) => item.check_name).slice(0, 4);
  const taxCheck = detail.tax_invoice_checks?.[0] || null;

  const annualRevenue = revenueSeries.at(-1)?.value;
  const annualProfit = profitSeries.at(-1)?.value;
  const annualProfitPrev = profitSeries.at(-2)?.value;
  const annualRevenuePrev = revenueSeries.at(-2)?.value;

  return {
    dimensionCards,
    headline: {
      summary:
        highlightedChecks.some((item) => item.status === "fail")
          ? "当前财务页以“勾稽先看风险、指标再看支撑”为主线，重点提示利润与现金、资本开支与固定资产之间的解释压力。"
          : "当前财务页以“结论先行、指标支撑、趋势复核”为主线，整体财务表现可支撑基础授信判断。",
      chips: [
        { label: "最新报表", value: formatPeriodLabel(detail.latest_financial_period?.period_code) },
        { label: "收入同比", value: annualRevenue && annualRevenuePrev ? formatPercent(computeChangeRatio(annualRevenue, annualRevenuePrev)) : "—" },
        { label: "利润同比", value: annualProfit && annualProfitPrev ? formatPercent(computeChangeRatio(annualProfit, annualProfitPrev)) : "—" },
        { label: "勾稽异常", value: `${highlightedChecks.filter((item) => item.status !== "pass").length} 项` },
      ],
    },
    statementCards: [
      {
        title: "资产负债结构",
        tone: dimensionCards[0].tone,
        items: [
          `总资产：${formatCurrency(metrics.total_assets)}`,
          `总负债：${formatCurrency(metrics.total_liabilities)}`,
          `资产负债率：${formatPercent(leverage)}`,
          `固定资产：${formatCurrency(metrics.fixed_assets)}`,
        ],
      },
      {
        title: "损益质量",
        tone: dimensionCards[1].tone,
        items: [
          `营业收入：${formatCurrency(metrics.revenue)}`,
          `毛利：${formatCurrency(metrics.gross_profit)}`,
          `净利润：${formatCurrency(metrics.net_profit)}`,
          `毛利率：${formatPercent(grossMargin)}`,
        ],
      },
      {
        title: "现金回款与流水",
        tone: dimensionCards[4].tone,
        items: [
          `经营现金流：${formatCurrency(metrics.operating_cash_flow)}`,
          `月度流入：${formatCurrency(bankSummary?.inflow_total_cny)}`,
          `月度流出：${formatCurrency(bankSummary?.outflow_total_cny)}`,
          `日均余额：${formatCurrency(bankSummary?.average_daily_balance_cny)}`,
        ],
      },
      {
        title: "税票与一致性核验",
        tone: getToneByStatus(taxCheck?.status),
        items: [
          `收入申报：${formatCurrency(taxCheck?.declared_revenue_cny)}`,
          `开票金额：${formatCurrency(taxCheck?.invoiced_amount_cny)}`,
          `银行回款：${formatCurrency(taxCheck?.bank_receipts_cny)}`,
          `偏差比例：${formatPercent(taxCheck?.gap_ratio)}`,
        ],
      },
    ],
    trendCards: [
      {
        title: "收入与利润趋势",
        tone: dimensionCards[5].tone,
        series: [
          { label: "收入", data: revenueSeries, formatter: formatCurrency },
          { label: "净利润", data: profitSeries, formatter: formatCurrency },
        ],
        bullets: [
          `营业收入${annualRevenue && annualRevenuePrev ? `${formatPeriodLabel(revenueSeries.at(-1)?.period)}较上年${formatPercent(computeChangeRatio(annualRevenue, annualRevenuePrev))}` : "暂无完整同比口径"}`,
          `净利润${annualProfit && annualProfitPrev ? `${formatPeriodLabel(profitSeries.at(-1)?.period)}较上年${formatPercent(computeChangeRatio(annualProfit, annualProfitPrev))}` : "暂无完整同比口径"}`,
          "如收入增速明显快于利润兑现，需回看毛利率、费用率和回款节奏。",
        ],
      },
      {
        title: "营运资本与回款压力",
        tone: dimensionCards[2].tone,
        bullets: [
          `应收账款：${formatCurrency(metrics.accounts_receivable)}，其中逾期 90 天以上 ${formatCurrency(receivable?.overdue_over_90d_cny)}`,
          `前五客户集中度：${receivable?.top5_ratio_pct ? formatPercent(receivable.top5_ratio_pct) : "—"}，应重点观察单一客户延迟回款影响。`,
          `银行月度大额交易 ${bankSummary?.large_transaction_count ?? "—"} 笔，可结合合同与发票核验对应真实性。`,
        ],
      },
      {
        title: "勾稽与核验重点",
        tone: highlightedChecks.some((item) => item.status === "fail") ? "pressure" : highlightedChecks.some((item) => item.status === "warn") ? "watch" : "stable",
        checks: highlightedChecks,
      },
      {
        title: "阶段性结论",
        tone: highlightedChecks.some((item) => item.status === "fail") ? "pressure" : "watch",
        bullets: [
          dimensionCards.filter((item) => item.tone === "pressure").length
            ? `当前承压维度：${dimensionCards.filter((item) => item.tone === "pressure").map((item) => item.title).join("、")}`
            : "当前未出现明显失衡维度。",
          `重点补证方向：${taxCheck?.status === "warn" ? "税票与银行回款一致性、" : ""}资本开支与固定资产滚动、利润到现金的转化质量。`,
          "若进入授信审批，建议把回款监测、客户集中度和月度资金流水作为持续跟踪项。",
        ],
      },
    ],
  };
}

function renderFieldPanel(title, description, items, extraClass = "") {
  return `
    <article class="content-card ${extraClass}">
      <h3>${title}</h3>
      <p>${description}</p>
      ${renderFieldGrid(items)}
    </article>
  `;
}

function renderMiniTrend(series, formatter) {
  const values = series.map((item) => Math.abs(toNumber(item.value) ?? 0));
  const maxValue = Math.max(...values, 1);
  return `
    <div class="mini-trend">
      ${series
        .map((item) => {
          const width = `${Math.max((Math.abs(toNumber(item.value) ?? 0) / maxValue) * 100, 8)}%`;
          return `
            <div class="mini-trend-row">
              <span>${formatPeriodLabel(item.period)}</span>
              <div class="mini-trend-track"><i style="width:${width}"></i></div>
              <strong>${formatter(item.value)}</strong>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderOwnershipMap(detail, company) {
  const peopleNodes = detail.people.slice(0, 6).map((item) => {
    const badges = [
      item.is_actual_controller ? renderToneBadge("实控", "pressure") : "",
      item.is_guarantor ? renderToneBadge("担保", "watch") : "",
      item.equity_ratio ? renderToneBadge(`持股 ${formatPercent(item.equity_ratio)}`, "stable") : "",
    ]
      .filter(Boolean)
      .join("");
    return `
      <div class="graph-node graph-node-person">
        <strong>${escapeHtml(item.full_name)}</strong>
        <span>${escapeHtml(localizeText(item.title || item.role_type || "关键人员"))}</span>
        <div class="graph-chip-row">${badges || renderToneBadge("治理角色", "stable")}</div>
      </div>
    `;
  });

  const relatedTransactions = detail.related_transactions || [];
  const relatedNodes = detail.related_companies.slice(0, 5).map((item) => {
    const tx = relatedTransactions.find((txItem) => txItem.related_party_name === item.related_company_name);
    return `
      <div class="graph-node graph-node-related">
        <strong>${escapeHtml(item.related_company_name)}</strong>
        <span>${escapeHtml(localizeText(item.relation_type || "关联方"))}</span>
        <p>${escapeHtml(compactText(item.note || tx?.pricing_comment || "关注交易定价、结算节奏与资金占用情况。"))}</p>
        <div class="graph-chip-row">
          ${renderToneBadge(tx?.transaction_type ? localizeText(tx.transaction_type) : "关系链路", tx?.risk_level === "high" ? "pressure" : "watch")}
          ${tx?.transaction_amount_cny ? renderToneBadge(formatCurrency(tx.transaction_amount_cny), "stable") : ""}
        </div>
      </div>
    `;
  });

  const changeNodes = detail.shareholding_changes.slice(0, 4).map((item) => `
    <div class="graph-node graph-node-change">
      <strong>${escapeHtml(item.change_date || "—")}</strong>
      <span>${escapeHtml(localizeText(item.change_type || "股权调整"))}</span>
      <p>${escapeHtml(compactText(item.risk_comment || item.declared_reason || "待补充说明"))}</p>
    </div>
  `);

  const controller = detail.people.find((item) => item.is_actual_controller);
  const guarantors = detail.people.filter((item) => item.is_guarantor);
  const controllerSummary = controller
    ? `${controller.full_name}｜${localizeText(controller.title || controller.role_type || "实控人")}`
    : "待补充实控人信息";

  return `
    <section class="ownership-map-panel" style="margin-top: 20px;">
      <div class="inline-head">
        <div>
          <h3>企业关系图谱</h3>
          <p>以主体公司为中心，串联实控、核心人员、关联交易与股权变化，突出可视化识别能力。</p>
        </div>
        <div class="graph-chip-row">
          ${renderToneBadge(`实控链 ${controller ? "已识别" : "待补充"}`, controller ? "pressure" : "watch")}
          ${renderToneBadge(`关联方 ${detail.related_companies.length} 家`, "stable")}
          ${renderToneBadge(`股权变更 ${detail.shareholding_changes.length} 条`, "watch")}
        </div>
      </div>
      <div class="ownership-map">
        <section class="graph-branch graph-branch-left">
          <div class="graph-branch-title">
            <h4>核心人物与控制链</h4>
            <p>重点看法人、实控人、财务负责人及担保关系。</p>
          </div>
          <div class="graph-node-stack">${peopleNodes.join("")}</div>
        </section>
        <div class="graph-core">
          <div class="graph-core-card">
            <span class="graph-core-kicker">主体公司</span>
            <h3>${escapeHtml(company.name)}</h3>
            <p>${escapeHtml(compactText(company.overview || "暂无企业摘要"))}</p>
            <div class="graph-core-metrics">
              <div><strong>${escapeHtml(controllerSummary)}</strong><span>控制核心</span></div>
              <div><strong>${guarantors.length} 名</strong><span>担保关联人</span></div>
              <div><strong>${detail.related_transactions.length} 条</strong><span>关联交易摘要</span></div>
            </div>
          </div>
        </div>
        <section class="graph-branch graph-branch-right">
          <div class="graph-cluster graph-cluster-related">
            <div class="graph-branch-title">
              <h4>关联企业与交易</h4>
              <p>观察交易类型、结算金额与关联路径。</p>
            </div>
            <div class="graph-node-stack">${relatedNodes.length ? relatedNodes.join("") : '<div class="graph-node graph-node-related"><strong>暂无数据</strong><p>可补充关联企业与交易摘要。</p></div>'}</div>
          </div>
          <div class="graph-cluster graph-cluster-change">
            <div class="graph-branch-title">
              <h4>股权变更与控制波动</h4>
              <p>突出持股变化、技术激励和资本压力信号。</p>
            </div>
            <div class="graph-node-stack">${changeNodes.length ? changeNodes.join("") : '<div class="graph-node graph-node-change"><strong>暂无变更</strong><p>当前未发现股权变更记录。</p></div>'}</div>
          </div>
        </section>
      </div>
    </section>
  `;
}

function renderFinancialDashboard(detail) {
  const summary = buildFinancialSummary(detail);
  return `
    <section class="finance-dashboard" style="margin-top: 20px;">
      <article class="finance-headline-card">
        <div class="inline-head">
          <div>
            <h3>财务判断摘要</h3>
            <p>${summary.headline.summary}</p>
          </div>
          <div class="graph-chip-row">
            ${summary.headline.chips.map((item) => renderToneBadge(`${item.label}：${item.value}`, "stable")).join("")}
          </div>
        </div>
      </article>

      <section class="finance-section">
        <div class="finance-section-head">
          <div>
            <h3>六维财务体检</h3>
            <p>风控先看结论，再展开关键指标与解释方向。</p>
          </div>
        </div>
        <div class="finance-dimension-grid">
          ${summary.dimensionCards
            .map(
              (card) => `
                <article class="finance-dimension-card finance-dimension-card-${card.tone}">
                  <div class="dimension-head">
                    <h4>${card.title}</h4>
                    ${renderToneBadge(getToneLabel(card.tone), card.tone)}
                  </div>
                  <div class="dimension-metrics">
                    ${card.metrics
                      .map(
                        (item) => `
                          <div class="dimension-metric-row">
                            <span>${item.label}</span>
                            <strong>${item.value}</strong>
                          </div>
                        `,
                      )
                      .join("")}
                  </div>
                  <p>${card.summary}</p>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>

      <section class="finance-section">
        <div class="finance-section-head">
          <div>
            <h3>当年财务数据分析</h3>
            <p>聚焦本期资产负债、损益质量、流水承接与税票一致性。</p>
          </div>
        </div>
        <div class="two-col-grid">
          ${summary.statementCards
            .map(
              (card) => `
                <article class="finance-panel-card finance-panel-card-${card.tone}">
                  <div class="dimension-head">
                    <h4>${card.title}</h4>
                    ${renderToneBadge(getToneLabel(card.tone), card.tone)}
                  </div>
                  <div class="finance-bullet-list">
                    ${card.items.map((item) => `<div class="finance-bullet-item">${escapeHtml(localizeText(item))}</div>`).join("")}
                  </div>
                </article>
              `,
            )
            .join("")}
        </div>
      </section>

      <section class="finance-section">
        <div class="finance-section-head">
          <div>
            <h3>趋势与勾稽分析</h3>
            <p>结合近年趋势、营运资本变化和勾稽检查，解释风险来源。</p>
          </div>
        </div>
        <div class="two-col-grid">
          ${summary.trendCards
            .map((card) => {
              const trendHtml = card.series
                ? card.series
                    .map(
                      (item) => `
                        <div class="trend-group">
                          <div class="trend-group-label">${item.label}</div>
                          ${renderMiniTrend(item.data, item.formatter)}
                        </div>
                      `,
                    )
                    .join("")
                : "";
              const checksHtml = card.checks
                ? card.checks
                    .map(
                      (item) => `
                        <div class="check-item">
                          <div class="check-item-head">
                            <strong>${escapeHtml(localizeText(item.check_name || "勾稽检查"))}</strong>
                            ${renderToneBadge(compactText(item.status), getToneByStatus(item.status))}
                          </div>
                          <p>${escapeHtml(compactText(item.interpretation || "待补充解释"))}</p>
                        </div>
                      `,
                    )
                    .join("")
                : "";
              const bulletsHtml = card.bullets
                ? `<div class="finance-bullet-list">${card.bullets.map((item) => `<div class="finance-bullet-item">${escapeHtml(localizeText(item))}</div>`).join("")}</div>`
                : "";
              return `
                <article class="finance-panel-card finance-panel-card-${card.tone}">
                  <div class="dimension-head">
                    <h4>${card.title}</h4>
                    ${renderToneBadge(getToneLabel(card.tone), card.tone)}
                  </div>
                  ${trendHtml}
                  ${checksHtml}
                  ${bulletsHtml}
                </article>
              `;
            })
            .join("")}
        </div>
      </section>
    </section>
  `;
}

function formatDataMode(value) {
  return value === "public_pack" ? "原始资料清单" : "完整尽调案例";
}

function getRiskDataInventory(activeId, detail = {}) {
  const inventoryMap = {
    "basic-info": ["企业工商基础信息", "统一社会信用代码", "成立日期及注册资本", "注册地与所属行业", "风险标签与案例编号"],
    "operation-info": ["经营状态", "企业规模", "授信申请产品", "第一还款来源", "合同/订单/发票/银行流水摘要"],
    "shareholder-related": ["核心人员信息", "股东及实控关系", "关联企业清单", "股权变更记录", "关联交易摘要"],
    "financial-status": ["近年财务指标", "资产负债表关键科目", "利润与现金流指标", "银行流水摘要", "财务勾稽核验结果"],
    "external-industry": ["行业分类", "政策环境", "生命周期判断", "公开风险事件", "同业经营及财务对比"],
    "guarantor-info": ["担保人身份材料", "担保关系说明", "保证能力证明", "征信或负债摘要", "担保承诺文件"],
    "collateral-info": ["抵质押物权属材料", "评估报告", "质押/抵押清单", "押品状态说明", "可处置性补充材料"],
    "other-risk": ["人工补件说明", "现场尽调备注", "特殊事项说明", "核验发现", "报告章节引用信息"],
  };
  const base = inventoryMap[activeId] || [];
  const uploaded = detail.due_diligence_materials?.length ? [`已上传资料 ${detail.due_diligence_materials.length} 份`] : ["当前未读取到人工上传材料"];
  return [...base, uploaded];
}

function getRiskFieldKey(item) {
  return `${getActiveSidebarItem()?.id || "risk"}:${item.label}`;
}

function renderCompletionUploadSlot(fieldKey, compact = false) {
  const files = state.riskCompletionUploads[fieldKey] || [];
  return `
    <div class="${compact ? "field-upload-slot field-upload-slot-compact" : "field-upload-slot"}">
      <input type="file" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg" data-risk-completion-upload="${escapeHtml(fieldKey)}" />
      <span>${files.length ? files.map(escapeHtml).join("、") : "尚未上传佐证材料"}</span>
    </div>
  `;
}

function getAllReportDataSourceIds() {
  return reportDataSourceGroups.flatMap((group) => group.items.map((item) => item.id));
}

function getReportDataSourceGroups(detail) {
  return reportDataSourceGroups.map((group) => ({
    ...group,
    items: group.items.map((item) => {
      const value = detail?.[item.id];
      const count = Array.isArray(value) ? value.length : value && typeof value === "object" ? Object.keys(value).length : value ? 1 : 0;
      return {
        ...item,
        countLabel: Array.isArray(value) ? `${count} 条` : count ? "已接入" : "待补充",
      };
    }),
  }));
}

function getSelectedKnowledgeFiles() {
  const fileMap = new Map((state.knowledgeBase?.files || []).map((item) => [item.id, item]));
  return state.pendingKnowledgeSelection.map((id) => fileMap.get(id)).filter(Boolean);
}

function renderDataCompletionControl() {
  if (state.topSectionId !== "risk-view" || !state.riskViewCompanyCode) return "";
  const modeLabel = state.riskCompletionMode === "manual" ? "手动修改中" : state.riskCompletionMode === "ai" ? "AI识别中" : "资料完善";
  return `
    <div class="completion-control">
      <div class="completion-action-row">
        <button class="secondary-action completion-trigger" type="button" data-action="toggle-completion-menu">${modeLabel}</button>
        ${state.riskCompletionMode ? '<button class="ghost-action completion-done" type="button" data-action="finish-completion-mode">完成修改</button>' : ""}
        ${state.riskCompletionMode ? '<button class="ghost-action completion-cancel" type="button" data-action="cancel-completion-mode">取消修改</button>' : ""}
      </div>
      <div class="completion-menu${state.riskCompletionMenuOpen ? " is-open" : ""}">
        <button type="button" data-action="set-completion-mode" data-mode="manual">手动修改</button>
        <button type="button" data-action="set-completion-mode" data-mode="ai">AI识别</button>
      </div>
    </div>
  `;
}

function getDirtyManualFieldsForSection(sectionId = getActiveSidebarItem()?.id) {
  if (!sectionId) return [];
  return Object.keys(state.riskManualDirtyFields).filter((key) => key.startsWith(`${sectionId}:`));
}

function promptManualEvidenceForSection(sectionId = getActiveSidebarItem()?.id, preferredFieldKey = null) {
  const dirtyFields = getDirtyManualFieldsForSection(sectionId);
  if (!dirtyFields.length) return false;
  state.completionModalOpen = true;
  state.completionModalType = "manual";
  state.completionModalField = preferredFieldKey && dirtyFields.includes(preferredFieldKey) ? preferredFieldKey : dirtyFields[0];
  renderCompletionModal();
  return true;
}

function createCompletionSnapshot() {
  return {
    riskCompletionUploads: { ...state.riskCompletionUploads },
    riskManualEdits: { ...state.riskManualEdits },
    riskManualDirtyFields: { ...state.riskManualDirtyFields },
    activeEditableField: state.activeEditableField,
  };
}

function restoreCompletionSnapshot() {
  const snapshot = state.riskCompletionSnapshot;
  state.riskCompletionUploads = snapshot ? { ...snapshot.riskCompletionUploads } : {};
  state.riskManualEdits = snapshot ? { ...snapshot.riskManualEdits } : {};
  state.riskManualDirtyFields = snapshot ? { ...snapshot.riskManualDirtyFields } : {};
  state.activeEditableField = snapshot?.activeEditableField || null;
}

function clearCompletionSession() {
  state.riskCompletionMode = null;
  state.riskCompletionMenuOpen = false;
  state.completionModalOpen = false;
  state.completionModalType = null;
  state.completionModalField = null;
  state.activeEditableField = null;
  state.riskCompletionSnapshot = null;
}

function getSectionHasCompany(sectionId) {
  return sectionId === "risk-view" ? Boolean(state.riskViewCompanyCode) : Boolean(state.processEngineCompanyCode);
}

function getCurrentTopSection() {
  return topSections.find((item) => item.id === state.topSectionId) || topSections[0];
}

function getSidebarItems() {
  return sidebarItems[state.topSectionId] || [];
}

function getActiveSidebarItem() {
  const currentId = state.activeSidebarBySection[state.topSectionId];
  return getSidebarItems().find((item) => item.id === currentId) || getSidebarItems()[0];
}

function getCurrentCompanyCode() {
  if (state.topSectionId === "risk-view") return state.riskViewCompanyCode;
  if (state.topSectionId === "process-engine") return state.processEngineCompanyCode;
  return null;
}

function getCurrentRecentCodes() {
  if (state.topSectionId === "risk-view") return state.riskRecentCodes;
  if (state.topSectionId === "process-engine") return state.processRecentCodes;
  return [];
}

function getCompanySummary(companyCode) {
  return state.companies.find((item) => item.company_code === companyCode) || null;
}

function getCompanyDetail(companyCode) {
  return companyCode ? state.companyDetailCache[companyCode] || null : null;
}

async function ensureCompanyDetail(companyCode) {
  if (!companyCode) return null;
  if (state.companyDetailCache[companyCode]) return state.companyDetailCache[companyCode];
  const detail = await fetchJson(`/api/company/${encodeURIComponent(companyCode)}`);
  state.companyDetailCache[companyCode] = detail;
  return detail;
}

async function refreshCompanyDetail(companyCode) {
  if (!companyCode) return null;
  const detail = await fetchJson(`/api/company/${encodeURIComponent(companyCode)}`);
  state.companyDetailCache[companyCode] = detail;
  syncSelectedVersion(detail);
  syncKnowledgeSelection(detail);
  return detail;
}

function syncSelectedVersion(detail) {
  if (!detail?.report_versions?.length) {
    state.reportVersionId = null;
    return;
  }
  const matched = detail.report_versions.find((item) => item.id === state.reportVersionId);
  state.reportVersionId = matched ? matched.id : detail.report_versions[detail.report_versions.length - 1].id;
}

function getCurrentVersion(detail = getCompanyDetail(state.processEngineCompanyCode)) {
  if (!detail?.report_versions?.length) return null;
  return detail.report_versions.find((item) => item.id === state.reportVersionId) || detail.report_versions[detail.report_versions.length - 1];
}

function syncKnowledgeSelection(detail) {
  const version = getCurrentVersion(detail);
  if (!version) {
    state.pendingKnowledgeVersionId = null;
    state.pendingKnowledgeSelection = [];
    state.pendingDataSourceSelection = getAllReportDataSourceIds();
    state.reportEditorText = "";
    state.reviewEditorText = "";
    return;
  }
  if (state.pendingKnowledgeVersionId !== version.id) {
    state.pendingKnowledgeVersionId = version.id;
    state.pendingKnowledgeSelection = version.knowledge_files.map((item) => item.id);
    state.pendingDataSourceSelection = version.selected_data_source_ids?.length ? [...version.selected_data_source_ids] : getAllReportDataSourceIds();
    state.reportEditorText = version.full_text || "";
    state.reviewEditorText = version.review_edit_text || version.full_text || "";
  }
}

function rememberCompany(sectionId, companyCode) {
  const key = sectionId === "risk-view" ? "riskRecentCodes" : "processRecentCodes";
  state[key] = [companyCode, ...state[key].filter((item) => item !== companyCode)].slice(0, 6);
}

async function selectCompany(sectionId, companyCode) {
  if (sectionId === "risk-view") state.riskViewCompanyCode = companyCode;
  if (sectionId === "process-engine") state.processEngineCompanyCode = companyCode;
  rememberCompany(sectionId, companyCode);
  await ensureCompanyDetail(companyCode);
  if (sectionId === "process-engine") {
    const detail = getCompanyDetail(companyCode);
    syncSelectedVersion(detail);
    syncKnowledgeSelection(detail);
  }
}

async function searchCompany(sectionId) {
  const keyword = sectionId === "risk-view" ? state.riskSearchKeyword.trim() : state.processSearchKeyword.trim();
  if (!keyword) return;
  const matched = state.companies.find((item) => item.name.includes(keyword));
  if (!matched) {
    window.alert("未找到匹配企业，请尝试点击下方示例企业。");
    return;
  }
  await selectCompany(sectionId, matched.company_code);
  render();
}

function renderTopbar() {
  topbarNavEl.innerHTML = topSections
    .map(
      (item) => `
        <button
          class="topbar-nav-item${item.id === state.topSectionId ? " is-active" : ""}"
          type="button"
          data-action="switch-top-section"
          data-top-section="${item.id}"
        >${item.title}</button>
      `,
    )
    .join("");
}

function renderSidebar() {
  const topSection = getCurrentTopSection();
  const activeSidebar = getActiveSidebarItem();
  const currentCompanyCode = getCurrentCompanyCode();

  if (topSection.id === "risk-view" || topSection.id === "process-engine") {
    sidebarContextEl.innerHTML = "";
    sidebarNoteEl.innerHTML = "";
    sidebarContextEl.style.display = "none";
    sidebarNoteEl.style.display = "none";
  } else {
    sidebarContextEl.style.display = "";
    sidebarNoteEl.style.display = "";
    sidebarContextEl.innerHTML = `
      <p class="section-kicker">${topSection.title}</p>
      <h2>${topSection.title}</h2>
      <p>${topSection.summary}</p>
    `;
    const note = {
      "knowledge-base": "知识库文件可上传、查看，并在尽调报告生成时按分类多选引用。",
      "system-admin": "系统管理用于展示用户、权限、菜单、知识权限与日志等后台能力。",
    }[topSection.id];

    sidebarNoteEl.innerHTML = `
      <p class="section-kicker">当前说明</p>
      <p>${note}</p>
      <p style="margin-top: 10px;"><strong>当前菜单：</strong>${activeSidebar.title}</p>
    `;
  }

  sidebarNavEl.innerHTML = getSidebarItems()
    .map(
      (item) => `
        <button
          class="sidebar-nav-item${item.id === activeSidebar.id ? " is-active" : ""}"
          type="button"
          data-action="switch-sidebar-item"
          data-sidebar-id="${item.id}"
        >${item.title}</button>
      `,
    )
    .join("");
}

function renderSearchToolbar(sectionId, title, subtitle) {
  const companyCode = sectionId === "risk-view" ? state.riskViewCompanyCode : state.processEngineCompanyCode;
  const company = getCompanySummary(companyCode);
  const recentCodes = sectionId === "risk-view" ? state.riskRecentCodes : state.processRecentCodes;
  const searchValue = sectionId === "risk-view" ? state.riskSearchKeyword : state.processSearchKeyword;
  const detail = getCompanyDetail(companyCode);
  const statCards = sectionId === "process-engine"
    ? []
    : company
    ? sectionId === "risk-view"
      ? [
          {
            value: formatDataMode(company.data_mode),
            label: "数据模式",
            inventory: getRiskDataInventory(getActiveSidebarItem().id, detail),
          },
        ]
      : [
          { value: formatRiskTier(company.risk_tier), label: "风险分层" },
          { value: detail?.report_versions?.length ? `${detail.report_versions.length} 个版本` : "待生成", label: "尽调报告" },
          { value: formatDataMode(company.data_mode), label: "数据模式" },
        ]
    : sectionId === "risk-view"
      ? []
      : [
          { value: "待选择", label: "当前企业" },
          { value: "流程工作区", label: "当前模式" },
          { value: "请输入企业名称", label: "下一步" },
        ];

  const companySummaryCard = company
    ? `
      <article class="panel-card company-summary-card">
        <div class="inline-head">
          <div>
            <h3>${escapeHtml(company.name)}</h3>
            <p>${escapeHtml(compactText(company.overview || "当前已选中企业，可继续查看右侧专题内容。"))}</p>
          </div>
          <button class="ghost-action" type="button" data-action="reset-company-search" data-section-id="${sectionId}">重新搜索</button>
        </div>
      </article>
    `
    : `
      <article class="panel-card">
        <h3>企业搜索</h3>
        <p>当前板块独立维护企业上下文，切换到另一个主栏不会自动带过去。</p>
        <div class="button-row" style="margin-top: 14px;">
          <input
            class="search-box"
            id="${sectionId}-search-input"
            placeholder="请输入企业名称，例如深圳市灵犀微传感科技有限公司"
            value="${escapeHtml(searchValue)}"
          />
          <button class="primary-action" type="button" data-action="search-company" data-section-id="${sectionId}">搜索企业</button>
        </div>
        <div class="pill-row" style="margin-top: 14px;">
          ${recentCodes.length
            ? recentCodes
                .map((code) => {
                  const item = getCompanySummary(code);
                  if (!item) return "";
                  return `
                    <button
                      class="pill-button${code === companyCode ? " is-active" : ""}"
                      type="button"
                      data-action="select-company"
                      data-section-id="${sectionId}"
                      data-company-code="${code}"
                    >${escapeHtml(item.name)}</button>
                  `;
                })
                .join("")
            : '<span class="muted-text">暂无最近查看企业</span>'}
        </div>
      </article>
    `;

  toolbarAreaEl.innerHTML = `
    <section class="hero-card">
      <div class="hero-head">
        <div>
          <p class="section-kicker">${sectionId === "risk-view" ? "风险洞察" : "全流程引擎"}</p>
          <h2>${title}</h2>
          <p>${subtitle}</p>
        </div>
        ${sectionId === "risk-view" ? renderDataCompletionControl() : ""}
      </div>

      <div class="toolbar-grid${sectionId === "risk-view" && company ? " risk-toolbar-grid" : ""}${!statCards.length ? " toolbar-grid-no-stats" : ""}">
        ${companySummaryCard}

        ${statCards.length
          ? `<div class="stats-grid">
              ${statCards
                .map(
                  (item) => `
                    <article class="metric-card">
                      <strong class="metric-value">${escapeHtml(item.value)}</strong>
                      <span class="metric-label">${item.label}</span>
                      ${item.inventory
                        ? `<div class="inventory-popover">${item.inventory.map((entry) => `<span>${escapeHtml(entry)}</span>`).join("")}</div>`
                        : ""}
                    </article>
                  `,
                )
                .join("")}
            </div>`
          : ""}
      </div>
    </section>
  `;
}

function renderKnowledgeToolbar() {
  const active = getActiveSidebarItem();
  const categoryTitle = active.title;
  const total = (state.knowledgeBase?.files || []).filter((item) => item.category === active.id).length;
  toolbarAreaEl.innerHTML = `
    <section class="hero-card">
      <div class="hero-head">
        <div>
          <p class="section-kicker">知识库</p>
          <h2>${categoryTitle}</h2>
          <p>用于沉淀可被尽调报告生成引用的知识文件，支持 PDF / Word 上传与分类管理。</p>
        </div>
      </div>
      <div class="toolbar-grid">
        <article class="panel-card">
          <h3>文件检索</h3>
          <p>可按文件名快速过滤当前分类中的文件。</p>
          <div class="button-row" style="margin-top: 14px;">
            <input
              class="search-box"
              id="knowledge-search-input"
              placeholder="请输入文件名关键字"
              value="${escapeHtml(state.knowledgeSearchKeyword)}"
            />
          </div>
        </article>
        <div class="stats-grid">
          <article class="metric-card">
            <strong class="metric-value">${total}</strong>
            <span class="metric-label">当前分类文件数</span>
          </article>
          <article class="metric-card">
            <strong class="metric-value">${state.knowledgeBase?.categories?.length || 3}</strong>
            <span class="metric-label">知识分类</span>
          </article>
          <article class="metric-card">
            <strong class="metric-value">可引用</strong>
            <span class="metric-label">支持尽调报告生成引用</span>
          </article>
        </div>
      </div>
    </section>
  `;
}

function renderSystemToolbar() {
  const active = getActiveSidebarItem();
  toolbarAreaEl.innerHTML = `
    <section class="hero-card">
      <div class="hero-head">
        <div>
          <p class="section-kicker">系统管理</p>
          <h2>${active.title}</h2>
          <p>以基础后台视角展示用户、角色、权限、知识权限和操作日志等平台管理能力。</p>
        </div>
      </div>
      <div class="stats-grid" style="margin-top: 22px;">
        <article class="metric-card">
          <strong class="metric-value">${state.systemAdmin?.users?.length || 0}</strong>
          <span class="metric-label">用户数量</span>
        </article>
        <article class="metric-card">
          <strong class="metric-value">${state.systemAdmin?.roles?.length || 0}</strong>
          <span class="metric-label">角色数量</span>
        </article>
        <article class="metric-card">
          <strong class="metric-value">${state.systemAdmin?.logs?.length || 0}</strong>
          <span class="metric-label">近期操作日志</span>
        </article>
      </div>
    </section>
  `;
}

function renderToolbar() {
  if (state.topSectionId === "risk-view") {
    renderSearchToolbar("risk-view", getActiveSidebarItem().title, "客户全景风险洞察，用于按专题查看主体、经营、财务、关联方和外部环境等风险信息。");
    return;
  }
  if (state.topSectionId === "process-engine") {
    renderSearchToolbar("process-engine", getActiveSidebarItem().title, "全流程引擎围绕授信节点组织作业，当前 POC 以“尽职调查”作为最深实现模块。");
    return;
  }
  if (state.topSectionId === "knowledge-base") {
    renderKnowledgeToolbar();
    return;
  }
  renderSystemToolbar();
}

function renderFieldGrid(items) {
  const editable = state.topSectionId === "risk-view" && state.riskCompletionMode === "manual";
  const aiMode = state.topSectionId === "risk-view" && state.riskCompletionMode === "ai";
  return `
    <div class="field-grid">
      ${items
        .map((item) => {
          const fieldKey = getRiskFieldKey(item);
          const displayValue = state.riskManualEdits[fieldKey] ?? item.value;
          return `
            <div class="field-item${editable ? " is-editable" : ""}">
              <strong>${escapeHtml(item.label)}</strong>
              <span
                ${editable ? 'contenteditable="true" spellcheck="false"' : ""}
                ${editable ? `data-editable-field="${escapeHtml(fieldKey)}"` : ""}
                ${editable ? `data-original-value="${escapeHtml(item.value)}"` : ""}
              >${escapeHtml(displayValue)}</span>
              ${aiMode ? renderCompletionUploadSlot(fieldKey, true) : ""}
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderListStack(title, description, items) {
  return `
    <article class="content-card">
      <h3>${title}</h3>
      <p>${description}</p>
      <div class="list-stack" style="margin-top: 16px;">
        ${items.length
          ? items.map((item) => `<div class="list-item">${item}</div>`).join("")
          : '<div class="list-item">暂无数据</div>'}
      </div>
    </article>
  `;
}

function renderBydIndustryAnalysis(detail) {
  const industryItems = [
    { label: "产业位置", value: "新能源汽车整车制造，覆盖乘用车、商用车、动力电池及储能，具备电池、电驱、电控等核心环节纵向一体化能力。" },
    { label: "行业周期", value: "行业已由高速渗透期进入规模化竞争和结构分化阶段，需求仍受以旧换新、出口、智能化配置升级支撑，但价格竞争和渠道库存管理压力上升。" },
    { label: "政策方向", value: "国家层面延续汽车以旧换新、新能源汽车购置税优惠、充换电基础设施完善与智能网联汽车试点等支持方向，政策重心从单纯补贴转向消费更新、技术安全和高质量出海。" },
    { label: "授信关注", value: "银行授信应重点观察销量增长质量、盈利韧性、经营现金流、海外扩张回款、供应链议价和研发资本化/费用化对利润的影响。" },
  ];
  const peerItems = [
    "AI分析｜比亚迪 2025 年新能源汽车销量约 460.2 万辆，规模优势和垂直整合能力突出，收入体量继续位居国内新能源车企前列。",
    "与特斯拉相比，比亚迪车型价格带更宽、插混与纯电并重，国内市场覆盖更深；特斯拉单车盈利和全球品牌溢价仍具优势。",
    "与吉利、长安、上汽等自主集团相比，比亚迪新能源转型更彻底，电池和电驱自研比例更高；但在白热化竞争下，盈利波动和经销/库存节奏需持续跟踪。",
    "同业比对结论：当前外部环境对头部新能源车企仍属支持，但风险从政策准入转向价格战、海外合规、产品迭代和现金流兑现能力。",
  ];
  return `
    <div class="two-col-grid" style="margin-top: 20px;">
      <article class="content-card industry-analysis-card">
        <div class="inline-head">
          <div>
            <h3>行业与政策环境</h3>
            <p>从政策、周期、竞争格局和授信影响四个维度观察外部环境。</p>
          </div>
          ${renderToneBadge("政策支持 / 竞争加剧", "watch")}
        </div>
        ${renderFieldGrid(industryItems)}
        <div class="divider"></div>
        <div class="finance-bullet-list">
          <div class="finance-bullet-item">汽车以旧换新政策继续拉动置换需求，新能源乘用车报废更新补贴仍是消费端重要支撑。</div>
          <div class="finance-bullet-item">行业竞争由“渗透率提升”转向“份额、成本、智能化和出海能力”综合竞争，价格战会压缩中短期利润空间。</div>
          <div class="finance-bullet-item">对授信而言，头部企业信用基础较强，但仍应把经营现金流、应收/存货周转和海外业务合规作为动态监测指标。</div>
        </div>
      </article>
      <article class="content-card peer-analysis-card">
        <div class="inline-head">
          <div>
            <h3>与同业比对</h3>
            <p>POC 阶段固定展示比亚迪同业分析，后续可接入公开数据自动更新。</p>
          </div>
          ${renderToneBadge("AI分析", "stable")}
        </div>
        <div class="list-stack" style="margin-top: 16px;">
          ${peerItems.map((item) => `<div class="list-item">${escapeHtml(item)}</div>`).join("")}
        </div>
      </article>
    </div>
  `;
}

function renderManualMaterialCard(title, suggestions, bucket) {
  const key = `${bucket}:手动补充材料`;
  return `
    <article class="upload-card manual-material-card">
      <h3>${title}</h3>
      <p>建议收集：${suggestions.join("、")}</p>
      <div class="divider"></div>
      ${renderCompletionUploadSlot(key)}
      <div class="upload-stack" style="margin-top: 16px;">
        <div class="upload-item">当前分组尚未上传文件</div>
      </div>
    </article>
  `;
}

function renderRiskView() {
  const companyCode = state.riskViewCompanyCode;
  const company = getCompanySummary(companyCode);
  const detail = getCompanyDetail(companyCode);
  const active = getActiveSidebarItem();

  if (!company || !detail) {
    contentAreaEl.innerHTML = `
      <div class="empty-state">
        <h3>请先在风险洞察中搜索企业</h3>
        <p>搜索后即可查看基本信息、经营情况、股东及关联方、财务状况、外部环境与行业、担保人信息、抵质押物等风险专题页面。</p>
      </div>
    `;
    return;
  }

  if (active.id === "basic-info") {
    const tags = [
      { value: company.company_code, label: "企业代码" },
      { value: formatRiskTier(company.risk_tier), label: "风险分层" },
      { value: compactText(detail.case_info?.case_no), label: "案例编号" },
      { value: formatDataMode(company.data_mode), label: "数据模式" },
    ];
    contentAreaEl.innerHTML = `
      <div class="two-col-grid" style="margin-top: 20px;">
        <article class="content-card">
          <h3>主体基础画像</h3>
          <p>用于识别企业主体、地区、行业与准入基础信息。</p>
          ${renderFieldGrid([
            { label: "企业名称", value: company.name },
            { label: "统一社会信用代码", value: compactText(detail.company.unified_social_credit_code) },
            { label: "成立时间", value: compactText(detail.company.established_on) },
            { label: "注册资本", value: formatCurrency(detail.company.registered_capital_cny) },
            { label: "地区", value: `${compactText(detail.company.region_province)}${detail.company.region_city || ""}` },
            { label: "行业", value: compactText(detail.company.subindustry || detail.company.industry_category) },
          ])}
        </article>
        <article class="summary-card">
          <h3>风险标签</h3>
          <p>当前企业在风险洞察中的基础标签。</p>
          <div class="tag-row" style="margin-top: 16px;">
            ${tags.map((tag) => `<span class="file-chip">${escapeHtml(tag.label)}：${escapeHtml(tag.value)}</span>`).join("")}
          </div>
          <div class="divider"></div>
          <p>${escapeHtml(company.overview || "暂无企业摘要。")}</p>
        </article>
      </div>
    `;
    return;
  }

  if (active.id === "operation-info") {
    contentAreaEl.innerHTML = `
      <div class="card-grid" style="margin-top: 20px;">
        ${renderFieldPanel(
          "经营能力",
          "围绕经营状态、企业规模和第一还款来源看经营稳定性。",
          [
            { label: "经营状态", value: compactText(detail.company.operating_status) },
            { label: "企业规模", value: compactText(detail.company.enterprise_scale || "—") },
            { label: "申请产品", value: compactText(detail.case_info?.product_type || "—") },
            { label: "第一还款来源", value: compactText(detail.case_info?.primary_repayment_source || "—") },
          ],
        )}
        ${renderFieldPanel(
          "交易闭环材料",
          "合同、订单、发票与回款材料可作为主营业务真实性判断依据。",
          [
            { label: "合同数量", value: `${detail.contracts.length} 份` },
            { label: "订单数量", value: `${detail.orders.length} 条` },
            { label: "发票数量", value: `${detail.invoices.length} 张` },
            { label: "银行摘要", value: `${detail.bank_summaries.length} 条` },
          ],
        )}
      </div>
    `;
    return;
  }

  if (active.id === "shareholder-related") {
    contentAreaEl.innerHTML = renderOwnershipMap(detail, company);
    return;
  }

  if (active.id === "financial-status") {
    contentAreaEl.innerHTML = renderFinancialDashboard(detail);
    return;
  }

  if (active.id === "external-industry") {
    contentAreaEl.innerHTML = renderBydIndustryAnalysis(detail);
    return;
  }

  if (active.id === "guarantor-info") {
    const guarantors = detail.people.filter((item) => item.is_guarantor);
    contentAreaEl.innerHTML = `
      <div class="card-grid" style="margin-top: 20px;">
        ${renderListStack(
          "担保人身份与关系",
          "查看担保人角色、身份与关联关系。",
          guarantors.map((item) => `${escapeHtml(item.full_name)}｜${escapeHtml(item.title || item.role_type)}`),
        )}
        ${renderListStack(
          "担保人相关信用摘要",
          "结合信用历史摘要判断代偿能力与外部负债压力。",
          detail.credit_history.slice(0, 6).map((item) => `${escapeHtml(item.subject_name)}｜余额 ${formatCurrency(item.outstanding_balance_cny)}`),
        )}
        ${renderManualMaterialCard("担保人材料补充", ["担保承诺", "担保人主体资格材料", "财务或征信材料", "与借款人关系说明"], "guarantor")}
      </div>
    `;
    return;
  }

  if (active.id === "collateral-info") {
    contentAreaEl.innerHTML = `
      <div class="card-grid" style="margin-top: 20px;">
        ${detail.guarantees.length
          ? detail.guarantees
              .map(
                (item) => `
                  <article class="section-card">
                    <h3>${escapeHtml(item.asset_name || item.guarantee_type)}</h3>
                    <p>类别：${escapeHtml(item.asset_category || item.guarantee_type || "—")}</p>
                    <p>评估值：${formatCurrency(item.appraised_value_cny)}</p>
                    <p>状态：${escapeHtml(item.guarantee_status || "—")}</p>
                  </article>
                `,
              )
              .join("")
          : '<div class="empty-state"><h3>暂无抵质押物信息</h3><p>可在全流程引擎 > 尽职调查 > 资料准备中补充抵质押材料。</p></div>'}
        ${renderManualMaterialCard("担保与抵质押材料", ["担保承诺", "抵押物权属材料", "评估报告", "质押清单"], "collateral")}
      </div>
    `;
    return;
  }

  contentAreaEl.innerHTML = `
    <div class="two-col-grid" style="margin-top: 20px;">
      ${renderListStack(
        "人工补件与特殊说明",
        "用于承接补件备注、特殊事项和人工判断。",
        [
          `建议状态：${escapeHtml(formatRecommendationStatus(detail.recommendation?.recommendation_status))}`,
          `补充要求：${escapeHtml(compactText(detail.recommendation?.supplemental_requirements))}`,
          `核验发现：${detail.validation_findings.length} 条`,
          `报告章节：${detail.report_sections.length} 段`,
        ],
      )}
      ${renderListStack(
        "重点发现",
        "当前需优先关注的风险或异常摘要。",
        detail.validation_findings.slice(0, 6).map((item) => `${escapeHtml(compactText(item.finding_title))}｜${escapeHtml(compactText(item.finding_summary))}`),
      )}
    </div>
  `;
}

function getCustomerSectionPayload(detail, sectionId) {
  const company = detail.company || {};
  const caseInfo = detail.case_info || {};
  const recommendation = detail.recommendation || {};
  const metrics = Object.fromEntries((detail.latest_metrics || []).map((item) => [item.metric_code, item.value]));
  const industry = detail.industry_profile || {};
  const guarantee = (detail.guarantees || [])[0] || {};
  const profile = detail.profile_attributes || [];
  const topFinding = (detail.validation_findings || [])[0] || {};

  const payloadMap = {
    basic: {
      title: "基本信息",
      items: [
        { label: "企业名称", value: company.name || "—" },
        { label: "统一社会信用代码", value: compactText(company.unified_social_credit_code) },
        { label: "成立时间", value: compactText(company.established_on) },
        { label: "风险分层", value: formatRiskTier(company.risk_tier) },
        { label: "案例编号", value: compactText(caseInfo.case_no) },
        { label: "申请产品", value: compactText(caseInfo.product_type || "—") },
      ],
      hints: ["检查企业主体画像是否完整。", "优先补充主体证照、成立时间与经营范围依据。", "该分组会直接进入报告“客户概况”章节。"],
    },
    operation: {
      title: "经营情况",
      items: [
        { label: "经营状态", value: compactText(company.operating_status) },
        { label: "企业规模", value: compactText(company.enterprise_scale || "—") },
        { label: "第一还款来源", value: compactText(caseInfo.primary_repayment_source || "—") },
        { label: "合同数量", value: `${detail.contracts.length} 份` },
        { label: "订单数量", value: `${detail.orders.length} 条` },
        { label: "发票数量", value: `${detail.invoices.length} 张` },
      ],
      hints: ["可补充主营产品、经营模式和上下游结构。", "建议核对合同、订单、发票、回款链路。", "如还款来源较弱，应在报告中突出风险点。"],
    },
    financial: {
      title: "财务情况",
      items: [
        { label: "营业收入", value: formatCurrency(metrics.revenue) },
        { label: "净利润", value: formatCurrency(metrics.net_profit) },
        { label: "货币资金", value: formatCurrency(metrics.cash) },
        { label: "应收账款", value: formatCurrency(metrics.accounts_receivable) },
        { label: "存货", value: formatCurrency(metrics.inventory) },
        { label: "银行摘要", value: `${detail.bank_summaries.length} 条` },
      ],
      hints: ["建议同时观察利润、现金和应收。", "如果流水和财务表现不一致，应作为预审重点。", "后续可增加派生比率指标。"],
    },
    industry: {
      title: "行业与外部环境信息",
      items: [
        { label: "行业分类", value: compactText(company.subindustry || company.industry_category) },
        { label: "生命周期", value: compactText(industry.lifecycle_stage) },
        { label: "政策方向", value: compactText(industry.policy_direction) },
        { label: "同业比较", value: `${detail.peer_comparisons.length} 条` },
        { label: "公开风险", value: `${detail.public_risks.length} 条` },
        { label: "关键外部事件", value: compactText(detail.public_risks[0]?.title, "暂无重大公开风险") },
      ],
      hints: ["建议至少覆盖政策、周期和外部风险。", "监管行业要优先补外规材料。", "可补充同业分位和行业波动说明。"],
    },
    collateral: {
      title: "抵质押物",
      items: [
        { label: "授信缓释要求", value: compactText(recommendation.guarantee_requirement) },
        { label: "担保方式", value: compactText(caseInfo.guarantee_mode) },
        { label: "担保记录", value: `${detail.guarantees.length} 项` },
        { label: "重点抵质押物", value: compactText(guarantee.asset_name || guarantee.guarantee_type, "待补充") },
        { label: "评估价值", value: formatCurrency(guarantee.appraised_value_cny) },
        { label: "状态", value: compactText(guarantee.guarantee_status) },
      ],
      hints: ["应重点补充权属、评估值和可执行性。", "依赖个人保证时需补代偿能力说明。", "可继续细化抵押率和权证状态。"],
    },
    other: {
      title: "其他",
      items: [
        { label: "画像属性", value: `${profile.length} 条` },
        { label: "核验发现", value: `${detail.validation_findings.length} 条` },
        { label: "建议状态", value: formatRecommendationStatus(recommendation.recommendation_status) },
        { label: "补充要求", value: compactText(recommendation.supplemental_requirements) },
        { label: "重点发现", value: compactText(topFinding.finding_title, "暂无重点异常") },
        { label: "报告章节", value: `${detail.report_sections.length} 段` },
      ],
      hints: ["这里适合放现场访谈、特殊事项和人工判断。", "建议把最需人工解释的风险点沉淀在此。", "后续 AI 生成报告时会优先吸收此处补充说明。"],
    },
  };

  return payloadMap[sectionId] || payloadMap.basic;
}

function renderDueDiligenceCustomerInfo(detail, company) {
  const payload = getCustomerSectionPayload(detail, state.customerSectionId);
  const currentIndex = customerSections.findIndex((item) => item.id === state.customerSectionId) + 1;
  return `
    <div class="two-col-grid" style="margin-top: 20px;">
      <article class="content-card">
        <div class="inline-head">
          <div>
            <h3>${payload.title}</h3>
            <p>案件编号 ${escapeHtml(compactText(detail.case_info?.case_no))}，当前正在整理客户基础输入信息。</p>
          </div>
          ${createStatusPill("open")}
        </div>
        <div class="tab-row" style="margin-top: 16px;">
          ${customerSections
            .map(
              (item) => `
                <button
                  class="tab-button${item.id === state.customerSectionId ? " is-active" : ""}"
                  type="button"
                  data-action="switch-customer-section"
                  data-customer-section="${item.id}"
                >${item.title}</button>
              `,
            )
            .join("")}
        </div>
        <div style="margin-top: 16px;">${renderFieldGrid(payload.items)}</div>
        <p style="margin-top: 16px;">当前进度：${currentIndex}/${customerSections.length}</p>
      </article>
      <article class="summary-card">
        <h3>AI 辅助提示</h3>
        <p>当前为后续接入 DeepSeek 预留智能提示位，先以静态建议方式展示。</p>
        <div class="summary-stack" style="margin-top: 16px;">
          ${payload.hints.map((item) => `<div class="summary-item"><strong>提示</strong><span>${escapeHtml(item)}</span></div>`).join("")}
        </div>
      </article>
    </div>
  `;
}

function renderDueDiligenceMaterials(detail) {
  const buckets = state.meta?.material_buckets || [];
  return `
    <div class="card-grid" style="margin-top: 20px;">
      ${buckets
        .map((bucket) => {
          const files = detail.due_diligence_materials.filter((item) => item.bucket === bucket.id);
          const hints = materialBucketDescriptions[bucket.id] || [];
          return `
            <article class="upload-card">
              <h3>${bucket.title}</h3>
              <p>建议收集：${hints.join("、")}</p>
              <div class="divider"></div>
              <input type="file" accept=".pdf,.doc,.docx" data-material-bucket="${bucket.id}" />
              <div class="upload-stack" style="margin-top: 16px;">
                ${files.length
                  ? files
                      .map(
                        (item) => `
                          <div class="upload-item">
                            <strong>${escapeHtml(item.name)}</strong>
                            <span>上传时间：${escapeHtml(item.uploaded_at)}</span><br />
                            <span>所属分组：${escapeHtml(item.bucket_title)}</span>
                          </div>
                        `,
                      )
                      .join("")
                  : '<div class="upload-item">当前分组尚未上传文件</div>'}
              </div>
            </article>
          `;
        })
        .join("")}
    </div>
  `;
}

function renderKnowledgeChooser(version) {
  const categories = state.knowledgeBase?.categories || [];
  const files = state.knowledgeBase?.files || [];
  return categories
    .map((category) => {
      const categoryFiles = files.filter((item) => item.category === category.id);
      const selectedCount = categoryFiles.filter((item) => state.pendingKnowledgeSelection.includes(item.id)).length;
      return `
        <article class="summary-card source-group-card">
          <div class="inline-head">
            <div>
              <h3>${category.title}</h3>
              <p>可从当前知识库中多选文件，作为尽调报告生成与预审的引用依据。</p>
            </div>
            <button class="ghost-action" type="button" data-action="toggle-knowledge-category" data-knowledge-category-toggle="${category.id}">
              ${selectedCount === categoryFiles.length && categoryFiles.length ? "取消全选" : "一键全选"}
            </button>
          </div>
          <div class="checkbox-group">
            ${categoryFiles.length
              ? categoryFiles
                  .map(
                    (file) => `
                      <label class="checkbox-item">
                        <input
                          type="checkbox"
                          data-knowledge-file-id="${file.id}"
                          ${state.pendingKnowledgeSelection.includes(file.id) ? "checked" : ""}
                        />
                        <div>
                          <strong>${escapeHtml(file.name)}</strong>
                          <span>${escapeHtml(file.description || "无说明")} · 上传人 ${escapeHtml(file.owner)}</span>
                        </div>
                      </label>
                    `,
                  )
                  .join("")
              : '<div class="list-item">当前分类暂无文件</div>'}
          </div>
        </article>
      `;
    })
    .join("");
}

function renderDataSourceChooser(detail) {
  return getReportDataSourceGroups(detail)
    .map(
      (group) => `
        <article class="summary-card source-group-card">
          <div class="inline-head">
            <div>
              <h3>${group.title}</h3>
              <p>${group.description}</p>
            </div>
            <button class="ghost-action" type="button" data-action="toggle-source-group" data-source-group="${group.id}">
              ${group.items.every((item) => state.pendingDataSourceSelection.includes(item.id)) ? "取消全选" : "一键全选"}
            </button>
          </div>
          <div class="checkbox-group">
            ${group.items
              .map(
                (item) => `
                  <label class="checkbox-item">
                    <input
                      type="checkbox"
                      data-report-source-id="${item.id}"
                      ${state.pendingDataSourceSelection.includes(item.id) ? "checked" : ""}
                    />
                    <div>
                      <strong>${item.label}</strong>
                      <span>${item.countLabel}</span>
                    </div>
                  </label>
                `,
              )
              .join("")}
          </div>
        </article>
      `,
    )
    .join("");
}

function renderDueDiligenceReportGenerate(detail) {
  const version = getCurrentVersion(detail);
  const selectedKnowledge = getSelectedKnowledgeFiles();
  return `
    <div class="report-workspace-grid" style="margin-top: 20px;">
      <div class="list-grid">
        <article class="content-card">
          <div class="inline-head">
            <div>
              <h3>左侧选择知识库依据</h3>
              <p>尽调报告默认调用全部结构化数据库内容，左侧仅保留知识库文件选择，作为写作口径和引用依据。</p>
            </div>
            ${createStatusPill("open")}
          </div>
          <div class="summary-stack" style="margin-top: 16px;">
            <div class="summary-item"><strong>已选知识文件</strong><span>${selectedKnowledge.length} 份</span></div>
          </div>
        </article>
        ${renderKnowledgeChooser(version)}
        <article class="summary-card">
          <div class="inline-head">
            <div>
              <h3>生成动作</h3>
              <p>确认知识库引用后，生成新的尽调报告版本。</p>
            </div>
          </div>
          <div class="button-row" style="margin-top: 16px;">
            <button class="primary-action" type="button" data-action="generate-version" ${state.isGeneratingVersion ? "disabled" : ""}>
              ${state.isGeneratingVersion ? "生成中..." : "关联选定知识库生成尽调报告"}
            </button>
          </div>
        </article>
      </div>

      <article class="content-card report-editor-panel">
        <div class="inline-head">
          <div>
            <h3>尽调报告全览</h3>
            <p>右侧保留版本管理和可编辑画布，客户经理可直接修订报告正文。</p>
          </div>
          ${version ? createStatusPill(version.review_result ? "reviewed" : "generated") : createStatusPill("draft")}
        </div>
        ${version
          ? `
            <div class="button-row" style="margin-top: 16px;">
              <select class="form-select" id="report-version-select">
                ${detail.report_versions
                  .map(
                    (item) => `
                      <option value="${item.id}" ${item.id === version.id ? "selected" : ""}>${item.version_label}</option>
                    `,
                  )
                  .join("")}
              </select>
              <button class="ghost-action" type="button" data-action="save-report-draft">保存修改</button>
              <a class="secondary-action" href="${version.pdf_url}" target="_blank" rel="noreferrer">下载 PDF</a>
            </div>
            <div class="summary-stack" style="margin-top: 16px;">
              <div class="summary-item"><strong>当前版本</strong><span>${escapeHtml(version.version_label)} · ${escapeHtml(version.created_at)}</span></div>
              <div class="summary-item"><strong>生成依据</strong><span>${escapeHtml(version.based_on.join("；"))}</span></div>
            </div>
            <div class="divider"></div>
            <h4>报告编辑画布</h4>
            <textarea class="form-textarea report-canvas" id="report-editor-textarea">${escapeHtml(state.reportEditorText)}</textarea>
          `
          : '<div class="empty-state"><h3>尚未生成报告</h3><p>请先在左侧勾选内容并生成新版本。</p></div>'}
      </article>
    </div>
  `;
}

function renderReviewSummary(version) {
  if (!version?.review_result) {
    return `
      <article class="summary-card">
        <h3>问题清单</h3>
        <p>点击“生成风险提示清单”后，这里会输出需要做出什么判断、还缺什么数据以及建议完善方向。</p>
      </article>
    `;
  }

  return `
    <article class="summary-card">
      <h3>预审总览</h3>
      <div class="summary-stack" style="margin-top: 16px;">
        <div class="summary-item"><strong>总体结论</strong><span>${escapeHtml(version.review_result.overall_result)}</span></div>
        <div class="summary-item"><strong>清单生成时间</strong><span>${escapeHtml(version.review_result.reviewed_at)}</span></div>
        <div class="summary-item"><strong>AI预审摘要</strong><span>${escapeHtml(version.review_result.review_summary || "已生成风险提示清单")}</span></div>
        <div class="summary-item"><strong>重点关注</strong><span>高风险 ${version.review_result.counts.high} 条 / 关注 ${version.review_result.counts.medium} 条</span></div>
      </div>
    </article>
  `;
}

function renderReviewFindings(version) {
  const findings = version.review_result?.findings || [];
  return findings.length
    ? findings
        .map(
          (item, index) => `
            <article class="summary-card checklist-card">
              <div class="finding-head">
                <h3>提示 ${index + 1}</h3>
                ${createStatusPill(item.severity === "high" ? "pressure" : item.severity === "medium" ? "watch" : "stable")}
              </div>
              <p>${escapeHtml(item.issue)}</p>
              <div class="summary-stack" style="margin-top: 16px;">
                <div class="summary-item"><strong>需要判断</strong><span>${escapeHtml(item.judgement_focus || item.section_title || "—")}</span></div>
                <div class="summary-item"><strong>还需数据</strong><span>${escapeHtml(item.required_data || item.source_rule || "—")}</span></div>
                <div class="summary-item"><strong>建议完善方向</strong><span>${escapeHtml(item.improvement_direction || item.suggestion)}</span></div>
              </div>
            </article>
          `,
        )
        .join("")
    : '<div class="summary-card"><h3>问题清单</h3><p>当前没有问题清单。</p></div>';
}

function renderReviewKnowledgeGroup(categoryId, title, description) {
  const files = (state.knowledgeBase?.files || []).filter((item) => item.category === categoryId);
  const selectedCount = files.filter((item) => state.pendingKnowledgeSelection.includes(item.id)).length;
  return `
    <section class="review-knowledge-section">
      <div class="inline-head">
        <div>
          <h3>${title}</h3>
          <p>${description}</p>
        </div>
        <button class="ghost-action" type="button" data-action="toggle-knowledge-category" data-knowledge-category-toggle="${categoryId}">
          ${selectedCount === files.length && files.length ? "取消全选" : "一键全选"}
        </button>
      </div>
      <div class="checkbox-group">
        ${files.length
          ? files
              .map(
                (file) => `
                  <label class="checkbox-item">
                    <input
                      type="checkbox"
                      data-knowledge-file-id="${file.id}"
                      ${state.pendingKnowledgeSelection.includes(file.id) ? "checked" : ""}
                    />
                    <div>
                      <strong>${escapeHtml(file.name)}</strong>
                      <span>${escapeHtml(file.description || "无说明")} · 上传人 ${escapeHtml(file.owner)}</span>
                    </div>
                  </label>
                `,
              )
              .join("")
          : '<div class="list-item">当前分类暂无文件</div>'}
      </div>
    </section>
  `;
}

function renderDueDiligenceReportReview(detail) {
  const version = getCurrentVersion(detail);
  if (!version) {
    return '<div class="empty-state"><h3>当前企业尚未生成尽调报告版本</h3><p>请先生成报告版本后再执行预审。</p></div>';
  }

  return `
    <div class="review-workspace-grid" style="margin-top: 20px;">
      <article class="content-card review-left-panel">
        <section class="review-left-panel-head">
          <h3>预审依据输入</h3>
          <p>从现有知识库中直接勾选外规、银行内规和专家经验，作为预审依据。</p>
          <div class="button-row" style="margin-top: 16px;">
            <button class="primary-action" type="button" data-action="run-review" ${state.isRunningReview ? "disabled" : ""}>
              ${state.isRunningReview ? "生成中..." : "生成风险提示清单"}
            </button>
          </div>
        </section>
        <div class="divider"></div>
        <section class="review-knowledge-panel">
          ${renderReviewKnowledgeGroup("laws", "法律法规", "从现有知识库中勾选监管政策、行业规范和名单类文件，作为外规审查依据。")}
          <div class="divider"></div>
          ${renderReviewKnowledgeGroup("policies", "行内制度", "从现有知识库中勾选内部授信政策、准入标准和审批口径文件，作为内规审查依据。")}
          <div class="divider"></div>
          ${renderReviewKnowledgeGroup("experience", "专家经验", "从现有知识库中勾选专家经验文件，作为风险判断和完善方向的补充口径。")}
        </section>
      </article>

      <div class="list-grid">
        ${renderReviewSummary(version)}
        ${renderReviewFindings(version)}
      </div>

      <article class="content-card report-editor-panel">
        <div class="inline-head">
          <div>
            <h3>预审修订画布</h3>
            <p>客户经理可结合中间风险提示，继续修订当前尽调报告。</p>
          </div>
          ${version.review_saved_at ? createStatusPill("reviewed") : createStatusPill("draft")}
        </div>
        <div class="button-row" style="margin-top: 16px;">
          <button class="ghost-action" type="button" data-action="save-review-draft">保存修改</button>
          <a class="secondary-action" href="${version.pdf_url}?variant=review" target="_blank" rel="noreferrer">下载 PDF</a>
        </div>
        <div class="divider"></div>
        <textarea class="form-textarea report-canvas report-canvas-review" id="review-editor-textarea">${escapeHtml(state.reviewEditorText)}</textarea>
      </article>
    </div>
  `;
}

function renderDueDiligence(detail) {
  const tabContent = state.dueDiligenceTabId === "report-generate" ? renderDueDiligenceReportGenerate(detail) : renderDueDiligenceReportReview(detail);
  contentAreaEl.innerHTML = `
    <div class="process-tab-strip" style="margin-top: 20px;">
      <div class="tab-row">
        ${dueDiligenceTabs
          .map(
            (item) => `
              <button
                class="tab-button${item.id === state.dueDiligenceTabId ? " is-active" : ""}"
                type="button"
                data-action="switch-dd-tab"
                data-dd-tab="${item.id}"
              >${item.title}</button>
            `,
          )
          .join("")}
      </div>
    </div>
    ${tabContent}
  `;
}

function renderProcessPlaceholder(detail) {
  const active = getActiveSidebarItem();
  const config = processPlaceholderMap[active.id];
  if (!config) {
    contentAreaEl.innerHTML = `<div class="empty-state"><h3>当前节点暂未配置</h3><p>请切换到其他流程节点。</p></div>`;
    return;
  }
  contentAreaEl.innerHTML = `
    <div class="stats-grid" style="margin-top: 20px;">
      ${config.metrics
        .map((item) => `<article class="metric-card"><strong class="metric-value">${item}</strong><span class="metric-label">POC 结构位</span></article>`)
        .join("")}
    </div>
    <div class="card-grid" style="margin-top: 18px;">
      ${config.cards
        .map(
          (item) => `
            <article class="section-card">
              <h3>${item}</h3>
              <p>当前节点已预留页面结构和文案空间，后续可继续接入真实流程能力与业务数据。</p>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
}

function renderProcessEngine() {
  const companyCode = state.processEngineCompanyCode;
  const detail = getCompanyDetail(companyCode);
  const company = getCompanySummary(companyCode);
  const active = getActiveSidebarItem();

  if (!company || !detail) {
    contentAreaEl.innerHTML = `
      <div class="empty-state">
        <h3>请先在全流程引擎中搜索企业</h3>
        <p>搜索企业后即可进入尽职调查、信用评级、授信方案、授信调查报告、合同与放款和贷后管理工作区。</p>
      </div>
    `;
    return;
  }

  syncSelectedVersion(detail);
  syncKnowledgeSelection(detail);

  if (active.id === "due-diligence") {
    renderDueDiligence(detail);
    return;
  }
  renderProcessPlaceholder(detail);
}

function renderKnowledgeBase() {
  const active = getActiveSidebarItem();
  const search = state.knowledgeSearchKeyword.trim().toLowerCase();
  const files = (state.knowledgeBase?.files || []).filter((item) => item.category === active.id);
  const filtered = search ? files.filter((item) => item.name.toLowerCase().includes(search)) : files;

  contentAreaEl.innerHTML = `
    <div class="two-col-grid" style="margin-top: 20px;">
      <article class="upload-card">
        <h3>${active.title}上传</h3>
        <p>支持上传 PDF / Word 文件，上传后可在尽调报告生成页中被多选引用。</p>
        <input type="file" accept=".pdf,.doc,.docx" data-knowledge-category="${active.id}" />
        <div class="divider"></div>
        <div class="summary-stack">
          <div class="summary-item"><strong>当前分类</strong><span>${active.title}</span></div>
          <div class="summary-item"><strong>上传人</strong><span>系统管理员</span></div>
          <div class="summary-item"><strong>用途</strong><span>可用于尽调报告生成时引用知识依据</span></div>
        </div>
      </article>
      <article class="table-card">
        <h3>文件列表</h3>
        <p>文件状态、分类、上传时间和说明在此统一展示。</p>
        <div class="table-stack" style="margin-top: 16px;">
          <div class="table-head" style="--cols: 5;">
            <span>文件名</span>
            <span>上传时间</span>
            <span>上传人</span>
            <span>说明</span>
            <span>操作</span>
          </div>
          ${filtered.length
            ? filtered
                .map(
                  (item) => `
                    <div class="table-row" style="--cols: 5;">
                      <span>${escapeHtml(item.name)}</span>
                      <span>${escapeHtml(item.uploaded_at)}</span>
                      <span>${escapeHtml(item.owner)}</span>
                      <span>${escapeHtml(compactText(item.description))}</span>
                      <span class="button-row">
                        <a class="ghost-action" href="${item.view_url}" target="_blank" rel="noreferrer">查看</a>
                        <a class="secondary-action" href="${item.download_url}" target="_blank" rel="noreferrer">下载</a>
                      </span>
                    </div>
                  `,
                )
                .join("")
            : '<div class="table-row" style="--cols: 1;"><span>当前没有匹配文件</span></div>'}
        </div>
      </article>
    </div>
  `;
}

function renderSystemTable(columns, rows) {
  return `
    <div class="table-stack" style="margin-top: 16px;">
      <div class="table-head" style="--cols: ${columns.length};">
        ${columns.map((item) => `<span>${item}</span>`).join("")}
      </div>
      ${rows.join("")}
    </div>
  `;
}

function renderSystemAdmin() {
  const active = getActiveSidebarItem().id;
  const data = state.systemAdmin || {};
  let html = "";

  if (active === "users") {
    html = renderSystemTable(
      ["用户", "所属部门/岗位", "角色", "状态"],
      (data.users || []).map(
        (item) => `
          <div class="table-row" style="--cols: 4;">
            <span>${escapeHtml(item.name)}</span>
            <span>${escapeHtml(item.department)} / ${escapeHtml(item.job_title)}</span>
            <span>${escapeHtml(item.role)}</span>
            <span>${escapeHtml(item.status)}</span>
          </div>
        `,
      ),
    );
  } else if (active === "roles") {
    html = renderSystemTable(
      ["角色", "角色说明", "关联菜单"],
      (data.roles || []).map(
        (item) => `
          <div class="table-row" style="--cols: 3;">
            <span>${escapeHtml(item.name)}</span>
            <span>${escapeHtml(item.description)}</span>
            <span>${escapeHtml(item.menus)}</span>
          </div>
        `,
      ),
    );
  } else if (active === "permissions") {
    html = renderSystemTable(
      ["权限类型", "说明", "控制范围"],
      (data.permissions || []).map(
        (item) => `
          <div class="table-row" style="--cols: 3;">
            <span>${escapeHtml(item.name)}</span>
            <span>${escapeHtml(item.description)}</span>
            <span>${escapeHtml(item.scope)}</span>
          </div>
        `,
      ),
    );
  } else if (active === "menus") {
    html = renderSystemTable(
      ["菜单对象", "说明", "可见性"],
      (data.menus || []).map(
        (item) => `
          <div class="table-row" style="--cols: 3;">
            <span>${escapeHtml(item.name)}</span>
            <span>${escapeHtml(item.description)}</span>
            <span>${escapeHtml(item.visibility)}</span>
          </div>
        `,
      ),
    );
  } else if (active === "knowledge-permissions") {
    html = renderSystemTable(
      ["角色", "法律法规", "行内制度", "专家经验"],
      (data.knowledge_permissions || []).map(
        (item) => `
          <div class="table-row" style="--cols: 4;">
            <span>${escapeHtml(item.role)}</span>
            <span>${escapeHtml(item.laws)}</span>
            <span>${escapeHtml(item.policies)}</span>
            <span>${escapeHtml(item.experience)}</span>
          </div>
        `,
      ),
    );
  } else {
    html = renderSystemTable(
      ["时间", "用户", "动作", "对象"],
      (data.logs || []).map(
        (item) => `
          <div class="table-row" style="--cols: 4;">
            <span>${escapeHtml(item.time)}</span>
            <span>${escapeHtml(item.user)}</span>
            <span>${escapeHtml(item.action)}</span>
            <span>${escapeHtml(item.target)}</span>
          </div>
        `,
      ),
    );
  }

  contentAreaEl.innerHTML = `
    <article class="table-card" style="margin-top: 20px;">
      <h3>${getActiveSidebarItem().title}</h3>
      <p>当前为基础后台框架页，重点展示角色权限、知识库权限与近期操作留痕。</p>
      ${html}
    </article>
  `;
}

function renderContent() {
  if (state.topSectionId === "risk-view") {
    renderRiskView();
    return;
  }
  if (state.topSectionId === "process-engine") {
    renderProcessEngine();
    return;
  }
  if (state.topSectionId === "knowledge-base") {
    renderKnowledgeBase();
    return;
  }
  renderSystemAdmin();
}

function renderPreviewDrawer() {
  const detail = getCompanyDetail(state.processEngineCompanyCode);
  const version = getCurrentVersion(detail);
  if (!state.previewOpen || !detail || !version) {
    previewOverlayEl.classList.add("is-hidden");
    return;
  }
  previewOverlayEl.classList.remove("is-hidden");
  previewTitleEl.textContent = `${detail.company.name} · ${version.version_label}`;
  previewOutlineEl.innerHTML = version.section_list
    .map(
      (section) => `
        <button
          class="preview-nav-item${section.id === state.previewSectionId ? " is-active" : ""}"
          type="button"
          data-action="switch-preview-section"
          data-preview-section="${section.id}"
        >${escapeHtml(section.title)}</button>
      `,
    )
    .join("");
  previewArticleEl.innerHTML = version.section_list
    .map(
      (section, index) => `
        <section class="preview-section${section.id === state.previewSectionId ? " is-target" : ""}" id="preview-${section.id}">
          <h4>${index + 1}. ${escapeHtml(section.title)}</h4>
          <p>${escapeHtml(section.content)}</p>
        </section>
      `,
    )
    .join("");
  if (state.previewSectionId) {
    const target = document.getElementById(`preview-${state.previewSectionId}`);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function renderCompletionModal() {
  if (!state.completionModalOpen) {
    completionModalEl.classList.add("is-hidden");
    return;
  }

  completionModalEl.classList.remove("is-hidden");
  const activeTitle = getActiveSidebarItem()?.title || "当前维度";
  const field = state.completionModalField ? `「${state.completionModalField.split(":").at(-1)}」` : activeTitle;
  const dirtyFields = state.completionModalType === "manual" ? getDirtyManualFieldsForSection(state.completionModalField?.split(":")[0]) : [];

  if (state.completionModalType === "ai") {
    const inventory = getRiskDataInventory(getActiveSidebarItem()?.id, getCompanyDetail(state.riskViewCompanyCode));
    completionModalTitleEl.textContent = "AI识别材料上传";
    completionModalBodyEl.innerHTML = `
      <p class="muted-text">请按指标上传佐证材料。POC 阶段先展示上传入口，后续可接入 OCR、结构化抽取和字段回写。</p>
      <div class="summary-stack" style="margin-top: 16px;">
        ${inventory
          .map((item) => {
            const key = `${getActiveSidebarItem()?.id || "risk"}:${item}`;
            return `
              <div class="summary-item">
                <strong>${escapeHtml(item)}</strong>
                ${renderCompletionUploadSlot(key)}
              </div>
            `;
          })
          .join("")}
      </div>
    `;
    return;
  }

  completionModalTitleEl.textContent = "手动修改需要补充材料";
  completionModalBodyEl.innerHTML = `
    <p class="muted-text">你已修改 ${escapeHtml(field)}。离开当前板块前，请上传能证明字段变化的材料，例如证照、报表、合同、流水、评估报告或客户经理现场记录。</p>
    ${dirtyFields.length > 1 ? `<p class="muted-text" style="margin-top: 10px;">当前板块还有 ${dirtyFields.length - 1} 个字段存在修改，请逐项补充依据。</p>` : ""}
    <div class="divider"></div>
    ${renderCompletionUploadSlot(state.completionModalField || `${getActiveSidebarItem()?.id || "risk"}:人工修改材料`)}
  `;
}

function render() {
  renderTopbar();
  renderSidebar();
  renderToolbar();
  renderContent();
  renderPreviewDrawer();
  renderCompletionModal();
}

async function handleGenerateVersion() {
  if (!state.processEngineCompanyCode) return;
  state.isGeneratingVersion = true;
  render();
  try {
    await fetchJson(`/api/company/${encodeURIComponent(state.processEngineCompanyCode)}/report-versions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        knowledge_file_ids: state.pendingKnowledgeSelection,
        data_source_ids: state.pendingDataSourceSelection,
      }),
    });
    await refreshCompanyDetail(state.processEngineCompanyCode);
  } catch (error) {
    console.error(error);
    window.alert(`生成尽调报告失败：${error.message}`);
  } finally {
    state.isGeneratingVersion = false;
    render();
  }
}

async function handleRunReview() {
  const version = getCurrentVersion();
  if (!state.processEngineCompanyCode || !version) return;
  state.isRunningReview = true;
  render();
  try {
    await fetchJson(
      `/api/company/${encodeURIComponent(state.processEngineCompanyCode)}/report-versions/${encodeURIComponent(version.id)}/review`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          knowledge_file_ids: state.pendingKnowledgeSelection,
          report_text: state.reviewEditorText || state.reportEditorText || version.review_edit_text || version.full_text || "",
        }),
      },
    );
    await refreshCompanyDetail(state.processEngineCompanyCode);
    window.alert("风险提示清单生成成功。");
  } catch (error) {
    console.error(error);
    window.alert(`生成风险提示清单失败：${error.message}`);
  } finally {
    state.isRunningReview = false;
    render();
  }
}

async function handleSaveKnowledgeLinks() {
  const version = getCurrentVersion();
  if (!state.processEngineCompanyCode || !version) return;
  await postJson(
    `/api/company/${encodeURIComponent(state.processEngineCompanyCode)}/report-versions/${encodeURIComponent(version.id)}/knowledge-links`,
    { file_ids: state.pendingKnowledgeSelection },
  );
  await refreshCompanyDetail(state.processEngineCompanyCode);
  render();
}

async function handleSaveReportDraft(variant = "generated") {
  const version = getCurrentVersion();
  if (!state.processEngineCompanyCode || !version) return;
  await postJson(
    `/api/company/${encodeURIComponent(state.processEngineCompanyCode)}/report-versions/${encodeURIComponent(version.id)}/draft`,
    { variant, full_text: variant === "review" ? state.reviewEditorText : state.reportEditorText },
  );
  await refreshCompanyDetail(state.processEngineCompanyCode);
  render();
}

document.addEventListener("click", async (event) => {
  const target = event.target.closest("[data-action]");
  if (!target) return;

  const action = target.dataset.action;
  if (action === "switch-top-section") {
    state.topSectionId = target.dataset.topSection;
    state.previewOpen = false;
    state.previewSectionId = null;
    render();
    return;
  }
  if (action === "switch-sidebar-item") {
    if (
      state.topSectionId === "risk-view" &&
      state.riskCompletionMode === "manual" &&
      target.dataset.sidebarId !== state.activeSidebarBySection[state.topSectionId] &&
      promptManualEvidenceForSection(state.activeSidebarBySection[state.topSectionId])
    ) {
      return;
    }
    state.activeSidebarBySection[state.topSectionId] = target.dataset.sidebarId;
    state.previewOpen = false;
    state.previewSectionId = null;
    state.riskCompletionMenuOpen = false;
    render();
    return;
  }
  if (action === "toggle-completion-menu") {
    state.riskCompletionMenuOpen = !state.riskCompletionMenuOpen;
    render();
    return;
  }
  if (action === "set-completion-mode") {
    state.riskCompletionSnapshot = createCompletionSnapshot();
    state.riskCompletionMode = target.dataset.mode;
    state.riskCompletionMenuOpen = false;
    state.completionModalOpen = target.dataset.mode === "ai";
    state.completionModalType = target.dataset.mode === "ai" ? "ai" : null;
    state.completionModalField = null;
    state.activeEditableField = null;
    render();
    return;
  }
  if (action === "finish-completion-mode") {
    if (state.riskCompletionMode === "manual" && promptManualEvidenceForSection()) {
      return;
    }
    clearCompletionSession();
    render();
    return;
  }
  if (action === "cancel-completion-mode") {
    restoreCompletionSnapshot();
    clearCompletionSession();
    render();
    return;
  }
  if (action === "close-completion-modal") {
    state.completionModalOpen = false;
    state.completionModalType = null;
    state.completionModalField = null;
    renderCompletionModal();
    return;
  }
  if (action === "search-company") {
    await searchCompany(target.dataset.sectionId);
    return;
  }
  if (action === "select-company") {
    await selectCompany(target.dataset.sectionId, target.dataset.companyCode);
    render();
    return;
  }
  if (action === "reset-company-search") {
    if (target.dataset.sectionId === "risk-view") state.riskViewCompanyCode = null;
    if (target.dataset.sectionId === "process-engine") state.processEngineCompanyCode = null;
    if (target.dataset.sectionId === "risk-view") {
      clearCompletionSession();
      state.riskManualEdits = {};
      state.riskManualDirtyFields = {};
      state.riskCompletionUploads = {};
    }
    state.previewOpen = false;
    state.previewSectionId = null;
    render();
    return;
  }
  if (action === "switch-dd-tab") {
    state.dueDiligenceTabId = target.dataset.ddTab;
    state.previewOpen = false;
    state.previewSectionId = null;
    render();
    return;
  }
  if (action === "switch-customer-section") {
    state.customerSectionId = target.dataset.customerSection;
    render();
    return;
  }
  if (action === "generate-version") {
    await handleGenerateVersion();
    return;
  }
  if (action === "run-review") {
    await handleRunReview();
    return;
  }
  if (action === "save-knowledge-links") {
    await handleSaveKnowledgeLinks();
    return;
  }
  if (action === "save-report-draft") {
    await handleSaveReportDraft("generated");
    return;
  }
  if (action === "save-review-draft") {
    await handleSaveReportDraft("review");
    return;
  }
  if (action === "toggle-source-group") {
    const group = reportDataSourceGroups.find((item) => item.id === target.dataset.sourceGroup);
    if (!group) return;
    const groupIds = group.items.map((item) => item.id);
    const allSelected = groupIds.every((id) => state.pendingDataSourceSelection.includes(id));
    state.pendingDataSourceSelection = allSelected
      ? state.pendingDataSourceSelection.filter((id) => !groupIds.includes(id))
      : Array.from(new Set([...state.pendingDataSourceSelection, ...groupIds]));
    render();
    return;
  }
  if (action === "toggle-knowledge-category") {
    const files = (state.knowledgeBase?.files || []).filter((item) => item.category === target.dataset.knowledgeCategoryToggle);
    const fileIds = files.map((item) => item.id);
    const allSelected = fileIds.length && fileIds.every((id) => state.pendingKnowledgeSelection.includes(id));
    state.pendingKnowledgeSelection = allSelected
      ? state.pendingKnowledgeSelection.filter((id) => !fileIds.includes(id))
      : Array.from(new Set([...state.pendingKnowledgeSelection, ...fileIds]));
    render();
    return;
  }
  if (action === "open-preview") {
    state.previewOpen = true;
    state.previewSectionId = getCurrentVersion()?.section_list?.[0]?.id || null;
    renderPreviewDrawer();
    return;
  }
  if (action === "close-preview") {
    state.previewOpen = false;
    state.previewSectionId = null;
    renderPreviewDrawer();
    return;
  }
  if (action === "switch-preview-section") {
    state.previewSectionId = target.dataset.previewSection;
    renderPreviewDrawer();
    return;
  }
  if (action === "preview-finding") {
    state.previewOpen = true;
    state.previewSectionId = target.dataset.previewSection;
    renderPreviewDrawer();
  }
});

document.addEventListener("input", (event) => {
  const target = event.target;
  if (target.matches("[data-editable-field]")) {
    const value = target.textContent.trim();
    const originalValue = target.dataset.originalValue.trim();
    const fieldKey = target.dataset.editableField;
    state.riskManualEdits[fieldKey] = value;
    if (value !== originalValue) {
      state.riskManualDirtyFields[fieldKey] = true;
    } else {
      delete state.riskManualDirtyFields[fieldKey];
    }
    return;
  }
  if (target.id === "risk-view-search-input") {
    state.riskSearchKeyword = target.value;
    return;
  }
  if (target.id === "process-engine-search-input") {
    state.processSearchKeyword = target.value;
    return;
  }
  if (target.id === "knowledge-search-input") {
    state.knowledgeSearchKeyword = target.value;
    renderKnowledgeBase();
    return;
  }
  if (target.id === "report-editor-textarea") {
    state.reportEditorText = target.value;
    return;
  }
  if (target.id === "review-editor-textarea") {
    state.reviewEditorText = target.value;
  }
});

document.addEventListener(
  "mousedown",
  (event) => {
    if (state.topSectionId !== "risk-view" || state.riskCompletionMode !== "manual" || state.completionModalOpen) return;
    const dirtyFields = getDirtyManualFieldsForSection();
    if (!dirtyFields.length) return;
    if (event.target.closest('[data-action="cancel-completion-mode"]')) return;

    const clickedEditable = event.target.closest("[data-editable-field]");
    const clickedFieldKey = clickedEditable?.dataset.editableField || null;
    const currentFieldKey = state.activeEditableField;

    if (clickedFieldKey && clickedFieldKey === currentFieldKey) return;
    if (event.target.closest("#completion-modal")) return;

    event.preventDefault();
    event.stopPropagation();
    promptManualEvidenceForSection(getActiveSidebarItem()?.id, currentFieldKey);
  },
  true,
);

document.addEventListener("focusin", (event) => {
  const target = event.target;
  if (!target.matches("[data-editable-field]")) return;
  state.activeEditableField = target.dataset.editableField;
});

document.addEventListener("change", async (event) => {
  const target = event.target;
  if (target.matches("[data-risk-completion-upload]")) {
    const [file] = target.files || [];
    if (!file) return;
    const key = target.dataset.riskCompletionUpload;
    state.riskCompletionUploads[key] = [file.name, ...(state.riskCompletionUploads[key] || []).filter((item) => item !== file.name)].slice(0, 3);
    if (state.riskManualDirtyFields[key]) delete state.riskManualDirtyFields[key];
    render();
    return;
  }

  if (target.id === "report-version-select") {
    state.reportVersionId = target.value;
    syncKnowledgeSelection(getCompanyDetail(state.processEngineCompanyCode));
    render();
    return;
  }

  if (target.matches("[data-material-bucket]")) {
    const [file] = target.files || [];
    if (!file || !state.processEngineCompanyCode) return;
    await uploadFile(
      `/api/company/${encodeURIComponent(state.processEngineCompanyCode)}/due-diligence-materials?bucket=${encodeURIComponent(target.dataset.materialBucket)}`,
      file,
    );
    await refreshCompanyDetail(state.processEngineCompanyCode);
    render();
    return;
  }

  if (target.matches("[data-review-category]")) {
    const [file] = target.files || [];
    const version = getCurrentVersion();
    if (!file || !state.processEngineCompanyCode || !version) return;
    await uploadFile(
      `/api/company/${encodeURIComponent(state.processEngineCompanyCode)}/report-versions/${encodeURIComponent(version.id)}/review-files?category=${encodeURIComponent(target.dataset.reviewCategory)}`,
      file,
    );
    await refreshCompanyDetail(state.processEngineCompanyCode);
    render();
    return;
  }

  if (target.matches("[data-knowledge-category]")) {
    const [file] = target.files || [];
    if (!file) return;
    state.knowledgeBase = await uploadFile(`/api/knowledge-files?category=${encodeURIComponent(target.dataset.knowledgeCategory)}`, file);
    render();
    return;
  }

  if (target.matches("[data-knowledge-file-id]")) {
    const checkedIds = Array.from(document.querySelectorAll("[data-knowledge-file-id]:checked")).map((item) => item.dataset.knowledgeFileId);
    state.pendingKnowledgeSelection = checkedIds;
    return;
  }

  if (target.matches("[data-report-source-id]")) {
    const checkedIds = Array.from(document.querySelectorAll("[data-report-source-id]:checked")).map((item) => item.dataset.reportSourceId);
    state.pendingDataSourceSelection = checkedIds;
  }
});

document.addEventListener("keydown", async (event) => {
  if (event.key !== "Enter") return;
  const target = event.target;
  if (target.id === "risk-view-search-input") {
    event.preventDefault();
    await searchCompany("risk-view");
  }
  if (target.id === "process-engine-search-input") {
    event.preventDefault();
    await searchCompany("process-engine");
  }
});

async function init() {
  const [meta, companies, knowledgeBase, systemAdmin] = await Promise.all([
    fetchJson("/api/meta"),
    fetchJson("/api/companies"),
    fetchJson("/api/knowledge-files"),
    fetchJson("/api/system-admin"),
  ]);
  state.meta = meta;
  state.companies = companies;
  state.knowledgeBase = knowledgeBase;
  state.systemAdmin = systemAdmin;
  render();
}

init().catch((error) => {
  console.error(error);
  document.body.innerHTML = `<pre style="padding:24px;color:#b44632;">前端初始化失败：${escapeHtml(error.message)}</pre>`;
});
