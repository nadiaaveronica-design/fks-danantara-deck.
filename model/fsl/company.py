"""Company layer: Financing (corporate loans + capital injection), FSL Financials (two BUMN cases),
Funding Requirement.

Design (no circular references):
  * LT loan repayment = planned share of the balance in the injection year (mode 1), or MIN(planned, fixed proceeds) (mode 2).
  * Interest accrues on the repaid part until the injection date (year fraction) and on the remaining balance for the full year.
  * Each case's Financials sheet carries a pre-equity cash path (opening cash + CFO - capex - debt service - dividends); dividends
    are capped by that pre-equity cash so they are never paid out of the injection. The equity requirement at the injection date is
    the largest shortfall against minimum cash from the injection year onward on that path. The Funding Requirement sheet selects the
    funding case; the Financing sheet books the injection; actual cash = pre-equity path + cumulative injection.
"""
from . import styles as S
from .engine import (Model, YEARS, YEAR_COL, FCOL, LCOL, L, DATA_ROW0, SCALAR_COL, LABEL_COL, UNIT_COL, TYPE_COL, SRC_COL, NOTE_COL, ROW_YEAR)
from .layout import plan_layout, write_layout

T_FS_WO = "FSL Financials — Without BUMN"
T_FS_W = "FSL Financials — With BUMN"
T_FUND = "Funding Requirement"
T_FIN = "Financing"
TAB_CO = "5B9BD5"

WORK_ITEMS = [
    # key, label, source kind, source key, sign note
    ("w_rev", "Revenue", "out", "revenue"),
    ("w_cogs", "Cost of sales", "out", "cogs"),
    ("w_opex", "Operating expenses", "out", "opex"),
    ("w_da", "Depreciation & amortisation", "out", "da"),
    ("w_tax", "Tax on project EBIT (unlevered, line method)", "out", "tax"),
    ("w_nopat", "NOPAT", "out", "nopat"),
    ("w_nci", "Non-controlling share of NOPAT = NOPAT x (1 - FSL interest)", "nci", None),
    ("w_capex", "Capex (IDR bn)", "calc", "capex_idr"),
    ("w_capex_usd", "Capex (USD m)", "calc", "capex_usd"),
    ("w_dnwc", "Increase in net working capital", "calc", "dnwc"),
    ("w_ar", "Trade receivables", "out", "bs_ar"),
    ("w_ap", "Trade payables (negative)", "out", "bs_ap"),
    ("w_ppe", "Fixed assets from project capex (NBV)", "out", "bs_ppe"),
    ("w_depex", "Depreciation of existing / other assets (not project capex)", "depex", None),
    ("w_fcff", "Free cash flow to firm", "out", "fcff"),
    ("w_fund", "Funding need (MAX(0, -FCFF))", "out", "fund_need"),
]


def _fs_rows(specs, case):
    """Row descriptors for one Financials sheet. case: 'wo' or 'w'."""
    flagkey = "flagwo" if case == "wo" else "flagw"
    cname = "Without BUMN" if case == "wo" else "With BUMN"
    rows = []
    rows += [
        ("section", f"Case: {cname} — scope and settings"),
        ("text", "case_name", "Company case", cname, {"bold": True}),
        ("scalar", "n_proj", "Projects included in this case (count)", "count", "=" + "+".join(f"{{g:{flagkey}.{sp['id']}}}" for sp in specs), "int", {}),
        ("text", None, "Scope", ("Existing businesses + committed and planned projects that are switched on in the Global Inputs register; excludes BUMN operatorship schemes (case 2 projects)." if case == "wo"
                                 else "Existing businesses + committed and planned projects switched on + BUMN operatorship schemes (case 2 projects)."), {}),
        ("scalar", "is_funding_case", "This case drives the Funding Requirement (1 = yes)", "0/1", ("=IF({g:funding_case}=1,1,0)" if case == "wo" else "=IF({g:funding_case}=2,1,0)"), "flag01", {}),
        ("note", "Sapphire is excluded (v29 Output_FSL!D2 = 0). Corporate items (LT loan, existing fixed assets, other assets / liabilities, inventory) are held centrally and not allocated to projects."),
        ("blank",),
        ("section", "A. Income statement (IDR bn)"),
        ("row", "revenue", "Revenue", "IDR bn", "={t:w_rev_total}", "idr_bn", {"total": True}),
        ("row", "cogs", "Cost of sales", "IDR bn", "={t:w_cogs_total}", "idr_bn", {"total": True}),
        ("row", "gp", "Gross profit", "IDR bn", "={t:revenue}+{t:cogs}", "idr_bn", {"bold": True, "total": True}),
        ("row", "opex", "Operating expenses", "IDR bn", "={t:w_opex_total}", "idr_bn", {"total": True}),
        ("row", "ebitda", "EBITDA", "IDR bn", "={t:gp}+{t:opex}", "idr_bn", {"bold": True, "total": True}),
        ("row", "da", "Depreciation & amortisation", "IDR bn", "={t:w_da_total}", "idr_bn", {"total": True}),
        ("row", "ebit", "EBIT", "IDR bn", "={t:ebitda}+{t:da}", "idr_bn", {"bold": True, "total": True}),
        ("row", "fin_cost", "Corporate financing cost — existing / LT loan interest (Financing sheet)", "IDR bn", "=-{s:fin:int_total}", "idr_bn", {"total": True, "link": True}),
        ("row", "ebt", "Profit before tax", "IDR bn", "={t:ebit}+{t:fin_cost}", "idr_bn", {"bold": True, "total": True}),
        ("row", "tax_unlev", "Tax on project EBIT (sum of project lines, v29 method)", "IDR bn", "={t:w_tax_total}", "idr_bn", {"total": True, "indent": 1}),
        ("row", "tax_shield", "Tax shield on corporate interest (Global switch)", "IDR bn", "={s:fin:int_shield}", "idr_bn", {"total": True, "indent": 1, "link": True}),
        ("row", "tax", "Tax", "IDR bn", "={t:tax_unlev}+{t:tax_shield}", "idr_bn", {"total": True}),
        ("row", "np", "Net profit", "IDR bn", "={t:ebt}+{t:tax}", "idr_bn", {"bold": True, "total": True}),
        ("row", "nci", "Memo: non-controlling share of project NOPAT (NPLOG 35% etc.; v29 consolidates 100%)", "IDR bn", "={t:w_nci_total}", "idr_bn", {"total": True, "indent": 1}),
        ("row", "np_attrib", "Memo: net profit attributable to FSL shareholders", "IDR bn", "={t:np}-{t:nci}", "idr_bn", {"total": True, "indent": 1}),
        ("row", "m_ebitda", "EBITDA margin", "%", "=IF({t:revenue}=0,0,{t:ebitda}/{t:revenue})", "pct", {}),
        ("row", "m_np", "Net margin", "%", "=IF({t:revenue}=0,0,{t:np}/{t:revenue})", "pct", {}),
        ("blank",),
        ("section", "B. Balance sheet (IDR bn) — 2023 column = opening balances (v29 Output_FSL column I)"),
        ("row", "cash", "Cash and equivalents", "IDR bn", "={t:cf_close}", "idr_bn", {}),
        ("row", "inventory", "Inventory (held flat, centrally)", "IDR bn", "={g:inventory}", "idr_bn2", {"link": True}),
        ("row", "ar", "Trade receivables (sum of projects)", "IDR bn", "={t:w_ar_total}", "idr_bn", {}),
        ("row", "fa_exist", "Fixed assets — existing businesses (unallocated; opening NBV less existing-asset depreciation)", "IDR bn", "={t:fa_exist@prev}-{t:w_depex_total}", "idr_bn", {"f0": "={g:open_fa}"}),
        ("row", "fa_proj", "Fixed assets — project capex (sum of project NBV)", "IDR bn", "={t:w_ppe_total}", "idr_bn", {}),
        ("row", "other_assets", "Other assets (Dec-23 balance excl. reclassified assets under construction; held flat)", "IDR bn", "={g:open_other_assets}", "idr_bn", {"link": True}),
        ("row", "total_assets", "Total assets", "IDR bn", "={t:cash}+{t:inventory}+{t:ar}+{t:fa_exist}+{t:fa_proj}+{t:other_assets}", "idr_bn", {"bold": True}),
        ("row", "ap", "Trade payables (sum of projects)", "IDR bn", "=-{t:w_ap_total}", "idr_bn", {}),
        ("row", "debt", "Bank loans (Financing sheet)", "IDR bn", "={s:fin:debt_close}", "idr_bn", {"link": True}),
        ("row", "other_liab", "Other liabilities (Dec-23 balance; held flat)", "IDR bn", "={g:open_other_liab}", "idr_bn", {"link": True}),
        ("row", "total_liab", "Total liabilities", "IDR bn", "={t:ap}+{t:debt}+{t:other_liab}", "idr_bn", {"bold": True}),
        ("row", "paid_in", "Paid-in capital (opening + capital injection)", "IDR bn", "={s:fin:paid_in}", "idr_bn", {"link": True}),
        ("row", "re", "Retained earnings", "IDR bn", "={t:re@prev}+{t:np}+{t:div_paid}", "idr_bn", {"f0": "={g:open_re}"}),
        ("row", "total_equity", "Total equity", "IDR bn", "={t:paid_in}+{t:re}", "idr_bn", {"bold": True}),
        ("row", "bs_check", "Balance check: assets - liabilities - equity (2023 shows the v29 opening residual of 0.006)", "IDR bn", "={t:total_assets}-{t:total_liab}-{t:total_equity}", "num4", {}),
        ("blank",),
        ("section", "C. Cash flow statement (IDR bn)"),
        ("row", "cf_np", "Net profit", "IDR bn", "={t:np}", "idr_bn", {"total": True}),
        ("row", "cf_da", "Add back depreciation & amortisation", "IDR bn", "=-{t:da}", "idr_bn", {"total": True}),
        ("row", "cf_dnwc", "Increase in net working capital", "IDR bn", "=-{t:w_dnwc_total}", "idr_bn", {"total": True}),
        ("row", "cfo", "Cash flow from operations", "IDR bn", "={t:cf_np}+{t:cf_da}+{t:cf_dnwc}", "idr_bn", {"bold": True, "total": True}),
        ("row", "cf_capex", "Capex (all projects in this case)", "IDR bn", "=-{t:w_capex_total}", "idr_bn", {"total": True}),
        ("row", "cfi", "Cash flow from investing", "IDR bn", "={t:cf_capex}", "idr_bn", {"bold": True, "total": True}),
        ("row", "cf_inj", "Capital injection received (Financing sheet)", "IDR bn", "={s:fin:inj_idr}", "idr_bn", {"total": True, "link": True}),
        ("row", "cf_repay", "Loan repayments — other loans FY2024 and LT loan at the injection date", "IDR bn", "=-{s:fin:debt_service}", "idr_bn", {"total": True, "link": True}),
        ("row", "cf_div", "Dividends paid", "IDR bn", "={t:div_paid}", "idr_bn", {"total": True}),
        ("row", "cff", "Cash flow from financing", "IDR bn", "={t:cf_inj}+{t:cf_repay}+{t:cf_div}", "idr_bn", {"bold": True, "total": True}),
        ("row", "cf_net", "Net cash flow", "IDR bn", "={t:cfo}+{t:cfi}+{t:cff}", "idr_bn", {"bold": True, "total": True}),
        ("row", "cf_open", "Opening cash", "IDR bn", "={t:cf_close@prev}", "idr_bn", {}),
        ("row", "cf_close", "Closing cash", "IDR bn", "={t:cf_open}+{t:cf_net}", "idr_bn", {"f0": "={g:open_cash}", "bold": True}),
        ("row", "cash_check", "Check: closing cash = pre-equity cash path + cumulative injection", "IDR bn", "={t:cf_close}-({t:pre_close}+{s:fin:inj_cum})", "num4", {}),
        ("blank",),
        ("section", "D. Funding roll-forward and dividends (this case) — cash BEFORE new equity; dividends are never paid out of the injection"),
        ("row", "pre_open", "Opening cash — pre-equity path", "IDR bn", "={t:pre_close@prev}", "idr_bn", {}),
        ("row", "pre_cfo", "Cash flow from operations", "IDR bn", "={t:cfo}", "idr_bn", {}),
        ("row", "pre_capex", "Capex", "IDR bn", "={t:cf_capex}", "idr_bn", {}),
        ("row", "pre_repay", "Debt service (principal): other loans FY2024, LT loan at the injection date", "IDR bn", "={t:cf_repay}", "idr_bn", {}),
        ("row", "pre_before_div", "Cash before dividends and new equity", "IDR bn", "={t:pre_open}+{t:pre_cfo}+{t:pre_capex}+{t:pre_repay}", "idr_bn", {"bold": True}),
        ("row", "div_cash_cap", "Dividend cap 1: cash available above the minimum cash (pre-equity)", "IDR bn", "=MAX(0,{t:pre_before_div}-{g:min_cash})", "idr_bn", {"indent": 1}),
        ("row", "div_base", "Profit attributable to FSL shareholders (net profit less non-controlling share)", "IDR bn", "={t:np}-{t:nci}", "idr_bn", {"indent": 1}),
        ("row", "div_payout", "Dividend cap 2: payout ratio x attributable profit", "IDR bn", "=MAX(0,{g:div_payout}*{t:div_base})", "idr_bn", {"indent": 1}),
        ("row", "div_reserve_cap", "Dividend cap 3: net profit + opening retained earnings - statutory reserve", "IDR bn",
         "=MAX(0,{t:np}+{t:re@prev}-{g:reserve_capital_usd}*{g:fx_open}/1000*{g:reserve_pct})", "idr_bn", {"indent": 1}),
        ("row", "div_paid", "Dividends paid = -MIN(caps) x policy switch", "IDR bn", "=-MIN({t:div_payout},{t:div_reserve_cap},{t:div_cash_cap})*{g:div_switch}*{flag}", "idr_bn", {"total": True, "f0": "=0"}),
        ("row", "pre_close", "Cash before new equity (pre-equity path)", "IDR bn", "={t:pre_before_div}+{t:div_paid}", "idr_bn", {"f0": "={g:open_cash}", "bold": True}),
        ("row", "min_cash", "Minimum operating cash", "IDR bn", "={g:min_cash}*{flag}", "idr_bn", {"link": True}),
        ("row", "shortfall", "Shortfall against minimum cash before new equity", "IDR bn", "=MAX(0,{t:min_cash}-{t:pre_close})", "idr_bn", {}),
        ("row", "shortfall_pre", "  of which before the injection year (bridge need — not covered by the injection assumption until received)", "IDR bn", "=IF({y}<{g:inj_year},{t:shortfall},0)", "idr_bn", {"indent": 1}),
        ("row", "shortfall_post", "  of which from the injection year onward", "IDR bn", "=IF({y}>={g:inj_year},{t:shortfall},0)", "idr_bn", {"indent": 1}),
        ("row", "req_inj", "Equity requirement at the injection date = MAX(largest shortfall from the injection year onward, planned LT loan repayment) — this case", "IDR bn",
         "=IF({y}={g:inj_year},MAX(MAX({t:shortfall_post@all}),{s:fin:lt_planned}),0)", "idr_bn", {"bold": True, "total": True,
         "note": "The injection always covers at least the planned loan repayment (board-deck use of proceeds); the shortfall already counts the repayment as a use of cash."}),
        ("row", "gap_after", "Residual gap after the actual injection (should be nil; non-nil if the injection is fixed too low or sized on the other case)", "IDR bn",
         "=MAX(0,{t:min_cash}-{t:cf_close})*{flag}", "idr_bn", {"total": True}),
        ("blank",),
        ("section", "E. Consolidation workings — project outputs x case inclusion flag (column E). Sums feed the statements above."),
    ]
    for key, label, kind, okey in WORK_ITEMS:
        rows.append(("sub", label))
        for sp in specs:
            pid = sp["id"]
            if kind == "out":
                src = f"{{xo:{pid}:{okey}}}"
            elif kind == "calc":
                src = f"{{x:{pid}:{okey}}}"
            elif kind == "nci":
                src = f"{{xo:{pid}:nopat}}*(1-{{xo:{pid}:eint}})"
            elif kind == "depex":
                src = f"({{x:{pid}:da_total}}-{{x:{pid}:dep_new}})"
            fmt = "usd_m" if key == "w_capex_usd" else "idr_bn"
            rows.append(("row", f"{key}.{pid}", f"{pid}  {sp['name']}", "USD m" if fmt == "usd_m" else "IDR bn", f"={src}*{{t:{key}.{pid}@e}}", fmt,
                         {"indent": 1, "link": True, "flagcell": f"{{g:{flagkey}.{pid}}}", "total": True}))
        rows.append(("row", f"{key}_total", f"Total — {label}", "USD m" if key == "w_capex_usd" else "IDR bn",
                     "=" + "+".join(f"{{t:{key}.{sp['id']}}}" for sp in specs), "usd_m" if key == "w_capex_usd" else "idr_bn", {"bold": True, "total": True}))
    return rows


def _fin_rows():
    return [
        ("section", "A. Existing loans (IDR bn) — Dec-23 balance 224.5 = other loans 29.3 (repaid FY2024 as in v29) + LT loan 12 USD m (195.2)"),
        ("row", "oth_open", "Other loans — opening balance", "IDR bn", "={t:oth_close@prev}", "idr_bn", {"f0": "=0"}),
        ("row", "oth_repay", "Other loans — repayment (v29: repaid in FY2024)", "IDR bn", "=IF({y}=2024,{t:oth_open},0)", "idr_bn", {"total": True, "f0": "=0"}),
        ("row", "oth_close", "Other loans — closing balance", "IDR bn", "={t:oth_open}-{t:oth_repay}", "idr_bn", {"f0": "={g:other_loans_idr}"}),
        ("blank",),
        ("row", "lt_open", "LT loan — opening balance", "IDR bn", "={t:lt_close@prev}", "idr_bn", {"f0": "=0"}),
        ("row", "lt_planned", "LT loan — planned repayment from the injection proceeds (share x balance, in the injection year)", "IDR bn", "=IF({y}={g:inj_year},{t:lt_open}*{g:repay_share},0)", "idr_bn", {"total": True, "f0": "=0"}),
        ("row", "lt_repay", "LT loan — actual repayment (mode 1: planned; mode 2: limited to the proceeds received)", "IDR bn",
         "=IF({g:inj_mode}=1,{t:lt_planned},MIN({t:lt_planned},{t:inj_idr}))", "idr_bn", {"total": True, "bold": True, "f0": "=0"}),
        ("row", "lt_shortfall", "LT loan — repayment shortfall (planned - actual); balance stays outstanding", "IDR bn", "={t:lt_planned}-{t:lt_repay}", "idr_bn", {"total": True, "f0": "=0"}),
        ("row", "lt_close", "LT loan — closing balance", "IDR bn", "={t:lt_open}-{t:lt_repay}", "idr_bn", {"f0": "={g:lt_loan_idr}", "bold": True}),
        ("row", "lt_frac", "Fraction of the year the repaid amount is outstanding (injection year: to the injection date)", "%", "=IF({y}={g:inj_year},{g:inj_frac},1)", "pct", {}),
        ("row", "lt_interest", "Interest — FY2024 = v29 figure for all loans; from FY2025 = rate x (balance carried full year + repaid amount x fraction)", "IDR bn",
         "=IF({y}=2024,{g:fin_cost_2024},{g:lt_rate}*(({t:lt_open}-{t:lt_repay})+{t:lt_repay}*{t:lt_frac}))*{flag}", "idr_bn", {"total": True, "f0": "=0"}),
        ("row", "int_total", "Total corporate financing cost", "IDR bn", "={t:lt_interest}", "idr_bn", {"total": True, "bold": True}),
        ("row", "int_shield", "Tax shield on corporate interest = switch x tax rate x interest", "IDR bn", "={g:int_shield}*{g:tax_rate}*{t:int_total}", "idr_bn", {"total": True}),
        ("row", "debt_close", "Total bank loans — closing balance", "IDR bn", "={t:oth_close}+{t:lt_close}", "idr_bn", {"bold": True}),
        ("row", "debt_service", "Debt service (principal repayments)", "IDR bn", "={t:oth_repay}+{t:lt_repay}", "idr_bn", {"total": True}),
        ("row", "lt_flag_repaid", "LT loan repaid in the year (1/0)", "flag", "=IF({t:lt_repay}>0,1,0)", "flag", {}),
        ("scalar", "lt_repay_year", "Year of LT loan repayment (0 = not repaid within the horizon)", "year", "=SUMPRODUCT({t:lt_flag_repaid@all},{g:year@all})", "year", {}),
        ("scalar", "lt_at_val", "LT loan outstanding at the valuation date (enters the equity bridge)", "IDR bn", "=INDEX({t:lt_close@all},MATCH({g:val_year},{g:year@all},0))", "idr_bn", {"bold": True}),
        ("scalar", "lt_shortfall_flag", "Repayment shortfall check", "text", '=IF(SUM({t:lt_shortfall@all})>0.0005,"SHORTFALL — planned repayment not fully funded by the injection; balance retained","OK — planned repayment funded")', "text", {"check": True}),
        ("blank",),
        ("section", "B. Capital injection (new equity) — timing and amount from Global Inputs; amount in mode 1 = equity requirement of the funding case"),
        ("row", "req_selected", "Equity requirement at the injection date — funding case (Funding Requirement sheet)", "IDR bn", "={s:fund:req_sel}", "idr_bn", {"link": True, "total": True}),
        ("row", "inj_idr", "Capital injection received (IDR bn)", "IDR bn", "=IF({y}={g:inj_year},IF({g:inj_mode}=1,{t:req_selected},{g:inj_amount_usd}*{g:fx}/1000),0)", "idr_bn", {"total": True, "bold": True}),
        ("row", "inj_usd", "Capital injection received (USD m)", "USD m", "={t:inj_idr}/{g:fx}*1000", "usd_m", {"total": True}),
        ("row", "inj_cum", "Cumulative capital injection", "IDR bn", "={t:inj_idr@cum}", "idr_bn", {}),
        ("row", "paid_in", "Paid-in capital — closing balance", "IDR bn", "={t:paid_in@prev}+{t:inj_idr}", "idr_bn", {"f0": "={g:open_equity}", "bold": True}),
        ("row", "use_repay", "Use of proceeds: LT loan repayment", "IDR bn", "={t:lt_repay}", "idr_bn", {"total": True}),
        ("row", "use_other", "Use of proceeds: project funding and minimum cash (balance)", "IDR bn", "={t:inj_idr}-{t:lt_repay}", "idr_bn", {"total": True}),
        ("note", "Mode 1 repays the planned amount by construction (the requirement includes it as a funding use). Mode 2 tests a fixed amount: with insufficient proceeds the unpaid balance is retained and flagged above; with nil proceeds the loan is carried and keeps accruing interest."),
    ]


def _fund_rows(specs):
    rows = [
        ("section", "A. How much equity do we need? (headline answers)"),
        ("text", "fund_case_name", "Operating case underlying the funding calculation (Global Inputs switch)", '=IF({g:funding_case}=1,"Without BUMN (conservative)","With BUMN")', {"bold": True, "link": True}),
        ("scalar", "inj_date_disp", "Capital injection date (provisional — Global Inputs)", "date", "={g:inj_date}", "date", {"link": True}),
        ("scalar", "inj_mode_disp", "Injection amount mode (1 = computed requirement, 2 = fixed amount)", "1/2", "={g:inj_mode}", "flag01", {"link": True}),
        ("scalar", "req_sel_total", "Equity requirement — valuation-scope operations incl. LT loan repayment (funding case), IDR bn", "IDR bn", "=SUM({t:req_sel@all})", "idr_bn", {"bold": True}),
        ("scalar", "req_sel_total_usd", "   same in USD m (injection-year exchange rate)", "USD m", "={t:req_sel_total}/INDEX({g:fx@all},MATCH({g:inj_year},{g:year@all},0))*1000", "usd_m", {}),
        ("scalar", "capexonly_total", "Additional capex-only request — Badas (when outside the valuation) and funding-only placeholders F01-F05, IDR bn", "IDR bn", "=SUM({t:co_total@all})", "idr_bn", {"bold": True}),
        ("scalar", "total_request", "TOTAL EQUITY FUNDING REQUEST (IDR bn)", "IDR bn", "={t:req_sel_total}+{t:capexonly_total}", "idr_bn", {"bold": True}),
        ("scalar", "total_request_usd", "TOTAL EQUITY FUNDING REQUEST (USD m)", "USD m", "={t:total_request}/INDEX({g:fx@all},MATCH({g:inj_year},{g:year@all},0))*1000", "usd_m", {"bold": True}),
        ("scalar", "prov_total", "   of which depends on provisional / DUMMY assumptions (Badas dummy capex, blank placeholders, unconfirmed pre-valuation spend timing)", "IDR bn", "={t:capexonly_total}+{t:req_prov_share}", "idr_bn", {}),
        ("scalar", "req_prov_share", "   unconfirmed pre-valuation capex (v29 timing, not actuals) within the valuation-scope requirement, IDR bn", "IDR bn",
         "=MIN({t:req_sel_total},-SUMPRODUCT({t:capex_sel@all},--({g:year@all}<={g:val_year}),--({g:year@all}>=2024)))", "idr_bn", {}),
        ("scalar", "repay_in_req", "   of which planned LT loan repayment funded from the proceeds", "IDR bn", "=SUM({s:fin:lt_planned@all})", "idr_bn", {"link": True}),
        ("scalar", "bridge_need", "Bridge need before the injection (largest pre-injection shortfall against minimum cash) — to be covered by shareholder / bank bridge", "IDR bn", "=MAX({t:shortfall_pre_sel@all})", "idr_bn", {}),
        ("scalar", "req_wo", "Comparison: requirement Without BUMN", "IDR bn", "=SUM({s:fs_wo:req_inj@all})", "idr_bn", {"link": True}),
        ("scalar", "req_w", "Comparison: requirement With BUMN", "IDR bn", "=SUM({s:fs_w:req_inj@all})", "idr_bn", {"link": True}),
        ("scalar", "resid_gap_sel", "Residual gap after the actual injection (funding case) — nil in mode 1", "IDR bn", "=SUM({t:gap_after_sel@all})", "idr_bn", {}),
        ("note", "Equity requirement (cash to be contributed) is NOT the equity value of FSL — see the Valuation sheets."),
        ("blank",),
        ("section", "B. Cash roll-forward — funding case (linked from the selected FSL Financials sheet; IDR bn)"),
    ]
    sel = lambda k: f"=IF({{g:funding_case}}=1,{{s:fs_wo:{k}}},{{s:fs_w:{k}}})"
    for key, label, fmt, opts in [
        ("pre_open_sel", "Opening cash (pre-equity path)", "idr_bn", {}),
        ("cfo_sel", "+ Cash flow from operations (net profit + D&A - working capital increase; interest and tax inside net profit)", "idr_bn", {}),
        ("capex_sel", "- Project investment (capex, projects in the case)", "idr_bn", {"total": True}),
        ("repay_sel", "- Debt service: other loans FY2024, LT loan repayment at the injection", "idr_bn", {"total": True}),
        ("div_sel", "- Dividends (policy; capped by pre-equity cash)", "idr_bn", {"total": True}),
        ("pre_close_sel", "Cash before new equity", "idr_bn", {"bold": True}),
        ("min_cash_sel", "Minimum operating cash", "idr_bn", {}),
        ("shortfall_sel", "Shortfall against minimum cash (before new equity)", "idr_bn", {}),
        ("shortfall_pre_sel", "  before the injection year (bridge need)", "idr_bn", {}),
        ("shortfall_post_sel", "  from the injection year onward", "idr_bn", {}),
        ("req_sel", "EQUITY REQUIREMENT at the injection date = largest shortfall from the injection year onward", "idr_bn", {"bold": True, "total": True}),
        ("inj_sel", "Capital injection received (Financing sheet)", "idr_bn", {"total": True}),
        ("cash_sel", "Closing cash after the injection", "idr_bn", {"bold": True}),
        ("gap_after_sel", "Residual gap after the injection", "idr_bn", {"total": True}),
    ]:
        src = {"pre_open_sel": "pre_open", "cfo_sel": "pre_cfo", "capex_sel": "pre_capex", "repay_sel": "pre_repay", "div_sel": "div_paid", "pre_close_sel": "pre_close",
               "min_cash_sel": "min_cash", "shortfall_sel": "shortfall", "shortfall_pre_sel": "shortfall_pre", "shortfall_post_sel": "shortfall_post", "req_sel": "req_inj",
               "inj_sel": "cf_inj", "cash_sel": "cf_close", "gap_after_sel": "gap_after"}[key]
        o = dict(opts)
        o["link"] = True
        rows.append(("row", key, label, "IDR bn", sel(src), fmt, o))
    rows += [
        ("note", "No double counting: interest and tax are inside net profit (CFO); working-capital movements are inside CFO; the LT loan repayment appears once, as debt service."),
        ("blank",),
        ("section", "C. Funding needs by project and year — projects in the funding case (cash shortfall = MAX(0, -FCFF); IDR bn)"),
    ]
    for sp in specs:
        pid = sp["id"]
        rows.append(("row", f"pn.{pid}", f"{pid}  {sp['name']}", "IDR bn", f"={{xo:{pid}:fund_need}}*IF({{g:funding_case}}=1,{{g:flagwo.{pid}}},{{g:flagw.{pid}}})", "idr_bn", {"indent": 1, "link": True, "total": True}))
    rows += [
        ("row", "pn_total", "Total project funding needs (before internally generated surpluses of other projects)", "IDR bn", "=" + "+".join(f"{{t:pn.{sp['id']}}}" for sp in specs), "idr_bn", {"bold": True, "total": True}),
        ("row", "pn_repay", "LT loan repayment at the injection (planned)", "IDR bn", "={s:fin:lt_planned}", "idr_bn", {"link": True, "total": True}),
        ("note", "The company-level requirement in section B is lower than the sum of project needs where cash generated by other businesses funds them."),
        ("blank",),
        ("section", "D. Capex-only projects (no feasibility study — excluded from valuation, included in the funding request): Badas and five placeholders"),
        ("row", "co_badas", "Badas capex while outside the valuation (P19 Badas Calc x (1 - in valuation) x funding-inclusion switch) — DUMMY capex", "IDR bn",
         ("={x:P19:capex_idr}*(1-{g:incl.P19})*{g:badas_in_funding}" if any(sp["id"] == "P19" for sp in specs) else "=0"), "idr_bn", {"link": True, "total": True}),
    ]
    for i in range(1, 6):
        f = f"F0{i}"
        rows += [
            ("sub", f"{f} — funding-only placeholder (fill name, total capex in USD m, spending % by year and the include switch; leave blank if unused)"),
            ("text", f"{f}_name", f"{f} project name", "", {"input": True}),
            ("scalar", f"{f}_total", f"{f} total capex", "USD m", 0, "usd_m", {"cls": "CONTROL", "note": "Blank / 0 = inactive placeholder (error-free)."}),
            ("scalar", f"{f}_incl", f"{f} include in the funding request (1 = yes)", "0/1", 0, "flag01", {"cls": "CONTROL"}),
            ("values", f"{f}_pct", f"{f} spending % of total capex by year (must add to 100% when used)", "%", {y: 0 for y in YEARS}, "pct", {"cls": "CONTROL", "total": True}),
            ("row", f"{f}_usd", f"{f} capex (USD m)", "USD m", f"={{t:{f}_total}}*{{t:{f}_pct}}*{{t:{f}_incl}}", "usd_m", {"total": True}),
            ("row", f"{f}_idr", f"{f} capex (IDR bn) = USD m x FX / 1,000 — 100% equity-funded request (no FS, no revenue, no return assumed)", "IDR bn", f"={{t:{f}_usd}}*{{g:fx}}/1000", "idr_bn", {"total": True}),
            ("scalar", f"{f}_check", f"{f} allocation check", "text", f'=IF({{t:{f}_total}}*{{t:{f}_incl}}=0,"inactive",IF(ABS(SUM({{t:{f}_pct@all}})-1)<0.000001,"PASS","CHECK: % not 100%"))', "text", {"check": True}),
            ("text", None, f"{f} operating results / returns", "FS not available — capex requirement only", {}),
        ]
    rows += [
        ("row", "co_placeholders", "Funding-only placeholders F01-F05 — total capex (IDR bn)", "IDR bn", "=" + "+".join(f"{{t:F0{i}_idr}}" for i in range(1, 6)), "idr_bn", {"bold": True, "total": True}),
        ("row", "co_total", "Total capex-only request (IDR bn) — never enters the valuation or the company statements", "IDR bn", "={t:co_badas}+{t:co_placeholders}", "idr_bn", {"bold": True, "total": True}),
        ("blank",),
        ("section", "E. Bridge: valuation-scope requirement -> total equity funding request (IDR bn by year)"),
        ("row", "br_req", "Equity requirement — valuation-scope operations (funding case), received in the injection year", "IDR bn", "={t:req_sel}", "idr_bn", {"total": True}),
        ("row", "br_repay", "   memo: of which planned LT loan repayment", "IDR bn", "={s:fin:lt_planned}", "idr_bn", {"indent": 1, "total": True, "link": True}),
        ("row", "br_badas", "+ Badas capex-only (DUMMY, when outside the valuation)", "IDR bn", "={t:co_badas}", "idr_bn", {"total": True}),
        ("row", "br_ph", "+ Funding-only placeholders F01-F05", "IDR bn", "={t:co_placeholders}", "idr_bn", {"total": True}),
        ("row", "br_total", "TOTAL equity funding request by year", "IDR bn", "={t:br_req}+{t:br_badas}+{t:br_ph}", "idr_bn", {"bold": True, "total": True}),
        ("row", "br_total_usd", "TOTAL equity funding request by year (USD m)", "USD m", "={t:br_total}/{g:fx}*1000", "usd_m", {"bold": True, "total": True}),
        ("row", "br_prov", "   of which provisional / DUMMY (capex-only items)", "IDR bn", "={t:br_badas}+{t:br_ph}", "idr_bn", {"indent": 1, "total": True}),
        ("note", "Capital raised for capex-only projects is ring-fenced: it is not routed through the company cash balance and therefore never appears in the valuation as excess cash."),
        ("blank",),
        ("section", "F. Use of proceeds — board deck Dec-2024 (user screenshot) vs v29 and this model (USD m, total project capex)"),
    ]
    deck = [
        ("Cigading Wharf 2", None, None, 12.8, "P01"), ("Cigading Ext. Conveyor", 8.0, None, 8.0, "P02"), ("Belawan / Medan (SGT3)", 14.0, None, 14.0, "E3"),
        ("Ciwandan Expansion (v29: Ciwandan 5.0 + KBS warehouse revitalisation 6.0)", 17.0, None, 11.0, ("P06", "P03")), ("Teluk Lamong silo (Surabaya, NP Log)", None, None, 3.8, "P04"),
        ("Dumai", None, 20.0, 6.8, "P05"), ("Badas", None, 10.0, None, "P19"), ("Port long-term warehouse storage", None, 60.0, None, None), ("Vietnam", None, 15.0, None, None),
    ]
    rows.append(("custom", lambda m, sk, r, ctx: _uop_header(m, sk, r)))
    for label, s1, s2, v29, pid in deck:
        rows.append(("custom", (lambda label, s1, s2, v29, pid: (lambda m, sk, r, ctx: _uop_row(m, sk, r, ctx, label, s1, s2, v29, pid)))(label, s1, s2, v29, pid)))
    rows.append(("custom", lambda m, sk, r, ctx: _uop_row(m, sk, r, ctx, "LT loan repayment", 12.0, None, 12.0, "LOAN")))
    rows.append(("note", "Stage 1 / Stage 2 columns = board deck Dec-2024 use of proceeds as supplied by the user (UPDATED information). v29 column = V29 Ruby FM totals. Model column links to the project Input sheets (v29 totals retained; Badas provisional 10.0)."))
    return rows


def _uop_header(m, sk, r):
    ws = m.ws(sk)
    for i, h in enumerate(["Project", "Board deck Stage 1", "Board deck Stage 2", "v29 model", "This model", "Model source"]):
        c = ws.cell(r, 2 + i)
        c.value = h
        c.font = S.F_HDR
        c.fill = S.FILL_HDR
        c.alignment = S.A_CENTER
    ws.cell(r, 2).alignment = S.A_LEFT


def _uop_row(m, sk, r, ctx, label, s1, s2, v29, pid):
    ws = m.ws(sk)
    ws.cell(r, 2).value = label
    ws.cell(r, 2).font = S.F_BODY
    for col, v in [(3, s1), (4, s2), (5, v29)]:
        c = ws.cell(r, col)
        c.value = v if v is not None else "-"
        c.number_format = S.NF["usd_m1"]
        c.font = S.F_INPUT if col in (3, 4) else S.F_BODY
        c.alignment = S.A_RIGHT
        if col in (3, 4) and v is not None:
            c.fill = S.FILL_UPDATED
    c = ws.cell(r, 6)
    present = (pid == "LOAN") or (pid is None) or (all(p in m.projects for p in pid) if isinstance(pid, tuple) else pid in m.projects)
    if not present:
        c.value = "-"
        src = "project sheets not built in this workbook"
    elif pid == "LOAN":
        c.value = "={g:lt_loan_usd}"
        src = "Global Inputs — LT loan principal"
    elif pid is None:
        c.value = "-"
        src = "Not in v29 / no FS — use a funding-only placeholder F01-F05 if a capex figure is to be included"
    elif isinstance(pid, tuple):
        c.value = "=" + "+".join(f"{{xin:{p}:capex_total_usd}}" for p in pid)
        src = " + ".join(f"{p} Input" for p in pid) + " (INFERRED grouping — to confirm)"
    else:
        c.value = f"={{xin:{pid}:capex_total_usd}}"
        src = f"{pid} Input — total project capex"
    if isinstance(c.value, str) and c.value.startswith("="):
        c.value = m.resolve(c.value, 6, ctx)
    c.number_format = S.NF["usd_m1"]
    c.font = S.F_LINK
    c.alignment = S.A_RIGHT
    ws.cell(r, 7).value = src
    ws.cell(r, 7).font = S.F_NOTE


class CompanyPlan:
    def __init__(self, model: Model, specs):
        self.m = model
        self.specs = specs
        model.add_sheet("fs_wo", T_FS_WO, TAB_CO)
        model.add_sheet("fs_w", T_FS_W, TAB_CO)
        model.add_sheet("fund", T_FUND, "C00000")
        model.add_sheet("fin", T_FIN, TAB_CO)
        self.p_fs_wo, _ = plan_layout(model, "fs_wo", _fs_rows(specs, "wo"))
        self.p_fs_w, _ = plan_layout(model, "fs_w", _fs_rows(specs, "w"))
        self.p_fund, _ = plan_layout(model, "fund", _fund_rows(specs))
        self.p_fin, _ = plan_layout(model, "fin", _fin_rows())

    def write(self):
        m = self.m
        for key, planned, title, sub in [
            ("fs_wo", self.p_fs_wo, "FSL FINANCIALS — WITHOUT BUMN (integrated income statement, balance sheet, cash flow)",
             "Sum of project outputs included in the Without-BUMN case + corporate items (LT loan, existing fixed assets, other balances). IDR bn. Green = link; black = formula."),
            ("fs_w", self.p_fs_w, "FSL FINANCIALS — WITH BUMN (integrated income statement, balance sheet, cash flow)",
             "Sum of project outputs included in the With-BUMN case (incl. BUMN operatorship schemes) + corporate items. IDR bn."),
            ("fund", self.p_fund, "FUNDING REQUIREMENT — how much equity do we need, and when?",
             "Cash roll-forward of the selected operating case: investment, internally generated cash, minimum cash, debt service incl. the LT loan repayment at the injection, remaining equity gap; capex-only projects added separately. IDR bn."),
            ("fin", self.p_fin, "FINANCING — corporate loans and capital injection",
             "LT loan carried until the capital injection; repayment linked to the proceeds received; interest to the repayment date. IDR bn."),
        ]:
            m.write_ts_header(key, title, sub)
            ctx = {"sheet": key, "pid": None}
            write_layout(m, key, planned, ctx)
            m.set_print(key)
        # flag cells for consolidation workings (column E holds the case flag)
        for key, planned in [("fs_wo", self.p_fs_wo), ("fs_w", self.p_fs_w)]:
            ws = m.ws(key)
            ctx = {"sheet": key, "pid": None}
            for r, d in planned:
                if d[0] == "row" and d[6] and d[6].get("flagcell"):
                    c = ws.cell(r, SCALAR_COL)
                    c.value = m.resolve("=" + d[6]["flagcell"], SCALAR_COL, ctx)
                    c.number_format = S.NF["flag01"]
                    c.font = S.F_LINK
                    c.alignment = S.A_CENTER
            ws.cell(ROW_YEAR, SCALAR_COL).value = "Flag / total"
        # placeholder name cells as inputs on the funding sheet
        ws = m.ws("fund")
        for r, d in self.p_fund:
            if d[0] == "text" and d[4] and d[4].get("input"):
                c = ws.cell(r, SCALAR_COL)
                c.font = S.F_INPUT
                c.fill = S.FILL_CONTROL
                c.value = None
