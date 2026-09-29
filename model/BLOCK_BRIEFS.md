# Block briefs for spec extraction (read SPEC_GUIDE.md first)

Common: v29 `Output_Standalone (IDR)` block rows per line = Net Sales, Cost of Sales, Operating Expenses, D&A, EBIT, Financing Cost, Tax, Net Profit.
Column map: v29 `Calculation_FSL` / `Calculation_SOEs` I = 2023, J..V = 2024..2036; `Input` J = 2023, K..W = 2024..2036.
The harness compares rev / cogs / opex / da / ebit. Hooks must be positive amounts. Do not model working capital, project-capex depreciation
(framework) or v29 financing-cost rows.

## E3 — Belawan (incl. Belawan expansion, SGT3)  → `model/fsl/specs/e3_belawan.py`, id "E3", code "Belawan"
* v29: Calculation_FSL rows 580-695; Input rows 529-693; Output_Standalone (IDR) rows 321-342; flag Output_FSL!F37 (=1). `existing: True`, `econ_interest 1.0`.
* Revenue (rows 584-589): volume index (Input!K532:W532) x base Input!J537 (750,000 t) + additional expansion volume `Calculation_FSL!J587:V587`
  = `Calculation_SOEs!J450:V450` (typed 200,000 in 2027 rising to 550,000 in 2034, EMPTY in 2035-36 — v29 source gap; reproduce it as an annual
  input with 0 in 2035-36 and a note); price Input!K539:W539 (29,658 in 2024-25, 43,947.5 from 2026 ...). Check Output_Standalone!J323:V323.
* Cost of sales (row 593 = sum of rows 614,619,625,631,637,643,649,655,660,666,672): employee 3.27962 (3.5%), security 1.93018 (3.5%), fuel per ton
  (0.825696 / 922,782 t, 3%), utilities per ton (0.631021, 3%), concession fee = 55.1356% x revenue (row 636 — check the exact base), ops other per
  ton (0.41231, 3%), R&M per ton (0.286582, 3%), overtime per ton (0.245423, 3.5%), insurance = Input!K619 x existing depreciation (row 659),
  insurance on new assets (row 662-666: capex 14.0246 USD m x rate — check formula; row 665 shows 0), labour per ton (0.0116, 3.5%). Base volume 922,782 t (row 623).
* Depreciation (row 609 = 597 + 602 + 607): existing Input!K546:W546 (5.23397, 5.23397, 2.61699, then 0) + additions Input!K437?? (row 596 references
  Input!K437 — verify what it points to; values are 0) + NEW assets 14.0246 USD m: building 90% / 20 yrs, equipment 10% / 8 yrs from 2026 (row 582 Operation Period 2026).
  → `capex`: total 14.0246 (Input!K551:L551 = 7.02459 FY2026 + 7.0 FY2027; Calculation_FSL row 1480), pct {2026: 7.02459/14.0246, 2027: 7/14.0246},
  building_share 0.9 (Input!K556), lives 20/8 (Input!K559:K560), `commissioning_year: 2026` (Calculation_FSL!F582) — this key inside `capex` makes
  depreciation start in 2026 while the business itself is existing (operating flag = forecast flag).
* Opex (row 686 = sum 687-695): nine fixed G&A lines Input!J637:J645 grown at Input rows 649-690 (check each growth row reference in Calculation_FSL rows 676-684).
* D&A total in Output_Standalone row 330 = -Calculation_FSL!J609 (check whether G&A depreciation exists here; row 686 excludes nothing?). Verify with values.

## E4 — WIN stevedoring (Cilegon, Makassar, Surabaya, Medan)  → `e4_win.py`, id "E4", code "WIN"
* v29: Calculation_FSL rows 729-1087 (Cilegon 729-843, Makassar 846-921, Surabaya 924-999, Medan 1001-1087); Input rows 695-1126;
  Output_Standalone (IDR) combined rows 459-480 (sub-blocks 367-457); flag Output_FSL!F39 (=1). `existing: True`. No project capex (`capex: None`).
* Each site: revenue = sum over commodities of volume (base x growth index, some commodities start 2026 — e.g. Medan corn/soybean row 1006/1016 "2026")
  x ASP (Input rows); cost of sales = depreciation (existing, fixed per site), dock & port facilities fee (blended % of revenue or per-commodity
  proportions — Cilegon rows 769-800 use per-commodity proportions of sales; Makassar row 871-873 uses a blended %), employee, maintenance,
  insurance; opex = fixed G&A lines with growth. Mirror the v29 structure with sections per site ("Cilegon — revenue", ...).
* Known v29 issue: Makassar sugar tariff FY2034-36 references an empty row (Calculation_FSL!T853:V853 -> Input!U810:W810) so Makassar sugar revenue is
  nil in 2034-36. Reproduce the effective behaviour (tariff input row with 0 in 2034-36) and document it as a v29 source issue in `note`.
* Existing depreciation per site is in the D&A hook (`da_other`). Combine: hooks revenue/cogs/opex/da_other = sums over the four sites.
* Compare with the COMBINED rows 461 (rev), 462 (cogs), 465 (opex), 468 (da), 469 (ebit).

## P03 — KBS warehouse revitalisation (Cigading)  → `p03_kbsWarehouse.py`, id "P03", code "KBSWarehouse"
* v29: Calculation_FSL rows 438-472 (+ volume index from Calculation_SOEs rows 363-373); Input rows 1269-1273 (capex) and the typed drivers in
  Calculation_FSL (volume 1,700,000 t, handling/bagging 28,000 IDR/t?, weighing 7,000, storage 25,000 — check units and the formula of row 449;
  KBS revenue share 51% (F451) so FSL revenue = 49% (row 453)); Output_Standalone (IDR) rows 206-227; flag Output_FSL!F34 (=1). Commissioning 2027 (F441).
  Hmm: Calculation_SOEs row 365 says Operation Period 2026 — use what Calculation_FSL actually applies (check values of row 453 by year).
* Costs: cost of sales 10% of revenue (F457), opex 50% of revenue (F458) — check bases (FSL revenue or gross).
* Capex 6.02459 USD m in FY2026 (Input!M1270; Calculation_FSL row 1477), building 100%? — v29 depreciates NOTHING because Calculation_FSL!F461 points
  to the empty cell Input!L1270 (source issue C02). Set `capex` with building_share 1.0 (Calculation_FSL!F462), lives 20/10 (E461/E466), pct {2026: 1.0},
  and declare `"v29_known_diffs": {"da": "v29 depreciates nil on the 6.02 USD m warehouse capex (broken reference Calculation_FSL!F461 -> empty Input!L1270); the revised model depreciates it", "ebit": "follows from the D&A difference"}`.
  All other lines must MATCH.

## P04 — Teluk Lamong silo  → `p04_ttlSilo.py`, id "P04", code "TTLSilo"
* v29: Calculation_FSL rows 127-165; Input rows 1263-1267 (capex 3.7623 USD m FY2026 = Input!M1264; Calculation_FSL row 1478); Output_Standalone (IDR)
  rows 42-64; flag Output_FSL!F29 (=1). Commissioning 2027 (F129). `econ_interest 1.0` (v29 treats the silo as 100% FSL although it is an NPLOG asset — note it).
* Revenue bagging (rows 131-135): "# of silo 2 x 8,500 t/month" and price index 65,000 IDR/t/month? Check the actual formula of row 135 (value 132.6 total;
  13.26 per year 2027-2036 -> 2 x 8,500 x 12 x 65,000 / 1e9 = 13.26). Revenue WB (rows 139-143) is 0. Cost of sales row 147 = 300 IDR/t x volume? (Output row 45 = -Calculation_FSL!J62 x flag — CHECK: Output_Standalone!J45 references Calculation_FSL row 62 (Teluk Lamong security expense??). Reproduce exactly what the standalone block does and document oddities.)
  Opex: Output row 48 = Calculation_FSL!J147 (sign: check). D&A: rows 150-158: building 63% / 20 yrs, equipment 37% / 10 yrs (E151/E156, F152/F157) from 2027 -> capex building_share 0.63, lives 20/10.
* Cross-links: volume is typed (65,000 t index?) — expose as inputs.

## P05 — Dumai bagging & weighbridge  → `p05_dumai.py`, id "P05", code "Dumai"
* v29: Calculation_FSL rows 168-218; Input rows 1257-1261 (capex 6.80952 USD m FY2026 = Input!M1258, Calculation_FSL row 1474 x Output_FSL!F30);
  Output_Standalone (IDR) rows 66-87; flag Output_FSL!F30 (=1). Commissioning 2026 (F170).
* Output block: Net Sales = (row 176 bagging revenue + row 184 WB revenue) x flag; Cost of Sales = -row 188; Opex = -(row 210 insurance + row 217 operational cost);
  D&A = -row 191?? (check: J75 = -Calculation_FSL!J191 x flag — row 191 is a header "1. Depreciation - building assets"... verify what row 191 holds by
  year; depreciation rows are 194 and 199 (building 60% / 20 yrs, equipment 40% / 8 yrs; equipment stops after its life? check row 197 formula).
  Reproduce the effective standalone numbers; if the standalone block references a header row and therefore shows nil D&A while rows 194/199 compute
  depreciation, treat that as a v29 source issue: build the correct depreciation through `capex` and declare `v29_known_diffs` for da/ebit with the explanation.
* Insurance row 207-210: capex 6.80952 x USD_IDR x 0.00218362 (F209) x flag. Operational cost rows 212-217: % cost to revenue for loading and WB — expose as inputs.

## P06 — Ciwandan expansion  → `p06_ciwandan.py`, id "P06", code "Ciwandan"
* v29: Calculation_FSL rows 508-546 (revenue drivers in Calculation_SOEs rows 407-441: volume 1,900,000 t x index growing 10% then 6%? check row 412;
  price row 414; Calculation_FSL row 512-516 apply an FSL share 52.0159% (G512/G513) — verify the chain: Calculation_FSL!J516 revenue vs Calculation_SOEs!J415);
  Input rows 482-527 (capex Input!K499:W499 = 2.5123 in FY2026 and FY2027 -> total 5.02459 USD m, x Output_FSL!F38; Input!G492 = 2 selects the SECOND ASP row);
  Output_Standalone (IDR) rows 275-296; flag Output_FSL!F38 (=1). Commissioning 2028 (F510).
* Cost of sales (row 522): depreciation building 50% / 20 yrs + equipment 50% / 8 yrs (rows 523-531) + other cost of sales = proportion vs existing x sales
  (rows 533-536; proportion row 534 by year — expose as an annual input, cite Calculation_SOEs rows 432-435 / Input);
  Output block: Cost of Sales = -row 522 (includes depreciation? check) and D&A = -row 520 (check for double counting: rows 520 vs 522).
  Reproduce the standalone block exactly; document how v29 splits depreciation between the two lines.
* Opex (rows 538-542): proportion to revenue by year (row 539/540) x revenue.

## P08 — DMS trucking fee (Teluk Lamong, Cigading, Ciwandan, Belawan)  → `p08_dms.py`, id "P08", code "DMSTrucking"
* v29 sub-blocks: TTL rows 220-250 (Output_Standalone 90-111), Cigading 474-503 (229-250), Ciwandan 548-578 (298-319), Belawan 697-727 (344-365);
  combined "DMS All" rows 505-526; flag Output_FSL!F36 (=1). Commissioning: 2027 for TTL/Cigading/Belawan, 2028 for Ciwandan (per-site flags in calc).
  Use `commissioning: {"year": 2027}` for the project and model per-site operating flags in `calc` (site start years as scalar inputs).
* Revenue per site = site volume x trucking cost/t (20,000 / 84,000?? check units: Cigading row 482 "Cost Trucking 84,000 Ton/Month" and row 484 formula;
  Ciwandan 29,000; Belawan 55,000) x service fee 2% x FKS share 50%. Site volumes link to other projects:
  TTL = E1 total volume (rows 22+27+32) - 300,000 (F222 "IWF") -> `{x:E1:volume}` minus an input; Cigading = "Total Cigading Volume" row 476 (check formula:
  E2 volume + Wharf 2 volume + conveyor volume?) -> {x:E2:volume} + {x:P01:volume} + {x:P02:volume} as applicable; Ciwandan = {x:P06:volume};
  Belawan = {x:E3:volume} (+ additional). Add the IDs to `depends`. If the site volume in v29 is a typed number, expose it as an input instead.
* Cost of sales: 0 (rows 238 etc. multiply 0). Opex = 20% x FKS revenue. Depreciation: v29 depreciates 0.04 / 0.04 / 0.03 / 0.04 USD m over 5 years from each
  site's start (rows 244, 498, 572, 721) but NO capex appears in the v29 investment schedule (source issue C08). Set `capex: None` and model the per-site
  depreciation in `calc` (hook `da_other`), with the equipment amounts as USD m inputs x {g:fx}/1000 / 5 years x site flag; document C08 in notes.
* Compare with the combined rows 507 (rev), 508, 511, 514, 515.

## P12 — BUMN operatorship schemes (Pelindo Teluk Lamong, KBS Cigading, Pelindo Belawan)  → `p12_bumnOps.py`, id "P12", code "BUMNOps"
* v29: Calculation_FSL rows 1161-1445 ("Operatorship with Pelindo / KBS / Belawan / Ciwandan" + "FKS PART" rows 1404-1445); tariffs Sheet3!G6/G8;
  Output_Standalone (IDR) rows 183-204: Net Sales = SUM(Calculation_FSL row 1417, 1427, 1437) x flag (formulas exist from column L = 2026; 2024-25 blank);
  Cost of Sales blank; Opex = -row 1445 (= sum of rows 1418, 1429, 1439 "Cost"); no D&A; flag Output_FSL!F35 (=1). `defaults.case = 2` (With-BUMN case only), category "BUMN synergy".
* Economics: FSL's revenue per scheme = volume x (current-scheme tariff - new-scheme tariff) (F1409 = E1224-F1224 grains; F1414 meals; F1426 KBS; F1436 Belawan);
  FSL cost = revenue x (1 - EBIT margin) with margins 49% (F1420), 43% (F1431), 43% (F1441). Volumes: NPLOG grains = E1 grains + additional/2 (row 1215),
  meals = E1 meals + additional/2 (row 1239); KBS = E2 volume + ethanol + addition + Wharf 2 volume (row 1302: SUM(J256:J258, J361)); Belawan = E3 volume + additional (row 1363).
  Use {x:E1:...}, {x:E2:...}, {x:P01:volume}, {x:E3:...} and add depends. Expose the effective tariff differentials as inputs with the derivation cited
  (E1218:F1224, E1242:F1248, E1305:F1311, F1347:F1348 vs F1364:F1365), and add scalar calc rows showing the derivation where practical.
* The Ciwandan operatorship (rows 1377-1402) is NOT part of FKS PART / the standalone block — exclude it (mention in the docstring).
* Reproduce the 2026 start (formulas exist from column L) even though row 1163 says 2027 — use a "first revenue year" input = 2026 and note the inconsistency.

## P15 — TBM (Tanjung Batu / Pelindo land lease, warehousing, cargo handling)  → `p15_tbm.py`, id "P15", code "TBM"
* v29: Calculation_FSL rows 1089-1159; Input rows 1128-1231; Output_Standalone (IDR) rows 482-503 (ALL ZERO because Output_FSL!F40 = 0 — TBM excluded);
  so compare against Calculation_FSL directly with `"v29_calc_rows": {"rev": ("Calculation_FSL", 1119, 1), "cogs": ("Calculation_FSL", 1140, 1), "opex": ("Calculation_FSL", 1159, 1), "da": ("Calculation_FSL", 1121, 1)}`
  (EBIT cannot be compared — omit "ebit" from v29_rows). `defaults.in_valuation = 0`, category "Pipeline (excluded by default)".
* Revenue: land lease (area Input!K1133:W1133 x price 0 -> nil), flat storage (% of TTL meals volume rows 1100-1104 with typed overrides in 2027: M1100 0.49, M1102 = 1.6m/12;
  price 55,000 IDR/t/month x index), silo (rows 1106-1111; M1109 = 1m/12 typed), cargo handling (rows 1113-1116: volume = flat-storage annual volume x 12; price 15,000 x index).
  Reproduce the effective values (including the typed 2027 overrides) via inputs with notes. Links: {x:E1:meals_vol}, {x:E1:grains_vol} where v29 references rows 22/27.
* Depreciation (row 1121, x0.5 in 2027!): 40.0246 USD m (Input!M1186) x (land 0% / 90 yrs, building 90% / 20 yrs, equipment 10% / 8 yrs) x Input!K1202:W1202 flag (1 from 2027).
  Capex cash flow in v29 row 1481 = Input!K1190:W1190 S-curve (28.0172 FY2025, 12.0074 FY2026) x F40 (0). Use `capex` total 40.0246, pct {2025: 28.0172/40.0246, 2026: 12.0074/40.0246},
  building_share 0.9, lives 20/8, commissioning 2027. The 2027 half-year factor (x0.5 in M1121 and M1159) cannot be produced by the framework -> declare
  `v29_known_diffs` for da (2027 only) and explain; opex x0.5 in 2027 can be reproduced with an annual "first-year factor" input row (1.0 except 0.5 in 2027).
* Cost of sales: warehouse rental cost 30% of warehouse revenue (Input!K1207:W1207); cargo handling cost = TTL cost-of-sales ratio (row 1148 = E1 cogs / E1 revenue) x cargo revenue -> {x:E1:cogs}/{x:E1:revenue}.
  Opex: 18% of revenue (Input!K1215:W1215) x first-year factor.
