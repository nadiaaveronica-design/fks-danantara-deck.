"""E2 Cigading existing terminal (SGT 2) — reference spec for an EXISTING business block.

v29: Calculation_FSL rows 252-353, Input rows 195-392, Output_Standalone (IDR) rows 113-135, flag Output_FSL!F31.
Effective v29 logic:
  Volume         : index (1 in 2023) x (1 + Input!K204:W204: 0% in 2024, 3% from 2025) x base 1,100,000 t
                   (Calculation_FSL!F256 = Input!J209*0 + 1,100,000: the 1.99 m t in Input!J209 is overridden by a typed 1.1 m t)
  Tariff         : FY2024 = Input!L211 x 1.03 = 35,143.6 (v29 formula J259 = Input!L211*K255); FY2025+ = Wharf 2 tariff (Calculation_FSL row 362)
  Cost of sales  : employee (5.423 x index 3.5%), electricity (3.8979 / 1,990,024.66 t x volume, index 3%), security (2.1487, 3.5%),
                   R&M (1.39159, 3%/t), insurance (3.31675% x depreciation), heavy-equipment rental (1.19846, 3%/t),
                   ops other variable (0.659907, 2%/t), overtime (0.213092, 3.5%/t), labour (0.0706463, 3.5%/t), pest control fixed (0.0025, 2%)
  Depreciation   : existing assets 40.8292 p.a. + additions Input!K218:W218 (0,0,1,1,1,2,2,2,3,3,3,3,3) + G&A depreciation (0.127107, 2%)
  Opex           : eleven fixed G&A lines (Input!J318:J328) grown at Input rows 332-383, excluding G&A depreciation (in D&A)
  Financing cost : Input!K388:W388 (5.47 FY2024, 1.94 FY2025) — LT loan interest; treated as corporate in the revised model
"""
from .helpers import Y, const, annual, scalar, row, growth_index, fixed_cost, per_ton_cost, sum_rows

REV, COS, OPX, DEP = "Revenue drivers", "Cost of sales drivers", "Operating expenses (G&A)", "Depreciation"
BASE_VOL = 1990024.66

opex_lines = [
    # key, label, base 2023 (Input!J318..J328), growth, growth source row
    ("ga_staff", "Staff costs — G&A", 4.2735, 0.035, 332),
    ("ga_legal", "Legal and professional fees", 3.07751, 0.03, 337),
    ("ga_security", "Security services / outsourcing", 0.434634, 0.03, 342),
    ("ga_other", "Other administrative expenses", 0.386327, 0.03, 348),
    ("ga_taxfee", "Tax fees", 0.35, 0.03, 353),
    ("ga_travel", "Travelling and entertainment", 0.245788, 0.03, 358),
    ("ga_donation", "Donation & CSR", 0.0474447, 0.03, 368),
    ("ga_office", "Office expenses", 0.0206404, 0.02, 373),
    ("ga_comm", "Communication expenses — G&A", 0.0170842, 0.02, 378),
    ("ga_rental", "Rental expenses — G&A", 0.0129, 0.02, 383),
]
BASE_ROW = {"ga_staff": 318, "ga_legal": 319, "ga_security": 320, "ga_other": 321, "ga_taxfee": 322, "ga_travel": 323,
            "ga_donation": 325, "ga_office": 326, "ga_comm": 327, "ga_rental": 328}

inputs = [
    scalar("vol_base", "Base volume FY2023 (grains & meals)", "t", 1100000, "Calculation_FSL!F256 (typed 1,100,000; Input!J209 = 1,990,025 is multiplied by 0 and not used)", section=REV,
           note="v29 overrides the input sheet with a typed 1.1 m t; kept as the effective v29 assumption."),
    annual("vol_growth", "Volume growth", "%", const(0.03, first=0.0), "Input!K204:W204 (baseline row 205)", section=REV),
    scalar("tariff_2024", "Tariff FY2024", "IDR/t", 35143.6, "Calculation_FSL!J259 = Input!L211 (34,120) x 1.03", section=REV,
           note="From FY2025 v29 applies the Wharf 2 tariff to the existing terminal (Calculation_FSL!K259:V259 = row 362); linked to P01 in the calc sheet."),
    # cost of sales
    scalar("emp_base", "Employee cost — base FY2023", "IDR bn", 5.423, "Input!J231", section=COS),
    annual("emp_growth", "Employee cost growth", "%", const(0.035), "Input!K226:W226", section=COS),
    scalar("base_vol_2023", "Volume base for cost per ton (FY2023 throughput)", "t", BASE_VOL, "Calculation_FSL!E277 (1,990,024.66 t)", section=COS),
    scalar("elec_base", "Electricity — cost FY2023", "IDR bn", 3.897911782, "Input!J239 / Calculation_FSL!F278", section=COS),
    annual("elec_growth", "Electricity cost growth", "%", const(0.03), "Input!K234:W234", section=COS),
    scalar("sec_base", "Security expense — base FY2023", "IDR bn", 2.1487, "Input!J255", section=COS),
    annual("sec_growth", "Security expense growth", "%", const(0.035), "Input!K250:W250", section=COS),
    scalar("rm_base", "Repair & maintenance — cost FY2023", "IDR bn", 1.39158765303, "Input!J263 / Calculation_FSL!F289", section=COS),
    annual("rm_growth", "Repair & maintenance growth", "%", const(0.03), "Input!K258:W258", section=COS),
    annual("ins_rate", "Insurance — % of depreciation charge", "%", const(0.033167495), "Input!K274:W274", section=COS, fmt="pct2"),
    scalar("solar_base", "Heavy-equipment rental (solar) — cost FY2023", "IDR bn", 1.198458964, "Input!J271 / Calculation_FSL!F300", section=COS),
    annual("solar_growth", "Heavy-equipment rental growth", "%", const(0.03), "Input!K266:W266", section=COS),
    scalar("oth_base", "Ops other expense (variable) — cost FY2023", "IDR bn", 0.659907061, "Input!J288 / Calculation_FSL!F306", section=COS),
    annual("oth_growth", "Ops other expense growth", "%", const(0.02), "Input!K283:W283", section=COS),
    scalar("ot_base", "Employee overtime (variable) — cost FY2023", "IDR bn", 0.213092265, "Input!J296 / Calculation_FSL!F312", section=COS),
    annual("ot_growth", "Overtime growth", "%", const(0.035), "Input!K291:W291", section=COS),
    scalar("lab_base", "Labour (variable) — cost FY2023", "IDR bn", 0.070646303, "Input!J303 / Calculation_FSL!F318", section=COS),
    annual("lab_growth", "Labour growth", "%", const(0.035), "Input!K298:W298", section=COS),
    scalar("pest_base", "Pest control (fixed) — base FY2023", "IDR bn", 0.0025, "Input!J311", section=COS),
    annual("pest_growth", "Pest control growth", "%", const(0.02), "Input!K306:W306", section=COS),
    # depreciation of existing assets
    scalar("dep_exist_base", "Depreciation of existing assets — annual charge", "IDR bn", 40.8292, "Input!J223 / Calculation_FSL!F266", section=DEP,
           note="Charged for the whole forecast in v29 (no net-book-value cap) — see Checks."),
    annual("dep_exist_add", "Additional depreciation on replacement / minor capex", "IDR bn", {2024: 0, 2025: 0, 2026: 1, 2027: 1, 2028: 1, 2029: 2, 2030: 2, 2031: 2, 2032: 3, 2033: 3, 2034: 3, 2035: 3, 2036: 3},
           "Input!K218:W218 (baseline row 219)", section=DEP, note="v29 shows no corresponding capex cash flow for these additions."),
    scalar("ga_dep_base", "Depreciation — G&A assets, base FY2023", "IDR bn", 0.127107, "Input!J324", section=DEP),
    annual("ga_dep_growth", "Depreciation — G&A growth", "%", const(0.02), "Input!K363:W363", section=DEP),
]
for key, label, base, g, grow_row in opex_lines:
    inputs.append(scalar(f"{key}_base", f"{label} — base FY2023", "IDR bn", base, f"Input!J{BASE_ROW[key]}", section=OPX))
    inputs.append(annual(f"{key}_growth", f"{label} — growth", "%", const(g), f"Input!K{grow_row}:W{grow_row}", section=OPX))

calc = [
    growth_index("vol_index", "Volume index (1.00 in FY2023)", "vol_growth", "Revenue"),
    row("volume", "Volume handled (grains & meals)", "t", "={in:vol_base}*{c:vol_index}*{flag}", "Revenue", fmt="tons", total=True),
    row("tariff", "Tariff (FY2024 own tariff; FY2025+ = Wharf 2 tariff, as in v29)", "IDR/t", "=IF({y}=2024,{in:tariff_2024},{xin:P01:tariff})", "Revenue", fmt="idr_t",
        note="v29 Calculation_FSL!K259:V259 link to the Wharf 2 tariff row 362"),
    row("revenue", "Revenue = volume x tariff / 1e9", "IDR bn", "={c:volume}*{c:tariff}/10^9", "Revenue", fmt="idr_bn", total=True, bold=True),
]
calc += fixed_cost("emp", "Employee cost", "emp_base", "emp_growth", "Cost of sales")
calc += per_ton_cost("elec", "Electricity", "elec_base", "base_vol_2023", "elec_growth", "volume", "Cost of sales")
calc += fixed_cost("sec", "Security expense", "sec_base", "sec_growth", "Cost of sales")
calc += per_ton_cost("rm", "Repair & maintenance", "rm_base", "base_vol_2023", "rm_growth", "volume", "Cost of sales")
calc += [row("insurance", "Insurance = rate x depreciation of existing assets", "IDR bn", "={in:ins_rate}*{c:dep_exist}", "Cost of sales", fmt="idr_bn", total=True)]
calc += per_ton_cost("solar", "Heavy-equipment rental", "solar_base", "base_vol_2023", "solar_growth", "volume", "Cost of sales")
calc += per_ton_cost("oth", "Ops other expense (variable)", "oth_base", "base_vol_2023", "oth_growth", "volume", "Cost of sales")
calc += per_ton_cost("ot", "Employee overtime (variable)", "ot_base", "base_vol_2023", "ot_growth", "volume", "Cost of sales")
calc += per_ton_cost("lab", "Labour (variable)", "lab_base", "base_vol_2023", "lab_growth", "volume", "Cost of sales")
calc += fixed_cost("pest", "Pest control (fixed)", "pest_base", "pest_growth", "Cost of sales")
calc += [sum_rows("cogs", "Total cost of sales (excl. depreciation)", ["emp", "elec", "sec", "rm", "insurance", "solar", "oth", "ot", "lab", "pest"], "Cost of sales")]
for key, label, base, g, grow_row in opex_lines:
    calc += fixed_cost(key, label, f"{key}_base", f"{key}_growth", "Operating expenses (G&A)")
calc += [sum_rows("opex", "Total operating expenses (excl. G&A depreciation)", [k for k, *_ in opex_lines], "Operating expenses (G&A)")]
calc += [
    row("dep_exist", "Depreciation of existing assets = annual charge x flag + additions", "IDR bn", "={in:dep_exist_base}*{flag}+{in:dep_exist_add}", "Depreciation of existing assets", fmt="idr_bn", total=True),
] + fixed_cost("ga_dep", "Depreciation — G&A assets", "ga_dep_base", "ga_dep_growth", "Depreciation of existing assets") + [
    sum_rows("da_other", "Depreciation of existing and G&A assets (excl. project capex)", ["dep_exist", "ga_dep"], "Depreciation of existing assets"),
]

SPEC = {
    "id": "E2",
    "code": "CigadingExist",
    "name": "Cigading Existing Terminal (SGT 2)",
    "short": "Cigading existing",
    "entity": "PT Sentral Grain Terminal (SGT, Cigading)",
    "entity_short": "SGT Cigading",
    "category": "Existing business",
    "description": "Existing grain terminal at Cigading: stevedoring / cargodoring volume at a per-ton tariff (Wharf 2 tariff from FY2025), variable costs per ton indexed from FY2023 actuals, fixed G&A lines, depreciation of existing assets.",
    "v29": {"calc": "Calculation_FSL rows 252-353", "input": "Input rows 195-392", "standalone": "Output_Standalone (IDR) rows 113-135", "flag": "Output_FSL!F31 (= 1)"},
    "v29_rows": {"rev": 115, "cogs": 116, "opex": 119, "da": 122, "fin": 125, "tax": 128, "np": 129, "ebit": 123},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": True,
    "depends": ["P01"],
    "commissioning": None,
    "capex": None,
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": "da_other"},
}
