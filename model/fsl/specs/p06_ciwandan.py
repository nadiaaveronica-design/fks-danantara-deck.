"""P06 Ciwandan expansion — new project block.

v29: Calculation_FSL rows 508-546 (a copy of the revenue/cost structure sits in Calculation_SOEs rows 407-441 but the FSL
standalone block reads Calculation_FSL only), Input rows 482-527, Output_Standalone (IDR) rows 275-296, flag Output_FSL!F38 (= 1).
Effective v29 logic (scenario Input!G4 = 1 -> baseline rows, EXCEPT Input!G492 = 2 -> second ASP row):
  Operating flag : 1 from 2028 (Calculation_FSL!F510; row 510 = IF(year < 2028, 0, 1) x model flag J$12)
  Volume index   : 0 before 2028, 1 in 2028, then prior x (1 + Input!K485:W485) x flag   [Calculation_FSL row 513]
                   growth = 10% in 2027-2031 (effective from 2029) and 6% from 2032 -> 1.00, 1.10, 1.21, 1.331, 1.41086 ... 1.78118 in 2036
  Volume         : index x base 1,600,000 t (Calculation_FSL!F514 = Input!J490*0 + 1,600,000: the 1.9 m t in Input!J490 is
                   multiplied by 0 and overridden by a typed 1.6 m t)                     [row 514; "Total Volume" row 518 = row 514]
                   (Calculation_SOEs row 413 uses the 1.9 m t without the override — that copy is NOT what the FSL block uses)
  ASP            : Input!K492:W492 with selector Input!G492 = 2 -> row 494: 36,411.15 IDR/t typed in 2028 (O494), then grown by the
                   BASELINE tariff step-ups (row 496 = row 493 growth) lagged one year: x1.2 in 2029, x1.1 in 2031, x1.06 in 2033,
                   x1.06 in 2035 -> 36,411.1 / 43,693.4 / 43,693.4 / 48,062.7 / 48,062.7 / 50,946.5 / 50,946.5 / 54,003.3 / 54,003.3
                   [row 515]. The baseline row 493 (Wharf 2 tariff 40,944 ...) is NOT selected.
  Revenue        : volume x ASP / Billion                                                  [row 516 -> Output_Standalone row 277]
                   Row 512 ("Revenue Ciwandan Expansion", G512 = 52.0159%, N512:V512 = row 515 / $G$512) and row 517 (90,000/50,000 x
                   USD_IDR) are memo / scratch rows that read FROM the ASP row; nothing in the revenue chain uses G512 -> not modelled.
  Cost of sales  : "3. Other Cost of Sales" = proportion vs existing x sales, where the proportion (row 534) = Cigading existing
                   cost of sales excl. depreciation / Cigading existing revenue (Calculation_FSL J264 / J260, IFERROR -> 0), by year
                   (0.2585 in 2028 ... 0.2292 in 2036) [rows 534-536 -> row 522 -> Output_Standalone row 278]. Modelled as a LIVE link
                   to E2 ({x:E2:cogs} / {x:E2:revenue}), exactly as v29 links the rows. The brief's pointer to Calculation_SOEs rows
                   432-435 is the SOE-PoV copy (it divides SOEs rows 189/185 and gives different ratios); the FSL block does not use it.
                   Row 522 contains ONLY this other cost of sales; the depreciation rows 526/531 are summed separately in row 520, so
                   there is no double counting between the Cost of Sales and D&A lines of the standalone block.
  Opex           : proportion to revenue (row 540) = (Cigading existing operating cost excl. depreciation, row 340, + Cigading existing
                   G&A depreciation, row 347) / Cigading existing revenue (row 260), x revenue [rows 540-542 -> Output_Standalone row 281].
                   Modelled as ({x:E2:opex} + {x:E2:ga_dep}) / {x:E2:revenue} x revenue. Note that v29 thereby treats the existing
                   terminal's G&A depreciation as part of the opex RATIO applied to the expansion (kept as effective behaviour).
  Depreciation   : capex 5.02459 USD m (Input!M499:N499 = 2.51230 in FY2026 and FY2027 = INDEX baseline M500:N500 = (5 + Input!K1276
                   legal fee 2 IDR bn / USD_IDR / Million / 5 = 0.0246) / 2; Calculation_FSL row 1479 x Output_FSL!F38 = 1; F524 =
                   SUM(I1479:V1479)). Building 50% (Input!J504 -> F525) / 20 yrs (Input!J507 -> E524), equipment 50% (Input!J505) /
                   8 yrs (Input!J508), both x operating flag from 2028 and with NO end within the horizon (the 8-year equipment life
                   is not enforced in 2036): 2.04312 + 5.10781 = 7.15094 IDR bn p.a. [rows 526/531 -> row 520 -> Output_Standalone
                   row 284]. Framework method 1 reproduces this exactly (total capex x share / life x in-service flag).
  Unused inputs  : Input!K511:W511 (electricity consumption vs existing) and K517:W517 (R&M) = 0 and are not referenced by
                   Calculation_FSL rows 508-546; Input!K522 (insurance) blank; Input!K524:W524 (financing cost) = 0.
  Financing cost : none (Output_Standalone row 287 blank). Tax: 22% of positive EBT (framework).
  Ownership      : 100% FSL in v29 (econ_interest 1.0).
"""
from .helpers import Y, const, annual, scalar, row

REV, COS, OPX = "Revenue drivers", "Cost of sales drivers", "Operating expense drivers"

# ASP (Input!K492:W492, selector G492 = 2 -> Input row 494): typed 36,411.15 in 2028 (O494), then
# P494 = O494 x (1 + N496), Q494 = P494 x (1 + O496) ... i.e. the baseline row 493 step-ups (row 496) applied one year late.
BASELINE_ASP = {2026: 40944, 2027: 49132.80000000001, 2028: 49132.80000000001, 2029: 54046.08, 2030: 54046.08,
                2031: 57288.844800000006, 2032: 57288.844800000006, 2033: 60726.17548800001, 2034: 60726.17548800001,
                2035: 60726.17548800001, 2036: 60726.17548800001}
BASE_GROWTH = {y: BASELINE_ASP[y] / BASELINE_ASP[y - 1] - 1 for y in range(2027, 2037)}          # Input row 496 (N..W)
ASP = {y: 0.0 for y in Y}
ASP[2028] = 36411.14974239654                                                                       # Input!O494 (typed)
for y in range(2029, 2037):
    ASP[y] = ASP[y - 1] * (1 + BASE_GROWTH[y - 2])                                                  # Input!P494:W494

VOL_GROWTH = {2024: 0.0, 2025: 0.0, 2026: 0.0, 2027: 0.10, 2028: 0.10, 2029: 0.10, 2030: 0.10, 2031: 0.10,
              2032: 0.06, 2033: 0.06, 2034: 0.06, 2035: 0.06, 2036: 0.06}                          # Input!K485:W485

LEGAL_FEE_USD_M = 2 * 10**9 / 16265 / 10**6 / 5          # Input!K1276 = (2 IDR bn / USD_IDR / Million) / 5 = 0.0245927
CAPEX_TOTAL = 5 + LEGAL_FEE_USD_M                       # Input!M500 + N500 = 2 x (5 + K1276) / 2 = 5.02459 USD m

inputs = [
    scalar("vol_base", "Base volume in the first operating year (FY2028)", "t", 1600000,
           "Calculation_FSL!F514 (= Input!J490*0 + 1,600,000)", section=REV,
           note="v29 overrides the 1.9 m t in Input!J490 with a typed 1.6 m t (the Input value is multiplied by 0); the typed value is the effective assumption. Calculation_SOEs row 413 still uses 1.9 m t but is not read by the FSL standalone block."),
    annual("vol_growth", "Volume growth (applied from the second operating year)", "%", VOL_GROWTH,
           "Input!K485:W485 (INDEX of baseline row 486: 10% 2027-2031, 6% 2032-2036)", section=REV,
           note="Row 513 applies the growth of the year to the prior index from 2029 (index = 1 in 2028)."),
    annual("asp", "ASP (average selling price per ton)", "IDR/t", ASP,
           "Input!K492:W492 (selector Input!G492 = 2 -> row 494: O494 = 36,411.15 typed; P494:W494 = prior x (1 + row 496 baseline growth, lagged one year))", section=REV,
           note="Second ASP row selected (not the 40,944 baseline row 493). Step-ups x1.2 in 2029, x1.1 in 2031, x1.06 in 2033 and 2035 follow the baseline tariff steps one year late."),
]

calc = [
    row("vol_index", "Volume index (1.00 in the commissioning year, then x (1 + growth))", "index",
        "=IF({y}<{in:commissioning},0,IF({y}={in:commissioning},1,{c:vol_index@prev}*(1+{in:vol_growth})))*{flag}", "Revenue", f0="=0", fmt="idx",
        note="Calculation_FSL row 513"),
    row("volume", "Volume handled = base x index", "t", "={in:vol_base}*{c:vol_index}", "Revenue", fmt="tons", total=True,
        note="Calculation_FSL row 514 (= row 518 'Total Volume')"),
    row("asp", "ASP", "IDR/t", "={in:asp}", "Revenue", fmt="idr_t", note="Calculation_FSL row 515"),
    row("revenue", "Revenue = volume x ASP / 1e9", "IDR bn", "={c:volume}*{c:asp}/10^9", "Revenue", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL row 516 -> Output_Standalone (IDR) row 277"),
    # cost of sales = proportion vs the existing Cigading terminal x sales
    row("e2_revenue", "Cigading existing terminal — revenue (link)", "IDR bn", "={x:E2:revenue}", "Cost of sales", fmt="idr_bn", link=True,
        note="Calculation_FSL row 260"),
    row("e2_cogs", "Cigading existing terminal — cost of sales excl. depreciation (link)", "IDR bn", "={x:E2:cogs}", "Cost of sales", fmt="idr_bn", link=True,
        note="Calculation_FSL row 264 'Cost of Sales - Non Depre'"),
    row("cogs_ratio", "Cost of sales proportion vs existing = existing cost of sales / existing revenue", "%", "=IFERROR({c:e2_cogs}/{c:e2_revenue},0)", "Cost of sales", fmt="pct",
        note="Calculation_FSL row 534 (= IFERROR(J264/J260, 0)); 0.2585 in 2028 ... 0.2292 in 2036"),
    row("cogs", "Other cost of sales = proportion x revenue", "IDR bn", "={c:cogs_ratio}*{c:revenue}", "Cost of sales", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL rows 535-536 -> row 522 -> Output_Standalone (IDR) row 278 (depreciation is NOT in this line; it is in row 520)"),
    # opex = proportion to revenue of the existing Cigading terminal x revenue
    row("e2_opex", "Cigading existing terminal — operating cost excl. depreciation (link)", "IDR bn", "={x:E2:opex}", "Operating expenses", fmt="idr_bn", link=True,
        note="Calculation_FSL row 340 'Operating Cost - Non Depre'"),
    row("e2_ga_dep", "Cigading existing terminal — G&A depreciation (link; v29 adds it back into the opex ratio)", "IDR bn", "={x:E2:ga_dep}", "Operating expenses", fmt="idr_bn", link=True,
        note="Calculation_FSL row 347 'Depreciation - G&A (fixed)'"),
    row("opex_ratio", "Opex proportion to revenue = (existing operating cost + existing G&A depreciation) / existing revenue", "%",
        "=IFERROR(({c:e2_opex}+{c:e2_ga_dep})/{c:e2_revenue},0)", "Operating expenses", fmt="pct",
        note="Calculation_FSL row 540 (= IFERROR((J340+J347)/J260, 0)); 0.1732 in 2028 ... 0.1426 in 2036"),
    row("opex", "Operating expenses = proportion x revenue", "IDR bn", "={c:opex_ratio}*{c:revenue}", "Operating expenses", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL rows 541-542 -> Output_Standalone (IDR) row 281"),
]

SPEC = {
    "id": "P06",
    "code": "Ciwandan",
    "name": "Ciwandan Expansion",
    "short": "Ciwandan",
    "entity": "FSL Ciwandan expansion (Banten) — 100% FSL in v29",
    "entity_short": "FSL Ciwandan",
    "category": "Planned project",
    "description": "Expansion at Ciwandan from FY2028: 1.6 m t growing 10% p.a. (6% from 2032) at an ASP of 36,411 IDR/t stepping up with the Cigading tariff; cost of sales and opex are the existing Cigading terminal's cost-to-revenue ratios applied to the expansion revenue; depreciation of the 5.02 USD m capex (50% building / 20 yrs, 50% equipment / 8 yrs).",
    "v29": {"calc": "Calculation_FSL rows 508-546", "input": "Input rows 482-527",
            "standalone": "Output_Standalone (IDR) rows 275-296", "flag": "Output_FSL!F38 (= 1)"},
    "v29_rows": {"rev": 277, "cogs": 278, "opex": 281, "da": 284, "ebit": 285, "fin": 287, "tax": 290, "np": 291},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": ["E2"],
    "commissioning": {"year": 2028, "source": "Calculation_FSL!F510", "cls": "v29",
                      "note": "Ciwandan expansion operating (revenue, costs and depreciation) from FY2028; capex spent in FY2026-FY2027."},
    "capex": {
        "total_usd": CAPEX_TOTAL,
        "source": "Input!M499:N499 (= INDEX baseline Input!M500:N500 = (5 + Input!K1276 legal fee 0.0246) / 2 = 2.51230 each); Calculation_FSL row 1479 (x Output_FSL!F38 = 1); Calculation_FSL!F524 = SUM(I1479:V1479) = 5.02459",
        "pct": {2026: 0.5, 2027: 0.5}, "pct_source": "v29 timing: Input!M499 (FY2026) and N499 (FY2027), equal halves; Calculation_FSL row 1479",
        "building_share": 0.5, "building_source": "Input!J504 (-> Calculation_FSL!F525); equipment Input!J505 (-> F530) = 50%",
        "life_b": 20, "life_e": 8, "lives_source": "Input!J507 (building 20, -> Calculation_FSL!E524) / Input!J508 (equipment 8, -> E529)",
        "hist_confirmed": 0,
        "note": "Two equal spends (FY2026, FY2027) depreciated from the 2028 operating year: 5.02459 x 0.5 / 20 + 5.02459 x 0.5 / 8 USD m x USD_IDR = 2.04312 + 5.10781 = 7.15094 IDR bn p.a. (Calculation_FSL rows 526/531). v29 keeps charging the 8-year equipment depreciation in 2036 (no end within the horizon).",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": None},
}
