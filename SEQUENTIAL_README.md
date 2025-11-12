# ALTER Logo Sequential Animation

## Two Animation Versions

You now have **TWO different animation concepts**:

### 1. **Original Version** (ALTER_LOGO_COMPLETE.py)
- **Run:** `GO.py`
- **Output:** `alter_logo_fire_animation.blend`
- **Concept:** Entire logo comes together as one unit with fire

### 2. **Sequential Version** (ALTER_LOGO_SEQUENTIAL.py) ⭐ NEW!
- **Run:** `GO_SEQUENTIAL.py`
- **Output:** `alter_logo_sequential.blend`
- **Concept:** Each element arrives separately with its own fire

---

## Sequential Animation Details

### Element Order:
1. **Treble Key** (first element from SVG)
2. **Letter A** (with fire)
3. **Letter L** (with fire)
4. **Letter T** (with fire)
5. **Letter E** (with fire)
6. **Letter R** (with fire)
7. **"BANJA LUKA"** text (final element)

### Timing:
- Each element takes **40 frames** to arrive (~1.3 seconds at 30fps)
- **30 frames** gap between elements starting
- Each element **holds position** as next one arrives
- Total animation depends on number of SVG components

### Fire Behavior:
- Each element has its own **fire emitter**
- Fire follows **element contours** (wireframe method)
- Fire appears when element **starts moving**
- Fire fades when element **reaches final position**
- **Shared fire domain** handles all elements

---

## How to Run

### Quick Start:
```bash
# Original version (logo comes as one)
python GO.py

# Sequential version (elements come separately)
python GO_SEQUENTIAL.py
```

### In Blender:
```bash
# Original
blender --background --python ALTER_LOGO_COMPLETE.py

# Sequential
blender --background --python ALTER_LOGO_SEQUENTIAL.py
```

---

## Output Comparison

| Feature | Original | Sequential |
|---------|----------|------------|
| Logo entrance | All at once | One element at a time |
| Fire coverage | Full logo outline | Each element separately |
| Animation length | ~10 seconds | ~12-15 seconds |
| Visual impact | Bold, unified | Dynamic, building |
| Output folder | `output/` | `output_sequential/` |
| File naming | `frame_####.png` | `seq_####.png` |

---

## Rendering Both Versions

You can render **both** while you work:

1. **Start Original:**
   ```bash
   python GO.py
   # Wait for generation (1-2 min)
   # Open alter_logo_fire_animation.blend
   # Press Ctrl+F12 to start render
   ```

2. **Start Sequential (in parallel):**
   ```bash
   python GO_SEQUENTIAL.py
   # Wait for generation (3-5 min, more elements)
   # Open alter_logo_sequential.blend
   # Press Ctrl+F12 to start render
   ```

3. **Compare Results:**
   - `output/frame_0001.png` - Original
   - `output_sequential/seq_0001.png` - Sequential

---

## Technical Details

### Sequential Animation Features:
- **Automatic element separation** from SVG components
- **Individual fire emitters** per element
- **Coordinated timing** - elements build up naturally
- **Smooth Bezier interpolation** for fluid motion
- **Same visual quality** as original (256 samples, OptiX)

### Scene Setup:
- **Ground plane:** Reflective dark surface
- **4-point lighting:** Key, Fill, Rim, Top
- **Sky environment:** Nishita sky for realistic reflections
- **Transparent background:** PNG sequence ready for compositing

---

## Use Cases

### When to use Original:
- Need quick, impactful logo reveal
- Want logo to feel solid and unified
- Shorter animation time
- Traditional logo animation

### When to use Sequential:
- Want dynamic, engaging build-up
- Need attention-grabbing effect
- Each letter matters individually
- Modern motion graphics style
- Building brand recognition letter by letter

---

## Premiere Pro Import

Both versions output **PNG sequences with transparency**:

1. Open Premiere Pro
2. **File → Import → Media**
3. Select first frame:
   - `output/frame_0001.png` (Original)
   - `output_sequential/seq_0001.png` (Sequential)
4. Premiere automatically imports full sequence
5. Drag to timeline
6. **Transparent background ready** for compositing!

---

## Tips

- **Run both:** Generate both versions to compare
- **Preview first:** Use SPACEBAR in Blender viewport before rendering
- **Rendered mode:** Press Z → Rendered to see fire in viewport
- **Frame by frame:** Scrub timeline to see how elements arrive
- **Customize timing:** Edit keyframes in Blender Graph Editor

---

## Troubleshooting

**"Elements look wrong":**
- Check that alter.svg has separate paths for each component
- SVG should have: treble key, A, L, T, E, R as separate elements

**"Fire not visible":**
- Make sure fire is baked (Step 12)
- Switch to Rendered viewport mode (Z → Rendered)
- Check domain size covers all element paths

**"Animation too long/short":**
- Edit `frame_offset` in ALTER_LOGO_SEQUENTIAL.py (line 177)
- Reduce for faster sequence, increase for slower

---

Enjoy both animation styles! 🔥✨
