"""P02 Cigading Extended Conveyor — reference spec for a NEW project block.

v29: Calculation_FSL rows 398-436, Input rows 436-481, Output_Standalone (IDR) rows 160-181, flag Output_FSL!F33.
Effective v29 logic (all effective values shown, scenario Input!G4 = 1 -> baseline rows):
  Operating flag      : 1 from 2025 (Calculation_FSL!F400)
  Volume              : 2025 = Input!L439 = 2.1 m t; 2026+ = 2.1 m t x Wharf 2 volume index (Calculation_SOEs!J328 = Wharf 2 index, +3% p.a.)
                        (Input!K439:W439 shows 2.35 m t from 2029 but v29 does not use it)
  Tariff              : Input!K445:W445 = 15,000 IDR/t flat
  Cost of sales       : electricity  = Cigading existing electricity cost/t (Calculation_FSL row 277) x volume x 30% (Input!K464:W464)
                        insurance    = total capex 8.0 USD m x USD_IDR x 0.5% (Calculation_FSL!F429; Input!K475 = 0.2% is NOT used) x operating flag
                        R&M          = Cigading existing R&M cost/t (row 288) x volume x 30% (Input!K470:W470)
  Opex                : none (Output_Standalone row 166 blank)
  Depreciation        : capex 8.0 USD m (2.2 pre-2024, 5.4 FY2024, 0.4 FY2025; Input!J452:L452); building 90.63% / 20 yrs, equipment 9.37% / 8 yrs, from 2025
  Financing cost      : Input!K477:W477 = 0 (row 479 alternative schedule not selected)
"""

Y = list(range(2024, 2037))

SPEC = {
    "id": "P02",
    "code": "CigConveyor",
    "name": "Cigading Extended Conveyor",
    "short": "Cig. Ext Conveyor",
    "entity": "PT Sentral Grain Terminal (SGT, Cigading)",
    "entity_short": "SGT Cigading",
    "category": "Committed project",
    "description": "Conveyor extension at Cigading: additional cargodoring volume charged at a per-ton tariff; costs are electricity and maintenance shares of the existing terminal's cost per ton plus insurance on the new assets.",
    "v29": {"calc": "Calculation_FSL rows 398-436", "input": "Input rows 436-481", "standalone": "Output_Standalone (IDR) rows 160-181", "flag": "Output_FSL!F33 (= 1)"},
    "v29_rows": {"rev": 162, "cogs": 163, "opex": 166, "da": 169, "fin": 172, "tax": 175, "np": 176, "ebit": 170},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": ["E2", "P01"],
    "commissioning": {"year": 2025, "source": "Calculation_FSL!F400", "cls": "v29", "note": "Conveyor operating from FY2025."},
    "capex": {
        "total_usd": 8.0, "source": "Input!J452:L452 (2.2 + 5.4 + 0.4 USD m); board deck Dec-2024 use of proceeds 8.0",
        "pct": {2023: 2.2 / 8.0, 2024: 5.4 / 8.0, 2025: 0.4 / 8.0}, "pct_source": "v29 timing: Input!J452 (pre-2024), K452 (FY2024), L452 (FY2025)",
        "building_share": 0.9063408335724765, "building_source": "Input!K457 (equipment = Input!K458)",
        "life_b": 20, "life_e": 8, "lives_source": "Input!K460:K461",
        "hist_confirmed": 0,
        "note": "Percentages apply to total capex. Pre-2024 spend (27.5%) sits in Dec-23 assets under construction.",
    },
    "inputs": [
        {"key": "vol_base", "label": "Base volume in the first operating year (grows with the Wharf 2 volume index thereafter)", "unit": "t", "kind": "scalar", "value": 2100000,
         "source": "Input!L439 (= Calculation_FSL!K404); 2026+ volume = base x Calculation_SOEs!J328 (Wharf 2 index)", "cls": "v29",
         "note": "v29 grows conveyor volume with the Wharf 2 index (3% p.a.) and does not use the 2.35 m t entered in Input!P439:W439.", "section": "Revenue drivers"},
        {"key": "tariff", "label": "Conveyor tariff", "unit": "IDR/t", "kind": "annual", "values": {y: 15000 for y in Y},
         "source": "Input!K445:W445 (INDEX of baseline row 446)", "cls": "v29", "section": "Revenue drivers"},
        {"key": "elec_share", "label": "Electricity: consumption relative to the existing Cigading terminal (share of its cost per ton)", "unit": "%", "kind": "annual",
         "values": {y: (0.0 if y == 2024 else 0.30) for y in Y}, "source": "Input!K464:W464 (baseline row 465)", "cls": "v29", "section": "Cost drivers"},
        {"key": "rm_share", "label": "Repair & maintenance: share of the existing Cigading terminal cost per ton", "unit": "%", "kind": "annual",
         "values": {y: (0.0 if y == 2024 else 0.30) for y in Y}, "source": "Input!K470:W470 (baseline row 471)", "cls": "v29", "section": "Cost drivers"},
        {"key": "ins_rate", "label": "Insurance on new assets (% of total capex p.a.)", "unit": "%", "kind": "scalar", "value": 0.005,
         "source": "Calculation_FSL!F429 (0.5%; the 0.2% in Input!K475 is not used by v29)", "cls": "v29", "fmt": "pct2", "section": "Cost drivers"},
    ],
    "calc": [
        {"key": "vol_index", "label": "Volume index (Wharf 2 volume index; 1.00 in 2025)", "unit": "index", "f": "={x:P01:vol_index}", "fmt": "idx", "section": "Revenue"},
        {"key": "volume", "label": "Volume handled", "unit": "t", "f": "={in:vol_base}*{c:vol_index}*{c:opflag}", "fmt": "tons", "section": "Revenue", "total": True},
        {"key": "tariff", "label": "Tariff", "unit": "IDR/t", "f": "={in:tariff}", "fmt": "idr_t", "section": "Revenue"},
        {"key": "revenue", "label": "Revenue = volume x tariff / 1e9", "unit": "IDR bn", "f": "={c:volume}*{c:tariff}/10^9", "fmt": "idr_bn", "section": "Revenue", "total": True, "bold": True},
        {"key": "elec_cost_t", "label": "Electricity cost per ton — existing Cigading terminal (link)", "unit": "IDR/t", "f": "={x:E2:elec_cost_t}", "fmt": "idr_t", "section": "Cost of sales", "link": True},
        {"key": "elec", "label": "Electricity = cost/t x volume x share / 1e9", "unit": "IDR bn", "f": "={c:elec_cost_t}*{c:volume}*{in:elec_share}/10^9", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "insurance", "label": "Insurance = total capex (IDR bn) x rate x operating flag", "unit": "IDR bn", "f": "=SUM({c:capex_idr@all})*{in:ins_rate}*{c:opflag}", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "rm_cost_t", "label": "Repair & maintenance cost per ton — existing Cigading terminal (link)", "unit": "IDR/t", "f": "={x:E2:rm_cost_t}", "fmt": "idr_t", "section": "Cost of sales", "link": True},
        {"key": "rm", "label": "Repair & maintenance = cost/t x volume x share / 1e9", "unit": "IDR bn", "f": "={c:rm_cost_t}*{c:volume}*{in:rm_share}/10^9", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "cogs", "label": "Total cost of sales (excl. depreciation)", "unit": "IDR bn", "f": "={c:elec}+{c:insurance}+{c:rm}", "fmt": "idr_bn", "section": "Cost of sales", "total": True, "bold": True},
    ],
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": None, "da_other": None},
}
