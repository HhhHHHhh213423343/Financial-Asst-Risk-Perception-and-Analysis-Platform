import { useMemo, useState } from "react";
import { RiskHouseSvg } from "./components/RiskHouseSvg";
import type { Risk } from "./components/RiskBlockSvg";

const mockRisks: Risk[] = [
  { id: "legal_execution", index: "01", name: "法律诉讼与执行风险", level: "high", score: 88 },
  { id: "abnormal_credit", index: "02", name: "经营异常与失信风险", level: "medium", score: 57 },
  { id: "ownership_control", index: "03", name: "实控人与股权控制风险", level: "medium", score: 61 },
  { id: "cashflow_debt", index: "04", name: "偿债与现金流风险", level: "high", score: 84 },
  { id: "financial_quality", index: "05", name: "财务质量风险", level: "high", score: 76 },
  { id: "related_network", index: "06", name: "关联网络风险", level: "high", score: 79 },
  { id: "contract_delivery", index: "07", name: "合同履约与交易风险", level: "medium", score: 64 },
  { id: "supply_customer", index: "08", name: "供应链与客户集中风险", level: "medium", score: 67 },
  { id: "industry_market", index: "09", name: "行业与市场风险", level: "low", score: 42 },
  { id: "identity_registration", index: "10", name: "主体身份与工商信息风险", level: "low", score: 31 },
  { id: "license_compliance", index: "11", name: "资质许可与合规备案风险", level: "unknown", score: 18 },
  { id: "public_reputation", index: "12", name: "舆情与声誉风险", level: "medium", score: 53 },
];

const levelLabels: Record<string, string> = {
  high: "高风险",
  medium: "中风险",
  low: "低风险",
  unknown: "信息不足",
  extreme: "极高风险",
};

export function RiskHouseSvgPreview() {
  const [selectedRisk, setSelectedRisk] = useState<Risk>(mockRisks[0]);
  const selectedDetail = useMemo(
    () => mockRisks.find((risk) => risk.id === selectedRisk.id) ?? mockRisks[0],
    [selectedRisk.id],
  );

  return (
    <main className="svg-preview-page">
      <section className="svg-preview-hero">
        <div>
          <p className="preview-kicker">SVG Risk House Preview</p>
          <h1>企业风险房屋矢量信息图</h1>
          <p>
            当前页面只展示 SVG Risk House 和 mock 数据。模块主体全部由 polygon 绘制，点击模块会更新右侧详情。
          </p>
        </div>
        <div className="preview-summary">
          <span>viewBox 0 0 1200 760</span>
          <strong>12 个三面体模块</strong>
        </div>
      </section>

      <section className="svg-preview-workbench">
        <div className="svg-preview-stage" aria-label="SVG Risk House 预览区域">
          <RiskHouseSvg risks={mockRisks} selectedRiskId={selectedDetail.id} onSelectRisk={setSelectedRisk} />
        </div>

        <aside className="svg-preview-detail" aria-label="风险详情">
          <p className="preview-kicker">Risk Detail Panel</p>
          <h2>{selectedDetail.name}</h2>
          <div className="detail-score">
            <strong>{selectedDetail.score}</strong>
            <span>/ 100</span>
          </div>
          <dl>
            <div>
              <dt>模块编号</dt>
              <dd>{selectedDetail.index}</dd>
            </div>
            <div>
              <dt>风险等级</dt>
              <dd>{levelLabels[selectedDetail.level] ?? "信息不足"}</dd>
            </div>
            <div>
              <dt>交互状态</dt>
              <dd>点击 SVG polygon 模块后由 onSelectRisk(risk) 更新</dd>
            </div>
          </dl>
        </aside>
      </section>
    </main>
  );
}
