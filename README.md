<a href="https://jibancat.github.io">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./img/ink/banner-dark.svg">
    <img alt="Ming-Feng Ho 何銘峰. A simulated Lyman-alpha forest field from PRIYA, drawn in ink; a light reads one sightline at a time and its spectrum rises behind it." src="./img/ink/banner-light.svg" width="100%">
  </picture>
</a>

<p align="center"><sub>
<a href="https://jibancat.github.io/#research">research</a> &nbsp;·&nbsp;
<a href="https://jibancat.github.io/#projects">projects</a> &nbsp;·&nbsp;
<a href="https://jibancat.github.io/talks/">talks</a> &nbsp;·&nbsp;
<a href="https://jibancat.github.io/#papers">papers</a> &nbsp;·&nbsp;
<a href="https://jibancat.github.io/cv/">cv</a>
</sub></p>

### Hi there, I am Ming-Feng ([Jibancat][website]) 👋

### I'm an astronomer, simulator, and data scientist

- 🔭 I'm a postdoc at the University of Michigan, working on the Lyα forest, dense absorbers, and the inference problems that come with them. Check out my personal website: [jibancat.github.io][website]!
- 🎤 New: my public talk, [*The Lyman-alpha Forest: Reading the Universe and Galaxies in Shadows*][talk], is built as a live web page you can click through.
- 🌱 I’m currently learning psychology and what is Taiwan/Taiwanese!
- 🧋 My past works include a machine learning pipeline for finding DLAs ([gp_dla_finder](https://github.com/jibanCat/gp_dla_finder), now one of the finders behind the DESI DR2 DLA catalogue), multi-fidelity emulators for cosmological simulations ([matter_multi_fidelity_emu](https://github.com/jibanCat/matter_multi_fidelity_emu), [matter_emu_mfbox](https://github.com/jibanCat/matter_emu_mfbox)), and an automated tool for quasar redshift estimation ([gp_qso_redshift](https://github.com/sbird/gp_qso_redshift)).
- 🥅 ~2025 Goals: Learn more about self-supervised learning and find a job~ 2026 Goals: Learn to use Claude and let the agents do works for me (躺平)
- ⚡ Fun fact: I love to play Elden Ring and cello. And before pursuing my astronomy PhD, I loved writing literature and (briefly) worked in the fascinating field of digital humanities!

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./img/ink/sightline-dark.svg">
  <img alt="" src="./img/ink/sightline-light.svg" width="100%">
</picture>

<sub>01 · RESEARCH</sub>

### From quasar light to small-scale structure

Light from a distant quasar crosses the cosmic web before it reaches us. Diffuse hydrogen along its filaments absorbs that light at different wavelengths, and together those absorption features form the Lyα forest. The forest probes very small scales, and the dense absorbers inside it (DLAs) leave their own mark on the same statistics, so their population enters the cosmological likelihood too.

`light → forest → sightlines → statistics → matter power`

<sub>02 · SELECTED WORK</sub>

### Small-scale Lyα cosmology with high-resolution spectra
<sub>JCAP 2026 · small-scale cosmology</sub>

<a href="https://arxiv.org/abs/2509.18271"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/figures/fig-lya-cosmo-dark.webp"><img alt="A sightline read from the PRIYA field: the transmission of one row rises above the simulated plane as an ink silhouette." src="./img/ink/figures/fig-lya-cosmo-light.webp" width="100%"></picture></a>
<p><sub><i>a sightline read from the field · simulated · PRIYA</i></sub></p>

High-resolution quasar spectra resolve the Lyα forest out to wavenumbers of order k ~ 10 h Mpc⁻¹. Using KODIAQ-SQUAD and XQ-100, we constrain the amplitude and slope of the small-scale matter power spectrum.<br>
[arXiv:2509.18271](https://arxiv.org/abs/2509.18271) · [JCAP 07 (2026) 094](https://doi.org/10.1088/1475-7516/2026/07/094)

### Finding damped absorbers automatically
<sub>2020 → DESI · absorbers · inference</sub>

<a href="https://github.com/jibanCat/gp_dla_finder"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/figures/fig-dla-finder-dark.webp"><img alt="How the DLA finder works: an inferred unabsorbed quasar spectrum over a synthetic absorbed spectrum, with the damped absorber marked in rust." src="./img/ink/figures/fig-dla-finder-light.webp" width="100%"></picture></a>
<p><sub><i>how it works · synthetic · illustrative</i></sub></p>

Rather than a yes-or-no detection, the finder keeps a posterior over each absorber's redshift and column density. It is now one of the complementary finders used for the DESI DR2 DLA catalogue.<br>
[DR12](https://arxiv.org/abs/2003.11036) · [DR16Q](https://arxiv.org/abs/2103.10964) · [DESI DR2](https://arxiv.org/abs/2503.14740) · [code](https://github.com/jibanCat/gp_dla_finder)

### Multi-fidelity emulation
<sub>2022 – 2023 · emulation · uncertainty</sub>

<a href="https://arxiv.org/abs/2306.03144"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/figures/fig-mf-emu-dark.webp"><img alt="One sightline, resolution rising from low resolution on the left to full detail on the right." src="./img/ink/figures/fig-mf-emu-light.webp" width="100%"></picture></a>
<p><sub><i>one sightline, resolution rising · simulated · PRIYA</i></sub></p>

High-resolution simulations are expensive, so there are never enough of them. Multi-fidelity emulation combines many low-resolution runs with a few high-resolution ones and learns the correction between them.<br>
[MF emulator](https://arxiv.org/abs/2105.01081) · [MF-Box](https://arxiv.org/abs/2306.03144) · [forest](https://arxiv.org/abs/2207.06445) · [code](https://github.com/jibanCat/matter_emu_mfbox) · [watch the method ▶](https://www.youtube.com/watch?v=tQIytDnWOzk)

### One population of black holes, or two?
<sub>PRD 2024 · population inference</sub>

<a href="https://arxiv.org/abs/2408.09024"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/figures/fig-bh-pop-dark.webp"><img alt="One population, or two?" src="./img/ink/figures/fig-bh-pop-light.webp" width="100%"></picture></a>

Hierarchical population inference on GWTC-3: how much could two proposed black-hole populations mix?<br>
[arXiv:2408.09024](https://arxiv.org/abs/2408.09024) · [PRD 110, 063031](https://doi.org/10.1103/PhysRevD.110.063031)

<sub>Full list on <a href="https://jibancat.github.io/#papers">my website</a> and <a href="https://scholar.google.com/citations?user=gF5V0LUAAAAJ&hl=en">Google Scholar</a>.</sub>

<sub>03 · TALKS</sub>

### 🎤 The Lyman-alpha Forest

<a href="https://jibancat.github.io/talks/lya/"><img alt="The Lyman-alpha Forest: Reading the Universe and Galaxies in Shadows. A public talk, built as a live web page." src="./img/ink/talk-card.svg" width="100%"></a>

A 20-minute public talk that reads quasar light through one simulated universe, [built as a live web page][talk] (arrow keys or space to go on; best on a laptop).

- 🎬 Videos: [watch the render](https://www.youtube.com/watch?v=4ccwRtn-NTQ) · [watch the method](https://www.youtube.com/watch?v=tQIytDnWOzk) · [a PRIYA sightline, full resolution](https://youtu.be/xBZLH14Qzyo)

<details>
<summary><sub>🗂️ older figures (2023)</sub></summary>
<br>

**PRIYA**: a new suite of Lyman-alpha forest simulations for cosmology [(arXiv:2306.05471)](https://arxiv.org/abs/2306.05471), and the companion paper using PRIYA for inference [(arXiv:2309.03943)](https://arxiv.org/abs/2309.03943)

<img alt="A sightline crossing a PRIYA simulation, with its HI absorption spectrum below" src="./img/old/priya-sightline.gif" width="100%">

**MF-Box**: multi-fidelity and multi-scale emulation for the matter power spectrum [(arXiv:2306.03144)](https://arxiv.org/abs/2306.03144)

<img alt="Illustration of multi-fidelity multi-scale emulation" src="./img/old/mf-box-illustration.png" width="100%">

**DLAs** from SDSS DR16Q with Gaussian processes [(arXiv:2103.10964)](https://arxiv.org/abs/2103.10964)

<img alt="Quasar spectra with Gaussian process continuum models" src="./img/old/dla-gp-spectra.jpg" width="100%">

</details>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./img/ink/sightline-dark.svg">
  <img alt="" src="./img/ink/sightline-light.svg" width="100%">
</picture>

### Connect with me:

<a href="https://jibancat.github.io"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/website-dark.svg"><img alt="website" title="website" src="./img/ink/icons/website-light.svg" width="44"></picture></a> <a href="https://jibancat.github.io/cv/"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/cv-dark.svg"><img alt="CV" title="CV" src="./img/ink/icons/cv-light.svg" width="44"></picture></a> <a href="https://scholar.google.com/citations?user=gF5V0LUAAAAJ&hl=en"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/scholar-dark.svg"><img alt="Google Scholar" title="Google Scholar" src="./img/ink/icons/scholar-light.svg" width="44"></picture></a> <a href="https://orcid.org/0000-0002-4457-890X"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/orcid-dark.svg"><img alt="ORCID" title="ORCID" src="./img/ink/icons/orcid-light.svg" width="44"></picture></a> <a href="mailto:mfho@umich.edu"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/email-dark.svg"><img alt="email" title="email" src="./img/ink/icons/email-light.svg" width="44"></picture></a> <a href="https://www.linkedin.com/in/ming-feng-ho-a20431121"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/linkedin-dark.svg"><img alt="LinkedIn" title="LinkedIn" src="./img/ink/icons/linkedin-light.svg" width="44"></picture></a> <a href="https://www.youtube.com/channel/UCTVjf6TgaA5LzXBtXAfAD2A"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/youtube-dark.svg"><img alt="YouTube" title="YouTube" src="./img/ink/icons/youtube-light.svg" width="44"></picture></a> <a href="https://www.instagram.com/jibancat/"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/instagram-dark.svg"><img alt="Instagram" title="Instagram" src="./img/ink/icons/instagram-light.svg" width="44"></picture></a> <a href="https://www.researchgate.net/profile/Ming-Feng-Ho"><picture><source media="(prefers-color-scheme: dark)" srcset="./img/ink/icons/researchgate-dark.svg"><img alt="ResearchGate" title="ResearchGate" src="./img/ink/icons/researchgate-light.svg" width="44"></picture></a>

<sub>Banner and figures are drawn from the PRIYA simulations (<a href="https://arxiv.org/abs/2306.05471">Bird et al. 2023</a>), via the public field on <a href="https://jibancat.github.io">jibancat.github.io</a>, by the scripts in <a href="./tools">tools/</a>.</sub>

[website]: https://jibancat.github.io
[talk]: https://jibancat.github.io/talks/lya/
