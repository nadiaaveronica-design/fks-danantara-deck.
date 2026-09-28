'use strict';
// FKS Group x Danantara Indonesia — investment discussion deck (pptxgenjs)
const pptxgen = require('pptxgenjs');
const path = require('path');
const L = require('./lib');
const P = require('./picto');
const { C, W, H, M, ASSETS, text, header, footer, rect, rrect, oval, line, arrow, stat, tag, mapLayer, projector, mapHeight, notes } = L;
const DATA = require('./data');

const OUT = process.argv[2] || 'deck_raw.pptx';
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'FKS Group — Business Development';
pres.company = 'FKS Group';
pres.title = 'FKS food & feed logistics platform — discussion materials for Danantara Indonesia';

const ID_BBOX = [94.5, -11.5, 141.5, 6.5];     // whole archipelago
const WEST_BBOX = [94.5, -9.5, 120.5, 6.5];    // Sumatra + Java + Kalimantan (west/central)

// --------------------------------------------------------------------------------------
// SLIDE 1 — COVER
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  // right navy panel
  rect(s, 7.6, 0, W - 7.6, H, { fill: { color: C.navy } });
  // logos
  s.addImage({ path: path.join(ASSETS, 'logo_fks_raw.png'), x: M, y: 0.55, w: 0.95, h: 0.79 });
  text(s, 'FOOD & FEED LOGISTICS PLATFORM', M, 2.35, 6.4, 0.3, { fontSize: 10, bold: true, color: C.gold, charSpacing: 3 });
  text(s, 'Integrated port-to-mill logistics for Indonesia’s food & feed supply chain', M, 2.7, 6.7, 1.9, { fontSize: 30, bold: true, color: C.navy, lineSpacingMultiple: 1.05 });
  text(s, 'Strategic investment discussion', M, 4.75, 6.4, 0.4, { fontSize: 16, color: C.ink });
  text(s, 'Prepared for Danantara Indonesia  |  ' + DATA.date, M, 5.15, 6.4, 0.35, { fontSize: 12, color: C.grey });
  text(s, 'Strictly private and confidential. Illustrative figures are labelled as such and remain subject to due diligence.', M, 6.75, 6.6, 0.4, { fontSize: 8, color: C.grey2 });

  // map on navy
  const mw = 5.0, mh = mapHeight(mw, ID_BBOX), mx = 7.6 + (W - 7.6 - mw) / 2, my = 2.55;
  mapLayer(s, 'neighbours', mx, my, mw, mh, ID_BBOX, { fill: '17305A', lineColor: C.navy, lineWidth: 0.5 });
  mapLayer(s, 'Indonesia', mx, my, mw, mh, ID_BBOX, { fill: '2E5185', lineColor: C.navy, lineWidth: 0.5 });
  const pj = projector(mx, my, mw, mh, ID_BBOX);
  for (const site of DATA.sites.filter(v => v.status === 'operating')) {
    const [x, y] = pj(site.lon, site.lat);
    oval(s, x - 0.075, y - 0.075, 0.15, 0.15, { fill: { color: C.gold }, line: { color: C.navy, width: 1 } });
  }
  for (const site of DATA.sites.filter(v => v.status === 'pipeline')) {
    const [x, y] = pj(site.lon, site.lat);
    oval(s, x - 0.065, y - 0.065, 0.13, 0.13, { fill: { color: C.navy }, line: { color: C.gold, width: 1.25 } });
  }
  // legend
  const ly = my + mh + 0.35;
  oval(s, mx, ly + 0.03, 0.13, 0.13, { fill: { color: C.gold }, line: { color: C.navy, width: 1 } });
  text(s, 'Integrated gateways in operation: Belawan, Cigading, Teluk Lamong', mx + 0.22, ly, 4.8, 0.22, { fontSize: 9.5, color: C.white });
  oval(s, mx, ly + 0.36, 0.13, 0.13, { fill: { color: C.navy }, line: { color: C.gold, width: 1.25 } });
  text(s, 'Identified next projects: Dumai, Ciwandan', mx + 0.22, ly + 0.33, 4.8, 0.22, { fontSize: 9.5, color: C.white });
  text(s, 'Three integrated gateways operating on Java and Sumatra since 2017', mx, 1.35, mw, 0.9, { fontSize: 15, color: C.white, bold: true, lineSpacingMultiple: 1.1 });

  notes(s, {
    objective: 'Set the frame in one line: FKS operates an integrated port-to-mill logistics platform for Indonesia’s food & feed supply chain, and is opening it to a strategic investor. The map anchors the three operating gateways and the two identified next projects that the deck returns to on slides 6-9.',
    talk: 'FKS Group has imported and processed food and feed raw materials in Indonesia for decades. Over the last eleven years it has built a dedicated logistics layer at three gateways that moves grain from ship to mill without conventional grab-and-truck handling. Today we want to walk through why that layer matters for the country, what it delivers, where it can be replicated next, and how Danantara could participate.',
    sources: 'FKS Group corporate materials; FKS infrastructure development journey slide (2015-2026); site coordinates from public port locations.',
    calc: 'None on this slide.',
    validate: 'Replace the raster logo lockup with vector brand files (FKS Group and Danantara Indonesia) from the brand team before external use. Confirm the exact presenting entity name and the meeting date.',
  });
}

// --------------------------------------------------------------------------------------
// SLIDE 2 — MARKET SIZE -> DEMAND CLUSTERS -> GATEWAY REQUIREMENT
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Market', DATA.s2.headline);

  // LEFT: market size
  const lx = M, lw = 3.6;
  text(s, 'ANNUAL IMPORTS OF CORE FOOD & FEED RAW MATERIALS', lx, 1.72, lw, 0.24, { fontSize: 9, bold: true, color: C.grey, charSpacing: 1 });
  text(s, DATA.s2.total, lx, 1.98, lw, 0.95, { fontSize: 56, bold: true, color: C.navy, valign: 'bottom' });
  text(s, DATA.s2.totalLabel, lx, 2.95, lw, 0.3, { fontSize: 11, color: C.ink });
  // composition chart (native)
  const cats = DATA.s2.composition.map(c => c.name), vals = DATA.s2.composition.map(c => c.mt);
  s.addChart('bar', [{ name: 'Mt per year', labels: cats, values: vals }], {
    x: lx - 0.05, y: 3.3, w: lw + 0.15, h: 2.05,
    barDir: 'bar', barGapWidthPct: 55,
    chartColors: [C.navy],
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 10, dataLabelColor: C.ink, dataLabelFontFace: L.FONT, dataLabelFormatCode: '0.0',
    catAxisLabelFontSize: 10, catAxisLabelColor: C.ink, catAxisLabelFontFace: L.FONT, catAxisOrientation: 'maxMin',
    valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, valAxisMaxVal: Math.max(...vals) * 1.28,
    catAxisLineShow: false, valAxisLineShow: false, showLegend: false, showTitle: false,
  });
  text(s, DATA.s2.chartNote, lx, 5.33, lw + 0.1, 0.36, { fontSize: 7.5, color: C.grey2 });

  // MIDDLE: processing layer
  const cx = 4.55, cw = 2.55;
  rect(s, cx, 1.72, cw, 3.55, { fill: { color: C.light } });
  text(s, 'PROCESSED BY', cx + 0.22, 1.9, cw - 0.4, 0.24, { fontSize: 9, bold: true, color: C.grey, charSpacing: 1 });
  stat(s, cx + 0.22, 2.12, cw - 0.4, DATA.s2.flourMills, DATA.s2.flourLabel, { numSize: 26, labelSize: 10, labelH: 0.28 });
  stat(s, cx + 0.22, 2.9, cw - 0.4, DATA.s2.feedMills, DATA.s2.feedLabel, { numSize: 26, labelSize: 10, labelH: 0.28 });
  line(s, cx + 0.22, 3.76, cx + cw - 0.22, 3.76, { line: { color: C.line, width: 0.75 } });
  text(s, 'CONCENTRATED ON JAVA', cx + 0.22, 3.88, cw - 0.4, 0.24, { fontSize: 9, bold: true, color: C.grey, charSpacing: 1 });
  stat(s, cx + 0.22, 4.06, (cw - 0.4) / 2, DATA.s2.javaShare, DATA.s2.javaLabel, { numSize: 20, labelSize: 8.5, labelH: 0.4 });
  stat(s, cx + 0.22 + (cw - 0.4) / 2, 4.06, (cw - 0.4) / 2, DATA.s2.feedShare, DATA.s2.feedShareLabel, { numSize: 20, labelSize: 8.5, labelH: 0.4 });
  text(s, DATA.s2.shareBasis, cx + 0.22, 4.88, cw - 0.4, 0.36, { fontSize: 7.5, color: C.grey2 });

  // RIGHT: map with demand clusters
  const mx = 7.45, mw = W - M - mx, mh = mapHeight(mw, ID_BBOX), my = 1.72;
  rect(s, mx, my, mw, mh, { fill: { color: C.sea } });
  mapLayer(s, 'neighbours', mx, my, mw, mh, ID_BBOX, { fill: C.land, lineColor: C.sea, lineWidth: 0.5 });
  mapLayer(s, 'Indonesia', mx, my, mw, mh, ID_BBOX, { fill: C.landID, lineColor: C.sea, lineWidth: 0.5 });
  const pj = projector(mx, my, mw, mh, ID_BBOX);
  // bubbles: size by share (diameter ~ sqrt(share))
  for (const cl of DATA.s2.clusters) {
    const [x, y] = pj(cl.lon, cl.lat);
    const d = 0.16 + Math.sqrt(cl.weight) * 0.42;
    oval(s, x - d / 2, y - d / 2, d, d, { fill: { color: C.gold, transparency: 25 }, line: { color: C.goldDark, width: 0.75 } });
    const tx = x + (cl.dx || 0.16), ty = y + (cl.dy || -0.11);
    text(s, cl.name, tx, ty, 1.6, 0.2, { fontSize: 8.5, bold: true, color: C.navy, align: cl.align || 'left' });
    if (cl.sub) text(s, cl.sub, tx, ty + 0.16, 1.6, 0.18, { fontSize: 7.5, color: C.grey, align: cl.align || 'left' });
  }
  text(s, 'MAIN FLOUR AND FEED MILLING CLUSTERS', mx, my + mh + 0.1, mw, 0.22, { fontSize: 8.5, bold: true, color: C.grey, charSpacing: 1 });
  text(s, DATA.s2.mapNote, mx, my + mh + 0.32, mw, 0.5, { fontSize: 9, color: C.ink, lineSpacingMultiple: 1.05 });
  // bubble legend
  const lgx = mx + 0.05, lgy = my + mh + 0.86;
  oval(s, lgx, lgy + 0.02, 0.14, 0.14, { fill: { color: C.gold, transparency: 25 }, line: { color: C.goldDark, width: 0.75 } });
  text(s, 'Bubble size indicates relative processing capacity in the cluster (proxy, see notes)', lgx + 0.22, lgy, mw - 0.3, 0.2, { fontSize: 7.5, color: C.grey2 });

  // BOTTOM: the bridge
  const by = 5.72, bh = 0.86, gap = 0.42;
  const bw = (W - 2 * M - 2 * gap) / 3;
  const steps = DATA.s2.bridge;
  for (let i = 0; i < 3; i++) {
    const bx = M + i * (bw + gap);
    const isLast = i === 2;
    rect(s, bx, by, bw, bh, { fill: { color: isLast ? C.navy : C.light } });
    text(s, steps[i].k, bx + 0.2, by + 0.1, bw - 0.4, 0.22, { fontSize: 8.5, bold: true, color: isLast ? C.gold : C.grey, charSpacing: 1 });
    text(s, steps[i].v, bx + 0.2, by + 0.32, bw - 0.4, bh - 0.4, { fontSize: 11, bold: true, color: isLast ? C.white : C.navy, lineSpacingMultiple: 1.05 });
    if (i < 2) {
      s.addShape('chevron', { x: bx + bw + 0.1, y: by + bh / 2 - 0.13, w: 0.22, h: 0.26, fill: { color: C.gold }, line: { color: C.gold, width: 0 } });
    }
  }

  footer(s, 2, DATA.s2.source);
  notes(s, DATA.s2.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 3 — THE CONVENTIONAL GATEWAY: SHIP PACED BY TRUCKS
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Opportunity', DATA.s3.headline);

  // top strip: gateway landscape (three tiles)
  const ty = 1.72, th = 1.28, tg = 0.25, tw = (W - 2 * M - 2 * tg) / 3;
  DATA.s3.tiles.forEach((t, i) => {
    const tx = M + i * (tw + tg);
    rect(s, tx, ty, tw, th, { fill: { color: i === 1 ? C.navy : C.light } });
    text(s, t.num, tx + 0.25, ty + 0.12, tw - 0.5, 0.62, { fontSize: 34, bold: true, color: i === 1 ? C.white : C.navy, valign: 'bottom' });
    text(s, t.label, tx + 0.25, ty + 0.78, tw - 0.5, 0.42, { fontSize: 10.5, color: i === 1 ? C.white : C.ink, lineSpacingMultiple: 1.05 });
  });
  text(s, DATA.s3.tileNote, M, ty + th + 0.05, W - 2 * M, 0.22, { fontSize: 7.5, color: C.grey2 });

  // flow schematic
  const fy = 3.75, fh = 1.45;
  text(s, 'WHAT HAPPENS TODAY AT A CONVENTIONAL GATEWAY', M, 3.3, 4.6, 0.22, { fontSize: 8.5, bold: true, color: C.grey, charSpacing: 1 });
  const stations = [
    { k: 'VESSEL', v: 'Bulk carrier alongside', draw: (x, y, w, h) => { P.ship(s, x + 0.05, y + 0.2, w - 0.1, h * 0.75, C.conv); P.water(s, x - 0.1, y + h * 0.92, w + 0.2, C.sea); } },
    { k: 'GRAB', v: 'Crane lifts ~10-20 t per cycle', draw: (x, y, w, h) => P.crane(s, x + 0.2, y + 0.05, w - 0.4, h * 0.9, C.conv) },
    { k: 'HOPPER', v: 'Open hopper feeds trucks one at a time', draw: (x, y, w, h) => P.hopper(s, x + 0.35, y + 0.15, w - 0.7, h * 0.8, C.conv) },
    { k: 'TRUCK', v: 'Road haulage to the mill', draw: (x, y, w, h) => { P.truck(s, x + 0.15, y + 0.3, w * 0.55, h * 0.5, C.conv); P.truck(s, x + 0.15 + w * 0.6, y + 0.3, w * 0.35, h * 0.5, C.conv); } },
    { k: 'CUSTOMER', v: 'Mill receives and weighs cargo', draw: (x, y, w, h) => P.mill(s, x + 0.3, y + 0.2, w - 0.6, h * 0.75, C.conv) },
  ];
  const sw = 2.15, sg = (W - 2 * M - 5 * sw) / 4;
  stations.forEach((st, i) => {
    const sx = M + i * (sw + sg);
    st.draw(sx, fy, sw, fh);
    text(s, st.k, sx, fy + fh + 0.08, sw, 0.22, { fontSize: 10, bold: true, color: C.navy, align: 'center', charSpacing: 1 });
    text(s, st.v, sx - 0.1, fy + fh + 0.3, sw + 0.2, 0.36, { fontSize: 9, color: C.grey, align: 'center', lineSpacingMultiple: 1.0 });
    if (i < 4) arrow(s, sx + sw + 0.06, fy + fh * 0.55, sx + sw + sg - 0.06, fy + fh * 0.55, { line: { color: C.grey2, width: 1.25, endArrowType: 'triangle' } });
  });
  // bottleneck bracket over GRAB -> TRUCK
  const bx1 = M + 1 * (sw + sg), bx2 = M + 3 * (sw + sg) + sw;
  line(s, bx1, fy - 0.1, bx2, fy - 0.1, { line: { color: C.gold, width: 1.5 } });
  line(s, bx1, fy - 0.1, bx1, fy + 0.03, { line: { color: C.gold, width: 1.5 } });
  line(s, bx2, fy - 0.1, bx2, fy + 0.03, { line: { color: C.gold, width: 1.5 } });
  rrect(s, (bx1 + bx2) / 2 - 1.55, fy - 0.26, 3.1, 0.32, { rectRadius: 0.16, fill: { color: C.white }, line: { color: C.white, width: 0 } });
  text(s, 'The ship is paced by the trucks', (bx1 + bx2) / 2 - 1.55, fy - 0.26, 3.1, 0.32, { fontSize: 11, bold: true, color: C.goldDark, align: 'center', valign: 'middle' });

  // consequence strip: 60 kt case
  const cy = 5.95, ch = 0.75;
  rect(s, M, cy, W - 2 * M, ch, { fill: { color: C.navy } });
  const items = DATA.s3.case;
  const iw = (W - 2 * M) / items.length;
  items.forEach((it, i) => {
    const ix = M + i * iw;
    text(s, it.num, ix + 0.3, cy + 0.08, iw - 0.6, 0.4, { fontSize: 20, bold: true, color: i === items.length - 1 ? C.gold : C.white, valign: 'middle' });
    text(s, it.label, ix + 0.3, cy + 0.46, iw - 0.6, 0.26, { fontSize: 9, color: 'C7D0DD' });
    if (i < items.length - 1) text(s, '→', ix + iw - 0.25, cy + 0.08, 0.3, 0.4, { fontSize: 18, color: C.gold, valign: 'middle', align: 'center' });
  });

  footer(s, 3, DATA.s3.source);
  notes(s, DATA.s3.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 4 — THE FKS OPERATING MODEL
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'FKS operating model', DATA.s4.headline);

  // ground / quay line
  const gy = 4.55;            // ground level
  rect(s, 3.35, gy, W - M - 3.35, 0.09, { fill: { color: C.light2 } });
  // sea
  rect(s, M, gy + 0.02, 2.85, 0.07, { fill: { color: C.sea } });
  // vessel (navy)
  P.ship(s, M + 0.05, 3.55, 2.75, 1.0, C.navy2, { hatches: 5 });
  // unloader on the quay
  P.unloader(s, 2.55, 2.75, 1.45, 1.8, C.navy);
  // conveyor gallery: elevated from unloader to buffer
  P.conveyor(s, 3.6, 2.95, 2.75, C.navy3, { legs: 3, legH: 1.6, thickness: 0.1 });
  // buffer: silos + warehouse, highlighted
  const bx = 6.35, bwid = 2.55;
  rrect(s, bx - 0.15, 2.55, bwid + 0.3, 2.0, { rectRadius: 0.1, fill: { color: C.goldLight }, line: { color: C.gold, width: 1.25 } });
  P.silos(s, bx + 0.05, 2.85, 1.05, 1.7, 3, C.navy);
  P.warehouse(s, bx + 1.2, 3.15, 1.3, 1.4, C.navy);
  // outbound conveyor from buffer to loading bay
  P.conveyor(s, bx + bwid + 0.15, 3.5, 0.7, C.navy3, { legs: 2, legH: 1.05, thickness: 0.08 });
  // controlled loading: bay + trucks
  const lx = 9.55;
  rect(s, lx, 3.35, 1.25, 0.14, { fill: { color: C.navy } });    // loading canopy
  rect(s, lx + 0.05, 3.49, 0.06, 0.55, { fill: { color: C.navy } });
  rect(s, lx + 1.14, 3.49, 0.06, 0.55, { fill: { color: C.navy } });
  P.truck(s, lx + 0.12, 3.85, 1.0, 0.7, C.navy2);
  // mill
  P.mill(s, 11.45, 3.35, 1.25, 1.2, C.navy);
  // direct conveyor to mill (dashed gold)
  line(s, bx + bwid + 0.15, 3.05, 11.5, 3.05, { line: { color: C.gold, width: 1.5, dashType: 'dash' } });
  line(s, 11.5, 3.05, 11.5, 3.35, { line: { color: C.gold, width: 1.5, dashType: 'dash' } });
  text(s, 'Direct conveyor to mill where applicable', 9.15, 2.72, 3.5, 0.28, { fontSize: 8.5, color: C.goldDark, italic: true, align: 'right' });
  // flow arrows (thin, grey) along the ground
  arrow(s, 2.35, 4.85, 2.65, 4.85, { line: { color: C.grey2, width: 1 } });

  // step labels
  const steps = DATA.s4.steps; // [{n,k,v,x,w}]
  steps.forEach(st => {
    oval(s, st.x, 1.78, 0.3, 0.3, { fill: { color: st.hi ? C.gold : C.navy } });
    text(s, String(st.n), st.x, 1.78, 0.3, 0.3, { fontSize: 10, bold: true, color: C.white, align: 'center', valign: 'middle' });
    text(s, st.k, st.x + 0.38, 1.78, st.w - 0.38, 0.3, { fontSize: 10, bold: true, color: C.navy, valign: 'middle' });
    text(s, st.v, st.x, 2.1, st.w, 0.5, { fontSize: 8.5, color: C.grey, lineSpacingMultiple: 1.0 });
  });

  // brackets: marine vs inland, decoupled at buffer
  const by = 4.85;
  const mL = M, mR = bx - 0.25, iL = bx + bwid + 0.25, iR = W - M;
  line(s, mL, by, mR, by, { line: { color: C.navy, width: 1.25 } });
  line(s, mL, by, mL, by - 0.1, { line: { color: C.navy, width: 1.25 } });
  line(s, mR, by, mR, by - 0.1, { line: { color: C.navy, width: 1.25 } });
  text(s, 'MARINE SIDE  —  runs at ship speed', mL, by + 0.06, mR - mL, 0.24, { fontSize: 9, bold: true, color: C.navy, align: 'center', charSpacing: 1 });
  line(s, iL, by, iR, by, { line: { color: C.navy, width: 1.25 } });
  line(s, iL, by, iL, by - 0.1, { line: { color: C.navy, width: 1.25 } });
  line(s, iR, by, iR, by - 0.1, { line: { color: C.navy, width: 1.25 } });
  text(s, 'INLAND SIDE  —  runs at mill demand', iL, by + 0.06, iR - iL, 0.24, { fontSize: 9, bold: true, color: C.navy, align: 'center', charSpacing: 1 });
  tag(s, 'DECOUPLED BY THE BUFFER', mR + 0.05, by - 0.13, iL - mR - 0.1, { fill: C.gold, color: C.white, size: 8, h: 0.27 });

  // outcomes row
  const oy = 5.55, oh = 1.05, og = 0.25, ow = (W - 2 * M - 2 * og) / 3;
  DATA.s4.outcomes.forEach((o, i) => {
    const ox = M + i * (ow + og);
    rect(s, ox, oy, ow, oh, { fill: { color: C.light } });
    text(s, o.num, ox + 0.25, oy + 0.1, ow - 0.5, 0.45, { fontSize: 20, bold: true, color: C.navy, valign: 'middle' });
    text(s, o.label, ox + 0.25, oy + 0.55, ow - 0.5, 0.45, { fontSize: 10, color: C.ink, lineSpacingMultiple: 1.05 });
  });

  footer(s, 4, DATA.s4.source);
  notes(s, DATA.s4.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 5 — VALUE PER 60 KT CARGO
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Value created', DATA.s5.headline);

  // left: days alongside comparison
  const lx = M, lw = 4.3;
  text(s, 'DAYS ALONGSIDE PER 60 KT CARGO', lx, 1.75, lw, 0.24, { fontSize: 9, bold: true, color: C.grey, charSpacing: 1 });
  const barX = lx, barMax = 3.35, perDay = barMax / 12;
  const rows = [
    { k: 'Conventional gateway', sub: '~5 kt/day discharge', days: 12, color: C.conv },
    { k: 'FKS integrated gateway', sub: '~20 kt/day discharge', days: 3, color: C.navy },
  ];
  rows.forEach((r, i) => {
    const ry = 2.15 + i * 1.05;
    text(s, r.k, barX, ry, lw, 0.24, { fontSize: 11, bold: true, color: C.navy });
    text(s, r.sub, barX, ry + 0.22, lw, 0.2, { fontSize: 8.5, color: C.grey });
    rect(s, barX, ry + 0.46, perDay * r.days, 0.36, { fill: { color: r.color } });
    text(s, `~${r.days} days`, barX + perDay * r.days + 0.1, ry + 0.46, 1.2, 0.36, { fontSize: 12, bold: true, color: r.color === C.conv ? C.ink : C.navy, valign: 'middle' });
  });
  // axis ticks
  for (let d = 0; d <= 12; d += 3) {
    line(s, barX + perDay * d, 4.3, barX + perDay * d, 4.38, { line: { color: C.grey2, width: 0.75 } });
    text(s, String(d), barX + perDay * d - 0.2, 4.4, 0.4, 0.18, { fontSize: 7.5, color: C.grey2, align: 'center' });
  }
  line(s, barX, 4.3, barX + barMax, 4.3, { line: { color: C.line, width: 0.75 } });
  text(s, 'days', barX + barMax + 0.1, 4.38, 0.5, 0.2, { fontSize: 7.5, color: C.grey2 });
  // big saving
  rect(s, lx, 4.85, lw, 1.45, { fill: { color: C.light } });
  text(s, '~9', lx + 0.25, 4.92, 1.3, 0.9, { fontSize: 48, bold: true, color: C.navy, valign: 'middle' });
  text(s, 'vessel-days saved per 60 kt cargo', lx + 1.55, 4.98, lw - 1.75, 0.5, { fontSize: 13, bold: true, color: C.navy, valign: 'middle', lineSpacingMultiple: 1.05 });
  text(s, '12 days conventional less 3 days integrated, at the illustrative discharge rates shown', lx + 1.55, 5.5, lw - 1.75, 0.65, { fontSize: 8.5, color: C.grey, lineSpacingMultiple: 1.05 });

  // right: three benefit panels
  const px0 = 5.35, pg = 0.22, pw = (W - M - px0 - 2 * pg) / 3, py = 1.75, ph = 4.55;
  DATA.s5.panels.forEach((p, i) => {
    const px = px0 + i * (pw + pg);
    rect(s, px, py, pw, ph, { fill: { color: i === 0 ? C.navy : C.light } });
    const dark = i === 0;
    text(s, p.k, px + 0.25, py + 0.22, pw - 0.5, 0.26, { fontSize: 10, bold: true, color: dark ? C.gold : C.goldDark, charSpacing: 2 });
    text(s, p.head, px + 0.25, py + 0.5, pw - 0.5, 0.6, { fontSize: 11, color: dark ? 'C7D0DD' : C.ink, lineSpacingMultiple: 1.05 });
    text(s, p.num, px + 0.25, py + 1.1, pw - 0.5, 0.8, { fontSize: p.numSize || 28, bold: true, color: dark ? C.white : C.navy, valign: 'middle', lineSpacingMultiple: 1.0 });
    text(s, p.numLabel, px + 0.25, py + 1.92, pw - 0.5, 0.5, { fontSize: 10.5, bold: true, color: dark ? C.white : C.navy, lineSpacingMultiple: 1.05 });
    text(s, p.basis, px + 0.25, py + 2.45, pw - 0.5, 0.95, { fontSize: 9, color: dark ? 'C7D0DD' : C.grey, lineSpacingMultiple: 1.05 });
    tag(s, p.tag, px + 0.25, py + ph - 0.6, pw - 0.5, { fill: dark ? C.navy2 : C.white, color: dark ? C.gold : C.goldDark, size: 7.5, h: 0.3 });
    if (p.mini === 'parcels') {
      // mini graphic: 2 x 30 kt vs 1 x 60 kt
      const gx = px + 0.25, gy = py + 3.42;
      P.ship(s, gx, gy, 0.7, 0.28, C.grey2, { hatches: 2 });
      P.ship(s, gx + 0.8, gy, 0.7, 0.28, C.grey2, { hatches: 2 });
      text(s, '2 × 30 kt', gx, gy + 0.3, 1.5, 0.18, { fontSize: 7.5, color: C.grey });
      text(s, 'vs', gx + 1.55, gy + 0.03, 0.3, 0.25, { fontSize: 9, color: C.grey, align: 'center' });
      P.ship(s, gx + 1.9, gy - 0.06, 1.05, 0.38, C.navy, { hatches: 4 });
      text(s, '1 × 60 kt', gx + 1.9, gy + 0.3, 1.2, 0.18, { fontSize: 7.5, color: C.navy, bold: true });
    }
  });
  text(s, DATA.s5.perTonne, M, 6.42, W - 2 * M, 0.28, { fontSize: 9, color: C.grey });

  footer(s, 5, DATA.s5.source);
  notes(s, DATA.s5.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 6 — FKS ALREADY OPERATES THE MODEL AT SCALE
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Operating platform', DATA.s6.headline);

  // top stats
  const st = DATA.s6.stats;
  const sw = (W - 2 * M) / st.length;
  st.forEach((v, i) => {
    stat(s, M + i * sw, 1.72, sw - 0.3, v.num, v.label, { numSize: 30, labelSize: 10.5, labelH: 0.3 });
  });
  line(s, M, 2.85, W - M, 2.85, { line: { color: C.line, width: 0.75 } });

  // three site cards
  const cy = 3.05, cg = 0.3, cw = (W - 2 * M - 2 * cg) / 3, ch = 3.55;
  DATA.s6.sites.forEach((site, i) => {
    const cx = M + i * (cw + cg);
    rect(s, cx, cy, cw, ch, { fill: { color: C.light } });
    s.addImage({ path: path.join(ASSETS, site.photo), x: cx, y: cy, w: cw, h: 1.5, sizing: { type: 'cover', w: cw, h: 1.5 }, rounding: false });
    text(s, site.name.toUpperCase(), cx + 0.25, cy + 1.65, cw - 0.5, 0.26, { fontSize: 12, bold: true, color: C.navy, charSpacing: 1 });
    text(s, site.where, cx + 0.25, cy + 1.9, cw - 0.5, 0.22, { fontSize: 9, color: C.grey });
    const offs = [2.22, 2.54, 3.12];
    site.rows.forEach((r, j) => {
      const ry = cy + offs[j];
      text(s, r.k, cx + 0.25, ry, 0.85, 0.3, { fontSize: 8, bold: true, color: C.grey, charSpacing: 1, valign: 'top' });
      text(s, r.v, cx + 1.1, ry, cw - 1.35, j === 1 ? 0.5 : 0.36, { fontSize: 9.5, color: C.ink, valign: 'top', lineSpacingMultiple: 1.0 });
    });
  });

  footer(s, 6, DATA.s6.source);
  notes(s, DATA.s6.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 7 — THE JOURNEY
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Track record', DATA.s7.headline);

  const stages = DATA.s7.stages;
  const n = stages.length, cg = 0.28, cw = (W - 2 * M - (n - 1) * cg) / n;
  const ty = 4.62; // timeline y
  line(s, M, ty, W - M, ty, { line: { color: C.line, width: 1.5 } });
  stages.forEach((st, i) => {
    const cx = M + i * (cw + cg);
    const last = i === n - 1;
    // photo
    if (st.photo) {
      s.addImage({ path: path.join(ASSETS, st.photo), x: cx, y: 1.85, w: cw, h: 2.15, sizing: { type: 'cover', w: cw, h: 2.15 } });
    } else {
      rect(s, cx, 1.85, cw, 2.15, { fill: { color: C.navy } });
      text(s, st.placeholder, cx + 0.2, 1.85, cw - 0.4, 2.15, { fontSize: 10, color: C.white, align: 'center', valign: 'middle', lineSpacingMultiple: 1.1 });
    }
    // year chip on the timeline
    const chipW = 1.0;
    rrect(s, cx + cw / 2 - chipW / 2, ty - 0.17, chipW, 0.34, { rectRadius: 0.17, fill: { color: last ? C.gold : C.navy }, line: { color: last ? C.gold : C.navy, width: 0 } });
    text(s, st.years, cx + cw / 2 - chipW / 2, ty - 0.17, chipW, 0.34, { fontSize: 10, bold: true, color: C.white, align: 'center', valign: 'middle' });
    line(s, cx + cw / 2, 4.0, cx + cw / 2, ty - 0.17, { line: { color: C.line, width: 1 } });
    // location + milestone
    text(s, st.loc.toUpperCase(), cx, ty + 0.35, cw, 0.28, { fontSize: 11.5, bold: true, color: C.navy, align: 'center', charSpacing: 1 });
    text(s, st.title, cx, ty + 0.65, cw, 0.3, { fontSize: 10.5, bold: true, color: last ? C.goldDark : C.ink, align: 'center' });
    text(s, st.detail, cx + 0.05, ty + 0.98, cw - 0.1, 0.9, { fontSize: 8.5, color: C.grey, align: 'center', lineSpacingMultiple: 1.05 });
  });

  footer(s, 7, DATA.s7.source);
  notes(s, DATA.s7.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 8 — PIPELINE: DUMAI AND CIWANDAN
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Pipeline', DATA.s8.headline);

  // map (western Indonesia)
  const mx = M, mw = 4.55, mh = mapHeight(mw, WEST_BBOX), my = 1.75;
  rect(s, mx, my, mw, mh, { fill: { color: C.sea } });
  mapLayer(s, 'neighbours', mx, my, mw, mh, WEST_BBOX, { fill: C.land, lineColor: C.sea, lineWidth: 0.5 });
  mapLayer(s, 'Indonesia', mx, my, mw, mh, WEST_BBOX, { fill: C.landID, lineColor: C.sea, lineWidth: 0.5 });
  const pj = projector(mx, my, mw, mh, WEST_BBOX);
  for (const site of DATA.sites) {
    const [x, y] = pj(site.lon, site.lat);
    const pipe = site.status === 'pipeline';
    if (pipe) {
      oval(s, x - 0.11, y - 0.11, 0.22, 0.22, { fill: { color: C.gold }, line: { color: C.white, width: 1 } });
    } else {
      oval(s, x - 0.08, y - 0.08, 0.16, 0.16, { fill: { color: C.navy }, line: { color: C.white, width: 1 } });
    }
    const tx = x + (site.dx == null ? 0.16 : site.dx), ty = y + (site.dy == null ? -0.12 : site.dy);
    text(s, site.name, tx, ty, 1.5, 0.2, { fontSize: 9, bold: true, color: pipe ? C.goldDark : C.navy, align: site.align || 'left' });
    if (site.tag) text(s, site.tag, tx, ty + 0.17, 1.5, 0.18, { fontSize: 7.5, color: C.grey, align: site.align || 'left' });
  }
  // legend
  const ly = my + mh + 0.12;
  oval(s, mx, ly + 0.03, 0.14, 0.14, { fill: { color: C.navy } });
  text(s, 'Operating integrated gateway', mx + 0.22, ly, 2.2, 0.2, { fontSize: 8.5, color: C.ink });
  oval(s, mx + 2.3, ly + 0.03, 0.14, 0.14, { fill: { color: C.gold } });
  text(s, 'Identified next project', mx + 2.52, ly, 2.0, 0.2, { fontSize: 8.5, color: C.ink });

  // existing-site expansions (under the map)
  const ey = ly + 0.45;
  rect(s, mx, ey, mw, 6.62 - ey, { fill: { color: C.light } });
  text(s, 'EXISTING-SITE EXPANSIONS', mx + 0.22, ey + 0.14, mw - 0.4, 0.22, { fontSize: 8.5, bold: true, color: C.grey, charSpacing: 1 });
  DATA.s8.expansions.forEach((e, i) => {
    const ry = ey + 0.42 + i * 0.5;
    text(s, e.k, mx + 0.22, ry, 1.35, 0.4, { fontSize: 9.5, bold: true, color: C.navy });
    text(s, e.v, mx + 1.55, ry, mw - 1.75, 0.45, { fontSize: 9, color: C.ink, lineSpacingMultiple: 1.0 });
  });

  // project panels
  const px0 = mx + mw + 0.35, pg = 0.3, pw = (W - M - px0 - pg) / 2, py = 1.75, ph = 4.87;
  DATA.s8.projects.forEach((p, i) => {
    const px = px0 + i * (pw + pg);
    rect(s, px, py, pw, ph, { fill: { color: C.white }, line: { color: C.line, width: 1 } });
    rect(s, px, py, pw, 0.95, { fill: { color: C.navy } });
    text(s, p.name.toUpperCase(), px + 0.25, py + 0.14, pw - 0.5, 0.3, { fontSize: 15, bold: true, color: C.white, charSpacing: 1 });
    text(s, p.where, px + 0.25, py + 0.5, pw - 0.5, 0.3, { fontSize: 9.5, color: 'C7D0DD' });
    tag(s, p.tag, px + pw - 1.85, py + 0.2, 1.6, { fill: C.gold, color: C.white, size: 7.5, h: 0.26 });
    // big number
    text(s, p.num, px + 0.25, py + 1.05, pw - 0.5, 0.62, { fontSize: p.numSize || 26, bold: true, color: C.navy, valign: 'middle' });
    text(s, p.numLabel, px + 0.25, py + 1.65, pw - 0.5, 0.3, { fontSize: 9, color: C.grey });
    // rows
    p.rows.forEach((r, j) => {
      const ry = py + 2.05 + j * 0.7;
      line(s, px + 0.25, ry - 0.06, px + pw - 0.25, ry - 0.06, { line: { color: C.line, width: 0.5 } });
      text(s, r.k, px + 0.25, ry, 1.05, 0.6, { fontSize: 8, bold: true, color: C.goldDark, charSpacing: 1 });
      text(s, r.v, px + 1.3, ry, pw - 1.55, 0.62, { fontSize: 9.5, color: C.ink, lineSpacingMultiple: 1.0 });
    });
  });

  footer(s, 8, DATA.s8.source);
  notes(s, DATA.s8.notes);
}

// --------------------------------------------------------------------------------------
// SLIDE 9 — INVESTMENT STRUCTURE
// --------------------------------------------------------------------------------------
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  header(s, 'Investment structure', DATA.s9.headline);

  const boxH = 0.62;
  function box(x, y, w, label, sub, opt = {}) {
    const fill = opt.fill || C.white, lineC = opt.line || C.navy, tc = opt.color || C.navy;
    rect(s, x, y, w, opt.h || boxH, { fill: { color: fill }, line: { color: lineC, width: opt.lw || 1.25 } });
    text(s, label, x + 0.1, y + 0.06, w - 0.2, sub ? 0.3 : (opt.h || boxH) - 0.12, { fontSize: opt.size || 11, bold: true, color: tc, align: 'center', valign: sub ? 'top' : 'middle' });
    if (sub) text(s, sub, x + 0.1, y + 0.33, w - 0.2, 0.25, { fontSize: 8.5, color: opt.subColor || C.grey, align: 'center' });
  }
  function vArrow(x, y1, y2, label) {
    arrow(s, x, y1, x, y2, { line: { color: C.navy, width: 1.25, endArrowType: 'triangle' } });
    if (label) {
      rrect(s, x + 0.08, (y1 + y2) / 2 - 0.13, 0.62, 0.26, { rectRadius: 0.13, fill: { color: C.white }, line: { color: C.white, width: 0 } });
      text(s, label, x + 0.08, (y1 + y2) / 2 - 0.13, 0.62, 0.26, { fontSize: 9, bold: true, color: C.navy, valign: 'middle' });
    }
  }

  // panels
  const pw = 5.05, ph = 4.85, py = 1.75;
  const lx = M, rx = W - M - pw;
  rect(s, lx, py, pw, ph, { fill: { color: C.light } });
  rect(s, rx, py, pw, ph, { fill: { color: C.light } });
  text(s, 'TODAY', lx + 0.3, py + 0.2, pw - 0.6, 0.26, { fontSize: 10, bold: true, color: C.grey, charSpacing: 2 });
  text(s, 'POST-TRANSACTION  —  ILLUSTRATIVE', rx + 0.3, py + 0.2, pw - 0.6, 0.26, { fontSize: 10, bold: true, color: C.goldDark, charSpacing: 2 });

  // LEFT: FKS Multi Agro -> 100% -> FSL -> assets
  const lcx = lx + pw / 2;
  box(lcx - 1.4, py + 0.65, 2.8, 'FKS Multi Agro', 'Sponsor');
  vArrow(lcx, py + 0.65 + boxH, py + 1.75, '100%');
  box(lcx - 1.4, py + 1.75, 2.8, DATA.s9.platform, 'Logistics platform', { fill: C.navy, line: C.navy, color: C.white, subColor: 'C7D0DD' });
  vArrow(lcx, py + 1.75 + boxH, py + 2.85);
  box(lx + 0.3, py + 2.85, pw - 0.6, 'Operating gateways', DATA.s9.assets, { size: 10, lw: 0.75, line: C.navy3, h: 0.72 });

  // MIDDLE: transaction arrow
  const ax0 = lx + pw + 0.2, ax1 = rx - 0.2, ay = py + 2.06;
  s.addShape('rightArrow', { x: ax0, y: ay - 0.22, w: ax1 - ax0, h: 0.44, fill: { color: C.gold }, line: { color: C.gold, width: 0 } });
  text(s, DATA.s9.arrowTop, ax0 - 0.15, ay - 0.95, ax1 - ax0 + 0.3, 0.7, { fontSize: 9.5, bold: true, color: C.navy, align: 'center', valign: 'bottom', lineSpacingMultiple: 1.0 });
  text(s, DATA.s9.arrowBottom, ax0 - 0.15, ay + 0.3, ax1 - ax0 + 0.3, 0.7, { fontSize: 8.5, bold: true, color: C.goldDark, align: 'center', valign: 'top', lineSpacingMultiple: 1.0 });

  // RIGHT: FKS 51% + Danantara 49% -> FSL -> assets + pipeline
  const rcx = rx + pw / 2;
  const hw = 2.3;
  box(rcx - hw - 0.15, py + 0.65, hw, 'FKS Multi Agro', '51%  —  retains control', { subColor: C.navy });
  box(rcx + 0.15, py + 0.65, hw, 'Danantara Indonesia', '49%  —  illustrative', { line: C.gold, color: C.goldDark, subColor: C.goldDark });
  // converge lines
  line(s, rcx - hw / 2 - 0.15, py + 0.65 + boxH, rcx - hw / 2 - 0.15, py + 1.55, { line: { color: C.navy, width: 1.25 } });
  line(s, rcx + hw / 2 + 0.15, py + 0.65 + boxH, rcx + hw / 2 + 0.15, py + 1.55, { line: { color: C.gold, width: 1.25 } });
  line(s, rcx - hw / 2 - 0.15, py + 1.55, rcx + hw / 2 + 0.15, py + 1.55, { line: { color: C.navy, width: 1.25 } });
  vArrow(rcx, py + 1.55, py + 1.75);
  box(rcx - 1.4, py + 1.75, 2.8, DATA.s9.platform, 'Logistics platform', { fill: C.navy, line: C.navy, color: C.white, subColor: 'C7D0DD' });
  vArrow(rcx, py + 1.75 + boxH, py + 2.75);
  const aw2 = (pw - 0.6 - 0.2) / 2;
  line(s, rx + 0.3 + aw2 / 2, py + 2.75, rx + 0.5 + aw2 * 1.5, py + 2.75, { line: { color: C.navy, width: 1.25 } });
  line(s, rx + 0.3 + aw2 / 2, py + 2.75, rx + 0.3 + aw2 / 2, py + 2.85, { line: { color: C.navy, width: 1.25 } });
  line(s, rx + 0.5 + aw2 * 1.5, py + 2.75, rx + 0.5 + aw2 * 1.5, py + 2.85, { line: { color: C.gold, width: 1.25 } });
  box(rx + 0.3, py + 2.85, aw2, 'Operating gateways', DATA.s9.assets, { size: 10, lw: 0.75, line: C.navy3, h: 0.72 });
  box(rx + 0.3 + aw2 + 0.2, py + 2.85, aw2, 'Pipeline', DATA.s9.pipeline, { size: 10, lw: 0.75, line: C.gold, color: C.goldDark, subColor: C.goldDark, h: 0.72 });
  // note inside right panel
  text(s, DATA.s9.rightNote, rx + 0.3, py + 4.0, pw - 0.6, 0.75, { fontSize: 8.5, color: C.grey, lineSpacingMultiple: 1.05 });
  text(s, DATA.s9.leftNote, lx + 0.3, py + 4.0, pw - 0.6, 0.75, { fontSize: 8.5, color: C.grey, lineSpacingMultiple: 1.05 });

  footer(s, 9, DATA.s9.source);
  notes(s, DATA.s9.notes);
}

pres.writeFile({ fileName: OUT }).then(f => console.log('written', f));
