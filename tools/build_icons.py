#!/usr/bin/env python3
"""Contact icons in ink: a dilute wash bleeding into the paper, the glyph laid over it with a brush.

    python3 tools/build_icons.py         # writes img/ink/icons/<name>-{light,dark}.svg

Glyphs are Feather icons (MIT) where one exists, drawn in the same 24-unit grid otherwise."""
import os

from inklib import DARK, LIGHT, REPO, text_path

OUT = os.path.join(REPO, 'img', 'ink', 'icons')

# name: (glyph markup in a 24-unit grid, filled?)
GLYPHS = {
    'website': '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>'
               '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    'cv': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>'
          '<line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
    'scholar': '<polygon points="12 3.5 23 9 12 14.5 1 9"/><path d="M5.5 11.3v5.2c0 1.6 2.9 3.2 6.5 3.2s6.5-1.6 6.5-3.2v-5.2"/>'
               '<line x1="21" y1="10" x2="21" y2="15.5"/>',
    'orcid': '<circle cx="12" cy="12" r="10"/><line x1="8.3" y1="10.2" x2="8.3" y2="17"/>'
             '<circle cx="8.3" cy="7.2" r="0.6" fill="currentColor"/><path d="M11.4 7.5v9.5h2.4a4.75 4.75 0 0 0 0-9.5z"/>',
    'email': '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    'linkedin': '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/>'
                '<rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    'youtube': '<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75'
               'a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25'
               ' 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/>',
    'instagram': '<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
                 '<line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>',
    'researchgate': None,           # set in type below
}
TITLES = {'website': 'website', 'cv': 'CV', 'scholar': 'Google Scholar', 'orcid': 'ORCID', 'email': 'email',
          'linkedin': 'LinkedIn', 'youtube': 'YouTube', 'instagram': 'Instagram', 'researchgate': 'ResearchGate'}


def icon(name, i, pal, dark):
    ink = pal['graphite']
    wash_fill = '#1A2330' if dark else pal['mist']
    rim = '#2C394A' if dark else '#C7D2DE'
    seed = 7 + 11 * i
    rot = (i * 67) % 360
    if name == 'researchgate':
        r, wr = text_path('R', 0, 0, 27, 'serif')
        g, wg = text_path('G', 0, 0, 15, 'serif')
        x0 = 32 - (wr + 0.6 + wg) / 2
        glyph_g = ('<g fill="%s" stroke="none"><path transform="translate(%.2f 41.5)" d="%s"/>'
                   '<path transform="translate(%.2f 31.5)" d="%s"/></g>' % (ink, x0, r, x0 + wr + 0.6, g))
    else:
        # the stroke twice: a dilute bleed into the paper, then the brush itself
        glyph_g = ''.join(
            '<g transform="translate(16.4 16.4) scale(1.3)" fill="none" stroke="%s" color="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round"%s>%s</g>' % (ink, ink, sw, extra, GLYPHS[name])
            for sw, extra in (('2.9', ' opacity="0.16" filter="url(#bleedline)"'), ('1.6', '')))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="{TITLES[name]}">
<title>{TITLES[name]}</title>
<defs>
<filter id="bleed" x="-25%" y="-25%" width="150%" height="150%"><feTurbulence type="fractalNoise" baseFrequency="0.055" numOctaves="3" seed="{seed}"/><feDisplacementMap in="SourceGraphic" scale="10" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation="0.5"/></filter>
<filter id="brush" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="{seed + 3}"/><feDisplacementMap in="SourceGraphic" scale="1.3" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="bleedline" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="0.7"/></filter>
<radialGradient id="wash" cx="0.45" cy="0.42" r="0.6"><stop offset="0" stop-color="{wash_fill}" stop-opacity="0.55"/><stop offset="0.78" stop-color="{wash_fill}" stop-opacity="0.95"/><stop offset="1" stop-color="{rim}" stop-opacity="1"/></radialGradient>
</defs>
<g filter="url(#bleed)" transform="rotate({rot} 32 32)"><ellipse cx="32" cy="32" rx="25" ry="23.5" fill="url(#wash)"/></g>
<g filter="url(#brush)">{glyph_g}</g>
</svg>
'''


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, name in enumerate(GLYPHS):
        for pal, tag in ((LIGHT, 'light'), (DARK, 'dark')):
            open(os.path.join(OUT, '%s-%s.svg' % (name, tag)), 'w', encoding='utf-8').write(icon(name, i, pal, pal is DARK))
    print('%d icons -> %s' % (len(GLYPHS) * 2, os.path.relpath(OUT, REPO)))
