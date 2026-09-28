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

def takeaway(s, txt, y):
    chevron(s, ML, y + 0.07, 0.12, 0.16)
    text(s, txt, ML + 0.22, y, MR - ML - 0.22, 0.3, size=11, bold=True, color=DARK, anchor='middle')

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
    dd = 0.14 + math.sqrt(cl['w']) * 0.44
    oval(s, x - dd / 2, y - dd / 2, dd, dd, fill=CREAM2, line=None, name='Halo ' + cl['name'])
    oval(s, x - 0.055, y - 0.055, 0.11, 0.11, fill=YELLOW, name='Dot ' + cl['name'])
    text(s, cl['name'], x + cl['dx'], y + cl['dy'], 1.3, 0.18, size=8, bold=True, color=MID, spacing=1)
sy = 1.32 + mh + 0.2
text(s, d['shares'][0][0], 5.3, sy, 1.4, 0.2, size=8.5, bold=True, color=GOLD, spacing=1.5)
text(s, d['shares'][0][1], 5.3, sy + 0.22, 1.9, 0.5, size=26, bold=True, color=DARK, anchor='middle')
text(s, d['share_rows'][0], 5.3, sy + 0.72, 1.9, 0.2, size=9, color=MID)
text(s, d['shares'][0][2], 7.4, sy + 0.22, 1.9, 0.5, size=26, bold=True, color=DARK, anchor='middle')
text(s, d['share_rows'][1], 7.4, sy + 0.72, 1.9, 0.2, size=9, color=MID)
text(s, d['share_other'], 5.3, sy + 1.0, 4.14, 0.36, size=9, color=DARK, line_spacing=1.05)
text(s, d['share_source'], 5.3, sy + 1.38, 4.14, 0.2, size=7.5, italic=True, color=MID)
takeaway(s, d['takeaway'], 4.72)
notes(s, d['notes'])

# ==================================================================== 3 OPPORTUNITY
d = C.S3
s = content_slide(d['title'], d['subtitle'], 3)
label(s, 'The gateway landscape', ML, 1.08, 4)
tw, tg, ty, th = 2.1, 0.16, 1.3, 0.64
for i, (num, lab) in enumerate(d['tiles']):
    tx = ML + i * (tw + tg)
    last = i == len(d['tiles']) - 1
    rect(s, tx, ty, tw, th, fill=CREAM2 if last else PANEL, name='Tile %d' % (i + 1))
    text(s, num, tx + 0.15, ty + 0.04, tw - 0.3, 0.34, size=22, bold=True, color=GOLD if last else DARK, anchor='middle')
    text(s, lab, tx + 0.15, ty + 0.38, tw - 0.3, 0.24, size=9, color=MID)
text(s, d['tile_note'], ML + 3 * (tw + tg), ty + th + 0.02, tw, 0.18, size=8, italic=True, color=MID, align='right')
for j, (lab, names, col) in enumerate([(d['list_fks'][0], d['list_fks'][1], GOLD), (d['list_conv'][0], d['list_conv'][1], MID)]):
    yy = 2.02 + j * 0.23
    text(s, lab, ML, yy + 0.02, 2.45, 0.2, size=7.5, bold=True, color=col, spacing=1.5)
    text(s, names, 3.05, yy, 6.4, 0.22, size=9.5, color=DARK)
text(s, d['list_note'], ML, 2.48, 8.88, 0.18, size=7.5, italic=True, color=MID)
label(s, 'What happens there today', ML, 2.76, 3.5)
fy = 3.1
ship(s, ML, fy + 0.04, 1.7, 0.58, GREY, aft_left=True)
crane(s, ML + 0.85, fy - 0.16, 0.85, 0.56, GREY2)
text(s, 'GRAB', ML + 1.72, fy - 0.12, 0.5, 0.16, size=7.5, bold=True, color=MID, spacing=1)
hopper(s, 2.85, fy + 0.06, 0.55, 0.56, GREY)
for k in range(3):
    truck(s, 3.75 + k * 0.98, fy + 0.24, 0.85, 0.38, GREY2 if k == 0 else GREY)
line(s, 6.75, fy + 0.42, 7.15, fy + 0.42, GREY2, 1.0, arrow=True)
mill(s, 7.3, fy + 0.04, 1.1, 0.58, GREY2)
line(s, ML, fy + 0.64, 8.5, fy + 0.64, LINE, 0.75)
for cap, cx, cw in [('VESSEL', ML, 1.7), ('HOPPER', 2.75, 0.75), ('TRUCKS', 3.75, 2.8), ('CUSTOMER', 7.2, 1.3)]:
    text(s, cap, cx, fy + 0.69, cw, 0.16, size=7.5, bold=True, color=MID, align='center', spacing=1.5)
text(s, [('Discharge speed ', {}), ('= ', {'color': YELLOW}), ('truck availability', {})], ML, fy + 0.9, 8.88, 0.3, size=13, bold=True, color=DARK, anchor='middle')
cy = fy + 1.28
for i, (lab, num, sub) in enumerate(d['consequences']):
    cx = ML + i * 3.06
    text(s, lab, cx, cy, 2.76, 0.18, size=8, bold=True, color=MID, spacing=1.5)
    text(s, num, cx, cy + 0.19, 2.76, 0.36, size=20, bold=True, color=DARK, anchor='middle')
    text(s, sub, cx, cy + 0.56, 2.76, 0.36, size=9, color=MID, line_spacing=1.05)
notes(s, d['notes'])

# ==================================================================== 4 FKS MODEL
d = C.S4
s = content_slide(d['title'], d['subtitle'], 4)
rect(s, ML, 1.1, MR - ML, 3.35, fill=CREAM, name='FKS panel')
label(s, d['panel_label'], 0.75, 1.22, 3, color=GOLD)
gy = 3.55
line(s, 2.0, gy, 9.25, gy, GREY, 1.0)
rect(s, 0.7, gy, 1.55, 0.05, fill=LINE)
ship(s, 0.72, 2.8, 1.5, 0.75, DARK, hatches=5, aft_left=True, hatch_color=YELLOW2)
unloader(s, 1.95, 2.1, 0.75, 1.45, YELLOW)
conveyor(s, 2.62, 2.3, 1.3, YELLOW, thickness=0.07, legs=3, leg_h=1.18)
warehouse(s, 3.95, 2.2, 2.1, 1.35, YELLOW)
truck(s, 6.4, 3.07, 0.95, 0.48, DARK, cab_color=YELLOW)
line(s, 7.45, 3.31, 7.75, 3.31, GREY2, 1.0, arrow=True)
silos(s, 7.85, 2.75, 0.5, 0.8, 3, DARK)
mill(s, 8.42, 2.75, 0.85, 0.8, DARK)
# direct-to-mill bypass: from the warehouse roof apex up, across, down onto the mill roof
line(s, 5.0, 2.2, 5.0, 1.92, GOLD2, 1.0, dash=True); line(s, 5.0, 1.92, 8.9, 1.92, GOLD2, 1.0, dash=True); line(s, 8.9, 1.92, 8.9, 2.72, GOLD2, 1.0, dash=True, arrow=True)
text(s, d['direct'], 5.6, 1.66, 3.2, 0.22, size=8.5, italic=True, color=GOLD, align='right')
for cap, cx, cw in [(d['captions'][0], 0.72, 1.2), (d['captions'][1], 1.95, 0.8), (d['captions'][2], 2.62, 1.3), (d['captions'][3], 3.8, 2.4), (d['captions'][4], 6.35, 1.05), (d['captions'][5], 7.85, 1.42)]:
    text(s, cap, cx, 3.65, cw, 0.18, size=7.5, bold=True, color=DARK, align='center', spacing=1.5)
bracket(s, 0.72, 3.9, 3.98); bracket(s, 6.4, 9.27, 3.98)
text(s, d['marine'], 0.72, 4.04, 3.15, 0.2, size=7.5, bold=True, color=DARK, align='center', spacing=0.5)
text(s, d['inland'], 6.4, 4.04, 2.87, 0.2, size=7.5, bold=True, color=DARK, align='center', spacing=1)
rrect(s, 3.95, 3.92, 2.4, 0.32, fill=YELLOW, radius=0.16, name='Buffer chip')
text(s, d['buffer'], 3.95, 3.92, 2.4, 0.32, size=8.5, bold=True, color=DARK, align='center', anchor='middle')
label(s, d['scope_label'], ML, 4.66, 1.0, color=GOLD)
text(s, d['scope_line'], 1.55, 4.63, 7.9, 0.26, size=8.5, color=DARK, anchor='middle')
notes(s, d['notes'])

# ==================================================================== 5 VALUE
d = C.S5
s = content_slide(d['title'], d['subtitle'], 5)
cx = [ML, 3.62, 6.68]; cw = 2.76
line(s, 3.47, 1.1, 3.47, 4.78, LINE, 0.75); line(s, 6.53, 1.1, 6.53, 4.78, LINE, 0.75)
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
text(s, d['faster_big'], x, 3.76, cw, 0.48, size=26, bold=True, color=DARK, anchor='middle')
text(s, d['faster_label'], x, 4.24, cw, 0.22, size=9, color=MID)
text(s, d['faster_small'], x, 4.46, cw, 0.3, size=8, italic=True, color=MID, line_spacing=1.05)
# BETTER ECONOMICS
x = cx[1]
text(s, [(d['chain'][0], {}), ('  →  ', {'color': YELLOW}), (d['chain'][1], {})], x, 1.75, cw, 0.22, size=9.5, bold=True, color=DARK)
text(s, [(d['chain'][2], {}), ('  →  ', {'color': YELLOW}), (d['chain'][3], {})], x, 1.97, cw, 0.22, size=9.5, bold=True, color=DARK)
text(s, 'CONVENTIONAL', x, 2.35, 1.5, 0.18, size=7.5, bold=True, color=MID, spacing=1.5)
ship(s, x, 2.56, 0.6, 0.27, GREY, hatches=2); ship(s, x + 0.68, 2.56, 0.6, 0.27, GREY, hatches=2)
text(s, d['parcel_conv'], x + 1.4, 2.5, 1.36, 0.4, size=9, color=MID, line_spacing=1.05)
text(s, 'FKS', x, 2.95, 1.0, 0.18, size=7.5, bold=True, color=MID, spacing=1.5)
ship(s, x, 3.13, 1.25, 0.42, DARK, hatches=4, hatch_color=YELLOW)
text(s, d['parcel_fks'], x + 1.4, 3.15, 1.36, 0.4, size=9, color=MID, line_spacing=1.05)
rrect(s, x, 3.74, cw, 0.74, fill=CREAM, line=YELLOW, lw=1.0, radius=0.08, name='Freight placeholder')
text(s, d['econ_big'], x + 0.12, 3.8, cw - 0.24, 0.32, size=14, bold=True, color=DARK, anchor='middle')
text(s, d['econ_label'], x + 0.12, 4.12, cw - 0.24, 0.3, size=7.5, bold=True, color=GOLD, spacing=1.2, line_spacing=1.05)
text(s, d['econ_small'], x, 4.54, cw, 0.2, size=8, italic=True, color=MID)
# MORE SECURE
x = cx[2]
for j, (lab, txt, col, wbar, y) in enumerate([('CONVENTIONAL', d['loss_conv'], GREY, 0.95, 1.78), ('FKS', d['loss_fks'], YELLOW, 0.38, 2.1)]):
    text(s, lab, x, y + 0.03, 1.0, 0.2, size=7.5, bold=True, color=MID, spacing=1.5)
    rect(s, x + 1.05, y, wbar, 0.24, fill=col)
    text(s, txt, x + 1.05 + wbar + 0.06, y, 0.7, 0.24, size=10, bold=True, color=DARK, anchor='middle')
text(s, d['loss_sub'], x, 2.4, cw, 0.34, size=8.5, color=MID, line_spacing=1.05)
for j, pt in enumerate(d['secure_points']):
    rect(s, x, 2.9 + j * 0.26, 0.09, 0.09, fill=YELLOW)
    text(s, pt, x + 0.17, 2.84 + j * 0.26, cw - 0.2, 0.22, size=10, bold=True, color=DARK)
text(s, d['secure_big'], x, 3.76, cw, 0.48, size=26, bold=True, color=DARK, anchor='middle')
text(s, d['secure_label'], x, 4.24, cw, 0.22, size=9, color=MID)
text(s, d['secure_small'], x, 4.46, cw, 0.2, size=8, italic=True, color=MID)
line(s, ML, 4.86, MR, 4.86, LINE, 0.75)
text(s, d['footer'], ML, 4.9, MR - ML, 0.2, size=8.5, color=MID)
notes(s, d['notes'])

# ==================================================================== 6 PLATFORM
d = C.S6
s = content_slide(d['title'], d['subtitle'], 6)
pj, mh = draw_map(s, ML, 1.12, 5.3, ID_BBOX)
for site in d['sites']:
    x, y = pj(site['lon'], site['lat'])
    oval(s, x - 0.08, y - 0.08, 0.16, 0.16, fill=YELLOW, line=WHITE, lw=0.75, name='Site ' + site['name'])
    al = 'right' if site['dx'] < 0 else 'left'
    text(s, site['name'], x + site['dx'], y + site['dy'], 1.1, 0.18, size=8, bold=True, color=DARK, spacing=1.5, align=al)
by = 1.12 + mh + 0.2
text(s, d['big'], ML, by, 2.4, 0.66, size=40, bold=True, color=DARK, anchor='middle')
text(s, d['big_sub1'], ML, by + 0.7, 5.3, 0.24, size=11, color=DARK)
text(s, d['big_sub2'], ML, by + 0.95, 5.3, 0.26, size=11, bold=True, color=DARK)
text(s, d['big_note'], ML, by + 1.3, 5.3, 0.2, size=8, italic=True, color=MID)
for i, site in enumerate(d['sites']):
    y = 1.12 + i * 1.27
    picture(s, A(site['photo']), 6.05, y, 1.02, 1.02, name='Photo ' + site['name'])
    text(s, site['name'], 7.2, y - 0.02, 1.5, 0.24, size=11, bold=True, color=DARK, spacing=1)
    text(s, site['mtpa'], 8.4, y - 0.02, 1.04, 0.24, size=12, bold=True, color=GOLD, align='right')
    text(s, site['place'], 7.2, y + 0.22, 2.24, 0.2, size=8.5, color=MID)
    text(s, site['line'], 7.2, y + 0.43, 2.24, 0.36, size=9.5, color=DARK, line_spacing=1.05)
    text(s, site['partner'], 7.2, y + 0.82, 2.24, 0.2, size=8.5, italic=True, color=MID)
    if i < 2:
        line(s, 6.05, y + 1.14, MR, y + 1.14, LINE, 0.75)
notes(s, d['notes'])

# ==================================================================== 7 JOURNEY
d = C.S7
s = content_slide(d['title'], d['subtitle'], 7)
n = len(d['stages']); cg = 0.195; cw = (MR - ML - (n - 1) * cg) / n
phY, phH = 1.12, 1.72
ty = 3.05
line(s, ML, ty, MR, ty, LINE, 1.0, arrow=True)
for i, st in enumerate(d['stages']):
    x = ML + i * (cw + cg)
    if st.get('photo'):
        picture(s, A(st['photo']), x, phY, cw, phH, name='Photo ' + st['loc'])
    else:
        rect(s, x, phY, cw, phH, fill=PANEL, name='Next panel')
        mw = cw - 0.24; mmh = map_height(mw, WEST_BBOX)
        pj, mh = draw_map(s, x + 0.12, phY + (phH - mmh) / 2 + 0.1, mw, WEST_BBOX, land='D0D2D4', neighbours='E4E5E6')
        for site in C.S8['sites']:
            if site['kind'] == 'watch':
                continue
            sx, sy = pj(site['lon'], site['lat']); sx += site.get('mdx', 0) * 0.5; sy += site.get('mdy', 0) * 0.5
            if site['kind'] == 'fks':
                oval(s, sx - 0.04, sy - 0.04, 0.08, 0.08, fill=YELLOW, line=WHITE, lw=0.5)
            else:
                oval(s, sx - 0.05, sy - 0.05, 0.1, 0.1, fill=WHITE, line=YELLOW, lw=1.25)
        text(s, 'NEXT', x + 0.12, phY + 0.08, 0.8, 0.16, size=7.5, bold=True, color=GOLD, spacing=2)
    last = i == n - 1
    if last:
        oval(s, x, ty - 0.07, 0.14, 0.14, fill=WHITE, line=YELLOW, lw=1.25)
    else:
        oval(s, x, ty - 0.07, 0.14, 0.14, fill=YELLOW)
    text(s, st['years'], x, ty + 0.13, cw, 0.3, size=13, bold=True, color=GOLD)
    text(s, st['loc'], x, ty + 0.43, cw, 0.26, size=11, bold=True, color=DARK)
    text(s, st['place'], x, ty + 0.69, cw, 0.2, size=8.5, color=MID)
    text(s, st['text'], x, ty + 0.96, cw, 0.95, size=9.5, color=DARK, line_spacing=1.08)
notes(s, d['notes'])

# ==================================================================== 8 PIPELINE
d = C.S8
s = content_slide(d['title'], d['subtitle'], 8)
pj, mh = draw_map(s, ML, 1.12, 4.3, WEST_BBOX)
for site in d['sites']:
    x, y = pj(site['lon'], site['lat']); x += site.get('mdx', 0); y += site.get('mdy', 0)
    k = site['kind']
    al = 'right' if site['dx'] < -0.5 else 'left'
    if k == 'fks':
        if site['name'] in ('CIGADING', 'TELUK LAMONG'):
            oval(s, x - 0.13, y - 0.13, 0.26, 0.26, fill=None, line=YELLOW, lw=1.25, name='Expansion ' + site['name'])
        oval(s, x - 0.08, y - 0.08, 0.16, 0.16, fill=YELLOW, line=WHITE, lw=0.75, name='Site ' + site['name'])
        text(s, site['name'], x + site['dx'], y + site['dy'], 1.2, 0.18, size=8, bold=True, color=DARK, spacing=1.5, align=al)
    elif k == 'new':
        oval(s, x - 0.1, y - 0.1, 0.2, 0.2, fill=WHITE, line=YELLOW, lw=1.75, name='New ' + site['name'])
        text(s, site['name'], x + site['dx'], y + site['dy'], 1.2, 0.18, size=8, bold=True, color=GOLD, spacing=1.5, align=al)
    else:
        oval(s, x - 0.06, y - 0.06, 0.12, 0.12, fill=WHITE, line=GREY, lw=1.0, name='Watch ' + site['name'])
        text(s, site['name'], x + site['dx'], y + site['dy'], 0.9, 0.16, size=7.5, color=MID, align='center' if site['dx'] < 0 else al)
ly = 1.12 + mh + 0.18
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
    py = 1.12 + i * 1.66; ph = 1.54
    rect(s, px, py, pw, ph, fill=PANEL, name='Card ' + p['name'])
    text(s, p['name'], px + 0.18, py + 0.08, 1.3, 0.26, size=12, bold=True, color=DARK, spacing=1)
    text(s, p['place'], px + 1.42, py + 0.11, 1.3, 0.22, size=8.5, color=MID)
    text(s, p['tag'], px + pw - 2.2, py + 0.1, 2.02, 0.22, size=7.5, bold=True, color=GOLD, align='right', spacing=1.2)
    text(s, p['num'], px + 0.18, py + 0.36, 1.2, 0.34, size=17, bold=True, color=DARK, anchor='middle')
    text(s, p['num_sub'], px + 1.42, py + 0.35, pw - 1.6, 0.36, size=8.5, color=MID, line_spacing=1.05)
    for j, (k, v) in enumerate(p['rows']):
        ry = py + 0.74 + j * 0.2
        text(s, k, px + 0.18, ry, 0.85, 0.2, size=7.5, bold=True, color=MID, spacing=1.5)
        text(s, v, px + 1.05, ry, pw - 1.2, 0.2, size=8.5, color=DARK)
ny = 1.12 + 1.66 + 1.54 + 0.06
text(s, d['cards_note'], px, ny, pw, 0.18, size=7.5, italic=True, color=MID)
ey = ny + 0.26
rect(s, px, ey, pw, 0.44, fill=CREAM, name='Expansion strip')
text(s, d['expansions_label'], px + 0.18, ey, 1.2, 0.44, size=7.5, bold=True, color=GOLD, spacing=1.5, anchor='middle')
text(s, d['expansions'], px + 1.42, ey + 0.03, pw - 1.6, 0.38, size=8.5, color=DARK, anchor='middle', line_spacing=1.05)
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
label(s, d['after'], 5.15, 1.1, 1.8)
text(s, d['illus'], 7.0, 1.1, 2.44, 0.22, size=7.5, bold=True, color=GOLD, align='right', spacing=0.8)
box(5.15, 1.35, 2.0, 0.5, d['parent'])
box(7.44, 1.35, 2.0, 0.5, d['danantara'], lc=YELLOW, lw=1.75, c1=DARK)
busy = 2.14
line(s, 6.15, 1.85, 6.15, busy, DARK, 1.0); line(s, 8.44, 1.85, 8.44, busy, DARK, 1.0); line(s, 6.15, busy, 8.44, busy, DARK, 1.0)
text(s, '51%', 5.5, 1.88, 0.58, 0.24, size=10, bold=True, color=DARK, align='right')
text(s, '49%', 8.52, 1.88, 0.6, 0.24, size=10, bold=True, color=GOLD)
line(s, 7.3, busy, 7.3, 2.3, DARK, 1.0, arrow=True)
box(6.0, 2.3, 2.6, 0.62, d['fsl'], d['fsl_sub'], fill=YELLOW, lc=YELLOW, c1=DARK, c2=DARK, s1=12)
line(s, 7.3, 2.92, 7.3, 3.1, DARK, 1.0, arrow=True)
rect(s, ML, 3.12, MR - ML, 1.32, fill=PANEL, name='Platform panel')
label(s, d['portfolio_label'], 0.72, 3.2, 1.6, color=MID, size=8)
text(s, d['portfolio_note'], 2.1, 3.19, 7.2, 0.2, size=8, italic=True, color=MID)
label(s, 'Operating today', 0.72, 3.46, 2.5, color=GOLD)
bw, bg = 1.1, 0.12
for i, (nm, ent) in enumerate(d['operating']):
    box(0.72 + i * (bw + bg), 3.68, bw, 0.55, nm, ent, lc=DARK, lw=0.75, s1=9.5)
px0 = MR - 0.16 - 4 * bw - 3 * bg
label(s, 'Pipeline', px0, 3.46, 2.0, color=GOLD)
for i, (nm, ent) in enumerate(d['pipeline']):
    box(px0 + i * (bw + bg), 3.68, bw, 0.55, nm, lc=YELLOW, lw=1.0, dash=True, s1=9)
for j, (k, v) in enumerate([d['fit'], d['next']]):
    yy = 4.56 + j * 0.27
    text(s, k, ML, yy + 0.02, 1.15, 0.2, size=7.5, bold=True, color=GOLD, spacing=1.5)
    text(s, v, 1.75, yy, MR - 1.75, 0.24, size=8.5, color=DARK)
notes(s, d['notes'])

# ==================================================================== 10 DISCLAIMER
s = prs.slides.add_slide(L_DISC)
text(s, '10', 9.0, 5.2, 0.44, 0.2, size=8, color=DARK, align='right', name='Page number')
notes(s, C.DISCLAIMER_NOTES)

prs.save(OUT)
print('written', OUT, 'slides', len(prs.slides))
