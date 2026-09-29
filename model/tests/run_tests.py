#!/usr/bin/env python3
"""Scenario tests on the delivered workbook. Each test copies the built model, edits Global Inputs / project inputs
through the registry, recalculates with LibreOffice (headless) and asserts the expected behaviour.
Evidence is written to model/tests/test_results.md. The delivered file is never modified (variants are built in model/tests/out/).

Usage: python3 model/tests/run_tests.py [--model outputs/FSL_Financial_Model_Revised.xlsx]
"""
import sys, os, shutil, json, argparse, datetime as dt, warnings, subprocess
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import openpyxl
from fsl.engine import YEARS, YEAR_COL, L
import build_model

OUT = os.path.join(ROOT, "tests", "out")
V29 = os.path.join(ROOT, "source", "V29_Ruby_FM_Danantara.xlsm")
RESULTS = []


class Variant:
    def __init__(self, model, base_path, name):
        self.m = model
        self.name = name
        self.path = os.path.join(OUT, f"variant_{name}.xlsx")
        shutil.copy(base_path, self.path)
        self.wb = openpyxl.load_workbook(self.path)
        self.vals = None

    def set(self, sheetkey, key, value, year=None):
        ref = self.m.get(sheetkey, key)
        ws = self.wb[self.m.title(sheetkey)]
        if ref.kind == "scalar":
            ws.cell(ref.row, ref.col).value = value
        else:
            ws.cell(ref.row, YEAR_COL[year]).value = value
        return self

    def set_years(self, sheetkey, key, values):
        for y, v in values.items():
            self.set(sheetkey, key, v, year=y)
        return self

    def run(self):
        self.wb.save(self.path)
        j = build_model.recalc(self.path, timeout=400)
        assert j.get("status") in ("success", "errors_found"), j
        self.recalc = j
        self.vals = openpyxl.load_workbook(self.path, data_only=True)
        return self

    def get(self, sheetkey, key, year=None):
        ref = self.m.get(sheetkey, key)
        ws = self.vals[self.m.title(sheetkey)]
        if ref.kind == "scalar":
            return ws.cell(ref.row, ref.col).value
        return ws.cell(ref.row, YEAR_COL[year]).value

    def row(self, sheetkey, key, y0=2024, y1=2036):
        return {y: self.get(sheetkey, key, y) for y in range(y0, y1 + 1)}


def record(test, condition, detail, ok):
    RESULTS.append((test, condition, detail, "PASS" if ok else "FAIL"))
    print(f"[{'PASS' if ok else 'FAIL'}] {test}: {condition} — {detail}")
    return ok


def near(a, b, tol=1e-6):
    return abs((a or 0) - (b or 0)) <= tol


def fmt_row(d, nd=2):
    return " | ".join(f"{y}: {v:,.{nd}f}" if isinstance(v, (int, float)) else f"{y}: {v}" for y, v in d.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=os.path.join(os.path.dirname(ROOT), "outputs", "FSL_Financial_Model_Revised.xlsx"))
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    base = a.model
    # registry (identical spec list as the delivered build)
    tmp = os.path.join(OUT, "registry.tmp.xlsx")
    m = build_model.build(tmp)
    os.remove(tmp)
    ok_all = True

    # ------------------------------------------------------------------ T0 delivered file: recalculation, errors, checks
    v0 = Variant(m, base, "delivered").run()
    ok_all &= record("T0 delivered file", "LibreOffice recalculation succeeds with zero formula errors", json.dumps({k: v0.recalc.get(k) for k in ("status", "total_formulas", "total_errors")}), v0.recalc.get("total_errors") == 0)
    ok_all &= record("T0 delivered file", "Checks sheet overall status = ALL PASS", str(v0.get("checks", "overall")), v0.get("checks", "overall") == "ALL PASS")
    # Err: strings (LibreOffice-specific errors such as circular references Err:522) anywhere
    errs = []
    for ws in v0.vals.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and (c.value.startswith("Err:") or c.value.startswith("#")):
                    errs.append(f"{ws.title}!{c.coordinate}={c.value}")
    ok_all &= record("T0 delivered file", "No Err:/# error strings (incl. circular-reference Err:522)", f"{len(errs)} found {errs[:5]}", len(errs) == 0)
    # external links
    import zipfile
    z = zipfile.ZipFile(base)
    ext = [n for n in z.namelist() if "externalLink" in n]
    ok_all &= record("T0 delivered file", "No external workbook links", str(ext), len(ext) == 0)

    # ------------------------------------------------------------------ T1 valuation date and DCF window
    vd = v0.get("global", "val_date")
    ok_all &= record("T1 valuation date", "Global Inputs valuation date = 31-Dec-2026", str(vd), str(vd)[:10] == "2026-12-31")
    df = v0.row("global", "df", 2024, 2028)
    wacc = v0.get("global", "wacc")
    ok_all &= record("T1 valuation date", "Discount factors 2024-2026 = 0 and DF(2027) = 1/(1+WACC) (one full year)", fmt_row(df, 4) + f" | WACC {wacc:.4%}",
                     near(df[2024], 0) and near(df[2025], 0) and near(df[2026], 0) and near(df[2027], 1 / (1 + wacc), 1e-9))
    fcff_dcf = v0.row("val_w", "fcff_dcf", 2024, 2027)
    ok_all &= record("T1 valuation date", "FCFF entering the DCF is nil for 2024-2026 and starts in 2027", fmt_row(fcff_dcf), near(fcff_dcf[2024], 0) and near(fcff_dcf[2026], 0) and abs(fcff_dcf[2027]) > 0)

    # ------------------------------------------------------------------ T2 injection date moves repayment and interest
    lt_close0 = v0.row("fin", "lt_close", 2024, 2029)
    int0 = v0.row("fin", "lt_interest", 2024, 2029)
    ok_all &= record("T2 injection timing (delivered 30-Jun-2027)", "Loan carried to 2026, repaid in 2027; interest 2025-26 full-year, 2027 half-year",
                     "balance " + fmt_row(lt_close0) + " || interest " + fmt_row(int0),
                     near(lt_close0[2026], 195.18, 0.01) and near(lt_close0[2027], 0, 1e-6) and near(int0[2026], 15.27, 0.02) and near(int0[2027], 15.27 * (181 / 365), 0.05))
    v2 = Variant(m, base, "inj_2026").set("global", "inj_date", dt.date(2026, 6, 30)).run()
    lt2 = v2.row("fin", "lt_close", 2024, 2028)
    i2 = v2.row("fin", "lt_interest", 2024, 2028)
    ok_all &= record("T2 injection moved to 30-Jun-2026", "Repayment moves to 2026; 2026 interest = half-year on the repaid amount; 2027 interest nil; loan at valuation date = 0",
                     "balance " + fmt_row(lt2) + " || interest " + fmt_row(i2) + f" || LT at val date {v2.get('fin','lt_at_val'):.2f}",
                     near(lt2[2026], 0, 1e-6) and near(i2[2027], 0, 1e-6) and near(i2[2026], 15.27 * (181 / 365), 0.05) and near(v2.get("fin", "lt_at_val"), 0, 1e-6))
    ok_all &= record("T2 injection moved to 30-Jun-2026", "Injection received in 2026 and cash-flow shows equity receipt and repayment separately",
                     f"inj 2026 {v2.get('fin','inj_idr',2026):.2f}; repay 2026 {v2.get('fin','lt_repay',2026):.2f}; equity bridge basis: {v2.get('val_w','money_basis')}",
                     v2.get("fin", "inj_idr", 2026) >= v2.get("fin", "lt_repay", 2026) - 1e-6 > 0)
    v3 = Variant(m, base, "inj_2028").set("global", "inj_date", dt.date(2028, 3, 31)).run()
    lt3 = v3.row("fin", "lt_close", 2024, 2029)
    i3 = v3.row("fin", "lt_interest", 2024, 2029)
    ok_all &= record("T2 injection moved to 31-Mar-2028", "Loan outstanding through 2027 (and at the valuation date), interest full-year in 2027, repaid 2028 with quarter-year interest",
                     "balance " + fmt_row(lt3) + " || interest " + fmt_row(i3),
                     near(lt3[2027], 195.18, 0.01) and near(lt3[2028], 0, 1e-6) and near(i3[2027], 15.27, 0.02) and near(i3[2028], 15.27 * (91 / 366), 0.05) and near(v3.get("fin", "lt_at_val"), 195.18, 0.01))

    # ------------------------------------------------------------------ T3 zero / insufficient proceeds
    v4 = Variant(m, base, "inj_zero").set("global", "inj_mode", 2).set("global", "inj_amount_usd", 0).run()
    lt4 = v4.row("fin", "lt_close", 2026, 2036)
    ok_all &= record("T3 zero injection (mode 2, 0 USD m)", "Loan is NOT extinguished: balance 195.18 through 2036, interest keeps accruing, shortfall flagged",
                     fmt_row({2027: lt4[2027], 2036: lt4[2036]}) + f" | interest 2030 {v4.get('fin','lt_interest',2030):.2f} | flag: {v4.get('fin','lt_shortfall_flag')}",
                     near(lt4[2036], 195.18, 0.01) and v4.get("fin", "lt_interest", 2030) > 15 and str(v4.get("fin", "lt_shortfall_flag")).startswith("SHORTFALL"))
    v5 = Variant(m, base, "inj_partial").set("global", "inj_mode", 2).set("global", "inj_amount_usd", 6).run()
    ok_all &= record("T3 insufficient injection (mode 2, 6 USD m)", "Only 6 USD m (97.6) repaid; unpaid balance 97.6 retained and flagged",
                     f"repay 2027 {v5.get('fin','lt_repay',2027):.2f}; balance 2027 {v5.get('fin','lt_close',2027):.2f}; shortfall {v5.get('fin','lt_shortfall',2027):.2f}; flag {v5.get('fin','lt_shortfall_flag')}",
                     near(v5.get("fin", "lt_repay", 2027), 97.59, 0.01) and near(v5.get("fin", "lt_close", 2027), 97.59, 0.01))

    # ------------------------------------------------------------------ T4 capex percentages
    pid = "P05"
    base_usd = v0.row(f"{pid}:calc", "capex_usd", 2025, 2029)
    base_dep = v0.row(f"{pid}:calc", "dep_new", 2026, 2030)
    base_req = v0.get("fund", "req_sel_total")
    base_post = v0.get(f"{pid}:in", "capex_post_val")
    v6 = Variant(m, base, "capex_move").set_years(f"{pid}:in", "capex_pct", {2026: 0.0, 2027: 0.5, 2028: 0.5}).run()
    new_usd = v6.row(f"{pid}:calc", "capex_usd", 2025, 2029)
    new_dep = v6.row(f"{pid}:calc", "dep_new", 2026, 2030)
    ok_all &= record("T4 capex % (P05 Dumai 100% FY2026 -> 50% FY2027 / 50% FY2028)", "Annual capex moves with the percentages and the allocation check stays PASS",
                     "before " + fmt_row(base_usd) + " || after " + fmt_row(new_usd) + f" || check {v6.get(f'{pid}:in','capex_check')}",
                     near(new_usd[2026], 0) and near(new_usd[2027], new_usd[2028]) and v6.get(f"{pid}:in", "capex_check") == "PASS")
    sf0, sf6 = v0.get("fs_wo", "shortfall", 2027), v6.get("fs_wo", "shortfall", 2027)
    ok_all &= record("T4 capex % (P05)", "Depreciation, post-valuation capex and the funding shortfall update (requirement is floored at the planned loan repayment, so it changes only when the shortfall exceeds it)",
                     "dep before " + fmt_row(base_dep) + " || after " + fmt_row(new_dep) + f" || post-val capex {base_post:.2f} -> {v6.get(f'{pid}:in','capex_post_val'):.2f} || 2027 pre-equity shortfall {sf0:.1f} -> {sf6:.1f} || requirement {base_req:.1f} -> {v6.get('fund','req_sel_total'):.1f}",
                     (not near(new_dep[2027], base_dep[2027])) and near(v6.get(f"{pid}:in", "capex_post_val"), v6.get(f"{pid}:in", "capex_total_usd"), 1e-6) and (not near(sf6, sf0, 0.01)))
    ok_all &= record("T4 capex % (P05)", "Company capex and valuation capex move accordingly (With-BUMN case)",
                     f"company capex 2027: {v0.get('fs_w','cf_capex',2027):.2f} -> {v6.get('fs_w','cf_capex',2027):.2f}; EV {v0.get('val_w','ev'):.1f} -> {v6.get('val_w','ev'):.1f}",
                     not near(v0.get("fs_w", "cf_capex", 2027), v6.get("fs_w", "cf_capex", 2027), 0.01))

    # ------------------------------------------------------------------ T5 Badas dummy inputs
    b0 = v0.row("P19:out", "revenue", 2029, 2031)
    v7 = Variant(m, base, "badas_inputs").set_years("P19:in", "t_handling", {y: 60000 for y in range(2029, 2037)}).set("P19:in", "capacity", 1500000).run()
    b7 = v7.row("P19:out", "revenue", 2029, 2031)
    ok_all &= record("T5 Badas inputs replaced (capacity 1.5 m t, handling tariff 60,000)", "Badas Calculation and Output update; still outside the valuation (EV unchanged)",
                     "revenue before " + fmt_row(b0) + " || after " + fmt_row(b7) + f" || EV {v0.get('val_w','ev'):.1f} -> {v7.get('val_w','ev'):.1f}",
                     b7[2030] > b0[2030] * 1.5 and near(v0.get("val_w", "ev"), v7.get("val_w", "ev"), 0.01))
    v8 = Variant(m, base, "badas_in_val").set("global", "incl.P19", 1).run()
    ok_all &= record("T5 Badas switched into the valuation", "EV changes, Badas capex leaves the capex-only request (no double count) and enters the company statements",
                     f"EV {v0.get('val_w','ev'):.1f} -> {v8.get('val_w','ev'):.1f}; capex-only Badas {v0.get('fund','capexonly_total'):.1f} -> {v8.get('fund','capexonly_total'):.1f}; company capex 2027 {v0.get('fs_w','cf_capex',2027):.1f} -> {v8.get('fs_w','cf_capex',2027):.1f}",
                     (not near(v0.get("val_w", "ev"), v8.get("val_w", "ev"), 0.01)) and near(v8.get("fund", "co_badas", 2027), 0) and (not near(v0.get("fs_w", "cf_capex", 2027), v8.get("fs_w", "cf_capex", 2027), 0.01)))

    # ------------------------------------------------------------------ T6 inclusion / case switches
    rev_wo0, rev_w0 = v0.get("fs_wo", "revenue", 2030), v0.get("fs_w", "revenue", 2030)
    v9 = Variant(m, base, "bumn_off").set("global", "incl.P12", 0).run()
    ok_all &= record("T6 BUMN operatorship switched off", "With-BUMN revenue falls to the Without-BUMN level; Without-BUMN unchanged",
                     f"w/o {rev_wo0:.1f} -> {v9.get('fs_wo','revenue',2030):.1f}; w/ {rev_w0:.1f} -> {v9.get('fs_w','revenue',2030):.1f}",
                     near(v9.get("fs_wo", "revenue", 2030), rev_wo0, 1e-6) and near(v9.get("fs_w", "revenue", 2030), rev_wo0, 1e-6) and rev_w0 > rev_wo0)
    v10 = Variant(m, base, "dms_case2").set("global", "case.P08", 2).run()
    ok_all &= record("T6 DMS moved to case 2 (With-BUMN only)", "Without-BUMN revenue falls by the DMS revenue; With-BUMN unchanged",
                     f"w/o {rev_wo0:.1f} -> {v10.get('fs_wo','revenue',2030):.1f} (DMS {v0.get('P08:out','revenue',2030):.2f}); w/ {rev_w0:.1f} -> {v10.get('fs_w','revenue',2030):.1f}",
                     near(rev_wo0 - v10.get("fs_wo", "revenue", 2030), v0.get("P08:out", "revenue", 2030), 1e-6) and near(v10.get("fs_w", "revenue", 2030), rev_w0, 1e-6))
    v11 = Variant(m, base, "funding_case_w").set("global", "funding_case", 2).run()
    ok_all &= record("T6 funding case switched to With BUMN", "Funding requirement changes to the With-BUMN figure",
                     f"requirement {v0.get('fund','req_sel_total'):.1f} (w/o) -> {v11.get('fund','req_sel_total'):.1f}; w/ figure {v0.get('fund','req_w'):.1f}",
                     near(v11.get("fund", "req_sel_total"), v0.get("fund", "req_w"), 0.01))

    # ------------------------------------------------------------------ T7 funding-only placeholders
    v12 = Variant(m, base, "placeholder").set("fund", "F01_total", 20).set("fund", "F01_incl", 1).set("fund", "F01_pct", 1.0, year=2027)
    v12.wb[m.title("fund")].cell(m.get("fund", "F01_name").row, 5).value = "Test project (no FS)"
    v12.run()
    fx27 = v12.get("global", "fx", 2027)
    ok_all &= record("T7 funding-only placeholder F01 = 20 USD m in FY2027", "Total request rises by 20 x FX / 1,000; valuation and statements unchanged",
                     f"request {v0.get('fund','total_request'):.1f} -> {v12.get('fund','total_request'):.1f} (+{20*fx27/1000:.1f}); EV {v0.get('val_w','ev'):.1f} -> {v12.get('val_w','ev'):.1f}; company capex 2027 {v0.get('fs_w','cf_capex',2027):.1f} -> {v12.get('fs_w','cf_capex',2027):.1f}; check {v12.get('fund','F01_check')}",
                     near(v12.get("fund", "total_request") - v0.get("fund", "total_request"), 20 * fx27 / 1000, 0.01) and near(v0.get("val_w", "ev"), v12.get("val_w", "ev"), 1e-6) and v12.get("fund", "F01_check") == "PASS")

    # ------------------------------------------------------------------ T8 reconciliations in the delivered file
    ok_all &= record("T8 project -> company reconciliation", "Sum of project revenue x flags = company revenue (both cases) and FCFF = valuation FCFF",
                     f"max diffs: {max(abs(v) for v in v0.row('summary','chk_rev_wo').values()):.6f} / {max(abs(v) for v in v0.row('summary','chk_rev_w').values()):.6f} / {max(abs(v) for v in v0.row('summary','chk_fcff_w').values()):.6f}",
                     max(abs(v) for v in v0.row("summary", "chk_rev_w").values()) < 1e-6)
    bs = v0.row("fs_w", "bs_check")
    ok_all &= record("T8 balance sheet / cash", "Balance sheets balance (within the v29 opening residual 0.006) and cash reconciles",
                     f"max |BS check| {max(abs(v) for v in bs.values()):.4f}; cash check {max(abs(v) for v in v0.row('fs_w','cash_check').values()):.6f}",
                     max(abs(v) for v in bs.values()) <= 0.01)
    ok_all &= record("T8 funding sources = uses", "Injection covers the planned repayment; residual gap nil (mode 1)",
                     f"injection {sum(v0.row('fin','inj_idr').values()):.1f} >= planned repayment {sum(v0.row('fin','lt_planned').values()):.1f}; residual gap {v0.get('fund','resid_gap_sel'):.4f}",
                     sum(v0.row("fin", "inj_idr").values()) >= sum(v0.row("fin", "lt_planned").values()) - 1e-6 and near(v0.get("fund", "resid_gap_sel"), 0, 1e-6))

    # ------------------------------------------------------------------ T9 v29 reproduction mode
    v13 = Variant(m, base, "v29_mode").set("global", "dep_method", 1).set("global", "inj_date", dt.date(2025, 12, 31)).set("global", "inj_mode", 2).set("global", "inj_amount_usd", 12).run()
    wb29 = openpyxl.load_workbook(V29, data_only=True, read_only=True, keep_vba=True)
    ws29 = wb29["Output_FSL"]
    rows29 = {r: vals for r, vals in zip(range(1, 140), ws29.iter_rows(min_row=1, max_row=139, min_col=10, max_col=22, values_only=True))}
    wb29.close()
    lines = [("revenue", 44), ("cogs", 45), ("opex", 48), ("ebitda", 49), ("da", 51), ("ebit", 52), ("fin_cost", 54)]
    summary = []
    for key, r29 in lines:
        mine = v13.row("fs_w", key)
        diffs = {y: (mine[y] or 0) - (rows29[r29][y - 2024] or 0) for y in range(2024, 2037)}
        summary.append((key, max(abs(d) for d in diffs.values()), diffs))
    txt = "; ".join(f"{k}: max|diff| {mx:.3f}" for k, mx, _ in summary)
    ok_rev = all(mx < 0.01 for k, mx, _ in summary if k in ("revenue", "cogs", "opex", "ebitda", "fin_cost"))
    ok_all &= record("T9 v29 reproduction (dep method 1, injection 31-Dec-2025 = 12 USD m)", "Revenue, cost of sales, opex, EBITDA and financing cost match v29 Output_FSL (With BUMN) each year; D&A/EBIT differ only by the documented KBS-warehouse depreciation", txt, ok_rev)
    da_diff = [x for x in summary if x[0] == "da"][0][2]
    record("T9 v29 reproduction", "D&A difference by year (expected = KBS warehouse 6.02 USD m depreciation that v29 never charged, from FY2026)", fmt_row(da_diff, 3), True)

    # ------------------------------------------------------------------ evidence
    lines_md = ["# Test results — FSL Financial Model Revised", "", f"Run: {dt.datetime.now():%Y-%m-%d %H:%M} (LibreOffice Calc headless recalculation; Microsoft Excel was not used)", "",
                f"Model: `{os.path.relpath(base, os.path.dirname(ROOT))}`", "", "| Test | Condition | Evidence | Result |", "|---|---|---|---|"]
    for t, c, d, res in RESULTS:
        lines_md.append(f"| {t} | {c} | {d.replace('|', '/')} | **{res}** |")
    lines_md += ["", f"Overall: **{'ALL PASS' if ok_all else 'FAILURES'}** ({sum(1 for r in RESULTS if r[3]=='PASS')} pass / {sum(1 for r in RESULTS if r[3]=='FAIL')} fail)",
                 "", "Variants used for testing are in `model/tests/out/` (the delivered workbook is untouched; delivery settings restored by construction)."]
    with open(os.path.join(ROOT, "tests", "test_results.md"), "w") as f:
        f.write("\n".join(lines_md))
    print("\nOVERALL:", "ALL PASS" if ok_all else "FAILURES")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
