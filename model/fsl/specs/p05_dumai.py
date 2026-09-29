"""P05 Dumai bagging & weighbridge — new project block.

v29: Calculation_FSL rows 168-218, Input rows 1257-1261, Output_Standalone (IDR) rows 66-87, flag Output_FSL!F30 (= 1).
Effective v29 logic (scenario Input!G4 = 1; every number below is the effective value in the v29 value dump):
  Operating flag : 1 from 2026 (Calculation_FSL!F170; row 170 = IF(year < 2026, 0, 1) x J$12)
  Volume         : typed in Calculation_FSL!L174:U174 (V174 = U174): 1,300,000 t 2026-28, 1,339,000 t 2029-32 (+3%), 1,379,170 t 2033-36 (+3%);
                   J174:K174 (2024-25) are blank -> nil revenue before commissioning. Weighbridge volume (row 182) = bagging volume (row 174).
  Bagging tariff : typed in Calculation_FSL!L175:V175: 35,000 IDR/t 2026-28, 36,400 2029-32 (+4%), 37,856 2033-36 (+4%)
  WB tariff      : Calculation_FSL!L183 = 2,000 IDR/t, M183:V183 = previous year (flat)
  Revenue        : bagging = volume x tariff / 1e9 x J$12 (row 176); WB = volume x tariff / 1e9 x J$12 (row 184); Net Sales = row 176 + row 184
  Cost of sales  : row 188 = (row 176 + row 184) x $F$188, and F188 is EMPTY -> cost of sales is nil in every year (exposed as an input = 0%)
  Opex           : insurance (row 210) = 6.80952 USD m (F208 = F192 = Input!J1258) x USD_IDR x 0.0021836245 (F209) x 1e6/1e9 x operating flag = 0.241851 IDR bn
                   operational cost (row 217) = bagging revenue x % (row 214, typed L214:V214: 47.49% .. 54.63%) + WB revenue x % (row 216, typed L216:V216: 19.2% .. 22.73%)
                   Output_Standalone row 72 = -(row 210 + row 217)
  Depreciation   : Output_Standalone row 75 = -row 191 = -(row 194 + row 199): building 60% (F193) of 6.80952 USD m over 20 yrs (E192) from 2026 (x row 170);
                   equipment 40% (F198) over 8 yrs (E197) x row 197, a life flag = 1 while 1 <= cumulative operating years <= 8, i.e. 2026-2033 only.
                   -> D&A 8.86055 IDR bn 2026-2033, 3.32271 IDR bn 2034-2036 (reproduced through the framework capex module plus an equipment life-end adjustment).
  Capex          : total 6.80952380952381 USD m (Input!M1259 = 6.5 + 0.30952380952381; Input!M1258 puts it all in FY2026);
                   Calculation_FSL row 1474 (the schedule the model actually uses) types 6.48452380952381 in FY2026 and 0.325 in FY2027.
  Financing cost : Output_Standalone row 78 = -Input!K386:W386 x $F$138 (stale references from the Cigading block) = 0 -> nothing (corporate in the revised model).

v29 source issues reproduced as effective behaviour (documented, not silently fixed):
  * Calculation_FSL!F188 (cost-of-sales %) is empty -> cost of sales nil.  Input cogs_pct = 0%.
  * The 2024-25 cells of the tariff / % rows point at unrelated Cigading input cells (J175 = Input!K261, J183 = Input!K268, J214 = Input!K286,
    J216 = Input!K288 = 0.659907 = Cigading 'Ops other expense' actual cost, ...). They only touch years with nil volume, so they have no effect;
    the effective values (0, and 0.659907 for the FY2024 WB cost %) are written into the inputs with notes.
  * Rows 201-205 (electricity = Wharf 2 cost/t row 379 x conveyor volume row 408 x Input!K280:W280 = 0) are nil and are NOT part of the
    standalone block (only the unused subtotal row 190 sums them) -> not modelled.
  * Row 192 J:V (IFERROR(row 191 / revenue)) is a memo ratio (D&A / revenue) that nothing uses -> not modelled.
Framework note / KNOWN LIMITATION (equipment life-end under depreciation method 1):
  Framework method 1 charges total capex x share / life from commissioning with no end (project.py dep_b / dep_e templates); v29 stops the
  equipment charge after its 8-year life (row 197 life flag x row 199). The calc row `dep_e_adj` (hooked as da_other) reverses the method-1
  equipment charge once cumulative operating years exceed the equipment life, so da_total and the P&L D&A line equal v29 (8.86055 IDR bn
  2026-2033, 3.32271 IDR bn 2034-2036). This is a workaround: `hooks.da_other` is defined by the framework as POSITIVE depreciation of
  non-capex assets, and the framework's fixed-asset roll-forward `nbv_new` (= previous + capex_idr - dep_new) and the Output line
  'Fixed assets — project capex at net book value' (bs_ppe) use dep_new, NOT da_total. Consequently under method 1 this block's NBV keeps
  falling by the 5.53785 IDR bn p.a. equipment charge in FY2034-36 while the P&L charges nil for equipment: P&L D&A and the NBV movement
  disagree by 5.54 IDR bn p.a. in those years and the equipment component of NBV goes below zero (capex ~110.757 IDR bn: correct end-2036
  NBV = building only, 66.454 - 11 x 3.32271 = ~29.90 IDR bn; framework method-1 NBV = ~13.29 IDR bn, i.e. understated by 3 x 5.53785 =
  ~16.61 IDR bn, equipment component ~ -16.61). Cash flow (FCFF) is unaffected because it adds back da_total, which is correct.
  Under method 2 the framework already ends each year's spend after its life, the adjustment is nil and NBV ties to the P&L.
  v29 itself has no NBV / balance-sheet row for this block (rows 191-199 are P&L depreciation only), so the harness comparison (rev, cogs,
  opex, da, ebit) is genuine; only the framework-generated balance-sheet line is affected.
  Requested framework fix (see framework_requests): method-1 dep_b / dep_e should multiply by a life flag (cumulative capflag years <= life)
  so the charge itself ends after the useful life, exactly as v29 row 197 does; once that lands, drop op_years / equip_life_flag / dep_e_adj
  from this spec and set hooks.da_other to None.
"""
from .helpers import Y, const, annual, scalar, row

REV, COS, OPX, DEP = "Revenue drivers", "Cost of sales drivers", "Operating expense drivers", "Depreciation"

CAPEX_TOTAL = 6.5 + 0.30952380952381            # Input!M1259 -> Input!J1258 = 6.80952380952381 USD m
CAPEX_2026, CAPEX_2027 = 6.48452380952381, 0.325  # Calculation_FSL!L1474, M1474 (typed)

VOLUME = {2024: 0, 2025: 0, 2026: 1300000, 2027: 1300000, 2028: 1300000, 2029: 1339000, 2030: 1339000, 2031: 1339000, 2032: 1339000,
          2033: 1379170, 2034: 1379170, 2035: 1379170, 2036: 1379170}
TARIFF_BAG = {2024: 0, 2025: 0, 2026: 35000, 2027: 35000, 2028: 35000, 2029: 36400, 2030: 36400, 2031: 36400, 2032: 36400,
              2033: 37856, 2034: 37856, 2035: 37856, 2036: 37856}
TARIFF_WB = {2024: 0, 2025: 0, **{y: 2000 for y in range(2026, 2037)}}
PCT_BAG = {2024: 0, 2025: 0, 2026: 0.4749039797217686, 2027: 0.4859138479296258, 2028: 0.49719896284267934, 2029: 0.48404241346923804,
           2030: 0.5041737390433625, 2031: 0.511270625206045, 2032: 0.5230944960193732, 2033: 0.5091882067107775, 2034: 0.5209821437523119,
           2035: 0.5413580792528154, 2036: 0.54629064932744}
PCT_WB = {2024: 0.659907061, 2025: 0, 2026: 0.192, 2027: 0.19612499999999997, 2028: 0.20035312499999997, 2029: 0.1995116049757281,
          2030: 0.20582439510012127, 2031: 0.2092450049776243, 2032: 0.21377613010206487, 2033: 0.212874304227783, 2034: 0.21749616183347756,
          2035: 0.22423356587931445, 2036: 0.2272894050262973}

inputs = [
    annual("volume", "Bagging volume (also the weighbridge volume)", "t", VOLUME,
           "Calculation_FSL!L174:U174 (typed; V174 = U174; J174:K174 blank = 0)", section=REV, fmt="tons",
           note="Typed in the calculation sheet, not on the Input sheet (F174 = Input!J267 is a stale Cigading reference = 0, unused). "
                "Steps +3% in FY2029 and FY2033. v29 row 182 sets the weighbridge volume equal to the bagging volume."),
    annual("tariff_bag", "Bagging tariff", "IDR/t", TARIFF_BAG,
           "Calculation_FSL!L175:V175 (typed); J175:K175 = Input!K261:L261 (empty Cigading cells = 0)", section=REV, fmt="idr_t",
           note="Steps +4% in FY2029 and FY2033. The 2024-25 cells reference unrelated empty Input cells; effective 0 with nil volume."),
    annual("tariff_wb", "Weighbridge tariff", "IDR/t", TARIFF_WB,
           "Calculation_FSL!L183 (typed 2,000; M183:V183 = previous year); J183:K183 = Input!K268:L268 (empty = 0)", section=REV, fmt="idr_t"),
    scalar("cogs_pct", "Cost of sales as % of total revenue", "%", 0.0, "Calculation_FSL!F188 (EMPTY cell -> 0%)", section=COS, fmt="pct2",
           note="v29 source issue: row 188 = (bagging + WB revenue) x $F$188 and F188 was never populated, so cost of sales is nil in every year. "
                "Kept at 0% as the effective v29 assumption."),
    scalar("ins_rate", "Insurance on new assets (% of total capex p.a.)", "%", 0.0021836245, "Calculation_FSL!F209 (applied to F208 = F192 = Input!J1258 = 6.80952 USD m x USD_IDR)",
           section=OPX, fmt="pct2", note="0.2184% x 110.757 IDR bn = 0.241851 IDR bn p.a. from FY2026 (x row 170 operating flag)."),
    annual("opcost_pct_bag", "Operational cost (excl. depreciation & insurance) as % of bagging revenue", "%", PCT_BAG,
           "Calculation_FSL!L214:V214 (typed); J214:K214 = Input!K286:L286 (empty Cigading cells = 0)", section=OPX, fmt="pct2",
           note="Typed year by year in v29 (47.5% FY2026 rising to 54.6% FY2036)."),
    annual("opcost_pct_wb", "Operational cost (excl. depreciation & insurance) as % of weighbridge revenue", "%", PCT_WB,
           "Calculation_FSL!L216:V216 (typed); J216 = Input!K288 (= 0.659907, Cigading 'Ops other expense' actual cost), K216 = Input!L288 (= 0)", section=OPX, fmt="pct2",
           note="v29 source issue: the FY2024 cell is a stale reference to a Cigading cost input (65.99%); harmless because WB revenue is nil before FY2026. "
                "Effective values kept (19.2% FY2026 rising to 22.7% FY2036)."),
]

calc = [
    row("volume", "Bagging volume = input x operating flag", "t", "={in:volume}*{c:opflag}", "Revenue", fmt="tons", total=True,
        note="Calculation_FSL row 174 (v29 leaves 2024-25 blank instead of applying row 170; identical values)"),
    row("tariff_bag", "Bagging tariff", "IDR/t", "={in:tariff_bag}", "Revenue", fmt="idr_t", note="Calculation_FSL row 175"),
    row("rev_bag", "Bagging revenue = volume x tariff / 1e9", "IDR bn", "={c:volume}*{c:tariff_bag}/10^9", "Revenue", fmt="idr_bn", total=True,
        note="Calculation_FSL row 176"),
    row("volume_wb", "Weighbridge volume = bagging volume", "t", "={c:volume}", "Revenue", fmt="tons", total=True, note="Calculation_FSL row 182 (= row 174)"),
    row("tariff_wb", "Weighbridge tariff", "IDR/t", "={in:tariff_wb}", "Revenue", fmt="idr_t", note="Calculation_FSL row 183"),
    row("rev_wb", "Weighbridge revenue = volume x tariff / 1e9", "IDR bn", "={c:volume_wb}*{c:tariff_wb}/10^9", "Revenue", fmt="idr_bn", total=True,
        note="Calculation_FSL row 184"),
    row("revenue", "Total revenue = bagging + weighbridge", "IDR bn", "={c:rev_bag}+{c:rev_wb}", "Revenue", fmt="idr_bn", total=True, bold=True,
        note="Output_Standalone (IDR) row 68 = Calculation_FSL row 176 + row 184"),
    row("cogs", "Cost of sales = total revenue x %", "IDR bn", "={c:revenue}*{in:cogs_pct}", "Cost of sales", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL row 188 (x empty $F$188 -> nil)"),
    row("insurance", "Insurance = total capex (IDR bn) x rate x operating flag", "IDR bn", "=SUM({c:capex_idr@all})*{in:ins_rate}*{c:opflag}", "Operating expenses",
        fmt="idr_bn", total=True, note="Calculation_FSL row 210"),
    row("opcost_bag", "Operational cost on bagging = bagging revenue x %", "IDR bn", "={c:rev_bag}*{in:opcost_pct_bag}", "Operating expenses", fmt="idr_bn", total=True,
        note="Calculation_FSL row 213 x row 214"),
    row("opcost_wb", "Operational cost on weighbridge = WB revenue x %", "IDR bn", "={c:rev_wb}*{in:opcost_pct_wb}", "Operating expenses", fmt="idr_bn", total=True,
        note="Calculation_FSL row 215 x row 216"),
    row("opcost", "Operational cost (excl. depreciation & insurance)", "IDR bn", "={c:opcost_bag}+{c:opcost_wb}", "Operating expenses", fmt="idr_bn", total=True,
        note="Calculation_FSL row 217"),
    row("opex", "Total operating expenses = insurance + operational cost", "IDR bn", "={c:insurance}+{c:opcost}", "Operating expenses", fmt="idr_bn", total=True, bold=True,
        note="Output_Standalone (IDR) row 72 = -(Calculation_FSL row 210 + row 217)"),
    row("op_years", "Cumulative operating years (v29 SUM($J$170:J170))", "years", "={c:opflag@cum}", DEP, fmt="int", note="Calculation_FSL row 197 argument"),
    row("equip_life_flag", "Equipment within its useful life (1 while 1 <= cumulative operating years <= equipment life)", "flag",
        "=IF(AND({c:op_years}>0,{c:op_years}<={in:life_e}),1,0)", DEP, fmt="flag", note="Calculation_FSL row 197 (= 1 in 2026-2033 only)"),
    row("dep_e_adj", "Adjustment: equipment depreciation ceases after its useful life (reverses the open-ended method-1 charge; nil under method 2)", "IDR bn",
        "=IF({g:dep_method}=1,-{c:dep_e}*(1-{c:equip_life_flag}),0)", DEP, fmt="idr_bn", total=True,
        note="v29 row 199 = equipment charge x row 197 life flag -> 5.53785 IDR bn 2026-2033, nil from 2034. Negative by construction: it is netted into da_total "
             "(P&L D&A correct). Workaround for a framework limitation: nbv_new / balance-sheet PPE subtract dep_new only, so under method 1 they do NOT reflect "
             "the equipment life-end (see module docstring). Remove once framework method 1 applies a life flag to dep_b/dep_e."),
]

SPEC = {
    "id": "P05",
    "code": "Dumai",
    "name": "Dumai bagging & weighbridge",
    "short": "Dumai",
    "entity": "FKS Sinar Lautan (FSL) — Dumai, Riau",
    "entity_short": "FSL Dumai",
    "category": "Planned project",
    "description": "Bagging and weighbridge services at Dumai from FY2026: a typed volume schedule (1.3 m t, stepping up 3% every four years) charged a bagging tariff (35,000 IDR/t, +4% every four years) and a weighbridge tariff (2,000 IDR/t); opex = insurance on the 6.81 USD m capex plus operational cost as a typed % of each revenue stream; cost of sales nil in v29.",
    "v29": {"calc": "Calculation_FSL rows 168-218", "input": "Input rows 1257-1261 (capex only; operating assumptions typed in Calculation_FSL)",
            "standalone": "Output_Standalone (IDR) rows 66-87", "flag": "Output_FSL!F30 (= 1)"},
    "v29_rows": {"rev": 68, "cogs": 69, "opex": 72, "da": 75, "ebit": 76, "fin": 78, "tax": 81, "np": 82},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": [],
    "commissioning": {"year": 2026, "source": "Calculation_FSL!F170", "cls": "v29", "note": "Bagging and weighbridge operating from FY2026 (row 170 flag)."},
    "capex": {
        "total_usd": CAPEX_TOTAL, "source": "Input!J1258 = SUM(K1258:W1258) = Input!M1259 (6.5 + 0.30952380952381 USD m, baseline row selected by Input!G1258 = 1)",
        "pct": {2026: CAPEX_2026 / CAPEX_TOTAL, 2027: CAPEX_2027 / CAPEX_TOTAL},
        "pct_source": "v29 timing: Calculation_FSL!L1474 = 6.48452380952381 (FY2026) and M1474 = 0.325 (FY2027), typed; Input!M1258 shows the full amount in FY2026",
        "building_share": 0.6, "building_source": "Calculation_FSL!F193 (equipment = F198 = 40%)",
        "life_b": 20, "life_e": 8, "lives_source": "Calculation_FSL!E192 (building 20 yrs) / E197 (equipment 8 yrs)",
        "hist_confirmed": 0,
        "note": "Percentages apply to total capex (95.2% FY2026, 4.8% FY2027 per Calculation_FSL row 1474). v29 depreciates the full amount from FY2026 (row 170) irrespective of the FY2027 spend. "
                "v29 ends the equipment charge after its 8-year life (row 197 life flag, FY2026-33 only); framework method 1 has no life-end, so the calc row dep_e_adj (hooked as da_other) "
                "reverses the equipment charge from FY2034 to make da_total / P&L D&A equal v29. KNOWN LIMITATION: under method 1 the framework's nbv_new and the Output line "
                "'Fixed assets — project capex at net book value' subtract dep_new (not da_total), so they keep charging 5.53785 IDR bn p.a. of equipment depreciation in FY2034-36 "
                "and do not reflect the equipment life-end (NBV understated by 5.54 IDR bn p.a. cumulatively from FY2034; equipment NBV goes negative). Under method 2 the adjustment is nil and NBV ties. "
                "Framework fix requested: method-1 dep_b/dep_e x life flag; then drop op_years/equip_life_flag/dep_e_adj and set da_other = None.",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": "dep_e_adj", "other_income": None},
}
