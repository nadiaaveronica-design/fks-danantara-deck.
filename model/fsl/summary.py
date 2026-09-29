"""Project Summary sheet: comparison table + one consistently formatted section per project (v29 Output_Standalone concept)."""
from . import styles as S
from .engine import Model, YEARS, YEAR_COL, FCOL, LCOL, L, SCALAR_COL, ROW_YEAR, DATA_ROW0
from .layout import plan_layout, write_layout

T_SUMMARY = "Project Summary"
TAB = "A9D08E"

LINES = [
    ("revenue", "Revenue", "xo", "revenue", "idr_bn", False),
    ("ebitda", "EBITDA", "xo", "ebitda", "idr_bn", False),
    ("ebit", "EBIT", "xo", "ebit", "idr_bn", True),
    ("nopat", "NOPAT (tax on project EBIT)", "xo", "nopat", "idr_bn", False),
    ("da", "Depreciation & amortisation", "xo", "da", "idr_bn", False),
    ("capex_usd", "Capex (USD m)", "xo", "bs_capex_usd", "usd_m", False),
    ("capex", "Capex (IDR bn)", "xo", "bs_capex", "idr_bn", False),
    ("dnwc", "Increase in net working capital", "xo", "f_dnwc", "idr_bn", False),
    ("fcff", "Free cash flow to firm", "xo", "fcff", "idr_bn", True),
    ("fcff_cum", "Cumulative FCFF", "xo", "fcff_cum", "idr_bn", False),
    ("noa", "Net operating assets funded by FSL (PPE + receivables - payables)", "xo", "bs_noa", "idr_bn", False),
    ("fund", "Funding need (cash shortfall to be funded by FSL)", "xo", "fund_need", "idr_bn", False),
    ("pv", "PV at the valuation date of FCFF incl. terminal value (years after 31-Dec-2026)", "xo", "pv", "idr_bn", False),
]


class SummaryPlan:
    def __init__(self, model: Model, specs):
        self.m = model
        self.specs = specs
        model.add_sheet("summary", T_SUMMARY, TAB)
        rows = [("section", "A. Comparison table — all projects (links to the project Output sheets; values in IDR bn unless stated)"), ("custom", self._table_header)]
        for sp in specs:
            rows.append(("custom", (lambda sp: (lambda m, sk, r, ctx: self._table_row(m, sk, r, ctx, sp)))(sp)))
        rows += [
            ("custom", self._table_total),
            ("blank",),
            ("section", "B. Bridge: sum of project outputs -> company statements (both cases; IDR bn)"),
            ("row", "sum_rev_wo", "Sum of project revenue x Without-BUMN flags", "IDR bn", "=" + "+".join(f"{{xo:{sp['id']}:revenue}}*{{g:flagwo.{sp['id']}}}" for sp in specs), "idr_bn", {}),
            ("row", "fs_rev_wo", "FSL Financials — Without BUMN revenue", "IDR bn", "={s:fs_wo:revenue}", "idr_bn", {"link": True}),
            ("row", "chk_rev_wo", "Difference", "IDR bn", "={t:sum_rev_wo}-{t:fs_rev_wo}", "num4", {}),
            ("row", "sum_rev_w", "Sum of project revenue x With-BUMN flags", "IDR bn", "=" + "+".join(f"{{xo:{sp['id']}:revenue}}*{{g:flagw.{sp['id']}}}" for sp in specs), "idr_bn", {}),
            ("row", "fs_rev_w", "FSL Financials — With BUMN revenue", "IDR bn", "={s:fs_w:revenue}", "idr_bn", {"link": True}),
            ("row", "chk_rev_w", "Difference", "IDR bn", "={t:sum_rev_w}-{t:fs_rev_w}", "num4", {}),
            ("row", "sum_fcff_w", "Sum of project FCFF x With-BUMN flags", "IDR bn", "=" + "+".join(f"{{xo:{sp['id']}:fcff}}*{{g:flagw.{sp['id']}}}" for sp in specs), "idr_bn", {}),
            ("row", "val_fcff_w", "Valuation — With BUMN FCFF", "IDR bn", "={s:val_w:fcff}", "idr_bn", {"link": True}),
            ("row", "chk_fcff_w", "Difference", "IDR bn", "={t:sum_fcff_w}-{t:val_fcff_w}", "num4", {}),
            ("note", "Company statements add corporate items (LT loan interest and its tax shield, dividends, injection, existing fixed assets, other balances) to the project sums; unlevered FCFF is identical by construction."),
            ("blank",),
        ]
        for sp in specs:
            pid = sp["id"]
            rows.append(("section", f"{pid}  {sp['name']}  —  {sp.get('category','')}  —  {sp.get('entity_short','')}"))
            rows.append(("custom", (lambda sp: (lambda m, sk, r, ctx: self._proj_links(m, sk, r, ctx, sp)))(sp)))
            for key, label, kind, okey, fmt, bold in LINES:
                rows.append(("row", f"{key}.{pid}", label, "USD m" if fmt == "usd_m" else "IDR bn", f"={{{kind}:{pid}:{okey}}}", fmt, {"link": True, "bold": bold, "total": key not in ("fcff_cum", "noa")}))
            rows.append(("custom", (lambda sp: (lambda m, sk, r, ctx: self._returns(m, sk, r, ctx, sp)))(sp)))
            rows.append(("blank",))
        self.planned, _ = plan_layout(model, "summary", rows)

    # ---- custom writers
    def _table_header(self, m, sk, r, ctx):
        ws = m.ws(sk)
        hdr = ["Project", "Category", "In val.", "Case", "FSL int.", "Start yr", "Capex USD m", "Capex post-val USD m", "Revenue 2027", "Revenue 2030", "EBITDA 2030", "NPV @ 31-Dec-26",
               "IRR full life", "Payback yr", "Input", "Calc", "Output"]
        for i, h in enumerate(hdr):
            c = ws.cell(r, 2 + i)
            c.value = h
            c.font = S.F_HDR
            c.fill = S.FILL_HDR
            c.alignment = S.Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.row_dimensions[r].height = 30

    def _table_row(self, m, sk, r, ctx, sp):
        ws = m.ws(sk)
        pid = sp["id"]
        ws.cell(r, 2).value = f"{pid}  {sp['name']}"
        ws.cell(r, 2).font = S.F_BODY
        ws.cell(r, 3).value = sp.get("category", "")
        ws.cell(r, 3).font = S.F_NOTE
        cells = [
            (4, f"={{g:incl.{pid}}}", "flag01"), (5, f"={{g:case.{pid}}}", "flag01"), (6, f"={{g:eint.{pid}}}", "pct0"),
            (7, (f"={{xin:{pid}:commissioning}}" if sp.get("commissioning") else '="existing"'), "year"),
            (8, (f"={{xin:{pid}:capex_total_usd}}" if sp.get("capex") else "=0"), "usd_m1"),
            (9, (f"={{xin:{pid}:capex_post_val}}" if sp.get("capex") else "=0"), "usd_m1"),
            (10, f"={{xo:{pid}:revenue@2027}}", "idr_bn"), (11, f"={{xo:{pid}:revenue@2030}}", "idr_bn"), (12, f"={{xo:{pid}:ebitda@2030}}", "idr_bn"),
            (13, f"={{xo:{pid}:r_npv}}", "idr_bn"), (14, f'=IF(ISNUMBER({{xo:{pid}:r_irr}}),{{xo:{pid}:r_irr}},"n/a")', "pct"),
            (15, f'=IF(ISNUMBER({{xo:{pid}:r_pb_year}}),{{xo:{pid}:r_pb_year}},"n/a")', "year"),
        ]
        for col, f, fmt in cells:
            c = ws.cell(r, col)
            c.value = m.resolve(f, col, ctx)
            c.number_format = S.NF[fmt]
            c.font = S.F_LINK
            c.alignment = S.A_RIGHT
        for col, k in [(16, "in"), (17, "calc"), (18, "out")]:
            c = ws.cell(r, col)
            c.value = "open"
            c.hyperlink = f"#'{m.title(f'{pid}:{k}')}'!A1"
            c.font = S.F_NAV
            c.alignment = S.A_CENTER

    def _table_total(self, m, sk, r, ctx):
        ws = m.ws(sk)
        ws.cell(r, 2).value = "Total (all projects listed, before case flags)"
        ws.cell(r, 2).font = S.F_BOLD
        first = r - len(self.specs)
        for col, fmt in [(8, "usd_m1"), (9, "usd_m1"), (10, "idr_bn"), (11, "idr_bn"), (12, "idr_bn"), (13, "idr_bn")]:
            c = ws.cell(r, col)
            c.value = f"=SUM({L(col)}{first}:{L(col)}{r-1})"
            c.number_format = S.NF[fmt]
            c.font = S.F_BOLD
            c.alignment = S.A_RIGHT
            c.border = S.B_TOTAL

    def _proj_links(self, m, sk, r, ctx, sp):
        ws = m.ws(sk)
        pid = sp["id"]
        ws.cell(r, 2).value = sp.get("description", "")
        ws.cell(r, 2).font = S.F_NOTE
        for col, k, label in [(3, "in", "Input"), (4, "calc", "Calc"), (5, "out", "Output")]:
            c = ws.cell(r, col)
            c.value = label
            c.hyperlink = f"#'{m.title(f'{pid}:{k}')}'!A1"
            c.font = S.F_NAV
            c.alignment = S.A_CENTER
        c = ws.cell(r, 7)
        c.value = m.resolve(f'="In valuation: "&{{g:incl.{pid}}}&"  |  case: "&{{g:case.{pid}}}&"  |  FSL interest: "&TEXT({{g:eint.{pid}}},"0%")', 7, ctx)
        c.font = S.F_NOTE

    def _returns(self, m, sk, r, ctx, sp):
        ws = m.ws(sk)
        pid = sp["id"]
        items = [("NPV @ 31-Dec-2026 (IDR bn)", f"={{xo:{pid}:r_npv}}", "idr_bn"), ("Full-life project IRR", f'=IF(ISNUMBER({{xo:{pid}:r_irr}}),{{xo:{pid}:r_irr}},"n/a")', "pct"),
                 ("IRR incl. terminal value", f'=IF(ISNUMBER({{xo:{pid}:r_irr_tv}}),{{xo:{pid}:r_irr_tv}},"n/a")', "pct"), ("Payback year", f'=IF(ISNUMBER({{xo:{pid}:r_pb_year}}),{{xo:{pid}:r_pb_year}},"n/a")', "year"),
                 ("Total capex (USD m)", f"={{xo:{pid}:r_capex_total}}", "usd_m1"), ("Capex after val. date (USD m)", f"={{xo:{pid}:r_capex_post}}", "usd_m1")]
        ws.cell(r, 2).value = "Returns:"
        ws.cell(r, 2).font = S.F_BOLD
        col = 3
        for label, f, fmt in items:
            c = ws.cell(r, col)
            c.value = label
            c.font = S.F_NOTE
            c.alignment = S.A_RIGHT
            c2 = ws.cell(r, col + 1)
            c2.value = m.resolve(f, col + 1, ctx)
            c2.number_format = S.NF[fmt]
            c2.font = S.F_LINK_B
            c2.alignment = S.A_RIGHT
            col += 2


def write_summary(model: Model, specs):
    plan = model._summary_plan if hasattr(model, "_summary_plan") else None
    raise RuntimeError("use SummaryPlan.write()")


def write(model: Model, plan: SummaryPlan):
    model.write_ts_header("summary", "PROJECT SUMMARY — project-by-project results (concept of v29 Output_Standalone)",
                          "Each section links to the project's Output sheet; the comparison table gives the headline numbers side by side. IDR bn unless stated.")
    ctx = {"sheet": "summary", "pid": None}
    write_layout(model, "summary", plan.planned, ctx)
    model.ws("summary").column_dimensions["B"].width = 58
    model.set_print("summary")
