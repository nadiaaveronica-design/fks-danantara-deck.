"""Valuation sheets (one per BUMN case): operating projections, FCFF, discounting from the valuation
date, terminal value, enterprise value, equity bridge, sensitivity, value by project."""
from . import styles as S
from .engine import Model, YEARS, YEAR_COL, FCOL, LCOL, L, SCALAR_COL, ROW_YEAR
from .layout import plan_layout, write_layout

T_VAL_WO = "Valuation — Without BUMN"
T_VAL_W = "Valuation — With BUMN"
TAB = "7030A0"


def _rows(specs, case):
    fs = "fs_wo" if case == "wo" else "fs_w"
    cname = "Without BUMN" if case == "wo" else "With BUMN"
    flagkey = "flagwo" if case == "wo" else "flagw"
    nci_terms = "+".join(f"(1-{{xo:{sp['id']}:eint}})*{{xo:{sp['id']}:r_npv}}*{{g:{flagkey}.{sp['id']}}}" for sp in specs)
    rows = [
        ("section", f"A. Basis — case: {cname}"),
        ("text", "case", "Company case valued", cname, {"bold": True}),
        ("scalar", "val_date", "Valuation date", "date", "={g:val_date}", "date", {"link": True, "bold": True}),
        ("scalar", "first_year", "First year of cash flows in the DCF (year-end convention: discounted one full year)", "year", "={g:first_dcf_year}", "year", {"link": True}),
        ("text", None, "Currency / units", "IDR bn (USD m at the valuation-year exchange rate where shown)", {}),
        ("scalar", "wacc", "WACC (Global Inputs — provisional build-up)", "%", "={g:wacc}", "pct2", {"link": True}),
        ("scalar", "tg", "Terminal growth rate", "%", "={g:tg}", "pct2", {"link": True}),
        ("scalar", "tv_factor", "Terminal-year normalised capex as a multiple of depreciation", "x", "={g:tv_capex_factor}", "num2", {"link": True}),
        ("scalar", "n_proj", "Projects included in this case (Global Inputs register)", "count", f"={{s:{fs}:n_proj}}", "int", {"link": True}),
        ("text", None, "Scope", ("Existing businesses and projects switched on, excluding BUMN operatorship schemes." if case == "wo" else
                                 "Existing businesses and projects switched on, including BUMN operatorship schemes (case 2)."), {}),
        ("text", None, "Excluded from this valuation", "Sapphire (v29 switch = 0); Badas while its register switch is 0 (dummy FS data); funding-only placeholders F01-F05; TBM unless switched on.", {}),
        ("blank",),
        ("section", "B. Operating projections and unlevered free cash flow (linked to the FSL Financials of this case; IDR bn)"),
        ("row", "revenue", "Revenue", "IDR bn", f"={{s:{fs}:revenue}}", "idr_bn", {"link": True}),
        ("row", "ebitda", "EBITDA", "IDR bn", f"={{s:{fs}:ebitda}}", "idr_bn", {"link": True}),
        ("row", "ebit", "EBIT", "IDR bn", f"={{s:{fs}:ebit}}", "idr_bn", {"link": True, "bold": True}),
        ("row", "tax", "Tax on EBIT (sum of project line taxes; excludes the corporate interest shield)", "IDR bn", f"={{s:{fs}:tax_unlev}}", "idr_bn", {"link": True}),
        ("row", "nopat", "NOPAT", "IDR bn", "={t:ebit}+{t:tax}", "idr_bn", {"bold": True}),
        ("row", "da", "Add back depreciation & amortisation", "IDR bn", f"=-{{s:{fs}:da}}", "idr_bn", {"link": True}),
        ("row", "capex", "Less capex", "IDR bn", f"={{s:{fs}:cf_capex}}", "idr_bn", {"link": True}),
        ("row", "dnwc", "Less increase in net working capital", "IDR bn", f"={{s:{fs}:cf_dnwc}}", "idr_bn", {"link": True}),
        ("row", "fcff", "Free cash flow to firm (FCFF, unlevered)", "IDR bn", "={t:nopat}+{t:da}+{t:capex}+{t:dnwc}", "idr_bn", {"bold": True}),
        ("blank",),
        ("section", "C. Discounting — only years after the valuation date"),
        ("row", "dcf_flag", "In DCF window (1 = year after the valuation date)", "flag", "={g:dcf_flag}", "flag", {"link": True}),
        ("row", "period", "Discount period (years from the valuation date)", "years", "={g:disc_period}", "num", {"link": True}),
        ("row", "df", "Discount factor = 1 / (1 + WACC)^period (0 before the valuation date)", "x", "={g:df}", "num4", {"link": True}),
        ("row", "fcff_dcf", "FCFF in the DCF window", "IDR bn", "={t:fcff}*{t:dcf_flag}", "idr_bn", {"total": True}),
        ("row", "pv", "Present value of FCFF", "IDR bn", "={t:fcff_dcf}*{t:df}", "idr_bn", {"total": True, "bold": True}),
        ("blank",),
        ("section", "D. Terminal value (Gordon growth on a normalised final-year cash flow)"),
        ("scalar", "tv_nopat", "NOPAT in the final forecast year", "IDR bn", "={t:nopat@2036}", "idr_bn", {}),
        ("scalar", "tv_da", "Depreciation in the final forecast year", "IDR bn", "={t:da@2036}", "idr_bn", {}),
        ("scalar", "tv_capex", "Normalised capex = factor x depreciation (v29 forecasts no capex after FY2028)", "IDR bn", "=-{t:tv_factor}*{t:tv_da}", "idr_bn", {}),
        ("scalar", "tv_nwc", "Normalised working-capital investment = g x final-year net working capital", "IDR bn", f"=-{{g:tg}}*({{s:{fs}:ar@2036}}-{{s:{fs}:ap@2036}})", "idr_bn", {}),
        ("scalar", "tv_fcff", "Normalised FCFF (final year)", "IDR bn", "={t:tv_nopat}+{t:tv_da}+{t:tv_capex}+{t:tv_nwc}", "idr_bn", {"bold": True}),
        ("scalar", "tv", "Terminal value at end-2036 = normalised FCFF x (1 + g) / (WACC - g)", "IDR bn", "={t:tv_fcff}*(1+{t:tg})/({t:wacc}-{t:tg})", "idr_bn", {}),
        ("scalar", "tv_pv", "Present value of the terminal value (discounted with the final-year factor)", "IDR bn", "={t:tv}*{t:df@2036}", "idr_bn", {"bold": True}),
        ("blank",),
        ("section", "E. Enterprise value at the valuation date"),
        ("scalar", "ev_explicit", "PV of FCFF FY2027-FY2036", "IDR bn", "=SUM({t:pv@all})", "idr_bn", {}),
        ("scalar", "ev_tv", "PV of terminal value", "IDR bn", "={t:tv_pv}", "idr_bn", {}),
        ("scalar", "ev", "ENTERPRISE VALUE (100%)", "IDR bn", "={t:ev_explicit}+{t:ev_tv}", "idr_bn", {"bold": True}),
        ("scalar", "ev_usd", "Enterprise value (USD m, valuation-year rate)", "USD m", "={t:ev}/{g:fx_val}*1000", "usd_m", {}),
        ("scalar", "tv_share", "Terminal value as % of enterprise value", "%", "=IF({t:ev}=0,0,{t:ev_tv}/{t:ev})", "pct", {}),
        ("blank",),
        ("section", "F. Equity value bridge at the valuation date (balances at 31-Dec-2026 are projections — FY2024-26 actuals not available)"),
        ("scalar", "b_ev", "Enterprise value", "IDR bn", "={t:ev}", "idr_bn", {}),
        ("scalar", "b_cash", "+ Cash at the valuation date (projected closing cash of the valuation year; includes the injection only if received on/before the valuation date)", "IDR bn",
         f"=INDEX({{s:{fs}:cash@all}},MATCH({{g:val_year}},{{g:year@all}},0))", "idr_bn", {}),
        ("scalar", "b_debt", "- Bank loans at the valuation date (LT loan outstanding unless repaid before the valuation date)", "IDR bn", "=-INDEX({s:fin:debt_close@all},MATCH({g:val_year},{g:year@all},0))", "idr_bn", {}),
        ("scalar", "b_other", "+/- Other assets less other liabilities (Dec-23 balances held flat) x switch (Global Inputs; default excluded)", "IDR bn",
         "=({g:open_other_assets}-{g:open_other_liab})*{g:other_bs_in_bridge}", "idr_bn", {}),
        ("scalar", "b_nci", "- Non-controlling interests: (1 - FSL interest) x value of each project line (NPLOG 35%)", "IDR bn", f"=-({nci_terms})", "idr_bn", {}),
        ("scalar", "eq", "EQUITY VALUE attributable to FSL shareholders (100% of shares)", "IDR bn", "={t:b_ev}+{t:b_cash}+{t:b_debt}+{t:b_other}+{t:b_nci}", "idr_bn", {"bold": True}),
        ("scalar", "eq_usd", "Equity value (USD m, valuation-year rate)", "USD m", "={t:eq}/{g:fx_val}*1000", "usd_m", {"bold": True}),
        ("text", "money_basis", "Pre-/post-money", '=IF({g:inj_date}<={g:val_date},"POST-money: injection received on/before the valuation date is inside cash","PRE-money: injection received after the valuation date (not in cash); LT loan still outstanding at the valuation date")', {"link": True}),
        ("scalar", "memo_req", "Memo: new equity funding requested (Funding Requirement — cash to be contributed; NOT a value)", "IDR bn", "={s:fund:total_request}", "idr_bn", {"link": True}),
        ("scalar", "memo_lt", "Memo: LT loan outstanding at the valuation date (Financing)", "IDR bn", "={s:fin:lt_at_val}", "idr_bn", {"link": True}),
        ("blank",),
        ("section", "G. Sensitivity of enterprise value (IDR bn) — WACC (rows) x terminal growth (columns)"),
        ("custom", lambda m, sk, r, ctx: _sens_grid(m, sk, r, ctx)),
    ] + [("blank",)] * 7 + [
        ("blank",),
        ("section", "H. Value by project line at the valuation date (project Output sheets: PV of FY2027+ FCFF incl. plain Gordon terminal value) x case flag"),
    ]
    for sp in specs:
        pid = sp["id"]
        rows.append(("scalar", f"pv.{pid}", f"{pid}  {sp['name']}", "IDR bn", f"={{xo:{pid}:r_npv}}*{{g:{flagkey}.{pid}}}", "idr_bn", {"link": True}))
    rows += [
        ("scalar", "pv_sum", "Sum of project line values", "IDR bn", "=" + "+".join(f"{{t:pv.{sp['id']}}}" for sp in specs), "idr_bn", {"bold": True}),
        ("scalar", "pv_tv_adj", "Terminal-value normalisation at company level (company TV uses normalised capex / working capital; project TVs use the plain FY2036 FCFF)", "IDR bn",
         "={t:ev}-{t:pv_sum}", "idr_bn", {}),
        ("scalar", "pv_check", "Check: sum of project PVs (explicit years) = company PV of explicit years", "IDR bn",
         "=" + "+".join(f"{{xo:{sp['id']}:r_npv_notv}}*{{g:{flagkey}.{sp['id']}}}" for sp in specs) + "-{t:ev_explicit}", "num4", {}),
    ]
    if case == "w":
        rows += [
            ("blank",),
            ("section", "I. Value of the BUMN operatorship schemes to FSL"),
            ("scalar", "bumn_ev", "Enterprise value With BUMN - Without BUMN", "IDR bn", "={t:ev}-{s:val_wo:ev}", "idr_bn", {"bold": True}),
            ("scalar", "bumn_eq", "Equity value With BUMN - Without BUMN", "IDR bn", "={t:eq}-{s:val_wo:eq}", "idr_bn", {"bold": True}),
            ("note", "Only FSL's entitlement under the schemes (tariff differential x volume, less FSL's operating cost) is valued; benefits retained by the BUMN partners are not included."),
        ]
    return rows


def _sens_grid(m, sk, r0, ctx):
    ws = m.ws(sk)
    ws.cell(r0, 2).value = "EV (IDR bn) — rows: WACC; columns: terminal growth"
    ws.cell(r0, 2).font = S.F_NOTE
    gs = [-0.01, -0.005, 0.0, 0.005, 0.01]
    ws_ = [-0.02, -0.01, 0.0, 0.01, 0.02]
    for j, dg in enumerate(gs):
        c = ws.cell(r0, 4 + j)
        c.value = m.resolve(f"={{t:tg}}+({dg})", 4 + j, ctx)
        c.number_format = S.NF["pct2"]
        c.font = S.F_HDR
        c.fill = S.FILL_HDR
        c.alignment = S.A_CENTER
    fc = m.rng(sk, "fcff_dcf", cur_sheet=sk)
    per = m.rng(sk, "period", cur_sheet=sk)
    flag = m.rng(sk, "dcf_flag", cur_sheet=sk)
    tvf = m.cell(sk, "tv_fcff", cur_sheet=sk)
    for i, dw in enumerate(ws_):
        rr = r0 + 1 + i
        c = ws.cell(rr, 3)
        c.value = m.resolve(f"={{t:wacc}}+({dw})", 3, ctx)
        c.number_format = S.NF["pct2"]
        c.font = S.F_BOLD
        c.fill = S.FILL_SUBSECTION
        c.alignment = S.A_CENTER
        for j, dg in enumerate(gs):
            cc = ws.cell(rr, 4 + j)
            w = f"$C{rr}"
            g = f"{L(4 + j)}${r0}"
            cc.value = (f"=SUMPRODUCT({fc},{flag},1/(1+{w})^{per})+({tvf}*(1+{g})/({w}-{g}))/(1+{w})^10")
            cc.number_format = S.NF["idr_bn"]
            cc.font = S.F_BODY
            cc.alignment = S.A_RIGHT
            if dw == 0 and dg == 0:
                cc.fill = S.FILL_KEY
                cc.font = S.F_BOLD
    ws.cell(r0 + 6, 2).value = "Terminal value discounted 10 years (FY2036 = 10th year after the valuation date). Centre cell = base case."
    ws.cell(r0 + 6, 2).font = S.F_NOTE


class ValuationPlan:
    def __init__(self, model: Model, specs):
        self.m = model
        self.specs = specs
        model.add_sheet("val_wo", T_VAL_WO, TAB)
        model.add_sheet("val_w", T_VAL_W, TAB)
        self.p_wo, _ = plan_layout(model, "val_wo", _rows(specs, "wo"))
        self.p_w, _ = plan_layout(model, "val_w", _rows(specs, "w"))

    def write(self):
        m = self.m
        for key, planned, title, sub in [
            ("val_wo", self.p_wo, "VALUATION — WITHOUT BUMN", "Company DCF at 31-Dec-2026 using FCFF from FY2027 (year-end convention), terminal value, enterprise value and equity bridge. Linked to 'FSL Financials — Without BUMN'. IDR bn."),
            ("val_w", self.p_w, "VALUATION — WITH BUMN", "Company DCF at 31-Dec-2026 using FCFF from FY2027 (year-end convention), terminal value, enterprise value and equity bridge. Linked to 'FSL Financials — With BUMN'. IDR bn."),
        ]:
            m.write_ts_header(key, title, sub)
            ctx = {"sheet": key, "pid": None}
            write_layout(m, key, planned, ctx)
            m.ws(key).column_dimensions["B"].width = 60
            m.set_print(key)
