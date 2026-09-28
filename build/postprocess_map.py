#!/usr/bin/env python3
"""Replace MAP|... placeholder rectangles with editable freeform coastline shapes (a:custGeom).
Usage: postprocess_map.py in.pptx out.pptx
"""
import sys, re, json, zipfile, os, shutil, math

HERE = os.path.dirname(os.path.abspath(__file__))
POLYS = json.load(open(os.path.join(HERE, 'assets', 'map_polys.json')))
NEIGHBOURS = ['Malaysia', 'Singapore', 'Brunei', 'East Timor', 'Papua New Guinea', 'Philippines', 'Australia', 'Thailand', 'Vietnam', 'Cambodia']

def emu(v):
    return int(round(v))

def build_paths(countries, lon0, lat0, lon1, lat1, cx, cy):
    """Return <a:path> elements for polygons of the given countries projected into a cx x cy EMU box."""
    paths = []
    for c in countries:
        for ring in POLYS.get(c, []):
            pts = []
            for lon, lat in ring:
                X = (lon - lon0) / (lon1 - lon0) * cx
                Y = (lat1 - lat) / (lat1 - lat0) * cy
                pts.append((X, Y))
            # skip polygons entirely outside the box
            if all(p[0] < 0 or p[0] > cx or p[1] < 0 or p[1] > cy for p in pts):
                continue
            # clamp to box (simple clipping: clamp coordinates)
            pts = [(min(max(X, 0), cx), min(max(Y, 0), cy)) for X, Y in pts]
            # drop consecutive duplicates
            dd = []
            for p in pts:
                if not dd or (abs(dd[-1][0]-p[0]) > 1 or abs(dd[-1][1]-p[1]) > 1):
                    dd.append(p)
            if len(dd) < 3:
                continue
            seg = ['<a:moveTo><a:pt x="%d" y="%d"/></a:moveTo>' % (emu(dd[0][0]), emu(dd[0][1]))]
            for X, Y in dd[1:]:
                seg.append('<a:lnTo><a:pt x="%d" y="%d"/></a:lnTo>' % (emu(X), emu(Y)))
            seg.append('<a:close/>')
            paths.append('<a:path w="%d" h="%d">%s</a:path>' % (cx, cy, ''.join(seg)))
    return ''.join(paths)

SP_RE = re.compile(r'<p:sp>.*?</p:sp>', re.S)

def process_slide(xml):
    def repl(m):
        sp = m.group(0)
        nm = re.search(r'<p:cNvPr[^>]*name="(MAP\|[^"]+)"', sp)
        if not nm:
            return sp
        parts = nm.group(1).split('|')
        which = parts[1]
        lon0, lat0, lon1, lat1 = [float(v) for v in parts[2:6]]
        ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', sp)
        cx, cy = int(ext.group(1)), int(ext.group(2))
        countries = [which] if which != 'neighbours' else NEIGHBOURS
        paths = build_paths(countries, lon0, lat0, lon1, lat1, cx, cy)
        geom = ('<a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/>'
                '<a:rect l="0" t="0" r="r" b="b"/><a:pathLst>%s</a:pathLst></a:custGeom>' % paths)
        sp2 = re.sub(r'<a:prstGeom prst="rect">.*?</a:prstGeom>', geom, sp, count=1, flags=re.S)
        if sp2 == sp:
            sp2 = re.sub(r'<a:prstGeom[^>]*/>', geom, sp, count=1)
        # rename so the shape reads well in the selection pane
        sp2 = sp2.replace(nm.group(1), 'Map - ' + ('Indonesia' if which == 'Indonesia' else 'Neighbouring countries'))
        return sp2
    return SP_RE.sub(repl, xml)

def main(src, dst):
    zin = zipfile.ZipFile(src)
    zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    n = 0
    for item in zin.infolist():
        data = zin.read(item.filename)
        if re.match(r'ppt/slides/slide\d+\.xml$', item.filename):
            xml = data.decode('utf-8')
            new = process_slide(xml)
            if new != xml:
                n += 1
            data = new.encode('utf-8')
        zout.writestr(item, data)
    zout.close()
    print('map shapes injected on %d slide(s) -> %s' % (n, dst))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
