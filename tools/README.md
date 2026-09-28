# tools

Scripts that draw the profile README's ink images. Everything comes from the public
[jibancat.github.io](https://jibancat.github.io): the PRIYA field (`data/f5.bin`), its metadata, and
the site's self-hosted fonts (SIL OFL). They are read from a checkout at `../jibanCat.github.io` if one
exists (override with `INK_SITE=/path`), otherwise downloaded into `tools/.cache/`.

Requires numpy, scipy, Pillow and fontTools ≥ 4.60 with brotli (`pip install "fonttools[woff]>=4.60"`).

| script | writes |
|---|---|
| `build_banner.py` | `img/ink/banner-{light,dark}.svg`: the hero field in ink (a port of the site's sumi shader), with two sightlines read across it on a 24 s SMIL loop |
| `build_cards.py` | `img/ink/talk-card.svg`, `img/ink/sightline-{light,dark}.svg` |
| `build_icons.py` | `img/ink/icons/<name>-{light,dark}.svg` |
| `capture_figures.js` | the project figures, captured in a browser from the site's own `js/figures.js` (see the header comment) |

Light is the site's palette; dark is the same print as a rubbing (拓本), on the talk's dark ground.
