# FKS Group x Danantara Indonesia — strategic investment deck

Editable PowerPoint deck (16:9, 9 slides, full speaker notes) presenting FKS Group's food & feed
port-logistics platform to Danantara Indonesia.

## Deliverable

| File | What it is |
|---|---|
| `FKS_Danantara_Platform_Deck_2026-09-28_v1.pptx` | The deck. Fully editable: native text boxes, shapes, lines, one native chart, editable freeform maps. Only the site photographs and the logo lockup are images. |
| `build/render/deck-01.png` … `deck-09.png` | Rendered slide images from the QA pass (LibreOffice, 110 dpi). |
| `build/research/*.txt` | Research notes with sources (FACT / DERIVED / PROXY / UNVERIFIED) and the six-agent review findings (`review_*.txt`). |

Version history: this is the first version stored in this repository. No earlier deck file existed
in the repository when it was created, so the deck was built from scratch to the agreed storyline.

## Storyline (one message per slide)

1. Cover — integrated port-to-mill logistics; three operating gateways, two identified next projects.
2. Market — ~22 Mt/yr of food & feed raw-material imports, processed in a few coastal clusters, mainly on Java.
3. Opportunity — only three gateways discharge grain mechanically (all built with FKS); the rest work by grab and truck, so the ship waits for the trucks (60 kt cargo ≈ 12 days).
4. FKS operating model — ship-speed discharge into an enclosed conveyor and transit buffer; marine and inland operations decoupled.
5. Value — per 60 kt cargo: ~9 vessel-days (≈US$146k), potential freight saving (to be quantified), ≈US$36k cargo value preserved (illustrative).
6. Operating platform — Teluk Lamong, Cigading, Belawan facts.
7. Track record — 2015-2026 chronology.
8. Pipeline — Dumai (PKE/PKS export loading with Pelindo) and Ciwandan (import gateway on the Cigading model); existing-site expansions.
9. Investment structure — FKS Multi Agro 100% of FSL today; illustrative 51% / 49% with Danantara post-transaction.

## Consistent case

All vessel arithmetic uses one 60,000 t cargo: 5 kt/day conventional (12 days) vs 20 kt/day integrated
(3 days); 9 days x US$16.2k/day = US$145.8k; 12 days x US$16.2k = US$194.4k; 60 kt x US$300/t = US$18.0m;
0.2% x US$18.0m = US$36k.

## Rebuilding the deck

```bash
cd build
npm install            # pptxgenjs, sharp, react-icons
node build.js deck_raw.pptx
python3 postprocess_map.py deck_raw.pptx deck.pptx   # injects the editable coastline freeforms
python3 render.py deck.pptx 110                       # LibreOffice -> PDF -> PNG, for QA
```

Content lives in `build/data.js` (all text, numbers and speaker notes); layout in `build/build.js`;
design tokens and helpers in `build/lib.js`; shape pictograms in `build/picto.js`.

## Open data points (also listed in each slide's speaker notes, section 5)

- Replace raster logo lockup with vector brand files.
- Confirm facility figures (unloader rates, storage) against FKS engineering data; press sources differ slightly.
- Quantify the freight / port-cost saving from FKS voyage data (slide 5, "better economics").
- Validate the 0.2 pp cargo-loss differential with customer weighbridge data.
- Confirm Dumai document status, entity (FKSSL), capex, ramp-up and volume share; define Ciwandan scope.
- Confirm the legal name and perimeter of FSL for slide 9.
