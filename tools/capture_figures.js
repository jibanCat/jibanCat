// Project figures for the README, drawn by the site's own renderer (js/figures.js).
// Open jibancat.github.io (or a local copy) in a browser with devicePixelRatio 2, paste this into the
// console, and it downloads fig-*-light.png and fig-*-dark.png. Convert with, e.g.
//   for f in fig-*.png; do cwebp -q 86 -m 6 -sharp_yuv "$f" -o "img/ink/figures/${f%.png}.webp"; done
(async () => {
  const SPECS = [
    { name: 'fig-lya-cosmo', ds: { fig: 'field', box: '120,400,120,1300', sil: '239' }, w: 830, h: 420 },
    { name: 'fig-dla-finder', ds: { fig: 'gp' }, w: 830, h: 300 },
    { name: 'fig-mf-emu', ds: { fig: 'fidelity', row: '239', c0: '380', c1: '900' }, w: 830, h: 300 },
    { name: 'fig-bh-pop', ds: { fig: 'ask', ask: 'One population, or two?' }, w: 830, h: 200 },
  ];
  // dark: the same print as a rubbing, matching tools/inklib.py DARK
  const DARK = { '--paper': '#0E141C', '--paper-2': '#121923', '--mist': '#1A2330', '--wash': '#5A6A80', '--ink': '#C9D4E0',
    '--pool': '#EEF1F4', '--muted': '#8C94A0', '--faint': '#3A4350', '--hair': '#26303C', '--rust': '#D2553A',
    '--ref': '#8A97A4', '--light': '#DCEBF6' };

  const host = document.createElement('div');
  host.style.cssText = 'position:absolute;left:0;top:0;z-index:9999';
  document.body.appendChild(host);
  const canvases = SPECS.map(s => {
    const c = document.createElement('canvas');
    Object.assign(c.dataset, s.ds);
    c.style.cssText = `display:block;width:${s.w}px;height:${s.h}px`;
    host.appendChild(c);
    return c;
  });
  const only = keep => document.querySelectorAll('canvas[data-fig]').forEach(c => {
    if (!keep.includes(c)) { c.dataset.figOff = c.dataset.fig; delete c.dataset.fig; }
  });
  const restore = () => document.querySelectorAll('canvas[data-fig-off]').forEach(c => {
    c.dataset.fig = c.dataset.figOff; delete c.dataset.figOff;
  });
  const save = async (c, file) => {
    const url = URL.createObjectURL(await new Promise(r => c.toBlob(r, 'image/png')));
    Object.assign(document.createElement('a'), { href: url, download: file }).click();
    await new Promise(r => setTimeout(r, 400));
  };
  const draw = list => { only(list); window.__figures.drawAll(); restore(); };

  draw(canvases);
  for (let i = 0; i < SPECS.length; i++) await save(canvases[i], SPECS[i].name + '-light.png');

  // colours the renderer writes literally rather than through CSS variables; `ridge` turns the lifted
  // silhouette into a dark ridge with a lit crest, like the banner's dark variant
  let ridge = false;
  const map = s => {
    if (typeof s !== 'string') return s;
    const t = s.trim().toUpperCase();
    if (ridge && t === '#EEF1F4') return '#05080C';
    if (ridge && t === '#C9D4E0') return '#131B26';
    if (ridge && /rgba\(244,\s*242,\s*237,\s*0\.9\)/.test(s)) return 'rgba(220,235,246,0.9)';
    return s.replace(/rgba\(244,\s*242,\s*237/g, 'rgba(14,20,28').replace(/rgba\(185,\s*58,\s*32/g, 'rgba(210,85,58');
  };
  const P = CanvasRenderingContext2D.prototype;
  for (const k of ['fillStyle', 'strokeStyle']) {
    const d = Object.getOwnPropertyDescriptor(P, k);
    Object.defineProperty(P, k, { set(v) { d.set.call(this, map(v)); }, get() { return d.get.call(this); }, configurable: true });
  }
  const addStop = CanvasGradient.prototype.addColorStop;
  CanvasGradient.prototype.addColorStop = function (o, c) { return addStop.call(this, o, map(c)); };
  for (const [k, v] of Object.entries(DARK)) document.documentElement.style.setProperty(k, v);

  draw(canvases.slice(1));
  ridge = true; draw(canvases.slice(0, 1)); ridge = false;
  for (let i = 0; i < SPECS.length; i++) await save(canvases[i], SPECS[i].name + '-dark.png');
  console.log('done: reload the page to restore it');
})();
