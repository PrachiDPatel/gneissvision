# GneissVision — Petrography Reference & Teaching Notes

> Focus: igneous and metamorphic rocks, with special attention to rare earth minerals.
> This file grows as the project grows. Concepts are explained as they come up.

---

## 1. What is a thin section and why does it work?

A thin section is a slice of rock ground down to ~30 micrometers (0.03 mm) — thin enough that most minerals become **translucent**. At this thickness, the optical properties of each mineral's crystal structure interact with polarized light in characteristic, reproducible ways. The same mineral will always produce the same optical signature (with minor variation by composition and orientation), so the microscope is essentially doing chemistry without chemicals.

The standard petrographic microscope has two polarizing filters:
- **Lower polarizer (analyzer out):** light is polarized before it hits the sample — this is PPL
- **Upper polarizer (analyzer in):** a second filter at 90° is inserted above the sample — this is XPL

---

## 2. PPL vs XPL — what each image tells you

### Plane Polarized Light (PPL)
Light is polarized in one direction before reaching the mineral. You observe:

| Property | What it tells you |
|---|---|
| **Color** | Iron content, oxidation state (e.g. Fe-rich amphiboles are green-brown) |
| **Pleochroism** | Whether the mineral absorbs different wavelengths at different orientations — rotate the stage and watch the color change. Strong pleochroism = anisotropic mineral with oriented crystal bonds |
| **Cleavage** | Straight parallel cracks following crystal planes. Count the sets and measure the angle between them — this is highly diagnostic |
| **Crystal form (habit)** | Euhedral (well-formed faces), subhedral, anhedral — tells you crystallization history |
| **Alteration products** | Sericite (muscovite) on feldspars, chlorite on biotite/hornblende, serpentine on olivine |
| **Inclusions** | Zircon in biotite makes radiation halos; apatite needles in biotite are diagnostic of some igneous types |
| **Relief** | How "bumpy" the grain looks relative to mounting medium. High relief = large difference in refractive index from epoxy |

### Crossed Polarized Light (XPL)
The second polarizer blocks all light *except* what the mineral has rotated. Isotropic minerals (cubic crystal system, glass) go **completely black** (extinct). Everything else shows **interference colors**.

| Property | What it tells you |
|---|---|
| **Interference color** | Determined by birefringence × thickness. Since thickness is ~30µm, color directly maps to birefringence (δ = ne − no). See Michel-Lévy chart below |
| **Extinction** | As you rotate the stage, each grain goes dark at specific angles. **Parallel extinction** (grain edges and extinction parallel) vs. **inclined extinction** (angled) is very diagnostic |
| **Undulatory extinction** | Patchy, sweeping extinction across a single grain — indicates crystal plastic deformation (common in metamorphic quartz). Visible as irregular waves without rotation |
| **Twinning** | Multiple domains within one grain extinguish at different positions — different twin types are highly diagnostic (polysynthetic in plagioclase, Carlsbad in K-spar, sector twins in pyroxene) |
| **Sign of elongation** | Whether the fast or slow ray is parallel to the long axis — requires accessory plate, determines optical character |

---

## 3. Birefringence and the Michel-Lévy chart

**Birefringence (δ)** is the difference between a mineral's maximum and minimum refractive indices:

```
δ = n_max − n_min
```

At 30µm thickness, this maps directly to interference color in XPL via the Michel-Lévy chart. The "orders" are:
- **1st order:** black → grey → white → yellow → orange → red (~550nm retardation)
- **2nd order:** violet → blue → green → yellow → orange → red  
- **3rd order:** pastel green → pink → green again...
- **Higher orders:** washed-out "pearl" pastels — very high birefringence (calcite, dolomite)

### Key birefringence landmarks (memorize these)
| Color in XPL | Birefringence | Minerals |
|---|---|---|
| Grey / white (1st order) | 0.005–0.012 | Quartz, feldspar |
| Yellow-orange (1st order) | 0.012–0.020 | Some pyroxenes |
| Bright 2nd order | 0.020–0.040 | Muscovite, hornblende, epidote |
| High 3rd order | 0.040–0.070 | Calcite, dolomite |
| Anomalous blue/brown | Variable | Epidote (unique), chlorite |

**Anomalous interference colors** (colors that shouldn't exist at the mineral's thickness/birefringence) are extremely diagnostic — epidote group minerals and chlorite both show these.

---

## 4. Systematic identification workflow

This is how a petrographer actually thinks. GneissVision mirrors this reasoning:

```
1. PPL: Is it colored?
   YES → pleochroic mineral (amphibole, pyroxene, biotite, tourmaline)
   NO  → go to step 2

2. PPL: What is the relief?
   HIGH → garnet, zircon, titanite, REE phosphates, epidote
   LOW  → quartz, feldspar, muscovite

3. XPL: Does it extinguish (go black)?
   YES, completely → isotropic (garnet, spinel, glass, opaques)
   NO → has birefringence, continue

4. XPL: What interference color?
   Grey-white → quartz OR feldspar (use twinning and alteration to split)
   Bright colored → amphibole, pyroxene, mica, epidote group
   Very high (pastels) → calcite/carbonate group

5. XPL: Any twinning?
   Polysynthetic (parallel stripes) → plagioclase feldspar
   Single Carlsbad twin → K-feldspar
   No twinning → quartz (among low-birefringence minerals)

6. PPL: Cleavage?
   Two sets at ~60/120° → amphibole
   Two sets at ~90°     → pyroxene
   One perfect set      → micas (biotite/muscovite)
   None                 → quartz, garnet, olivine
```

---

## 5. Igneous rock families and their typical mineral assemblages

Understanding what rocks *should* contain narrows the identification problem enormously.

### Felsic igneous (granite, rhyolite, granodiorite)
Quartz + K-feldspar + plagioclase + biotite ± muscovite ± hornblende  
Accessories: zircon, apatite, titanite, allanite, monazite

### Intermediate igneous (diorite, andesite)
Plagioclase + hornblende ± biotite ± augite  
Accessories: apatite, titanite, zircon

### Mafic igneous (gabbro, basalt)
Plagioclase (calcic) + augite + olivine ± hornblende (secondary)  
Accessories: ilmenite, magnetite, apatite, chromite

### Ultramafic (peridotite, dunite)
Olivine + orthopyroxene + clinopyroxene ± spinel  
Often serpentinized: olivine → serpentine + magnetite

### Metamorphic — low to medium grade
Quartz + feldspar + biotite + muscovite + chlorite  
Characteristic: garnet (almandine), staurolite, kyanite, sillimanite, andalusite

### Metamorphic — high grade (granulite facies)
Quartz + feldspar + pyroxene + garnet  
Micas largely absent (dehydration)

### Carbonatite (REE-critical)
Calcite/dolomite + apatite + pyrochlore + magnetite + monazite + bastnäsite  
These are the primary source of many REE deposits — very distinctive in thin section

---

## 6. The Big 8 — detailed identification notes

### Quartz (SiO₂)
- **PPL:** Colorless, no pleochroism, no cleavage, conchoidal fracture (curved cracks), vitreous luster, low relief
- **XPL:** 1st order grey-white, undulatory extinction common in metamorphic rocks (deformation), no twinning
- **Key:** No cleavage + low relief + no alteration + no twinning = quartz. If it has any alteration or twinning, look at feldspar instead.
- **Trap:** Can look like feldspar. Check: quartz never alters to sericite, never twins (polysynthetically)

### K-feldspar (KAlSi₃O₈ — orthoclase, sanidine, microcline)
- **PPL:** Colorless to cloudy (sericite/clay alteration very common), low relief, perfect cleavage in two directions at ~90°
- **XPL:** 1st order grey-white, Carlsbad twinning (two large domains), perthitic texture (exsolved Na-feldspar lamellae)
- **Microcline:** distinctive tartan/grid twinning (cross-hatch pattern) — unmistakable
- **Key:** Alteration + cleavage + low birefringence = feldspar. Carlsbad or grid twinning = K-spar specifically.

### Plagioclase (NaAlSi₃O₈ to CaAl₂Si₂O₈)
- **PPL:** Colorless, low relief, two cleavages at ~90°, commonly altered (sericite, epidote in calcic varieties)
- **XPL:** 1st order grey-white, **polysynthetic twinning** (parallel stripes) — the single most diagnostic feature
- **Composition clue:** More calcic plagioclase (anorthite-rich) alters more heavily and has higher relief
- **Key:** Striped twinning in XPL = plagioclase. End of story.

### Biotite (K(Mg,Fe)₃AlSi₃O₁₀(OH)₂)
- **PPL:** Strong pleochroism — brown/orange/red when cleavage is visible, pale yellow when looking down the c-axis ("birds-eye")
- **XPL:** Moderate-high birefringence (2nd–3rd order), nearly parallel extinction to cleavage
- **Alteration:** → chlorite (green, lower birefringence) or vermiculite
- **Key:** Strong brown pleochroism + one perfect cleavage + birds-eye view in PPL = biotite.

### Muscovite (KAl₂AlSi₃O₁₀(OH)₂)
- **PPL:** Colorless (no pleochroism), perfect single cleavage, low relief
- **XPL:** Very high 2nd–3rd order interference colors (bright pink, green, orange) — much higher than quartz/feldspar
- **Key:** Colorless PPL + super bright XPL colors + perfect cleavage = muscovite. The high birefringence is unmistakable.

### Hornblende (amphibole group)
- **PPL:** Green-brown pleochroism (green when perpendicular to c-axis, brown parallel), two cleavages at **60°/120°** — this angle is the key diagnostic vs pyroxene
- **XPL:** Moderate 2nd order interference colors, inclined extinction (~15–25°)
- **Key:** Two cleavages at 60/120° + green-brown pleochroism = amphibole (hornblende specifically in most igneous/metamorphic contexts)

### Augite (clinopyroxene, Ca(Mg,Fe,Al)(Si,Al)₂O₆)
- **PPL:** Pale green/brown, weak pleochroism, two cleavages at **~90°** — distinguishes from amphibole
- **XPL:** Moderate 2nd order, sector twinning, inclined extinction (~35–48°)
- **Key:** 90° cleavage angle (vs 60° for amphibole) + weak pleochroism = pyroxene. Measure the cleavage angle when you can.

### Olivine ((Mg,Fe)₂SiO₄)
- **PPL:** Colorless to pale green (Fe-rich), high relief, no cleavage, irregular cracks
- **XPL:** High birefringence (bright 2nd–3rd order), parallel extinction
- **Alteration:** Almost always partially serpentinized — mesh texture of green serpentine along cracks is very diagnostic of original olivine
- **Key:** High relief + no cleavage + high birefringence + serpentinization = olivine.

---

## 7. Metamorphic index minerals

These minerals only form above specific temperature/pressure conditions — their presence tells you the metamorphic grade (how much the rock was cooked and squeezed). This is enormously useful context for identification.

| Mineral | Grade | Appearance |
|---|---|---|
| **Chlorite** | Low (greenschist) | Green, low birefringence, anomalous XPL colors (blue-purple tinge) |
| **Biotite** | Low-medium | Brown pleochroism, appears replacing chlorite |
| **Garnet** | Medium | Isotropic (black in XPL), high relief, pink/red in PPL if almandine |
| **Staurolite** | Medium | Yellow-brown PPL, cruciform twins, high relief, moderate birefringence |
| **Kyanite** | Medium-high | Colorless, very high relief, two cleavages at ~90°, moderate birefringence, patchy blue in hand sample |
| **Sillimanite** | High | Colorless needles (fibrolite) or prismatic, high birefringence, often in bundles |
| **Andalusite** | Medium (low P) | Pink/brown pleochroism, distinctive chiastolite cross-pattern inclusion |

**Why this matters for GneissVision:** If you can identify the rock type/grade from the assemblage, you can dramatically narrow the list of possible minerals before classifying any individual grain.

---

## 8. REE (Rare Earth Element) Minerals — the interesting ones

These are typically **accessory minerals** — small grains, often <100µm, but chemically critical. They tend to cluster at grain boundaries or as inclusions in major minerals.

### Monazite (Ce,La,Nd,Th)PO₄
- **Why it matters:** Primary ore mineral for light REEs (La, Ce, Nd, Pr) and thorium. Also used for U-Th-Pb geochronology.
- **PPL:** Yellow-brown, high relief, often shows alteration (reacted corona)
- **XPL:** Moderate-high birefringence, often shows anomalous colors due to Th content
- **Habit:** Small rounded to subhedral grains, often as inclusions in biotite/garnet. In granites and pegmatites.
- **Key diagnostic:** High relief + yellow-brown color + small grain size + often radioactive (radiation damage halos in surrounding mineral)

### Xenotime (YPO₄)
- **Why it matters:** Primary ore for Y and heavy REEs (Yb, Er, Ho). Isostructural with zircon.
- **PPL:** Yellow-brown to reddish, high relief — looks like zircon
- **XPL:** Very high birefringence (higher than zircon) — this is the key difference
- **Key:** Distinguished from zircon by higher birefringence and warmer color in PPL

### Zircon (ZrSiO₄)
- **Why it matters:** Not primarily REE but concentrates U, Th, Hf, and some REEs. Critical for geochronology. Economically important as ZrO₂ source.
- **PPL:** Colorless to pale yellow/pink, extremely high relief, very high refractive index
- **XPL:** Very high birefringence, often appears "ghostly" in images due to pleochroic halos in surrounding biotite
- **Habit:** Tiny perfect prisms/pyramids. Often included in biotite (look for dark radiation halos around clear grain)
- **Key:** Pleochroic halos in host mineral around tiny high-relief grain = zircon

### Allanite (Ca,Ce)(Al,Fe)₃Si₃O₁₂(OH) — epidote group
- **Why it matters:** Light REE ore mineral, often the main REE carrier in granites
- **PPL:** Brown to reddish-brown, strong pleochroism (darker when at certain orientations), high relief, often shows metamict (radiation-damaged) texture
- **XPL:** Anomalous interference colors (like other epidote minerals), often nearly opaque in thick sections
- **Key:** Strong brown pleochroism + epidote-group anomalous XPL colors + often partly opaque = allanite

### Apatite Ca₅(PO₄)₃(F,Cl,OH)
- **Why it matters:** Common accessory, concentrates REEs especially Ce and La. Also source of P — critical for agriculture.
- **PPL:** Colorless, moderate-high relief, often euhedral hexagonal prisms
- **XPL:** Very low birefringence (almost extinct, barely shows grey)
- **Key:** High relief + almost no birefringence in XPL + hexagonal habit = apatite. The near-extinct XPL is distinctive.

### Titanite/Sphene (CaTiSiO₅)
- **Why it matters:** Concentrates REEs, U, Th. Important for geochronology. Indicator of oxidized felsic magmas.
- **PPL:** Yellow-brown to brown, very high relief, distinctive wedge/diamond shapes (sphene-shaped — literally where the name comes from)
- **XPL:** Very high birefringence, bright interference colors, often shows anomalous colors
- **Key:** Wedge/envelope shape + very high relief + warm brown PPL color = titanite. Shape alone is usually enough.

### Bastnäsite (REE)(CO₃)F
- **Why it matters:** Primary ore mineral for light REEs — Mountain Pass (USA), Bayan Obo (China). Main global REE source.
- **PPL:** Yellow, moderate relief, hexagonal habit
- **XPL:** Moderate birefringence
- **Occurrence:** Carbonatites and associated alkaline rocks. If you see this, you're in a REE deposit.
- **Key:** Yellow hexagonal grains + carbonatite host rock context = bastnäsite

### Pyrochlore (Ca,Na)₂Nb₂O₆(OH,F)
- **Why it matters:** Primary ore for Nb (niobium, critical for steel and superconductors). Also contains Ta, REEs, U, Th.
- **PPL:** Yellow-brown to brown, very high relief, often metamict (isotropic)
- **XPL:** Isotropic (black) if metamict — goes completely dark like garnet
- **Occurrence:** Carbonatites, syenites, pegmatites
- **Key:** High relief brown grain that is isotropic in XPL in a carbonatite = pyrochlore

---

## 9. GneissVision system limitations — what the model can and cannot do

### Can do reliably with PPL + XPL
- Identify major rock-forming minerals (the Big 8 and most common accessories)
- Detect alteration products and assemblage context
- Flag high-relief small grains as potential REE accessories
- Detect undulatory extinction character in quartz (deformation indicator)
- Identify twinning types

### Cannot do without stage rotation
- Precise extinction angle measurement (distinguishing pyroxene varieties, amphibole orientation)
- Sign of elongation determination
- Maximum birefringence confirmation (estimates only from interference color range)

### Requires EDS/TIMA-X to confirm
- Distinguishing xenotime from zircon definitively (similar optical properties)
- Identifying REE mineral compositions (which REEs specifically)
- Distinguishing monazite from similar phosphates (e.g. huttonite)
- Any grain <20µm

### Planned future capability
- Multi-rotation XPL stacking (0°, 45°, 90°) to recover extinction angles
- Integration with EDS data for chemical confirmation of optically ambiguous minerals

---

## 10. Why the VLM + active learning approach

Traditional approach: collect thousands of labeled images → train a CNN → classify.

GneissVision approach:
1. **Knowledge base (this document + minerals.json):** structured optical properties fed as context to a Vision-Language Model (VLM). The model "reads" the reference while looking at your image.
2. **VLM inference:** Claude claude-sonnet-4-6 (or GPT-4o) receives PPL + XPL image pair and produces a prediction with reasoning — explaining *why* it thinks a mineral is what it is, mirroring the systematic workflow in section 4.
3. **You correct it:** corrections are saved as labeled examples.
4. **Active learning:** the system prioritizes your corrections on uncertain predictions (60/40 confidence, not 99/1). Maximum label value per minute of your time.
5. **Local model (later):** once ~100 labeled examples per class exist, fine-tune a small ViT for fast offline inference.

This approach requires zero labeled data to start and improves continuously with your expertise.

---

## 11. Vocabulary reference

| Term | Definition |
|---|---|
| **Birefringence (δ)** | Difference between max and min refractive index. Controls interference color. |
| **Pleochroism** | Color change with stage rotation in PPL. Caused by oriented crystal bonds. |
| **Relief** | How "bumpy" a grain looks relative to mounting epoxy. Controlled by refractive index difference. |
| **Extinction** | When a grain goes black in XPL upon rotation. |
| **Undulatory extinction** | Wavy, uneven extinction across a grain — crystal plastic deformation. |
| **Twinning** | Multiple crystal domains within one grain, extinguishing separately. |
| **Euhedral** | Well-formed crystal faces present. |
| **Anhedral** | No crystal faces — irregular grain shape. |
| **Metamict** | Crystal structure destroyed by radiation damage from U/Th decay. Usually isotropic in XPL. |
| **Accessory mineral** | Present in small amounts (<5%), doesn't control rock name but is chemically important. |
| **Carbonatite** | Igneous rock with >50% carbonate minerals — most important REE deposit type. |
| **Pegmatite** | Extremely coarse-grained igneous rock. Concentrates rare elements. Critical target for REEs, Li, Nb, Ta. |
| **Modal analysis** | Measuring the percentage of each mineral in a thin section — what TIMA-X does automatically. |
| **Assemblage** | The full set of minerals present in a rock — constrains temperature/pressure conditions. |
