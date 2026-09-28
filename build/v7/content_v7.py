# -*- coding: utf-8 -*-
"""All v7 slide content and speaker notes. FKS internal figures (from v6) take priority; conflicts with public data are flagged in notes."""

DATE = 'October 2026'

COVER = {
    'title': 'Building Indonesia’s food & feed logistics backbone',
    'sub1': 'Strategic investment discussion  |  FKS Group × Danantara Indonesia',
    'sub2': DATE + '  ·  Strictly private and confidential',
    'notes': {
        'objective': 'Open the discussion: FKS operates an integrated port-to-mill logistics platform for Indonesia’s food & feed supply chain and is inviting Danantara to invest in its growth.',
        'talk': 'FKS Group has imported and processed food and feed raw materials in Indonesia for decades. Since 2015 it has built a dedicated logistics layer at three gateways. Today we want to walk through why that layer matters for the country, what it delivers, where it goes next, and how Danantara could participate.',
        'sources': 'FKS template (FKS Food & Agri, ICON design, 16:9). Content per v6 deck and FKS Business Development.',
        'calc': 'None.',
        'validate': 'Confirm meeting date and presenting entity.',
    },
}

# ---------------------------------------------------------------- SLIDE 2
S2 = {
    'title': '~22 Mt of food & feed imports a year, concentrated in a few clusters',
    'subtitle': 'A limited number of port gateways therefore matter disproportionately',
    'total': '~22 Mt',
    'total_sub': 'of core food & feed raw materials imported (2024)',
    'rows': [
        {'icon': 'icon_wheat.png', 'name': 'Wheat', 'sub': 'flour, bread, noodles', 'mt': 11.7},
        {'icon': 'icon_sbm.png', 'name': 'Soybean meal', 'sub': 'poultry & livestock feed', 'mt': 6.2},
        {'icon': 'icon_soy.png', 'name': 'Soybeans', 'sub': 'tempeh & tofu', 'mt': 2.6},
        {'icon': 'icon_feed.png', 'name': 'Other feed', 'sub': 'DDGS, corn gluten, meat meal', 'mt': 1.8},
    ],
    'clusters': [  # lon, lat, weight, label
        {'name': 'NORTH SUMATRA', 'lon': 98.7, 'lat': 3.6, 'w': 0.10, 'dx': 0.2, 'dy': -0.09},
        {'name': 'BANTEN · JAKARTA', 'lon': 106.6, 'lat': -6.1, 'w': 0.45, 'dx': -1.42, 'dy': 0.16},
        {'name': 'EAST JAVA', 'lon': 112.7, 'lat': -7.2, 'w': 0.30, 'dx': 0.24, 'dy': -0.06},
        {'name': 'MAKASSAR', 'lon': 119.4, 'lat': -5.1, 'w': 0.08, 'dx': 0.16, 'dy': -0.09},
    ],
    'shares': [  # column, flour capacity, feed output
        ('JAVA', '~80%', '~70%'),
        ('SUMATRA', '~10%', '~15%'),
        ('OTHER ISLANDS', '~10%', '~15%'),
    ],
    'share_rows': ('of flour milling capacity', 'of animal feed output'),
    'share_other': 'Sumatra ~10-15%, other islands ~10-15%  ·  23 of 30 flour mills and 81 of 110 feed mills are on Java',
    'share_source': 'Shares are FKS estimates from published mill capacities (USDA GAIN 2026, APTINDO, GPMT)',
    'takeaway': 'A large import market and concentrated milling: a few port corridors on Java and Sumatra carry most of the flow',
    'notes': {
        'objective': 'Bridge the market size to its geography. The audience should leave with three linked ideas: the cargo base is large and structural (~22 Mt a year); it is milled by a concentrated set of flour and feed mills, mostly on Java; therefore a small number of port corridors carry most of the flow and the handling efficiency at those gateways matters disproportionately. This sets up slide 3.',
        'talk': 'Indonesia grows no wheat and produces almost no soybean meal, so the raw materials for bread, noodles, tempeh and animal feed arrive by sea every year, around twenty-two million tonnes of them. Wheat alone is close to twelve million tonnes, which makes Indonesia the largest or second-largest wheat importer in the world. That cargo is not spread evenly. Twenty-three of the thirty flour mills and eighty-one of the one hundred and ten feed mills are on Java, and because the largest mills are also on Java, roughly four-fifths of wheat milling capacity and about seventy percent of feed output sit there, in three corridors: Banten and Greater Jakarta, Central Java, and East Java. Sumatra, mainly Medan and Lampung, is the second concentration. So a handful of deep-water gateways carry most of the flow, and the way cargo is handled at those gateways sets the landed cost for the whole chain.',
        'sources': 'FKS INTERNAL (v6 deck, priority source): import volumes 2024 - wheat 11.7 Mt, soybean meal 6.2 Mt, soybeans 2.6 Mt, other feed ingredients (DDGS, corn gluten, meat meal) 1.8 Mt; total ~22.3 Mt. Mill counts: 23 of 30 flour mills and 81 of 110 feed mills on Java.\nPUBLIC CROSS-CHECK (FACT): wheat 11.71 Mt CY2024 (BPS via Katadata); soybean meal 5.43 Mt CY2024 (BPS via Kompas) versus 6.2 Mt in the FKS figure, which matches the USDA marketing-year basis (6.1-6.2 MMT MY2024/25, USDA Oilseeds circular) - CONFLICT of basis, not of substance, flagged here; soybeans 2.68 Mt CY2024 (BPS); DDGS 0.84-1.02 Mt (USDA GAIN ID2025-0030), MBM ~0.5 Mt (Tridge/UN Comtrade), corn gluten ~0.3 Mt (derived) = ~1.7-1.8 Mt other feed. USDA GAIN ID2026-0010 (Apr 2026): 31 flour mills, 14.8 Mt/yr installed grind capacity, 24 on Java, 5 on Sumatra, 2 on Sulawesi; 110 feed mills, 44 companies, 10 provinces, 81 on Java; GPMT installed feed capacity ~30-31 Mt/yr, output ~21.5 Mt (2025).\nDERIVED ESTIMATE - Java share of flour milling capacity ~80%: bottom-up sum of published mill capacities (Bogasari Jakarta 11,600 t/d, Surabaya 6,000, Cibitung 2,600, Tangerang 500; Bungasari Cilegon 2,600; Harvestar Gresik 2,200; Sriboga Semarang 1,850; Cerestar Cilegon 1,500; Manunggal Cilacap 1,200; Wilmar Gresik, Fugui Gresik and Pundi Kencana ~1,000 each; Golden Grand 600; small Sidoarjo and Tangerang mills) = ~34,700 t/d on Java versus ~3,400-4,500 t/d on Sumatra (Bungasari Medan 1,500, Cerestar Medan 500, Agri First 370, Wilmar Dumai ~1,000 unverified) and ~2,850-3,400 t/d on Sulawesi (Eastern Pearl, Bungasari Makassar); total ~41-43k t/d reconciles with USDA’s 14.8 Mt/yr. Java 81-85%, Sumatra 8-11%, other 7-8%: shown as ~80 / ~10 / ~10.\nDERIVED ESTIMATE - Java share of feed output ~70%: triangulated from mill location (81/110 = 74%), broiler population (Java 62.9%, BPS 2024), layer population (East and Central Java 46%, BPS 2024) and Lampung installed capacity (1.96 Mt/yr, Disnak Lampung) with the Medan cluster ~1 Mt/yr named capacity; range Java 65-74%, Sumatra 12-20%, other 8-15%: shown as ~70 / ~15 / ~15. Feed is produced close to the poultry belts, so mill location is a strong proxy for where imported soybean meal is discharged.\nPROXY - Map halos are sized by approximate share of flour and feed milling capacity in each cluster (Greater Jakarta and Banten ~50% of flour capacity, East Java ~26%, Central Java ~7%, Makassar ~7%, Medan ~6%, Lampung feed cluster ~6.5% of feed capacity).\nMill count is not mill capacity and neither is import tonnage; the slide therefore shows capacity and output shares, with counts only in this note.',
        'calc': '~22 Mt = 11.7 + 6.2 + 2.6 + 1.8 = 22.3 Mt (FKS basis, 2024). Excludes raw sugar (~4-5 Mt/yr), corn (~1.4 Mt in 2024, ~0.5 Mt in 2025 under the self-sufficiency policy) and rice (bagged). Island shares as derived above; rounding to the nearest 5-10 points is deliberate.',
        'validate': '1) Confirm the FKS import basis for soybean meal (6.2 Mt is a marketing-year figure; BPS calendar 2024 is 5.43 Mt) and decide which to present. 2) Replace the derived island shares with APTINDO and GPMT capacity-by-province tables if FKS can obtain them (GPMT member decks carry a provincial table). 3) Confirm FKS’s own share of national wheat and soybean-meal imports if it can be disclosed. 4) Confirm the corn treatment (excluded here; policy-limited since 2025).',
    },
}

# ---------------------------------------------------------------- SLIDE 3
S3 = {
    'title': 'Indonesia already has the cargo; the bottleneck is at the port',
    'subtitle': 'Six of the nine food & feed gateways still discharge at the speed of the trucks',
    'tiles': [
        ('102', 'commercial ports'),
        ('~20', 'state-run dry-bulk gateways'),
        ('9', 'serve the food & feed mills'),
        ('6', 'still handle cargo conventionally'),
    ],
    'tile_note': 'The other three are FKS gateways',
    'list_fks': ('FKS GATEWAYS · MECHANISED', 'Belawan  ·  Cigading  ·  Teluk Lamong'),
    'list_conv': ('CONVENTIONAL · COMMON-USER', 'Tanjung Priok  ·  Ciwandan  ·  Panjang  ·  Tanjung Emas  ·  Tanjung Perak  ·  Makassar'),
    'list_note': 'FKS screen of public data; captive single-miller jetties excluded; classification to be confirmed',
    'gateways': [  # name, lon, lat, kind (fks|conv), label offsets
        {'name': 'Belawan', 'lon': 98.69, 'lat': 3.78, 'kind': 'fks', 'dx': 0.12, 'dy': -0.13},
        {'name': 'Cigading', 'lon': 105.96, 'lat': -5.93, 'kind': 'fks', 'dx': -0.72, 'dy': -0.2},
        {'name': 'Teluk Lamong', 'lon': 112.68, 'lat': -7.19, 'kind': 'fks', 'dx': 0.12, 'dy': 0.04},
        {'name': 'Tanjung Priok', 'lon': 106.88, 'lat': -6.1, 'kind': 'conv', 'dx': 0.1, 'dy': -0.17},
        {'name': 'Ciwandan', 'lon': 106.02, 'lat': -6.01, 'kind': 'conv', 'dx': -0.75, 'dy': 0.02},
        {'name': 'Panjang', 'lon': 105.32, 'lat': -5.46, 'kind': 'conv', 'dx': -0.62, 'dy': -0.2},
        {'name': 'Semarang', 'lon': 110.42, 'lat': -6.95, 'kind': 'conv', 'dx': -0.25, 'dy': 0.06},
        {'name': 'Tanjung Perak', 'lon': 112.73, 'lat': -7.2, 'kind': 'conv', 'dx': 0.12, 'dy': -0.17},
        {'name': 'Makassar', 'lon': 119.41, 'lat': -5.13, 'kind': 'conv', 'dx': 0.12, 'dy': -0.1},
    ],
    'flow_caption': 'Discharge speed = truck availability',
    'consequences': [
        ('SLOWER DISCHARGE', '~5 kt/day', 'typical conventional discharge rate'),
        ('LONGER TURNAROUND', '~12 days', 'alongside per 60 kt cargo; ~200 vessel-days per 1 Mt a year'),
        ('VESSEL TIME AT STAKE', '~US$194k', 'indicative value of vessel time per 60 kt cargo, before demurrage'),
    ],
    'notes': {
        'objective': 'Frame the opportunity as a landscape, not a funnel: the relevant gateway universe is identifiable (102 commercial ports, ~20 state-run dry-bulk gateways, 9 serving the food & feed mills), and six of the nine still discharge conventionally. Then show what conventional handling means physically and in vessel time. The slide ends on the problem; slide 4 is the answer.',
        'talk': 'We do not need to talk about six hundred ports. Indonesia has about one hundred commercial ports, roughly twenty state-run dry-bulk gateways, and nine of those serve the flour and feed mills we just showed. Three of the nine are FKS gateways. The other six still work the way the right of this slide shows: a crane lifts the grain out of the hold with a grab, drops it into an open hopper, the hopper fills one truck at a time, and the truck drives to the mill. The crane can only work as fast as trucks arrive, so discharge speed is set by truck availability. Pelindo’s own productivity figures at conventional berths are between two and three and a half thousand tonnes per ship per day; we use a generous five thousand. For the sixty-thousand-tonne cargo we use throughout this deck, that is about twelve days alongside and, at an indicative sixteen thousand dollars a day of vessel time, close to two hundred thousand dollars per cargo before any demurrage, plus the truck queues, congestion and operational risk that come with it.',
        'sources': 'FKS INTERNAL (v6 deck, FKS screen of public data): 636 public ports in the national port plan; 102 commercial ports; ~20 state-run dry-bulk gateways; 9 serve food & feed mills and refineries; 6 still handled conventionally, the other three being FKS gateways. Vessel-time benchmark ~US$16k per vessel-day, Panamax (2024). The 636 figure is deliberately not shown: it describes the whole national port plan, not the addressable landscape.\nPUBLIC (FACT): Kemenhub National Port Master Plan (RIPN, KP 432/2017) lists 636 ports of which 102 are commercially operated (Antara / Kemenhub). Pelindo Multi Terminal operates ~20 branches for non-container cargo after the 2021 merger. Conventional productivity at public dry-bulk berths: Jamrud (Surabaya) 1,814-3,509 t/ship/day (Bisnis Surabaya, May 2024); Tanjung Emas (Semarang) 2,480-3,098 t/ship/day (Antara Jateng, 2024); before the Belawan conveyor, 20-24 kt soybean-meal cargoes took 4-5 days (~4,000-6,000 t/day; Bisnis Sumatra, May 2021). Mechanised common-user grain discharge exists only at the three FKS gateways (Cigading SGT2 continuous ship unloader 1,300 t/h; Teluk Lamong 2 x 2,000 t/h; Belawan 850-900 t/h conveyor).\nMAP (FKS screen, classification to be confirmed): the nine gateways shown are Belawan, Cigading and Teluk Lamong (FKS, mechanised) and Tanjung Priok, Ciwandan, Panjang, Semarang (Tanjung Emas), Tanjung Perak (Jamrud) and Makassar (conventional). Captive flour-mill jetties (Bogasari at Tanjung Priok and Surabaya, Eastern Pearl at Makassar) are excluded because they serve one miller; several conventional classifications rest on the absence of any published mechanised facility.\nVessel time versus demurrage: the US$16.2k/day figure is an indicative time-charter value of a Panamax vessel-day; demurrage is a contractual rate that applies only beyond laytime and is not shown.',
        'calc': '60,000 t / 5,000 t per day = 12 days alongside. 12 days x US$16,200 per day = US$194,400 (~US$194k) of indicative vessel time per 60 kt cargo. If the underlying rate is US$16,157/day the figure is US$193,900; both round to ~US$194k. Replaces the earlier 55 kt example (11 days) everywhere in the deck. Scaling shown on the slide (DERIVED from the deck’s own numbers): 1 Mt / 60 kt = ~17 cargoes x 12 days = ~200 vessel-days a year, worth ~US$3.2m of indicative vessel time at US$16.2k/day.',
        'validate': '1) FKS operations to confirm the nine-gateway list and the conventional / mechanised classification for each port, ideally with 2025 vessel-call data; also confirm the ~20 state-run dry-bulk gateway count. 2) Confirm the ~5 kt/day conventional benchmark against FKS statements of facts at conventional berths (FKS internal range 6-8 kt/day per v6). 3) Refresh the US$16.2k/day vessel-time value with a dated Baltic Panamax 5TC or Supramax 10TC average before the meeting and recompute US$194k / US$146k if it moves materially. 4) Share of the ~22 Mt that moves through the six conventional gateways: FKS input required (the v6 placeholder is kept out of the slide face).',
    },
}

# ---------------------------------------------------------------- SLIDE 4
S4 = {
    'title': 'The vessel no longer waits for the trucks',
    'subtitle': 'A transit warehouse decouples vessel discharge from road logistics',
    'panel_label': 'FKS INTEGRATED GATEWAY',
    'captions': ['VESSEL', 'UNLOADING', 'CONVEYOR', 'TRANSIT WAREHOUSE · THE BUFFER', 'DISPATCH', 'CUSTOMER · MILL'],
    'direct': 'direct to the mill · planned at Cigading (2026)',
    'marine': 'MARINE CLOCK  ·  ~20 kt/day  ·  ~3 days per 60 kt',
    'inland': 'INLAND CLOCK  ·  trucks load to mill demand',
    'buffer': 'THE BUFFER SEPARATES THE TWO CLOCKS',
    'scope_label': 'FKS SCOPE',
    'scope_line': 'unloading with the port operator  ·  enclosed conveyor  ·  transit storage  ·  controlled dispatch and delivery management  ·  direct mill link where applicable',
    'notes': {
        'objective': 'Sell the FKS operating model as one integrated, physical system and make the transit warehouse the visual centre. The single takeaway: marine operations and inland logistics no longer run on the same clock. The conventional process is not repeated here; slide 3 has just shown it.',
        'talk': 'This is the same cargo handled the FKS way. Ship unloaders lift the grain out of the hold at around twenty thousand tonnes a day. It travels in an enclosed conveyor, weighed as it goes, into a transit warehouse on the quay. That warehouse is the buffer: it can absorb the whole cargo, so the vessel discharges at the unloader’s speed and sails. From the buffer, trucks and bagging lines load to the mill’s own schedule, and where a customer is adjacent, as at Cigading with the Bungasari and Tereos plants from 2026, a conveyor runs straight into the factory. The marine clock and the inland clock are separated by the buffer. The ship is no longer paced by the trucks, the cargo is never in the open, and the port is not filled with trucks queuing for a hopper. FKS’s scope covers the whole chain from the unloader to the mill gate: unloading with the port operator, the conveyor, transit storage, controlled dispatch and delivery management, and the mill link where one exists.',
        'sources': 'FKS INTERNAL (v6 deck): FKS scope = unloading with the port operator, conveyor, transit warehouse, delivery management, mill link; direct conveyor to the mill planned at Cigading (2026); FKS integrated discharge benchmark ~20 kt/day (internal range 25-30 kt/day, to validate). Facility facts (public, for the talk track): Teluk Lamong two 2,000 t/h ship unloaders on the Pelindo berth (-14 m LWS) with 1.3 km conveyors and ~200 kt of silos and flat storage (Majalah Dermaga; Ocean Week; Kompas, Jul 2024); Cigading continuous ship unloader 1,300 t/h into the integrated warehouse on the KBS jetty (-21 m LWS) (Bisnis.com 2016, Antara Banten 2020); Belawan 388 m conveyor at 850-900 t/h into a 30 kt warehouse (Bisnis Sumatra, May 2021). FKS internal storage figures (v6): Cigading 400 kt, Teluk Lamong ~220 kt, Belawan 30 kt; differences from press figures are flagged on slide 6.',
        'calc': '60,000 t / 20,000 t per day = 3 days alongside (versus 12 days conventional on slide 3). Schematic is illustrative and not to scale.',
        'validate': '1) Confirm rated and achieved discharge rates per site (t/h and t/day, 2024-25 statements of facts). 2) Confirm the status of the Cigading conveyor into the mills at the meeting date (planned vs commissioning vs operating). 3) Confirm which sites have in-line weighing and traceability. 4) Consider replacing the schematic with a brand-approved photograph of the Cigading conveyor gallery if available.',
    },
}

# ---------------------------------------------------------------- SLIDE 5
S5 = {
    'title': 'Faster discharge, better freight economics, less cargo lost',
    'subtitle': 'What the operating model is worth to the cargo owner, per 60 kt cargo',
    'cols': [
        {'k': 'FASTER', 'sub': 'The ship discharges at full speed'},
        {'k': 'BETTER ECONOMICS', 'sub': 'Deep berths (−14 m, −21 m LWS) take larger parcels'},
        {'k': 'MORE SECURE', 'sub': 'An enclosed, reconciled chain from hold to mill'},
    ],
    'rate_from': '~5', 'rate_to': '~20', 'rate_sub': 'thousand tonnes discharged per day',
    'days_conv': 12, 'days_fks': 3, 'days_sub': 'alongside for one 60 kt cargo',
    'saved': '~9 vessel-days saved',
    'faster_big': '~US$146k', 'faster_label': 'indicative value of vessel time per 60 kt cargo',
    'faster_small': '~US$2.4 / t  ·  at ~US$16.2k per vessel-day (Panamax, 2024 benchmark)',
    'chain': ['Deeper berth', 'Larger parcel', 'Fewer port calls', 'Lower freight per tonne'],
    'parcel_conv': 'Smaller parcels, two port calls', 'parcel_fks': 'Panamax parcel, one gateway',
    'econ_big': 'Potential freight saving', 'econ_label': 'TO BE QUANTIFIED FROM FKS VOYAGE DATA',
    'econ_small': 'Port calls ≥2 → 1: FKS voyage statement, to validate',
    'loss_conv': '0.2–0.3%', 'loss_fks': '~0.1%', 'loss_sub': 'net cargo loss  ·  FKS experience vs indicative industry range, to validate',
    'secure_points': ['Enclosed handling', 'Fewer touchpoints', 'Reconciled movements'],
    'secure_big': '~US$36k', 'secure_label': 'cargo value preserved per 60 kt cargo  ·  illustrative',
    'secure_small': '~US$0.6 / t  ·  0.2 pp on a US$18m wheat cargo',
    'footer': 'Quantified value ~US$182k per 60 kt cargo (~US$3 / t) before any freight saving; the ~US$146k is the avoidable part of the ~US$194k on slide 3',
    'notes': {
        'objective': 'Turn the operating model into money on one intuitive unit, the 60 kt cargo. The audience should retain: ~9 vessel-days saved, about US$146k of vessel time, a real but not-yet-quantified freight saving, and about US$36k of cargo value preserved (illustrative). Leads into slide 6: FKS already does this at scale.',
        'talk': 'Take one sixty-thousand-tonne cargo. At a conventional berth it sits alongside for about twelve days; through the FKS system it is discharged in about three. Nine vessel-days at an indicative Panamax vessel-time value of sixteen thousand two hundred dollars a day is roughly one hundred and forty-six thousand dollars per cargo, or about two dollars forty a tonne, before any demurrage. The second benefit is freight: a deep berth and a buffer let a customer bring one Panamax instead of two smaller parcels, which lowers freight per tonne and halves the number of port calls. We have deliberately not put a number on that yet; it will come from FKS voyage data. The third benefit is cargo integrity. Enclosed handling removes the spillage and moisture exposure of open grabs and hoppers; our internal experience is around a tenth of a percent of net loss against two to three tenths conventionally. If that preserves just two-tenths of a percent of an eighteen-million-dollar wheat cargo, it is worth about thirty-six thousand dollars per vessel. That figure is illustrative until the loss differential is validated with customer data.',
        'sources': 'FKS INTERNAL (v6 deck): discharge benchmarks ~5 kt/day conventional vs ~20 kt/day FKS integrated (internal 6-8 vs 25-30 kt/day, to validate); vessel time ~US$16k per vessel-day, Panamax (2024); deep berths -14 m LWS (Teluk Lamong) and -21 m LWS (Cigading); net cargo loss 0.2-0.3% conventional (industry data required) vs ~0.1% FKS (internal, to validate); port calls ≥2 → 1 (FKS statement, to validate). PUBLIC corroboration: Pelindo productivity 1,800-3,500 t/ship/day at conventional berths (Bisnis Surabaya, Antara Jateng, 2024); equipment ratings Cigading 1,300 t/h CSU, Teluk Lamong 2 x 2,000 t/h (KBS, Pelindo). Wheat value ~US$300/t: BPS unit value 2024 (11.71 Mt for US$3.5 bn = ~US$300/t). Vessel-time value: indicative time-charter equivalent, to be refreshed with a dated Baltic index; it is not a demurrage rate.',
        'calc': 'FASTER: 60,000 / 5,000 = 12.0 days; 60,000 / 20,000 = 3.0 days; saving 9.0 days x US$16,200 = US$145,800 (~US$146k); with US$16,157/day the result is US$145,400 (~US$145k). Per tonne: 145,800 / 60,000 = US$2.43/t.\nBETTER ECONOMICS: not quantified. Logic: freight per tonne on a 60 kt Panamax is lower than on two ~30 kt Handysize/Supramax parcels on the same route, and port-call charges are incurred once instead of twice; the saving depends on route, season and berth draft and must come from FKS voyage data.\nMORE SECURE: cargo value 60,000 t x US$300/t = US$18.0m; 0.2 percentage points x US$18.0m = US$36,000 (~US$36k); per tonne 36,000 / 60,000 = US$0.60/t.\nCombined quantified value: ~US$182k per 60 kt cargo (~US$3.0/t) before any freight saving.',
        'validate': '1) Replace benchmark discharge rates with measured statement-of-facts averages per site (2024-25). 2) Refresh the vessel-time value with a dated Baltic Panamax 5TC / Supramax 10TC average and state the date on the slide footnote. 3) Quantify the freight and port-cost saving from FKS voyage data (Panamax vs smaller parcels; Australia and Black Sea routes). 4) Validate the cargo-loss differential with customer weighbridge reconciliations and industry data for the conventional rate. 5) Confirm the wheat price basis.',
    },
}

# ---------------------------------------------------------------- SLIDE 6
S6 = {
    'title': 'FKS already operates at three strategic food & feed gateways',
    'subtitle': 'All three sit inside state-owned ports, run with Pelindo and Krakatau',
    'big': '~9 Mt', 'big_sub1': 'a year through FKS’s three gateways', 'big_sub2': 'about 40% of Indonesia’s ~22 Mt of core food & feed imports',
    'big_note': 'Volumes and capacities: FKS data, to be validated',
    'sites': [
        {'name': 'BELAWAN', 'mtpa': '~1 Mtpa', 'place': 'Medan · North Sumatra · Pelindo', 'line': 'Revitalised 30 kt warehouse and conveyor', 'partner': 'Operating partnership with Pelindo', 'photo': 'site_belawan.png', 'lon': 98.69, 'lat': 3.78, 'dx': 0.14, 'dy': -0.12},
        {'name': 'CIGADING', 'mtpa': '~4 Mtpa', 'place': 'Cilegon · Banten · Krakatau (KBS)', 'line': 'Integrated 400 kt warehouse fed by conveyor from the jetty', 'partner': 'Co-invested with KBS; 30 + 20-year term', 'photo': 'site_cigading.png', 'lon': 105.96, 'lat': -5.93, 'dx': -1.05, 'dy': -0.09},
        {'name': 'TELUK LAMONG', 'mtpa': '~4 Mtpa', 'place': 'Surabaya · East Java · Pelindo', 'line': '~220 kt transit storage behind the deep-water berth', 'partner': 'JV with anchor feed customers', 'photo': 'site_teluklamong.png', 'lon': 112.68, 'lat': -7.19, 'dx': 0.14, 'dy': 0.02},
    ],
    'notes': {
        'objective': 'Establish credibility: the model on slides 4-5 is not a concept, it runs today at three gateways inside state-owned ports, with Pelindo and Krakatau Bandar Samudera as partners, handling about a third of the country’s food & feed dry-bulk imports.',
        'talk': 'None of this is theoretical. FKS has operated the model at Teluk Lamong in Surabaya since 2017, at Cigading in Cilegon since 2020 and at Belawan in Medan since 2021, inside Pelindo and Krakatau ports. Together the three gateways move around nine million tonnes a year, about a third of Indonesia’s food and feed dry-bulk imports. Cigading is the largest, with a four-hundred-thousand-tonne integrated warehouse fed by conveyor from the jetty at Indonesia’s deepest dry-bulk port, under a thirty-plus-twenty-year term with KBS. Teluk Lamong has around two hundred and twenty thousand tonnes of transit storage behind Pelindo’s deep-water berth and is a joint venture with anchor feed customers. Belawan is the smallest and the fastest to deliver: an idle Pelindo warehouse and conveyor brought back into service, now turning soybean-meal vessels in two days instead of four or five.',
        'sources': 'FKS INTERNAL (v6 deck, priority source): Belawan ~1 Mtpa, revitalised 30 kt warehouse and conveyor, operating partnership with Pelindo; Cigading ~4 Mtpa, integrated 400 kt warehouse fed by conveyor from the jetty, co-invested with KBS, 30 + 20-year term; Teluk Lamong ~4 Mtpa, ~220 kt transit storage behind the deep-water berth, JV with anchor feed customers; ~9 Mt a year through the three gateways, about a third of Indonesia’s food & feed dry-bulk imports; volumes and capacities are FKS data to be validated.\nPUBLIC CROSS-CHECK: Teluk Lamong storage reported as 200 kt (10 silos 80 kt plus 120 kt flat; Majalah Dermaga) versus FKS ~220 kt; Cigading reported as 200 kt flat storage plus 70-100 kt silos (Bisnis.com, Antara Banten) versus FKS 400 kt - CONFLICTS flagged, FKS figures used on the face pending validation. Belawan conveyor 850-900 t/h, 30 kt warehouse, SBM vessels discharged in 2 days versus 4-5 (Bisnis Sumatra, May 2021) - consistent. Operating entities (v6): PT SGT (Cigading), PT NPL, a JV (Teluk Lamong), PT SGTM (Belawan). Share of imports: 9 / ~22-26 Mt = ~35-40%; “about a third” is conservative.',
        'calc': '~9 Mt = ~1 + ~4 + ~4 Mtpa. 9 / 22.3 = 40% of the four core commodities on slide 2 (the denominator used on the face); v6 said “about a third”, which corresponds to ~26 Mt including raw sugar. One denominator (the ~22 Mt) is now used across the deck.',
        'validate': '1) FKS to confirm throughput by site (t/yr 2023-2025), utilisation and the split between FKS Multi Agro’s own cargo and third-party customers. 2) Reconcile storage capacities with press figures (Cigading 400 kt vs 200 kt + silos; Teluk Lamong 220 vs 200 kt). 3) Confirm cooperation agreement tenors (Cigading 30 + 20 years; Teluk Lamong and Belawan). 4) Replace the low-resolution site photographs with brand-approved originals.',
    },
}

# ---------------------------------------------------------------- SLIDE 7
S7 = {
    'title': 'FKS has built the platform step by step since 2015',
    'subtitle': 'From one terminal in Surabaya to three gateways, now being linked from berth to mill',
    'stages': [
        {'years': '2015–17', 'loc': 'Teluk Lamong', 'place': 'Surabaya · East Java', 'text': 'First transit warehouse and conveyor, at Pelindo’s new deep-water berth', 'photo': 'tl_tl2017.png'},
        {'years': '2019–20', 'loc': 'Cigading', 'place': 'Cilegon · Banten', 'text': 'Integrated warehouse fed by conveyor from Jetty 1, co-invested with KBS', 'photo': 'tl_cg2020.png'},
        {'years': '2020–21', 'loc': 'Belawan', 'place': 'Medan · North Sumatra', 'text': 'Idle Pelindo warehouse and conveyor back in service in ~11 months', 'photo': 'tl_bw2021.png'},
        {'years': '2024–26', 'loc': 'Connecting the chain', 'place': 'Cigading · Teluk Lamong', 'text': 'Jetty 2 conveyor, a bagging line and a conveyor into the mills (2026, planned)', 'photo': 'tl_cg2026.png'},
        {'years': 'Next', 'loc': 'Expansion', 'place': 'Sites and new gateways', 'text': 'Cigading 4 → 6 Mtpa\nTeluk Lamong 4 → 5 Mtpa\nNew: Ciwandan, Dumai', 'map': True},
    ],
    'notes': {
        'objective': 'Show the journey as a simple left-to-right chronology: where FKS started, how it expanded, how the platform became more integrated, and where it goes next. No greenfield / brownfield categories.',
        'talk': 'The platform was built step by step. It started at Teluk Lamong in 2015, with the first transit warehouse and conveyor at Pelindo’s new deep-water berth, in commercial operation from 2017. Cigading followed in 2019 and 2020, an integrated warehouse fed by conveyor from Jetty 1 and co-invested with KBS. Belawan came next: an idle Pelindo warehouse and conveyor brought back into service in about eleven months. Since 2024 the emphasis has shifted from new sites to connecting the chain: a second jetty conveyor at Cigading, a bagging line at Teluk Lamong, and a conveyor straight into the mills at Cigading, planned for 2026. The next stage is the one on the following slide: capacity at Cigading and Teluk Lamong, and two new gateways at Ciwandan and Dumai.',
        'sources': 'FKS INTERNAL: FKS infrastructure development journey 2015-2026 (Teluk Lamong construction 2015, commercial 2017, bagging facility 2025; Cigading construction 2019, Jetty 1 conveyor 2020, Jetty 2 conveyor 2024, extension into the Bungasari and Tereos factories 2026; Belawan revitalisation 2020, operations 2021) and the v6 deck (Belawan back in service in ~11 months; Cigading 4 → 6 Mtpa; Teluk Lamong 4 → 5 Mtpa; new gateways Ciwandan and Dumai). Photographs: FKS sites (from v6). PUBLIC: Belawan conveyor inaugurated May 2021 (Bisnis Sumatra); Cigading Sentral Grain Terminal 2 soft launch reported in 2016 with phase 2 in 2020 (FKS Multi Agro, Antara Banten) - treated as the earlier phase of the same site.',
        'calc': 'None.',
        'validate': '1) Confirm the status wording for the 2026 Cigading mill conveyor at the meeting date (planned / commissioning / operating). 2) Reconcile the 2016 SGT2 soft launch with the 2019-20 dates on the journey slide. 3) Replace photographs with high-resolution originals.',
    },
}

# ---------------------------------------------------------------- SLIDE 8
S8 = {
    'title': 'Next projects identified: two new gateways and two site expansions',
    'subtitle': 'Ciwandan replicates the import model next to Cigading; Dumai applies it to palm-kernel exports',
    'sites': [
        {'name': 'BELAWAN', 'lon': 98.69, 'lat': 3.78, 'kind': 'fks', 'dx': 0.16, 'dy': -0.1},
        {'name': 'CIGADING', 'lon': 105.96, 'lat': -5.93, 'kind': 'fks', 'dx': -1.1, 'dy': -0.32},
        {'name': 'TELUK LAMONG', 'lon': 112.68, 'lat': -7.19, 'kind': 'fks', 'dx': 0.16, 'dy': -0.1},
        {'name': 'DUMAI', 'lon': 101.45, 'lat': 1.68, 'kind': 'new', 'dx': 0.18, 'dy': -0.1},
        {'name': 'CIWANDAN', 'lon': 106.02, 'lat': -6.01, 'kind': 'new', 'dx': -0.55, 'dy': 0.13, 'mdx': 0.14, 'mdy': 0.16},
        {'name': 'Teluk Bayur', 'lon': 100.37, 'lat': -0.99, 'kind': 'watch', 'dx': 0.12, 'dy': -0.08},
        {'name': 'Makassar', 'lon': 119.41, 'lat': -5.13, 'kind': 'watch', 'dx': -0.45, 'dy': -0.26},
    ],
    'legend': [('fks', 'FKS gateway today'), ('new', 'New gateway in the pipeline'), ('exp', 'Expansion at an FKS site'), ('watch', 'Watchlist, public data only')],
    'projects': [
        {'name': 'DUMAI', 'place': 'Riau · Pelindo', 'tag': 'NEW GATEWAY · EXPORT LOADING', 'num': '~1.3 Mt', 'num_sub': 'of PKE and PKS a year (agreement estimate, subject to anchor cargo); ~2 Mt of dry bulk in total',
         'rows': [('WHY', 'Riau’s main port for palm-kernel feed exports'),
                  ('TODAY', 'Conventional handling, ~1.7 kt per ship-day'),
                  ('FKS PLAN', 'Pit, conveyor, ship loader and weighbridge, with Pelindo'),
                  ('UNLOCKS', 'Faster loading; initial FKS tariff component of Rp40,000/t')]},
        {'name': 'CIWANDAN', 'place': 'Banten · next to Cigading', 'tag': 'NEW GATEWAY', 'num': '~1.2 Mt', 'num_sub': 'of wheat and soybean meal a year, still handled by grab and truck',
         'rows': [('WHY', 'The Banten cluster, where FKS already runs Cigading'),
                  ('TODAY', 'Grab, hopper and truck, ~5 kt per ship-day'),
                  ('FKS PLAN', 'Warehouse, conveyor and controlled dispatch'),
                  ('UNLOCKS', 'The Cigading model, replicated next door')]},
    ],
    'cards_note': 'Capex, timing and cooperation-agreement status for both projects: to be shared with the feasibility model',
    'expansions_label': 'SITE EXPANSIONS',
    'expansions': 'Cigading 4 → 6 Mtpa  ·  Teluk Lamong 4 → 5 Mtpa  ·  lowest-risk capital: the sites are already in place',
    'notes': {
        'objective': 'Connect the gap on slide 3 to specific, investable next projects: Dumai and Ciwandan as new gateways, and expansions at Cigading and Teluk Lamong as the lowest-risk capital. Danantara should see tangible places where capital can be deployed.',
        'talk': 'Slide 3 said six import gateways still handle cargo conventionally. Ciwandan is the one where FKS has identified a specific project on the import model; Dumai is an adjacent opportunity outside that screen, applying the same mechanised handling to exports. Dumai is Riau’s main port and the outlet for the region’s palm-kernel feed products, around one point three million tonnes a year of palm kernel expeller and shell, loaded conventionally from trucks at under two thousand tonnes per ship-day. Under the cooperation terms with Pelindo for the dry-bulk terminal, FKS would install a mechanised loading line, dumping pit, conveyor, ship loader and weighbridge, with an FKS tariff component of forty thousand rupiah per tonne alongside Pelindo’s port services. Ciwandan is next door to Cigading in the Banten cluster and still receives about one point two million tonnes of wheat and soybean meal a year by grab, hopper and truck; the project replicates the Cigading model there. On the existing sites, Cigading can grow from four to six million tonnes and Teluk Lamong from four to five with bagging, conveyor, warehouse and wharf works: the lowest-risk capital, because the sites are in place.',
        'sources': 'DUMAI - FKS-Pelindo cooperation document “Tujuan Utama dan Ruang Lingkup Dumai”, tariff and cargo volume section (SOURCE OF TRUTH for scope): initial tariff component for FKSSL Rp40,000/t (dumping pit, intake, conveyor and ship loader Rp37,000/t; weighbridge Rp3,000/t); receiving, cargodoring and port services remain Pelindo’s portion at ~Rp65,000/t; joint socialisation of the new loading tariff for PKE and PKS at TCK Pelabuhan Dumai; PKE and PKS cargo currently estimated at 1.3 Mt per year; the parties to jointly serve all PKE and PKS potential in Riau. PKE = palm kernel expeller; PKS = palm kernel shell; TCK = Terminal Curah Kering. FKS INTERNAL (v6): ~2 Mt of dry bulk a year at Dumai, Riau’s main port; conventional handling at ~1.7 kt per ship-day; value created: faster turnaround, subject to anchor cargo. PUBLIC: Pelindo Multi Terminal Dumai dry-bulk traffic 2.12 Mt through Q3 2024, dominated by palm kernel meal, shell and kernel exports (Pelindo Multi Terminal news) - consistent with FKS’s ~2 Mt.\nCIWANDAN - FKS INTERNAL (v6): ~1.2 Mt of wheat and soybean meal a year; grab, hopper and truck at ~5 kt per ship-day; FKS opportunity: warehouse, conveyor, controlled dispatch; the Cigading model replicated next door. PUBLIC: PTP Nonpetikemas Banten handles wheat, corn and soybean meal at Ciwandan; soybean-meal volume 116,926 t in Jan-Aug 2026, +28% (Kompas Money, Antara); no mechanised grain unloader reported.\nSITE EXPANSIONS - FKS INTERNAL (v6): Cigading 4 → 6 Mtpa (bagging, conveyor, warehouse); Teluk Lamong 4 → 5 Mtpa (new wharf and warehouse). WATCHLIST (public data only): Teluk Bayur, Makassar.',
        'calc': 'Dumai indicative FKS revenue at full capture (DERIVED, not on the slide): 1.3 Mt/yr x Rp40,000/t = Rp52 bn/yr (~US$3.2m at Rp16,300/US$) before ramp-up, volume share and operating cost; combined customer tariff Rp40,000 (FKS) + ~Rp65,000 (Pelindo) = ~Rp105,000/t.',
        'validate': '1) Confirm the Dumai document status (MoU vs signed cooperation agreement, date), the FKSSL entity, capex, ramp-up and volume share; brief the presenter for “is it signed?”. 2) Confirm current loading rates at TCK Dumai and the target rate with the ship loader. 3) Define Ciwandan scope, capacity, capex and the Pelindo cooperation structure; prepare the answer to “why Ciwandan rather than more capacity at Cigading?”. 4) Confirm the ~1.2 Mt Ciwandan wheat and soybean-meal volume with port data. 5) Provide an indicative capex envelope and timing per project, or state when it will be shared.',
    },
}

# ---------------------------------------------------------------- SLIDE 9
S9 = {
    'title': 'Danantara could acquire a strategic stake in FSL',
    'subtitle': 'Danantara would take a stake at platform level, with exposure to FSL’s operating assets and pipeline',
    'today': 'TODAY', 'invests': 'DANANTARA INVESTS', 'after': 'AFTER INVESTMENT', 'illus': 'ILLUSTRATIVE · SUBJECT TO NEGOTIATION',
    'parent': 'FKS Multi Agro', 'fsl': 'FSL', 'fsl_sub': 'FKS Solusi Logistik', 'danantara': 'Danantara Indonesia',
    'invest_text': 'capital injection\nand / or share acquisition',
    'portfolio_label': 'FSL PLATFORM',
    'portfolio_note': 'Illustrative asset and project entities under FSL; entities, JV shares and cooperation-agreement tenors to be confirmed',
    'operating': [('Cigading', 'PT SGT'), ('Teluk Lamong', 'PT NPL · JV'), ('Belawan', 'PT SGTM')],
    'pipeline': [('Ciwandan', ''), ('Dumai', ''), ('Site expansions', ''), ('Future port projects', '')],
    'fit': ('WHY THE FIT', 'Pelindo, FKS’s port partner at four of the five sites, is a Danantara portfolio company; concession governance to be addressed in the structure'),
    'next': ('NEXT STEPS', 'NDA and data room  ·  feasibility model with project and equity returns and capex per project  ·  valuation, stake size, new capital versus share purchase and use of proceeds to be agreed'),
    'notes': {
        'objective': 'Close with a structure that reads in seconds: today FKS Multi Agro owns 100% of FSL; after the investment Danantara would hold an illustrative 49% alongside FKS Multi Agro at 51%; FSL gives exposure to the operating assets and the pipeline. The 49% is illustrative and subject to negotiation; the legal hierarchy of the assets under FSL is to be confirmed.',
        'talk': 'The proposed route for Danantara is a direct stake in FSL, FKS Solusi Logistik, the logistics platform. Today FSL is wholly owned by FKS Multi Agro. In the illustrative structure, Danantara would take a forty-nine percent interest through a capital injection and, or, a share acquisition, with FKS Multi Agro retaining fifty-one percent and operatorship. Through FSL, Danantara would have exposure to the three operating gateways and to the pipeline: Ciwandan, Dumai, the site expansions and future port projects. The percentage, the mix of new capital and share purchase, the valuation and the use of proceeds are all to be agreed and modelled; what we are proposing today is the shape.',
        'sources': 'FKS INTERNAL (v6 deck): FKS Multi Agro 100% of FSL (FKS Solusi Logistik) today; illustrative post-transaction FKS Multi Agro 51% / Danantara 49%; Danantara invests by capital injection and / or share acquisition; operating entities Cigading (PT SGT), Teluk Lamong (PT NPL, JV), Belawan (PT SGTM); pipeline Ciwandan, Dumai, site expansions, future port projects; “illustrative asset and project entities under FSL; legal structure to be confirmed”; to be agreed and modelled: valuation and stake size, new capital versus share purchase, use of proceeds (pipeline capex), returns (project and equity IRR, payback). No change has been made to this logic. Pelindo, FKS’s port partner at Belawan, Teluk Lamong, Dumai and Ciwandan, sits within the Danantara portfolio of state enterprises; concession governance should be addressed in the transaction structure. NAMING CONFLICT (public vs internal): public references describe PT FKS Solusi Logistik as the Belawan operating company (abbreviated FKSSL in the Dumai document) and Nusa Prima Logistik / PT Sentral Grain Terminal as the Teluk Lamong / Cigading operators, whereas v6 names FSL as the platform and PT SGTM as the Belawan entity; whether FSL is the holding entity of PT SGT, PT NPL and PT SGTM is to be confirmed by FKS Legal before the meeting. The v6 face is kept until confirmed. Transaction route: the face keeps v6’s “capital injection and / or share acquisition”; note that only a primary injection funds the pipeline, and a secondary purchase pays FKS Multi Agro; the subtitle is worded to be true for both.',
        'calc': 'None on the slide. The investment case follows the standard chain: volume x handling and storage tariff = revenue, less operating expenses, landlord / concession payments and maintenance = EBITDA, less tax, maintenance capex and working capital = project cash flow, set against initial capex and the financing structure to derive project IRR, equity IRR, payback, ROIC and valuation. These outputs are to be produced in the feasibility model and are deliberately not shown until validated.',
        'validate': '1) Confirm the legal perimeter: which entities (PT SGT, PT NPL, PT SGTM) sit under FSL and how the JV at Teluk Lamong is held. 2) Confirm whether the entry is primary (capital injection) or secondary (share purchase) or both, and the indicative size; only a primary injection funds the pipeline. 3) Confirm cooperation agreement tenors per site for the data room. 4) Prepare feasibility model outputs (project and equity IRR, payback, ROIC) and an indicative capex envelope for Dumai, Ciwandan and the expansions for the next meeting. 5) Confirm Pelindo’s position within the Danantara portfolio and how concession governance would be handled.',
    },
}

DISCLAIMER_NOTES = {
    'objective': 'Standard FKS disclaimer from the template.',
    'talk': 'None.', 'sources': 'FKS template.', 'calc': 'None.', 'validate': 'Legal to confirm wording for an external investor audience.',
}
