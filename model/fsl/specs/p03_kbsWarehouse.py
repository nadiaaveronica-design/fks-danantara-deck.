"""P03 KBS Warehouse Revitalisation (Cigading) — new project block.

v29: Calculation_FSL rows 438-472 (volume index from Calculation_SOEs rows 363-373), Input rows 1269-1276 (capex),
Output_Standalone (IDR) rows 206-227, flag Output_FSL!F34 (= 1).
Effective v29 logic (scenario Input!G4 = 1 -> baseline rows):
  Operating flag : 1 from 2027 (Calculation_FSL!F441). Calculation_SOEs!F365 says 2026, but that flag only drives the
                   volume INDEX; revenue in Calculation_FSL row 445/453 starts in 2027.
  Volume index   : Calculation_SOEs row 368 = IF(SOEs operating flag (from 2026) = 0, 1, prior x (1 + 3%)) -> 1.00 in
                   2023-2025, 1.03 in 2026, 1.0609 in 2027 ... 1.38423 in 2036 (growth typed as 3% inside the formula)
  Volume         : Calculation_FSL!F445 = Calculation_SOEs!F369*0 + 1.7*Million -> typed 1,700,000 t (the 2.8 m t in
                   Calculation_SOEs!F369 is multiplied by 0); volume = 1.7 m t x index x operating flag [row 445]
                   -> 1,803,530 t in 2027 (index already 1.0609 in the first operating year)
  Tariff         : three components summed per ton: handling/bagging 28,000 (F446), weighing 7,000 (F447), storage 25,000 (F448)
                   = 60,000 IDR/t. v29 labels F446 "Ton/Month" but the formula (row 449 = volume x SUM(446:448) / Billion) applies
                   it as IDR per ton handled. Rows 446 in 2024-25 reference Input!K485:L485 (the Ciwandan volume-growth row, = 0)
                   and rows 447-448 are blank in 2024-25 — irrelevant because volume is nil before 2027.
  Revenue split  : gross revenue [row 449] x FKS share 49% (Calculation_FSL!F452) = FKS revenue [row 453]; KBS keeps 51% (F451 = 1 - F452)
  Cost of sales  : 10% of FKS revenue (Calculation_FSL!F457)
  Opex           : 50% of FKS revenue (Calculation_FSL!F458 = (38/60*100%-10%)*0 + 50%: the 53.3% expression is multiplied by 0)
  Depreciation   : NIL in v29 — v29 source issue C02: Calculation_FSL!F461 = Input!L1270 points at the EMPTY FY2025 capex cell;
                   the 6.02459 USD m capex is in Input!M1270 (FY2026, = 6 + Input!K1276 legal fee 2 IDR bn / USD_IDR / 5).
                   Building share 100% (F462), lives 20 yrs building (E461) / 10 yrs equipment (E466).
                   The revised model depreciates the capex from 2027 -> declared in v29_known_diffs (da, ebit).
  Financing cost : none (Output_Standalone row 218 blank); Tax: 22% of positive EBT (framework).
"""
from .helpers import Y, const, annual, scalar, row

REV, COS = "Revenue drivers", "Cost drivers"

inputs = [
    scalar("vol_base", "Base volume (tons handled through the revitalised warehouse, before indexation)", "t", 1700000,
           "Calculation_FSL!F445 (= Calculation_SOEs!F369*0 + 1.7*Million)", section=REV,
           note="v29 overrides the 2.8 m t in Calculation_SOEs!F369 with a typed 1.7 m t; the typed value is the effective assumption."),
    scalar("idx_start", "First year of volume indexation (index grows from this year; Calculation_SOEs 'Operation Period')", "year", 2026,
           "Calculation_SOEs!F365", section=REV, fmt="year",
           note="The index starts growing in 2026 although revenue starts in 2027 (Calculation_FSL!F441), so the first operating year already carries index 1.0609."),
    annual("idx_growth", "Volume index growth p.a. (applied from the indexation start year)", "%", const(0.03),
           "Calculation_SOEs!J368:V368 (3% typed inside the formula IF(J365=0,1,I368*(1+3%)))", section=REV),
    annual("tariff_handling", "Handling / bagging fee per ton", "IDR/t", const(28000),
           "Calculation_FSL!F446 (L446:V446 = $F$446)", section=REV,
           note="v29 labels the cell 'Ton/Month' but row 449 applies it per ton handled. J446:K446 (2024-25) reference Input!K485:L485 (= 0), irrelevant as volume is nil before 2027."),
    annual("tariff_weighing", "Weighing fee per ton", "IDR/t", const(7000),
           "Calculation_FSL!F447 (L447:V447 = $F$447; blank in 2024-25)", section=REV),
    annual("tariff_storage", "Storage fee per ton", "IDR/t", const(25000),
           "Calculation_FSL!F448 (L448:V448 = $F$448; blank in 2024-25)", section=REV),
    scalar("fks_share", "FKS (FSL) share of gross warehouse revenue (KBS keeps the remainder)", "%", 0.49,
           "Calculation_FSL!F452 (KBS share F451 = 1 - F452 = 51%)", section=REV),
    scalar("cogs_pct", "Cost of sales as % of FKS revenue", "%", 0.10, "Calculation_FSL!F457", section=COS),
    scalar("opex_pct", "Operating expenses as % of FKS revenue", "%", 0.50,
           "Calculation_FSL!F458 (= (38/60*100%-10%)*0 + 50%: typed 50% override)", section=COS,
           note="The 53.3% expression in the same cell is multiplied by 0; 50% is the effective assumption."),
]

calc = [
    row("vol_index", "Volume index (1.00 until the indexation start year, then x (1 + growth))", "index",
        "=IF({y}<{in:idx_start},1,{c:vol_index@prev}*(1+{in:idx_growth}))*{flag}", "Revenue", f0="=1", fmt="idx",
        note="Calculation_SOEs row 368 (1.03 in 2026, 1.0609 in 2027 ...)"),
    row("volume", "Volume handled = base x index x operating flag", "t", "={in:vol_base}*{c:vol_index}*{c:opflag}", "Revenue", fmt="tons", total=True,
        note="Calculation_FSL row 445"),
    row("tariff", "Tariff per ton = handling + weighing + storage", "IDR/t", "={in:tariff_handling}+{in:tariff_weighing}+{in:tariff_storage}", "Revenue", fmt="idr_t",
        note="Calculation_FSL SUM(J446:J448) = 60,000 IDR/t"),
    row("revenue_gross", "Gross warehouse revenue = volume x tariff / 1e9", "IDR bn", "={c:volume}*{c:tariff}/10^9", "Revenue", fmt="idr_bn", total=True,
        note="Calculation_FSL row 449"),
    row("revenue_kbs", "Revenue attributable to KBS = gross x (1 - FKS share) (memo, not FSL revenue)", "IDR bn", "={c:revenue_gross}*(1-{in:fks_share})", "Revenue", fmt="idr_bn", total=True,
        note="Calculation_FSL row 451"),
    row("revenue", "Revenue FKS = gross x FKS share", "IDR bn", "={c:revenue_gross}*{in:fks_share}", "Revenue", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL row 453 -> Output_Standalone (IDR) row 208"),
    row("cogs", "Cost of sales = FKS revenue x %", "IDR bn", "={c:revenue}*{in:cogs_pct}", "Cost of sales", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL row 457"),
    row("opex", "Operating expenses = FKS revenue x %", "IDR bn", "={c:revenue}*{in:opex_pct}", "Operating expenses", fmt="idr_bn", total=True, bold=True,
        note="Calculation_FSL row 458"),
]

SPEC = {
    "id": "P03",
    "code": "KBSWarehouse",
    "name": "KBS Warehouse Revitalisation (Cigading)",
    "short": "KBS Warehouse",
    "entity": "PT Sentral Grain Terminal (SGT, Cigading) with PT Krakatau Bandar Samudera (KBS)",
    "entity_short": "SGT Cigading / KBS",
    "category": "Planned project",
    "description": "Revitalisation of the KBS warehouse at Cigading: handling/bagging, weighing and storage fees per ton on an indexed 1.7 m t base; FKS books 49% of gross revenue, with cost of sales 10% and opex 50% of that revenue.",
    "v29": {"calc": "Calculation_FSL rows 438-472 (+ Calculation_SOEs rows 363-373)", "input": "Input rows 1269-1276",
            "standalone": "Output_Standalone (IDR) rows 206-227", "flag": "Output_FSL!F34 (= 1)"},
    "v29_rows": {"rev": 208, "cogs": 209, "opex": 212, "da": 215, "ebit": 216, "fin": 218, "tax": 221, "np": 222},
    "v29_known_diffs": {
        "da": "v29 depreciates nil on the 6.02 USD m warehouse capex (broken reference Calculation_FSL!F461 -> empty Input!L1270); the revised model depreciates it",
        "ebit": "follows from the D&A difference",
    },
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": [],
    "commissioning": {"year": 2027, "source": "Calculation_FSL!F441", "cls": "v29",
                      "note": "Revenue from FY2027 (Calculation_SOEs!F365 = 2026 only starts the volume index)."},
    "capex": {
        "total_usd": 6.02459, "source": "Input!M1270 (= Input!M1271 baseline = 6 + Input!K1276 legal fee 2 IDR bn / USD_IDR / 5 = 0.0246); Calculation_FSL!L1477",
        "pct": {2026: 1.0}, "pct_source": "v29 timing: Input!M1270 (FY2026 only); Calculation_FSL row 1477",
        "building_share": 1.0, "building_source": "Calculation_FSL!F462 (equipment = F467 = 1 - F462 = 0)",
        "life_b": 20, "life_e": 10, "lives_source": "Calculation_FSL!E461 (building 20) / E466 (equipment 10)",
        "hist_confirmed": 0,
        "note": "v29 source issue C02: Calculation_FSL!F461 (= Input!L1270, FY2025) is empty so v29 depreciates nothing; the revised model depreciates the FY2026 spend from the 2027 commissioning year.",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": None},
}
