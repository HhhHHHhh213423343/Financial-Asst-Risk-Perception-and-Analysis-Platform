import { useMemo, useState } from "react";
import { RiskBlockSvg, type Point, type Risk, type RiskBlockLayout } from "./RiskBlockSvg";

type RiskHouseSvgProps = {
  risks: Risk[];
  selectedRiskId?: string;
  onSelectRisk: (risk: Risk) => void;
};

type BlockGeometry = {
  index: string;
  layer: RiskBlockLayout["layer"];
  x: number;
  y: number;
  w: number;
  h: number;
  skew: number;
  depthX: number;
  depthY: number;
};

const blockGeometry: BlockGeometry[] = [
  { index: "01", layer: "top", x: 278, y: 218, w: 205, h: 106, skew: 18, depthX: 38, depthY: 30 },
  { index: "02", layer: "top", x: 498, y: 212, w: 205, h: 106, skew: 18, depthX: 38, depthY: 30 },
  { index: "03", layer: "top", x: 718, y: 222, w: 205, h: 106, skew: 18, depthX: 38, depthY: 30 },

  { index: "04", layer: "upper", x: 236, y: 318, w: 235, h: 112, skew: 20, depthX: 42, depthY: 32 },
  { index: "05", layer: "upper", x: 488, y: 310, w: 235, h: 112, skew: 20, depthX: 42, depthY: 32 },
  { index: "06", layer: "upper", x: 740, y: 322, w: 235, h: 112, skew: 20, depthX: 42, depthY: 32 },

  { index: "07", layer: "middle", x: 188, y: 424, w: 275, h: 116, skew: 23, depthX: 46, depthY: 34 },
  { index: "08", layer: "middle", x: 480, y: 414, w: 275, h: 116, skew: 23, depthX: 46, depthY: 34 },
  { index: "09", layer: "middle", x: 772, y: 428, w: 275, h: 116, skew: 23, depthX: 46, depthY: 34 },

  { index: "10", layer: "base", x: 142, y: 536, w: 310, h: 120, skew: 26, depthX: 50, depthY: 36 },
  { index: "11", layer: "base", x: 470, y: 524, w: 310, h: 120, skew: 26, depthX: 50, depthY: 36 },
  { index: "12", layer: "base", x: 798, y: 540, w: 310, h: 120, skew: 26, depthX: 50, depthY: 36 },
];

function createLayout({ index, layer, x, y, w, h, skew, depthX, depthY }: BlockGeometry): RiskBlockLayout {
  const front: Point[] = [
    [x, y],
    [x + w, y],
    [x + w - skew, y + h],
    [x + skew, y + h],
  ];
  const top: Point[] = [
    [x, y],
    [x + w, y],
    [x + w + depthX, y - depthY],
    [x + depthX, y - depthY],
  ];
  const side: Point[] = [
    [x + w, y],
    [x + w - skew, y + h],
    [x + w - skew + depthX, y + h - depthY],
    [x + w + depthX, y - depthY],
  ];

  return {
    index,
    layer,
    front,
    top,
    side,
    text: {
      x: x + w / 2,
      y: y + h / 2 - 4,
    },
  };
}

export const riskBlockLayout: RiskBlockLayout[] = blockGeometry.map(createLayout);

const fallbackRiskNames: Record<string, string> = {
  "01": "法律诉讼与执行风险",
  "02": "经营异常与失信风险",
  "03": "实控人与股权控制风险",
  "04": "偿债与现金流风险",
  "05": "财务质量风险",
  "06": "关联网络风险",
  "07": "合同履约与交易风险",
  "08": "供应链与客户集中风险",
  "09": "行业与市场风险",
  "10": "主体身份与工商信息风险",
  "11": "资质许可与合规备案风险",
  "12": "舆情与声誉风险",
};

function getRiskForLayout(risks: Risk[], layout: RiskBlockLayout): Risk {
  return (
    risks.find((risk) => risk.index === layout.index) ?? {
      id: `missing-${layout.index}`,
      index: layout.index,
      name: fallbackRiskNames[layout.index],
      level: "unknown",
      score: 0,
    }
  );
}

function RiskGradients() {
  return (
    <defs>
      <radialGradient id="baseGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#8fdcff" stopOpacity="0.7" />
        <stop offset="48%" stopColor="#5179ff" stopOpacity="0.2" />
        <stop offset="100%" stopColor="#2a3f99" stopOpacity="0" />
      </radialGradient>

      <linearGradient id="roofFront" x1="360" y1="86" x2="840" y2="214" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stopColor="#f3f8ff" stopOpacity="0.82" />
        <stop offset="54%" stopColor="#7aa6ff" stopOpacity="0.4" />
        <stop offset="100%" stopColor="#182c63" stopOpacity="0.74" />
      </linearGradient>
      <linearGradient id="roofTop" x1="385" y1="92" x2="810" y2="150" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stopColor="#ffffff" stopOpacity="0.74" />
        <stop offset="58%" stopColor="#79ddff" stopOpacity="0.32" />
        <stop offset="100%" stopColor="#24407a" stopOpacity="0.62" />
      </linearGradient>
      <linearGradient id="glassSheen" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#ffffff" stopOpacity="0" />
        <stop offset="42%" stopColor="#ffffff" stopOpacity="0.42" />
        <stop offset="100%" stopColor="#ffffff" stopOpacity="0" />
      </linearGradient>

      <linearGradient id="riskExtremeFront" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ffb199" stopOpacity="0.82" />
        <stop offset="52%" stopColor="#ff4d63" stopOpacity="0.58" />
        <stop offset="100%" stopColor="#4e1025" stopOpacity="0.82" />
      </linearGradient>
      <linearGradient id="riskExtremeTop" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ffe0d5" stopOpacity="0.78" />
        <stop offset="100%" stopColor="#ff5f6d" stopOpacity="0.34" />
      </linearGradient>
      <linearGradient id="riskExtremeSide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ff6a78" stopOpacity="0.48" />
        <stop offset="100%" stopColor="#160713" stopOpacity="0.86" />
      </linearGradient>

      <linearGradient id="riskHighFront" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ffd0a6" stopOpacity="0.82" />
        <stop offset="48%" stopColor="#ff884d" stopOpacity="0.58" />
        <stop offset="100%" stopColor="#4a1e13" stopOpacity="0.84" />
      </linearGradient>
      <linearGradient id="riskHighTop" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ffe7c7" stopOpacity="0.78" />
        <stop offset="100%" stopColor="#ff8f42" stopOpacity="0.34" />
      </linearGradient>
      <linearGradient id="riskHighSide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ff9f59" stopOpacity="0.46" />
        <stop offset="100%" stopColor="#160a08" stopOpacity="0.86" />
      </linearGradient>

      <linearGradient id="riskMediumFront" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#fff0af" stopOpacity="0.82" />
        <stop offset="52%" stopColor="#ffd166" stopOpacity="0.54" />
        <stop offset="100%" stopColor="#4b3614" stopOpacity="0.84" />
      </linearGradient>
      <linearGradient id="riskMediumTop" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#fff7ca" stopOpacity="0.78" />
        <stop offset="100%" stopColor="#ffd166" stopOpacity="0.34" />
      </linearGradient>
      <linearGradient id="riskMediumSide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#ffd978" stopOpacity="0.42" />
        <stop offset="100%" stopColor="#151008" stopOpacity="0.86" />
      </linearGradient>

      <linearGradient id="riskLowFront" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#a8d8ff" stopOpacity="0.82" />
        <stop offset="52%" stopColor="#5f8cff" stopOpacity="0.52" />
        <stop offset="100%" stopColor="#14244d" stopOpacity="0.84" />
      </linearGradient>
      <linearGradient id="riskLowTop" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#d8f3ff" stopOpacity="0.76" />
        <stop offset="100%" stopColor="#5f8cff" stopOpacity="0.32" />
      </linearGradient>
      <linearGradient id="riskLowSide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#5f8cff" stopOpacity="0.42" />
        <stop offset="100%" stopColor="#070d22" stopOpacity="0.86" />
      </linearGradient>

      <linearGradient id="riskUnknownFront" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#c1cde2" stopOpacity="0.76" />
        <stop offset="54%" stopColor="#7385ab" stopOpacity="0.48" />
        <stop offset="100%" stopColor="#1d263a" stopOpacity="0.84" />
      </linearGradient>
      <linearGradient id="riskUnknownTop" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#dce5f7" stopOpacity="0.7" />
        <stop offset="100%" stopColor="#7385ab" stopOpacity="0.3" />
      </linearGradient>
      <linearGradient id="riskUnknownSide" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#7c92bc" stopOpacity="0.38" />
        <stop offset="100%" stopColor="#070b16" stopOpacity="0.86" />
      </linearGradient>

      {[
        ["riskGlowExtreme", "#ff5f6d"],
        ["riskGlowHigh", "#ff8f42"],
        ["riskGlowMedium", "#ffd166"],
        ["riskGlowLow", "#5f8cff"],
        ["riskGlowUnknown", "#8da0c8"],
      ].map(([id, color]) => (
        <filter key={id} id={id} x="-20%" y="-30%" width="150%" height="170%">
          <feDropShadow dx="0" dy="12" stdDeviation="10" floodColor="#020615" floodOpacity="0.52" />
          <feDropShadow dx="0" dy="0" stdDeviation="9" floodColor={color} floodOpacity="0.22" />
        </filter>
      ))}
      {[
        ["riskGlowExtremeStrong", "#ff5f6d"],
        ["riskGlowHighStrong", "#ff8f42"],
        ["riskGlowMediumStrong", "#ffd166"],
        ["riskGlowLowStrong", "#5f8cff"],
        ["riskGlowUnknownStrong", "#9badce"],
      ].map(([id, color]) => (
        <filter key={id} id={id} x="-25%" y="-35%" width="160%" height="190%">
          <feDropShadow dx="0" dy="18" stdDeviation="12" floodColor="#020615" floodOpacity="0.62" />
          <feDropShadow dx="0" dy="0" stdDeviation="15" floodColor={color} floodOpacity="0.48" />
        </filter>
      ))}
    </defs>
  );
}

export function RiskHouseSvg({ risks, selectedRiskId, onSelectRisk }: RiskHouseSvgProps) {
  const [hoveredRiskId, setHoveredRiskId] = useState<string | null>(null);
  const orderedBlocks = useMemo(
    () =>
      riskBlockLayout.map((layout) => ({
        layout,
        risk: getRiskForLayout(risks, layout),
      })),
    [risks],
  );

  return (
    <svg
      className="risk-house-svg"
      viewBox="0 0 1200 760"
      role="img"
      aria-labelledby="risk-house-title risk-house-desc"
      preserveAspectRatio="xMidYMid meet"
    >
      <title id="risk-house-title">SVG Risk House</title>
      <desc id="risk-house-desc">由屋顶、十二个三面体风险模块和发光椭圆基座构成的企业风险房屋。</desc>
      <RiskGradients />

      <rect x="0" y="0" width="1200" height="760" rx="42" fill="#030915" />
      <circle cx="600" cy="155" r="390" fill="#235cff" opacity="0.08" />
      <circle cx="912" cy="512" r="260" fill="#28dcff" opacity="0.05" />
      <path
        d="M118 676 C280 614, 930 604, 1084 678"
        fill="none"
        stroke="#78dfff"
        strokeOpacity="0.15"
        strokeWidth="2"
      />
      <ellipse cx="620" cy="692" rx="470" ry="54" fill="url(#baseGlow)" />
      <ellipse cx="620" cy="690" rx="362" ry="31" fill="none" stroke="#8fdcff" strokeOpacity="0.24" />

      <g filter="url(#riskGlowLow)">
        <polygon points="600,58 888,206 312,206" fill="url(#roofFront)" stroke="rgba(235, 245, 255, 0.55)" />
        <polygon points="356,164 844,164 888,206 312,206" fill="url(#roofTop)" stroke="rgba(235, 245, 255, 0.34)" />
        <polygon points="600,58 888,206 844,164 600,100 356,164 312,206" fill="url(#glassSheen)" opacity="0.3" />
      </g>

      {orderedBlocks.map(({ layout, risk }) => (
        <RiskBlockSvg
          key={risk.id}
          risk={risk}
          layout={layout}
          selected={risk.id === selectedRiskId}
          hovered={risk.id === hoveredRiskId}
          onSelectRisk={onSelectRisk}
          onHoverRisk={setHoveredRiskId}
        />
      ))}

      <g className="risk-house-svg__legend" transform="translate(286 724)">
        <circle cx="0" cy="0" r="6" fill="#ff8f42" />
        <text x="14" y="5">高风险</text>
        <circle cx="116" cy="0" r="6" fill="#ffd166" />
        <text x="130" y="5">中风险</text>
        <circle cx="232" cy="0" r="6" fill="#5f8cff" />
        <text x="246" y="5">低风险</text>
        <circle cx="348" cy="0" r="6" fill="#7385ab" />
        <text x="362" y="5">信息不足</text>
      </g>
    </svg>
  );
}
