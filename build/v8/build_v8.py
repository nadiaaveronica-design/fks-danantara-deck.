# -*- coding: utf-8 -*-
"""Build FKS_Danantara_Strategic_Partnership_v8.pptx: v7 identity (FKS template, v6 palette), simplified content."""
import os, sys, math
HERE8 = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE8)
from lib_v8 import *
import content_v8 as C

OUT = sys.argv[1] if len(sys.argv) > 1 else 'v8_raw.pptx'
TEMPLATE = os.path.join(HERE8, '..', 'v7', 'template_BACKUP.pptx')

prs = Presentation(TEMPLATE)
sldIdLst = prs.slides._sldIdLst
for sldId in list(sldIdLst):
    prs.part.drop_rel(sldId.rId); sldIdLst.remove(sldId)
masters = prs.slide_masters
L_COVER = masters[0].slide_layouts[0]
L_CONTENT = [l for l in masters[2].slide_layouts if l.name == 'Content All Text'][0]
L_DISC = [l for l in masters[2].slide_layouts if l.name == 'Disclaimer'][0]

def A(name):
    return os.path.join(ASSETS, name)

def content_slide(title, subtitle, n):
    s = prs.slides.add_slide(L_CONTENT)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx in (1, 13):
            ph._element.getparent().remove(ph._element)
    t = s.placeholders[16]; t.text_frame.text = title
    for r in t.text_frame.paragraphs[0].runs:
        r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = rgb(DARK); r.font.name = FONT
    st = s.placeholders[15]; st.text_frame.text = subtitle
    for r in st.text_frame.paragraphs[0].runs:
        r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = rgb(MID); r.font.name = FONT
    line(s, ML, 0.97, MR, 0.97, LINE, 0.75, name='Title rule')
    text(s, str(n), 9.0, 5.2, 0.44, 0.2, size=8, color=DARK, align='right', name='Page number')
    return s

def takeaway(s, txt, y, x=ML, w=None):
    w = w or (MR - x)
    chevron(s, x, y + 0.08, 0.13, 0.18)
    text(s, txt, x + 0.24, y, w - 0.24, 0.34, size=BODY, bold=True, color=DARK, anchor='middle')

def footnote(s, txt, y=4.98, w=8.1, h=0.2):
    text(s, txt, ML, y, w, h, size=FOOT, italic=True, color=MID, name='Footnote')

def box(s, x, y, w, h, t1, t2=None, fill=WHITE, lc=DARK, lw=1.0, c1=DARK, c2=DARK, dash=None, s1=BODY, s2=LAB):
    shape(s, MSO_SHAPE.RECTANGLE, x, y, w, h, fill, lc, lw, dash=dash)
    if t2:
        text(s, [(t1, {'size': s1, 'bold': True, 'color': c1}), ('\n' + t2, {'size': s2, 'color': c2})], x + 0.05, y, w - 0.1, h, size=s1, align='center', anchor='middle')
    else:
        text(s, t1, x + 0.05, y, w - 0.1, h if s1 < 20 else h * 0.6, size=s1, bold=True, color=c1, align='center', anchor='middle')

# ==================================================================== 1 COVER
s = prs.slides.add_slide(L_COVER)
s.placeholders[0].text_frame.text = C.COVER['title']
for r in s.placeholders[0].text_frame.paragraphs[0].runs:
    r.font.size = Pt(24); r.font.bold = True; r.font.color.rgb = rgb(DARK); r.font.name = FONT
s.placeholders[1].height = I(0.9)
tf = s.placeholders[1].text_frame
tf.text = C.COVER['sub1']
for r in tf.paragraphs[0].runs:
    r.font.size = Pt(18); r.font.color.rgb = rgb(MID); r.font.name = FONT; r.font.bold = False
p = tf.add_paragraph(); r = p.add_run(); r.text = C.COVER['sub2']; r.font.size = Pt(12); r.font.color.rgb = rgb(MID); r.font.name = FONT
notes(s, C.COVER['notes'])

# ==================================================================== 2 MARKET -> PROCESSING -> CORRIDORS
d = C.S2
s = content_slide(d['title'], d['subtitle'], 2)
lab(s, d['col_labels'][0], ML, 1.1, 2.9)
lab(s, d['col_labels'][1], 3.85, 1.1, 1.7)
lab(s, d['col_labels'][2], 5.6, 1.1, 3.84)
text(s, d['total'], ML, 1.3, 2.4, 0.8, size=50, bold=True, color=DARK, anchor='middle')
text(s, d['total_sub'], 2.92, 1.42, 2.6, 0.6, size=16, color=MID)
for i, r in enumerate(d['rows']):
    ry = 2.34 + i * 0.74
    picture(s, A(r['icon']), ML, ry, 0.62, 0.62, name='Icon ' + r['name'])
    text(s, r['name'], 1.3, ry - 0.03, 2.4, 0.3, size=BODY, bold=True, color=DARK)
    text(s, r['mt'], 1.3, ry + 0.27, 2.4, 0.38, size=22, bold=True, color=GOLD)
    chevron(s, 3.72, ry + 0.2, 0.15, 0.22)
    text(s, r['to'], 3.95, ry, 1.7, 0.62, size=BODY, color=DARK, anchor='middle')
mx, my, mw = 5.6, 1.34, 3.84
pj, mh = draw_map(s, mx, my, mw, ID_BBOX)
highlight_island(s, (101.5, -1.0), mx, my, mw, ID_BBOX, GREY, name='Map - Sumatra')
highlight_island(s, (110.0, -7.3), mx, my, mw, ID_BBOX, YELLOW, name='Map - Java')
jx, jy = pj(110.0, -7.3); sx, sy = pj(101.0, -1.2)
text(s, d['java'], jx - 0.6, jy + 0.12, 1.2, 0.22, size=LAB, bold=True, color=GOLD, align='center', spacing=1.5)
text(s, d['sumatra'], 5.1, 2.16, 1.05, 0.2, size=LAB, bold=True, color=MID, align='right', spacing=1.5)
for j, (num, lbl) in enumerate([d['share1'], d['share2']]):
    xx = mx + j * 2.0
    text(s, num, xx, 3.0, 1.85, 0.52, size=34, bold=True, color=GOLD, anchor='middle')
    text(s, lbl, xx, 3.54, 1.85, 0.55, size=16, color=DARK)
text(s, d['others'], mx, 4.2, 3.84, 0.26, size=16, color=MID)
takeaway(s, d['takeaway'], 4.6)
footnote(s, d['footnote'])
notes(s, d['notes'])

# ==================================================================== 3 THE PROBLEM
d = C.S3
s = content_slide(d['title'], d['subtitle'], 3)
text(s, [(d['hero_a'], {'size': 64, 'color': GOLD}), (d['hero_b'], {'size': 36, 'color': DARK})], ML, 1.06, 2.9, 0.92, bold=True, anchor='bottom')
text(s, d['hero_sub'], ML, 2.04, 2.9, 0.95, size=BODY, color=DARK)
ly = 3.0
oval(s, ML, ly + 0.05, 0.15, 0.15, fill=YELLOW, line=WHITE, lw=0.5)
text(s, d['legend'][0][1], 0.79, ly, 1.35, 0.25, size=LAB, color=MID)
oval(s, 2.3, ly + 0.05, 0.15, 0.15, fill=WHITE, line=GREY2, lw=1.25)
text(s, d['legend'][1][1], 2.53, ly, 1.1, 0.25, size=LAB, color=MID)
S3_BBOX = (94.5, -9.5, 121.0, 6.5)
pj, mh = draw_map(s, ML, 3.3, 2.55, S3_BBOX)
offs = {'Ciwandan': (-0.09, 0.11), 'Tanjung Priok': (0.13, 0.04), 'Tanjung Perak': (0.11, 0.1), 'Panjang': (-0.06, -0.02)}
for site in d['sites']:
    x, y = pj(site['lon'], site['lat']); dx, dy = offs.get(site['name'], (0, 0)); x += dx; y += dy
    if site['kind'] == 'fks':
        oval(s, x - 0.075, y - 0.075, 0.15, 0.15, fill=YELLOW, line=WHITE, lw=0.5, name='Gateway ' + site['name'])
for site in d['sites']:
    x, y = pj(site['lon'], site['lat']); dx, dy = offs.get(site['name'], (0, 0)); x += dx; y += dy
    if site['kind'] == 'conv':
        oval(s, x - 0.07, y - 0.07, 0.14, 0.14, fill=WHITE, line=GREY2, lw=1.25, name='Gateway ' + site['name'])
# conventional flow, large
FX = 3.85
lab(s, d['flow_label'], FX, 1.1, 4.0)
fy = 1.66
ship(s, FX, fy + 0.12, 1.8, 0.86, GREY, hatches=4, aft_left=True)
crane(s, FX + 1.12, fy - 0.24, 0.78, 1.02, GREY2)
text(s, d['captions'][1], FX + 1.92, fy - 0.24, 0.7, 0.22, size=LAB, bold=True, color=GREY2, spacing=1.5)
hopper(s, FX + 2.12, fy + 0.2, 0.62, 0.78, GREY)
truck(s, FX + 2.95, fy + 0.42, 0.95, 0.56, GREY2)
line(s, FX + 4.02, fy + 0.72, FX + 4.28, fy + 0.72, GREY2, 1.0, arrow=True)
mill(s, FX + 4.42, fy + 0.1, 1.15, 0.88, GREY2)
gy = fy + 1.0
line(s, FX, gy, MR, gy, GREY, 1.0)
for cap, cx, cw in [(d['captions'][0], FX, 1.6), (d['captions'][2], FX + 1.98, 0.9), (d['captions'][3], FX + 2.85, 1.15), (d['captions'][4], FX + 4.42, 1.15)]:
    text(s, cap, cx, gy + 0.06, cw, 0.22, size=LAB, bold=True, color=GREY2, align='center', spacing=1.5)
ky = 3.14
for i, (num, lbl) in enumerate(d['kpis']):
    kx = FX + i * 1.93
    if i < 2:
        text(s, num, kx, ky, 1.73, 0.48, size=26, bold=True, color=DARK, anchor='middle')
        text(s, lbl, kx, ky + 0.5, 1.73, 0.5, size=16, color=MID)
        chevron(s, kx + 1.76, ky + 0.14, 0.12, 0.2)
    else:
        text(s, num, kx, ky, 1.76, 0.48, size=24, bold=True, color=GOLD, anchor='middle')
        text(s, lbl, kx, ky + 0.5, 1.76, 0.5, size=16, color=MID)
takeaway(s, d['statement'], 4.32, x=FX)
footnote(s, d['footnote'], y=4.98, w=7.9)
notes(s, d['notes'])

# ==================================================================== 4 THE FKS MODEL
d = C.S4
s = content_slide(d['title'], d['subtitle'], 4)
rect(s, ML, 1.08, MR - ML, 2.96, fill=CREAM, name='FKS panel')
lab(s, d['panel_label'], 0.75, 1.18, 3.2, color=GOLD)
gy = 3.42
line(s, 0.75, gy, 9.3, gy, GREY, 1.0)
ship(s, 0.75, 2.58, 1.62, 0.84, DARK, hatches=5, aft_left=True, hatch_color=YELLOW2)
unloader(s, 2.1, 1.6, 0.85, 1.82, YELLOW)
conveyor(s, 2.95, 1.84, 1.45, YELLOW, thickness=0.08, legs=3, leg_h=1.5)
warehouse(s, 4.4, 1.48, 2.3, 1.94, YELLOW)
text(s, d['warehouse_name'], 4.4, 2.22, 2.3, 0.26, size=LAB, bold=True, color=WHITE, align='center', spacing=1.5)
truck(s, 6.95, 2.86, 1.05, 0.56, DARK, cab_color=YELLOW)
line(s, 8.08, 3.14, 8.28, 3.14, GREY2, 1.0, arrow=True)
silos(s, 8.33, 2.6, 0.42, 0.82, 3, DARK)
mill(s, 8.78, 2.6, 0.55, 0.82, DARK)
for cap, cx, cw in [(d['captions'][0], 1.95, 1.15), (d['captions'][1], 3.0, 1.35), (d['captions'][2], 4.4, 2.3), (d['captions'][3], 6.85, 1.25), (d['captions'][4], 8.22, 1.15)]:
    text(s, cap, cx, gy + 0.03, cw, 0.22, size=LAB, bold=True, color=DARK, align='center', spacing=1.5)
by = 3.8
bracket(s, 0.75, 4.3, by); bracket(s, 6.85, 9.3, by)
text(s, d['marine'], 0.75, by + 0.04, 3.55, 0.2, size=LAB, bold=True, color=DARK, align='center', spacing=1.5)
text(s, d['inland'], 6.85, by + 0.04, 2.45, 0.2, size=LAB, bold=True, color=DARK, align='center', spacing=1.5)
rrect(s, 4.4, 3.7, 2.3, 0.3, fill=YELLOW, radius=0.15, name='Buffer chip')
text(s, d['buffer'], 4.4, 3.7, 2.3, 0.3, size=16, bold=True, color=DARK, align='center', anchor='middle', spacing=1.0)
for i, (k, v) in enumerate(d['outcomes']):
    x = ML + i * 2.98
    chevron(s, x, 4.24, 0.13, 0.18)
    text(s, k, x + 0.24, 4.18, 2.72, 0.3, size=BODY, bold=True, color=GOLD)
    text(s, v, x + 0.24, 4.48, 2.72, 0.3, size=16, color=DARK)
notes(s, d['notes'])

# ==================================================================== 5 VALUE PER 60 KT CARGO
d = C.S5
s = content_slide(d['title'], d['subtitle'], 5)
LW = 1.62
cxs = [2.25, 4.68, 7.11]; PW = 2.33
rows = [('CONVENTIONAL', 2.36), ('FKS', 2.88)]
for i, p in enumerate(d['panels']):
    cx = cxs[i]
    text(s, p['head'], cx, 1.1, PW, 0.32, size=BODY, bold=True, color=GOLD)
    if p['pic'] == 'ship':
        ship(s, cx + 0.35, 1.58, 1.6, 0.68, DARK, hatches=4, hatch_color=YELLOW2)
    elif p['pic'] == 'parcels':
        ship(s, cx + 0.02, 1.9, 0.62, 0.36, GREY, hatches=2)
        ship(s, cx + 0.7, 1.9, 0.62, 0.36, GREY, hatches=2)
        text(s, 'vs', cx + 1.36, 1.92, 0.3, 0.3, size=LAB, color=MID, align='center')
        ship(s, cx + 1.02, 1.58, 1.3, 0.68, DARK, hatches=4, hatch_color=YELLOW2) if False else ship(s, cx + 1.62, 1.66, 0.72, 0.6, DARK, hatches=3, hatch_color=YELLOW2)
    else:
        conveyor(s, cx + 0.15, 1.82, 0.95, YELLOW, thickness=0.06, legs=2, leg_h=0.44)
        warehouse(s, cx + 1.15, 1.58, 1.0, 0.68, YELLOW)
    for (rl, ry), (val, _) in zip(rows, [p['conv'], p['fks']]):
        text(s, val, cx, ry, PW, 0.46, size=24, bold=True, color=DARK if rl == 'CONVENTIONAL' else GOLD, anchor='middle')
    hc = GOLD if p['hero_color'] == 'gold' else GREY
    text(s, p['hero'], cx, 3.48, PW, 0.6, size=36, bold=True, color=hc, anchor='middle')
    text(s, p['hero_sub'], cx, 4.1, PW, 0.55, size=16, color=DARK)
for rl, ry in rows:
    lab(s, rl, ML, ry + 0.13, LW, color=MID if rl == 'CONVENTIONAL' else GOLD)
lab(s, 'Value per 60 kt cargo', ML, 3.56, LW, color=MID)
for yy in (2.32, 2.84, 3.4):
    line(s, ML, yy, MR, yy, LINE, 0.75)
for xx in (2.12, 4.55, 6.98):
    line(s, xx, 1.12, xx, 4.62, LINE, 0.75)
footnote(s, d['footnote'], y=4.76, w=8.3, h=0.4)
notes(s, d['notes'])

# ==================================================================== 6 THREE GATEWAYS
d = C.S6
s = content_slide(d['title'], d['subtitle'], 6)
PW6 = 2.86
for i, site in enumerate(d['sites']):
    x = ML + i * (PW6 + 0.15)
    picture(s, A(site['photo']), x, 1.12, PW6, 1.85, name='Photo ' + site['name'])
    text(s, site['name'], x, 3.04, 1.9, 0.3, size=BODY, bold=True, color=DARK)
    text(s, site['mtpa'], x + 1.5, 3.0, PW6 - 1.5, 0.36, size=22, bold=True, color=GOLD, align='right')
    text(s, site['fact'], x, 3.42, PW6, 0.6, size=16, color=MID)
text(s, d['big'], ML, 4.18, 2.0, 0.7, size=44, bold=True, color=DARK, anchor='middle')
text(s, d['big_sub'], 2.62, 4.2, 6.6, 0.64, size=BODY, color=DARK, anchor='middle')
footnote(s, d['footnote'], y=4.98, w=8.0)
notes(s, d['notes'])

# ==================================================================== 7 JOURNEY
d = C.S7
s = content_slide(d['title'], d['subtitle'], 7)
n = len(d['stages']); cg = 0.2; cw = (MR - ML - (n - 1) * cg) / n
phY, phH = 1.12, 2.0
ty = 3.3
line(s, ML, ty, MR, ty, LINE, 1.0, arrow=True)
for i, st in enumerate(d['stages']):
    x = ML + i * (cw + cg)
    if st.get('photo'):
        picture(s, A(st['photo']), x, phY, cw, phH, name='Photo ' + st['loc'])
    else:
        rect(s, x, phY, cw, phH, fill=PANEL, name='Next panel')
        mw = cw - 0.2; mmh = map_height(mw, WEST_BBOX)
        pj, mh = draw_map(s, x + 0.1, phY + (phH - mmh) / 2 + 0.12, mw, WEST_BBOX, land='D0D2D4', neighbours='E4E5E6')
        for lon, lat in C.S8['fks_sites']:
            sx, sy = pj(lon, lat)
            oval(s, sx - 0.05, sy - 0.05, 0.1, 0.1, fill=YELLOW, line=WHITE, lw=0.5)
        for c in C.S8['cards']:
            sx, sy = pj(c['lon'], c['lat']); sy += 0.09 if c['name'] == 'CIWANDAN' else 0
            oval(s, sx - 0.06, sy - 0.06, 0.12, 0.12, fill=WHITE, line=YELLOW, lw=1.25)
        lab(s, 'Next', x + 0.12, phY + 0.1, 0.8, color=GOLD)
    last = i == n - 1
    if last:
        oval(s, x, ty - 0.08, 0.16, 0.16, fill=WHITE, line=YELLOW, lw=1.5)
    else:
        oval(s, x, ty - 0.08, 0.16, 0.16, fill=YELLOW)
    text(s, st['years'], x, ty + 0.14, cw, 0.4, size=22, bold=True, color=GOLD)
    text(s, st['loc'], x, ty + 0.56, cw, 0.3, size=BODY, bold=True, color=DARK)
    text(s, st['text'], x, ty + 0.9, cw, 0.8, size=16, color=DARK, line_spacing=1.05)
notes(s, d['notes'])

# ==================================================================== 8 NEXT PROJECTS
d = C.S8
s = content_slide(d['title'], d['subtitle'], 8)
CW8, CH8 = 4.3, 3.0
for i, c in enumerate(d['cards']):
    x = ML + i * (CW8 + 0.28); y = 1.1
    rect(s, x, y, CW8, CH8, fill=PANEL, name='Card ' + c['name'])
    text(s, c['name'], x + 0.2, y + 0.12, 1.9, 0.38, size=22, bold=True, color=DARK, spacing=1.0)
    text(s, c['place'], x + 0.2, y + 0.5, 2.05, 0.25, size=LAB, color=MID)
    mw = 1.5; mmh = map_height(mw, WEST_BBOX)
    pj, mh = draw_map(s, x + 0.2, y + 0.85, mw, WEST_BBOX, land='D0D2D4', neighbours='E4E5E6')
    for lon, lat in d['fks_sites']:
        sx, sy = pj(lon, lat)
        oval(s, sx - 0.045, sy - 0.045, 0.09, 0.09, fill=YELLOW, line=WHITE, lw=0.5)
    sx, sy = pj(c['lon'], c['lat']); sy += 0.08 if c['name'] == 'CIWANDAN' else 0
    oval(s, sx - 0.11, sy - 0.11, 0.22, 0.22, fill=None, line=GOLD2, lw=1.75, name='Ring ' + c['name'])
    oval(s, sx - 0.05, sy - 0.05, 0.1, 0.1, fill=WHITE, line=GOLD2, lw=1.25)
    text(s, c['num'], x + 0.2, y + 1.9, 1.9, 0.5, size=32, bold=True, color=GOLD, anchor='middle')
    text(s, c['num_sub'], x + 0.2, y + 2.42, 1.9, 0.5, size=16, color=DARK)
    rx = x + 2.15; rw = CW8 - 2.15 - 0.18
    lab(s, d['labels'][0], rx, y + 0.16, 1.3, color=GOLD)
    lab(s, d['labels'][1], rx, y + 1.58, 1.9, color=GOLD)
    text(s, c['problem'], rx, y + 0.44, rw, 0.98, size=BODY, color=DARK, line_spacing=1.02)
    text(s, c['fix'], rx, y + 1.86, rw, 1.0, size=BODY, color=DARK, line_spacing=1.02)
rect(s, ML, 4.24, MR - ML, 0.46, fill=CREAM2, name='Expansions strip')
lab(s, d['expansions_label'], 0.75, 4.37, 1.7, color=GOLD)
text(s, d['expansions'], 2.5, 4.24, 6.8, 0.46, size=BODY, color=DARK, anchor='middle')
footnote(s, d['footnote'], y=4.8, w=8.3, h=0.36)
notes(s, d['notes'])

# ==================================================================== 9 STRUCTURE
d = C.S9
s = content_slide(d['title'], d['subtitle'], 9)
lab(s, d['today'], ML, 1.1, 2.6)
lab(s, d['invests'], 3.5, 1.1, 2.0, color=GOLD, align='center', spacing=1.0)
lab(s, d['after'], 5.6, 1.1, 3.0)
# today
box(s, ML, 1.42, 2.6, 0.62, d['parent'])
line(s, 1.86, 2.04, 1.86, 2.76, DARK, 1.0, arrow=True)
text(s, d['pct_today'], 1.98, 2.14, 1.3, 0.45, size=30, bold=True, color=GOLD, anchor='middle')
box(s, ML, 2.78, 2.6, 0.8, d['fsl'], fill=YELLOW, lc=YELLOW, s1=22)
text(s, d['fsl_sub'], ML, 3.22, 2.6, 0.28, size=LAB, color=DARK, align='center')
# investment
chevron(s, 4.15, 1.9, 0.7, 0.95)
text(s, d['invest_text'], 3.3, 2.95, 2.4, 0.6, size=16, color=MID, align='center')
# after
box(s, 5.6, 1.42, 1.72, 0.62, d['parent'])
box(s, 7.5, 1.42, 1.94, 0.62, d['danantara'], lc=YELLOW, lw=1.5)
xa, xb = 6.46, 8.47
bus = 2.4
line(s, xa, 2.04, xa, bus, DARK, 1.0); line(s, xb, 2.04, xb, bus, DARK, 1.0); line(s, xa, bus, xb, bus, DARK, 1.0)
xm = (xa + xb) / 2
line(s, xm, bus, xm, 2.76, DARK, 1.0, arrow=True)
text(s, d['pct_fks'], xa - 0.95, 2.06, 0.88, 0.4, size=26, bold=True, color=DARK, align='right', anchor='middle')
text(s, d['pct_dan'], xb + 0.07, 2.06, 0.9, 0.4, size=26, bold=True, color=GOLD, anchor='middle')
box(s, 5.9, 2.78, 3.34, 0.8, d['fsl'], fill=YELLOW, lc=YELLOW, s1=22)
text(s, d['fsl_sub'], 5.9, 3.22, 3.34, 0.28, size=LAB, color=DARK, align='center')
line(s, xm, 3.58, xm, 3.76, DARK, 1.0, arrow=True)
rect(s, 5.0, 3.78, MR - 5.0, 1.14, fill=PANEL, name='Platform panel')
lab(s, d['operating_label'], 5.15, 3.86, 2.3, color=GOLD, spacing=1.0)
for j, nm in enumerate(d['operating']):
    text(s, nm, 5.15, 4.1 + j * 0.26, 2.2, 0.26, size=16, color=DARK)
lab(s, d['pipeline_label'], 7.7, 3.86, 1.7, color=GOLD)
for j, nm in enumerate(d['pipeline']):
    text(s, nm, 7.7, 4.1 + j * 0.26, 1.7, 0.26, size=16, color=DARK)
text(s, d['illus'], ML, 4.98, 4.4, 0.2, size=12, bold=True, color=GOLD, spacing=1.0)
notes(s, d['notes'])

# ==================================================================== 10 DISCLAIMER
s = prs.slides.add_slide(L_DISC)
text(s, '10', 9.0, 5.2, 0.44, 0.2, size=8, color=DARK, align='right', name='Page number')
notes(s, C.DISCLAIMER_NOTES)

prs.save(OUT)
print('written', OUT, 'slides', len(prs.slides))
