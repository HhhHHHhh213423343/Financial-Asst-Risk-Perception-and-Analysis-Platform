import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const workbookDataPath = path.join(root, "artifacts", "workbook_data.json");
const outputDir = path.join(root, "outputs", "sme_due_diligence_demo");
const outputPath = path.join(outputDir, "sme_due_diligence_demo.xlsx");

function chunkRows(headers, rows) {
  return [headers, ...rows];
}

function estimateColumnWidths(headers, rows) {
  return headers.map((header, index) => {
    const values = rows.slice(0, 80).map((row) => row[index]);
    const maxLen = Math.max(
      String(header ?? "").length,
      ...values.map((value) => String(value ?? "").length),
    );
    return Math.min(Math.max(maxLen * 9 + 24, 90), 260);
  });
}

function formatHeader(range) {
  range.format.font.bold = true;
  range.format.font.color = "#FFFFFF";
  range.format.fill.color = "#1F4E78";
  range.format.wrapText = true;
}

function formatBody(range) {
  range.format.wrapText = true;
  range.format.verticalAlignment = "top";
}

function addTableSheet(workbook, sheetName, headers, rows) {
  const sheet = workbook.worksheets.add(sheetName);
  const matrix = chunkRows(headers, rows);
  const lastCol = headers.length;
  const lastRow = matrix.length;
  if (!lastCol) {
    sheet.getRange("A1:A1").writeValues([["No data"]]);
    return sheet;
  }
  sheet.getRangeByIndexes(0, 0, lastRow, lastCol).writeValues(matrix);
  const headerRange = sheet.getRangeByIndexes(0, 0, 1, lastCol);
  const bodyRange = sheet.getRangeByIndexes(1, 0, Math.max(lastRow - 1, 1), lastCol);
  formatHeader(headerRange);
  formatBody(bodyRange);
  sheet.freezePanes.freezeRows(1);
  const widths = estimateColumnWidths(headers, rows);
  widths.forEach((width, idx) => {
    sheet.getRangeByIndexes(0, idx, Math.max(lastRow, 1), 1).format.columnWidthPx = width;
  });
  sheet.getRangeByIndexes(0, 0, Math.max(lastRow, 1), lastCol).format.rowHeightPx = 24;
  return sheet;
}

function addSummarySheet(workbook, summary, companyRows, caseRows) {
  const sheet = workbook.worksheets.add("Overview");
  sheet.getRange("A1:H1").merge();
  sheet.getRange("A1:H1").writeValues([["SME Due Diligence Demo Data Overview", "", "", "", "", "", "", ""]]);
  sheet.getRange("A1:H1").format.font.bold = true;
  sheet.getRange("A1:H1").format.font.size = 16;
  sheet.getRange("A1:H1").format.font.color = "#FFFFFF";
  sheet.getRange("A1:H1").format.fill.color = "#17365D";
  sheet.getRange("A1:H1").format.rowHeightPx = 28;

  const kpiRows = [
    ["Metric", "Value"],
    ["Companies", summary.companies],
    ["People", summary.persons],
    ["Profile attributes", summary.company_profile_attributes ?? 0],
    ["Cases", summary.due_diligence_cases],
    ["Documents", summary.documents],
    ["Financial metrics", summary.financial_metrics],
    ["Statement lines", summary.financial_statement_line_items ?? 0],
    ["Reconciliation checks", summary.financial_reconciliation_checks ?? 0],
    ["Settlement summaries", summary.bank_settlement_summaries ?? 0],
    ["Tax-invoice checks", summary.tax_invoice_consistency_checks ?? 0],
    ["Related-party summaries", summary.related_party_transaction_summaries ?? 0],
    ["Credit summaries", summary.credit_history_summaries ?? 0],
    ["Bank transactions", summary.bank_transactions],
    ["Validation findings", summary.validation_findings],
  ];
  sheet.getRangeByIndexes(2, 0, kpiRows.length, 2).writeValues(kpiRows);
  formatHeader(sheet.getRange("A3:B3"));
  formatBody(sheet.getRangeByIndexes(3, 0, kpiRows.length - 1, 2));

  const companyMatrix = [
    ["Company code", "Company name", "Subindustry", "Risk tier", "Requested amount", "Decision status"],
    ...companyRows.map((row) => {
      const linkedCase = caseRows.find((c) => c[0] === row[0]);
      return [
        row[0],
        row[1],
        row[6],
        row[9],
        linkedCase?.[5] ?? "",
        linkedCase?.[8] ?? "",
      ];
    }),
  ];
  sheet.getRangeByIndexes(13, 0, companyMatrix.length, companyMatrix[0].length).writeValues(companyMatrix);
  formatHeader(sheet.getRangeByIndexes(13, 0, 1, companyMatrix[0].length));
  formatBody(sheet.getRangeByIndexes(14, 0, companyMatrix.length - 1, companyMatrix[0].length));

  sheet.getRange("D3:H8").writeValues([
    ["Usage notes", "", "", "", ""],
    ["1", "Use the Overview sheet for quick borrower comparison.", "", "", ""],
    ["2", "Use the detailed sheets to cross-check records against the SQLite database.", "", "", ""],
    ["3", "Document Index points to generated source files for each borrower.", "", "", ""],
    ["4", "Main showcase borrower is COMP-001.", "", "", ""],
    ["5", "Replace demo shells and source files as real materials arrive.", "", "", ""],
  ]);
  formatHeader(sheet.getRange("D3:H3"));
  formatBody(sheet.getRange("D4:H8"));

  [0, 1, 2, 3, 4, 5, 6, 7].forEach((idx) => {
    sheet.getRangeByIndexes(0, idx, 20, 1).format.columnWidthPx = [120, 220, 160, 120, 150, 160, 160, 160][idx] ?? 140;
  });
  sheet.freezePanes.freezeRows(1);
  return sheet;
}

async function main() {
  const workbookData = JSON.parse(await fs.readFile(workbookDataPath, "utf8"));
  const workbook = Workbook.create();

  const sheetMap = new Map(workbookData.sheets.map((sheet) => [sheet.name, sheet]));
  addSummarySheet(
    workbook,
    workbookData.summary,
    sheetMap.get("companies")?.rows ?? [],
    sheetMap.get("cases")?.rows ?? [],
  );

  const sheetOrder = [
    ["companies", "企业基础画像"],
    ["company_profile_attributes", "画像属性"],
    ["related_companies", "关联实体"],
    ["core_people", "核心自然人"],
    ["cases", "尽调项目"],
    ["financial_summary", "财务摘要"],
    ["annual_financial_metrics", "年度财务指标"],
    ["financial_statement_lines", "三大表明细"],
    ["financial_reconciliation_checks", "勾稽检查"],
    ["bank_settlement_summaries", "结算汇总"],
    ["tax_invoice_consistency_checks", "税票一致性"],
    ["related_party_transaction_summaries", "关联交易摘要"],
    ["credit_history_summaries", "信用历史摘要"],
    ["tax_filings", "税务摘要"],
    ["bank_transactions", "银行流水"],
    ["contracts", "合同台账"],
    ["orders", "订单台账"],
    ["invoices", "发票台账"],
    ["innovation", "科创能力"],
    ["public_risks", "外部风险"],
    ["validation_findings", "核验发现"],
    ["credit_recommendations", "授信建议"],
    ["document_index", "文档索引"],
  ];

  for (const [sourceName, sheetName] of sheetOrder) {
    const source = sheetMap.get(sourceName);
    addTableSheet(workbook, sheetName, source?.headers ?? [], source?.rows ?? []);
  }

  const inspect = await workbook.inspect({
    kind: "table",
    range: "Overview!A1:H18",
    include: "values,formulas",
    tableMaxRows: 20,
    tableMaxCols: 8,
  });
  if (!inspect?.ndjson) {
    throw new Error("Workbook inspection failed for Overview sheet.");
  }

  await workbook.render({ sheetName: "Overview", range: "A1:H18", scale: 1.5 });
  for (const [, sheetName] of sheetOrder) {
    await workbook.render({ sheetName, range: "A1:F12", scale: 1 });
  }

  await fs.mkdir(outputDir, { recursive: true });
  const exported = await SpreadsheetFile.exportXlsx(workbook);
  await exported.save(outputPath);
  console.log(`Workbook exported to ${outputPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
