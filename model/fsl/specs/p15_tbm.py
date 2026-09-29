"""P15 TBM (Tanjung Batu / Pelindo land lease, warehousing, cargo handling) — pipeline project block, EXCLUDED in v29.

v29: Calculation_FSL rows 1089-1159, Input rows 1128-1231, Output_Standalone (IDR) rows 482-503 ("Profit and Loss - TBM"),
     inclusion flag Output_FSL!F40 = 0 -> every standalone P&L line is multiplied by 0 and the capex row Calculation_FSL!1481
     (= Input!K1190:W1190 x Output_FSL!$F$40) is nil. The harness therefore compares the Calculation_FSL rows directly
     (v29_calc_rows: 1119 sales, 1140 cost of sales, 1159 opex, 1121 depreciation); EBIT is not compared.
     defaults.in_valuation = 0 (excluded by default, as in v29), category "Pipeline (excluded by default)".

Effective v29 logic (scenario Input!G4 = 1 -> baseline rows; all values shown are the effective ones):
  Operating flag    : 1 from 2027 (Calculation_FSL!F1091 "Operation Period") — used only as the land-lease index start (F1094 = F1091)
                      and, through Input!K1202:W1202 (= 1 from 2027), as the depreciation flag.
  1. Land lease     : index 1.00 in 2027 then x (1 + Input!K1140:W1140 = 3% from 2028) [row 1094]; area Input!K1133:W1133
                      (0 to 2027, 255,000 sqm 2028, 355,000 sqm 2029, 500,000 sqm from 2030) [row 1095]; price = Input!N1138 = 0
                      IDR/sqm/month x index [row 1096] -> revenue = area x price x 12 / 1e9 = NIL [row 1097].
  2. Flat storage   : index 1.00 in 2029 (F1099 typed) then x (1 + Input!K1153:W1153 = 3% from 2029) [row 1099].
                      Stored volume per month [row 1102]: 2024-26 = E1 meals volume (row 22) x % of Teluk Lamong (Input!K1146:M1146 = 0)
                      / 12 -> nil; 2027-29 TYPED 1.6 m t / 12 = 133,333.3 t/month; 2030+ TYPED 240,000 t/month. The "% of Teluk
                      Lamong" row 1100 (0.49 typed in 2027, 0.145 2028, 0.13 2029, 0.145 from 2030) is therefore bypassed from 2027.
                      Price = Input!O1151 = 55,000 IDR/t/month x index [row 1103]; revenue = volume x price x 12 / 1e9 [row 1104]
                      -> 88.0 in 2029, 163.15 in 2030 ... 194.81 in 2036.
  3. Silo           : index 1.00 in 2029 (F1106) then x (1 + Input!K1166:W1166 = 3% from 2030) [row 1106].
                      Stored volume per month [row 1109]: 2024-26 = E1 grains volume x % x 0 + cargo-handling volume / 12 (= flat-storage
                      monthly volume = 0) -> nil; 2027 TYPED 1.0 m t / 12 = 83,333.3; 2028 TYPED 1.6 m t / 12 = 133,333.3;
                      2029 = (E1 grains volume row 27 - 300,000 t) x 70% / 12 = 90,873 t/month; 2030+ TYPED 208,000 t/month.
                      The "% of Teluk Lamong" row 1107 (0.15) is never effective (multiplied by 0 / bypassed by typed values).
                      Price = Input!P1164 = 65,000 IDR/t/month x index [row 1110]; revenue = volume x price x 12 / 1e9 [row 1111]
                      -> 70.88 in 2029, 167.11 in 2030 ... 199.54 in 2036.
  4. Cargo handling : volume = flat-storage monthly volume x 12 [row 1114] (1.6 m t 2027-29, 2.88 m t from 2030);
                      price = Input!K1177:W1177 (0 to 2027, 15,000 IDR/t from 2028) x index [row 1115], where the index [row 1113]
                      = silo index (row 1106) from 2026 (2024-25 use an own formula that references the EMPTY growth row Input!K1143:L1143
                      -> 0); revenue = volume x price / 1e9 [row 1116] -> 24.0 in 2029, 44.50 in 2030 ... 53.13 in 2036.
  Total sales       : row 1119 = sum of the four streams -> nil to 2028, 182.88 in 2029, 374.76 in 2030 ... 447.48 in 2036.
  Cost of sales     : row 1140 = warehouse rental cost (Input!K1207:W1207 = 30% from 2025 x (flat storage + silo revenue), rows 1142-1144)
                      + cargo handling cost (= E1 Teluk Lamong cost of sales / revenue ratio, IFERROR(row 39 / row 38, 0) ~20%,
                      x cargo-handling revenue, rows 1147-1149).
  Opex              : row 1159 = total sales x Input!K1215:W1215 (18% from 2027) x 0.5 in 2027 (typed half-year factor in M1159).
  Depreciation      : row 1121 = SUM(land, building, equipment) x 0.5 in 2027 (typed in M1121). Capex 40.0246 USD m (Input!M1186
                      = 108 - 68 + Input!K1276 legal fee 2 IDR bn / USD_IDR / 5) x proportions land 0% (Input!J1193, life 90 yrs J1197),
                      building 90% (J1194, 20 yrs J1198), equipment 10% (J1195, 8 yrs J1199) x Input!K1202:W1202 (1 from 2027)
                      -> 29.295 + 8.1375 = 37.4325 p.a. from 2028 (18.716 in 2027).
                      Capex cash flow: Input!K1190:W1190 S-curve 28.0172 USD m FY2025 + 12.0074 USD m FY2026 (row 1481, x F40 = 0).
  Financing cost    : none (Output_Standalone row 494 blank). Working capital days Input!K1224:K1226 = 0 (framework globals apply).

v29 source issues reproduced as effective behaviour / documented:
  * Output_FSL!F40 = 0: TBM is excluded from the FSL consolidation and from the capex schedule -> in_valuation default 0 here.
  * Half-year factor 0.5 in 2027 on depreciation (M1121) and opex (M1159). Opex is reproduced through the annual "first-year factor"
    input (immaterial: revenue is nil in 2027). Depreciation cannot take the factor through the framework's capex module, so the
    revised model charges the full 37.43 in 2027 vs 18.72 in v29 -> declared in v29_known_diffs (da, 2027 only).
  * Commissioning 2027 (F1091) but every revenue stream with a price starts in 2029 (F1099 / F1106 / F1113 typed) -> FY2027-28 carry
    depreciation without revenue in v29 as well.
  * Flat storage / silo volumes are TYPED inside the Calculation_FSL formulas from 2027 (M1102:V1102, M1109:V1109); the "% of Teluk
    Lamong volume" inputs (Input rows 1146 / 1159) are effectively dead. Exposed as override inputs (0 = use % of E1 volume).
  * The cargo-handling volume input Input!K1172:W1172 (1.0 m t 2029 ... 3.0 m t) is NOT used by the TBM block (F1114 = Input!K1148 is a
    stray reference; row 1114 = row 1102 x 12); it only feeds E1 row 32 (switched off by Calculation_FSL!D5 = 0).
  * Row 1114 is labelled "IDR Bio" but holds tons; Input rows 1197-1199 are mislabelled (1197 "Building" = land life 90 yrs,
    1198 "Equipment" = building life 20 yrs). Stray helper cells (rows 1093, 1105, 1112, 1151-1153 "Land Lease Cost") are not used.
  * Land assets (0% of capex, 90 yrs) carry no depreciation; the framework's two-class capex module (building 90% / equipment 10%)
    reproduces the v29 charge exactly.
"""
from .helpers import Y, const, annual, scalar, row

TIM, LL, FS, SI, CH, COS, OPX = ("Revenue timing", "Land lease", "Warehouse rental — flat storage", "Warehouse rental — silo",
                                 "Cargo handling", "Cost of sales drivers", "Operating expenses")
MILLION = 1_000_000
CAPEX_TOTAL = 40 + 2 / 16.265 / 5                     # Input!M1186 = 108 - 68 + K1276 (K1276 = 2 IDR bn / USD_IDR / 5) = 40.0245927 USD m
CAPEX_2025, CAPEX_2026 = 28.017214878573625, 12.007377805102983    # Input!L1190, M1190 (S-curve)

LL_AREA = {2024: 0, 2025: 0, 2026: 0, 2027: 0, 2028: 255000, 2029: 355000, 2030: 500000, 2031: 500000, 2032: 500000, 2033: 500000,
           2034: 500000, 2035: 500000, 2036: 500000}
FS_PCT = {2024: 0, 2025: 0, 2026: 0, 2027: 0.49, 2028: 0.145, 2029: 0.13, 2030: 0.145, 2031: 0.145, 2032: 0.145, 2033: 0.145,
          2034: 0.145, 2035: 0.145, 2036: 0.145}
FS_OVERRIDE = {y: (0 if y < 2027 else (1.6 * MILLION / 12 if y <= 2029 else 240000)) for y in Y}
SILO_OVERRIDE = {y: (0 if y < 2027 else (1.0 * MILLION / 12 if y == 2027 else (1.6 * MILLION / 12 if y == 2028 else (0 if y == 2029 else 208000)))) for y in Y}
SILO_SHARE = {y: (0.70 if y == 2029 else 0) for y in Y}
CH_PRICE = {y: (0 if y <= 2027 else 15000) for y in Y}

inputs = [
    scalar("wh_start", "First revenue year of flat storage, silo and cargo handling (price index = 1.00 in this year)", "year", 2029,
           "Calculation_FSL!F1099, F1106, F1113 (typed 2029)", section=TIM, fmt="year",
           note="Two years after the 2027 commissioning (F1091) that starts depreciation; the land-lease index starts in the commissioning year (F1094 = F1091)."),
    annual("first_year_factor", "First-year factor applied by v29 to opex (and depreciation) in the commissioning year (0.5 = half year)", "x",
           {y: (0.5 if y == 2027 else 1.0) for y in Y}, "Calculation_FSL!M1159 (*0.5), M1121 (*0.5)", section=TIM, fmt="num2",
           note="v29 source issue: typed half-year factor in 2027 only. Applied to opex here; the framework's depreciation cannot take it (declared v29 known diff)."),
    # land lease
    annual("ll_area", "Land lease — leased area", "sqm", LL_AREA, "Input!K1133:W1133 (INDEX of baseline row 1134) -> Calculation_FSL row 1095", section=LL),
    scalar("ll_asp", "Land lease — rent per sqm per month (base, indexed from the commissioning year)", "IDR/sqm/month", 0,
           "Input!N1138 (= Calculation_FSL!F1096)", section=LL, note="v29 carries no land-lease price: revenue stream is nil."),
    annual("ll_growth", "Land lease — rent growth p.a.", "%", {y: (0 if y <= 2027 else 0.03) for y in Y},
           "Input!K1140:W1140 (baseline row 1141; 3% from FY2028) -> Calculation_FSL row 1094", section=LL),
    # flat storage
    annual("fs_pct", "Flat storage — % of Teluk Lamong (E1) meals volume stored (used only when the override below is 0)", "%", FS_PCT,
           "Calculation_FSL!J1100:V1100 (2024-26 = Input!K1146:M1146 = 0; 0.49 typed in M1100, 0.145 N1100, 0.13 O1100, 0.145 P1100:V1100)", section=FS,
           note="Bypassed by v29 from 2027 because the stored volume is typed directly into row 1102 (see override)."),
    annual("fs_vol_override", "Flat storage — stored volume per month typed by v29 (0 = derive from % of E1 meals volume)", "t/month", FS_OVERRIDE,
           "Calculation_FSL!M1102:O1102 (= 1.6*Million/Month_Year), P1102:V1102 (240,000)", section=FS,
           note="v29 typed values inside the formulas; effective assumption. 2024-26 formula = E1 meals volume x % / 12 with % = 0."),
    scalar("fs_asp", "Flat storage — storage fee per ton per month (base, indexed from the first revenue year)", "IDR/t/month", 55000,
           "Input!O1151 (= Calculation_FSL!F1103)", section=FS),
    annual("fs_growth", "Flat storage — fee growth p.a.", "%", {y: (0 if y <= 2028 else 0.03) for y in Y},
           "Input!K1153:W1153 (baseline row 1154; 3% from FY2029) -> Calculation_FSL row 1099", section=FS),
    # silo
    annual("silo_vol_override", "Silo — stored volume per month typed by v29 (0 = derive from E1 grains volume below)", "t/month", SILO_OVERRIDE,
           "Calculation_FSL!M1109 (= 1*Million/12), N1109 (= 1.6*Million/12), P1109:V1109 (208,000); O1109 (2029) is a formula", section=SI,
           note="v29 typed values inside the formulas; the '% of Teluk Lamong' input (Input!K1159:W1159 / row 1107 = 15%) is multiplied by 0 and never effective."),
    scalar("silo_grains_deduct", "Silo — grains volume deducted before applying the share (2029 formula)", "t", 300000,
           "Calculation_FSL!O1109 (= (O1108 - 0.3*Million) * 70% / 12)", section=SI),
    annual("silo_grains_share", "Silo — share of (E1 grains volume - deduction) stored per year, / 12 for the monthly volume (used when the override is 0)", "%",
           SILO_SHARE, "Calculation_FSL!O1109 (70% typed, FY2029 only); other years 0 (2024-26 formula = cargo-handling volume / 12 = 0)", section=SI),
    scalar("silo_asp", "Silo — storage fee per ton per month (base, indexed from the first revenue year)", "IDR/t/month", 65000,
           "Input!P1164 (= Calculation_FSL!F1110)", section=SI),
    annual("silo_growth", "Silo — fee growth p.a.", "%", {y: (0 if y <= 2029 else 0.03) for y in Y},
           "Input!K1166:W1166 (baseline row 1167; 3% from FY2030) -> Calculation_FSL row 1106", section=SI),
    # cargo handling
    annual("ch_price", "Cargo handling — fee per ton (base, x silo price index)", "IDR/t", CH_PRICE,
           "Input!K1177:W1177 (baseline row 1178; 15,000 from FY2028) -> Calculation_FSL row 1115", section=CH,
           note="Index row 1113 = silo index (row 1106) from 2026; 2024-25 reference the empty growth row Input!K1143:L1143 (-> 0). Volume = flat-storage monthly volume x 12 (row 1114); Input!K1172:W1172 is not used by the block."),
    # costs
    annual("wh_cost_pct", "Warehouse rental cost as % of warehouse (flat storage + silo) revenue", "%", const(0.30, first=0.0),
           "Input!K1207:W1207 (INDEX of row 1208; 0 in FY2024) -> Calculation_FSL row 1143", section=COS),
    annual("opex_pct", "Operating expenses as % of total revenue", "%", {y: (0 if y <= 2026 else 0.18) for y in Y},
           "Input!K1215:W1215 (baseline row 1216; 18% from FY2027) -> Calculation_FSL row 1158", section=OPX),
]

calc = [
    # land lease
    row("ll_idx", "Land lease — rent index (1.00 in the commissioning year, then x (1 + growth))", "index",
        "=IF({y}<{in:commissioning},0,IF({y}={in:commissioning},1,{c:ll_idx@prev}*(1+{in:ll_growth})))*{flag}", "Revenue — land lease", f0="=0", fmt="idx",
        src="Calculation_FSL row 1094"),
    row("ll_area", "Land lease — leased area", "sqm", "={in:ll_area}*{flag}", "Revenue — land lease", fmt="sqm", src="Calculation_FSL row 1095"),
    row("ll_price", "Land lease — rent per sqm per month = base x index", "IDR/sqm/month", "={in:ll_asp}*{c:ll_idx}", "Revenue — land lease", fmt="idr_t", src="Calculation_FSL row 1096"),
    row("ll_rev", "Land lease revenue = area x rent x 12 / 1e9", "IDR bn", "={c:ll_area}*{c:ll_price}*12/10^9", "Revenue — land lease", fmt="idr_bn", total=True, src="Calculation_FSL row 1097"),
    # flat storage
    row("fs_idx", "Flat storage — fee index (1.00 in the first revenue year, then x (1 + growth))", "index",
        "=IF({y}<{in:wh_start},0,IF({y}={in:wh_start},1,{c:fs_idx@prev}*(1+{in:fs_growth})))*{flag}", "Revenue — flat storage", f0="=0", fmt="idx", src="Calculation_FSL row 1099"),
    row("tl_meals_vol", "Teluk Lamong meals volume (E1 link)", "t", "={x:E1:meals_vol}", "Revenue — flat storage", fmt="tons", link=True, src="Calculation_FSL row 1101 = row 22"),
    row("fs_vol_pct", "Flat storage — monthly volume from % of E1 meals volume = volume x % / 12", "t/month", "={c:tl_meals_vol}*{in:fs_pct}/12", "Revenue — flat storage", fmt="tons",
        src="Calculation_FSL row 1102 (2024-26 formula)"),
    row("fs_vol", "Flat storage — stored volume per month = override if > 0, else % of E1 volume", "t/month", "=IF({in:fs_vol_override}>0,{in:fs_vol_override},{c:fs_vol_pct})*{flag}",
        "Revenue — flat storage", fmt="tons", src="Calculation_FSL row 1102"),
    row("fs_price", "Flat storage — fee per ton per month = base x index", "IDR/t/month", "={in:fs_asp}*{c:fs_idx}", "Revenue — flat storage", fmt="idr_t", src="Calculation_FSL row 1103"),
    row("fs_rev", "Flat storage revenue = monthly volume x fee x 12 / 1e9", "IDR bn", "={c:fs_vol}*{c:fs_price}*12/10^9", "Revenue — flat storage", fmt="idr_bn", total=True, src="Calculation_FSL row 1104"),
    # silo
    row("silo_idx", "Silo — fee index (1.00 in the first revenue year, then x (1 + growth))", "index",
        "=IF({y}<{in:wh_start},0,IF({y}={in:wh_start},1,{c:silo_idx@prev}*(1+{in:silo_growth})))*{flag}", "Revenue — silo", f0="=0", fmt="idx", src="Calculation_FSL row 1106"),
    row("tl_grains_vol", "Teluk Lamong grains volume (E1 link)", "t", "={x:E1:grains_vol}", "Revenue — silo", fmt="tons", link=True, src="Calculation_FSL row 1108 = row 27"),
    row("silo_vol_grains", "Silo — monthly volume from E1 grains = (grains volume - deduction) x share / 12", "t/month",
        "=({c:tl_grains_vol}-{in:silo_grains_deduct})*{in:silo_grains_share}/12", "Revenue — silo", fmt="tons", src="Calculation_FSL!O1109"),
    row("silo_vol", "Silo — stored volume per month = override if > 0, else from E1 grains volume", "t/month",
        "=IF({in:silo_vol_override}>0,{in:silo_vol_override},{c:silo_vol_grains})*{flag}", "Revenue — silo", fmt="tons", src="Calculation_FSL row 1109"),
    row("silo_price", "Silo — fee per ton per month = base x index", "IDR/t/month", "={in:silo_asp}*{c:silo_idx}", "Revenue — silo", fmt="idr_t", src="Calculation_FSL row 1110"),
    row("silo_rev", "Silo revenue = monthly volume x fee x 12 / 1e9", "IDR bn", "={c:silo_vol}*{c:silo_price}*12/10^9", "Revenue — silo", fmt="idr_bn", total=True, src="Calculation_FSL row 1111"),
    # cargo handling
    row("ch_idx", "Cargo handling — price index (= silo index, as in v29)", "index", "={c:silo_idx}", "Revenue — cargo handling", f0="=0", fmt="idx", src="Calculation_FSL row 1113 (= row 1106 from 2026)"),
    row("ch_vol", "Cargo handling — annual volume = flat-storage monthly volume x 12", "t", "={c:fs_vol}*12", "Revenue — cargo handling", fmt="tons", total=True, src="Calculation_FSL row 1114"),
    row("ch_price", "Cargo handling — fee per ton = base x index", "IDR/t", "={in:ch_price}*{c:ch_idx}", "Revenue — cargo handling", fmt="idr_t", src="Calculation_FSL row 1115"),
    row("ch_rev", "Cargo handling revenue = volume x fee / 1e9", "IDR bn", "={c:ch_vol}*{c:ch_price}/10^9", "Revenue — cargo handling", fmt="idr_bn", total=True, src="Calculation_FSL row 1116"),
    row("revenue", "Total revenue (land lease + flat storage + silo + cargo handling)", "IDR bn", "={c:ll_rev}+{c:fs_rev}+{c:silo_rev}+{c:ch_rev}", "Revenue — cargo handling",
        fmt="idr_bn", total=True, bold=True, src="Calculation_FSL row 1119"),
    # cost of sales
    row("wh_rev", "Warehouse revenue (flat storage + silo)", "IDR bn", "={c:fs_rev}+{c:silo_rev}", "Cost of sales", fmt="idr_bn", total=True, src="Calculation_FSL row 1142"),
    row("wh_cost", "Warehouse rental cost = warehouse revenue x %", "IDR bn", "={c:wh_rev}*{in:wh_cost_pct}", "Cost of sales", fmt="idr_bn", total=True, src="Calculation_FSL row 1144"),
    row("e1_cogs", "Teluk Lamong cost of sales excl. depreciation (E1 link)", "IDR bn", "={x:E1:cogs}", "Cost of sales", fmt="idr_bn", link=True, src="Calculation_FSL row 39"),
    row("e1_rev", "Teluk Lamong revenue (E1 link)", "IDR bn", "={x:E1:revenue}", "Cost of sales", fmt="idr_bn", link=True, src="Calculation_FSL row 38"),
    row("ch_cost_ratio", "Cargo handling cost ratio = E1 cost of sales / E1 revenue", "%", "=IFERROR({c:e1_cogs}/{c:e1_rev},0)", "Cost of sales", fmt="pct", src="Calculation_FSL row 1148"),
    row("ch_cost", "Cargo handling cost = cargo handling revenue x ratio", "IDR bn", "={c:ch_rev}*{c:ch_cost_ratio}", "Cost of sales", fmt="idr_bn", total=True, src="Calculation_FSL row 1149"),
    row("cogs", "Total cost of sales (excl. depreciation)", "IDR bn", "={c:wh_cost}+{c:ch_cost}", "Cost of sales", fmt="idr_bn", total=True, bold=True, src="Calculation_FSL row 1140"),
    # opex
    row("opex", "Operating expenses = total revenue x % x first-year factor", "IDR bn", "={c:revenue}*{in:opex_pct}*{in:first_year_factor}", "Operating expenses",
        fmt="idr_bn", total=True, bold=True, src="Calculation_FSL row 1159"),
]

SPEC = {
    "id": "P15",
    "code": "TBM",
    "name": "TBM — Tanjung Batu / Pelindo land lease, warehousing and cargo handling",
    "short": "TBM",
    "entity": "PT FKS Multi Agro / NPLOG (Pelindo land, Teluk Lamong area) — pipeline",
    "entity_short": "TBM (pipeline)",
    "category": "Pipeline (excluded by default)",
    "description": "Pipeline warehousing project on Pelindo land: flat storage and silo rental (stored tons per month x monthly fee, indexed), cargo handling on the stored volume, land sub-lease (no price in v29); warehouse cost 30% of warehouse revenue, cargo cost at the Teluk Lamong cost ratio, opex 18% of revenue; 40.0 USD m capex depreciated from 2027.",
    "v29": {"calc": "Calculation_FSL rows 1089-1159", "input": "Input rows 1128-1231", "standalone": "Output_Standalone (IDR) rows 482-503 (all nil: flag = 0)",
            "flag": "Output_FSL!F40 (= 0 — TBM excluded in v29)"},
    "v29_rows": {"rev": 484, "cogs": 485, "opex": 488, "da": 491, "fin": 494, "tax": 497, "np": 498},
    # the standalone block is zeroed by Output_FSL!F40 = 0 -> compare the Calculation_FSL rows (Output sheet signs: costs negative)
    "v29_calc_rows": {"rev": ("Calculation_FSL", 1119, 1), "cogs": ("Calculation_FSL", 1140, -1), "opex": ("Calculation_FSL", 1159, -1), "da": ("Calculation_FSL", 1121, -1)},
    "v29_known_diffs": {
        "da": "2027 only: v29 applies a typed half-year factor (Calculation_FSL!M1121 = SUM(...)*0.5 -> 18.72); the framework's capex module charges the full year (37.43). All other years match.",
    },
    "defaults": {"in_valuation": 0, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": ["E1"],
    "commissioning": {"year": 2027, "source": "Calculation_FSL!F1091 (Operation Period); depreciation flag Input!K1202:W1202 = 1 from 2027", "cls": "v29",
                      "note": "Depreciation and the land-lease index start in 2027; the priced revenue streams start in 2029 (separate input)."},
    "capex": {
        "total_usd": CAPEX_TOTAL, "source": "Input!M1186 (= 108 - 68 + Input!K1276: 40 USD m + legal fee 2 IDR bn / USD_IDR / 5 = 40.0246 USD m); Calculation_FSL!F1126",
        "pct": {2025: CAPEX_2025 / CAPEX_TOTAL, 2026: CAPEX_2026 / CAPEX_TOTAL},
        "pct_source": "v29 timing: Input!L1190 (FY2025 28.0172 USD m), M1190 (FY2026 12.0074 USD m) S-curve; Calculation_FSL row 1481 (x Output_FSL!F40 = 0 in v29)",
        "building_share": 0.9, "building_source": "Input!J1194 (building 90%; equipment Input!J1195 = 10%; land Input!J1193 = 0% / 90 yrs Input!J1197 -> no charge)",
        "life_b": 20, "life_e": 8, "lives_source": "Input!J1198 (20 yrs, labelled 'Equipment' in v29), J1199 (8 yrs)",
        "hist_confirmed": 0,
        "note": "Percentages apply to total capex; no pre-2024 spend. In v29 the cash flow is multiplied by Output_FSL!F40 = 0 (project excluded) while depreciation is still computed in Calculation_FSL row 1121 (x0.5 in 2027).",
    },
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": None},
}
