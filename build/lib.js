// Design system + helpers for the FKS x Danantara deck (pptxgenjs)
'use strict';
const path = require('path');
const fs = require('fs');

const C = {
  navy: '0F2340',      // primary
  navy2: '1E3A5F',     // secondary navy
  navy3: '2F5387',     // tertiary navy (conveyor, accents)
  ink: '1F2937',       // body text
  grey: '6B7280',      // secondary text
  grey2: '9CA3AF',     // muted
  line: 'D5DBE3',      // hairlines
  light: 'F2F4F7',     // panels
  light2: 'E6EAF0',    // deeper panel
  gold: 'C39B2A',      // single accent
  goldLight: 'F6EED3', // accent tint
  goldDark: '9A7A1C',
  white: 'FFFFFF',
  sea: 'E4EBF3',       // map sea / water
  land: 'CBD5E1',      // map neighbours
  landID: 'A9B8CC',    // map Indonesia
  conv: '8A929E',      // conventional (muted)
};
const FONT = 'Calibri';
const W = 13.333, H = 7.5;
const M = 0.6; // outer margin
const ASSETS = path.join(__dirname, 'assets');

function px(v) { return v; }

// ---------- text helpers ----------
function text(slide, str, x, y, w, h, opt = {}) {
  const o = Object.assign({
    x, y, w, h, fontFace: FONT, fontSize: 12, color: C.ink, isTextBox: true,
    margin: 0, valign: 'top', align: 'left', wrap: true,
  }, opt);
  slide.addText(str, o);
}

// header: small section label + headline sentence
function header(slide, section, headline, opt = {}) {
  text(slide, section.toUpperCase(), M, 0.42, 9.5, 0.25, {
    fontSize: 9.5, bold: true, color: C.gold, charSpacing: 2,
  });
  text(slide, headline, M, 0.68, 10.7, 0.95, {
    fontSize: opt.size || 22, bold: true, color: C.navy, valign: 'top', lineSpacingMultiple: 1.0,
  });
  slide.addImage({ path: path.join(ASSETS, 'logo_lockup_raw.png'), x: W - M - 1.42, y: 0.38, w: 1.42, h: 0.477 });
}

function footer(slide, n, source) {
  text(slide, 'FKS Group  |  Strictly private and confidential  |  Discussion materials for Danantara Indonesia', M, 7.08, 8, 0.22, {
    fontSize: 8, color: C.grey2,
  });
  text(slide, String(n), W - M - 0.6, 7.08, 0.6, 0.22, { fontSize: 8, color: C.grey2, align: 'right' });
  if (source) {
    text(slide, source, M, 6.78, W - 2 * M, 0.26, { fontSize: 7.5, color: C.grey2, valign: 'bottom' });
  }
}

// ---------- shapes ----------
function rect(slide, x, y, w, h, opt = {}) {
  const o = Object.assign({ x, y, w, h, fill: { color: C.light }, line: { color: C.light, width: 0 } }, opt);
  if (o.line && o.line.width === 0) o.line = { color: o.fill ? o.fill.color : C.white, width: 0 };
  slide.addShape('rect', o);
}
function rrect(slide, x, y, w, h, opt = {}) {
  const o = Object.assign({ x, y, w, h, rectRadius: 0.08, fill: { color: C.light }, line: { color: C.light, width: 0 } }, opt);
  slide.addShape('roundRect', o);
}
function oval(slide, x, y, w, h, opt = {}) {
  const o = Object.assign({ x, y, w, h, fill: { color: C.navy }, line: { color: C.navy, width: 0 } }, opt);
  slide.addShape('ellipse', o);
}
function line(slide, x1, y1, x2, y2, opt = {}) {
  const o = Object.assign({ x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), line: { color: C.line, width: 1 } }, opt);
  if ((x2 < x1 && y2 > y1) || (x2 > x1 && y2 < y1)) o.flipV = true;
  slide.addShape('line', o);
}
function arrow(slide, x1, y1, x2, y2, opt = {}) {
  const lopt = Object.assign({ color: C.grey, width: 1.25, endArrowType: 'triangle' }, opt.line || {});
  line(slide, x1, y1, x2, y2, Object.assign({}, opt, { line: lopt }));
}
function chevron(slide, x, y, w, h, opt = {}) {
  slide.addShape('chevron', Object.assign({ x, y, w, h, fill: { color: C.gold }, line: { color: C.gold, width: 0 } }, opt));
}

// big number tile: number, label, optional sublabel
function stat(slide, x, y, w, num, label, opt = {}) {
  const numSize = opt.numSize || 34;
  const numH = numSize / 72 * 1.35;
  text(slide, num, x, y, w, numH, { fontSize: numSize, bold: true, color: opt.numColor || C.navy, align: opt.align || 'left', valign: 'bottom' });
  text(slide, label, x, y + numH + 0.04, w, opt.labelH || 0.5, { fontSize: opt.labelSize || 11, color: opt.labelColor || C.ink, align: opt.align || 'left', bold: !!opt.labelBold, lineSpacingMultiple: 1.05 });
  if (opt.sub) text(slide, opt.sub, x, y + numH + 0.04 + (opt.labelH || 0.5), w, 0.3, { fontSize: 9, color: C.grey, align: opt.align || 'left' });
}

// pill/tag
function tag(slide, str, x, y, w, opt = {}) {
  const h = opt.h || 0.26;
  rrect(slide, x, y, w, h, { rectRadius: 0.13, fill: { color: opt.fill || C.goldLight }, line: { color: opt.fill || C.goldLight, width: 0 } });
  text(slide, str, x, y, w, h, { fontSize: opt.size || 8, bold: true, color: opt.color || C.goldDark, align: 'center', valign: 'middle', charSpacing: 1 });
}

// ---------- map ----------
// Placeholder rect that postprocess_map.py replaces with an editable freeform of the coastline.
// name encodes: MAP|<country|neighbours>|lon0|lat0|lon1|lat1
function mapLayer(slide, which, x, y, w, h, bbox, opt = {}) {
  const fill = opt.fill || (which === 'Indonesia' ? C.landID : C.land);
  slide.addShape('rect', {
    x, y, w, h, fill: { color: fill }, line: { color: opt.lineColor || C.white, width: opt.lineWidth == null ? 0.5 : opt.lineWidth },
    objectName: `MAP|${which}|${bbox.join('|')}`,
  });
}
function projector(x, y, w, h, bbox) {
  const [lon0, lat0, lon1, lat1] = bbox;
  return (lon, lat) => [x + (lon - lon0) / (lon1 - lon0) * w, y + (lat1 - lat) / (lat1 - lat0) * h];
}
// aspect-correct height for a bbox at a given width (equirectangular, cos(mean lat))
function mapHeight(w, bbox) {
  const [lon0, lat0, lon1, lat1] = bbox;
  const meanLat = (lat0 + lat1) / 2 * Math.PI / 180;
  return w * (lat1 - lat0) / ((lon1 - lon0) * Math.cos(meanLat));
}

// ---------- icons (react-icons -> png) ----------
async function iconPng(IconComp, color, size = 256) {
  const React = require('react');
  const ReactDOMServer = require('react-dom/server');
  const sharp = require('sharp');
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(IconComp, { color: '#' + color, size }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return 'image/png;base64,' + buf.toString('base64');
}

// ---------- notes ----------
function notes(slide, { objective, talk, sources, calc, validate }) {
  const s = [];
  s.push('1. SLIDE OBJECTIVE\n' + objective.trim());
  s.push('2. TALK TRACK\n' + talk.trim());
  s.push('3. SOURCES\n' + sources.trim());
  s.push('4. CALCULATION BASIS\n' + calc.trim());
  s.push('5. DATA STILL TO BE VALIDATED\n' + validate.trim());
  slide.addNotes(s.join('\n\n'));
}

module.exports = { C, FONT, W, H, M, ASSETS, text, header, footer, rect, rrect, oval, line, arrow, chevron, stat, tag, mapLayer, projector, mapHeight, iconPng, notes };
