"""E4 WIN stevedoring (Cilegon, Makassar, Surabaya, Medan) — existing business block with four site sub-blocks.

v29: Calculation_FSL rows 729-1087 (Cilegon 729-843, Makassar 846-921, Surabaya 924-999, Medan 1001-1087), Input rows 695-1126,
     Output_Standalone (IDR) combined rows 459-480 (site blocks 367-457), flag Output_FSL!F39 (= 1). No project capex.
Effective v29 logic (scenario Input!G4 = 1 -> baseline rows; all values quoted are the effective ones):
  Revenue per site = sum over commodities of volume x ASP / 1e9, volume = FY2023 base x index (1 in 2023, then x (1 + growth) x flag):
    Cilegon  : corn 346,296 t / SBM 225,200 / soybean 295,847 / sugar 336,474 / wheat 923,727 (Input!J704..J756), growth 5% p.a. from FY2024
               (Input rows 699-751); ASPs Input rows 706-758 (FY2024 typed levels, then 2,575 / 3,605 / 2,607 IDR/t growing 3% to 2033, flat after)
    Makassar : sugar 276,000 t (Input!J849, 0% 2024 then 4%), wheat 80,000 t (Input!J862, 0%/4%); ASP sugar Input!K852:T852, wheat Input!K864:W864
    Surabaya : SBM 533,360 t (Input!J940, 0%/5%), soybean 214,500 t (Input!J953, 0%/5%); ASPs Input rows 942 / 955
    Medan    : SBM 771,624 t (Input!K1034), wheat 490,000 t (Input!K1060) from FY2024 (0%/5%); corn 100,000 t (Input!M1021) and soybean 200,000 t
               (Input!M1047) from FY2026 (Calculation_FSL!F1006 / F1016 = 2026; corn volume also x Medan operation period row 1003); ASPs rows 1023-1062
  Cost of sales (excl. depreciation; depreciation is reported in the D&A line of the standalone block):
    dock & port facilities fee: Cilegon = blended 85.1376% of total sales in FY2024 (Input!K767) + per-commodity proportions of commodity sales from
               FY2025 (Input!L769:W773: corn 35.12%, SBM 45.2%, soybean 35.28%, sugar 87.19% in 2025 then 35.28%, wheat 34.69%);
               Makassar 83.9036% (Calculation_FSL!F872), Surabaya 74.8766% (F950), Medan 48.8804% (F1038) of total sales
    employee cost: fixed FY2023 base x index 3.5% (Cilegon 2.5544, Makassar 0.80716, Surabaya 0.33450, Medan 0.25664)
    maintenance : Cilegon fixed 0.0085201 x index 1%; Makassar 0.110652% of sales (F883); Surabaya Input!K969:W969 = 0.000528% of sales;
                  Medan 0.004625% of sales (F1049)
    insurance   : Cilegon 0.0149747% of sales (F815); Makassar fixed 0.0044701 (Input!J876); Surabaya fixed 0.0026526 (Input!J971); Medan nil (F1054 empty)
  Opex: fixed G&A lines x index 1% p.a. (legal, travelling, audit, other admin, office; Makassar/Surabaya also utility; Medan also rental)
  Depreciation of existing assets (fixed p.a.): Cilegon 0.0434415 (Input!K777), Makassar 0.296297 (Input!J874), Surabaya 0.0833216 (Input!J965),
        Medan 0.01642 (Input!J1072) -> hook da_other
  Financing cost: none.
v29 source issues reproduced as effective behaviour (documented in the input notes):
  * Makassar sugar ASP FY2034-36: Calculation_FSL!T853:V853 reference the empty cells Input!U810:W810 (instead of Input!U852:W852 = 41,752.7),
    so Makassar sugar revenue is nil in 2034-36 (Total Sales drop from 28.9 to 13.0 IDR bn). Reproduced with a 0 tariff in 2034-36.
  * Surabaya audit-fee and utility G&A lines have an empty / zero base (Calculation_FSL!F983 empty, F998 = 0) and their growth references point to
    empty Input rows 980 / 1001 -> nil; kept as zero lines.
  * Medan insurance base Calculation_FSL!F1054 is empty -> nil insurance.
  * Cilegon insurance and Makassar/Surabaya insurance index rows (Calculation_FSL rows 813, 887, 965) are computed but not used.
  * Cilegon "Proportion" Calculation_FSL!F766 references Input!J650 (a Belawan growth row) and is not used.
"""
from .helpers import Y, const, annual, scalar, row, growth_index, fixed_cost, sum_rows

# ------------------------------------------------------------------------------------------------ v29 effective values
def series(vals):
    """13 values for 2024..2036 -> dict."""
    assert len(vals) == 13
    return dict(zip(Y, vals))


def step_flat(first, base, g, n_grow=9):
    """FY2024 typed level, then base x (1+g)^k for k = 0..n_grow-1 (FY2025-FY2033), flat thereafter (v29 ASP pattern)."""
    out = [first] + [base * (1 + g) ** k for k in range(n_grow)]
    out += [out[-1]] * (13 - len(out))
    return out


# Cilegon ASPs (Input rows 706/719/732/745/758, baseline rows 707/720/733/746/759 typed values)
CIL_CORN_P = [12328.621061691381, 2575, 2652.25, 2731.8175, 2813.772025, 2898.18518575, 2985.1307413225, 3074.684663562175, 3166.9252034690403,
              3261.9329595731115, 3261.9329595731115, 3261.9329595731115, 3261.9329595731115]
CIL_SBM_P = [57137.3691142518, 3605, 3713.15, 3824.5445, 3939.280835, 4057.45926005, 4179.1830378515, 4304.558528987045, 4433.695284856656,
             4566.706143402356, 4566.706143402356, 4566.706143402356, 4566.706143402356]
CIL_SOY_P = [4495.8039581760495] + CIL_CORN_P[1:]
CIL_SUGAR_P = [34880, 35926.4] + CIL_CORN_P[2:]
CIL_WHEAT_P = [13346.475053638678, 2606.9300000000003, 2685.1379, 2765.6920370000003, 2848.66279811, 2934.1226820533, 3022.146362514899,
               3112.810753390346, 3206.195075992056, 3302.3809282718175, 3302.3809282718175, 3302.3809282718175, 3302.3809282718175]
# Makassar
MAK_SUGAR_P = [32000.000000000007, 32960.00000000001, 33948.80000000001, 34967.26400000001, 36016.28192000001, 37096.770377600005,
               38209.673488928005, 39355.96369359585, 40536.64260440372, 41752.74188253583, 0, 0, 0]          # 2034-36 nil: v29 broken reference
MAK_WHEAT_P = [84400, 86932, 89539.96, 92226.1588, 94992.943564, 97842.73187092, 100778.0138270476, 103801.35424185902, 106915.3948691148,
               110122.85671518825, 110122.85671518825, 110122.85671518825, 110122.85671518825]
# Surabaya
SBY_SBM_P = [14625.411202416168, 15064.173538488652, 15516.098744643312, 15981.581706982612, 16461.02915819209, 16954.860032937853,
             17463.50583392599, 17987.411008943767, 18527.03333921208, 19082.844339388444, 19082.844339388444, 19082.844339388444, 19082.844339388444]
SBY_SOY_P = [6500.000000000002, 6695.000000000002, 6895.850000000002, 7102.725500000002, 7315.807265000002, 7535.281482950002, 7761.339927438502,
             7994.180125261657, 8234.005529019507, 8481.025694890091, 8481.025694890091, 8481.025694890091, 8481.025694890091]
# Medan
MDN_GRAIN_P = [16189.178284696094, 16674.853633236977, 17175.099242234086, 17690.35221950111, 18221.062786086142, 18767.694669668726,
               19330.725509758788, 19910.64727505155, 19910.64727505155, 19910.64727505155, 19910.64727505155]      # FY2026-FY2036
MDN_CORN_P = [0, 0] + MDN_GRAIN_P
MDN_SOY_P = [0, 0] + MDN_GRAIN_P
MDN_SBM_P = [14300.28815172633, 14729.29679627812, 15171.175700166465, 15626.310971171459, 16095.100300306602, 16577.9533093158,
             17075.291908595274, 17587.550665853134, 18115.17718582873, 18658.63250140359, 18658.63250140359, 18658.63250140359, 18658.63250140359]
MDN_WHEAT_P = [15259.853223391548, 15717.648820093294] + MDN_GRAIN_P

G_5_FROM_2024 = const(0.05)                 # Cilegon: 5% already in FY2024 (index 1.05 in 2024)
G_4_FROM_2025 = const(0.04, first=0.0)      # Makassar
G_5_FROM_2025 = const(0.05, first=0.0)      # Surabaya / Medan

# ------------------------------------------------------------------------------------------------ site definitions
# commodities: (key, label, base volume t, base source, growth values, growth source, price values, price source, start year or None)
SITES = {
    "cil": {
        "name": "Cilegon", "calc_rows": "Calculation_FSL rows 729-843", "std": "Output_Standalone (IDR) rows 367-388",
        "commodities": [
            ("corn", "Corn", 346296.036, "Input!J704 (= K704)", G_5_FROM_2024, "Input!K699:W699 (baseline row 700)", CIL_CORN_P, "Input!K706:W706 (baseline row 707)", None),
            ("sbm", "Soybean meal (SBM)", 225199.88000000003, "Input!J717 (= K717)", G_5_FROM_2024, "Input!K712:W712 (baseline row 713 = row 699)", CIL_SBM_P, "Input!K719:W719 (baseline row 720)", None),
            ("soy", "Soybean", 295847.011, "Input!J730 (= K730)", G_5_FROM_2024, "Input!K725:W725 (baseline row 726 = row 712)", CIL_SOY_P, "Input!K732:W732 (baseline row 733)", None),
            ("sugar", "Sugar", 336474.04000000004, "Input!J743 (= K743)", G_5_FROM_2024, "Input!K738:W738 (baseline row 739 = row 725)", CIL_SUGAR_P, "Input!K745:W745 (baseline row 746; FY2025 typed 35,926.4)", None),
            ("wheat", "Wheat", 923727.06, "Input!J756 (= K756)", G_5_FROM_2024, "Input!K751:W751 (baseline row 752 = row 738)", CIL_WHEAT_P, "Input!K758:W758 (baseline row 759)", None),
        ],
        "emp": (2.554436939, "Input!J787 (Calculation_FSL!F804)", 0.035, "Input!K782:W782 (baseline row 783)"),
        "dep": (0.04344148942, "Input!K777 (Calculation_FSL!F765; baseline row 778 'Actual Cost')"),
        "opex": [
            ("legal", "Legal and professional fees", 1.38451682168, "Input!J809 (Calculation_FSL!F822)", "Input!K804:W804"),
            ("travel", "Travelling and entertainment costs", 0.091772826, "Input!J816 (Calculation_FSL!F827)", "Input!K811:W811"),
            ("audit", "Audit fees", 0.09, "Input!J823 (Calculation_FSL!F832)", "Input!K818:W818"),
            ("other", "Other administrative expenses", 0.04422234244, "Input!J830 (Calculation_FSL!F837)", "Input!K825:W825"),
            ("office", "Office expenses", 0.011234156, "Input!J837 (Calculation_FSL!F842)", "Input!K832:W832"),
        ],
    },
    "mak": {
        "name": "Makassar", "calc_rows": "Calculation_FSL rows 846-921", "std": "Output_Standalone (IDR) rows 390-411",
        "commodities": [
            ("sugar", "Sugar", 276000, "Input!J849 (= K849)", G_4_FROM_2025, "Input!K844:W844 (baseline row 845; empty in FY2024 -> 0%)", MAK_SUGAR_P,
             "Calculation_FSL!J853:S853 = Input!K852:T852 (baseline row); T853:V853 = Input!U810:W810 (EMPTY) -> 0 in FY2034-36", None),
            ("wheat", "Wheat", 80000, "Input!J862 (= K862)", G_4_FROM_2025, "Input!K857:W857 (baseline row 858 = row 844)", MAK_WHEAT_P, "Input!K864:W864 (baseline row 865)", None),
        ],
        "emp": (0.80716489633, "Input!J884 (Calculation_FSL!F878)", 0.035, "Input!K879:W879 (baseline row 880)"),
        "dep": (0.29629731224, "Input!J874 (Calculation_FSL!F866)"),
        "opex": [
            ("legal", "Legal and professional fees", 0.041260886, "Input!J893 (Calculation_FSL!F895)", "Input!K888:W888"),
            ("travel", "Travelling and entertainment costs", 0.0175, "Input!J900 (Calculation_FSL!F900)", "Input!K895:W895"),
            ("audit", "Audit fees", 0.0305, "Input!J907 (Calculation_FSL!F905)", "Input!K902:W902"),
            ("other", "Other administrative expenses", 0.05032715733, "Input!J914 (Calculation_FSL!F910)", "Input!K909:W909"),
            ("office", "Office expenses", 0.00383204, "Input!J921 (Calculation_FSL!F915)", "Input!K916:W916"),
            ("utility", "Utility expenses", 0.006, "Input!J928 (Calculation_FSL!F920)", "Input!K923:W923"),
        ],
    },
    "sby": {
        "name": "Surabaya", "calc_rows": "Calculation_FSL rows 924-999", "std": "Output_Standalone (IDR) rows 413-434",
        "commodities": [
            ("sbm", "Soybean meal (SBM)", 533360.0000000001, "Input!J940 (= K940)", G_5_FROM_2025, "Input!K935:W935 (baseline row 936; empty in FY2024 -> 0%)", SBY_SBM_P, "Input!K942:W942 (baseline row 943)", None),
            ("soy", "Soybean", 214500, "Input!J953 (= K953)", G_5_FROM_2025, "Input!K948:W948 (baseline row 949 = row 935)", SBY_SOY_P, "Input!K955:W955 (baseline row 956)", None),
        ],
        "emp": (0.33450115961, "Input!J979 (Calculation_FSL!F956)", 0.035, "Input!K974:W974 (baseline row 975)"),
        "dep": (0.08332161371999999, "Input!J965 (Calculation_FSL!F944)"),
        "opex": [
            ("legal", "Legal and professional fees", 0.03800000001, "Input!J988 (Calculation_FSL!F973)", "Input!K983:W983"),
            ("travel", "Travelling and entertainment costs", 0.018822505, "Input!J995 (Calculation_FSL!F978)", "Input!K990:W990"),
            ("audit", "Audit fees", 0.0, "Calculation_FSL!F983 (EMPTY -> nil)", "Calculation_FSL row 982 -> Input!K980:W980 (empty row -> 0%)"),
            ("other", "Other administrative expenses", 0.01571300067, "Input!J1002 (Calculation_FSL!F988)", "Input!K997:W997"),
            ("office", "Office expenses", 0.0093992, "Input!J1009 (Calculation_FSL!F993)", "Input!K1004:W1004"),
            ("utility", "Utility expenses", 0.0, "Calculation_FSL!F998 (typed 0)", "Calculation_FSL row 997 -> Input!K1001:W1001 (empty row -> 0%)"),
        ],
    },
    "mdn": {
        "name": "Medan", "calc_rows": "Calculation_FSL rows 1001-1087", "std": "Output_Standalone (IDR) rows 436-457",
        "commodities": [
            ("corn", "Corn", 100000, "Input!M1021 (Calculation_FSL!F1007; FY2026 column)", G_5_FROM_2025, "Input!K1016:W1016 (baseline row 1017)", MDN_CORN_P, "Input!K1023:W1023 (baseline row 1024; empty before FY2026)", 2026),
            ("sbm", "Soybean meal (SBM)", 771624, "Input!K1034 (Calculation_FSL!F1012)", G_5_FROM_2025, "Input!K1029:W1029 (baseline row 1030 = row 1016)", MDN_SBM_P, "Input!K1036:W1036 (baseline row 1037)", None),
            ("soy", "Soybean", 200000, "Input!M1047 (Calculation_FSL!F1017; FY2026 column)", G_5_FROM_2025, "Input!K1042:W1042 (baseline row 1043 = row 1029)", MDN_SOY_P, "Input!K1049:W1049 (baseline row 1050; empty before FY2026)", 2026),
            ("wheat", "Wheat", 490000, "Input!K1060 (Calculation_FSL!F1022)", G_5_FROM_2025, "Input!K1055:W1055 (baseline row 1056 = row 1042)", MDN_WHEAT_P, "Input!K1062:W1062 (baseline row 1063)", None),
        ],
        "emp": (0.256643347, "Input!J1082 (Calculation_FSL!F1044)", 0.035, "Input!K1077:W1077 (baseline row 1078)"),
        "dep": (0.01641999997, "Input!J1072 (Calculation_FSL!F1032)"),
        "opex": [
            ("legal", "Legal and professional fees", 0.025705494, "Input!J1091 (Calculation_FSL!F1061)", "Input!K1086:W1086"),
            ("travel", "Travelling and entertainment costs", 0.206967525, "Input!J1098 (Calculation_FSL!F1066)", "Input!K1093:W1093"),
            ("audit", "Audit fees", 0.033630008, "Input!J1105 (Calculation_FSL!F1071)", "Input!K1100:W1100"),
            ("other", "Other administrative expenses", 0.09643942712999999, "Input!J1112 (Calculation_FSL!F1076)", "Input!K1107:W1107"),
            ("office", "Office expenses", 0.00165, "Input!J1119 (Calculation_FSL!F1081)", "Input!K1114:W1114"),
            ("rental", "Rental expenses", 0.0516, "Input!J1126 (Calculation_FSL!F1086)", "Input!K1121:W1121"),
        ],
    },
}

inputs, calc = [], []


def sec(site, part):
    return f"{SITES[site]['name']} — {part}"


# ------------------------------------------------------------------------------------------------ revenue (all sites)
for s, d in SITES.items():
    REV = sec(s, "revenue")
    name = d["name"]
    if s == "mdn":
        inputs.append(scalar("mdn_start", "Medan — operation period start (site operating flag)", "year", 2026, "Calculation_FSL!F1003", section=REV,
                             note="v29 multiplies the Medan corn volume by this operation-period flag (row 1003); SBM and wheat run from FY2024 regardless."))
        calc.append(row("mdn_opflag", "Medan — operation period flag (1 from the start year)", "flag", "=IF({y}>={in:mdn_start},1,0)*{flag}", REV, f0="=0", fmt="flag"))
    vol_keys, rev_keys = [], []
    for ck, clabel, base, base_src, growth, growth_src, prices, price_src, start in d["commodities"]:
        k = f"{s}_{ck}"
        vol_note = None
        if start:
            inputs.append(scalar(f"{k}_start", f"{name} — {clabel}: first year of volume", "year", start,
                                 f"Calculation_FSL!F{'1006' if ck == 'corn' else '1016'}", section=REV,
                                 note="Volume index = 0 before this year, 1 in this year, then grown; v29 cites the FY2026 column of the Input volume row."))
        inputs.append(scalar(f"{k}_base", f"{name} — {clabel}: base volume ({'FY2023' if not start else 'first operating year'})", "t", base, base_src, section=REV))
        inputs.append(annual(f"{k}_growth", f"{name} — {clabel}: volume growth", "%", growth, growth_src, section=REV))
        price_note = None
        if s == "mak" and ck == "sugar":
            price_note = ("v29 source issue: Calculation_FSL!T853:V853 (FY2034-36) reference the EMPTY cells Input!U810:W810 instead of Input!U852:W852 "
                          "(41,752.7 IDR/t), so Makassar sugar revenue is nil in FY2034-36. Reproduced with a 0 tariff; Input!U852:W852 hold 41,752.74.")
        elif start:
            price_note = "Empty in v29 before the first operating year (shown as 0)."
        inputs.append(annual(f"{k}_price", f"{name} — {clabel}: stevedoring tariff (ASP)", "IDR/t", series(prices), price_src, section=REV, note=price_note))
        if start:
            calc.append(row(f"{k}_idx", f"{name} — {clabel}: volume index (0 before the start year, 1.00 in the start year, then x (1 + growth))", "index",
                            f"=IF({{y}}<{{in:{k}_start}},0,IF({{y}}={{in:{k}_start}},1,{{c:{k}_idx@prev}}*(1+{{in:{k}_growth}})))*{{flag}}", REV, f0="=0", fmt="idx"))
        else:
            calc.append(growth_index(f"{k}_idx", f"{name} — {clabel}: volume index (1.00 in FY2023)", f"{k}_growth", REV))
        opf = "*{c:mdn_opflag}" if (s == "mdn" and ck == "corn") else ""
        calc.append(row(f"{k}_vol", f"{name} — {clabel}: volume = base x index" + (" x Medan operation flag" if opf else ""), "t",
                        f"={{in:{k}_base}}*{{c:{k}_idx}}{opf}", REV, fmt="tons", total=True))
        calc.append(row(f"{k}_price", f"{name} — {clabel}: tariff", "IDR/t", f"={{in:{k}_price}}", REV, fmt="idr_t"))
        calc.append(row(f"{k}_rev", f"{name} — {clabel}: revenue = volume x tariff / 1e9", "IDR bn", f"={{c:{k}_vol}}*{{c:{k}_price}}/10^9", REV, fmt="idr_bn", total=True))
        vol_keys.append(f"{k}_vol")
        rev_keys.append(f"{k}_rev")
    calc.append(sum_rows(f"{s}_volume", f"{name} — total volume", vol_keys, REV, unit="t", fmt="tons"))
    calc.append(sum_rows(f"{s}_revenue", f"{name} — total revenue", rev_keys, REV))

# ------------------------------------------------------------------------------------------------ cost of sales
# Cilegon: dock fee = blended % x total sales (FY2024) + per-commodity proportions x commodity sales (FY2025+)
COS = sec("cil", "cost of sales")
inputs += [
    annual("cil_dock_blend_pct", "Cilegon — dock & port facilities fee: blended % of total sales", "%", {y: (0.851375743347412 if y == 2024 else 0.0) for y in Y},
           "Input!K767:W767 (only K767 = 85.1376% is filled; L767:W767 empty -> 0)", section=COS, fmt="pct2",
           note="v29 Calculation_FSL row 774 = Input!K767 x total sales; from FY2025 the per-commodity proportions (row 776) take over."),
    annual("cil_dock_prop_corn", "Cilegon — dock fee proportion of corn sales", "%", {y: (0.0 if y == 2024 else 0.3512) for y in Y}, "Input!K769:W769 (K769 empty -> 0 in FY2024)", section=COS, fmt="pct2"),
    annual("cil_dock_prop_sbm", "Cilegon — dock fee proportion of SBM sales", "%", {y: (0.0 if y == 2024 else 0.452) for y in Y}, "Input!K770:W770 (K770 empty -> 0 in FY2024)", section=COS, fmt="pct2"),
    annual("cil_dock_prop_soy", "Cilegon — dock fee proportion of soybean sales", "%", {y: (0.0 if y == 2024 else 0.3528) for y in Y}, "Input!K771:W771 (K771 empty -> 0 in FY2024)", section=COS, fmt="pct2"),
    annual("cil_dock_prop_sugar", "Cilegon — dock fee proportion of sugar sales", "%", {y: (0.0 if y == 2024 else (0.8719036697247706 if y == 2025 else 0.3528)) for y in Y},
           "Input!K772:W772 (K772 empty -> 0 in FY2024; L772 = 87.19% typed for FY2025)", section=COS, fmt="pct2"),
    annual("cil_dock_prop_wheat", "Cilegon — dock fee proportion of wheat sales", "%", {y: (0.0 if y == 2024 else 0.3468984591070723) for y in Y}, "Input!K773:W773 (K773 empty -> 0 in FY2024)", section=COS, fmt="pct2"),
    scalar("cil_emp_base", "Cilegon — employee cost, base FY2023", "IDR bn", SITES["cil"]["emp"][0], SITES["cil"]["emp"][1], section=COS),
    annual("cil_emp_growth", "Cilegon — employee cost growth", "%", const(SITES["cil"]["emp"][2]), SITES["cil"]["emp"][3], section=COS),
    scalar("cil_maint_base", "Cilegon — maintenance, base FY2023 (fixed)", "IDR bn", 0.0085200651, "Input!J794 (Calculation_FSL!F809)", section=COS),
    annual("cil_maint_growth", "Cilegon — maintenance growth", "%", const(0.01), "Input!K789:W789 (baseline row 790)", section=COS),
    scalar("cil_ins_rate", "Cilegon — insurance, % of total sales (0.0149747%)", "%", 0.00014974683466982317, "Calculation_FSL!F815 (typed; = Input!K796:W796)", section=COS, fmt="pct2",
           note="v29 also builds an insurance index (row 813, growth Input!K796) that is not used."),
]
calc += [
    row("cil_dock_blend", "Cilegon — dock fee (blended) = blended % x total sales", "IDR bn", "={in:cil_dock_blend_pct}*{c:cil_revenue}", COS, fmt="idr_bn", total=True),
]
for ck in ["corn", "sbm", "soy", "sugar", "wheat"]:
    calc.append(row(f"cil_dock_{ck}", f"Cilegon — dock fee on {ck} sales = proportion x {ck} revenue", "IDR bn", f"={{in:cil_dock_prop_{ck}}}*{{c:cil_{ck}_rev}}", COS, fmt="idr_bn", total=True))
calc += [
    sum_rows("cil_dock", "Cilegon — dock & port facilities fee (blended + per commodity)", ["cil_dock_blend"] + [f"cil_dock_{c}" for c in ["corn", "sbm", "soy", "sugar", "wheat"]], COS),
]
calc += fixed_cost("cil_emp", "Cilegon — employee cost", "cil_emp_base", "cil_emp_growth", COS)
calc += fixed_cost("cil_maint", "Cilegon — maintenance (fixed)", "cil_maint_base", "cil_maint_growth", COS)
calc += [
    row("cil_ins", "Cilegon — insurance = rate x total sales", "IDR bn", "={in:cil_ins_rate}*{c:cil_revenue}", COS, fmt="idr_bn", total=True),
    sum_rows("cil_cogs", "Cilegon — total cost of sales (excl. depreciation)", ["cil_dock", "cil_emp", "cil_maint", "cil_ins"], COS),
]

# Makassar
COS = sec("mak", "cost of sales")
inputs += [
    scalar("mak_dock_pct", "Makassar — dock & port facilities fee, % of total sales", "%", 0.8390362840532454, "Calculation_FSL!F872 (typed; Input!J875 = 0.017999 'Sales' base not used)", section=COS, fmt="pct2"),
    scalar("mak_emp_base", "Makassar — employee cost, base FY2023", "IDR bn", SITES["mak"]["emp"][0], SITES["mak"]["emp"][1], section=COS),
    annual("mak_emp_growth", "Makassar — employee cost growth", "%", const(SITES["mak"]["emp"][2]), SITES["mak"]["emp"][3], section=COS),
    scalar("mak_maint_pct", "Makassar — maintenance, % of total sales (0.110652%)", "%", 0.0011065192600795278, "Calculation_FSL!F883 (typed)", section=COS, fmt="pct2"),
    scalar("mak_ins_base", "Makassar — insurance, fixed annual amount", "IDR bn", 0.004470121, "Input!J876 (Calculation_FSL!F888)", section=COS,
           note="v29 builds an index (row 887, growth Input!K912) but applies the flat base every year."),
]
calc += [
    row("mak_dock", "Makassar — dock & port facilities fee = % x total sales", "IDR bn", "={in:mak_dock_pct}*{c:mak_revenue}", COS, fmt="idr_bn", total=True),
]
calc += fixed_cost("mak_emp", "Makassar — employee cost", "mak_emp_base", "mak_emp_growth", COS)
calc += [
    row("mak_maint", "Makassar — maintenance = % x total sales", "IDR bn", "={in:mak_maint_pct}*{c:mak_revenue}", COS, fmt="idr_bn", total=True),
    row("mak_ins", "Makassar — insurance = fixed amount x flag", "IDR bn", "={in:mak_ins_base}*{flag}", COS, fmt="idr_bn", total=True),
    sum_rows("mak_cogs", "Makassar — total cost of sales (excl. depreciation)", ["mak_dock", "mak_emp", "mak_maint", "mak_ins"], COS),
]

# Surabaya
COS = sec("sby", "cost of sales")
inputs += [
    scalar("sby_dock_pct", "Surabaya — dock & port facilities fee, % of total sales", "%", 0.7487662332490136, "Calculation_FSL!F950 (typed)", section=COS, fmt="pct2"),
    scalar("sby_emp_base", "Surabaya — employee cost, base FY2023", "IDR bn", SITES["sby"]["emp"][0], SITES["sby"]["emp"][1], section=COS),
    annual("sby_emp_growth", "Surabaya — employee cost growth", "%", const(SITES["sby"]["emp"][2]), SITES["sby"]["emp"][3], section=COS),
    annual("sby_maint_pct", "Surabaya — maintenance, % of total sales (0.000528% p.a.)", "%", const(5.2761990118854e-06), "Input!K969:W969 (Calculation_FSL row 961; the typed 0.110652% in F961 is not used)", section=COS, fmt="pct2"),
    scalar("sby_ins_base", "Surabaya — insurance, fixed annual amount", "IDR bn", 0.002652611, "Input!J971 (Calculation_FSL!F966)", section=COS,
           note="v29 builds an index (row 965, growth Input!K990) but applies the flat base every year."),
]
calc += [
    row("sby_dock", "Surabaya — dock & port facilities fee = % x total sales", "IDR bn", "={in:sby_dock_pct}*{c:sby_revenue}", COS, fmt="idr_bn", total=True),
]
calc += fixed_cost("sby_emp", "Surabaya — employee cost", "sby_emp_base", "sby_emp_growth", COS)
calc += [
    row("sby_maint", "Surabaya — maintenance = % x total sales", "IDR bn", "={in:sby_maint_pct}*{c:sby_revenue}*{flag}", COS, fmt="idr_bn", total=True),
    row("sby_ins", "Surabaya — insurance = fixed amount x flag", "IDR bn", "={in:sby_ins_base}*{flag}", COS, fmt="idr_bn", total=True),
    sum_rows("sby_cogs", "Surabaya — total cost of sales (excl. depreciation)", ["sby_dock", "sby_emp", "sby_maint", "sby_ins"], COS),
]

# Medan
COS = sec("mdn", "cost of sales")
inputs += [
    scalar("mdn_dock_pct", "Medan — dock & port facilities fee, % of total sales", "%", 0.4888044237002548, "Calculation_FSL!F1038 (typed)", section=COS, fmt="pct2"),
    scalar("mdn_emp_base", "Medan — employee cost, base FY2023", "IDR bn", SITES["mdn"]["emp"][0], SITES["mdn"]["emp"][1], section=COS),
    annual("mdn_emp_growth", "Medan — employee cost growth", "%", const(SITES["mdn"]["emp"][2]), SITES["mdn"]["emp"][3], section=COS),
    scalar("mdn_maint_pct", "Medan — maintenance, % of total sales (0.004625%)", "%", 4.6250166566207664e-05, "Calculation_FSL!F1049 (typed)", section=COS, fmt="pct2"),
    scalar("mdn_ins_base", "Medan — insurance, fixed annual amount", "IDR bn", 0.0, "Calculation_FSL!F1054 (EMPTY -> nil)", section=COS,
           note="v29 source gap: the Medan insurance base cell is empty, so no insurance is charged (index row 1053 unused)."),
]
calc += [
    row("mdn_dock", "Medan — dock & port facilities fee = % x total sales", "IDR bn", "={in:mdn_dock_pct}*{c:mdn_revenue}", COS, fmt="idr_bn", total=True),
]
calc += fixed_cost("mdn_emp", "Medan — employee cost", "mdn_emp_base", "mdn_emp_growth", COS)
calc += [
    row("mdn_maint", "Medan — maintenance = % x total sales", "IDR bn", "={in:mdn_maint_pct}*{c:mdn_revenue}", COS, fmt="idr_bn", total=True),
    row("mdn_ins", "Medan — insurance = fixed amount x flag", "IDR bn", "={in:mdn_ins_base}*{flag}", COS, fmt="idr_bn", total=True),
    sum_rows("mdn_cogs", "Medan — total cost of sales (excl. depreciation)", ["mdn_dock", "mdn_emp", "mdn_maint", "mdn_ins"], COS),
]

# ------------------------------------------------------------------------------------------------ opex (G&A) and depreciation per site
for s, d in SITES.items():
    OPX = sec(s, "operating expenses (G&A)")
    name = d["name"]
    keys = []
    for ok, olabel, base, base_src, growth_src in d["opex"]:
        k = f"{s}_ga_{ok}"
        g = 0.0 if base == 0.0 and s == "sby" else 0.01
        note = None
        if base == 0.0:
            note = "v29 source gap: empty / zero base and a growth reference to an empty Input row -> nil line; kept for structure."
        inputs.append(scalar(f"{k}_base", f"{name} — {olabel}, base FY2023", "IDR bn", base, base_src, section=OPX, note=note))
        inputs.append(annual(f"{k}_growth", f"{name} — {olabel} growth", "%", const(g), growth_src, section=OPX))
        calc += fixed_cost(k, f"{name} — {olabel}", f"{k}_base", f"{k}_growth", OPX)
        keys.append(k)
    calc.append(sum_rows(f"{s}_opex", f"{name} — total operating expenses (G&A)", keys, OPX))

for s, d in SITES.items():
    DEP = sec(s, "depreciation of existing assets")
    name = d["name"]
    inputs.append(scalar(f"{s}_dep_base", f"{name} — depreciation of existing assets, annual charge", "IDR bn", d["dep"][0], d["dep"][1], section=DEP,
                         note="Fixed charge for the whole forecast in v29 (no net-book-value cap; 'Capex up to 2025' label)."))
    calc.append(row(f"{s}_dep", f"{name} — depreciation of existing assets = annual charge x flag", "IDR bn", f"={{in:{s}_dep_base}}*{{flag}}", DEP, fmt="idr_bn", total=True))

# ------------------------------------------------------------------------------------------------ combined
COMB = "WIN combined (four sites)"
calc += [
    sum_rows("volume", "WIN — total volume handled (all sites)", [f"{s}_volume" for s in SITES], COMB, unit="t", fmt="tons"),
    sum_rows("revenue", "WIN — total revenue (Cilegon + Makassar + Surabaya + Medan)", [f"{s}_revenue" for s in SITES], COMB),
    sum_rows("cogs", "WIN — total cost of sales excl. depreciation", [f"{s}_cogs" for s in SITES], COMB),
    sum_rows("opex", "WIN — total operating expenses (G&A)", [f"{s}_opex" for s in SITES], COMB),
    sum_rows("da_other", "WIN — depreciation of existing assets (all sites)", [f"{s}_dep" for s in SITES], COMB),
]

SPEC = {
    "id": "E4",
    "code": "WIN",
    "name": "WIN stevedoring (Cilegon, Makassar, Surabaya, Medan)",
    "short": "WIN stevedoring",
    "entity": "PT Wahana Insan Nusantara (WIN) — stevedoring at Cilegon, Makassar, Surabaya and Medan",
    "entity_short": "WIN",
    "category": "Existing business",
    "description": "Existing stevedoring business at four ports: per-commodity volume (FY2023 base x growth index) x stevedoring tariff; cost of sales = dock & port facilities fee (share of sales), employee cost, maintenance and insurance; fixed G&A lines; fixed depreciation of existing assets per site.",
    "v29": {"calc": "Calculation_FSL rows 729-1087 (Cilegon 729-843, Makassar 846-921, Surabaya 924-999, Medan 1001-1087)", "input": "Input rows 695-1126",
            "standalone": "Output_Standalone (IDR) rows 459-480 (combined; site blocks 367-457)", "flag": "Output_FSL!F39 (= 1)"},
    "v29_rows": {"rev": 461, "cogs": 462, "opex": 465, "da": 468, "fin": 471, "tax": 474, "np": 475, "ebit": 469},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": True,
    "depends": [],
    "commissioning": None,
    "capex": None,
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": "cogs", "opex": "opex", "da_other": "da_other"},
}
