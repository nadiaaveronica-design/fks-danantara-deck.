'use strict';
// All slide content in one place. Numbers carry their basis in the notes.
const D = {};
D.date = 'September 2026';

// Site coordinates (approximate port locations). mdx/mdy: marker nudge (inches, scaled per map) so Cigading and Ciwandan do not overlap.
D.sites = [
  { name: 'Belawan', lon: 98.69, lat: 3.78, status: 'operating', tag: 'Medan', dx: 0.18, dy: -0.1 },
  { name: 'Cigading', lon: 105.96, lat: -5.93, status: 'operating', tag: 'Cilegon', mdx: -0.09, mdy: -0.07, dx: -1.35, dy: -0.28, align: 'right' },
  { name: 'Teluk Lamong', lon: 112.68, lat: -7.19, status: 'operating', tag: 'Surabaya', dx: 0.16, dy: -0.12 },
  { name: 'Dumai', lon: 101.45, lat: 1.68, status: 'pipeline', tag: 'Riau', dx: 0.2, dy: -0.04 },
  { name: 'Ciwandan', lon: 106.02, lat: -6.01, status: 'pipeline', tag: 'Cilegon', mdx: 0.11, mdy: 0.09, dx: 0.2, dy: 0.06 },
];

// ---------------------------------------------------------------- SLIDE 2
D.s2 = {
  headline: 'Indonesia imports ~22 Mt of food & feed raw materials a year, milled mostly in a few coastal clusters on Java',
  total: '~22 Mt',
  totalLabel: 'a year, all seaborne; wheat and soybean meal have no domestic substitute',
  composition: [
    { name: 'Wheat', mt: 11.8 },
    { name: 'Soybean meal', mt: 5.9 },
    { name: 'Soybeans', mt: 2.6 },
    { name: 'Other feed ingredients', mt: 1.6 },
    { name: 'Corn', mt: 0.5 },
  ],
  chartNote: 'Mt, calendar 2025 (BPS; USDA FAS for feed ingredients). Corn imports policy-limited since 2025. Excludes raw sugar and rice.',
  flourMills: '31',
  flourLabel: 'flour mills, 24 of them on Java',
  feedMills: '110',
  feedLabel: 'feed mills, 81 of them on Java',
  javaShare: '~80%',
  javaLabel: 'of wheat milling capacity',
  feedShare: '~70%',
  feedShareLabel: 'of animal feed output',
  shareBasis: 'Derived from mill-level data; Sumatra holds roughly 10-15%. Basis in notes.',
  clusters: [
    { name: 'Medan', sub: 'flour + feed', lon: 98.7, lat: 3.6, weight: 0.08, dx: 0.2, dy: -0.28 },
    { name: 'Dumai', sub: 'flour', lon: 101.45, lat: 1.68, weight: 0.03, dx: 0.14, dy: 0.0 },
    { name: 'Lampung', sub: 'feed', lon: 105.3, lat: -5.45, weight: 0.05, dx: -1.5, dy: -0.62, align: 'right', leader: true },
    { name: 'Banten – Greater Jakarta', sub: 'flour + feed + starch', lon: 106.5, lat: -6.1, weight: 0.45, dx: -1.0, dy: 0.3, align: 'right', leader: true },
    { name: 'Semarang', sub: 'flour + feed', lon: 110.4, lat: -6.95, weight: 0.08, dx: -0.45, dy: 0.16, align: 'center' },
    { name: 'Surabaya – Gresik', sub: 'flour + feed', lon: 112.7, lat: -7.2, weight: 0.3, dx: 0.26, dy: -0.06 },
    { name: 'Makassar', sub: 'flour + feed', lon: 119.4, lat: -5.1, weight: 0.08, dx: 0.16, dy: -0.12 },
  ],
  bridge: [
    { k: 'MARKET', v: '~22 Mt of grain, oilseed and feed imports every year' },
    { k: 'DEMAND', v: 'Milled in a few coastal clusters, mainly on Java' },
    { k: 'GATEWAY REQUIREMENT', v: 'A small number of gateways carry the flow, so their handling efficiency sets the landed cost' },
  ],
  source: 'Sources: BPS import statistics 2024-25; USDA FAS GAIN Indonesia Grain & Feed Annual (Apr 2026) and Oilseeds Annual (Apr 2026); APTINDO; GPMT; company disclosures. Bubble size is a proxy for cluster milling capacity. Classification (fact / derived / proxy) in speaker notes.',
  notes: {
    objective: 'Bridge market size to geography. Danantara should leave this slide with three linked ideas: the cargo base is large and structural (~22 Mt/yr); it is processed by a concentrated set of mills, mostly on Java; therefore a few gateways carry the flow and their handling efficiency matters disproportionately. This sets up slide 3 (most of those gateways still handle conventionally).',
    talk: 'Indonesia grows no wheat and produces almost no soybean meal, so the raw materials for bread, noodles, tempe and animal feed arrive by sea every year. Around 22 million tonnes of grain, oilseeds and feed ingredients came in last year, with wheat alone close to 12 million tonnes, which makes Indonesia the largest or second-largest wheat importer in the world. Corn is the exception: imports have been cut back under the self-sufficiency policy, and soybean-meal and feed-wheat imports have been licensed since May 2026 with a large share channelled through state companies, which is itself relevant to Danantara. That cargo is not spread evenly across the archipelago. Twenty-four of the country’s thirty-one flour mills and eighty-one of its one hundred and ten feed mills are on Java. On our bottom-up estimate about four-fifths of wheat milling capacity and roughly seventy percent of feed output sit there, with Greater Jakarta, the Cilegon coast of Banten and Surabaya–Gresik as the three largest clusters. Medan and Lampung are the main clusters on Sumatra. The consequence is simple: a handful of deep-water gateways carry most of the flow, so the way cargo is handled at those gateways sets the landed cost for the whole chain.',
    sources: 'FACT - Wheat imports: 11.71 Mt CY2024 (BPS via Katadata Databoks, https://databoks.katadata.co.id/perdagangan/statistik/68110587bfb69/daftar-pengirim-gandum-dan-meslin-terbanyak-ke-indonesia-2024); ~11.8 Mt CY2025 (BPS Jan-Nov 10.45 Mt plus December run-rate; 11.76 Mt cited in one secondary source); USDA FAS GAIN ID2026-0010 (Apr 2026): 10.45 MMT MY2024/25, forecast 12.3 MMT MY2025/26; USDA WASDE 13.2 Mt 2025/26, level with Egypt as the world’s largest importer (Grain Central, https://www.graincentral.com/markets/indonesian-wheat-imports-on-the-rise/).\nFACT - Soybean meal imports: 5.43 Mt CY2024 (BPS via Kompas.id), 5.9-5.96 Mt 2025 (USDA GAIN ID2026-0017). Import licensing and ~60% SOE allocation from May 2026 (GAIN ID2026-0017).\nFACT - Soybeans: 2.68 Mt CY2024, 2.56 Mt CY2025 (BPS via Katadata / Koran Jakarta).\nFACT - Corn: ~1.3 Mt Jan-Nov 2024 (BPS via Kontan); 2025 imports ~0.4-0.6 Mt under the self-sufficiency policy, industrial quota 0.3-0.6 Mt for 2025/26 (Kementan, USDA GAIN).\nFACT - DDGS: 1.02 Mt U.S.-origin MY2023/24, 0.84 Mt MY2024/25 (USDA GAIN ID2025-0030); MBM ~0.5 Mt (2023, Tridge/UN Comtrade); CGM ~0.3 Mt (derived). Shown as ~1.6 Mt other feed ingredients.\nFACT - Raw sugar (excluded): 5.31 Mt 2024, 3.93 Mt 2025 (BPS). Rice (excluded, bagged): 4.52 Mt 2024, ~0.4 Mt Jan-Oct 2025 (BPS).\nFACT - Flour mills: 31 mills, 14.8 Mt/yr installed wheat-grind capacity; 24 on Java, 5 on Sumatra, 2 on Sulawesi (USDA FAS GAIN Indonesia Grain and Feed Annual ID2026-0010, 1 Apr 2026). Flour consumption 7.41 Mt in 2025, ~10 Mt wheat equivalent (APTINDO via Katadata, Jan 2026).\nFACT - Feed mills: 110 mills operated by 44 companies in 10 provinces, 81 on Java (USDA GAIN ID2022-0008 / ID2024-0010 / ID2026-0010); GPMT installed capacity ~30-31 Mt/yr, production ~21.5 Mt 2025 (GPMT outlook seminar, Nov 2025, via Majalah Infovet); USDA basis 21.4 MMT (2024/25), 23.3 MMT forecast (2025/26).\nDERIVED - Java share of wheat milling capacity ~81-85%: bottom-up sum of published mill capacities (Bogasari Jakarta 11,600 t/d, Surabaya 6,000, Cibitung 2,600, Tangerang 500; Bungasari Cilegon 2,600; Harvestar Gresik 2,200; Sriboga Semarang 1,850; Cerestar Cilegon 1,500; Manunggal Cilacap 1,200; Wilmar Gresik, Fugui Gresik, Pundi Kencana ~1,000 each; Golden Grand 600; small Sidoarjo/Tangerang mills) = ~34,700 t/d on Java vs ~3,400-4,500 t/d on Sumatra and ~2,850-3,400 t/d on Sulawesi; total ~41-43k t/d reconciles with USDA 14.8 Mt/yr. Cluster shares of flour capacity: Greater Jakarta ~36%, Surabaya/Gresik/Sidoarjo ~26%, Cilegon/Banten ~14%, Semarang + Cilacap ~7%, Makassar ~7%, Medan ~6%, Dumai ~2%.\nDERIVED - Java share of feed output ~65-74%: triangulated from mill location (81/110 = 74%), broiler population (Java 62.9%, BPS 2024) and layer population (East + Central Java 46%, BPS 2024); Sumatra ~12-20% (Lampung installed capacity 1.96 Mt/yr per Disnak Lampung; Medan cluster ~1 Mt/yr named capacity). Feed is produced close to the poultry belts, so mill location is a strong proxy for where imported SBM and corn are discharged.\nPROXY - Map bubbles are sized by approximate share of flour and feed milling capacity in each cluster.',
    calc: '~22 Mt (CY2025) = wheat ~11.8 + soybean meal 5.9 + soybeans 2.6 + other feed ingredients ~1.6 + corn ~0.5 = ~22.4 Mt. Cross-check CY2024 = 11.71 + 5.43 + 2.68 + ~1.4 + ~1.7 = ~22.9 Mt. Including raw sugar the total is ~26-28 Mt; including 2024 rice imports (4.5 Mt, bagged) ~32 Mt. Mill count shares: flour 24/31 = 77% Java; feed 81/110 = 74% Java. Capacity shares as above (derived).',
    validate: '1) Pull the primary USDA GAIN PDFs (ID2026-0010, ID2026-0013) and BPS tables to confirm each figure; the research run could only read search snippets because PDF hosts were blocked. 2) Confirm full-year 2025 wheat imports with the BPS table. 3) Replace the derived Java capacity shares with APTINDO and GPMT capacity-by-province data if FKS can obtain them (GPMT member presentations carry a provincial table). 4) Quantify the share of the ~22 Mt discharged at captive mill jetties (Bogasari Tanjung Priok and Surabaya, Eastern Pearl Makassar) versus common-user gateways; this defines the volume addressable by the FKS model and will be asked. 5) Wilmar Dumai and Bogasari Medan mill capacities are undisclosed. 6) Add FKS internal import-share data if it can be disclosed.',
  },
};

// ---------------------------------------------------------------- SLIDE 3
D.s3 = {
  headline: 'Only three of ~14 public gateways discharge grain mechanically, and all three were built with FKS; the rest still work by grab and truck',
  tiles: [
    { num: '~14', label: 'public gateways handle food & feed dry bulk for the milling clusters' },
    { num: '3', label: 'have mechanised common-user discharge into a conveyor and warehouse, all built with FKS' },
    { num: '~11', label: 'still discharge conventionally, at roughly one-third to one-seventh of the speed' },
  ],
  tileNote: 'Greater Jakarta, the largest milling cluster, has no mechanised common-user grain berth identified.',
  case: [
    { num: '~5 kt/day', label: 'conventional discharge benchmark' },
    { num: '60 kt of cargo', label: 'as two ~30 kt parcels at a conventional berth' },
    { num: '~12 days', label: 'alongside in total' },
    { num: '~US$194k', label: 'of vessel time per 60 kt at US$16.2k/day' },
  ],
  source: 'Desk screening of 14 public gateways from published port data (2026), to be confirmed with FKS operations; captive flour-mill jetties (e.g. Bogasari) excluded; some ports classified by the absence of a published mechanised facility. Conventional rates: Pelindo Multi Terminal releases for Jamrud and Tanjung Emas, 2024. Vessel time: Panamax/Supramax time-charter benchmark.',
  notes: {
    objective: 'Make the infrastructure gap concrete without a misleading funnel. Two messages: (1) the relevant gateway landscape is small and identifiable, and only the three FKS sites have mechanised common-user handling; (2) conventional discharge is paced by truck cycles, which turns 60 kt of cargo into roughly 12 days alongside. Leads into slide 4 (what FKS does differently).',
    talk: 'We do not need to talk about six hundred ports. Indonesia’s master plan lists 636 ports, but only 102 are commercial, and the milling clusters we just showed are served by about fourteen public gateways. Of those, three have mechanised grain discharge into a conveyor and warehouse for any customer, and all three were built with FKS. The largest millers have their own captive jetties; everyone else, and all of the feed industry, uses the public berths, and those still work the way the bottom of this slide shows: a crane lifts the grain out of the hold with a grab, drops it into an open hopper, the hopper fills one truck at a time, and the truck drives to the mill. The crane can only work as fast as trucks arrive, so the ship is paced by the trucks. Pelindo’s own productivity figures at conventional berths in Surabaya and Semarang are between eighteen hundred and thirty-five hundred tonnes per ship per day; we use a generous five thousand. Sixty thousand tonnes of cargo, which at a shallow conventional berth arrives as two thirty-thousand-tonne parcels, takes about twelve days alongside in total and close to two hundred thousand dollars of vessel time, before demurrage, cargo loss and the trucks queuing in the city.',
    sources: 'FACT - Port counts: Kemenhub National Port Master Plan (RIPN, KP 432/2017) lists 636 ports (28 main, 164 collector, 166 regional feeder, 278 local feeder), of which 102 are commercially operated; 1,394 special/own-use terminals sit outside the count (Antara / Kemenhub, https://www.antaranews.com/berita/3751818/mewujudkan-indonesia-poros-maritim-dunia-lewat-konektivitas-pelabuhan). Pelindo operates 110 ports after the 2021 merger; Pelindo Multi Terminal handled 59.08 Mt of all-commodity dry bulk in 2024 (Kontan).\nDESK SCREENING (DERIVED, to be confirmed by FKS operations) - 14 public gateways handling food & feed dry bulk: Tanjung Priok (PTP multipurpose), Ciwandan (Banten), Cigading (KBS), Panjang (Lampung), Tanjung Emas (Semarang), Cilacap, Tanjung Perak Jamrud (Surabaya), Teluk Lamong (Surabaya), Gresik, Belawan (Medan), Kuala Tanjung, Makassar (public berths), Banjarmasin, Pontianak. Dumai is an export gateway for palm-kernel products and is not counted. Mechanised common-user grain discharge (unloader + conveyor + silo/warehouse) exists at three: Cigading Sentral Grain Terminal 2 (FKS with KBS; continuous ship unloader 1,300 t/h, ~20,000 t/day; Bisnis.com 2016, Antara Banten 2020), Teluk Lamong (Pelindo with FKS’s Nusa Prima Logistik; 2 x 2,000 t/h grab ship unloaders, up to 24,000 t/day, 200,000 t storage; Majalah Dermaga, Ocean Week) and Belawan dry-bulk terminal (FKS Solusi Logistik with Pelindo; 850-900 t/h conveyor, ~10,300 t/day; Bisnis Sumatra 11 May 2021). Two captive flour-mill jetties (Bogasari Tanjung Priok, up to 3,200 t/h; Eastern Pearl Makassar, pneumatic) are excluded because they serve one miller; Bogasari Surabaya also has its own discharge. Positive evidence of conventional handling: Jamrud truck-lossing (Universitas Maritim AMNI repository), Tanjung Emas gang-based productivity metrics (Antara Jateng), Ciwandan and Tanjung Priok with no unloader reported (PTP lists grab ship unloaders only as a planned investment). Gresik, Panjang, Cilacap, Makassar public berths, Banjarmasin, Pontianak and Kuala Tanjung are classified by absence of any published mechanised grain system.\nFACT - Conventional productivity: Pelindo Multi Terminal reports 1,814-3,509 t/ship/day at Jamrud (Bisnis Surabaya, May 2024) and 2,480-3,098 t/ship/day at Tanjung Emas (Antara Jateng, 2024); branch averages cover all dry-bulk commodities and include idle time. Before the Belawan conveyor, 20-24 kt soybean-meal cargoes took 4-5 days (~4,000-6,000 t/day; Bisnis Sumatra 2021). FKS/Nusa Prima Logistik cites ~6,000 t/day conventional vs up to 30,000 t/day mechanised (Kompas, Jul 2024). The deck’s 5 kt/day benchmark is therefore generous to the conventional case.\nBENCHMARK - Vessel-time value US$16,200/day: consistent with 2025-26 Panamax/Supramax time-charter levels reported by the Baltic Exchange and trade press; treat as a benchmark, not a contracted rate. Berth depths: Tanjung Priok -7/-12 m, Tanjung Emas -10/-12 m, Belawan -9 m, versus Teluk Lamong -14 m and Cigading -21 m; a laden 60 kt Panamax needs roughly -13 m, so at conventional berths the same tonnage arrives as smaller parcels.',
    calc: '60,000 t / 5,000 t per day = 12 days alongside in total, whether as one call or as two ~30 kt parcels (2 x 30,000 / 5,000 = 2 x 6 days). 12 days x US$16,200/day = US$194,400 (~US$194k) of vessel time per 60 kt. Speed ratio: 20,000-24,000 t/day mechanised vs 3,000-6,000 t/day conventional = 3x to 7x. Scaling (derived, not on slide): at ~US$2.4/t of vessel time, each 1 Mt handled conventionally ties up about US$2.4m of vessel time a year. This replaces the earlier 55 kt example; every dependent figure in the deck now uses the 60 kt case.',
    validate: '1) FKS operations to confirm the 14-gateway list and the classification of each port, ideally with 2025 vessel-call data; confirm Kuala Tanjung and Cilacap status. 2) Confirm the ~5 kt/day conventional benchmark against FKS statements of facts at conventional berths. 3) Refresh the US$16.2k/day vessel-time value with the Baltic Exchange Panamax 5TC or Supramax 10TC average for a stated week before the meeting and recompute US$194k / US$146k if it moves materially. 4) All port facts were read from search snippets because page fetches were blocked; spot-check the cited URLs.',
  },
};

// ---------------------------------------------------------------- SLIDE 4
D.s4 = {
  headline: 'The FKS transit buffer lets the ship discharge at its own speed while trucks load at the mill’s',
  steps: [
    { n: 1, k: 'High-capacity unloading', v: 'Up to 2,000 t/h; ~20 kt/day', x: 0.6, w: 2.3 },
    { n: 2, k: 'Enclosed conveyor', v: 'Covered and weighed', x: 3.25, w: 2.3 },
    { n: 3, k: 'Transit warehouse & silos', v: 'Up to 200,000 t; holds a full cargo', x: 6.0, w: 2.6, hi: true },
    { n: 4, k: 'Controlled loading', v: 'Trucks and bagging to mill schedule', x: 9.0, w: 2.2 },
    { n: 5, k: 'Customer / mill', v: 'Delivered on demand', x: 11.45, w: 1.3 },
  ],
  outcomes: [
    { num: '~3 days', label: 'to discharge 60 kt instead of ~12' },
    { num: '0', label: 'open-air transfers from hold to mill' },
    { num: '200,000 t', label: 'of buffer at Teluk Lamong and at Cigading' },
  ],
  source: 'Facilities operated with FKS: Teluk Lamong (Pelindo berth, 2 x 2,000 t/h unloaders; FKS conveyors and 200,000 t storage) and Cigading (FKS 1,300 t/h continuous ship unloader, 200,000 t warehouse plus silos). ~20 kt/day is the conservative benchmark for these two deep-water sites; Belawan discharges ~10 kt/day into a 30,000 t warehouse at a shallower berth. Schematic not to scale.',
  notes: {
    objective: 'Sell the FKS operating layer as one integrated system and make the transit buffer visually obvious. The single takeaway: marine operations and inland logistics are decoupled, so the ship discharges at its own speed and trucks load at the mill’s speed. Leads into slide 5 (what that is worth per cargo).',
    talk: 'This is the same cargo handled the FKS way. Ship unloaders rated at up to two thousand tonnes an hour lift the grain out of the hold, around twenty thousand tonnes a day in practice. It travels in an enclosed conveyor, weighed as it goes, into a transit warehouse and silo complex on the quay. That buffer is the heart of the model: at Teluk Lamong and Cigading it holds up to two hundred thousand tonnes, so the vessel discharges at the unloader’s speed and sails. From the buffer, trucks and bagging lines load to the mill’s own schedule, and where a customer is adjacent, as at Cigading with Bungasari and Tereos, a conveyor runs straight into the factory. Marine and inland operations are decoupled. The ship is no longer paced by the trucks, the cargo is never in the open, and the city is not filled with trucks queuing for a hopper. Belawan runs the same model at a smaller scale, around ten thousand tonnes a day into a thirty-thousand-tonne warehouse, because the berth there is shallower.',
    sources: 'Teluk Lamong dry-bulk terminal: two grab ship unloaders of 2,000 t/h each (up to 24,000 t/day) on the Pelindo berth (-14 m LWS); two 1.3 km conveyor lines, 10 silos (80,000 t) plus flat storage (120,000 t) = 200,000 t, operated by Nusa Prima Logistik, an FKS Group company (Majalah Dermaga; Ocean Week; Kompas, 14 Jul 2024). Cigading Sentral Grain Terminal 2 (PT Sentral Grain Terminal, FKS, with Krakatau Bandar Samudera): continuous ship unloader 1,300 t/h (~20,000 t/day), food-grade conveyor to an 11.6 ha integrated warehouse with 200,000 t flat storage plus silos; port depth -21 m LWS (Bisnis.com, 4 Dec 2016; Antara Banten 2020). Belawan dry-bulk terminal (FKS Solusi Logistik with Pelindo, 2021): 388 m conveyor at 850-900 t/h, 30,000 t warehouse, four truck-loading conveyors; soybean-meal discharge cut to 2 days from 4-5 (Bisnis Sumatra, 11 May 2021). Direct conveyor to mill: Cigading extension to the Bungasari and Tereos factories (FKS journey slide, 2026). Asset boundary (to confirm): at Teluk Lamong the berth and unloaders are Pelindo / Terminal Teluk Lamong assets and FKS operates the conveyors and storage; at Cigading the unloader, conveyor and warehouse are FKS’s on the KBS jetty; at Belawan FKS revitalised and operates a Pelindo warehouse.',
    calc: '60,000 t / 20,000 t per day = 3 days alongside (versus 12 days conventional on slide 3). Equipment ratings imply up to 24,000-30,000 t/day at Teluk Lamong; the deck uses a conservative 20,000 t/day for the two deep-water sites.',
    validate: '1) Confirm rated and achieved discharge rates (t/h and t/day, 2024-25 statements of facts) and storage capacity per site with the FKS engineering team; press figures differ between sources (Cigading silos 70,000-100,000 t; Teluk Lamong 24,000 vs 30,000 t/day). 2) Confirm the asset boundary per site (FKS-owned vs partner-owned vs operated by FKS); this is the transaction perimeter on slide 9. 3) Confirm which sites have in-line weighing and traceability systems. 4) Add a photograph or render of the Cigading conveyor gallery if brand-approved imagery is available.',
  },
};

// ---------------------------------------------------------------- SLIDE 5
D.s5 = {
  headline: 'Per 60 kt of cargo, the integrated model saves about nine vessel-days and protects cargo value',
  convLabel: 'Conventional berth',
  convSub: '60 kt as two ~30 kt parcels at ~5 kt/day',
  fksLabel: 'FKS integrated gateway',
  fksSub: 'one 60 kt call at ~20 kt/day',
  tileNum: '~US$3.0/t',
  tileLabel: 'quantified value per tonne of cargo',
  tileSub: 'vessel time ~US$2.4/t plus cargo preserved ~US$0.6/t, before any freight saving',
  panels: [
    { k: 'FASTER', head: 'Vessel time released', num: '~US$146k', numLabel: 'vessel-time value per 60 kt', basis: '~9 vessel-days saved at US$16.2k/day', tag: 'BENCHMARK BASIS' },
    { k: 'BETTER ECONOMICS', head: 'Freight and port cost', num: 'Potential freight saving', numSize: 18, numLabel: 'to be quantified from FKS voyage data', basis: 'One 60 kt Panamax call at a deep berth instead of two ~30 kt parcels', tag: 'NOT YET QUANTIFIED', mini: 'parcels' },
    { k: 'MORE SECURE', head: 'Cargo value preserved', num: '~US$36k', numLabel: 'cargo value preserved per 60 kt', basis: '0.2 pp less cargo loss on a US$18.0m wheat cargo', tag: 'ILLUSTRATIVE, TO BE VALIDATED' },
  ],
  source: 'Basis: 60 kt of cargo; FKS operating benchmarks of 5 kt/day conventional and 20 kt/day integrated (corroborated by Pelindo productivity data, slide 3 notes); vessel time US$16.2k/day (Panamax/Supramax time-charter benchmark); wheat ~US$300/t (BPS unit value 2024); loss differential 0.2 pp (illustrative). Arithmetic in notes.',
  notes: {
    objective: 'Turn the operating model into money on one intuitive unit, 60 kt of cargo. The audience should retain three numbers: nine days saved, about US$146k of vessel time, about US$36k of cargo preserved, and understand that the freight saving is real but not yet quantified. Leads into slide 6 (FKS already does this at scale).',
    talk: 'Take sixty thousand tonnes of cargo. At a conventional berth it arrives as two smaller parcels and sits alongside for about twelve days in total; through the FKS system it comes in one Panamax and is discharged in about three. Nine vessel-days at a market time-charter benchmark of sixteen thousand two hundred dollars a day is roughly one hundred and forty-six thousand dollars, or about two dollars forty a tonne, before demurrage. The second benefit is freight: a deep berth and a buffer let a customer bring one Panamax instead of two smaller parcels, which lowers freight per tonne and halves the number of port calls. We have deliberately not put a number on that yet; we will quantify it from FKS voyage data. The third benefit is cargo integrity. Enclosed handling removes the spillage and moisture exposure of open grabs and hoppers. If that preserves just two-tenths of a percent of an eighteen-million-dollar wheat cargo, it is worth about thirty-six thousand dollars per vessel. That figure is illustrative until the loss differential is validated with customer data. Together, the quantified benefits are about three dollars a tonne before any freight saving.',
    sources: 'Discharge rates: FKS operating benchmarks (5 kt/day conventional, 20 kt/day integrated), corroborated by Pelindo productivity data (1,800-3,500 t/ship/day at conventional berths in Surabaya and Semarang) and equipment ratings (Cigading 1,300 t/h CSU, Teluk Lamong 2 x 2,000 t/h). The 20 kt/day benchmark applies to the two deep-water sites (Teluk Lamong -14 m, Cigading -21 m); Belawan runs ~10 kt/day at -9 m. Vessel-time value US$16,200/day: benchmark consistent with 2025-26 Panamax/Supramax time-charter levels (Baltic Exchange, trade press); to be refreshed with a dated Baltic index value before the meeting. Wheat value ~US$300/t: BPS unit value, 2024 wheat imports 11.71 Mt for US$3.5 bn = ~US$300/t. Cargo loss differential 0.2 percentage points: illustrative assumption carried from earlier versions of this deck; not yet validated. Platform revenue capture (tariff per tonne) is not shown; see validation list.',
    calc: 'FASTER: 60,000 / 5,000 = 12.0 days (as two 30 kt parcels: 2 x 6 days); 60,000 / 20,000 = 3.0 days; saving 9.0 days x US$16,200 = US$145,800 (~US$146k); per tonne 145,800 / 60,000 = US$2.43/t.\nMORE SECURE: cargo value 60,000 t x US$300/t = US$18.0m; 0.2% x US$18.0m = US$36,000 (~US$36k); per tonne 36,000 / 60,000 = US$0.60/t.\nBETTER ECONOMICS: not quantified. Indicative logic: freight per tonne on a 60 kt Panamax is typically lower than on two ~30 kt Handysize/Supramax parcels on the same route, and port-call charges are incurred once instead of twice; the saving depends on route, season and berth draft and must come from FKS voyage data.\nCombined quantified value: 145,800 + 36,000 = US$181,800 per 60 kt = US$3.03/t (~US$3.0/t) before freight savings.',
    validate: '1) Replace benchmark discharge rates with measured FKS statement-of-facts data (average t/day at each site, 2024-25). 2) Refresh the vessel-time value with a dated Baltic Panamax 5TC / Supramax 10TC average. 3) Quantify the freight and port-cost saving from FKS voyage data (Panamax vs smaller parcels, Australia and Black Sea routes). 4) Validate the cargo loss differential with customer weighbridge reconciliations. 5) Add how the platform captures value: handling and storage tariff per tonne and revenue per 60 kt cargo, so the customer-value story connects to FSL revenue and to Danantara’s return.',
  },
};

// ---------------------------------------------------------------- SLIDE 6
D.s6 = {
  headline: 'FKS already runs the integrated model at three gateways on Java and Sumatra',
  stats: [
    { num: '3', label: 'gateways operating since 2017, 2020 and 2021 with Pelindo and Krakatau Bandar Samudera' },
    { num: '~430 kt', label: 'of covered transit storage across the three sites (excl. Cigading silos)' },
    { num: '~20 kt/day', label: 'integrated discharge benchmark; rated up to 24 kt/day at Teluk Lamong' },
    { num: '2 days', label: 'soybean-meal vessel turnaround at Belawan, down from 4-5' },
  ],
  sites: [
    { name: 'Teluk Lamong', where: 'Surabaya, East Java  |  with Pelindo', photo: 'duo_tl2017.png', rows: [
      { k: 'SINCE', v: '2017; bagging facility added 2025' },
      { k: 'FACILITIES', v: 'Pelindo berth (-14 m) with 2 x 2,000 t/h unloaders; FKS-operated 1.3 km conveyors, silos and flat storage of 200,000 t' },
      { k: 'SERVES', v: 'Surabaya–Gresik flour and feed cluster' },
    ] },
    { name: 'Cigading', where: 'Cilegon, Banten  |  with Krakatau Bandar Samudera', photo: 'duo_cg2024.png', rows: [
      { k: 'SINCE', v: '2020; Jetty 2 linked 2024, factory links 2026' },
      { k: 'FACILITIES', v: 'FKS 1,300 t/h continuous ship unloader, conveyor and 200,000 t integrated warehouse plus silos on the KBS jetty (-21 m)' },
      { k: 'SERVES', v: 'Banten cluster incl. Bungasari and Tereos FKS' },
    ] },
    { name: 'Belawan', where: 'Medan, North Sumatra  |  with Pelindo', photo: 'duo_bw2021.png', rows: [
      { k: 'SINCE', v: '2021; Pelindo warehouse revitalised by FKS' },
      { k: 'FACILITIES', v: '388 m conveyor at 850-900 t/h (~10 kt/day), 30,000 t warehouse, four truck-loading lines' },
      { k: 'SERVES', v: 'Medan flour and feed cluster, North Sumatra' },
    ] },
  ],
  source: 'Sources: FKS infrastructure development journey 2015-2026; Pelindo / Terminal Teluk Lamong; Krakatau Bandar Samudera; FKS Multi Agro; Bisnis.com, Kompas, Majalah Dermaga. Site throughput and customer mix to be provided under NDA.',
  notes: {
    objective: 'Establish credibility: the model on slides 4-5 is not a concept, it runs today at three gateways with two port partners. Keep the face of the slide to location, partner, facilities and the cluster served; throughput and customer mix are to be provided under NDA.',
    talk: 'None of this is theoretical. FKS has operated the model at Teluk Lamong in Surabaya since 2017, at Cigading in Cilegon since 2020 and at Belawan in Medan since 2021, in partnership with Pelindo at two sites and with Krakatau Bandar Samudera at Cigading. Together the three sites hold around four hundred and thirty thousand tonnes of covered transit storage. Teluk Lamong discharges up to twenty-four thousand tonnes a day with two ship unloaders on the Pelindo berth into two hundred thousand tonnes of FKS-operated silos and warehouse; Cigading runs FKS’s own continuous ship unloader into a two-hundred-thousand-tonne integrated warehouse at Indonesia’s deepest dry-bulk port; and at Belawan the conveyor cut soybean-meal vessel turnaround from four or five days to two. Cigading is the most integrated: cargo now moves by conveyor from two jetties into the warehouse and, from this year, straight into the Bungasari and Tereos FKS factories. Throughput by site and the customer mix, including the share that is FKS Multi Agro’s own cargo, will be shared under NDA.',
    sources: 'Teluk Lamong: two grab ship unloaders of 2,000 t/h (up to 24,000 t/day) on the Pelindo / Terminal Teluk Lamong berth, -14 m LWS; two 1.3 km conveyors, 10 silos (80,000 t) and flat storage (120,000 t) operated by Nusa Prima Logistik, an FKS Group company, which cites up to 30,000 t/day and 5 Mt/yr capacity (Majalah Dermaga, https://majalahdermaga.co.id/post/1755/terminalcurah; Ocean Week; Telusur; Kompas, 14 Jul 2024). Cigading: Sentral Grain Terminal 2, PT Sentral Grain Terminal (FKS) with PT Krakatau Bandar Samudera; CSU 1,300 t/h, 11.6 ha integrated warehouse, 200,000 t flat storage plus silos (70,000-100,000 t by source); Krakatau International Port depth -21 m LWS, 200,000 DWT (Bisnis.com 5 Sep 2019 and 4 Dec 2016; Antara Banten 2020; FKS Multi Agro). Belawan: PT FKS Solusi Logistik with Pelindo 1, 388 m conveyor at 850-900 t/h with telescopic chutes, 6,912 m2 / 30,000 t warehouse, four truck-loading conveyors, productivity ~10,000-10,300 t/day; MV Sea Odyssey (19,411 t) and MV Castellani (24,040 t) soybean meal discharged in 2 days vs 4-5 (Bisnis Sumatra, 11 May 2021; Liputan6; Investor.id). Chronology: FKS infrastructure development journey 2015-2026. Bungasari Flour Mills Cilegon (FKS JV with Malayan Flour Mills and Toyota Tsusho group), ~2,600 t/day; Tereos FKS Indonesia starch and sweetener plant, Cilegon.',
    calc: 'Covered storage: 200,000 (Teluk Lamong silos and flat storage) + 200,000 (Cigading flat storage, excluding its silos) + 30,000 (Belawan) = 430,000 t. Discharge: Teluk Lamong 24,000 t/day = 2 unloaders x 2,000 t/h x ~6 effective hours, the equipment rating quoted by Pelindo; Cigading ~20,000 t/day = 1,300 t/h x ~15 effective hours; the deck uses ~20 kt/day as the conservative benchmark.',
    validate: '1) FKS engineering to confirm every facility figure before the meeting; press sources differ (Cigading silos 70,000 vs 100,000 t; Teluk Lamong 24,000 vs 30,000 t/day). 2) Prepare annual throughput (t/yr, 2023-2025), utilisation and third-party versus FKS Multi Agro cargo share per site for release under NDA. 3) Confirm the asset boundary and legal entity per site (Nusa Prima Logistik, Sentral Grain Terminal, FKS Solusi Logistik) and the cooperation agreement tenors with Pelindo and KBS. 4) Confirm the Bungasari shareholding. 5) Replace the low-resolution site photographs (taken from the earlier journey slide; shown here in a navy duotone) with high-resolution brand-approved images.',
  },
};

// ---------------------------------------------------------------- SLIDE 7
D.s7 = {
  headline: 'FKS has built three gateways since 2015 and, since 2024, has been linking them straight into customers’ factories',
  stages: [
    { years: '2015–17', loc: 'Teluk Lamong', title: 'Platform established', detail: 'Transit warehouse terminal built from 2015; warehouse and conveyor in commercial operation from 2017', photo: 'photo_tl2015.png' },
    { years: '2019–20', loc: 'Cigading', title: 'Integrated terminal developed', detail: 'Integrated warehouse built from 2019; commercial operations with conveyor from Jetty 1 in 2020', photo: 'photo_cg2020.png' },
    { years: '2020–21', loc: 'Belawan', title: 'Pelindo facility revitalised', detail: 'Warehouse revitalisation started 2020; warehouse and conveyor system operating from 2021', photo: 'photo_bw2020.png' },
    { years: '2024–26', loc: 'Integration & capacity', title: 'Hubs linked to customers', detail: 'Cigading conveyor from Jetty 2 (2024); Teluk Lamong bagging facility (2025); Cigading conveyor into the Bungasari and Tereos factories (2026)', photo: 'photo_cg2026.png' },
    { years: '2026+', loc: 'Next gateways', title: 'Dumai and Ciwandan', detail: 'The model replicated where handling is still conventional; scope on the next slide', map: true },
  ],
  source: 'Source: FKS infrastructure development journey 2015-2026. Photographs: FKS sites.',
  notes: {
    objective: 'Show the journey as a simple chronology: one platform, then additional gateways, then deeper integration into customers’ plants, then the next gateways. Replaces the earlier greenfield / brownfield / expansion framing, which mixed sites and made the timeline hard to follow.',
    talk: 'The platform was built step by step. It started at Teluk Lamong in 2015, with commercial operations from 2017. Cigading followed in 2019 and 2020, and the Belawan facility was revitalised with Pelindo in 2020 and 2021. Since 2024 the emphasis has shifted from new sites to integration and capacity: a second jetty was connected at Cigading, a bagging facility was added at Teluk Lamong, and this year the conveyor was extended straight into the Bungasari and Tereos factories. The next stage is the one we come to on the following slide: replicating the model at Dumai and Ciwandan.',
    sources: 'FKS infrastructure development journey (2015-2026), attached by FKS Business Development: 2015 Teluk Lamong construction of transit warehouse terminal commenced; 2017 Teluk Lamong commissioning and commercial operations of transit warehouse and conveyor; 2019 Cigading integrated warehouse construction commenced; 2020 Cigading commercial operations of warehouse transit and conveyor from Jetty 1, Belawan warehouse revitalisation initiated; 2021 Belawan commercial operations of warehouse and conveyor system; 2024 Cigading conveyor connection from Jetty 2 to integrated warehouse; 2025 Teluk Lamong bagging facility begins commercial operations; 2026 Cigading conveyor extension from integrated warehouse to Bungasari and Tereos factories. Public corroboration: Belawan conveyor inaugurated May 2021 (Bisnis Sumatra); Cigading Sentral Grain Terminal 2 soft launch reported in 2016 with phase 2 in 2020 (FKS Multi Agro, Antara Banten), which the timeline treats as the earlier phase of the same site.',
    calc: 'None.',
    validate: '1) Confirm exact commissioning months and the 2026 Cigading extension status (in operation vs commissioning) at the meeting date and label it accordingly. 2) Reconcile the 2016 Cigading SGT2 soft launch reported in the press with the 2019-2020 dates on the journey slide (phase 1 vs phase 2) and decide whether to show both. 3) Replace photographs with high-resolution originals.',
  },
};

// ---------------------------------------------------------------- SLIDE 8
D.s8 = {
  headline: 'Two identified projects apply the model where handling is still conventional: Ciwandan for imports, Dumai for palm-kernel exports',
  expansions: [
    { k: 'Delivered 2025–26', v: 'Teluk Lamong bagging facility; Cigading conveyor links into the Bungasari and Tereos factories (funded by FKS)' },
    { k: 'Next', v: 'Further capacity at Cigading and Teluk Lamong as demand grows; to be sized' },
  ],
  projects: [
    { name: 'Dumai', where: 'Riau, Sumatra  |  Pelindo dry-bulk terminal (TCK)', tag: 'EXPORT LOADING', num: '~1.3 Mt / yr', numLabel: 'palm kernel expeller and shell cargo base in Riau', rows: [
      { k: 'WHY HERE', v: 'Gateway for Riau’s palm complex; recurring dry-bulk exports' },
      { k: 'GAP TODAY', v: 'Conventional truck-to-vessel loading' },
      { k: 'FKS SCOPE', v: 'Mechanised loading line with Pelindo: dumping pit, intake, conveyor, ship loader, weighbridge' },
      { k: 'UNLOCKS', v: 'Faster loading; initial FKS tariff component of Rp40,000/t under the FKS–Pelindo cooperation terms' },
    ] },
    { name: 'Ciwandan', where: 'Cilegon, Banten  |  Pelindo port beside Cigading', tag: 'IMPORT GATEWAY', num: 'Scope in development', numSize: 20, numLabel: 'capacity and investment to be sized with Pelindo', rows: [
      { k: 'WHY HERE', v: 'Banten cluster, where FKS runs Cigading, Bungasari and Tereos' },
      { k: 'GAP TODAY', v: 'Wheat, corn and soybean meal discharged by grab, hopper and truck' },
      { k: 'FKS SCOPE', v: 'Mechanised discharge, conveyor and transit buffer on the Cigading model' },
      { k: 'UNLOCKS', v: 'A second integrated gateway for Java’s largest western cluster' },
    ] },
  ],
  source: 'Sources: Dumai - FKS–Pelindo cooperation terms for the Dumai dry-bulk terminal (tariff and cargo volume schedule; document status to be confirmed); Pelindo Multi Terminal Dumai. Ciwandan - FKS project screening; Pelindo Regional 2 Banten releases (2026). Estimates subject to final documentation.',
  notes: {
    objective: 'Connect the opportunity on slide 3 to specific, investable next projects. Ciwandan is the direct replication of the Cigading import model next door; Dumai applies the same mechanised conveyor-and-loader handling to Riau’s palm-kernel feed exports and has the most concrete commercial terms. Existing-site expansions are shown but kept secondary.',
    talk: 'Slide 3 said most gateways still handle cargo conventionally. These are the two where FKS has identified a specific project. Dumai is the gateway for Riau’s palm complex. Palm kernel expeller and shell, around 1.3 million tonnes a year in the region, are exported as dry bulk and today are loaded conventionally from trucks. Under the cooperation terms with Pelindo for the Dumai dry-bulk terminal, FKS would install a mechanised loading line, dumping pit, intake, conveyor, ship loader and weighbridge, with an initial FKS tariff component of Rp40,000 per tonne alongside Pelindo’s port services, and both parties would jointly serve the PKE and PKS potential in Riau. Ciwandan is next door to Cigading in the Banten cluster, where FKS already runs the integrated warehouse and holds stakes in Bungasari and Tereos. It still receives wheat, corn and soybean meal by grab and truck, and its soybean-meal volumes grew by more than a quarter this year. The project would replicate the Cigading model there, with capacity sized together with Pelindo. On the existing sites, the 2025 bagging facility at Teluk Lamong and the 2026 factory conveyor at Cigading were funded by FKS and show that the hubs keep growing; further capacity is to be sized.',
    sources: 'DUMAI (from the FKS–Pelindo cooperation document "Tujuan Utama dan Ruang Lingkup Dumai", tariff and cargo volume section, attached; document status MoU vs signed agreement to be confirmed): (1) initial tariff component for FKSSL of Rp40,000/t, comprising dumping pit, intake, conveyor and ship loader Rp37,000/t and weighbridge Rp3,000/t; (2) all tariff components for receiving (warehouse, heavy equipment, weighing), cargodoring (line-1 trucking) and port services (berth and cargo pass) remain Pelindo’s portion at about Rp65,000/t; (3) the parties will jointly socialise the new loading tariff for PKE and PKS at TCK Pelabuhan Dumai; (4) PKE and PKS dry-bulk cargo currently estimated at 1.3 million tonnes per year; the parties agree to jointly serve all PKE and PKS cargo potential in Riau. PKE = palm kernel expeller (bungkil inti sawit); PKS = palm kernel shell (cangkang sawit); TCK = Terminal Curah Kering. Context (FACT): Pelindo Multi Terminal Dumai dry-bulk traffic 2.12 Mt through Q3 2024 (+3.8%), dominated by palm kernel meal, shell and kernel exports (Pelindo Multi Terminal news, https://pelindomultiterminal.co.id/news/kinerja-pelabuhan-dumai-jalur-utama-ekspor-hasil-tani-dan-kebun-riau); period to be confirmed.\nCIWANDAN (FKS screening plus public facts): Pelindo Regional 2 Banten / PTP Nonpetikemas port at Cilegon; handles wheat, corn (dry bulk at berth 05B) and soybean meal for the feed industry; soybean-meal volume 116,926 t in Jan-Aug 2026, +28.4% y/y; dedicated dry-bulk terminal licence at berth 02; no mechanised grain unloader reported (Beritakota, Kompas Money 20 May 2026, Antara). Adjacent Cigading / Krakatau cluster: Bungasari, Cerestar and Pundi Kencana flour mills, Golden Grand Mills, Tereos FKS starch plant, feed mills (Charoen Pokphand, Japfa, CJ, Malindo in Serang-Cikande). Scope, capacity and capex not yet defined.',
    calc: 'Dumai indicative revenue at full capture (DERIVED, not on slide): 1.3 Mt/yr x Rp40,000/t = Rp52 billion per year (~US$3.2m at Rp16,300/US$) for the FKS tariff component, before ramp-up, volume share and operating cost. Combined customer tariff = Rp40,000 (FKS) + ~Rp65,000 (Pelindo) = ~Rp105,000/t.',
    validate: '1) Confirm the Dumai document status (MoU vs signed cooperation agreement, date), the FKSSL entity, term, capex, ramp-up and volume share; brief the presenter so the answer to "is it signed?" is ready. 2) Confirm current loading rates at TCK Dumai and the target rate with the ship loader. 3) Define Ciwandan scope, capacity, capex and Pelindo cooperation structure, and prepare the answer to "why Ciwandan rather than more capacity at Cigading?" (customer set, berth availability, KBS concession scope, Cigading utilisation). 4) Add Ciwandan total food & feed dry-bulk volume (wheat, corn, SBM) and Riau PKE/PKS export statistics (BPS). 5) Provide an indicative capex envelope and timing per project, or state when it will be shared. 6) Decide whether to show the derived Rp52 bn/yr revenue potential once the volume share is agreed.',
  },
};

// ---------------------------------------------------------------- SLIDE 9
D.s9 = {
  headline: 'Danantara would invest directly into the logistics platform alongside FKS Multi Agro, funding the next gateways',
  platform: 'FSL',
  platformSub: 'FKS logistics platform',
  assets: 'Teluk Lamong  ·  Cigading  ·  Belawan',
  pipeline: 'Dumai  ·  Ciwandan  ·  site expansions',
  arrowTop: 'Primary capital injection into FSL',
  arrowBottom: 'Subject to negotiation; any secondary element to be discussed',
  leftNote: 'FSL (simplified; legal entity and perimeter to be confirmed) is wholly owned by FKS Multi Agro and operates the FKS facilities at the three gateways.',
  rightNote: 'Primary proceeds fund Dumai, Ciwandan and existing-site expansion; FKS retains majority ownership and operatorship. Pelindo, FKS’s port partner at four of the five sites, sits within the Danantara portfolio; concession governance to be addressed in the structure.',
  nextSteps: 'Proposed next steps:  NDA and information sharing  ·  site throughput, customer mix and agreement tenors  ·  feasibility model with project and equity returns for Dumai and Ciwandan  ·  agree perimeter, governance and valuation approach',
  source: 'Structure is illustrative and does not imply a confirmed transaction. Ownership percentages, perimeter and terms are subject to negotiation and due diligence.',
  notes: {
    objective: 'Close with a structure that can be understood in seconds: today FKS Multi Agro owns 100% of the logistics platform; post-transaction Danantara would hold an illustrative 49% alongside FKS Multi Agro at 51% through a primary capital injection, and the platform would hold both the operating facilities and the pipeline projects. Do not imply a confirmed transaction. End with the proposed next steps so the open items become a plan.',
    talk: 'The proposed route for Danantara is a direct stake in the logistics platform. Today FSL is wholly owned by FKS Multi Agro and operates the FKS facilities at the three gateways. In the illustrative structure, Danantara would take a forty-nine percent interest through a primary capital injection, with FKS Multi Agro retaining fifty-one percent and operatorship, and the proceeds would fund Dumai, Ciwandan and the expansion of the existing hubs. Any secondary element is open for discussion. One point we want to name rather than leave unsaid: Pelindo, our port partner at four of the five sites, now sits within the Danantara portfolio. We see that as the strategic fit, and we expect the concession governance to be addressed in the structure. The percentage, the perimeter and the terms are all open; what we are proposing today is the shape, and the next steps on the bottom of the slide are how we would get to a term sheet.',
    sources: 'Current ownership and the illustrative post-transaction structure as provided by FKS Business Development (FKS Multi Agro 100% of FSL today; illustrative 51% / 49% post-transaction). No change to the ownership logic has been made. Pipeline projects from slide 8. Public references name the operating entities as Nusa Prima Logistik (Teluk Lamong), PT Sentral Grain Terminal (Cigading) and PT FKS Solusi Logistik (Belawan; abbreviated FKSSL in the Dumai document), all described as FKS Group companies. Pelindo is a state-owned enterprise whose shareholding was consolidated under Danantara Indonesia in 2025 (to be confirmed at meeting date).',
    calc: 'None on the slide. The investment case behind the structure follows the standard project-finance chain: volume x tariff = revenue, less operating cost = EBITDA, less tax, maintenance capex and working capital = project cash flow, set against capex and financing to derive project IRR, equity IRR, payback and valuation. Those metrics are to be developed in the feasibility model and are deliberately not shown until validated.',
    validate: '1) Confirm the full legal name of FSL, whether the three operating entities named above sit under it (transaction perimeter), and whether the listed FKS Multi Agro Tbk is the direct parent (disclosure implications). 2) Provide the counterparty and tenor of each cooperation agreement (Pelindo at Teluk Lamong and Belawan, KBS at Cigading), at least under NDA. 3) Confirm that the entry is a primary capital injection and whether any secondary component is intended; the indicative size. 4) Prepare the feasibility model outputs (project and equity IRR, payback, ROIC) and an indicative capex envelope for the next meeting. 5) Confirm Pelindo’s position within the Danantara portfolio and how concession governance would be handled.',
  },
};

module.exports = D;
