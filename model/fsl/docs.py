"""Navigation and Model Flow sheets (documentation layer)."""
from . import styles as S
from .engine import Model, GLOBAL_TITLE, L
from .company import T_FS_WO, T_FS_W, T_FUND, T_FIN

T_NAV = "Navigation"
T_FLOW = "Model Flow"
T_SUMMARY = "Project Summary"
T_VAL_WO = "Valuation — Without BUMN"
T_VAL_W = "Valuation — With BUMN"
T_CHECKS = "Checks"
T_RECON = "Reconciliation v29"


def plan_docs(model: Model):
    model.add_sheet("nav", T_NAV, "1F3864", ts=False, widths={"A": 2, "B": 34, "C": 46, "D": 16, "E": 16, "F": 16, "G": 60})
    model.add_sheet("flow", T_FLOW, "1F3864", ts=False, widths={"A": 2, "B": 30, "C": 120})


def _link(ws, r, c, text, target):
    cell = ws.cell(r, c)
    cell.value = text
    cell.hyperlink = f"#'{target}'!A1"
    cell.font = S.F_NAV
    return cell


def write_docs(model: Model, specs):
    ws = model.ws("nav")
    ws["B1"] = "FSL — FKS Solusi Logistik — Financial Model (revised from v29)"
    ws["B1"].font = S.F_TITLE
    ws["B2"] = "Valuation date 31-Dec-2026 · IDR bn unless stated · Sapphire excluded · two BUMN cases · built with live Excel formulas"
    ws["B2"].font = S.F_SUB
    r = 4
    ws.cell(r, 2).value = "Start here"
    ws.cell(r, 2).font = S.F_BOLD
    r += 1
    for text, target, desc in [
        ("Model Flow", T_FLOW, "How the model is organised, what changed versus v29, how to use the controls, tests performed."),
        ("Global Inputs", GLOBAL_TITLE, "Shared assumptions, switches (depreciation method, funding case, Badas funding), valuation parameters, project register (inclusion / case / interest)."),
        ("Project Summary", T_SUMMARY, "One section per project (income statement, FCFF, capex, funding need, returns) + comparison table."),
        (T_FS_WO, T_FS_WO, "Integrated statements — Without BUMN case."),
        (T_FS_W, T_FS_W, "Integrated statements — With BUMN case."),
        (T_FUND, T_FUND, "How much equity do we need and when: cash roll-forward, requirement at the injection date, capex-only projects, bridge, use of proceeds."),
        (T_FIN, T_FIN, "Corporate loans: LT loan carried until the capital injection; interest to the repayment date; injection booking."),
        (T_VAL_WO, T_VAL_WO, "DCF from FY2027 at 31-Dec-2026 — Without BUMN."),
        (T_VAL_W, T_VAL_W, "DCF from FY2027 at 31-Dec-2026 — With BUMN."),
        (T_CHECKS, T_CHECKS, "Formula-based integrity checks (balance sheet, cash, consolidation, funding, valuation timing, capex allocation)."),
        (T_RECON, T_RECON, "Line-by-line reconciliation to v29 (Output_FSL) with explanations of the differences."),
    ]:
        _link(ws, r, 2, text, target)
        ws.cell(r, 3).value = desc
        ws.cell(r, 3).font = S.F_NOTE
        r += 1
    r += 1
    hdr = ["Project", "Description", "Input", "Calc", "Output", "Category / notes"]
    for i, h in enumerate(hdr):
        c = ws.cell(r, 2 + i)
        c.value = h
        c.font = S.F_HDR
        c.fill = S.FILL_HDR
    r += 1
    for sp in specs:
        pid = sp["id"]
        base = f"{pid} {sp['code']}"
        ws.cell(r, 2).value = f"{pid}  {sp['name']}"
        ws.cell(r, 2).font = S.F_BOLD
        ws.cell(r, 3).value = sp.get("description", "")
        ws.cell(r, 3).font = S.F_NOTE
        ws.cell(r, 3).alignment = S.A_WRAP
        for c, suffix in [(4, "Input"), (5, "Calc"), (6, "Output")]:
            title = model.title(f"{pid}:in") if suffix == "Input" else (model.title(f"{pid}:calc") if suffix == "Calc" else model.title(f"{pid}:out"))
            _link(ws, r, c, suffix, title)
        ws.cell(r, 7).value = f"{sp.get('category','')} — {sp.get('entity_short','')}"
        ws.cell(r, 7).font = S.F_NOTE
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
    ws.cell(r, 2).value = "Colour conventions"
    ws.cell(r, 2).font = S.F_BOLD
    r += 1
    for fill, text in [(S.FILL_INPUT, "Blue text on pale yellow = hard-coded input (v29 source or derived)"), (S.FILL_CONTROL, "Bold blue on gold = control / switch"),
                       (S.FILL_CHANGE, "Light blue = user-requested modelling change"), (S.FILL_UPDATED, "Light green = updated information supplied by the user"),
                       (S.FILL_PROV, "Orange = provisional — to confirm"), (S.FILL_DUMMY, "Salmon = DUMMY — REPLACE WITH FS DATA (Badas)"),
                       (S.FILL_WHITE, "Black text = formula; green text = link from another sheet; blue underlined = navigation link")]:
        ws.cell(r, 2).fill = fill
        ws.cell(r, 3).value = text
        ws.cell(r, 3).font = S.F_NOTE
        r += 1
    model.set_print("nav", landscape=False)

    # ---------------- Model Flow (detailed explanations)
    ws = model.ws("flow")
    ws["B1"] = "MODEL FLOW — architecture, changes versus v29, controls, tests"
    ws["B1"].font = S.F_TITLE
    ws["B2"] = "Detailed explanations live here so that calculation sheets stay focused on drivers and numbers."
    ws["B2"].font = S.F_SUB
    r = 4
    for head, body in FLOW_TEXT:
        ws.cell(r, 2).value = head
        ws.cell(r, 2).font = S.F_BOLD
        ws.cell(r, 2).alignment = S.A_WRAP
        ws.cell(r, 3).value = body
        ws.cell(r, 3).font = S.F_BODY
        ws.cell(r, 3).alignment = S.A_WRAP
        lines = max(1, len(body) // 115 + body.count("\n") + 1)
        ws.row_dimensions[r].height = 13 * lines + 4
        r += 1
    model.set_print("flow", landscape=False)


FLOW_TEXT = [
    ("1. Purpose", "Revised FSL model built from V29_Ruby_FM_Danantara.xlsm (v29) with live formulas. v29 remains the source of business assumptions and calculation logic; "
     "the changes requested by the user are: valuation date 31-Dec-2026 with a DCF from FY2027, LT loan repaid when the capital injection is received, capex spending controlled "
     "by annual percentages, Badas built as a feasibility-study working paper, a funding requirement sheet with five capex-only placeholders, and separate With / Without BUMN cases. Sapphire stays excluded."),
    ("2. Architecture", "Global Inputs (shared assumptions and the project register) -> one Input / Calc / Output triplet per project -> Project Summary and the two FSL Financials sheets "
     "(sum of project outputs x case flags + corporate items) -> Funding Requirement and Financing (LT loan, injection) -> two Valuation sheets -> Checks and Reconciliation.\n"
     "Sheet names carry the project ID and code (e.g. 'P02 CigConveyor Input / Calc / Output'). Every time-series sheet uses the same columns: F = 2023 (opening / pre-2024), G..S = 2024..2036."),
    ("3. Inputs and classification", "Column D on every input row classifies the assumption: v29 (value and cell reference from v29, including effective values typed inside v29 formulas), "
     "DERIVED (computed from v29), UPDATED (information supplied by the user, e.g. the board-deck use of proceeds), CHANGE (user-requested modelling change), DUMMY (Badas placeholders to be replaced "
     "with FS data), PROV (provisional, to confirm), CONTROL (switch). Annual assumptions have one editable cell per year; genuine one-off parameters sit in column E."),
    ("4. Project sheets", "Input: register, controls (links to Global Inputs), commissioning year, operating assumptions, capex allocation (total USD m, % by year, USD and IDR schedules, "
     "pre- vs post-valuation split, allocation check, building share, useful lives). Calc: operating flag, revenue and cost drivers exactly as v29 computes them, capex and depreciation, "
     "working capital. Output: unlevered project income statement (tax on project EBIT, v29 line method), FCFF, net operating assets (no project-level cash or debt), funding need, returns "
     "(NPV at the valuation date, full-life IRR with and without terminal value, payback), case inclusion flags."),
    ("5. Two BUMN cases", "v29 Output_FSL is the With-BUMN case: it includes the 'Operatorship with BUMN' block (FSL's entitlement under the Pelindo Teluk Lamong, KBS Cigading and Pelindo "
     "Belawan operatorship schemes; v29 Output_FSL!F35 = 1). The Without-BUMN case removes the case-2 projects (register column 'Case' = 2). Both cases are computed at the same time on "
     "their own Financials and Valuation sheets; the Funding Requirement uses the case selected on Global Inputs (default: Without BUMN, conservative). DMS trucking fees are shared 50/50 "
     "with the port operator but are kept in both cases as in v8; set their case to 2 on the register to treat them as BUMN-dependent."),
    ("6. Valuation date and DCF", "Valuation date 31-Dec-2026 (Global Inputs). Only FCFF of years after the valuation date enters the DCF (flag row 'DCF window'); FY2027 is discounted "
     "one full year (year-end convention). FCFF = EBIT - tax on EBIT (sum of project line taxes) + D&A - capex - increase in working capital, unlevered and consistent with WACC. "
     "Terminal value: Gordon growth on a normalised FY2036 cash flow (capex = factor x depreciation, working capital growing with g). Equity bridge at 31-Dec-2026: + cash, - LT loan "
     "outstanding at that date (depends on whether the injection date falls before or after it), +/- other balances (switch), - non-controlling interests (35% of NPLOG line values)."),
    ("7. LT loan and capital injection", "The 12 USD m LT loan (195.2 IDR bn) is carried until the capital injection. Injection date and mode are inputs on Global Inputs "
     "(provisional 30-Jun-2027). Mode 1 sizes the injection to the equity requirement of the funding case; mode 2 uses a fixed amount. Repayment = planned share of the balance in the "
     "injection year, limited in mode 2 to the proceeds received; any unpaid balance is retained, flagged, and keeps accruing interest. Interest accrues on the repaid part to the injection "
     "date and on the remaining balance for the full year. The equity receipt and the loan repayment are separate lines in the cash-flow statement. No circular references: the requirement "
     "is computed on a pre-equity cash path; dividends are capped by that path so they are never paid out of the injection."),
    ("8. Capex percentages", "Each project's capex = total (USD m) x annual % of total (Input sheet). The 2023 column is pre-2024 (sunk) spend; columns up to the valuation year are "
     "pre-valuation estimates (v29 projected timing; actuals not supplied — flag 'historical spend confirmed' = 0). Only spend after the valuation date enters the 2027+ DCF. Depreciation "
     "method switch: 2 (default) depreciates each year's spend over its life from MAX(spend year, commissioning); 1 reproduces v29 (total x share / life from commissioning, no end)."),
    ("9. Badas", "P19 Badas is a complete project template with DUMMY inputs (salmon rows, 'DUMMY — REPLACE WITH FS DATA'). Its working paper lists definition, unit, period, "
     "status and destination for every requested input plus questions for the operations team. Badas is excluded from the headline valuation by default (register 'In valuation' = 0) "
     "while its capex (provisional 10 USD m from the board deck) enters the funding request through the separate 'Badas in funding' switch."),
    ("10. Funding-only placeholders", "F01-F05 on the Funding Requirement sheet accept a name, total capex (USD m), annual % and an include switch. They add to the equity request "
     "only; they never enter the statements or the valuation and carry no revenue, profit or return ('FS not available')."),
    ("11. Corporate and unallocated items", "Existing fixed assets (Dec-23 NBV 826.0), other assets, other liabilities, inventory, the loans and paid-in capital are company-level "
     "balances from v29 and are not allocated to projects. Dec-23 receivables and payables are allocated to the existing businesses pro rata FY2024 activity (labelled as an allocation). "
     "Pre-2024 project spend on Wharf 2 and the conveyor (assets under construction) is reclassified from other assets to project fixed assets."),
    ("12. Reconciliation to v29", "The Reconciliation sheet compares the With-BUMN case with v29 Output_FSL line by line and explains each difference (valuation date, LT loan timing and "
     "interest, depreciation method, injection basis, inventory and other v29 formula breaks). Setting depreciation method = 1 and the injection date to 31-Dec-2025 reproduces v29's "
     "income statement through EBIT; v29's two equity tranches (FY2026-27 capex) are replaced by one requirement-based injection."),
    ("13. Checks", "All checks are live formulas (PASS / FAIL): balance sheets, cash reconciliation, sum of projects = company, capex allocations = 100%, sources = uses, valuation "
     "date and DCF window, loan repayment <= balance, residual funding gap in mode 1, non-negative dividends, project NPVs vs enterprise value."),
    ("14. Calculation engine and tests", "Recalculated and tested with LibreOffice Calc (headless), not Microsoft Excel. Tests: injection date moved (2026 / 2028) moves the repayment "
     "and interest; zero / insufficient proceeds keep the loan outstanding; capex % moved between years updates capex, depreciation, cash and funding; Badas dummy inputs replaced update "
     "its sheets; inclusion switches affect the correct case; funding-only placeholders change the request but not the valuation; project outputs reconcile to company outputs; "
     "balance sheets and cash reconcile. Settings were restored to the delivery values after testing (see model/tests/)."),
]
