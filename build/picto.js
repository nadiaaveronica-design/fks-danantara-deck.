// Simple editable pictograms built from native shapes (no images)
'use strict';
const { C } = require('./lib');

function fillOpt(color) { return { fill: { color }, line: { color, width: 0 } }; }

// Bulk carrier silhouette, side view. Box x,y,w,h.
function ship(slide, x, y, w, h, color = C.navy, opt = {}) {
  const f = fillOpt(color);
  // hull (wide at deck, narrow at keel)
  slide.addShape('trapezoid', Object.assign({ x, y: y + h * 0.58, w, h: h * 0.42, flipV: true }, f));
  // deck house + bridge (aft = right)
  slide.addShape('rect', Object.assign({ x: x + w * 0.74, y: y + h * 0.28, w: w * 0.16, h: h * 0.32 }, f));
  slide.addShape('rect', Object.assign({ x: x + w * 0.77, y: y + h * 0.1, w: w * 0.1, h: h * 0.2 }, f));
  // hatch covers
  const n = opt.hatches || 4;
  const hw = (w * 0.62) / n;
  for (let i = 0; i < n; i++) {
    slide.addShape('rect', Object.assign({ x: x + w * 0.08 + i * hw + hw * 0.1, y: y + h * 0.46, w: hw * 0.8, h: h * 0.12 }, f));
  }
}

// Water line under a ship
function water(slide, x, y, w, color = C.sea) {
  slide.addShape('rect', { x, y, w, h: 0.06, fill: { color }, line: { color, width: 0 } });
}

// Crane with a grab. Mast at left, jib to the right, grab hanging near jib end.
function crane(slide, x, y, w, h, color = C.conv) {
  const f = fillOpt(color);
  slide.addShape('rect', Object.assign({ x: x + w * 0.12, y, w: w * 0.07, h }, f));             // mast
  slide.addShape('rect', Object.assign({ x: x + w * 0.12, y, w: w * 0.8, h: h * 0.07 }, f));       // jib
  slide.addShape('line', { x: x + w * 0.8, y: y + h * 0.07, w: 0, h: h * 0.45, line: { color, width: 1.25 } }); // hoist rope
  slide.addShape('flowChartMerge', Object.assign({ x: x + w * 0.66, y: y + h * 0.52, w: w * 0.28, h: h * 0.3 }, f)); // grab
}

// Open hopper (funnel)
function hopper(slide, x, y, w, h, color = C.conv) {
  const f = fillOpt(color);
  slide.addShape('rect', Object.assign({ x, y, w, h: h * 0.32 }, f));
  slide.addShape('flowChartMerge', Object.assign({ x: x + w * 0.08, y: y + h * 0.3, w: w * 0.84, h: h * 0.7 }, f));
  // legs
  slide.addShape('rect', Object.assign({ x: x + w * 0.1, y: y + h * 0.3, w: w * 0.05, h: h * 0.7 }, f));
  slide.addShape('rect', Object.assign({ x: x + w * 0.85, y: y + h * 0.3, w: w * 0.05, h: h * 0.7 }, f));
}

// Truck, side view, cab to the right
function truck(slide, x, y, w, h, color = C.conv) {
  const f = fillOpt(color);
  slide.addShape('rect', Object.assign({ x, y: y + h * 0.1, w: w * 0.66, h: h * 0.55 }, f));                 // body
  slide.addShape('roundRect', Object.assign({ x: x + w * 0.68, y: y + h * 0.3, w: w * 0.3, h: h * 0.35, rectRadius: 0.03 }, f)); // cab
  const d = h * 0.34;
  slide.addShape('ellipse', Object.assign({ x: x + w * 0.1, y: y + h * 0.66, w: d, h: d }, f));
  slide.addShape('ellipse', Object.assign({ x: x + w * 0.36, y: y + h * 0.66, w: d, h: d }, f));
  slide.addShape('ellipse', Object.assign({ x: x + w * 0.74, y: y + h * 0.66, w: d, h: d }, f));
}

// Mill / factory: body with saw-tooth roof and a chimney
function mill(slide, x, y, w, h, color = C.navy) {
  const f = fillOpt(color);
  slide.addShape('rect', Object.assign({ x, y: y + h * 0.42, w, h: h * 0.58 }, f));
  const n = 3, tw = w / n;
  for (let i = 0; i < n; i++) {
    slide.addShape('rtTriangle', Object.assign({ x: x + i * tw, y: y + h * 0.16, w: tw, h: h * 0.27, flipH: true }, f));
  }
  slide.addShape('rect', Object.assign({ x: x + w * 0.8, y, w: w * 0.1, h: h * 0.3 }, f));
}

// Silo group (cylinders)
function silos(slide, x, y, w, h, n = 3, color = C.navy) {
  const f = fillOpt(color);
  const gap = w * 0.06, sw = (w - gap * (n - 1)) / n;
  for (let i = 0; i < n; i++) {
    slide.addShape('can', Object.assign({ x: x + i * (sw + gap), y, w: sw, h }, f));
  }
}

// Warehouse: body with a low-pitched roof
function warehouse(slide, x, y, w, h, color = C.navy) {
  const f = fillOpt(color);
  slide.addShape('triangle', Object.assign({ x, y, w, h: h * 0.3 }, f));
  slide.addShape('rect', Object.assign({ x, y: y + h * 0.28, w, h: h * 0.72 }, f));
}

// Elevated conveyor gallery: horizontal beam on legs
function conveyor(slide, x, y, w, color = C.navy3, opt = {}) {
  const f = fillOpt(color);
  const t = opt.thickness || 0.09;
  slide.addShape('rect', Object.assign({ x, y, w, h: t }, f));
  const legs = opt.legs || 3, legH = opt.legH || 0.5;
  for (let i = 0; i < legs; i++) {
    const lx = x + (w - 0.04) * (i / (legs - 1)) + 0.02;
    slide.addShape('rect', Object.assign({ x: lx - 0.015, y: y + t, w: 0.03, h: legH }, f));
  }
}

// Ship unloader: gantry with a boom reaching out to the left over the vessel
function unloader(slide, x, y, w, h, color = C.navy) {
  const f = fillOpt(color);
  slide.addShape('rect', Object.assign({ x: x + w * 0.55, y: y + h * 0.15, w: w * 0.07, h: h * 0.85 }, f)); // leg
  slide.addShape('rect', Object.assign({ x: x + w * 0.85, y: y + h * 0.15, w: w * 0.07, h: h * 0.85 }, f)); // leg
  slide.addShape('rect', Object.assign({ x: x + w * 0.5, y: y + h * 0.12, w: w * 0.5, h: h * 0.1 }, f));   // portal beam
  slide.addShape('rect', Object.assign({ x, y: y + h * 0.02, w: w * 0.62, h: h * 0.08 }, f));               // boom over ship
  slide.addShape('rect', Object.assign({ x: x + w * 0.08, y: y + h * 0.08, w: w * 0.06, h: h * 0.5 }, f)); // vertical arm into hold
  slide.addShape('rect', Object.assign({ x: x + w * 0.62, y: y + h * 0.02, w: w * 0.05, h: h * 0.2 }, f)); // tower
}

module.exports = { ship, water, crane, hopper, truck, mill, silos, warehouse, conveyor, unloader };
