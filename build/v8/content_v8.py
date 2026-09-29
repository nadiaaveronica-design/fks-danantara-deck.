# -*- coding: utf-8 -*-
"""v8 slide content: one message per slide, detail in the speaker notes.
Face-of-slide text is deliberately short; sources, calculations and open items are carried over from v7 and extended."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v7'))
import content_v7 as C7

DATE = 'October 2026'

def _notes(prev, objective, talk, moved='', extra_validate=''):
    n = dict(prev)
    n['objective'] = objective
    n['talk'] = talk
    if moved:
        n['sources'] = 'DETAIL MOVED OFF THE SLIDE IN v8 (say it, do not show it): ' + moved + '\n\n' + prev['sources']
    if extra_validate:
        n['validate'] = prev['validate'] + '\n' + extra_validate
    return n

COVER = {
    'title': 'Building Indonesia’s food & feed logistics backbone',
    'sub1': 'Strategic investment discussion  |  FKS Group × Danantara Indonesia',
    'sub2': DATE + '  ·  Strictly private and confidential',
    'notes': C7.COVER['notes'],
}

# ---------------------------------------------------------------- SLIDE 2
S2 = {
    'title': '~22 Mt of imports a year, processed in a few corridors',
    'subtitle': 'The cargo is large and recurring; the mills that take it are concentrated',
    'col_labels': ['WHAT ARRIVES', 'PROCESSED BY', 'WHERE THE MILLS ARE'],
    'total': '~22 Mt',
    'total_sub': 'food & feed raw materials imported in 2024',
    'rows': [
        {'icon': 'icon_wheat.png', 'name': 'Wheat', 'mt': '11.7 Mt', 'to': 'Flour mills'},
        {'icon': 'icon_sbm.png', 'name': 'Soybean meal\nand other feed', 'mt': '8.0 Mt', 'to': 'Feed mills'},
        {'icon': 'icon_soy.png', 'name': 'Soybeans', 'mt': '2.6 Mt', 'to': 'Food industry'},
    ],
    'java': 'JAVA', 'sumatra': 'SUMATRA',
    'share1': ('~80%', 'of flour milling\ncapacity is on Java'),
    'share2': ('~70%', 'of feed output\nis on Java'),
    'others': 'Sumatra ~10–15%  ·  others ~10–15%',
    'takeaway': 'A few port corridors on Java and Sumatra carry most of the flow',
    'footnote': 'Imports 2024: FKS. Shares: FKS estimates from published mill capacities and feed-output data (USDA GAIN, APTINDO, GPMT).',
    'notes': _notes(C7.S2['notes'],
        'One question, answered visually: why does a large import market create a concentrated port-logistics opportunity? Left: what arrives (~22 Mt). Middle: who processes it (flour mills, feed mills, food processors). Right: where those mills are (Java first, Sumatra second). The audience should leave with “large, recurring, concentrated”.',
        'Indonesia imports about twenty-two million tonnes of food and feed raw materials every year: wheat for flour, soybean meal and other ingredients for animal feed, and soybeans for tempeh and tofu. That cargo is not spread around the archipelago. The flour mills and feed mills that take it sit in a few industrial corridors, most of them on Java, with Sumatra as the second cluster. Roughly four fifths of flour milling capacity and about seventy percent of feed output are on Java. So a small number of port corridors carry most of this flow, and that is where port logistics matters. We are not saying “X million tonnes go to Java”; we are saying the processing capacity is there, so the cargo follows.',
        'commodity sub-uses (wheat: flour, bread, noodles; soybean meal: poultry and livestock feed; soybeans: tempeh and tofu; other feed: DDGS, corn gluten, meat meal); the split of the 8.0 Mt feed line into soybean meal 6.2 Mt and other feed ingredients 1.8 Mt; the four milling clusters (North Sumatra, Banten-Jakarta, East Java, Makassar); mill counts (23 of 30 flour mills and 81 of 110 feed mills on Java); the source line (USDA GAIN 2026, APTINDO, GPMT).'),
}

# ---------------------------------------------------------------- SLIDE 3
S3 = {
    'title': 'At 6 of the 9 food & feed gateways, the ship still waits for the trucks',
    'subtitle': 'Most gateways that serve the mills still discharge by grab, hopper and truck',
    'hero_a': '6', 'hero_b': ' of 9',
    'hero_sub': 'relevant food & feed gateways in our screen still handle cargo conventionally',
    'legend': [('fks', 'FKS, mechanised'), ('conv', 'conventional')],
    'sites': [
        {'name': 'Belawan', 'lon': 98.69, 'lat': 3.78, 'kind': 'fks'},
        {'name': 'Cigading', 'lon': 105.96, 'lat': -5.93, 'kind': 'fks'},
        {'name': 'Teluk Lamong', 'lon': 112.68, 'lat': -7.19, 'kind': 'fks'},
        {'name': 'Tanjung Priok', 'lon': 106.88, 'lat': -6.10, 'kind': 'conv'},
        {'name': 'Ciwandan', 'lon': 106.02, 'lat': -6.01, 'kind': 'conv'},
        {'name': 'Panjang', 'lon': 105.32, 'lat': -5.47, 'kind': 'conv'},
        {'name': 'Tanjung Emas', 'lon': 110.42, 'lat': -6.95, 'kind': 'conv'},
        {'name': 'Tanjung Perak', 'lon': 112.73, 'lat': -7.20, 'kind': 'conv'},
        {'name': 'Makassar', 'lon': 119.41, 'lat': -5.13, 'kind': 'conv'},
    ],
    'flow_label': 'WHAT HAPPENS THERE TODAY',
    'captions': ['VESSEL', 'GRAB', 'HOPPER', 'TRUCKS', 'MILL'],
    'kpis': [('~5 kt/day', 'discharge rate'), ('~12 days', 'at berth per cargo'), ('Truck-paced', 'trucks set the pace')],
    'statement': 'Conventional handling ties marine productivity to truck availability',
    'footnote': 'FKS screen of gateways serving the food & feed mills; captive single-miller jetties excluded. 60 kt Panamax cargo at ~5 kt/day.',
    'notes': _notes(C7.S3['notes'],
        'Make the problem obvious in one look: most of the gateways that matter to this cargo still discharge by grab, hopper and truck, so the vessel is paced by the trucks. The hero number is 6 of 9 relevant gateways in the FKS screen, never “most ports in Indonesia”. The slide ends on the problem; slide 4 is the answer.',
        'We screened the gateways that actually serve the food and feed mills. Nine matter. Six of them still discharge the conventional way: a grab lifts the grain from the hold into a hopper, and the hopper fills trucks one by one. The vessel can only discharge as fast as the trucks arrive, about five thousand tonnes a day. A sixty-thousand-tonne Panamax cargo sits alongside for around twelve days. At an indicative Panamax time-charter value of about sixteen thousand dollars a day, that is close to two hundred thousand dollars of vessel time per cargo, before any demurrage. The three that work differently are the FKS gateways, which is the next slide.',
        'the landscape funnel (102 commercial ports, ~20 state-run dry-bulk gateways, 9 serving the food & feed mills, 636 ports in the national plan); the names of the six conventional gateways (Tanjung Priok, Ciwandan, Panjang, Tanjung Emas, Tanjung Perak, Makassar) are now only dots on the map; the ~US$194k indicative value of vessel time per 60 kt cargo (12 days x ~US$16.2k/day) and the ~200 vessel-days per 1 Mt a year scaling; the equation “discharge speed = truck availability”.'),
}

# ---------------------------------------------------------------- SLIDE 4
S4 = {
    'title': 'The FKS model: the ship no longer waits for the trucks',
    'subtitle': 'A transit warehouse separates the marine clock from the inland clock',
    'panel_label': 'FKS INTEGRATED GATEWAY',
    'captions': ['UNLOAD', 'TRANSFER', 'STORE', 'DISPATCH', 'DELIVER'],
    'warehouse_name': 'TRANSIT WAREHOUSE',
    'marine': 'MARINE CLOCK  ·  ~20 kt/day', 'inland': 'INLAND CLOCK', 'buffer': 'THE BUFFER',
    'outcomes': [('FASTER', 'discharge at full speed'), ('BETTER ECONOMICS', 'larger parcels, fewer calls'), ('MORE SECURE', 'enclosed and weighed')],
    'notes': _notes(C7.S4['notes'],
        'Sell the FKS operating model as one integrated physical system with the transit warehouse as the visual centre. One takeaway: the buffer separates the marine clock from the inland clock, so the ship no longer waits for the trucks. The three outcomes at the bottom set up slide 5; they are not quantified here.',
        'This is the same cargo handled the FKS way. Ship unloaders lift the grain out of the hold at around twenty thousand tonnes a day. It travels in an enclosed conveyor, weighed as it goes, into a transit warehouse on the quay. That warehouse is the buffer: it can absorb the whole cargo, so the vessel discharges at the unloader’s speed and sails in about three days. From the buffer, trucks and bagging lines load to the mill’s own schedule, and where a customer is next door, as at Cigading with the mills from 2026, a conveyor runs straight into the factory. Marine operations and inland logistics run on separate clocks. FKS’s scope covers the whole chain: unloading with the port operator, the conveyor, transit storage, controlled dispatch and delivery management, and the mill link where one exists. Three things follow: it is faster, the freight economics are better and the cargo is more secure. The next slide puts numbers on each.',
        'the rates on the marine bracket (~20 kt/day, ~3 days alongside per 60 kt); the inland-clock wording (trucks load to mill demand); the direct-to-mill bypass note (planned at Cigading, 2026); the FKS scope line (unloading with the port operator, enclosed conveyor, transit storage, controlled dispatch and delivery management, direct mill link where applicable).'),
}

# ---------------------------------------------------------------- SLIDE 5
S5 = {
    'title': 'What the model is worth per 60 kt cargo',
    'subtitle': 'Conventional versus FKS, one Panamax cargo of 60,000 tonnes',
    'panels': [
        {'head': 'FASTER', 'pic': 'ship', 'conv': ('~12 days', 'CONVENTIONAL'), 'fks': ('~3 days', 'FKS'),
         'hero': '~US$146k', 'hero_color': 'gold', 'hero_sub': 'indicative vessel-time value, ~9 days saved'},
        {'head': 'BETTER ECONOMICS', 'pic': 'parcels', 'conv': ('2 port calls', 'SMALLER PARCELS'), 'fks': ('1 port call', 'ONE PANAMAX'),
         'hero': 'US$XX', 'hero_color': 'grey', 'hero_sub': 'to be confirmed from FKS voyage data'},
        {'head': 'MORE SECURE', 'pic': 'enclosed', 'conv': ('0.2–0.3% loss', 'CARGO LOSS'), 'fks': ('~0.1% loss', 'ENCLOSED'),
         'hero': '~US$36k', 'hero_color': 'gold', 'hero_sub': 'cargo value preserved, illustrative'},
    ],
    'footnote': 'Indicative Panamax time-charter value ~US$16.2k per day (2024 benchmark), not a demurrage rate; cargo value ~US$300/t; loss rates indicative, to be validated.',
    'notes': _notes(C7.S5['notes'],
        'Turn the operating model into money on one intuitive unit, the 60 kt cargo, in three clean panels: conventional, FKS, value. The audience should retain ~US$146k of vessel time saved per cargo; that the freight saving is real but not yet quantified; and ~US$36k of cargo value preserved as an illustration. No formulas on the face; no total, because one component is still open.',
        'Take one sixty-thousand-tonne cargo. Faster: at a conventional berth it sits alongside for about twelve days; through the FKS system it is discharged in about three. Nine vessel-days at an indicative Panamax time-charter value of about sixteen thousand dollars a day is roughly a hundred and forty-six thousand dollars per cargo. Better economics: a deep berth takes a full Panamax parcel in one call instead of two smaller parcels; the freight saving is real, but we will quantify it from our own voyage data before we put a number in front of you. More secure: an enclosed, weighed chain loses less cargo. If the difference is two tenths of a percent on an eighteen-million-dollar cargo, that is about thirty-six thousand dollars, illustrative until we validate loss rates with customer weighbridge data. Only the two quantified items are on the slide; if asked for the sum, it is roughly a hundred and eighty thousand dollars per cargo before any freight saving, about three dollars a tonne.',
        'discharge rates (~5 vs ~20 kt/day); ~9 vessel-days saved; per-tonne equivalents (~US$2.4/t vessel time, ~US$0.6/t cargo value); the berth depths (−14 m, −21 m LWS); the deeper berth > larger parcel > fewer port calls > lower freight per tonne chain; the enclosed handling / fewer touchpoints / reconciled movements points; the combined ~US$182k per 60 kt (~US$3/t) before any freight saving and its link to the ~US$194k of vessel time on slide 3. FREIGHT SAVING SEARCH (v8): the attached FKS materials (v6 deck, v7 deck, Dumai tariff table, journey slide, template) contain no current-versus-to-be freight rate or per-tonne freight saving; v6 itself carried “US$ [ X ] / t”. No management estimate was therefore used; the panel shows US$XX until FKS voyage data supports a figure.'),
}

# ---------------------------------------------------------------- SLIDE 6
S6 = {
    'title': 'FKS already runs the model at three gateways',
    'subtitle': 'All three sit inside state-owned ports, run with Pelindo and Krakatau',
    'sites': [
        {'name': 'BELAWAN', 'mtpa': '~1 Mtpa', 'fact': 'Revitalised Pelindo warehouse and conveyor', 'photo': 'tl_bw2021.png'},
        {'name': 'CIGADING', 'mtpa': '~4 Mtpa', 'fact': '400 kt warehouse fed by conveyor, with Krakatau', 'photo': 'tl_cg2020.png'},
        {'name': 'TELUK LAMONG', 'mtpa': '~4 Mtpa', 'fact': '220 kt transit storage at the deep-water berth', 'photo': 'tl_tl2017.png'},
    ],
    'big': '~9 Mtpa', 'big_sub': 'of capacity across the three gateways, equivalent to ~40% of Indonesia’s core food & feed imports',
    'footnote': 'Source: FKS operating data.',
    'notes': _notes(C7.S6['notes'],
        'Credibility through the real assets: three large photographs, three capacities, one hero number (~9 Mt a year). The model on slides 4-5 is not a concept; it runs today inside Pelindo and Krakatau ports.',
        'None of this is theoretical. FKS has run the model at Teluk Lamong in Surabaya since 2017, at Cigading in Cilegon since 2020 and at Belawan in Medan since 2021, inside Pelindo and Krakatau ports. Belawan is a revitalised Pelindo warehouse and conveyor, about one million tonnes a year. Cigading is an integrated four-hundred-thousand-tonne warehouse fed by conveyor from the jetty, co-invested with Krakatau Bandar Samudera, about four million tonnes a year. Teluk Lamong has two hundred and twenty thousand tonnes of transit storage behind Pelindo’s deep-water berth, also about four million tonnes a year. Together that is about nine million tonnes a year of capacity, equivalent to roughly forty percent of the country’s core food and feed imports; actual throughput by site is in the feasibility model.',
        'city and partner lines (Medan · North Sumatra · Pelindo; Cilegon · Banten · Krakatau (KBS); Surabaya · East Java · Pelindo); partnership lines (operating partnership with Pelindo; co-invested with KBS, 30 + 20-year term; JV with anchor feed customers); the map with site markers (now on slides 3 and 8).',
        '6) Photographs on this slide are the 398 x 360 px images extracted from the v6 PDF; obtain high-resolution originals from FKS corporate communications before the meeting.'),
}

# ---------------------------------------------------------------- SLIDE 7
S7 = {
    'title': 'Built step by step since 2015',
    'subtitle': 'From one terminal in Surabaya to a network now being linked from berth to mill',
    'stages': [
        {'years': '2015–17', 'loc': 'Teluk Lamong', 'text': 'First transit warehouse and conveyor', 'photo': 'tl_tl2017.png'},
        {'years': '2019–20', 'loc': 'Cigading', 'text': 'Integrated warehouse fed from the jetty', 'photo': 'tl_cg2020.png'},
        {'years': '2020–21', 'loc': 'Belawan', 'text': 'Idle Pelindo warehouse back in service', 'photo': 'tl_bw2021.png'},
        {'years': '2024–26', 'loc': 'Berth to mill', 'text': 'Jetty 2 conveyor, bagging, mill conveyor (2026)', 'photo': 'tl_cg2026.png'},
        {'years': 'Next', 'loc': 'Expansion', 'text': 'Two site expansions, two new gateways', 'map': True},
    ],
    'notes': _notes(C7.S7['notes'],
        'A journey, not a project register: five steps left to right, each with a year, a place and one milestone. It should feel progressive and lead into the pipeline on slide 8.',
        'The platform was built step by step. It started at Teluk Lamong in 2015, with the first transit warehouse and conveyor at Pelindo’s new deep-water berth, in commercial operation from 2017. Cigading followed in 2019 and 2020, an integrated warehouse fed by conveyor from Jetty 1, co-invested with Krakatau Bandar Samudera. In 2020 and 2021 FKS took an idle Pelindo warehouse and conveyor at Belawan and had it back in service in about eleven months. From 2024 the chain is being linked further: a second jetty conveyor at Cigading, a bagging line at Teluk Lamong, and from 2026 a conveyor straight into the mills next to Cigading. The next step is expansion at the existing sites and two new gateways, which is the next slide.',
        'city lines (Surabaya · East Java; Cilegon · Banten; Medan · North Sumatra; Cigading · Teluk Lamong); the ~11-month Belawan turnaround; the “co-invested with KBS” and “Jetty 1 / Jetty 2” detail; the expansion figures (Cigading 4 → 6 Mtpa, Teluk Lamong 4 → 5 Mtpa, Ciwandan, Dumai) now on slide 8.'),
}

# ---------------------------------------------------------------- SLIDE 8
S8 = {
    'title': 'Next: two new gateways and two site expansions',
    'subtitle': 'Dumai for Riau’s palm-kernel exports; Ciwandan next door to Cigading',
    'cards': [
        {'name': 'DUMAI', 'place': 'Riau · with Pelindo', 'num': '~1.3 Mt', 'num_sub': 'of palm-kernel exports a year',
         'problem': 'Truck-to-vessel loading at ~1.7 kt per ship-day', 'fix': 'Pit, conveyor, ship loader and weighbridge',
         'lon': 101.45, 'lat': 1.68, 'ppic': 'truck', 'fpic': 'loader'},
        {'name': 'CIWANDAN', 'place': 'next to Cigading', 'num': '~1.2 Mt', 'num_sub': 'of wheat and soybean meal a year',
         'problem': 'Grab, hopper and truck at ~5 kt per ship-day', 'fix': 'Transit warehouse, conveyor and controlled dispatch',
         'lon': 106.02, 'lat': -6.01, 'ppic': 'grab', 'fpic': 'warehouse'},
    ],
    'labels': ('TODAY', 'WITH FKS'),
    'fks_sites': [(98.69, 3.78), (105.96, -5.93), (112.68, -7.19)],
    'expansions_label': 'EXISTING SITES',
    'expansions': 'Cigading 4 → 6 Mtpa   ·   Teluk Lamong 4 → 5 Mtpa',
    'footnote': 'Dumai: FKS–Pelindo cooperation document (scope and tariff); Ciwandan: FKS estimate. Capex and timing follow with the feasibility model.',
    'notes': _notes(C7.S8['notes'],
        'Two concrete next projects, each in two lines: the current problem and what FKS will improve. Dumai is export loading of palm-kernel products with Pelindo; Ciwandan replicates the Cigading import model next door. Existing-site expansions are the secondary strip. Nothing else on the face.',
        'Slide 3 said most relevant gateways still handle cargo conventionally. Here are the two projects FKS has identified: Ciwandan is one of those import gateways; Dumai is an adjacent opportunity outside that import screen, applying the same mechanised handling to export loading. Dumai is Riau’s main port for palm-kernel exports, about one point three million tonnes a year of expeller and shell. Today it is loaded truck to vessel at under two thousand tonnes a ship-day. With Pelindo, FKS would install a dumping pit, conveyor, ship loader and weighbridge, the same mechanised handling applied to export loading, under a cooperation agreement whose scope and tariff are already documented. Ciwandan sits next to Cigading in the Banten cluster and handles about one point two million tonnes of wheat and soybean meal a year by grab, hopper and truck. FKS would replicate the Cigading model there: a transit warehouse, a conveyor and controlled dispatch. Alongside those, the lowest-risk capital is expansion at the existing sites: Cigading from four to six million tonnes and Teluk Lamong from four to five.',
        'the WHY / TODAY / FKS PLAN / UNLOCKS rows; the Dumai tariff component (initial FKS component Rp40,000/t; Pelindo portion ~Rp65,000/t); ~2 Mt of dry bulk in total at Dumai; “agreement estimate, subject to anchor cargo”; the watchlist sites (Teluk Bayur, Makassar) and the four-symbol legend; the “lowest-risk capital: the sites are already in place” line.'),
}

# ---------------------------------------------------------------- SLIDE 9
S9 = {
    'title': 'Danantara can invest at the FSL platform level',
    'subtitle': 'Illustrative structure: FKS Multi Agro 51%, Danantara 49% of FSL',
    'today': 'TODAY', 'invests': 'DANANTARA INVESTS', 'after': 'AFTER INVESTMENT', 'illus': 'ILLUSTRATIVE  ·  SUBJECT TO NEGOTIATION',
    'parent': 'FKS Multi Agro', 'fsl': 'FSL', 'fsl_sub': 'FKS Solusi Logistik', 'danantara': 'Danantara Indonesia',
    'pct_today': '100%', 'pct_fks': '51%', 'pct_dan': '49%',
    'invest_text': 'capital injection and / or share acquisition',
    'operating_label': 'OPERATING PLATFORM', 'operating': ['Cigading', 'Teluk Lamong (JV)', 'Belawan'],
    'pipeline_label': 'PIPELINE', 'pipeline': ['Ciwandan', 'Dumai', 'Site expansions'],
    'notes': _notes(C7.S9['notes'],
        'A transaction structure that reads in five seconds: today FKS Multi Agro owns 100% of FSL; after an illustrative investment Danantara holds 49% alongside FKS Multi Agro at 51%; FSL carries the operating platform and the pipeline. Only one qualification on the face; the legal caveats, the fit with Pelindo and the next steps are in these notes.',
        'The proposed route for Danantara is a stake in FSL, FKS Solusi Logistik, the logistics platform. Today FSL is wholly owned by FKS Multi Agro. In the illustrative structure Danantara would take forty-nine percent, by capital injection into FSL, by acquiring shares from FKS Multi Agro, or a combination; that is for negotiation. Through FSL, Danantara gets exposure to the three operating gateways and to the pipeline: Ciwandan, Dumai and the site expansions. There is a natural fit: Pelindo, our port partner at four of the five sites, is a Danantara portfolio company, and concession governance will be addressed in the structure. Next steps are an NDA and data room, a feasibility model with project and equity returns and capex per project, and then valuation, stake size and use of proceeds.',
        'the platform note (illustrative asset and project entities under FSL; entities, JV shares and cooperation-agreement tenors to be confirmed); operating entity names (PT SGT, PT NPL · JV, PT SGTM); “Future port projects”; WHY THE FIT (Pelindo, FKS’s port partner at four of the five sites, is a Danantara portfolio company; concession governance to be addressed in the structure); NEXT STEPS (NDA and data room; feasibility model with project and equity returns and capex per project; valuation, stake size, new capital versus share purchase and use of proceeds to be agreed).'),
}

DISCLAIMER_NOTES = C7.DISCLAIMER_NOTES
