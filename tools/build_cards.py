#!/usr/bin/env python3
"""Two small pieces for the README:

  talk-card.svg            the Lyα talk as a slide: dark pool, a far lamp, and its light as a strip whose
                           blue half carries the forest (the site's hero row, resampled)
  sightline-{light,dark}   a divider: the site's named DLA row as a low ink ridge, rust in the saturated run

    python3 tools/build_cards.py"""
import os

import numpy as np

from inklib import DARK, LIGHT, REPO, fmt, load_field, saturated_runs, text_path

OUT = os.path.join(REPO, 'img', 'ink')


def talk_card(F):
    W, H = 1600, 400
    bg, cream, muted, dim = '#0B1119', '#E6E2D8', '#8C94A0', '#6B778A'
    x0, x1, ys, sh = 760, 1480, 236, 14          # the strip
    row = F[239]
    n = 360                                      # forest columns across the blue part of the strip
    xf = np.linspace(0, len(row) - 1, n)
    fr = np.interp(xf, np.arange(len(row)), row)
    blue_w = (x1 - x0) * 0.62
    bars = []
    for k, f in enumerate(fr):
        a = (1 - f) ** 1.3
        if a > 0.06:
            bars.append('<rect x="%s" y="%d" width="%s" height="%d" fill="%s" fill-opacity="%.2f"/>' % (
                fmt(x0 + k * blue_w / n), ys, fmt(blue_w / n + 0.4), sh, bg, min(0.95, a)))
    title, _ = text_path('The Lyman-alpha Forest', 72, 292, 62, 'serif')
    sub, _ = text_path('Reading the Universe and Galaxies in Shadows', 75, 336, 25, 'sans')
    lab, _ = text_path('A PUBLIC TALK, BUILT AS A LIVE WEB PAGE', 75, 84, 17, 'mono', tracking=2.2)
    go, _ = text_path('start the talk  →', W - 72, 336, 24, 'sans', anchor='end')
    note, _ = text_path('simulated universe', W - 72, 84, 19, 'sans', anchor='end')
    lx, ly = x1 - 60, 150
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">The Lyman-alpha Forest: Reading the Universe and Galaxies in Shadows (a public talk)</title>
<defs>
<linearGradient id="light" x1="0" x2="1"><stop offset="0" stop-color="#6D7C9C"/><stop offset="0.45" stop-color="#9DB0B0"/><stop offset="0.7" stop-color="#E6DDBF"/><stop offset="1" stop-color="#D6A55A"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#F3EEDD" stop-opacity="0.55"/><stop offset="1" stop-color="#F3EEDD" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="{bg}"/>
<circle cx="{lx}" cy="{ly}" r="46" fill="url(#glow)"><animate attributeName="opacity" values="0.55;1;0.55" dur="5s" repeatCount="indefinite"/></circle>
<circle cx="{lx}" cy="{ly}" r="5.5" fill="#F6F2E6"/>
<rect x="{x0}" y="{ys}" width="{x1 - x0}" height="{sh}" fill="url(#light)"/>
{''.join(bars)}
<path d="{title}" fill="{cream}"/>
<g fill="{muted}"><path d="{sub}"/><path d="{go}"/></g>
<g fill="{dim}"><path d="{lab}"/><path d="{note}"/></g>
</svg>
'''
    open(os.path.join(OUT, 'talk-card.svg'), 'w', encoding='utf-8').write(svg)


def divider(F, pal, tag):
    W, H, RH, base = 1600, 64, 40, 50
    row = F[341]
    nx = len(row)
    pts = ' L'.join('%s,%s' % (fmt((c + 0.5) * W / nx), fmt(base - RH * row[c])) for c in range(0, nx, 2))
    runs = saturated_runs(row)
    ink = pal['graphite'] if pal is LIGHT else '#8D9CAE'
    rust = ''.join('<rect x="%s" y="%d" width="%s" height="3" fill="%s"/>' % (
        fmt((s + 0.5) * W / nx), base + 2, fmt((e - s) * W / nx), pal['rust']) for s, e in runs)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="one sightline">
<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{ink}" stop-opacity="0"/><stop offset="0.12" stop-color="{ink}" stop-opacity="1"/><stop offset="0.88" stop-color="{ink}" stop-opacity="1"/><stop offset="1" stop-color="{ink}" stop-opacity="0"/></linearGradient></defs>
<path d="M0,{base} L{pts} L{W},{base} Z" fill="url(#fade)" fill-opacity="{0.8 if pal is LIGHT else 0.55}"/>
<rect x="0" y="{base}" width="{W}" height="1.2" fill="url(#fade)"/>
{rust}
</svg>
'''
    open(os.path.join(OUT, 'sightline-%s.svg' % tag), 'w', encoding='utf-8').write(svg)


if __name__ == '__main__':
    F, _ = load_field()
    talk_card(F)
    divider(F, LIGHT, 'light')
    divider(F, DARK, 'dark')
    for f in ('talk-card.svg', 'sightline-light.svg', 'sightline-dark.svg'):
        print('img/ink/%s  %.0f KB' % (f, os.path.getsize(os.path.join(OUT, f)) / 1024))
