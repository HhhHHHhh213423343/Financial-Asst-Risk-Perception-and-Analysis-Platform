import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RiskHouseSvgPreview } from "./RiskHouseSvgPreview";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RiskHouseSvgPreview />
  </StrictMode>,
);
