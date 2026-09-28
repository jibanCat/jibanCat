#!/usr/bin/env python3
"""The README banner: the site's hero field in ink (a port of the "sumi" treatment in
js/hero/field-gl.js, at rest), with sightlines read across it the way the hero reads them.

    python3 tools/build_banner.py        # writes img/ink/banner-light.svg and banner-dark.svg

Each row of the field is one PRIYA sightline; the ridge that rises behind the probe is that row's
transmission. The second row read is the DLA row the site names (341)."""
import base64
import io
import os

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates

from inklib import DARK, LIGHT, REPO, fmt, load_field, rgb, saturated_runs, text_path

W, FH = 1600, 380                  # banner width; field height (viewBox units = raster pixels)
H = 560                            # full banner, with the paper band under the field
R0, R1 = 40, 420                   # field rows shown
ROWS = [239, 341]                  # the site's hero row, then its named DLA row
RIDGE, LIFT, STRIP = 112, 12, 9   # ridge height, lift of the strip above the row, strip thickness
DUR = 24.0                         # one full cycle, seconds
OUT = os.path.join(REPO, 'img', 'ink')


# ------------------------------------------------------------------ field (port of the sumi shader at rest)
def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def mix(a, b, t):
    t = np.asarray(t)[..., None] if np.ndim(t) else t
    return a + (b - a) * t


def hash2(x, y):
    v = np.sin(x * 127.1 + y * 311.7) * 43758.5453
    return v - np.floor(v)


def noise(x, y):
    ix, iy = np.floor(x), np.floor(y)
    fx, fy = x - ix, y - iy
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = hash2(ix, iy), hash2(ix + 1, iy)
    c, d = hash2(ix, iy + 1), hash2(ix + 1, iy + 1)
    return (a + (b - a) * fx) + ((c + (d - c) * fx) - (a + (b - a) * fx)) * fy


def fbm(x, y):
    v, a = 0.0, 0.5
    for _ in range(4):
        v = v + a * noise(x, y)
        x, y, a = x * 2.03, y * 2.03, a * 0.5
    return v


def pigment_maps(F):
    tau = -np.log(np.maximum(F, 1e-6))
    lt = np.clip((np.log10(tau + 1e-3) + 3) / 8, 0, 1)
    p = smoothstep(0.2375, 0.5625, lt)
    g = lambda sy, sx: gaussian_filter(p, (sy, sx), mode='nearest', truncate=3.0)
    pM, pL, pX = g(1.3, 1.3), g(5.0, 5.0), g(0.6, 14.0)
    pXL = np.minimum(1, g(14.0, 14.0) * 1.6)
    gy, gx = np.gradient(pM)
    edge = np.minimum(1, np.hypot(2 * gx, 2 * gy) * 2.5)
    return dict(lt=lt, pM=pM, pL=pL, pX=pX, pXL=pXL, edge=edge)


def render_field(maps, pal, w=W, h=FH):
    ny = R1 - R0
    nx = maps['lt'].shape[1]
    fy, fx = np.mgrid[0:h, 0:w].astype(np.float64) + 0.5
    ty = R0 + fy / h * ny - 0.5                          # texel coordinates, GL-style linear sampling
    tx = fx / w * nx - 0.5
    S = {k: map_coordinates(v, [ty, tx], order=1, mode='nearest') for k, v in maps.items()}
    P = {k: rgb(pal[k]) for k in ('paper', 'mist', 'wash', 'ink', 'pool', 'rust')}

    fibre = fbm(fx * 0.05, fy * 0.8) - 0.5
    speck = noise(fx * 1.7, fy * 1.7) - 0.5
    ex, ey = np.abs(fx / w - 0.5) * 2, np.abs(fy / h - 0.5) * 2
    plate = 1 - 0.035 * smoothstep(0.6, 1.2, np.hypot(ex, ey))
    paper = P['paper'] * (plate * (1 + fibre * 0.03 + speck * 0.035))[..., None]

    p = smoothstep(0.2375, 0.5625, S['lt'])
    pM, pL, pX, pXL, edge = S['pM'], S['pL'], S['pX'], S['pXL'], S['edge']
    pFine = pM + (p - pM) * 0.18
    gran = (noise(fx * 0.9, fy * 0.9) - 0.5) * 0.35 * smoothstep(0.5, 1.0, pM)
    thin = smoothstep(0.12, 0.45, p - 1.5 * pL)
    dry = 0.35 + 0.65 * noise(fx * 0.28, fy * 2.6)
    brush = 1 + (dry - 1) * thin

    c = mix(paper, P['mist'], (1 - smoothstep(0.0, 0.30, pL)) * 0.42)
    c = mix(c, P['wash'] * 0.92 if pal is LIGHT else P['wash'], 0.34 * smoothstep(0.03, 0.34, pXL))
    c = mix(c, P['wash'], 0.22 * smoothstep(0.04, 0.55, pX))
    c = mix(c, P['wash'], 0.80 * smoothstep(0.02, 0.42, pL))
    c = mix(c, P['ink'], 0.72 * smoothstep(0.20, 0.72, pM) * brush * (0.72 + 0.28 * smoothstep(0.02, 0.22, pXL)))
    poolA = smoothstep(0.42, 0.9, pFine + gran) * brush
    rim = smoothstep(0.08, 0.35, edge) * smoothstep(0.25, 0.6, pM) * (1 - smoothstep(0.6, 0.95, pM)) * 0.5
    poolC = mix(np.broadcast_to(P['ink'], c.shape), P['pool'], smoothstep(0.6, 1.0, pFine))
    c = c + (poolC - c) * np.clip(poolA + rim, 0, 1)[..., None]
    deposit = smoothstep(0.55, 0.95, pL) * (1 - smoothstep(0.5, 0.9, pFine)) * 0.45
    c = mix(c, P['rust'] * 0.85, deposit)
    return (np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8)


def data_uri(img, fmt_='JPEG', **kw):
    buf = io.BytesIO()
    img.save(buf, fmt_, **kw)
    mime = 'jpeg' if fmt_ == 'JPEG' else fmt_.lower()
    return 'data:image/%s;base64,%s' % (mime, base64.b64encode(buf.getvalue()).decode())


# ------------------------------------------------------------------ sightlines
def row_y(r):
    return (r - R0 + 0.5) * FH / (R1 - R0)


def col_x(c, nx):
    return (c + 0.5) * W / nx


def ridge_path(row, y0):
    nx = len(row)
    base = y0 - LIFT - STRIP
    pts = ['%s,%s' % (fmt(col_x(c, nx)), fmt(base - RIDGE * row[c])) for c in range(nx)]
    return 'M0,%s L%s L%d,%s Z' % (fmt(base), ' '.join(pts), W, fmt(base)), 'M' + ' L'.join(pts)


def strip_uri(row, runs, pal):
    """The row's own pixels, paper to ink by transmission, rust where saturated (the site's strip)."""
    paper, ink, rust = rgb(pal['paper']), rgb(pal['graphite'] if pal is LIGHT else pal['ink']), rgb(pal['rust'])
    a = np.clip((1 - row) ** 1.25 * 1.05, 0, 1)[:, None]
    px = paper + (ink - paper) * a
    for s, e in runs:
        px[s:e] = rust
    img = Image.fromarray((px[None] * 255 + 0.5).astype(np.uint8), 'RGB')
    return data_uri(img, 'PNG', optimize=True)


def kt(*pairs):
    """SMIL values/keyTimes from (time_seconds, value) pairs over one cycle."""
    return ';'.join(str(v) for _, v in pairs), ';'.join('%.4f' % min(1.0, t / DUR) for t, _ in pairs)


def anim(attr, pairs, spline=True, extra=''):
    vals, times = kt(*pairs)
    n = len(pairs) - 1
    sp = ''
    if spline:
        sp = ' calcMode="spline" keySplines="%s"' % ';'.join(['0.45 0 0.55 1'] * n)
    return '<animate attributeName="%s" values="%s" keyTimes="%s" dur="%ss" repeatCount="indefinite"%s%s/>' % (
        attr, vals, times, fmt(DUR), sp, extra)


def anim_x(pairs):
    """Probe travel: piecewise, linear in the middle so the light moves at a steady pace."""
    vals = ';'.join('%s 0' % fmt(v) for _, v in pairs)
    times = ';'.join('%.4f' % min(1.0, t / DUR) for t, _ in pairs)
    n = len(pairs) - 1
    splines = ['0 0 1 1'] * n
    return ('<animateTransform attributeName="transform" type="translate" values="%s" keyTimes="%s" dur="%ss" '
            'repeatCount="indefinite" calcMode="spline" keySplines="%s"/>' % (vals, times, fmt(DUR), ';'.join(splines)))


def sightline(i, r, row, pal, t0):
    """One read: hairline → probe crosses (steady; slower through a saturated run) → hold → fade."""
    nx = len(row)
    y0 = row_y(r)
    runs = saturated_runs(row)
    fill_d, edge_d = ridge_path(row, y0)
    SPEED = W / 6.2                                       # px per second
    LABOUR = 1.4                                          # extra seconds inside a saturated run
    # probe x(t) keyframes
    t, x = t0 + 0.6, -40.0
    keys = [(0, x), (t, x)]
    for s, e in runs:
        xs, xe = col_x(s, nx), col_x(e, nx)
        t += (xs - x) / SPEED
        keys.append((t, xs))
        t += (xe - xs) / SPEED + LABOUR
        keys.append((t, xe))
        x = xe
    t += (W + 60 - x) / SPEED
    t_end = t
    keys += [(t_end, W + 60), (DUR, W + 60)]
    t_hold, t_fade = t_end + 2.2, t_end + 3.2

    soft = 90                                             # the soft leading edge of the reveal
    mask_keys = [(tt, xx - W - 20) for tt, xx in keys]    # mask rect spans [-W-20-soft .. 0] + offset

    g = ['<g opacity="0">',
         anim('opacity', [(0, 0), (t0, 0), (t0 + 0.5, 1), (t_hold, 1), (t_fade, 0), (DUR, 0)]),
         '<mask id="m%d" maskUnits="userSpaceOnUse" x="0" y="0" width="%d" height="%d">' % (i, W, FH),
         '<g>%s<rect x="%d" y="0" width="%d" height="%d" fill="url(#soft)"/></g>' % (anim_x(mask_keys), 0, W + 20, FH),
         '</mask>',
         # the row named, not yet read
         '<line x1="0" y1="%s" x2="%d" y2="%s" stroke="%s" stroke-opacity="0.45" stroke-width="1.6" stroke-dasharray="2 6"/>'
         % (fmt(y0 + 0.5), W, fmt(y0 + 0.5), pal['graphite']),
         '<g mask="url(#m%d)">' % i,
         # the cut the reading leaves, with a soft shadow beneath
         '<rect x="0" y="%s" width="%d" height="3" fill="%s"/>' % (fmt(y0 - 1.5), W, pal['cut']),
         '<rect x="0" y="%s" width="%d" height="6" fill="%s" opacity="0.10"/>' % (fmt(y0 + 1.5), W, pal['pool'] if pal is LIGHT else '#000'),
         # the strip: the row's own pixels, lifted
         '<image href="%s" x="0" y="%s" width="%d" height="%d" preserveAspectRatio="none" style="image-rendering:pixelated"/>'
         % (strip_uri(row, runs, pal), fmt(y0 - LIFT - STRIP), W, STRIP),
         '<line x1="0" y1="%s" x2="%d" y2="%s" stroke="%s" stroke-width="1.2"/>' % (fmt(y0 - LIFT + 0.5), W, fmt(y0 - LIFT + 0.5), pal['graphite']),
         # the silhouette: transmission along the row
         '<path d="%s" fill="url(#ridge%d)"/>' % (fill_d, i),
         '<path d="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="2" stroke-linejoin="round"/>'
         % (edge_d, pal['ridge_edge'], pal['ridge_edge_a']),
         '</g>']
    for s, e in runs:                                     # a dense absorber: bloom, then a rust stain and a name
        xs, xe = col_x(s, nx), col_x(e, nx)
        xm = (xs + xe) / 2
        t_in = next(tt for tt, xx in keys if xx >= xs)
        t_out = next(tt for tt, xx in keys if xx >= xe)
        g.append('<ellipse cx="%s" cy="%s" rx="%s" ry="70" fill="url(#bloom)" opacity="0">%s</ellipse>' % (
            fmt(xm), fmt(y0), fmt((xe - xs) / 2 + 120),
            anim('opacity', [(0, 0), (t_in - 0.2, 0), (t_out, 0.85), (t_out + 1.2, 0.45), (t_hold, 0.45), (t_fade, 0), (DUR, 0)])))
        label = 'DLA' if r == 341 else 'dense absorber'
        d, _ = text_path(label, xm, y0 - LIFT - STRIP - 16, 22, 'sans', tracking=3, anchor='middle')
        d2, _ = text_path('log N(HI) = %.2f' % 20.671642785549373, xm, y0 + 40, 19, 'mono', anchor='middle')
        g.append('<g fill="%s" stroke="%s" stroke-opacity="0.8" stroke-width="7" stroke-linejoin="round" paint-order="stroke" '
                 'opacity="0">%s<path d="%s"/><path d="%s"/></g>' % (
            pal['rust'], pal['paper'], anim('opacity', [(0, 0), (t_out + 0.3, 0), (t_out + 1.3, 1), (t_hold, 1), (t_fade, 0), (DUR, 0)]), d, d2))
    # the probe: a small cool light with a fine vertical beam through the row
    g += ['<g opacity="0">',
          anim('opacity', [(0, 0), (t0 + 0.6, 0), (t0 + 0.9, 1), (t_end - 0.4, 1), (t_end, 0), (DUR, 0)]),
          '<g>' + anim_x(keys),
          '<line x1="0" y1="%s" x2="0" y2="%s" stroke="%s" stroke-opacity="0.9" stroke-width="1.8"/>' % (
              fmt(y0 - LIFT - STRIP - RIDGE - 14), fmt(y0 + 22), pal['beam']),
          '<circle cx="0" cy="%s" r="13" fill="%s" fill-opacity="0.55"/>' % (fmt(y0), pal['glow']),
          '<circle cx="0" cy="%s" r="6.4" fill="%s"/>' % (fmt(y0), pal['probe_core']),
          '<circle cx="0" cy="%s" r="2.5" fill="%s"/>' % (fmt(y0), pal['probe_dot']),
          '</g></g>']
    g.append('</g>')
    grad = ('<linearGradient id="ridge%d" gradientUnits="userSpaceOnUse" x1="0" y1="%s" x2="0" y2="%s">'
            '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
            '</linearGradient>' % (i, fmt(y0 - LIFT - STRIP), fmt(y0 - LIFT - STRIP - RIDGE), *pal['ridge']))
    return grad, '\n'.join(g), t_fade


def banner(maps, F, pal, name):
    field = Image.fromarray(render_field(maps, pal), 'RGB')
    field_uri = data_uri(field, 'WEBP', quality=88, method=6)

    defs, groups, t = [], [], 0.4
    for i, r in enumerate(ROWS):
        grad, g, t_fade = sightline(i, r, F[r], pal, t)
        defs.append(grad)
        groups.append(g)
        t = t_fade + 0.6
    assert t <= DUR + 0.6, 'cycle too short: %.1f s' % t

    ink, muted = pal['text'], pal['muted']
    cap, _ = text_path('each row is a sightline through simulated hydrogen  ·  Lyα forest at z = 3  ·  PRIYA', 56, FH + 38, 21, 'sans')
    nm, wn = text_path('Ming-Feng Ho', 54, H - 66, 74, 'serif')
    han, _ = text_path('何銘峰', 54 + wn + 26, H - 66, 60, 'han')
    tag, _ = text_path('Lyα forest · dense absorbers · inference', 58, H - 22, 25, 'sans')
    url, _ = text_path('jibancat.github.io  ↗', W - 56, H - 66, 24, 'sans', anchor='end')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">
<title id="title">Ming-Feng Ho 何銘峰</title>
<desc id="desc">A simulated Lyman-alpha forest field from the PRIYA simulations, drawn in ink. A light reads one sightline at a time across it, and the absorption spectrum of that sightline rises behind it as an ink ridge; the second sightline crosses a damped Lyman-alpha absorber.</desc>
<defs>
<linearGradient id="soft" gradientUnits="objectBoundingBox" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="{1 - 90 / (W + 20):.4f}" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<radialGradient id="bloom"><stop offset="0" stop-color="{pal['rust']}" stop-opacity="0.55"/><stop offset="1" stop-color="{pal['rust']}" stop-opacity="0"/></radialGradient>
{chr(10).join(defs)}
</defs>
<rect width="{W}" height="{H}" fill="{pal['paper']}"/>
<image href="{field_uri}" x="0" y="0" width="{W}" height="{FH}" preserveAspectRatio="none"/>
{chr(10).join(groups)}
<g fill="{muted}"><path d="{cap}"/><path d="{tag}"/><path d="{url}"/></g>
<g fill="{ink}"><path d="{nm}"/><path d="{han}"/></g>
</svg>
'''
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'banner-%s.svg' % name)
    open(path, 'w', encoding='utf-8').write(svg)
    if os.environ.get('INK_DEBUG'):
        field.save(os.path.join(os.environ['INK_DEBUG'], 'field-%s.png' % name))
    print('%s  %.0f KB' % (os.path.relpath(path, REPO), os.path.getsize(path) / 1024))


if __name__ == '__main__':
    F, meta = load_field()
    maps = pigment_maps(F)
    banner(maps, F, LIGHT, 'light')
    banner(maps, F, DARK, 'dark')
