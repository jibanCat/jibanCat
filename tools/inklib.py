"""Shared pieces for the README's ink assets: the public PRIYA field, the site's palettes and fonts,
and text set as SVG paths (GitHub serves SVGs as images, so no web fonts reach them).

Everything is read from the public site (jibancat.github.io): a local checkout next to this repo if
there is one, otherwise the live files, cached under tools/.cache/."""
import json
import math
import os
import re
import urllib.request

import numpy as np
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SITE_LOCAL = os.environ.get('INK_SITE', os.path.join(os.path.dirname(REPO), 'jibanCat.github.io'))
SITE_URL = 'https://jibancat.github.io/'
CACHE = os.path.join(HERE, '.cache')


def site_file(rel):
    local = os.path.join(SITE_LOCAL, rel)
    if os.path.exists(local):
        return local
    dst = os.path.join(CACHE, rel)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        urllib.request.urlretrieve(SITE_URL + rel, dst)
    return dst


# ------------------------------------------------------------------ palettes
# light: the site's "cool contemporary ink" (css/site.css, js/hero/engine.js palette A)
# dark:  the same print as a rubbing (拓本): the ground is the talk's pool, pigment lifts toward paper
LIGHT = dict(
    paper='#F4F2ED', mist='#DDE5EE', wash='#7D8DA3', ink='#28323F', pool='#0C121B', rust='#B93A20',
    graphite='#1F2732', muted='#6F7278', faint='#C9CBCF', light='#DCEBF6',
    ridge=('#0C121B', '#1F2732', '#28323F'), ridge_edge='#F3F1EB', ridge_edge_a=0.9,
    beam='#D9E7F1', glow='#DCEBF6', probe_core='#FFFFFF', probe_dot='#1F2732',
    cut='#F4F2ED', text='#1F2732',
)
DARK = dict(
    paper='#0E141C', mist='#131A24', wash='#45556A', ink='#A6B5C6', pool='#E9ECEF', rust='#D2553A',
    graphite='#DDE5EE', muted='#8C94A0', faint='#39424E', light='#DCEBF6',
    ridge=('#05080C', '#0A0F16', '#131B26'), ridge_edge='#DCEBF6', ridge_edge_a=0.9,
    beam='#DCEBF6', glow='#DCEBF6', probe_core='#FFFFFF', probe_dot='#0E141C',
    cut='#0E141C', text='#E6EBF0',
)


def rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float64) / 255.0


# ------------------------------------------------------------------ the field
def load_field():
    s = open(site_file('data/f5-meta.js'), encoding='utf-8').read()
    meta = json.loads(s[s.index('{'):s.rindex('}') + 1])
    nx, ny = meta['nx'], meta['ny']
    F = np.fromfile(site_file('data/f5.bin'), dtype='<u2').astype(np.float64) / meta['field_scale']
    return F.reshape(ny, nx), meta


def saturated_runs(row, f_sat=0.02, min_run=50):
    """Saturated stretches on the site's criterion: transmission below 0.02 for >= 500 km/s."""
    out, run, start = [], 0, 0
    for x, v in enumerate(list(row) + [1.0]):
        if v < f_sat:
            if run == 0:
                start = x
            run += 1
        else:
            if run >= min_run:
                out.append((start, x))
            run = 0
    return out


# ------------------------------------------------------------------ text as paths
# (file, variable-axis location): the site sets both faces at weight 300; Fraunces at the optical
# size a ~40 px heading gets from font-optical-sizing: auto
FONTS = {
    'serif': ('assets/fonts/Fraunces-300-latin.woff2', {'wght': 300, 'opsz': 40}),
    'sans': ('assets/fonts/Inter-300-latin.woff2', {'wght': 300}),
    'greek': ('assets/fonts/Inter-300-greek-arrows.woff2', None),
    'han': ('assets/fonts/NotoSerifTC-300-name.woff2', None),
    'mono': ('assets/fonts/IBMPlexMono-400-latin.woff2', None),
}
_fonts = {}


def font(key):
    if key not in _fonts:
        path, axes = FONTS[key]
        t = TTFont(site_file(path))
        if axes and 'fvar' in t:
            t = instancer.instantiateVariableFont(t, axes)
        _fonts[key] = (t, t.getBestCmap(), t.getGlyphSet(), _pair_kerning(t))
    return _fonts[key]


def _pair_kerning(t):
    """First-match pair kerning (PairPos formats 1 and 2) from GPOS 'kern'; enough for display text."""
    kern = {}
    if 'GPOS' not in t:
        return kern
    gpos = t['GPOS'].table
    idx = set()
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'kern':
            idx.update(fr.Feature.LookupListIndex)
    for li in sorted(idx):
        lk = gpos.LookupList.Lookup[li]
        for st in lk.SubTable:
            if lk.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, 'LookupType', 2) != 2 and lk.LookupType not in (2, 9):
                continue
            if not hasattr(st, 'Format'):
                continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for g1, ps in zip(cov, st.PairSet):
                    for pvr in ps.PairValueRecord:
                        v = getattr(pvr.Value1, 'XAdvance', 0) if pvr.Value1 else 0
                        kern.setdefault((g1, pvr.SecondGlyph), v)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs if st.ClassDef1 else {}
                c2 = st.ClassDef2.classDefs if st.ClassDef2 else {}
                second = {}
                for g, c in c2.items():
                    second.setdefault(c, []).append(g)
                for g1 in cov:
                    rec = st.Class1Record[c1.get(g1, 0)]
                    for c, r2 in enumerate(rec.Class2Record):
                        v = getattr(r2.Value1, 'XAdvance', 0) if r2.Value1 else 0
                        if v and c in second:
                            for g2 in second[c]:
                                kern.setdefault((g1, g2), v)
    return kern


def text_path(s, x, y, size, family='sans', tracking=0.0, anchor='start'):
    """SVG path data for `s` set at baseline (x, y). Falls back per glyph: greek/arrows, then han."""
    chain = [family, 'greek', 'han', 'sans']
    runs, pen_x, prev = [], 0.0, None
    for ch in s:
        for key in chain:
            t, cmap, gs, kern = font(key)
            if ord(ch) in cmap:
                break
        else:
            raise ValueError('no glyph for %r' % ch)
        gname = cmap[ord(ch)]
        scale = size / t['head'].unitsPerEm
        if prev and prev[0] == key:
            pen_x += kern.get((prev[1], gname), 0) * scale
        runs.append((key, gname, pen_x, scale))
        pen_x += t['hmtx'][gname][0] * scale + tracking
        prev = (key, gname)
    width = pen_x - tracking
    if anchor == 'end':
        x -= width
    elif anchor == 'middle':
        x -= width / 2
    d = []
    for key, gname, gx, scale in runs:
        t, cmap, gs, kern = font(key)
        pen = SVGPathPen(gs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
        gs[gname].draw(TransformPen(pen, (scale, 0, 0, -scale, x + gx, y)))
        d.append(pen.getCommands())
    return ' '.join(p for p in d if p), width


def fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')
