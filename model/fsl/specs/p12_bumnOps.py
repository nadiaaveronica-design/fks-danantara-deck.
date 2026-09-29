"""P12 BUMN operatorship schemes (Pelindo Teluk Lamong, KBS Cigading, Pelindo Belawan) — "FKS PART" block.

v29: Calculation_FSL rows 1161-1445 (scheme economics rows 1161-1375, FKS PART rows 1404-1445), tariffs Sheet3!G4/G6/G8,
     Output_Standalone (IDR) rows 183-204 ("Profit and Loss - Operatorship with BUMN"), flag Output_FSL!F35 (= 1).
     With-BUMN case only (defaults.case = 2), category "BUMN synergy". No capex, no depreciation, no cost of sales in v29.

Effective v29 logic (FKS PART):
  Under each operatorship scheme FKS takes over part of the port operator's stevedoring services. FSL's revenue per scheme is the
  volume handled x the tariff differential between the BUMN's CURRENT scheme tariff and the proposed NEW scheme tariff
  (the part of the tariff FKS now earns); FSL's cost is revenue x (1 - FSL EBIT margin).
  Start           : the standalone P&L formulas exist from column L = FY2026 (Output_Standalone (IDR)!L185:V185, L189:V189 and
                    Calculation_FSL!L1417:V1417 "Total Sales"); FY2024-25 are blank -> nil. Calculation_FSL!F1163 / F1275 show an
                    "Operation Period" of 2027 but those flags are NOT referenced by the FKS PART rows (v29 inconsistency, reproduced
                    through the commissioning / first-revenue-year input = 2026).
  1. NPLOG-Pelindo (Teluk Lamong)
     grains volume  : Calculation_FSL row 1215 = row 27 (E1 grains volume) + row 32 (additional TBM-linked grains, = 0 in v29) / 2
     meals volume   : row 1239 = row 22 (E1 meals volume) + row 32 / 2
     grains price   : F1409 = E1224 - F1224 = 78,259 - 61,039.53 = 17,219.47 IDR/t, where the new-scheme tariff for the ship unloader /
                      grabber / hopper and conveyor components = (Pelindo depreciation + overhead per ton for the FKS-funded 2 GSU /
                      conveyor, E1233:F1234) / (1 - 27% Pelindo EBIT margin); the other four components are unchanged
     meals price    : F1414 = E1248 - F1248 = 84,841 - 71,600.45 = 13,240.55 IDR/t (same construction, E1257:F1258)
     revenue        : rows 1410 + 1415 = volume x price / 1e9 (row 1417 from FY2026); cost row 1418 = revenue x (1 - 49%) (F1420)
  2. KBS (Cigading)
     volume         : row 1302 = SUM(rows 256:258, 361) = E2 Cigading existing volume + ethanol (row 257 = 0) + addition (row 258 = 0)
                      + P01 Wharf 2 volume
     price          : F1426 = E1311 - F1311 = 34,880 - 19,589.81 = 15,290.19 IDR/t; current scheme = dermaga 10,464 + ship unloader 24,416
                      (70% of 34,880); new-scheme ship-unloader tariff = (crane depreciation 2,377.46 + overhead 3,174.08) / (1 - 27%) x 120%
     revenue        : row 1427 = volume x price / 1e9; cost row 1429 = revenue x (1 - 43%) (F1431)
  3. Belawan (Pelindo)
     volume         : row 1363 = SUM(rows 586:587) = E3 Belawan volume + additional expansion volume
     price          : F1436 = (26,000 port + 29,000 ship unloader; Sheet3!G6, G8) - (26,000 + 12,910.74 new SU tariff, F1365) = 16,089.26 IDR/t
     revenue        : row 1437 = volume x price / 1e9; cost row 1439 = revenue x (1 - 43%) (F1441)
  Driver chain     : v29 computes each differential as a live formula of its components (F1409 = E1224 - F1224, F1414, F1426, F1436), so
                     here the COMPONENT inputs (current-scheme tariff parts, Pelindo / KBS depreciation + overhead per ton, 27% margin, KBS
                     120% uplift, Belawan new SU tariff) are the only drivers: scalar memo rows on the Calc sheet re-derive the four
                     differentials exactly as v29 does and the revenue rows read those memo rows. The four v29 differential values are
                     also carried as inputs, but purely as reconciliation references — each has a check row (derived - v29, must be nil)
                     and none of them drives revenue.
  Standalone P&L   : Net Sales (row 185) = SUM(rows 1417, 1427, 1437) from FY2026; Operating Expenses (row 189) = -row 1445
                    (= SUM(rows 1418, 1429, 1439)); Cost of Sales, D&A and Financing Cost blank; tax 22% on positive EBT.
  Excluded         : the "Operatorship with Ciwandan" rows 1377-1402 are not part of FKS PART / the standalone block (the Ciwandan
                    economics sit in the P06 block) and are not modelled here.

v29 source issues reproduced as effective behaviour:
  * Operation Period rows 1163 / 1275 say 2027, but the FKS PART P&L starts in FY2026 (column L) — first revenue year = 2026.
  * Rows 1427 / 1429 / 1437 / 1439 carry FY2024-25 values that never reach the standalone P&L (block starts at column L) — nil here.
  * The KBS ethanol / addition volumes (rows 257-258) are switched off by Calculation_FSL!D5 = 0 — exposed as zero inputs.
"""
from .helpers import Y, const, annual, scalar, row

TIM = "Scheme timing and volume allocation"
NPL = "Pelindo Teluk Lamong (NPLOG) — tariff differential (IDR/t)"
KBS = "KBS Cigading — tariff differential (IDR/t)"
BEL = "Pelindo Belawan — tariff differential (IDR/t)"
MRG = "FSL EBIT margins per scheme (cost = revenue x (1 - margin))"
VOLK = "KBS volume components (v29 rows 257-258, switched off)"

# ---------------------------------------------------------------- v29 tariff differentials, derived exactly as v29 does
# (Python-side derivation only feeds the *_diff reference inputs used by the check rows; the live drivers are the component inputs
#  below, re-derived on the Calc sheet in the memo rows that the revenue rows read.)
PEL_MARGIN = 0.27                                                    # Calculation_FSL!E1185 (-> E1236, E1261, E1297)
# NPLOG grains: current-scheme components E1218:E1223; FKS-funded cost items E1233:F1234 (stored negative in v29)
GR_CUR = [2526, 36303, 23777, 8421, 6935, 297]                       # dermaga, OPP/OPT, ship unloader/grabber/hopper, conveyor, throughput fee, dana sosial
GR_GSU_DEP, GR_GSU_OH = 3175.80717203884, 3091.01                    # E1233, F1233 (2 GSU units)
GR_CV_DEP, GR_CV_OH = 3572.78306854369, 1094.73                      # E1234, F1234 (conveyor)
GR_NEW_SU = (GR_GSU_DEP + GR_GSU_OH) / (GR_CUR[2] * (1 - PEL_MARGIN)) * GR_CUR[2]   # F1220 = -SUM(E1233:F1233)/G1220*E1220
GR_NEW_CV = (GR_CV_DEP + GR_CV_OH) / (GR_CUR[3] * (1 - PEL_MARGIN)) * GR_CUR[3]     # F1221
GR_NEW = GR_CUR[0] + GR_CUR[1] + GR_NEW_SU + GR_NEW_CV + GR_CUR[4] + GR_CUR[5]      # F1224
GR_DIFF = sum(GR_CUR) - GR_NEW                                                       # F1409 = E1224 - F1224 = 17,219.47
# NPLOG meals: E1242:E1247 (= F1191:F1196), cost items E1257:F1258
ML_CUR = [3705, 42588, 23245, 8232, 6780, 291]
ML_GSU_DEP, ML_GSU_OH = 4339.10564784449, 3021.85                    # E1257, F1257
ML_CV_DEP, ML_CV_OH = 4881.49385382505, 1070.16                      # E1258, F1258
ML_NEW_SU = (ML_GSU_DEP + ML_GSU_OH) / (ML_CUR[2] * (1 - PEL_MARGIN)) * ML_CUR[2]   # F1244
ML_NEW_CV = (ML_CV_DEP + ML_CV_OH) / (ML_CUR[3] * (1 - PEL_MARGIN)) * ML_CUR[3]     # F1245
ML_NEW = ML_CUR[0] + ML_CUR[1] + ML_NEW_SU + ML_NEW_CV + ML_CUR[4] + ML_CUR[5]      # F1248
ML_DIFF = sum(ML_CUR) - ML_NEW                                                       # F1414 = 13,240.55
# KBS: F1279 = 34,880 all-in tariff; ship unloader = 70% (F1283); crane depreciation E1320, overhead F1320 (= F1291); x120% (F1307)
KBS_ALL, KBS_SU_SHARE, KBS_UPLIFT = 34880, 0.70, 1.20
KBS_CRANE_DEP, KBS_OH = 2377.45698361021, 3174.08
KBS_SU_CUR = KBS_ALL * KBS_SU_SHARE                                                  # F1283 = 24,416
KBS_DERMAGA = KBS_ALL - KBS_SU_CUR                                                   # F1281 = 10,464
KBS_SU_NEW = (KBS_CRANE_DEP + KBS_OH) / (KBS_SU_CUR * (1 - PEL_MARGIN)) * KBS_SU_CUR * KBS_UPLIFT   # F1307 = 9,125.81
KBS_DIFF = (KBS_DERMAGA + KBS_SU_CUR) - (KBS_DERMAGA + KBS_SU_NEW)                   # F1426 = E1311 - F1311 = 15,290.19
# Belawan: Sheet3!G4 = 55,000 all-in, G8 = 29,000 ship unloader, G6 = G4 - G8 = 26,000 port; new SU tariff F1365 (typed)
BEL_ALL, BEL_SU_CUR, BEL_SU_NEW = 55000, 29000, 12910.73564857438
BEL_PORT = BEL_ALL - BEL_SU_CUR                                                      # Sheet3!G6 = F1347 = F1364 = 26,000
BEL_DIFF = (BEL_PORT + BEL_SU_CUR) - (BEL_PORT + BEL_SU_NEW)                         # F1436 = 16,089.26

inputs = [
    scalar("add_share", "Share of the additional (TBM-linked) grains volume of E1 allocated to each of grains and meals under the Pelindo scheme", "%", 0.5,
           "Calculation_FSL!J1215:V1215 and J1239:V1239 ('+ row 32 / 2')", section=TIM,
           note="Row 32 (additional grains) is nil in v29 (switch Calculation_FSL!D5 = 0), so this allocation has no effect on the v29 result."),
    # --- NPLOG grains
    scalar("gr_c1", "Grains — current-scheme tariff: 1. Dermaga", "IDR/t", GR_CUR[0], "Calculation_FSL!E1218 (= F1169)", section=NPL),
    scalar("gr_c2", "Grains — current-scheme tariff: 2. Biaya OPP/OPT", "IDR/t", GR_CUR[1], "Calculation_FSL!E1219 (= F1170)", section=NPL),
    scalar("gr_c3", "Grains — current-scheme tariff: 3. Ship unloader, grabber, hopper", "IDR/t", GR_CUR[2], "Calculation_FSL!E1220 (= F1171)", section=NPL),
    scalar("gr_c4", "Grains — current-scheme tariff: 4. Sewa conveyor", "IDR/t", GR_CUR[3], "Calculation_FSL!E1221 (= F1172)", section=NPL),
    scalar("gr_c5", "Grains — current-scheme tariff: 5. Throughput fee", "IDR/t", GR_CUR[4], "Calculation_FSL!E1222 (= F1173)", section=NPL),
    scalar("gr_c6", "Grains — current-scheme tariff: 6. Dana sosial & APBMI", "IDR/t", GR_CUR[5], "Calculation_FSL!E1223 (= F1174)", section=NPL),
    scalar("gr_gsu_dep", "Grains — Pelindo depreciation per ton recovered under the new scheme: 2 GSU units", "IDR/t", GR_GSU_DEP, "Calculation_FSL!E1233 (stored as -3,175.81)", section=NPL),
    scalar("gr_gsu_oh", "Grains — Pelindo overhead & others per ton recovered: 2 GSU units", "IDR/t", GR_GSU_OH, "Calculation_FSL!F1233 (stored as -3,091.01)", section=NPL),
    scalar("gr_cv_dep", "Grains — Pelindo depreciation per ton recovered: conveyor", "IDR/t", GR_CV_DEP, "Calculation_FSL!E1234 (stored as -3,572.78)", section=NPL),
    scalar("gr_cv_oh", "Grains — Pelindo overhead & others per ton recovered: conveyor", "IDR/t", GR_CV_OH, "Calculation_FSL!F1234 (stored as -1,094.73)", section=NPL),
    scalar("pel_margin", "Pelindo / KBS EBIT margin retained on the new-scheme tariff components (new tariff = cost per ton / (1 - margin))", "%", PEL_MARGIN,
           "Calculation_FSL!E1185 (-> E1236, E1261, E1297)", section=NPL),
    scalar("gr_diff", "Grains — v29 tariff differential (current scheme - new scheme), for reconciliation only (check)", "IDR/t", GR_DIFF,
           "Calculation_FSL!F1409 = E1224 - F1224 (78,259 - 61,039.53); derivation E1218:F1224 reproduced in the Calc memo rows", section=NPL,
           note="Reference value only — does NOT drive revenue. Revenue uses the Calc memo derivation from the components above; the check row (derived - v29) must be nil."),
    # --- NPLOG meals
    scalar("ml_c1", "Meals — current-scheme tariff: 1. Dermaga", "IDR/t", ML_CUR[0], "Calculation_FSL!E1242 (= F1191)", section=NPL),
    scalar("ml_c2", "Meals — current-scheme tariff: 2. Biaya OPP/OPT", "IDR/t", ML_CUR[1], "Calculation_FSL!E1243 (= F1192)", section=NPL),
    scalar("ml_c3", "Meals — current-scheme tariff: 3. Ship unloader, grabber, hopper", "IDR/t", ML_CUR[2], "Calculation_FSL!E1244 (= F1193)", section=NPL),
    scalar("ml_c4", "Meals — current-scheme tariff: 4. Sewa conveyor", "IDR/t", ML_CUR[3], "Calculation_FSL!E1245 (= F1194)", section=NPL),
    scalar("ml_c5", "Meals — current-scheme tariff: 5. Throughput fee", "IDR/t", ML_CUR[4], "Calculation_FSL!E1246 (= F1195)", section=NPL),
    scalar("ml_c6", "Meals — current-scheme tariff: 6. Dana sosial & APBMI", "IDR/t", ML_CUR[5], "Calculation_FSL!E1247 (= F1196)", section=NPL),
    scalar("ml_gsu_dep", "Meals — Pelindo depreciation per ton recovered under the new scheme: 2 GSU units", "IDR/t", ML_GSU_DEP, "Calculation_FSL!E1257 (stored as -4,339.11)", section=NPL),
    scalar("ml_gsu_oh", "Meals — Pelindo overhead & others per ton recovered: 2 GSU units", "IDR/t", ML_GSU_OH, "Calculation_FSL!F1257 (stored as -3,021.85)", section=NPL),
    scalar("ml_cv_dep", "Meals — Pelindo depreciation per ton recovered: conveyor", "IDR/t", ML_CV_DEP, "Calculation_FSL!E1258 (stored as -4,881.49)", section=NPL),
    scalar("ml_cv_oh", "Meals — Pelindo overhead & others per ton recovered: conveyor", "IDR/t", ML_CV_OH, "Calculation_FSL!F1258 (stored as -1,070.16)", section=NPL),
    scalar("ml_diff", "Meals — v29 tariff differential (current scheme - new scheme), for reconciliation only (check)", "IDR/t", ML_DIFF,
           "Calculation_FSL!F1414 = E1248 - F1248 (84,841 - 71,600.45); derivation E1242:F1248", section=NPL,
           note="Reference value only — does NOT drive revenue. Revenue uses the Calc memo derivation from the components above; the check row (derived - v29) must be nil."),
    # --- KBS
    scalar("kbs_all", "KBS — current all-in stevedoring tariff (grains)", "IDR/t", KBS_ALL, "Calculation_FSL!F1279 (Cigading existing FY2023 tariff)", section=KBS),
    scalar("kbs_su_share", "KBS — ship unloader / grabber / hopper share of the all-in tariff (balance = dermaga)", "%", KBS_SU_SHARE,
           "Calculation_FSL!F1283 = F1279 x 70%; F1281 = F1279 - F1283", section=KBS),
    scalar("kbs_crane_dep", "KBS — depreciation per ton recovered under the new scheme: crane", "IDR/t", KBS_CRANE_DEP, "Calculation_FSL!E1320 (stored as -2,377.46)", section=KBS),
    scalar("kbs_oh", "KBS — overhead & others per ton recovered", "IDR/t", KBS_OH, "Calculation_FSL!F1320 = F1315 = F1291 (stored as -3,174.08)", section=KBS),
    scalar("kbs_uplift", "KBS — uplift applied to the new-scheme ship-unloader tariff (x120%)", "x", KBS_UPLIFT, "Calculation_FSL!F1307 ('*120%' typed inside the formula)", section=KBS, fmt="num2"),
    scalar("kbs_diff", "KBS — v29 tariff differential (current scheme - new scheme), for reconciliation only (check)", "IDR/t", KBS_DIFF,
           "Calculation_FSL!F1426 = E1311 - F1311 (34,880 - 19,589.81); derivation E1305:F1311", section=KBS,
           note="Reference value only — does NOT drive revenue. Revenue uses the Calc memo derivation from the components above; the check row (derived - v29) must be nil."),
    # --- Belawan
    scalar("bel_all", "Belawan — current all-in stevedoring tariff (port + ship unloader)", "IDR/t", BEL_ALL, "Sheet3!G4", section=BEL),
    scalar("bel_su_cur", "Belawan — current ship unloader & hopper tariff", "IDR/t", BEL_SU_CUR, "Sheet3!G8 (-> Calculation_FSL!F1348)", section=BEL),
    scalar("bel_su_new", "Belawan — new-scheme ship unloader & hopper tariff (Pelindo share)", "IDR/t", BEL_SU_NEW, "Calculation_FSL!F1365 (typed 12,910.74)", section=BEL,
           note="Port operation tariff is unchanged under the new scheme (F1364 = F1347 = Sheet3!G6 = G4 - G8 = 26,000)."),
    scalar("bel_diff", "Belawan — v29 tariff differential (current scheme - new scheme), for reconciliation only (check)", "IDR/t", BEL_DIFF,
           "Calculation_FSL!F1436 = SUM(F1347:F1348) - SUM(F1364:F1365) (55,000 - 38,910.74); derivation F1347:F1348 vs F1364:F1365", section=BEL,
           note="Reference value only — does NOT drive revenue. Revenue uses the Calc memo derivation from the components above; the check row (derived - v29) must be nil."),
    # --- margins
    scalar("np_margin", "NPLOG-Pelindo scheme — FSL EBIT margin", "%", 0.49, "Calculation_FSL!F1420 (cost row 1418 = revenue x (1 - 49%), F1418 = 0.51)", section=MRG),
    scalar("kbs_margin", "KBS scheme — FSL EBIT margin", "%", 0.43, "Calculation_FSL!F1431 (cost row 1429 = revenue - EBIT)", section=MRG),
    scalar("bel_margin", "Belawan scheme — FSL EBIT margin", "%", 0.43, "Calculation_FSL!F1441 (cost row 1439 = revenue - EBIT)", section=MRG),
    # --- KBS volume components that v29 switches off
    annual("kbs_ethanol", "KBS — ethanol volume added to the Cigading volume", "t", const(0.0), "Calculation_FSL!J257:V257 (= 1,490,024.66 t x D5 from 2027, +3% p.a.; D5 = 0 -> nil)", section=VOLK,
           note="v29 switch Calculation_FSL!D5 = 0 zeroes this row; the base 1.49 m t in F257 is not used."),
    annual("kbs_addition", "KBS — additional volume added to the Cigading volume", "t", const(0.0), "Calculation_FSL!J258:V258 (= 300,000 t x D5 from 2028, +20% p.a.; D5 = 0 -> nil)", section=VOLK,
           note="v29 switch Calculation_FSL!D5 = 0 zeroes this row; the base 300,000 t in F258 is not used."),
]

MEMO_N = "Memo: tariff differential derivation — Pelindo Teluk Lamong (IDR/t, as v29 rows 1217-1248)"
MEMO_K = "Memo: tariff differential derivation — KBS Cigading (IDR/t, as v29 rows 1304-1311)"
MEMO_B = "Memo: tariff differential derivation — Pelindo Belawan (IDR/t, as v29 rows 1347-1365)"


def memo(key, label, f, section, unit="IDR/t", fmt="idr_t", bold=False):
    d = row(key, label, unit, f, section, fmt=fmt, bold=bold)
    d["kind"] = "scalar"
    return d


calc = [
    # ---- memo derivations (scalar rows)
    memo("m_gr_cur", "Grains — current-scheme tariff = sum of the six components", "={in:gr_c1}+{in:gr_c2}+{in:gr_c3}+{in:gr_c4}+{in:gr_c5}+{in:gr_c6}", MEMO_N),
    memo("m_gr_new_su", "Grains — new-scheme ship unloader tariff = (GSU depreciation + overhead) / (1 - Pelindo margin)", "=({in:gr_gsu_dep}+{in:gr_gsu_oh})/(1-{in:pel_margin})", MEMO_N),
    memo("m_gr_new_cv", "Grains — new-scheme conveyor tariff = (conveyor depreciation + overhead) / (1 - Pelindo margin)", "=({in:gr_cv_dep}+{in:gr_cv_oh})/(1-{in:pel_margin})", MEMO_N),
    memo("m_gr_new", "Grains — new-scheme tariff = unchanged components 1, 2, 5, 6 + new ship unloader + new conveyor", "={in:gr_c1}+{in:gr_c2}+{c:m_gr_new_su}+{c:m_gr_new_cv}+{in:gr_c5}+{in:gr_c6}", MEMO_N),
    memo("m_gr_diff", "Grains — derived differential = current - new — DRIVES REVENUE", "={c:m_gr_cur}-{c:m_gr_new}", MEMO_N, bold=True),
    memo("m_gr_chk", "Grains — check: derived differential - v29 reference input (must be nil)", "={c:m_gr_diff}-{in:gr_diff}", MEMO_N, fmt="num2"),
    memo("m_ml_cur", "Meals — current-scheme tariff = sum of the six components", "={in:ml_c1}+{in:ml_c2}+{in:ml_c3}+{in:ml_c4}+{in:ml_c5}+{in:ml_c6}", MEMO_N),
    memo("m_ml_new_su", "Meals — new-scheme ship unloader tariff = (GSU depreciation + overhead) / (1 - Pelindo margin)", "=({in:ml_gsu_dep}+{in:ml_gsu_oh})/(1-{in:pel_margin})", MEMO_N),
    memo("m_ml_new_cv", "Meals — new-scheme conveyor tariff = (conveyor depreciation + overhead) / (1 - Pelindo margin)", "=({in:ml_cv_dep}+{in:ml_cv_oh})/(1-{in:pel_margin})", MEMO_N),
    memo("m_ml_new", "Meals — new-scheme tariff = unchanged components 1, 2, 5, 6 + new ship unloader + new conveyor", "={in:ml_c1}+{in:ml_c2}+{c:m_ml_new_su}+{c:m_ml_new_cv}+{in:ml_c5}+{in:ml_c6}", MEMO_N),
    memo("m_ml_diff", "Meals — derived differential = current - new — DRIVES REVENUE", "={c:m_ml_cur}-{c:m_ml_new}", MEMO_N, bold=True),
    memo("m_ml_chk", "Meals — check: derived differential - v29 reference input (must be nil)", "={c:m_ml_diff}-{in:ml_diff}", MEMO_N, fmt="num2"),
    memo("m_kbs_su_cur", "KBS — current ship unloader tariff = all-in tariff x share", "={in:kbs_all}*{in:kbs_su_share}", MEMO_K),
    memo("m_kbs_dermaga", "KBS — dermaga tariff = all-in tariff - ship unloader (unchanged under the new scheme)", "={in:kbs_all}-{c:m_kbs_su_cur}", MEMO_K),
    memo("m_kbs_su_new", "KBS — new-scheme ship unloader tariff = (crane depreciation + overhead) / (1 - margin) x uplift", "=({in:kbs_crane_dep}+{in:kbs_oh})/(1-{in:pel_margin})*{in:kbs_uplift}", MEMO_K),
    memo("m_kbs_diff", "KBS — derived differential = (dermaga + current SU) - (dermaga + new SU) — DRIVES REVENUE", "=({c:m_kbs_dermaga}+{c:m_kbs_su_cur})-({c:m_kbs_dermaga}+{c:m_kbs_su_new})", MEMO_K, bold=True),
    memo("m_kbs_chk", "KBS — check: derived differential - v29 reference input (must be nil)", "={c:m_kbs_diff}-{in:kbs_diff}", MEMO_K, fmt="num2"),
    memo("m_bel_port", "Belawan — port operation tariff = all-in - ship unloader (unchanged under the new scheme)", "={in:bel_all}-{in:bel_su_cur}", MEMO_B),
    memo("m_bel_diff", "Belawan — derived differential = (port + current SU) - (port + new SU) — DRIVES REVENUE", "=({c:m_bel_port}+{in:bel_su_cur})-({c:m_bel_port}+{in:bel_su_new})", MEMO_B, bold=True),
    memo("m_bel_chk", "Belawan — check: derived differential - v29 reference input (must be nil)", "={c:m_bel_diff}-{in:bel_diff}", MEMO_B, fmt="num2"),
    # ---- volumes
    row("np_gr_vol", "NPLOG grains volume under the scheme = E1 grains volume + share x E1 additional grains volume, x operating flag", "t",
        "=({x:E1:grains_vol}+{x:E1:add_vol}*{in:add_share})*{c:opflag}", "Volumes handled under the schemes", fmt="tons", total=True, link=True,
        note="v29 Calculation_FSL row 1215 = row 27 + row 32 / 2"),
    row("np_ml_vol", "NPLOG meals volume under the scheme = E1 meals volume + share x E1 additional grains volume, x operating flag", "t",
        "=({x:E1:meals_vol}+{x:E1:add_vol}*{in:add_share})*{c:opflag}", "Volumes handled under the schemes", fmt="tons", total=True, link=True,
        note="v29 Calculation_FSL row 1239 = row 22 + row 32 / 2"),
    row("kbs_vol", "KBS volume under the scheme = E2 Cigading existing volume + ethanol + addition + P01 Wharf 2 volume, x operating flag", "t",
        "=({x:E2:volume}+{in:kbs_ethanol}+{in:kbs_addition}+{x:P01:volume})*{c:opflag}", "Volumes handled under the schemes", fmt="tons", total=True, link=True,
        note="v29 Calculation_FSL row 1302 = SUM(rows 256:258, 361)"),
    row("bel_vol", "Belawan volume under the scheme = E3 Belawan total volume (existing terminal + expansion), x operating flag", "t",
        "={x:E3:volume}*{c:opflag}", "Volumes handled under the schemes", fmt="tons", total=True, link=True,
        note="v29 Calculation_FSL row 1363 = SUM(rows 586:587); E3 'volume' = existing (row 586) + additional expansion (row 587)"),
    # ---- revenue
    row("np_gr_rev", "NPLOG grains revenue = volume x derived grains differential (memo row) / 1e9", "IDR bn", "={c:np_gr_vol}*{c:m_gr_diff}/10^9", "Revenue (FSL share of the scheme tariffs)", fmt="idr_bn", total=True),
    row("np_ml_rev", "NPLOG meals revenue = volume x derived meals differential (memo row) / 1e9", "IDR bn", "={c:np_ml_vol}*{c:m_ml_diff}/10^9", "Revenue (FSL share of the scheme tariffs)", fmt="idr_bn", total=True),
    row("np_rev", "NPLOG-Pelindo scheme revenue", "IDR bn", "={c:np_gr_rev}+{c:np_ml_rev}", "Revenue (FSL share of the scheme tariffs)", fmt="idr_bn", total=True, bold=True),
    row("kbs_rev", "KBS scheme revenue = volume x derived KBS differential (memo row) / 1e9", "IDR bn", "={c:kbs_vol}*{c:m_kbs_diff}/10^9", "Revenue (FSL share of the scheme tariffs)", fmt="idr_bn", total=True, bold=True),
    row("bel_rev", "Belawan scheme revenue = volume x derived Belawan differential (memo row) / 1e9", "IDR bn", "={c:bel_vol}*{c:m_bel_diff}/10^9", "Revenue (FSL share of the scheme tariffs)", fmt="idr_bn", total=True, bold=True),
    row("revenue", "Total revenue — BUMN operatorship schemes", "IDR bn", "={c:np_rev}+{c:kbs_rev}+{c:bel_rev}", "Revenue (FSL share of the scheme tariffs)", fmt="idr_bn", total=True, bold=True),
    # ---- cost
    row("np_cost", "NPLOG-Pelindo scheme cost = revenue x (1 - FSL EBIT margin)", "IDR bn", "={c:np_rev}*(1-{in:np_margin})", "Scheme operating cost (v29: Operating Expenses)", fmt="idr_bn", total=True),
    row("kbs_cost", "KBS scheme cost = revenue x (1 - FSL EBIT margin)", "IDR bn", "={c:kbs_rev}*(1-{in:kbs_margin})", "Scheme operating cost (v29: Operating Expenses)", fmt="idr_bn", total=True),
    row("bel_cost", "Belawan scheme cost = revenue x (1 - FSL EBIT margin)", "IDR bn", "={c:bel_rev}*(1-{in:bel_margin})", "Scheme operating cost (v29: Operating Expenses)", fmt="idr_bn", total=True),
    row("cost", "Total scheme operating cost (v29 Calculation_FSL row 1445 -> Operating Expenses)", "IDR bn", "={c:np_cost}+{c:kbs_cost}+{c:bel_cost}", "Scheme operating cost (v29: Operating Expenses)", fmt="idr_bn", total=True, bold=True),
    # ---- memo EBIT
    row("np_ebit", "Memo: NPLOG-Pelindo scheme EBIT = revenue - cost", "IDR bn", "={c:np_rev}-{c:np_cost}", "Memo: EBIT by scheme", fmt="idr_bn", total=True),
    row("kbs_ebit", "Memo: KBS scheme EBIT = revenue - cost", "IDR bn", "={c:kbs_rev}-{c:kbs_cost}", "Memo: EBIT by scheme", fmt="idr_bn", total=True),
    row("bel_ebit", "Memo: Belawan scheme EBIT = revenue - cost", "IDR bn", "={c:bel_rev}-{c:bel_cost}", "Memo: EBIT by scheme", fmt="idr_bn", total=True),
]

SPEC = {
    "id": "P12",
    "code": "BUMNOps",
    "name": "BUMN operatorship schemes (Pelindo Teluk Lamong, KBS Cigading, Pelindo Belawan)",
    "short": "BUMN operatorship",
    "entity": "PT FKS Sinar Logistik (FSL) with Pelindo (Teluk Lamong, Belawan) and KBS (Cigading)",
    "entity_short": "FSL / Pelindo / KBS",
    "category": "BUMN synergy",
    "description": "FKS takes over part of the BUMN port operators' stevedoring services: revenue = volume handled at each terminal x (current-scheme tariff - new-scheme tariff); cost = revenue x (1 - FSL EBIT margin). No capex or depreciation in v29.",
    "v29": {"calc": "Calculation_FSL rows 1161-1445 (FKS PART rows 1404-1445); tariffs Sheet3!G4, G6, G8", "input": "none (all drivers typed in Calculation_FSL)",
            "standalone": "Output_Standalone (IDR) rows 183-204", "flag": "Output_FSL!F35 (= 1)"},
    "v29_rows": {"rev": 185, "cogs": 186, "opex": 189, "da": 192, "ebit": 193, "fin": 195, "tax": 198, "np": 199},
    "defaults": {"in_valuation": 1, "case": 2, "econ_interest": 1.0},
    "existing": False,
    "depends": ["E1", "E2", "E3", "P01"],
    "commissioning": {"year": 2026, "source": "Output_Standalone (IDR)!L185 / L189 and Calculation_FSL!L1417 (formulas exist from column L = FY2026; FY2024-25 blank)", "cls": "v29",
                      "note": "First revenue year of the FKS PART P&L. v29 source issue: Calculation_FSL!F1163 / F1275 show an Operation Period of 2027, but those flags are not used by the FKS PART rows — the standalone P&L starts in FY2026."},
    "capex": None,
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": None, "opex": "cost", "da_other": None},
}
