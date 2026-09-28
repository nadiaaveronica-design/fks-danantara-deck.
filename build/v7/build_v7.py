# -*- coding: utf-8 -*-
"""Build FKS_Danantara_Strategic_Partnership_v7.pptx on the FKS template with the v6 visual identity."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_v7 import *
import content_v7 as C

OUT = sys.argv[1] if len(sys.argv) > 1 else 'v7_raw.pptx'
TEMPLATE = os.path.join(HERE, 'template_BACKUP.pptx')

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

def bracket(s, x1, x2, y, color=DARK, tick=0.08):
    line(s, x1, y, x2, y, color, 1.0); line(s, x1, y - tick, x1, y, color, 1.0); line(s, x2, y - tick, x2, y, color, 1.0)

# ==================================================================== 1 COVER
s = prs.slides.add_slide(L_COVER)
s.placeholders[0].text_frame.text = C.COVER['title']
for r in s.placeholders[0].text_frame.paragraphs[0].runs:
    r.font.size = Pt(22); r.font.bold = True; r.font.color.rgb = rgb(DARK); r.font.name = FONT
s.placeholders[1].height = I(0.9)
tf = s.placeholders[1].text_frame
tf.text = C.COVER['sub1']
for r in tf.paragraphs[0].runs:
    r.font.size = Pt(15); r.font.color.rgb = rgb(MID); r.font.name = FONT; r.font.bold = False
p = tf.add_paragraph(); r = p.add_run(); r.text = C.COVER['sub2']; r.font.size = Pt(10.5); r.font.color.rgb = rgb(MID); r.font.name = FONT
notes(s, C.COVER['notes'])

# ==================================================================== 2 MARKET
d = C.S2
s = content_slide(d['title'], d['subtitle'], 2)
label(s, 'What arrives every year', ML, 1.1, 3.6)
text(s, d['total'], ML, 1.28, 1.95, 0.62, size=36, bold=True, color=DARK, anchor='middle')
text(s, d['total_sub'], 2.52, 1.36, 1.95, 0.5, size=10, color=MID, line_spacing=1.05)
y0, dy = 2.12, 0.6
for i, r in enumerate(d['rows']):
    y = y0 + i * dy
    picture(s, A(r['icon']), ML, y, 0.46, 0.46, name='Icon ' + r['name'])
    text(s, r['name'], 1.15, y - 0.01, 1.75, 0.24, size=11, bold=True, color=DARK)
    text(s, r['sub'], 1.15, y + 0.23, 1.75, 0.2, size=9, color=MID)
    L = r['mt'] / 11.7 * 1.2
    rect(s, 2.95, y + 0.1, L, 0.26, fill=YELLOW, name='Bar ' + r['name'])
    text(s, '%.1f Mt' % r['mt'], 2.95 + L + 0.08, y + 0.08, 0.9, 0.3, size=12, bold=True, color=DARK, anchor='middle')
chevron(s, 4.68, 1.33, 0.28, 0.42)
label(s, 'Where it is milled', 5.3, 1.1, 4.1)
pj, mh = draw_map(s, 5.3, 1.32, 4.14, ID_BBOX)
for cl in d['clusters']:
    x, y = pj(cl['lon'], cl['lat'])
    dd = 0.12 + math.sqrt(cl['w']) * 0.42
    oval(s, x - dd / 2, y - dd / 2, dd, dd, fill=CREAM2, line=None, name='Halo ' + cl['name'])
    oval(s, x - 0.05, y - 0.05, 0.1, 0.1, fill=YELLOW, name='Dot ' + cl['name'])
    text(s, cl['name'], x + cl['dx'], y + cl['dy'], 1.2, 0.18, size=7.5, bold=True, color=MID, spacing=1)
sy = 1.32 + mh + 0.18
cols = [5.3, 6.72, 8.14]
for i, (hdr, f, fd) in enumerate(d['shares']):
    cx = cols[i]
    text(s, hdr, cx, sy, 1.3, 0.2, size=8.5, bold=True, color=GOLD if i == 0 else MID, spacing=1.5)
    text(s, f, cx, sy + 0.22, 1.3, 0.38, size=20, bold=True, color=DARK, anchor='middle')
    text(s, d['share_rows'][0], cx, sy + 0.6, 1.3, 0.2, size=8.5, color=MID)
    text(s, fd, cx, sy + 0.88, 1.3, 0.38, size=20, bold=True, color=DARK, anchor='middle')
    text(s, d['share_rows'][1], cx, sy + 1.26, 1.3, 0.2, size=8.5, color=MID)
tri_marker(s, ML, 4.76)
text(s, d['takeaway'], 0.78, 4.68, 8.6, 0.3, size=11, bold=True, color=DARK, anchor='middle')
notes(s, d['notes'])

# ==================================================================== 3 OPPORTUNITY
d = C.S3
s = content_slide(d['title'], d['subtitle'], 3)
label(s, 'The gateway landscape', ML, 1.08, 4)
tw, tg, ty, th = 2.1, 0.16, 1.3, 0.72
for i, (num, lab) in enumerate(d['tiles']):
    tx = ML + i * (tw + tg)
    last = i == len(d['tiles']) - 1
    rect(s, tx, ty, tw, th, fill=CREAM2 if last else PANEL, name='Tile %d' % (i + 1))
    text(s, num, tx + 0.15, ty + 0.05, tw - 0.3, 0.38, size=22, bold=True, color=GOLD if last else DARK, anchor='middle')
    text(s, lab, tx + 0.15, ty + 0.44, tw - 0.3, 0.26, size=9, color=MID)
text(s, d['tile_note'], ML + 3 * (tw + tg), ty + th + 0.03, tw, 0.2, size=8.5, italic=True, color=MID, align='right')
for j, (lab, names, col) in enumerate([(d['list_fks'][0], d['list_fks'][1], GOLD), (d['list_conv'][0], d['list_conv'][1], MID)]):
    yy = 2.14 + j * 0.24
    text(s, lab, ML, yy, 2.35, 0.2, size=7.5, bold=True, color=col, spacing=1.5)
    text(s, names, 2.95, yy - 0.02, 6.5, 0.22, size=9.5, color=DARK)
label(s, 'What happens there today', ML, 2.62, 3.5)
text(s, [('Discharge speed ', {}), ('= ', {'color': YELLOW}), ('truck availability', {})], 4.5, 2.5, 4.94, 0.3, size=13, bold=True, color=DARK, align='right', anchor='middle')
fy = 2.98
ship(s, ML, fy + 0.04, 1.7, 0.58, GREY)
crane(s, ML + 0.85, fy - 0.16, 0.85, 0.56, GREY2)
text(s, 'GRAB', ML + 1.72, fy - 0.12, 0.5, 0.16, size=7.5, bold=True, color=MID, spacing=1)
hopper(s, 2.85, fy + 0.06, 0.55, 0.56, GREY)
for k in range(3):
    truck(s, 3.75 + k * 0.98, fy + 0.24, 0.85, 0.38, GREY2 if k == 0 else GREY)
line(s, 6.75, fy + 0.42, 7.15, fy + 0.42, GREY2, 1.0, arrow=True)
mill(s, 7.3, fy + 0.04, 1.1, 0.58, GREY2)
line(s, ML, fy + 0.64, 8.5, fy + 0.64, LINE, 0.75)
for cap, cx, cw in [('VESSEL', ML, 1.7), ('HOPPER', 2.75, 0.75), ('TRUCKS', 3.75, 2.8), ('CUSTOMER', 7.2, 1.3)]:
    text(s, cap, cx, fy + 0.7, cw, 0.16, size=7.5, bold=True, color=MID, align='center', spacing=1.5)
cy = 4.02
for i, (lab, num, sub) in enumerate(d['consequences']):
    cx = ML + i * 3.06
    text(s, lab, cx, cy, 2.76, 0.18, size=8, bold=True, color=MID, spacing=1.5)
    text(s, num, cx, cy + 0.2, 2.76, 0.4, size=20, bold=True, color=DARK, anchor='middle')
    text(s, sub, cx, cy + 0.62, 2.76, 0.38, size=9, color=MID, line_spacing=1.05)
notes(s, d['notes'])

# ==================================================================== 4 FKS MODEL
d = C.S4
s = content_slide(d['title'], d['subtitle'], 4)
rect(s, ML, 1.1, MR - ML, 2.95, fill=CREAM, name='FKS panel')
label(s, d['panel_label'], 0.75, 1.2, 3, color=GOLD)
gy = 3.3
line(s, 2.0, gy, 9.25, gy, GREY, 1.0)
rect(s, 0.7, gy, 1.55, 0.05, fill=LINE)
ship(s, 0.72, 2.55, 1.5, 0.75, DARK, hatches=5, aft_left=True, hatch_color=YELLOW2)
unloader(s, 1.95, 1.85, 0.75, 1.45, YELLOW)
conveyor(s, 2.62, 2.05, 1.3, YELLOW, thickness=0.07, legs=3, leg_h=1.18)
warehouse(s, 3.95, 1.95, 2.1, 1.35, YELLOW)
label(s, 'Buffer', 3.95, 1.62, 2.1, color=GOLD)
s.shapes[-1].text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
truck(s, 6.4, 2.82, 0.95, 0.48, DARK, cab_color=YELLOW)
line(s, 7.45, 3.06, 7.75, 3.06, GREY2, 1.0, arrow=True)
silos(s, 7.85, 2.5, 0.5, 0.8, 3, DARK)
mill(s, 8.42, 2.5, 0.85, 0.8, DARK)
line(s, 6.0, 1.95, 6.0, 1.78, GOLD2, 1.0, dash=True); line(s, 6.0, 1.78, 8.85, 1.78, GOLD2, 1.0, dash=True); line(s, 8.85, 1.78, 8.85, 2.45, GOLD2, 1.0, dash=True, arrow=True)
text(s, d['direct'], 6.1, 1.52, 2.8, 0.22, size=8.5, italic=True, color=GOLD, align='right')
for cap, cx, cw in [(d['captions'][0], 0.72, 1.2), (d['captions'][1], 1.95, 0.8), (d['captions'][2], 2.62, 1.3), (d['captions'][3], 3.95, 2.1), (d['captions'][4], 6.35, 1.05), (d['captions'][5], 7.85, 1.42)]:
    text(s, cap, cx, 3.4, cw, 0.18, size=7.5, bold=True, color=DARK, align='center', spacing=1.5)
bracket(s, 0.72, 3.9, 3.72); bracket(s, 6.4, 9.27, 3.72)
text(s, d['marine'], 0.72, 3.78, 3.18, 0.2, size=7.5, bold=True, color=DARK, align='center', spacing=1)
text(s, d['inland'], 6.4, 3.78, 2.87, 0.2, size=7.5, bold=True, color=DARK, align='center', spacing=1)
rrect(s, 4.05, 3.66, 2.2, 0.3, fill=YELLOW, radius=0.15, name='Buffer chip')
text(s, d['buffer'], 4.05, 3.66, 2.2, 0.3, size=7, bold=True, color=WHITE, align='center', anchor='middle', spacing=1)
label(s, d['scope_label'], ML, 4.32, 1.0, color=GOLD)
for i, item in enumerate(d['scope']):
    ix = 1.55 + i * 1.58
    rect(s, ix, 4.35, 0.09, 0.09, fill=YELLOW)
    text(s, item, ix + 0.16, 4.28, 1.4, 0.42, size=9, color=DARK, line_spacing=1.05)
notes(s, d['notes'])

# ==================================================================== 5 VALUE
d = C.S5
s = content_slide(d['title'], d['subtitle'], 5)
cx = [ML, 3.62, 6.68]; cw = 2.76
line(s, 3.47, 1.1, 3.47, 4.9, LINE, 0.75); line(s, 6.53, 1.1, 6.53, 4.9, LINE, 0.75)
for i, col in enumerate(d['cols']):
    text(s, col['k'], cx[i], 1.1, cw, 0.3, size=14, bold=True, color=DARK)
    text(s, col['sub'], cx[i], 1.4, cw, 0.2, size=9, color=MID)
# FASTER
x = cx[0]
text(s, [(d['rate_from'] + ' ', {}), ('→ ', {'color': YELLOW}), (d['rate_to'], {})], x, 1.75, cw, 0.45, size=24, bold=True, color=DARK, anchor='middle')
text(s, d['rate_sub'], x, 2.2, cw, 0.2, size=9, color=MID)
perday = 1.05 / 12
for j, (lab, days, col, y) in enumerate([('CONVENTIONAL', d['days_conv'], GREY, 2.58), ('FKS', d['days_fks'], YELLOW, 2.9)]):
    text(s, lab, x, y + 0.03, 1.0, 0.2, size=7.5, bold=True, color=MID, spacing=1.5)
    rect(s, x + 1.05, y, perday * days, 0.24, fill=col)
    text(s, '%d days' % days, x + 1.05 + perday * days + 0.06, y, 0.7, 0.24, size=10, bold=True, color=DARK, anchor='middle')
text(s, d['days_sub'], x, 3.2, cw, 0.2, size=9, color=MID)
text(s, d['saved'], x, 3.48, cw, 0.28, size=13, bold=True, color=GOLD)
text(s, d['faster_big'], x, 3.78, cw, 0.5, size=26, bold=True, color=DARK, anchor='middle')
text(s, d['faster_label'], x, 4.28, cw, 0.34, size=9, color=MID)
text(s, d['faster_small'], x, 4.62, cw, 0.2, size=8, italic=True, color=MID)
# BETTER ECONOMICS
x = cx[1]
text(s, [(d['chain'][0], {}), ('  \u276f  ', {'color': YELLOW}), (d['chain'][1], {})], x, 1.75, cw, 0.22, size=9.5, bold=True, color=DARK)
text(s, [(d['chain'][2], {}), ('  \u276f  ', {'color': YELLOW}), (d['chain'][3], {})], x, 1.97, cw, 0.22, size=9.5, bold=True, color=DARK)
text(s, 'CONVENTIONAL', x, 2.35, 1.5, 0.18, size=7.5, bold=True, color=MID, spacing=1.5)
ship(s, x, 2.56, 0.6, 0.27, GREY, hatches=2); ship(s, x + 0.68, 2.56, 0.6, 0.27, GREY, hatches=2)
text(s, d['parcel_conv'], x + 1.4, 2.5, 1.36, 0.4, size=9, color=MID, line_spacing=1.05)
text(s, 'FKS', x, 2.95, 1.0, 0.18, size=7.5, bold=True, color=MID, spacing=1.5)
ship(s, x, 3.13, 1.25, 0.42, DARK, hatches=4, hatch_color=YELLOW)
text(s, d['parcel_fks'], x + 1.4, 3.15, 1.36, 0.4, size=9, color=MID, line_spacing=1.05)
rrect(s, x, 3.76, cw, 0.76, fill=CREAM, line=YELLOW, lw=1.0, radius=0.08, name='Freight placeholder')
text(s, d['econ_big'], x + 0.12, 3.82, cw - 0.24, 0.32, size=14, bold=True, color=DARK, anchor='middle')
text(s, d['econ_label'], x + 0.12, 4.14, cw - 0.24, 0.3, size=7.5, bold=True, color=GOLD, spacing=1.2, line_spacing=1.05)
text(s, d['econ_small'], x, 4.62, cw, 0.2, size=8, italic=True, color=MID)
# MORE SECURE
x = cx[2]
for j, (lab, txt, col, wbar, y) in enumerate([('CONVENTIONAL', d['loss_conv'], GREY, 1.0, 1.78), ('FKS', d['loss_fks'], YELLOW, 0.4, 2.1)]):
    text(s, lab, x, y + 0.03, 1.0, 0.2, size=7.5, bold=True, color=MID, spacing=1.5)
    rect(s, x + 1.05, y, wbar, 0.24, fill=col)
    text(s, txt, x + 1.05 + wbar + 0.06, y, 0.7, 0.24, size=10, bold=True, color=DARK, anchor='middle')
text(s, d['loss_sub'], x, 2.4, cw, 0.2, size=9, color=MID)
for j, pt in enumerate(d['secure_points']):
    rect(s, x, 2.78 + j * 0.26, 0.09, 0.09, fill=YELLOW)
    text(s, pt, x + 0.17, 2.72 + j * 0.26, cw - 0.2, 0.22, size=10, bold=True, color=DARK)
text(s, d['secure_big'], x, 3.78, cw, 0.5, size=26, bold=True, color=DARK, anchor='middle')
text(s, d['secure_label'], x, 4.28, cw, 0.34, size=9, color=MID)
text(s, d['secure_small'], x, 4.62, cw, 0.2, size=8, italic=True, color=MID)
notes(s, d['notes'])

# ==================================================================== 6 PLATFORM
d = C.S6
s = content_slide(d['title'], d['subtitle'], 6)
pj, mh = draw_map(s, ML, 1.15, 5.15, ID_BBOX)
for site in d['sites']:
    x, y = pj(site['lon'], site['lat'])
    oval(s, x - 0.075, y - 0.075, 0.15, 0.15, fill=YELLOW, line=WHITE, lw=0.75, name='Site ' + site['name'])
    text(s, site['name'], x + site['dx'], y + site['dy'], 1.1, 0.18, size=8, bold=True, color=DARK, spacing=1.5)
by = 1.15 + mh + 0.22
text(s, d['big'], ML, by, 1.75, 0.6, size=30, bold=True, color=DARK, anchor='middle')
text(s, d['big_sub1'], 2.4, by + 0.02, 3.3, 0.25, size=10, color=DARK)
text(s, d['big_sub2'], 2.4, by + 0.27, 3.3, 0.36, size=10, bold=True, color=DARK, line_spacing=1.05)
text(s, 'Partners: Pelindo (Belawan, Teluk Lamong)  ·  Krakatau Bandar Samudera (Cigading)', ML, by + 0.85, 5.15, 0.22, size=8.5, color=MID)
for i, site in enumerate(d['sites']):
    y = 1.15 + i * 1.25
    picture(s, A(site['photo']), 6.05, y, 0.95, 0.95, name='Photo ' + site['name'])
    text(s, site['name'], 7.12, y - 0.02, 1.5, 0.24, size=11, bold=True, color=DARK, spacing=1)
    text(s, site['mtpa'], 8.4, y - 0.02, 1.04, 0.24, size=12, bold=True, color=GOLD, align='right')
    text(s, site['place'], 7.12, y + 0.22, 2.32, 0.2, size=8.5, color=MID)
    text(s, site['line'], 7.12, y + 0.42, 2.32, 0.36, size=9.5, color=DARK, line_spacing=1.05)
    text(s, site['partner'], 7.12, y + 0.77, 2.32, 0.2, size=8.5, italic=True, color=MID)
    if i < 2:
        line(s, 6.05, y + 1.1, MR, y + 1.1, LINE, 0.75)
notes(s, d['notes'])

# ==================================================================== 7 JOURNEY
d = C.S7
s = content_slide(d['title'], d['subtitle'], 7)
n = len(d['stages']); cg = 0.195; cw = (MR - ML - (n - 1) * cg) / n
ty = 2.85
line(s, ML, ty, MR, ty, LINE, 1.0, arrow=True)
for i, st in enumerate(d['stages']):
    x = ML + i * (cw + cg)
    if st.get('photo'):
        picture(s, A(st['photo']), x, 1.12, cw, 1.48, name='Photo ' + st['loc'])
    else:
        rect(s, x, 1.12, cw, 1.48, fill=PANEL, name='Next panel')
        pj, mh = draw_map(s, x + 0.12, 1.12 + (1.48 - map_height(cw - 0.24, WEST_BBOX)) / 2 + 0.08, cw - 0.24, WEST_BBOX, land='D0D2D4', neighbours='E4E5E6')
        for site in C.S8['sites']:
            if site['kind'] == 'watch':
                continue
            sx, sy = pj(site['lon'], site['lat']); sx += site.get('mdx', 0) * 0.6; sy += site.get('mdy', 0) * 0.6
            if site['kind'] == 'fks':
                oval(s, sx - 0.05, sy - 0.05, 0.1, 0.1, fill=YELLOW, line=WHITE, lw=0.5)
            else:
                oval(s, sx - 0.06, sy - 0.06, 0.12, 0.12, fill=WHITE, line=YELLOW, lw=1.25)
        text(s, 'NEXT', x + 0.12, 1.18, 0.8, 0.16, size=7.5, bold=True, color=GOLD, spacing=2)
    last = i == n - 1
    if last:
        oval(s, x, ty - 0.07, 0.14, 0.14, fill=WHITE, line=YELLOW, lw=1.25)
    else:
        oval(s, x, ty - 0.07, 0.14, 0.14, fill=YELLOW)
    text(s, st['years'], x, 2.98, cw, 0.3, size=13, bold=True, color=GOLD)
    text(s, st['loc'], x, 3.28, cw, 0.26, size=11, bold=True, color=DARK)
    text(s, st['place'], x, 3.54, cw, 0.2, size=8.5, color=MID)
    text(s, st['text'], x, 3.81, cw, 0.95, size=9.5, color=DARK, line_spacing=1.08)
notes(s, d['notes'])

# ==================================================================== 8 PIPELINE
d = C.S8
s = content_slide(d['title'], d['subtitle'], 8)
pj, mh = draw_map(s, ML, 1.12, 4.3, WEST_BBOX)
for site in d['sites']:
    x, y = pj(site['lon'], site['lat']); x += site.get('mdx', 0); y += site.get('mdy', 0)
    k = site['kind']
    if k == 'fks':
        if site['name'] in ('CIGADING', 'TELUK LAMONG'):
            oval(s, x - 0.16, y - 0.16, 0.32, 0.32, fill=None, line=YELLOW, lw=1.25, name='Expansion ' + site['name'])
        oval(s, x - 0.085, y - 0.085, 0.17, 0.17, fill=YELLOW, line=WHITE, lw=0.75, name='Site ' + site['name'])
        text(s, site['name'], x + site['dx'], y + site['dy'], 1.2, 0.18, size=8, bold=True, color=DARK, spacing=1.5)
    elif k == 'new':
        oval(s, x - 0.11, y - 0.11, 0.22, 0.22, fill=WHITE, line=YELLOW, lw=1.75, name='New ' + site['name'])
        text(s, site['name'], x + site['dx'], y + site['dy'], 1.2, 0.18, size=8, bold=True, color=GOLD, spacing=1.5)
    else:
        oval(s, x - 0.06, y - 0.06, 0.12, 0.12, fill=WHITE, line=GREY, lw=1.0, name='Watch ' + site['name'])
        text(s, site['name'], x + site['dx'], y + site['dy'], 0.9, 0.16, size=7.5, color=MID)
ly = 1.12 + mh + 0.15
leg = [(0, 0), (1, 0), (0, 1), (1, 1)]
for (col, row), (kind, txt) in zip(leg, d['legend']):
    lx = ML + col * 2.2; yy = ly + row * 0.26
    if kind == 'fks':
        oval(s, lx, yy + 0.02, 0.14, 0.14, fill=YELLOW)
    elif kind == 'new':
        oval(s, lx, yy + 0.02, 0.14, 0.14, fill=WHITE, line=YELLOW, lw=1.75)
    elif kind == 'exp':
        oval(s, lx - 0.03, yy - 0.01, 0.2, 0.2, fill=None, line=YELLOW, lw=1.25); oval(s, lx + 0.035, yy + 0.055, 0.07, 0.07, fill=YELLOW)
    else:
        oval(s, lx + 0.01, yy + 0.03, 0.12, 0.12, fill=WHITE, line=GREY, lw=1.0)
    text(s, txt, lx + 0.24, yy, 1.9, 0.2, size=8.5, color=MID)
px, pw = 5.15, MR - 5.15
for i, p in enumerate(d['projects']):
    py = 1.12 + i * 1.78; ph = 1.62
    rect(s, px, py, pw, ph, fill=PANEL, name='Card ' + p['name'])
    text(s, p['name'], px + 0.18, py + 0.1, 1.3, 0.26, size=12, bold=True, color=DARK, spacing=1)
    text(s, p['place'], px + 1.42, py + 0.13, 1.6, 0.22, size=8.5, color=MID)
    text(s, p['tag'], px + pw - 1.45, py + 0.12, 1.27, 0.22, size=7.5, bold=True, color=GOLD, align='right', spacing=1.5)
    text(s, p['num'], px + 0.18, py + 0.38, 1.2, 0.36, size=17, bold=True, color=DARK, anchor='middle')
    text(s, p['num_sub'], px + 1.42, py + 0.38, pw - 1.6, 0.38, size=8.5, color=MID, line_spacing=1.05)
    for j, (k, v) in enumerate(p['rows']):
        ry = py + 0.8 + j * 0.21
        text(s, k, px + 0.18, ry, 0.85, 0.2, size=7.5, bold=True, color=MID, spacing=1.5)
        text(s, v, px + 1.05, ry, pw - 1.2, 0.2, size=8.5, color=DARK)
ey = 1.12 + 1.78 + 1.62 + 0.12
rect(s, px, ey, pw, 0.46, fill=CREAM, name='Expansion strip')
text(s, d['expansions_label'], px + 0.18, ey, 1.2, 0.46, size=7.5, bold=True, color=GOLD, spacing=1.5, anchor='middle')
text(s, d['expansions'], px + 1.42, ey + 0.03, pw - 1.6, 0.4, size=8.5, color=DARK, anchor='middle', line_spacing=1.05)
notes(s, d['notes'])

# ==================================================================== 9 STRUCTURE
d = C.S9
s = content_slide(d['title'], d['subtitle'], 9)
def box(x, y, w, h, t1, t2=None, fill=WHITE, lc=DARK, lw=1.0, c1=DARK, c2=MID, dash=None, s1=11):
    shape(s, MSO_SHAPE.RECTANGLE, x, y, w, h, fill, lc, lw, dash=dash)
    if t2:
        text(s, t1, x, y + 0.06, w, 0.28, size=s1, bold=True, color=c1, align='center', anchor='middle')
        text(s, t2, x, y + 0.32, w, 0.22, size=8.5, color=c2, align='center')
    else:
        text(s, t1, x, y, w, h, size=s1, bold=True, color=c1, align='center', anchor='middle')
label(s, d['today'], ML, 1.1, 2.7)
box(ML, 1.35, 2.7, 0.5, d['parent'])
line(s, 1.91, 1.85, 1.91, 2.28, DARK, 1.0, arrow=True)
text(s, '100%', 2.0, 1.9, 0.6, 0.28, size=10, bold=True, color=DARK, anchor='middle')
box(ML, 2.3, 2.7, 0.62, d['fsl'], d['fsl_sub'], fill=YELLOW, lc=YELLOW, c1=DARK, c2=DARK, s1=12)
label(s, d['invests'], 3.45, 1.1, 1.6, color=GOLD)
chevron(s, 3.95, 1.55, 0.5, 0.62)
text(s, d['invest_text'], 3.4, 2.3, 1.6, 0.5, size=9, color=MID, align='center', line_spacing=1.05)
label(s, d['after'], 5.15, 1.1, 2.6)
box(5.15, 1.35, 2.0, 0.5, d['parent'])
box(7.44, 1.35, 2.0, 0.5, d['danantara'], lc=YELLOW, lw=1.75, c1=DARK)
text(s, '51%', 5.35, 1.9, 0.7, 0.26, size=10, bold=True, color=DARK)
text(s, '49%', 8.55, 1.9, 0.89, 0.26, size=10, bold=True, color=GOLD, align='right')
text(s, 'illustrative, subject to negotiation', 7.5, 2.12, 1.94, 0.18, size=8, color=GOLD, align='right')
line(s, 6.15, 1.85, 6.15, 2.1, DARK, 1.0); line(s, 8.44, 1.85, 8.44, 2.1, DARK, 1.0); line(s, 6.15, 2.1, 8.44, 2.1, DARK, 1.0)
line(s, 7.3, 2.1, 7.3, 2.28, DARK, 1.0, arrow=True)
box(6.0, 2.3, 2.6, 0.62, d['fsl'], d['fsl_sub'], fill=YELLOW, lc=YELLOW, c1=DARK, c2=DARK, s1=12)
line(s, 7.3, 2.92, 7.3, 3.1, DARK, 1.0, arrow=True)
rect(s, ML, 3.12, MR - ML, 1.55, fill=PANEL, name='Platform panel')
text(s, d['portfolio_label'], 0.72, 3.2, 8.5, 0.2, size=8, bold=True, color=MID, spacing=1.2)
label(s, 'Operating today', 0.72, 3.5, 2.5, color=GOLD)
for i, (nm, ent) in enumerate(d['operating']):
    bx = 0.72 + i * 1.37
    box(bx, 3.72, 1.25, 0.55, nm, ent, lc=DARK, lw=0.75, s1=9.5)
label(s, 'Pipeline', 5.15, 3.5, 2.0, color=GOLD)
for i, (nm, ent) in enumerate(d['pipeline']):
    bx = 5.15 + i * 1.08
    box(bx, 3.72, 0.98, 0.55, nm, lc=YELLOW, lw=1.0, dash=True, s1=9)
text(s, d['agree'], 0.72, 4.4, 8.55, 0.22, size=8.5, color=MID)
notes(s, d['notes'])

# ==================================================================== 10 DISCLAIMER
s = prs.slides.add_slide(L_DISC)
text(s, '10', 9.0, 5.2, 0.44, 0.2, size=8, color=DARK, align='right', name='Page number')
notes(s, C.DISCLAIMER_NOTES)

prs.save(OUT)
print('written', OUT, 'slides', len(prs.slides))
