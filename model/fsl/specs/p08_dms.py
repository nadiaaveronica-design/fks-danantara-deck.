"""P08 DMS trucking fee (Teluk Lamong, Cigading, Ciwandan, Belawan) — new project block with four sites.

v29: Calculation_FSL sub-blocks TTL rows 220-250, Cigading 474-503, Ciwandan 548-578, Belawan 697-727;
     Output_Standalone (IDR) sub-blocks 90-111 / 229-250 / 298-319 / 344-365, combined "Profit and Loss - DMS All" rows 505-526;
     flag Output_FSL!F36 (= 1). No Input-sheet rows: every driver is typed inside Calculation_FSL.
Effective v29 logic (per site; FKS earns a 2% service fee on the trucking cost of the site's volume and keeps 50% of it):
  Site flags     : TTL 2027 (F223), Cigading 2027 (F477), Ciwandan 2028 (F551), Belawan 2027 (F700)  [IF(year < start, 0, 1) x J$12]
  Volumes        : TTL      = Teluk Lamong total volume (Calculation_FSL rows 22 + 27 + 32 = E1 volume) - 300,000 t "IWF" (F222), x TTL flag   [rows 222, 227]
                   Cigading = 1,700,000 t (Calculation_FSL!$F$445, the typed KBS-warehouse volume) x Cigading existing volume index (row 255 = E2 index,
                              3% p.a. from 2025) x Cigading flag                                                                          [rows 480-481]
                              (row 476 "Total Cigading Volume" = SUM(J389, J284:J286) mixes capex and revenue rows and is NOT used)
                   Ciwandan = Ciwandan expansion volume (row 514 = P06 volume, 1.6 m t from 2028 growing 10% / 6%)                       [row 555]
                   Belawan  = Belawan existing-terminal volume (row 586 = E3 base volume, 750,000 t x index; the expansion volume of row 587
                              is NOT included) x Belawan flag                                                                            [rows 704, 707]
  Fee per ton    : trucking cost/t x service fee 2% (all four sites reference $F$483): TTL 20,000 (F228) -> 400; Cigading 84,000 (F482, labelled
                   "Ton/Month" but used as IDR/t) -> 1,680; Ciwandan 29,000 (F556) -> 580; Belawan 55,000 (F705) -> 1,100
  Gross revenue  : volume x fee / 1e9 (TTL and Belawan multiply by the site flag again; Cigading has the flag in the volume; Ciwandan has none)
  FKS revenue    : 50% of gross (F233; 1 - F486; 1 - F560; F710) -> Output_Standalone Net Sales rows 92, 231, 300, 346
  Cost of sales  : nil — rows 238, 492, 566, 715 = (empty cell F) x Calculation_FSL row 453 (KBS warehouse FKS revenue) = 0; Output rows 93/232/301/347 blank
  Opex           : 20% x FKS revenue (F239, F493, F567, F716)
  Depreciation   : equipment 0.04 / 0.04 / 0.03 / 0.04 USD m (F242, F496, F570, F719 typed as 40000/Million etc.) / 5 years (E242 ...) x USD_IDR / 1e9
                   = 0.13012 / 0.13012 / 0.09759 / 0.13012 IDR bn p.a., charged in every year from the site start to 2036
  Financing cost : none (row 517 blank); Tax = sum of the sub-blocks (framework taxes MAX(0, EBIT))

v29 source issues reproduced as effective behaviour (documented here, in input notes and in the company-level reconciliation):
  C08  The DMS equipment is depreciated (rows 244, 498, 572, 721) but NO capex appears in the v29 investment schedule (rows 1474-1481).
       -> `capex: None`; the depreciation is modelled in calc as equipment USD m x fx / 1000 / life x site flag and hooked to `da_other`.
  (a)  v29 never stops the charge after the 5-year life (10 years x 0.008 = 0.08 USD m charged on a 0.04 USD m asset). Reproduced (no NBV cap).
  (b)  The depreciation flag of TTL / Cigading / Belawan is the KBS-warehouse operation period (row 441 = 2027, `J$441`), not the site's own flag;
       Ciwandan uses row 441 x its own flag (row 551). Both start in the same years as the site flags, so the site flag reproduces the values.
  (c)  Equipment rows 247 / 501 / 724 point to Input!$J$1264 (Teluk Lamong silo capex, 3.7623 USD m) with proportion 0 (F248 = 100% - F243) -> nil;
       row 575 is empty. Nothing to reproduce (0), noted only.
  (d)  Belawan row 711 (J711) uses the gross revenue formula in 2024 and the FKS share (row 710) from 2025; effective 0 in 2024 because the flag is 0.
  (e)  Output_Standalone D&A of Ciwandan (row 307) references the sub-total row 569 while the other sites reference the building row (244/498/721);
       the values are identical because the equipment rows are nil.
"""
from .helpers import Y, const, annual, scalar, row, sum_rows

START, REV, COST, DEP = "Site start years", "Revenue drivers", "Cost drivers", "Depreciation of DMS equipment (no capex in v29 — source issue C08)"
SITES = [
    # key, name, start year, start cell, trucking cost/t, cost cell, fee row, FKS share cell, opex cell, equipment USD m, equipment cell, life cell
    ("ttl", "Teluk Lamong", 2027, "Calculation_FSL!F223", 20000, "Calculation_FSL!F228 (J228:V228 = $F228)", 229, "Calculation_FSL!F233 (Pelindo share F232 = 1 - F233)",
     "Calculation_FSL!F239", 0.04, "Calculation_FSL!F242 (= 40000/Million)", "Calculation_FSL!E242"),
    ("cig", "Cigading", 2027, "Calculation_FSL!F477", 84000, "Calculation_FSL!F482 (J482:V482 = $F$482; labelled 'Ton/Month' but applied as IDR/t)", 483,
     "Calculation_FSL!F487 (= 1 - F486 KBS portion 50%)", "Calculation_FSL!F493", 0.04, "Calculation_FSL!F496 (= 40000/Million)", "Calculation_FSL!E496"),
    ("ciw", "Ciwandan", 2028, "Calculation_FSL!F551", 29000, "Calculation_FSL!F556 (J556:V556 = $F$556)", 557, "Calculation_FSL!F561 (= 1 - F560 SOE share 50%)",
     "Calculation_FSL!F567", 0.03, "Calculation_FSL!F570 (= 30000/Million)", "Calculation_FSL!E570"),
    ("bel", "Belawan", 2027, "Calculation_FSL!F700", 55000, "Calculation_FSL!F705 (J705:V705 = $F705)", 706, "Calculation_FSL!F710 (Pelindo share F709 = 1 - F710)",
     "Calculation_FSL!F716", 0.04, "Calculation_FSL!F719 (= 40000/Million)", "Calculation_FSL!E719"),
]

inputs = []
for key, name, start, start_src, *_ in SITES:
    inputs.append(scalar(f"{key}_start", f"{name} — first operating year of the DMS trucking service", "year", start, start_src, section=START, fmt="year",
                         note=("v29 applies the flag to the volume (row 227) and again to the revenue (row 230)." if key == "ttl" else
                               "v29 applies the flag to the volume (row 481); the revenue row 484 carries no flag." if key == "cig" else
                               "v29 applies no site flag to the Ciwandan revenue (rows 555-562): the volume is nil before 2028 because the Ciwandan expansion (P06) starts in 2028. "
                               "The flag is used for depreciation (row 572)." if key == "ciw" else
                               "v29 applies the flag to the revenue (row 707); the volume row 704 (= E3 volume) is not flagged.")))
inputs += [
    scalar("ttl_iwf_deduct", "Teluk Lamong — volume not trucked by DMS ('IWF'), deducted from the terminal volume", "t", 300000,
           "Calculation_FSL!F222 (row 222 = rows 22 + 27 + 32 - $F$222)", section=REV,
           note="Rows 22 + 27 + 32 = Teluk Lamong meals + grains + additional grains volume = E1 total volume (linked in the calc sheet)."),
    scalar("cig_vol_base", "Cigading — base volume trucked (typed KBS-warehouse volume, before indexation)", "t", 1700000,
           "Calculation_FSL!$F$445 (= Calculation_SOEs!F369*0 + 1.7*Million), referenced by row 481", section=REV,
           note="v29 grows this base with the Cigading EXISTING terminal volume index (row 255 = E2 index, 3% p.a. from 2025), not with the KBS-warehouse index "
                "(row 444). Row 476 'Total Cigading Volume' = SUM(J389, J284:J286) sums a capex cell and revenue rows and is not used by the block."),
    scalar("service_fee", "DMS service fee — % of the trucking cost per ton earned as revenue (all four sites)", "%", 0.02,
           "Calculation_FSL!$F$483 (rows 229, 483, 557 and 706 all reference $F$483)", section=REV, fmt="pct2"),
]
for key, name, start, start_src, truck, truck_src, fee_row, share_src, *_ in SITES:
    inputs.append(annual(f"{key}_truck", f"{name} — trucking cost per ton (fee base)", "IDR/t", const(truck), truck_src, section=REV,
                         note=f"Fee per ton = trucking cost x service fee (Calculation_FSL row {fee_row})."))
    inputs.append(scalar(f"{key}_fks", f"{name} — FKS share of the DMS service fee (partner keeps the remainder)", "%", 0.5, share_src, section=REV))
inputs += [
    scalar("opex_pct", "Operating expenses — % of FKS revenue (all four sites)", "%", 0.20,
           "Calculation_FSL!F239, F493, F567, F716 (each typed 20%)", section=COST,
           note="Cost of sales is nil in v29: rows 238, 492, 566 and 715 multiply an empty cell (column F) by Calculation_FSL row 453 (KBS warehouse FKS revenue); "
                "Output_Standalone Cost of Sales rows 93 / 232 / 301 / 347 are blank. Not modelled."),
    scalar("dep_life", "Useful life of the DMS equipment", "years", 5, "Calculation_FSL!E242 (= E496 = E570 = E719)", section=DEP, fmt="int",
           note="v29 source issue: the annual charge (amount / 5) is applied in every year from the site start to 2036 and never stops after the 5-year life "
                "(no net-book-value cap); reproduced as effective behaviour."),
]
for key, name, start, start_src, truck, truck_src, fee_row, share_src, opex_src, equip, equip_src, life_src in SITES:
    inputs.append(scalar(f"{key}_equip_usd", f"{name} — DMS equipment depreciated by v29 (no capex cash flow — source issue C08)", "USD m", equip, equip_src,
                         section=DEP, fmt="num2",
                         note=("v29 source issue C08: depreciated in Calculation_FSL row "
                               + {"ttl": "244", "cig": "498", "ciw": "572", "bel": "721"}[key]
                               + " but absent from the v29 investment schedule (rows 1474-1481). The depreciation flag in v29 is the KBS-warehouse operation period "
                               "(row 441 = 2027)" + (" x the Ciwandan site flag (row 551 = 2028)" if key == "ciw" else "")
                               + "; the site flag reproduces the same values. Equipment row "
                               + {"ttl": "247", "cig": "501", "ciw": "575", "bel": "724"}[key]
                               + (" is empty" if key == "ciw" else " references Input!$J$1264 (Teluk Lamong silo capex 3.7623 USD m) with proportion 0") + " -> nil.")))

VOL_LINK = {
    "ttl": ("Teluk Lamong terminal volume — meals + grains + additional grains (link to E1; Calculation_FSL rows 22 + 27 + 32)", "={x:E1:volume}", "tons"),
    "cig": ("Cigading existing-terminal volume index (link to E2; Calculation_FSL row 255, 1.00 in FY2023)", "={x:E2:vol_index}", "idx"),
    "ciw": ("Ciwandan expansion volume (link to P06; Calculation_FSL row 514)", "={x:P06:volume}", "tons"),
    "bel": ("Belawan existing-terminal volume, excl. expansion (link to E3; Calculation_FSL row 586)", "={x:E3:base_vol}", "tons"),
}
VOL_F = {
    "ttl": ("Volume trucked = (terminal volume - IWF deduction) x site flag", "=({c:ttl_link}-{in:ttl_iwf_deduct})*{c:ttl_flag}"),
    "cig": ("Volume trucked = base volume x Cigading existing index x site flag", "={in:cig_vol_base}*{c:cig_link}*{c:cig_flag}"),
    "ciw": ("Volume trucked = Ciwandan expansion volume x site flag", "={c:ciw_link}*{c:ciw_flag}"),
    "bel": ("Volume trucked = Belawan existing volume x site flag", "={c:bel_link}*{c:bel_flag}"),
}

calc = []
for key, name, *_ in SITES:
    sec = f"{name} — DMS trucking"
    link_label, link_f, link_fmt = VOL_LINK[key]
    vol_label, vol_f = VOL_F[key]
    calc += [
        row(f"{key}_flag", f"{name} — site operating flag (1 from the site start year)", "flag", f"=IF({{y}}<{{in:{key}_start}},0,1)*{{flag}}", sec, f0="=0", fmt="flag"),
        row(f"{key}_link", f"{name} — {link_label}", "index" if link_fmt == "idx" else "t", link_f, sec, fmt=link_fmt, link=True),
        row(f"{key}_volume", f"{name} — {vol_label}", "t", vol_f, sec, fmt="tons", total=True),
        row(f"{key}_fee_t", f"{name} — fee per ton = trucking cost/t x service fee", "IDR/t", f"={{in:{key}_truck}}*{{in:service_fee}}", sec, fmt="idr_t"),
        row(f"{key}_rev_gross", f"{name} — gross service fee = volume x fee/t / 1e9", "IDR bn", f"={{c:{key}_volume}}*{{c:{key}_fee_t}}/10^9", sec, fmt="idr_bn2", total=True),
        row(f"{key}_revenue", f"{name} — FKS revenue = gross fee x FKS share", "IDR bn", f"={{c:{key}_rev_gross}}*{{in:{key}_fks}}", sec, fmt="idr_bn2", total=True, bold=True),
        row(f"{key}_opex", f"{name} — operating expenses = FKS revenue x %", "IDR bn", f"={{c:{key}_revenue}}*{{in:opex_pct}}", sec, fmt="idr_bn2", total=True),
        row(f"{key}_dep", f"{name} — depreciation of DMS equipment = USD m x fx / 1000 / life x site flag", "IDR bn",
            f"={{in:{key}_equip_usd}}*{{g:fx}}/1000/{{in:dep_life}}*{{c:{key}_flag}}", sec, fmt="idr_bn2", total=True,
            note="No capex cash flow in v29 (C08); the charge does not stop after the useful life, as in v29."),
    ]
TOT = "DMS total (four sites)"
calc += [
    sum_rows("volume", "Total volume trucked (four sites)", [f"{k}_volume" for k, *_ in SITES], TOT, unit="t", fmt="tons"),
    sum_rows("rev_gross", "Total gross DMS service fee (before partner shares)", [f"{k}_rev_gross" for k, *_ in SITES], TOT),
    sum_rows("revenue", "Total FKS revenue", [f"{k}_revenue" for k, *_ in SITES], TOT),
    sum_rows("opex", "Total operating expenses", [f"{k}_opex" for k, *_ in SITES], TOT),
    sum_rows("da_other", "Total depreciation of DMS equipment (no project capex)", [f"{k}_dep" for k, *_ in SITES], TOT),
]

SPEC = {
    "id": "P08",
    "code": "DMSTrucking",
    "name": "DMS trucking fee (Teluk Lamong, Cigading, Ciwandan, Belawan)",
    "short": "DMS trucking",
    "entity": "PT FKS Multi Agro / DMS trucking partnership with the port operators (Pelindo, KBS, SOE partner)",
    "entity_short": "DMS trucking",
    "category": "Planned project",
    "description": "Digital trucking management service at four terminals: FKS earns a 2% service fee on the trucking cost per ton of each terminal's volume and keeps 50% of the fee; opex 20% of FKS revenue; small equipment depreciated per site (no capex in v29).",
    "v29": {"calc": "Calculation_FSL rows 220-250 (TTL), 474-503 (Cigading), 548-578 (Ciwandan), 697-727 (Belawan)",
            "input": "none — all drivers typed in Calculation_FSL (Input!J1264 referenced with a 0% proportion)",
            "standalone": "Output_Standalone (IDR) rows 505-526 (DMS All; sub-blocks 90-111, 229-250, 298-319, 344-365)", "flag": "Output_FSL!F36 (= 1)"},
    "v29_rows": {"rev": 507, "cogs": 508, "opex": 511, "da": 514, "ebit": 515, "fin": 517, "tax": 520, "np": 521},
    "defaults": {"in_valuation": 1, "case": 1, "econ_interest": 1.0},
    "existing": False,
    "depends": ["E1", "E2", "E3", "P06"],
    "commissioning": {"year": 2027, "source": "Calculation_FSL!F223 (TTL), F477 (Cigading), F700 (Belawan); Ciwandan F551 = 2028", "cls": "v29",
                      "note": "First DMS revenue year (three sites in 2027; Ciwandan follows in 2028 — per-site start years are inputs below)."},
    "capex": None,
    "inputs": inputs,
    "calc": calc,
    "hooks": {"revenue": "revenue", "cogs": None, "opex": "opex", "da_other": "da_other"},
}
