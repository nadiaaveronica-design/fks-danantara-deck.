#!/usr/bin/env python3
"""Render deck.pptx -> deck.pdf -> render/<stem>-NN.png (+ contact sheet). Usage: render.py deck.pptx [dpi]"""
import sys, os, subprocess, glob, shutil
import pymupdf
from PIL import Image, ImageDraw
SOFFICE = '/root/.claude/skills/synced/ca1271e6-ddce-4c4e-8f01-c832fbb88730_653470ac-0907-46f7-93c1-15505bb7874c/pptx/scripts/office/soffice.py'
src = sys.argv[1]; dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 110
stem = os.path.splitext(os.path.basename(src))[0]
outdir = os.path.join(os.path.dirname(os.path.abspath(src)), 'render')
os.makedirs(outdir, exist_ok=True)
for f in glob.glob(os.path.join(outdir, stem + '-*.png')): os.remove(f)
subprocess.run(['python3', SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', outdir, src], check=True, capture_output=True)
pdf = os.path.join(outdir, stem + '.pdf')
doc = pymupdf.open(pdf)
paths = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=dpi)
    p = os.path.join(outdir, '%s-%02d.png' % (stem, i + 1)); pix.save(p); paths.append(p)
# contact sheet
ims = [Image.open(p) for p in paths]
tw, th = ims[0].size; cols = 3; rows = (len(ims) + cols - 1) // cols; sc = 0.5
sheet = Image.new('RGB', (int(cols * tw * sc) + (cols + 1) * 10, int(rows * th * sc) + (rows + 1) * 10), (60, 60, 60))
for i, im in enumerate(ims):
    r, c = divmod(i, cols); im2 = im.resize((int(tw * sc), int(th * sc)))
    sheet.paste(im2, (10 + c * (im2.width + 10), 10 + r * (im2.height + 10)))
sp = os.path.join(outdir, stem + '-sheet.png'); sheet.save(sp)
print('\n'.join(paths)); print(sp)
