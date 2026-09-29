"""P04 Teluk Lamong silo (TTL Silo) — new project block.

v29: Calculation_FSL rows 127-165, Input rows 1263-1267 (capex), Output_Standalone (IDR) rows 42-64, flag Output_FSL!F29 (= 1).
Effective v29 logic (scenario Input!G4 = 1 -> baseline rows):
  Operating flag : 1 from 2027 (Calculation_FSL!F129; row 129 = IF(year < 2027, 0, 1) x model flag J$12)
  Capacity       : 2 silos (E133) x 8,500 t/month (F133) = 17,000 t/month [row 133 = row 137 "Total Volume", constant all years]
  Fee            : 65,000 IDR/t/month (F132 — labelled "Volume Index" in v29 but used as the price index: J134:V134 = $F$132)
  Revenue bagging: 17,000 x 65,000 / Billion x operating flag x Month_Year (12) = 13.26 IDR bn p.a. from 2027 [row 135]
                   -> Output_Standalone (IDR) row 44 = Calculation_FSL row 135
  Revenue WB     : nil — row 143 = volume (row 141 = row 133 monthly tonnage) x price (row 142) / Billion x J$12 x 0.
                   Row 142 references Input!K227:L227 in 2024-25 (= the Teluk Lamong EMPLOYEE COST GROWTH baseline, 3.5% — a
                   wrong reference) and a typed 2,000 IDR/t from 2026; irrelevant because the formula ends "* 0".
                   Reproduced with a weighbridge switch input = 0 and the effective price row (documented as v29 source issue).
  "Cost of Sales": row 147 = -300 IDR/t (F147) x 17,000 t/month x 12 / Billion x operating flag = -0.0612 IDR bn p.a.
                   The standalone block posts this row under OPERATING EXPENSES (Output_Standalone row 48 = Calculation_FSL row 147),
                   so the effective classification is opex -> hooked as `opex` here.
  Cost of sales  : NIL in the standalone block — v29 source issue: Output_Standalone row 45 = -Calculation_FSL!J62 x $F$19, and
                   Calculation_FSL row 62 is the EMPTY header row "5. Security Expense" of the Teluk Lamong (E1) block (a stale
                   copy-paste reference). Reproduced as nil (hook cogs = None) and documented.
  Depreciation   : capex 3.7623 USD m in FY2026 (Input!M1264 = INDEX baseline M1265 = (7.5 + Input!K1276) / 2, where K1276 =
                   legal fee 2 IDR bn / USD_IDR / Million / 5 = 0.0246; Calculation_FSL!L1478). Building 63% (F152) / 20 yrs (E151),
                   equipment 37% (F157 = 1 - F152) / 10 yrs (E156), both x operating flag from 2027, no end within the horizon:
                   1.9276 + 2.26417 = 4.19177 IDR bn p.a. [rows 153/158 -> row 150 -> Output_Standalone row 51]. Framework method 1
                   reproduces this exactly (total capex x share / life x in-service flag).
  Orphan rows    : rows 160-164 "Other Cost (exc Depre)" (cost/t = Calculation_FSL row 379 = Cigading Wharf 2 electricity cost/t;
                   proportion = Input!K239:W239 = Cigading electricity ACTUAL COST 3.89791 in 2024 then blank; volume = row 408 =
                   Extended Conveyor volume) evaluate to 0 and are NOT referenced by the standalone block -> not modelled.
  Financing cost : none (Output_Standalone row 54 blank). Tax: 22% of positive EBT (framework).
  Ownership      : v29 treats the silo as 100% FSL (econ_interest 1.0) although it is located at / operated with the NPLOG
                   Teluk Lamong terminal in which FSL holds 65% — kept as in v29 and noted.
"""
from .helpers import Y, const, annual, scalar, row

REV, WB, OPX = "Revenue drivers (silo bagging / storage)", "Revenue drivers (weighbridge — nil in v29)", "Cost drivers"

inputs = [
    scalar("n_silo", "Number of silos", "silos", 2, "Calculation_FSL!E133", section=REV, fmt="int"),
    scalar("silo_cap", "Throughput capacity per silo per month", "t/month", 8500, "Calculation_FSL!F133 (row 133 = E133 x F133 = 17,000 t/month)", section=REV),
    scalar("months_pa", "Operating months per year", "months", 12, "Named constant Month_Year (= 12) used in Calculation_FSL rows 135 and 147", section=REV, fmt="int"),
    annual("storage_fee", "Silo bagging / storage fee per ton per month", "IDR/t/month", const(65000),
           "Calculation_FSL!F132 (row 134 J134:V134 = $F$132)", section=REV,
           note="v29 labels F132 'Volume Index' but applies it as the price index (IDR/ton/month) in row 134/135."),
    scalar("wb_switch", "Weighbridge revenue switch (1 = include, 0 = excluded as in v29)", "flag", 0,
           "Calculation_FSL!J143:V143 — formula ends '*0' so weighbridge revenue is nil", section=WB, fmt="flag",
           note="v29 source issue: the weighbridge revenue row exists but is multiplied by 0; Output_Standalone row 44 only links to the bagging revenue row 135."),
    annual("wb_price", "Weighbridge price per ton (effective v29 values; not used while the switch is 0)", "IDR/t",
           {y: (0.035 if y <= 2025 else 2000) for y in Y},
           "Calculation_FSL!J142:K142 = Input!K227:L227 (2024-25); L142 = 2,000 typed, M142:V142 = prior year", section=WB,
           note="v29 source issue: J142:K142 point at Input!K227:L227 = Teluk Lamong employee-cost growth baseline (3.5%), not a price; the effective values are reproduced as-is because the row is inert (x 0)."),
    scalar("handling_cost_t", "Handling cost per ton (v29 'Cost of Sales' 300 IDR/MT; posted as operating expenses in the standalone block)", "IDR/t", 300,
           "Calculation_FSL!F147 (row 147 = -F147 x row 133 / Billion x Month_Year x row 129)", section=OPX,
           note="Output_Standalone (IDR) row 48 (Operating Expenses) = Calculation_FSL row 147 -> effective classification is opex."),
]

calc = [
    row("capacity_m", "Silo capacity per month = number of silos x capacity per silo", "t/month", "={in:n_silo}*{in:silo_cap}", "Revenue — silo bagging / storage", fmt="tons",
        note="Calculation_FSL row 133 (= row 137 'Total Volume'; 17,000 t/month, constant in all years)"),
    row("volume", "Annual volume = monthly capacity x months x operating flag", "t", "={c:capacity_m}*{in:months_pa}*{c:opflag}", "Revenue — silo bagging / storage", fmt="tons", total=True,
        note="Derived: v29 keeps the monthly figure in row 133/137 and applies Month_Year (12) inside the revenue and cost formulas (rows 135, 147)"),
    row("fee", "Fee per ton per month", "IDR/t/month", "={in:storage_fee}", "Revenue — silo bagging / storage", fmt="idr_t",
        note="Calculation_FSL row 134"),
    row("revenue_bagging", "Revenue bagging = annual volume x fee / 1e9", "IDR bn", "={c:volume}*{c:fee}/10^9", "Revenue — silo bagging / storage", fmt="idr_bn", total=True,
        note="Calculation_FSL row 135 (= 17,000 x 65,000 / Billion x flag x 12 = 13.26 p.a. from 2027) -> Output_Standalone (IDR) row 44"),
    row("wb_price", "Weighbridge price per ton", "IDR/t", "={in:wb_price}", "Revenue — weighbridge (nil in v29)", fmt="idr_t",
        note="Calculation_FSL row 142"),
    row("revenue_wb", "Revenue weighbridge = monthly capacity x price / 1e9 x forecast flag x switch", "IDR bn", "={c:capacity_m}*{c:wb_price}/10^9*{flag}*{in:wb_switch}", "Revenue — weighbridge (nil in v29)", fmt="idr_bn", total=True,
        note="Calculation_FSL row 143 (= row 141 x row 142 / Billion x J$12 x 0): v29 uses the MONTHLY tonnage without x12 and without the operating flag; nil because of the x0"),
    row("revenue", "Total revenue = bagging + weighbridge", "IDR bn", "={c:revenue_bagging}+{c:revenue_wb}", "Revenue — total", fmt="idr_bn", total=True, bold=True,
        note="Output_Standalone (IDR) row 44 links to the bagging row only; the weighbridge row is nil in v29"),
    row("cogs", "Cost of sales — nil in v29 (standalone block links to an empty header row)", "IDR bn", "=0", "Cost of sales", fmt="idr_bn", total=True, bold=True,
        note="v29 source issue: Output_Standalone (IDR) row 45 = -Calculation_FSL!J62 x $F$19; row 62 is the empty header '5. Security Expense' of the Teluk Lamong block -> 0"),
    row("handling_cost", "Handling cost = cost per ton x annual volume / 1e9 (v29 'Cost of Sales', posted as opex)", "IDR bn", "={in:handling_cost_t}*{c:volume}/10^9", "Operating expenses", fmt="idr_bn", total=True,
        note="Calculation_FSL row 147 (= -300 x 17,000 / Billion x 12 x flag = -0.0612 p.a. from 2027) -> Output_Standalone (IDR) row 48"),
    row("opex", "Operating expenses (total)", "IDR bn", "={c:handling_cost}", "Operating expenses", fmt="idr_bn", total=True, bold=True,
        note="Output_Standalone (IDR) row 48 = Calculation_FSL row 147"),
]

SPEC = {
    "id": "P04",
    "code": "TTLSilo",
    "name": "Teluk Lamong Silo",
    "short": "TTL Silo",
    "entity": "PT Nusantara Pelabuhan Logistik (NPLOG, Teluk Lamong, Surabaya) — v29 treats the silo as 100% FSL",
    "entity_short": "NPLOG Teluk Lamong",
    "category": "Planned project",
    "description": "Two 8,500 t/month silos at Teluk Lamong charging a bagging/storage fee of 65,000 IDR per ton per month from 2027; a 300 IDR/t handling cost (booked as opex in v29) and depreciation of the 3.76 USD m capex (building 63% / 20 yrs, equipment 37% / 10 yrs).",
    "v29": {"calc": "Calculation_FSL rows 127-165", "input": "Input rows 1263-1267 (capex)",
            "standalone": "Output_Standalone (IDR) rows 42-64", "flag": "Output_FSL!F29 (= 1)"},
    "v29_rows": {"rev": 44, "cogs": 45, "opex": 48, "da": 51, "ebit": 52, "fin": 54, "tax": 57, "np": 58},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": [],
    "commissioning": {"year": 2027, "source": "Calculation_FSL!F129", "cls": "v29",
                      "note": "Silo operating (revenue, handling cost and depreciation) from FY2027; capex spent in FY2026."},
    "capex": {
        "total_usd": 3.7623, "source": "Input!M1264 (= INDEX baseline Input!M1265 = (7.5 + Input!K1276 legal fee 0.0246) / 2); Calculation_FSL!L1478; F151",
        "pct": {2026: 1.0}, "pct_source": "v29 timing: Input!M1264 (FY2026 only); Calculation_FSL row 1478",
        "building_share": 0.63, "building_source": "Calculation_FSL!F152 (equipment = F157 = 1 - F152 = 37%)",
        "life_b": 20, "life_e": 10, "lives_source": "Calculation_FSL!E151 (building 20) / E156 (equipment 10)",
        "hist_confirmed": 0,
        "note": "Single FY2026 spend depreciated from the 2027 operating year: 3.7623 x 0.63 / 20 + 3.7623 x 0.37 / 10 USD m x USD_IDR = 4.19177 IDR bn p.a. (Calculation_FSL rows 153/158). v29 treats the asset as 100% FSL although it sits at the 65%-owned NPLOG terminal.",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": None, "opex": "opex", "da_other": None},
}
