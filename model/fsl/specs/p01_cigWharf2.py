"""P01 Cigading Wharf 2 — new project block.

v29: Calculation_FSL rows 355-396, Input rows 393-435, Output_Standalone (IDR) rows 137-158, flag Output_FSL!F32.
Effective v29 logic:
  Operating flag : 1 from 2025 (Calculation_FSL!F357)
  Volume index   : 0 before 2025, 1 in 2025, then x (1 + Input!K400:W400 growth 3%)   [Calculation_FSL row 360]
  Volume         : index x base 2,449,985.568 t (Input!K405 = 3,049,985.568 - 600,000)          [row 361]
  Tariff         : Input!K407:W407 (40,944 in 2025-26; 49,132.8 2027-28; 54,046.1 2029-30; 57,288.8 2031-32; 60,726.2 2033-36)
  Opex           : 20% of revenue (Calculation_FSL!F366)  -> Output_Standalone row 143
  Cost of sales  : electricity cost/t (Cigading existing row 277) x volume; heavy-equipment rental cost/t (row 299) x volume;
                   R&M cost/t (row 288) x volume; insurance = 12.8 USD m x USD_IDR x 0.5% (F390; Input!K431 = 0.2% not used) x flag
  Depreciation   : 12.8 USD m (10 pre-2024, 2.3 FY2024, 0.5 FY2025); building 52.68% / 20 yrs, equipment 47.32% / 8 yrs, from 2025
  Financing cost : Input!K433:W433 -> 13.33 in FY2025 only (LT loan interest allocated by v29 to this line; treated as corporate in the revised model)
"""
Y = list(range(2024, 2037))
TARIFF = {2024: 0, 2025: 40944, 2026: 40944, 2027: 49132.8, 2028: 49132.8, 2029: 54046.08, 2030: 54046.08, 2031: 57288.8448,
          2032: 57288.8448, 2033: 60726.175488, 2034: 60726.175488, 2035: 60726.175488, 2036: 60726.175488}

SPEC = {
    "id": "P01",
    "code": "CigWharf2",
    "name": "Cigading Wharf 2",
    "short": "Cig. Wharf 2",
    "entity": "PT Sentral Grain Terminal (SGT, Cigading)",
    "entity_short": "SGT Cigading",
    "category": "Committed project",
    "description": "Second wharf at Cigading: additional meals/grains volume at a stevedoring tariff; variable costs use the existing terminal's cost per ton, opex 20% of revenue, insurance on new assets.",
    "v29": {"calc": "Calculation_FSL rows 355-396", "input": "Input rows 393-435", "standalone": "Output_Standalone (IDR) rows 137-158", "flag": "Output_FSL!F32 (= 1)"},
    "v29_rows": {"rev": 139, "cogs": 140, "opex": 143, "da": 146, "fin": 149, "tax": 152, "np": 153, "ebit": 147},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": ["E2"],
    "commissioning": {"year": 2025, "source": "Calculation_FSL!F357", "cls": "v29", "note": "Wharf 2 operating from FY2025."},
    "capex": {
        "total_usd": 12.8, "source": "Input!J420:L420 (10.0 + 2.3 + 0.5 USD m); board deck / v29 use of proceeds 12.8",
        "pct": {2023: 10.0 / 12.8, 2024: 2.3 / 12.8, 2025: 0.5 / 12.8}, "pct_source": "v29 timing: Input!J420 (pre-2024), K420 (FY2024), L420 (FY2025)",
        "building_share": 0.5267870771133069, "building_source": "Input!K425 (equipment = Input!K426)",
        "life_b": 20, "life_e": 8, "lives_source": "Input!K428:K429",
        "hist_confirmed": 0,
        "note": "Percentages apply to total capex. Pre-2024 spend (78.1%) sits in Dec-23 assets under construction.",
    },
    "inputs": [
        {"key": "vol_base", "label": "Base volume in the first operating year (FY2025)", "unit": "t", "kind": "scalar", "value": 2449985.568,
         "source": "Input!K405 (= 3,049,985.568 - 600,000)", "cls": "v29", "section": "Revenue drivers"},
        {"key": "vol_growth", "label": "Volume growth (applied from the second operating year)", "unit": "%", "kind": "annual", "values": {y: (0.0 if y == 2024 else 0.03) for y in Y},
         "source": "Input!K400:W400 (baseline row 401)", "cls": "v29", "section": "Revenue drivers"},
        {"key": "tariff", "label": "Stevedoring tariff (meals)", "unit": "IDR/t", "kind": "annual", "values": TARIFF,
         "source": "Input!K407:W407 (baseline row 408; step-ups every two years)", "cls": "v29", "section": "Revenue drivers"},
        {"key": "opex_pct", "label": "Operating expenses as % of revenue", "unit": "%", "kind": "scalar", "value": 0.20, "source": "Calculation_FSL!F366", "cls": "v29", "section": "Cost drivers"},
        {"key": "ins_rate", "label": "Insurance on new assets (% of total capex p.a.)", "unit": "%", "kind": "scalar", "value": 0.005,
         "source": "Calculation_FSL!F390 (0.5%; the 0.2% in Input!K431 is not used by v29)", "cls": "v29", "fmt": "pct2", "section": "Cost drivers"},
    ],
    "calc": [
        {"key": "vol_index", "label": "Volume index (1.00 in the commissioning year, then x (1 + growth))", "unit": "index",
         "f": "=IF({y}<{in:commissioning},0,IF({y}={in:commissioning},1,{c:vol_index@prev}*(1+{in:vol_growth})))*{flag}", "f0": "=0", "fmt": "idx", "section": "Revenue"},
        {"key": "volume", "label": "Volume handled", "unit": "t", "f": "={c:vol_index}*{in:vol_base}", "fmt": "tons", "section": "Revenue", "total": True},
        {"key": "tariff", "label": "Tariff", "unit": "IDR/t", "f": "={in:tariff}", "fmt": "idr_t", "section": "Revenue"},
        {"key": "revenue", "label": "Revenue = volume x tariff / 1e9", "unit": "IDR bn", "f": "={c:volume}*{c:tariff}/10^9", "fmt": "idr_bn", "section": "Revenue", "total": True, "bold": True},
        {"key": "elec_cost_t", "label": "Electricity cost per ton — existing Cigading terminal (link)", "unit": "IDR/t", "f": "={x:E2:elec_cost_t}", "fmt": "idr_t", "section": "Cost of sales", "link": True},
        {"key": "elec", "label": "Electricity = cost/t x volume / 1e9", "unit": "IDR bn", "f": "={c:elec_cost_t}*{c:volume}/10^9", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "solar_cost_t", "label": "Heavy-equipment rental cost per ton — existing Cigading terminal (link)", "unit": "IDR/t", "f": "={x:E2:solar_cost_t}", "fmt": "idr_t", "section": "Cost of sales", "link": True},
        {"key": "solar", "label": "Heavy-equipment rental = cost/t x volume / 1e9", "unit": "IDR bn", "f": "={c:solar_cost_t}*{c:volume}/10^9", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "insurance", "label": "Insurance = total capex (IDR bn) x rate x operating flag", "unit": "IDR bn", "f": "=SUM({c:capex_idr@all})*{in:ins_rate}*{c:opflag}", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "rm_cost_t", "label": "Repair & maintenance cost per ton — existing Cigading terminal (link)", "unit": "IDR/t", "f": "={x:E2:rm_cost_t}", "fmt": "idr_t", "section": "Cost of sales", "link": True},
        {"key": "rm", "label": "Repair & maintenance = cost/t x volume / 1e9", "unit": "IDR bn", "f": "={c:rm_cost_t}*{c:volume}/10^9", "fmt": "idr_bn", "section": "Cost of sales", "total": True},
        {"key": "cogs", "label": "Total cost of sales (excl. depreciation)", "unit": "IDR bn", "f": "={c:elec}+{c:solar}+{c:insurance}+{c:rm}", "fmt": "idr_bn", "section": "Cost of sales", "total": True, "bold": True},
        {"key": "opex", "label": "Operating expenses = revenue x %", "unit": "IDR bn", "f": "={c:revenue}*{in:opex_pct}", "fmt": "idr_bn", "section": "Operating expenses", "total": True, "bold": True},
    ],
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": None},
}
