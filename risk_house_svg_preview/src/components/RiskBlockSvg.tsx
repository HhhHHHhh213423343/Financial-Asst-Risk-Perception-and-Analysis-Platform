export type RiskLevel = "extreme" | "high" | "medium" | "low" | "unknown";

export type Point = [number, number];

export type Risk = {
  id: string;
  index: string;
  name: string;
  level: RiskLevel | string;
  score: number;
};

export type RiskBlockLayout = {
  index: string;
  layer: "top" | "upper" | "middle" | "base";
  front: Point[];
  top: Point[];
  side: Point[];
  text: {
    x: number;
    y: number;
  };
};

type RiskBlockSvgProps = {
  risk: Risk;
  layout: RiskBlockLayout;
  selected: boolean;
  hovered: boolean;
  onSelectRisk: (risk: Risk) => void;
  onHoverRisk: (riskId: string | null) => void;
};

const levelGradientIds: Record<RiskLevel, { front: string; top: string; side: string; glow: string }> = {
  extreme: { front: "riskExtremeFront", top: "riskExtremeTop", side: "riskExtremeSide", glow: "riskGlowExtreme" },
  high: { front: "riskHighFront", top: "riskHighTop", side: "riskHighSide", glow: "riskGlowHigh" },
  medium: { front: "riskMediumFront", top: "riskMediumTop", side: "riskMediumSide", glow: "riskGlowMedium" },
  low: { front: "riskLowFront", top: "riskLowTop", side: "riskLowSide", glow: "riskGlowLow" },
  unknown: { front: "riskUnknownFront", top: "riskUnknownTop", side: "riskUnknownSide", glow: "riskGlowUnknown" },
};

function normalizeLevel(level: Risk["level"]): RiskLevel {
  if (level === "extreme" || level === "极高风险") return "extreme";
  if (level === "high" || level === "高风险") return "high";
  if (level === "medium" || level === "中风险") return "medium";
  if (level === "low" || level === "低风险") return "low";
  return "unknown";
}

function pointsToString(points: Point[]) {
  return points.map(([x, y]) => `${x},${y}`).join(" ");
}

function splitRiskName(name: string) {
  if (name.length <= 9) return [name];
  if (name.length <= 14) return [name.slice(0, 7), name.slice(7)];
  return [name.slice(0, 8), name.slice(8, 15), name.slice(15)];
}

export function RiskBlockSvg({
  risk,
  layout,
  selected,
  hovered,
  onSelectRisk,
  onHoverRisk,
}: RiskBlockSvgProps) {
  const level = normalizeLevel(risk.level);
  const gradients = levelGradientIds[level];
  const elevated = selected || hovered;
  const textLines = splitRiskName(risk.name);
  const strokeOpacity = selected ? 0.98 : hovered ? 0.72 : 0.36;

  return (
    <g
      className={`risk-block-svg risk-block-svg--${level}${selected ? " is-selected" : ""}`}
      role="button"
      tabIndex={0}
      aria-label={`${risk.index} ${risk.name} ${risk.level} ${risk.score}分`}
      transform={elevated ? "translate(0 -10)" : undefined}
      filter={`url(#${elevated ? `${gradients.glow}Strong` : gradients.glow})`}
      onClick={() => onSelectRisk(risk)}
      onMouseEnter={() => onHoverRisk(risk.id)}
      onMouseLeave={() => onHoverRisk(null)}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onSelectRisk(risk);
        }
      }}
    >
      <polygon
        points={pointsToString(layout.top)}
        fill={`url(#${gradients.top})`}
        stroke="rgba(228, 240, 255, 0.34)"
        strokeWidth={selected ? 2.4 : 1.2}
      />
      <polygon
        points={pointsToString(layout.side)}
        fill={`url(#${gradients.side})`}
        stroke="rgba(158, 190, 255, 0.24)"
        strokeWidth={selected ? 2 : 1}
      />
      <polygon
        points={pointsToString(layout.front)}
        fill={`url(#${gradients.front})`}
        stroke="rgba(240, 247, 255, 0.64)"
        strokeOpacity={strokeOpacity}
        strokeWidth={selected ? 3 : 1.4}
      />
      <polygon
        points={pointsToString(layout.front)}
        fill="url(#glassSheen)"
        opacity={hovered ? 0.42 : 0.24}
      />
      {selected ? (
        <polygon
          points={pointsToString(layout.front)}
          fill="none"
          stroke="rgba(255, 255, 255, 0.88)"
          strokeWidth={1.4}
          strokeDasharray="8 8"
        />
      ) : null}
      <text
        x={layout.text.x}
        y={layout.text.y - 26}
        textAnchor="middle"
        className="risk-block-svg__index"
      >
        {risk.index}
      </text>
      <text x={layout.text.x} y={layout.text.y} textAnchor="middle" className="risk-block-svg__name">
        {textLines.map((line, lineIndex) => (
          <tspan key={`${risk.id}-${lineIndex}`} x={layout.text.x} dy={lineIndex === 0 ? 0 : 25}>
            {line}
          </tspan>
        ))}
      </text>
    </g>
  );
}
