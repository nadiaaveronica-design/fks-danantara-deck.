"""E1 Teluk Lamong (NPLOG) — existing business block.

v29: Calculation_FSL rows 18-125, Input rows 29-191, Output_Standalone (IDR) rows 18-40 ("Nplog"), flag Output_FSL!F28.
Effective v29 logic:
  Meals    : volume index (1 in 2023) x (1 + Input!K36:W36: 0% FY2024, 3% after) x base Input!J41 = 2,063,650 t; tariff Input!K43:W43
  Grains   : index (Input!K50:W50) x base Input!J55 = 1,602,570 t; tariff Input!K57:W57
  Additional grains: TBM operating flag x Input!K1172:W1172 (TBM cargo-handling volume) x Calculation_FSL!D5 (= 0 -> nil) at the grains tariff
  Cost of sales (per ton lines use the FY2023 volume 3,579,865.85 t, Calculation_FSL!E52):
    employee 12.869 (3.5%), electricity 4.3342 x 120% (3%), fuel 2.5548 x 120% (3%), security 2.0920 (3.5%), R&M 2.0449 x 120% (3%),
    overtime 1.2463 (3.5%), insurance 2.13023% x depreciation, labour 0.64506 (3.5%), ops other 0.23896 (3%)
  Depreciation: existing 41.4671 p.a. + additions Input!K62:W62 (0,0,1,1,1,2,2,2,3,3,3,3,3) + G&A depreciation 0.26834 (2%)
  Opex     : twelve fixed G&A lines (Input!J119:J130) grown at Input rows 134-190 (staff costs grown with Input!K134 = 3%, a v29 reference to the legal-fee row)
  Financing cost: none
"""
from .helpers import Y, const, annual, scalar, row, growth_index, fixed_cost, per_ton_cost, sum_rows

REV, COS, OPX, DEP = "Revenue drivers", "Cost of sales drivers", "Operating expenses (G&A)", "Depreciation"
BASE_VOL = 3579865.85
MEALS_P = {2024: 42880, 2025: 42880, 2026: 42880, 2027: 42880, 2028: 42880, 2029: 44166.4, 2030: 44166.4, 2031: 44166.4,
           2032: 45491.392, 2033: 45491.392, 2034: 45491.392, 2035: 45491.392, 2036: 45491.392}
GRAINS_P = {2024: 42400, 2025: 42400, 2026: 42400, 2027: 42400, 2028: 42400, 2029: 43672, 2030: 43672, 2031: 43672,
            2032: 44982.16, 2033: 44982.16, 2034: 44982.16, 2035: 44982.16, 2036: 44982.16}
TBM_VOL = {2024: 0, 2025: 0, 2026: 0, 2027: 0, 2028: 0, 2029: 1000000, 2030: 1500000, 2031: 2700000, 2032: 2000000, 2033: 3000000, 2034: 3000000, 2035: 3000000, 2036: 3000000}

opex_lines = [
    # key, label, base 2023 (Input!J119..J130), effective growth, growth source
    ("ga_legal", "Legal and professional fees", 6.647, 0.03, "Input!K134:W134"),
    ("ga_staff", "Staff costs — G&A", 2.55729, 0.03, "Input!K134:W134 (v29 Calculation_FSL row 99 references the legal-fee growth row instead of Input!K139 = 3.5%; effective 3% kept)"),
    ("ga_taxfee", "Tax fees", 1.0491, 0.03, "Input!K144:W144"),
    ("ga_travel", "Travelling and entertainment", 0.994492, 0.03, "Input!K150:W150"),
    ("ga_office", "Office expenses", 0.785963, 0.02, "Input!K155:W155"),
    ("ga_other", "Other administrative expenses", 0.658344, 0.03, "Input!K160:W160"),
    ("ga_rental", "Rental expenses — G&A", 0.274084, 0.02, "Input!K165:W165"),
    ("ga_comm", "Communication expenses — G&A", 0.225279, 0.02, "Input!K175:W175"),
    ("ga_security", "Security services / outsourcing", 0.212824, 0.03, "Input!K180:W180"),
    ("ga_donation", "Donation & CSR", 0.192331, 0.03, "Input!K185:W185"),
    ("ga_utility", "Utility expenses", 0.00210121, 0.02, "Input!K190:W190"),
]
BASE_ROW = {"ga_legal": 119, "ga_staff": 120, "ga_taxfee": 121, "ga_travel": 122, "ga_office": 123, "ga_other": 124, "ga_rental": 125,
            "ga_comm": 127, "ga_security": 128, "ga_donation": 129, "ga_utility": 130}

inputs = [
    scalar("meals_base", "Meals — base volume FY2023", "t", 2063650, "Input!J41 (Calculation_FSL!F22)", section=REV),
    annual("meals_growth", "Meals — volume growth", "%", const(0.03, first=0.0), "Input!K36:W36 (baseline row 37)", section=REV),
    annual("meals_tariff", "Meals — tariff", "IDR/t", MEALS_P, "Input!K43:W43 (baseline row 44; steps in FY2029 and FY2032)", section=REV),
    scalar("grains_base", "Grains — base volume FY2023", "t", 1602570, "Input!J55 (Calculation_FSL!F27)", section=REV),
    annual("grains_growth", "Grains — volume growth", "%", const(0.03, first=0.0), "Input!K50:W50 (baseline row 51)", section=REV),
    annual("grains_tariff", "Grains — tariff", "IDR/t", GRAINS_P, "Input!K57:W57 (baseline row 58)", section=REV),
    scalar("add_switch", "Additional grains volume switch (v29 Calculation_FSL!D5 = 0: TBM-linked additional volume not counted)", "0/1", 0, "Calculation_FSL!D5", cls="CONTROL", section=REV,
           note="v29 multiplies the TBM cargo-handling volume by this switch (0) and by the TBM operating flag; kept at 0."),
    annual("add_volume", "Additional grains volume (TBM cargo-handling volume; effective only when the switch = 1)", "t", TBM_VOL, "Input!K1172:W1172 (Calculation_FSL row 32)", section=REV),
    scalar("emp_base", "Employee cost — base FY2023", "IDR bn", 12.86929567153, "Calculation_FSL!F47 (typed)", section=COS),
    annual("emp_growth", "Employee cost growth", "%", const(0.035), "Input!K68:W68", section=COS),
    scalar("base_vol_2023", "Volume base for cost per ton (FY2023 throughput)", "t", BASE_VOL, "Calculation_FSL!E52 (3,579,865.85 t)", section=COS),
    scalar("uplift", "Cost-per-ton uplift applied by v29 to electricity, fuel and R&M (x1.20)", "x", 1.2, "Calculation_FSL!F52, F58, F69 (x120%)", section=COS, fmt="num2"),
    scalar("elec_base", "Electricity — cost FY2023", "IDR bn", 4.3341669714466, "Calculation_FSL!F53", section=COS),
    annual("elec_growth", "Electricity cost growth", "%", const(0.03), "Input!K75:W75", section=COS),
    scalar("fuel_base", "Fuel — cost FY2023", "IDR bn", 2.5548429764421, "Calculation_FSL!F59", section=COS),
    annual("fuel_growth", "Fuel cost growth", "%", const(0.03), "Input!K80:W80", section=COS),
    scalar("sec_base", "Security expense — base FY2023", "IDR bn", 2.092034448, "Calculation_FSL!F64", section=COS),
    annual("sec_growth", "Security expense growth", "%", const(0.035), "Input!K85:W85", section=COS),
    scalar("rm_base", "Repair & maintenance — cost FY2023", "IDR bn", 2.0448544530069, "Calculation_FSL!F70", section=COS),
    annual("rm_growth", "Repair & maintenance growth", "%", const(0.03), "Input!K91:W91", section=COS),
    scalar("ot_base", "Employee overtime (variable) — cost FY2023", "IDR bn", 1.246304098, "Calculation_FSL!F76", section=COS),
    annual("ot_growth", "Overtime growth", "%", const(0.035), "Input!K95:W95", section=COS),
    annual("ins_rate", "Insurance — % of depreciation charge", "%", const(0.0213023), "Input!K100:W100", section=COS, fmt="pct2"),
    scalar("lab_base", "Labour (variable) — cost FY2023", "IDR bn", 0.64506, "Calculation_FSL!F88", section=COS),
    annual("lab_growth", "Labour growth", "%", const(0.035), "Input!K105:W105", section=COS),
    scalar("oth_base", "Ops other expense (variable) — cost FY2023", "IDR bn", 0.2389568971904, "Calculation_FSL!F94", section=COS),
    annual("oth_growth", "Ops other expense growth", "%", const(0.03), "Input!K110:W110", section=COS),
    scalar("dep_exist_base", "Depreciation of existing assets — annual charge", "IDR bn", 41.4670756824223, "Calculation_FSL!F41", section=DEP,
           note="Charged for the whole forecast in v29 (no net-book-value cap) — see Checks."),
    annual("dep_exist_add", "Additional depreciation on replacement / minor capex", "IDR bn", {2024: 0, 2025: 0, 2026: 1, 2027: 1, 2028: 1, 2029: 2, 2030: 2, 2031: 2, 2032: 3, 2033: 3, 2034: 3, 2035: 3, 2036: 3},
           "Input!K62:W62 (baseline row 63)", section=DEP, note="v29 shows no corresponding capex cash flow for these additions."),
    scalar("ga_dep_base", "Depreciation — G&A assets, base FY2023", "IDR bn", 0.26834, "Input!J126", section=DEP),
    annual("ga_dep_growth", "Depreciation — G&A growth", "%", const(0.02), "Input!K170:W170", section=DEP),
]
for key, label, base, g, src in opex_lines:
    inputs.append(scalar(f"{key}_base", f"{label} — base FY2023", "IDR bn", base, f"Input!J{BASE_ROW[key]}", section=OPX))
    inputs.append(annual(f"{key}_growth", f"{label} — growth", "%", const(g), src, section=OPX))

calc = [
    growth_index("meals_idx", "Meals — volume index (1.00 in FY2023)", "meals_growth", "Revenue"),
    row("meals_vol", "Meals — volume", "t", "={in:meals_base}*{c:meals_idx}*{flag}", "Revenue", fmt="tons", total=True),
    row("meals_rev", "Meals — revenue = volume x tariff / 1e9", "IDR bn", "={c:meals_vol}*{in:meals_tariff}/10^9", "Revenue", fmt="idr_bn", total=True),
    growth_index("grains_idx", "Grains — volume index (1.00 in FY2023)", "grains_growth", "Revenue"),
    row("grains_vol", "Grains — volume", "t", "={in:grains_base}*{c:grains_idx}*{flag}", "Revenue", fmt="tons", total=True),
    row("grains_rev", "Grains — revenue = volume x tariff / 1e9", "IDR bn", "={c:grains_vol}*{in:grains_tariff}/10^9", "Revenue", fmt="idr_bn", total=True),
    row("add_vol", "Additional grains volume (TBM-linked) x switch", "t", "={in:add_volume}*{in:add_switch}*{flag}", "Revenue", fmt="tons", total=True),
    row("add_rev", "Additional grains — revenue at the grains tariff", "IDR bn", "={c:add_vol}*{in:grains_tariff}/10^9", "Revenue", fmt="idr_bn", total=True),
    row("volume", "Total volume handled", "t", "={c:meals_vol}+{c:grains_vol}+{c:add_vol}", "Revenue", fmt="tons", total=True, bold=True),
    row("revenue", "Total revenue", "IDR bn", "={c:meals_rev}+{c:grains_rev}+{c:add_rev}", "Revenue", fmt="idr_bn", total=True, bold=True),
]
calc += fixed_cost("emp", "Employee cost", "emp_base", "emp_growth", "Cost of sales")
calc += per_ton_cost("elec", "Electricity", "elec_base", "base_vol_2023", "elec_growth", "volume", "Cost of sales", uplift="uplift")
calc += per_ton_cost("fuel", "Fuel", "fuel_base", "base_vol_2023", "fuel_growth", "volume", "Cost of sales", uplift="uplift")
calc += fixed_cost("sec", "Security expense", "sec_base", "sec_growth", "Cost of sales")
calc += per_ton_cost("rm", "Repair & maintenance", "rm_base", "base_vol_2023", "rm_growth", "volume", "Cost of sales", uplift="uplift")
calc += per_ton_cost("ot", "Employee overtime (variable)", "ot_base", "base_vol_2023", "ot_growth", "volume", "Cost of sales")
calc += [row("insurance", "Insurance = rate x depreciation of existing assets", "IDR bn", "={in:ins_rate}*{c:dep_exist}", "Cost of sales", fmt="idr_bn", total=True)]
calc += per_ton_cost("lab", "Labour (variable)", "lab_base", "base_vol_2023", "lab_growth", "volume", "Cost of sales")
calc += per_ton_cost("oth", "Ops other expense (variable)", "oth_base", "base_vol_2023", "oth_growth", "volume", "Cost of sales")
calc += [sum_rows("cogs", "Total cost of sales (excl. depreciation)", ["emp", "elec", "fuel", "sec", "rm", "ot", "insurance", "lab", "oth"], "Cost of sales")]
for key, label, base, g, src in opex_lines:
    calc += fixed_cost(key, label, f"{key}_base", f"{key}_growth", "Operating expenses (G&A)")
calc += [sum_rows("opex", "Total operating expenses (excl. G&A depreciation)", [k for k, *_ in opex_lines], "Operating expenses (G&A)")]
calc += [
    row("dep_exist", "Depreciation of existing assets = annual charge x flag + additions", "IDR bn", "={in:dep_exist_base}*{flag}+{in:dep_exist_add}", "Depreciation of existing assets", fmt="idr_bn", total=True),
] + fixed_cost("ga_dep", "Depreciation — G&A assets", "ga_dep_base", "ga_dep_growth", "Depreciation of existing assets") + [
    sum_rows("da_other", "Depreciation of existing and G&A assets (excl. project capex)", ["dep_exist", "ga_dep"], "Depreciation of existing assets"),
]

SPEC = {
    "id": "E1",
    "code": "TelukLamong",
    "name": "Teluk Lamong (NPLOG) cargodoring & delivery",
    "short": "Teluk Lamong",
    "entity": "PT Nusantara Pelabuhan Logistik (NPLOG, Teluk Lamong, Surabaya) — 65% FSL",
    "entity_short": "NPLOG Teluk Lamong",
    "category": "Existing business",
    "description": "Existing grain and meal terminal operations at Teluk Lamong (conveyor, warehouse, delivery): volume x tariff for meals and grains; variable costs per ton indexed from FY2023; fixed G&A lines; depreciation of existing assets.",
    "v29": {"calc": "Calculation_FSL rows 18-125", "input": "Input rows 29-191", "standalone": "Output_Standalone (IDR) rows 18-40 (Nplog)", "flag": "Output_FSL!F28 (= 1)"},
    "v29_rows": {"rev": 20, "cogs": 21, "opex": 24, "da": 27, "fin": 30, "tax": 33, "np": 34, "ebit": 28},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 0.65},
    "existing": True,
    "depends": [],
    "commissioning": None,
    "capex": None,
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": "da_other"},
}
