# -*- coding: utf-8 -*-
"""v8 additions on top of the v7 design helpers (same palette, fonts and template)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v7'))
from lib_v7 import *
from lib_v7 import _style
from PIL import ImageFont

ML, MR = 0.56, 9.44
BODY, LAB, FOOT = 18, 14, 10.5
_FONT_DIR = '/usr/share/fonts/truetype/crosextra/'
_fonts = {}

def tw(s, size, bold=False, spacing=0.0):
    """Approximate rendered width in inches of a single line of Calibri text (measured with Carlito, the metric-compatible font)."""
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(_FONT_DIR + ('Carlito-Bold.ttf' if bold else 'Carlito-Regular.ttf'), int(size * 10))
    w = _fonts[key].getlength(s) / 10.0 / 72.0
    return w + len(s) * spacing / 72.0

def lab(slide, s, x, y, w, color=MID, size=LAB, align='left', spacing=1.5, bold=True):
    """Section label, v6 style (small caps, letter-spaced, bold) at the v8 size."""
    return text(slide, s.upper(), x, y, w, size / 72.0 * 1.3, size=size, bold=bold, color=color, spacing=spacing, align=align)

def island_rings(point):
    """Rings of the Indonesia polygon whose bounding box contains `point` (lon, lat)."""
    out = []
    for ring in POLYS['Indonesia']:
        xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
        if min(xs) <= point[0] <= max(xs) and min(ys) <= point[1] <= max(ys):
            out.append(ring)
    return out

def rings_layer(slide, rings, x, y, w, h, bbox, fill, line_color=WHITE, lw=0.5, name=None):
    lon0, lat0, lon1, lat1 = bbox
    E = 914400
    ff = None
    for ring in rings:
        pts = [((lon - lon0) / (lon1 - lon0) * w, (lat1 - lat) / (lat1 - lat0) * h) for lon, lat in ring]
        if all(p[0] < 0 or p[0] > w or p[1] < 0 or p[1] > h for p in pts):
            continue
        pts = [(min(max(X, 0), w), min(max(Y, 0), h)) for X, Y in pts]
        dd = []
        for p in pts:
            q = (int(round(p[0] * E)), int(round(p[1] * E)))
            if not dd or abs(dd[-1][0] - q[0]) > 1 or abs(dd[-1][1] - q[1]) > 1:
                dd.append(q)
        if len(dd) < 3:
            continue
        if ff is None:
            ff = slide.shapes.build_freeform(dd[0][0], dd[0][1], scale=1.0)
        else:
            ff.move_to(dd[0][0], dd[0][1])
        ff.add_line_segments(dd[1:], close=True)
    if ff is None:
        return None
    shp = ff.convert_to_shape(I(x), I(y))
    _style(shp, fill, line_color, lw)
    shp.name = name or 'Map - island'
    return shp

def highlight_island(slide, point, x, y, w, bbox, fill, name=None):
    h = map_height(w, bbox)
    return rings_layer(slide, island_rings(point), x, y, w, h, bbox, fill, name=name)

def loader(slide, x, y, w, h, color=YELLOW, ship_color=DARK):
    """Ship loader: pit, rising boom, small vessel."""
    shape(slide, MSO_SHAPE.TRAPEZOID, x, y + h * 0.62, w * 0.22, h * 0.3, color, None, flipV=True)
    shape(slide, MSO_SHAPE.RECTANGLE, x + w * 0.05, y + h * 0.4, w * 0.55, h * 0.12, color, None, rot=-22)
    shape(slide, MSO_SHAPE.RECTANGLE, x + w * 0.4, y + h * 0.45, w * 0.05, h * 0.5, color, None)
    ship(slide, x + w * 0.52, y + h * 0.5, w * 0.48, h * 0.5, ship_color, hatches=2)

def bracket(slide, x1, x2, y, color=DARK, tick=0.08):
    line(slide, x1, y, x2, y, color, 1.0); line(slide, x1, y - tick, x1, y, color, 1.0); line(slide, x2, y - tick, x2, y, color, 1.0)
