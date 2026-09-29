"""E3 Belawan (incl. Belawan expansion, SGT3) — existing business block with a new-asset capex module.

v29: Calculation_FSL rows 580-695, Input rows 529-693, Output_Standalone (IDR) rows 321-342, flag Output_FSL!F37 (= 1).
Effective v29 logic (scenario Input!G4 = 1 -> baseline rows):
  Volume (existing) : index (1 in 2023) x (1 + Input!K532:W532: 0% FY2024, 3% after) x base Input!J537 = 750,000 t
                      (Input!L537 = 922,782 t is the second, unselected column)                           [Calculation_FSL rows 585-586]
  Additional volume : Calculation_FSL!J587:V587 = Calculation_SOEs!J450:V450 — typed 200,000 t in FY2027 rising by 50,000 t p.a. to
                      550,000 t in FY2034; FY2035-36 are EMPTY cells (v29 source gap -> 0), not multiplied by any flag      [row 587]
  Tariff            : Input!K539:W539 (29,658 FY2024-25; 43,947.5 FY2026-27; then +3% p.a.)                                 [row 588]
  Revenue           : (existing + additional volume) x tariff / 1e9                                                          [row 589]
  Cost of sales (row 593 = sum of rows 614, 619, 625, 631, 637, 643, 649, 655, 660, 666, 672); per-ton lines use the FY2023
  volume 922,782 t (Calculation_FSL!E623) and the TOTAL volume incl. additional (row 591):
    employee 3.279620518 fixed (3.5%), security 1.930177428 fixed (3.5%), fuel 0.82569621188/t (3%), utilities 0.631021441/t (3%),
    concession fee = revenue x Input!K591:W591 = 2.5% (Input!J596 = 0.5514 IDR bn is the FY2023 actual concession fee, ~2.5% of
    FY2023 revenue 22.24 bn; it sits in Calculation_FSL!F636 under the label "% to Revenue" and, with index row 634, is NOT used
    by row 637), ops other 0.41230965056/t (3%), R&M 0.28658186344/t (3%), overtime 0.245423178/t (3.5%),
    insurance on existing assets = rate x existing depreciation (rate typed 1.0919279% in Calculation_FSL!J658:L658 for FY2024-26,
    then Input!N619:W619 = 0.2%), insurance on new assets = 14.0246 USD m x USD_IDR x Input!K619:W619 (0, 0, 0.2% from FY2026),
    labour 0.0116/t (3.5%)
  Depreciation (row 609 = 597 + 602 + 607):
    existing assets Input!K546:W546 (5.23397, 5.23397, 2.61699, then 0) + "Addition" Input!K437:W437 (EMPTY cells inside the Cigading
    conveyor input block -> 0; v29 source issue, the base cell F595 = Input!J442 is also empty and unused)
    new assets 14.024592683676605 USD m (Input!M551 = 7 + Input!K1276 legal-fee share 0.0246; Input!N551 = 7.0; F600 = SUM(Input!K551:O551))
    building 90% / 20 yrs (Input!J556, J559), equipment 10% / 8 yrs (Input!J557, J560), from FY2026: rows 602/607 multiply by
    Calculation_FSL row 582 (Belawan operation period 2026) AND row 357 (Cigading Wharf 2 operation period, 1 from 2025) — effective start 2026
  Opex (row 686 = sum 687-695): nine fixed G&A lines Input!J637:J645 grown at Input rows 649, 654, 659, 665, 670, 675, 680, 685, 690
  Financing cost    : none (Output_Standalone row 333 blank)
v29 source issues reproduced as effective behaviour: (1) additional volume blank in FY2035-36; (2) "Addition" depreciation references
empty Input!K437:W437; (3) concession fee: row 637 applies Input!K591:W591 (2.5%) directly to revenue; Calculation_FSL!F636 holds the FY2023 actual fee
0.5514 IDR bn (Input!J596) under a "% to Revenue" label and the index row 634 is computed but unused — a labelling quirk only, the
2.5% x revenue logic is consistent with the FY2023 actual;
(4) new-asset depreciation flag also references the Wharf 2 operating period (no effect on values).
"""
from .helpers import Y, const, annual, scalar, row, growth_index, fixed_cost, per_ton_cost, sum_rows

REV, COS, OPX, DEP = "Revenue drivers", "Cost of sales drivers", "Operating expenses (G&A)", "Depreciation"
BASE_VOL = 922782                     # Calculation_FSL!E623 (FY2023 throughput used for cost per ton)
CAPEX_2026 = 7.024592683676606        # Input!M551 = 7 + Input!K1276 (legal-fee allocation 2 IDR bn / USD_IDR / 5)
CAPEX_2027 = 7.0                      # Input!N551
CAPEX_TOTAL = CAPEX_2026 + CAPEX_2027 # Calculation_FSL!F600 = SUM(Input!K551:O551) = 14.0246 USD m

TARIFF = {2024: 29658, 2025: 29658, 2026: 43947.5, 2027: 43947.5, 2028: 45265.925, 2029: 46623.90275, 2030: 48022.6198325,
          2031: 49463.298427475, 2032: 50947.19737979925, 2033: 52475.61330119323, 2034: 54049.98170022902,
          2035: 55671.48115123589, 2036: 57341.62558577297}
ADD_VOL = {2024: 0, 2025: 0, 2026: 0, 2027: 200000, 2028: 250000, 2029: 300000, 2030: 350000, 2031: 400000, 2032: 450000,
           2033: 500000, 2034: 550000, 2035: 0, 2036: 0}
DEP_EXIST = {2024: 5.233974213430001, 2025: 5.233974213430001, 2026: 2.6169871067150003, **{y: 0 for y in range(2027, 2037)}}
INS_RATE_EXIST = {y: (0.010919279054404601 if y <= 2026 else 0.002) for y in Y}
INS_RATE_NEW = {y: (0.0 if y <= 2025 else 0.002) for y in Y}

opex_lines = [
    # key, label, base 2023 (Input!J637..J645), growth, growth source row
    ("ga_legal", "Legal and professional fees", 1.702367004, 0.03, 649),
    ("ga_office", "Office expenses", 0.25867063399, 0.02, 654),
    ("ga_travel", "Travelling and entertainment", 0.23960182307999997, 0.03, 659),
    ("ga_donation", "Donation & CSR", 0.17580518881999999, 0.03, 665),
    ("ga_rental", "Rental expenses — G&A", 0.147776114, 0.02, 670),
    ("ga_comm", "Communication expenses — G&A", 0.146392455, 0.02, 675),
    ("ga_staff", "Staff costs — G&A", 0.140993213, 0.035, 680),
    ("ga_security", "Security services / outsourcing", 0.13922671138, 0.03, 685),
    ("ga_audit", "Audit fees", 0.036134992, 0.03, 690),
]
BASE_ROW = {"ga_legal": 637, "ga_office": 638, "ga_travel": 639, "ga_donation": 640, "ga_rental": 641, "ga_comm": 642,
            "ga_staff": 643, "ga_security": 644, "ga_audit": 645}

inputs = [
    # revenue
    scalar("vol_base", "Base volume FY2023 — existing terminal", "t", 750000, "Input!J537 (= Input!K537; Calculation_FSL!F586)", section=REV,
           note="Input!L537 (922,782 t, the FY2023 throughput used for cost per ton) is the second, unselected column of the INDEX."),
    annual("vol_growth", "Volume growth — existing terminal", "%", const(0.03, first=0.0), "Input!K532:W532 (baseline row 533)", section=REV),
    annual("add_volume", "Additional volume — Belawan expansion (SGT3)", "t", ADD_VOL, "Calculation_FSL!J587:V587 = Calculation_SOEs!J450:V450 (typed 200,000 in M450, +50,000 p.a. to T450)", section=REV,
           note="v29 source issue: Calculation_SOEs!U450:V450 (FY2035-36) are empty cells, so the expansion volume drops to nil in FY2035-36; reproduced as 0."),
    annual("tariff", "Tariff (ASP)", "IDR/t", TARIFF, "Input!K539:W539 (baseline row 540; 29,658 FY2024-25, 43,947.5 FY2026-27, then +3% p.a.)", section=REV),
    # cost of sales
    scalar("emp_base", "Employee cost (ops) — base FY2023", "IDR bn", 3.279620518, "Input!J568 (Calculation_FSL!F613)", section=COS),
    annual("emp_growth", "Employee cost growth", "%", const(0.035), "Input!K563:W563", section=COS),
    scalar("sec_base", "Security expense — base FY2023", "IDR bn", 1.930177428, "Input!J575 (Calculation_FSL!F618)", section=COS),
    annual("sec_growth", "Security expense growth", "%", const(0.035), "Input!K570:W570", section=COS),
    scalar("base_vol_2023", "Volume base for cost per ton (FY2023 throughput)", "t", BASE_VOL, "Calculation_FSL!E623 (= E629, E641, E647, E653, E670; typed 922,782 t)", section=COS),
    scalar("fuel_base", "Fuel — cost FY2023", "IDR bn", 0.82569621188, "Input!J582 (Calculation_FSL!F624)", section=COS),
    annual("fuel_growth", "Fuel cost growth", "%", const(0.03), "Input!K577:W577", section=COS),
    scalar("util_base", "Utilities — cost FY2023", "IDR bn", 0.631021441, "Input!J589 (Calculation_FSL!F630)", section=COS),
    annual("util_growth", "Utilities cost growth", "%", const(0.03), "Input!K584:W584", section=COS),
    annual("conc_pct", "Concession fee — % of revenue", "%", const(0.025), "Calculation_FSL!J636:V636 = Input!K591:W591 (baseline row 592)", section=COS, fmt="pct2",
           note="Input!J596 = 0.5514 IDR bn is the FY2023 actual concession fee (~2.5% of FY2023 revenue of 22.24 bn); v29 row 637 applies the 2.5% of Input!K591:W591 directly to revenue; Calculation_FSL!F636 (labelled '% to Revenue' but holding that IDR bn amount) and the index row 634 are unused."),
    scalar("oth_base", "Ops other expense (variable) — cost FY2023", "IDR bn", 0.41230965056, "Input!J603 (Calculation_FSL!F642)", section=COS),
    annual("oth_growth", "Ops other expense growth", "%", const(0.03), "Input!K598:W598", section=COS),
    scalar("rm_base", "Repair & maintenance — cost FY2023", "IDR bn", 0.28658186344, "Input!J610 (Calculation_FSL!F648)", section=COS),
    annual("rm_growth", "Repair & maintenance growth", "%", const(0.03), "Input!K605:W605", section=COS),
    scalar("ot_base", "Employee overtime (variable) — cost FY2023", "IDR bn", 0.245423178, "Input!J617 (Calculation_FSL!F654)", section=COS),
    annual("ot_growth", "Overtime growth", "%", const(0.035), "Input!K612:W612", section=COS),
    annual("ins_rate", "Insurance on existing assets — % of existing depreciation charge", "%", INS_RATE_EXIST,
           "Calculation_FSL!J658:L658 (typed 1.0919279% FY2024-26); M658:V658 = Input!N619:W619 (0.2%)", section=COS, fmt="pct2",
           note="The typed FY2024-26 rate overrides the input sheet (Input!K619:M619 = 0, 0, 0.2%); from FY2027 the existing depreciation is nil so the rate has no effect."),
    annual("ins_new_rate", "Insurance on new assets — % of total capex p.a.", "%", INS_RATE_NEW, "Input!K619:W619 (baseline row 620; Calculation_FSL!J665:V665)", section=COS, fmt="pct2",
           note="Applied to the full 14.0246 USD m capex (Calculation_FSL!F664 = F605) from FY2026; the rate row is nil in FY2024-25 (no operating flag in the v29 formula)."),
    scalar("lab_base", "Labour (variable) — cost FY2023", "IDR bn", 0.0116, "Input!J631 (Calculation_FSL!F671)", section=COS),
    annual("lab_growth", "Labour growth", "%", const(0.035), "Input!K626:W626", section=COS),
    # depreciation of existing assets
    annual("dep_exist", "Depreciation of existing assets — annual charge", "IDR bn", DEP_EXIST, "Input!K546:W546 (baseline row 547; Calculation_FSL!J595:V595)", section=DEP,
           note="Existing Belawan assets are fully depreciated by FY2026 in v29 (5.23, 5.23, 2.62, then nil)."),
    annual("dep_exist_add", "Additional depreciation on replacement / minor capex", "IDR bn", const(0.0), "Calculation_FSL!J596:V596 = Input!K437:W437", section=DEP,
           note="v29 source issue: Input!K437:W437 are EMPTY cells (inside the Cigading conveyor input block, between rows 436 and 438), so the 'Addition' line is nil; the base cell Calculation_FSL!F595 = Input!J442 is likewise empty and unused. Reproduced as 0."),
]
for key, label, base, g, grow_row in opex_lines:
    inputs.append(scalar(f"{key}_base", f"{label} — base FY2023", "IDR bn", base, f"Input!J{BASE_ROW[key]}", section=OPX))
    inputs.append(annual(f"{key}_growth", f"{label} — growth", "%", const(g), f"Input!K{grow_row}:W{grow_row}", section=OPX))

calc = [
    growth_index("vol_index", "Volume index — existing terminal (1.00 in FY2023)", "vol_growth", "Revenue"),
    row("base_vol", "Volume — existing terminal = base x index", "t", "={in:vol_base}*{c:vol_index}*{flag}", "Revenue", fmt="tons", total=True),
    row("add_vol", "Volume — Belawan expansion (additional)", "t", "={in:add_volume}*{flag}", "Revenue", fmt="tons", total=True),
    row("volume", "Total volume handled (existing + expansion)", "t", "={c:base_vol}+{c:add_vol}", "Revenue", fmt="tons", total=True, bold=True),
    row("tariff", "Tariff (ASP)", "IDR/t", "={in:tariff}", "Revenue", fmt="idr_t"),
    row("revenue", "Revenue = total volume x tariff / 1e9", "IDR bn", "={c:volume}*{c:tariff}/10^9", "Revenue", fmt="idr_bn", total=True, bold=True),
]
calc += fixed_cost("emp", "Employee cost (ops)", "emp_base", "emp_growth", "Cost of sales")
calc += fixed_cost("sec", "Security expense", "sec_base", "sec_growth", "Cost of sales")
calc += per_ton_cost("fuel", "Fuel", "fuel_base", "base_vol_2023", "fuel_growth", "volume", "Cost of sales")
calc += per_ton_cost("util", "Utilities", "util_base", "base_vol_2023", "util_growth", "volume", "Cost of sales")
calc += [row("concession", "Concession fee = revenue x %", "IDR bn", "={c:revenue}*{in:conc_pct}", "Cost of sales", fmt="idr_bn", total=True)]
calc += per_ton_cost("oth", "Ops other expense (variable)", "oth_base", "base_vol_2023", "oth_growth", "volume", "Cost of sales")
calc += per_ton_cost("rm", "Repair & maintenance", "rm_base", "base_vol_2023", "rm_growth", "volume", "Cost of sales")
calc += per_ton_cost("ot", "Employee overtime (variable)", "ot_base", "base_vol_2023", "ot_growth", "volume", "Cost of sales")
calc += [
    row("insurance", "Insurance on existing assets = rate x depreciation of existing assets", "IDR bn", "={in:ins_rate}*{c:dep_exist}", "Cost of sales", fmt="idr_bn", total=True),
    row("insurance_new", "Insurance on new assets = total capex (IDR bn) x rate", "IDR bn", "=SUM({c:capex_idr@all})*{in:ins_new_rate}", "Cost of sales", fmt="idr_bn", total=True,
        note="v29 Calculation_FSL row 666: 14.0246 USD m x USD_IDR x Input!K619:W619 (0.2% from FY2026)"),
]
calc += per_ton_cost("lab", "Labour (variable)", "lab_base", "base_vol_2023", "lab_growth", "volume", "Cost of sales")
calc += [sum_rows("cogs", "Total cost of sales (excl. depreciation)",
                  ["emp", "sec", "fuel", "util", "concession", "oth", "rm", "ot", "insurance", "insurance_new", "lab"], "Cost of sales")]
for key, label, base, g, grow_row in opex_lines:
    calc += fixed_cost(key, label, f"{key}_base", f"{key}_growth", "Operating expenses (G&A)")
calc += [sum_rows("opex", "Total operating expenses", [k for k, *_ in opex_lines], "Operating expenses (G&A)")]
calc += [
    row("dep_exist", "Depreciation of existing assets = annual charge x flag + additions", "IDR bn", "={in:dep_exist}*{flag}+{in:dep_exist_add}", "Depreciation of existing assets", fmt="idr_bn", total=True),
    row("da_other", "Depreciation of existing assets (excl. project capex — see capex module below)", "IDR bn", "={c:dep_exist}", "Depreciation of existing assets", fmt="idr_bn", total=True, bold=True),
]

SPEC = {
    "id": "E3",
    "code": "Belawan",
    "name": "Belawan terminal (SGT3) incl. Belawan expansion",
    "short": "Belawan",
    "entity": "PT Sentral Grain Terminal (SGT3, Belawan)",
    "entity_short": "SGT Belawan",
    "category": "Existing business",
    "description": "Existing grain terminal at Belawan plus its expansion: existing volume (3% growth) and typed additional expansion volume from FY2027 at a per-ton tariff; fixed and per-ton costs indexed from FY2023, concession fee 2.5% of revenue, insurance; nine fixed G&A lines; existing-asset depreciation plus 14.0 USD m of new assets depreciated from FY2026.",
    "v29": {"calc": "Calculation_FSL rows 580-695", "input": "Input rows 529-693", "standalone": "Output_Standalone (IDR) rows 321-342", "flag": "Output_FSL!F37 (= 1)"},
    "v29_rows": {"rev": 323, "cogs": 324, "opex": 327, "da": 330, "ebit": 331, "fin": 333, "tax": 336, "np": 337},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": True,
    "depends": [],
    "commissioning": None,
    "capex": {
        "total_usd": CAPEX_TOTAL, "source": "Input!M551:N551 (7.02459 FY2026 + 7.0 FY2027; M552 = 7 + Input!K1276 legal-fee allocation); Calculation_FSL!F600 = SUM(Input!K551:O551); Calculation_FSL row 1480",
        "pct": {2026: CAPEX_2026 / CAPEX_TOTAL, 2027: CAPEX_2027 / CAPEX_TOTAL}, "pct_source": "v29 timing: Input!M551 (FY2026), N551 (FY2027); Calculation_FSL!L1480:M1480",
        "building_share": 0.9, "building_source": "Input!J556 (= K556; equipment Input!J557 = 100% - K556)",
        "life_b": 20, "life_e": 8, "lives_source": "Input!J559:J560 (= K559:K560)",
        "commissioning_year": 2026, "commissioning_source": "Calculation_FSL!F582 (Operation Period 2026); rows 602/607 also multiply by the Wharf 2 operating period row 357 (1 from 2025) — effective start FY2026",
        "hist_confirmed": 0,
        "note": "Belawan expansion (SGT3) capex; the business itself is existing (operating flag = forecast flag) while depreciation of the new assets starts in the capex commissioning year 2026. Percentages apply to total capex.",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": "da_other"},
}
