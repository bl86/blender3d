# Usage Examples

Complete guide with practical examples for different use cases.

## Quick Start Examples

### 1. Generate Default Animation (10 seconds, golden logo)
```bash
./quickstart.sh
```
This runs system check, generates scene, and opens in Blender.

### 2. Preview Render (Fast)
```bash
./scripts/render_animation.sh preview
```
- 64 samples, 720p resolution
- ~10 minutes on modern GPU
- Good for testing

### 3. Production Render (High Quality)
```bash
./scripts/render_animation.sh production
```
- 256 samples, 1080p resolution
- ~45 minutes on RTX 3080
- Final deliverable quality

## Custom Animation Examples

### Example 1: Quick 5-Second Teaser
```bash
blender --background --python scripts/advanced_setup.py -- \
  --timing quick \
  --render preview \
  --color classic_gold \
  --fire intense
```
**Result:** Fast 5-second reveal with intense fire

### Example 2: Cinematic Rose Gold
```bash
blender --background --python scripts/advanced_setup.py -- \
  --timing cinematic \
  --render production \
  --color rose_gold \
  --fire moderate \
  --camera telephoto \
  --lighting dramatic
```
**Result:** Slow 18-second cinematic reveal with rose gold material

### Example 3: Ultra 4K Production
```bash
blender --background --python scripts/advanced_setup.py -- \
  --timing extended \
  --render ultra \
  --color platinum \
  --fire extreme \
  --camera dramatic \
  --lighting cinematic
```
**Result:** 20-second 4K ultra-quality showcase (very slow to render)

### Example 4: Soft Silver Presentation
```bash
blender --background --python scripts/advanced_setup.py -- \
  --timing standard \
  --render production \
  --color silver \
  --fire subtle \
  --camera standard \
  --lighting soft
```
**Result:** Professional presentation with subtle fire

## Python API Examples

### Example 1: Basic Programmatic Setup
```python
import bpy
from logo_animation import LogoAnimationSetup

# Create animation
animation = LogoAnimationSetup(
    svg_path="/path/to/alter.svg",
    output_path="/path/to/output"
)

# Generate scene
animation.setup_animation()

# Save
bpy.ops.wm.save_as_mainfile(filepath="my_animation.blend")
```

### Example 2: Custom Timing
```python
from logo_animation import LogoAnimationSetup

animation = LogoAnimationSetup(
    svg_path="alter.svg",
    output_path="output"
)

# Customize timing
animation.total_frames = 450  # 15 seconds at 30fps
animation.fire_end_frame = 300  # Fire ends at 10 seconds

animation.setup_animation()
```

### Example 3: Override Material Color
```python
import bpy
from logo_animation import LogoAnimationSetup

class CustomColorAnimation(LogoAnimationSetup):
    def create_golden_material(self):
        mat = super().create_golden_material()

        # Find principled BSDF and change color
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                # Custom emerald green
                node.inputs['Base Color'].default_value = (0.1, 0.8, 0.3, 1.0)
                node.inputs['Metallic'].default_value = 0.8
                node.inputs['Roughness'].default_value = 0.3

        return mat

animation = CustomColorAnimation("alter.svg", "output")
animation.setup_animation()
```

### Example 4: Batch Render Multiple Variants
```python
import bpy
import os
from advanced_setup import AdvancedAnimationSetup
from animation_config import get_preset

variants = [
    ('classic_gold', 'intense'),
    ('rose_gold', 'moderate'),
    ('silver', 'subtle'),
    ('platinum', 'extreme'),
]

for color, fire in variants:
    print(f"Rendering {color} with {fire} fire...")

    presets = {
        'timing': get_preset('timing', 'standard'),
        'render': get_preset('render', 'draft'),
        'color': get_preset('color', color),
        'fire': get_preset('fire', fire),
        'camera': get_preset('camera', 'standard'),
        'lighting': get_preset('lighting', 'studio'),
    }

    animation = AdvancedAnimationSetup(
        svg_path="alter.svg",
        output_path=f"output/{color}_{fire}",
        presets=presets
    )

    animation.setup_animation()

    # Save blend file
    blend_path = f"animation_{color}_{fire}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    # Render
    bpy.ops.render.render(animation=True)

    print(f"Completed: {color} with {fire}")
```

## Command-Line Rendering

### Render Specific Frame Range
```bash
blender -b alter_logo_animation.blend -s 1 -e 100 -a
```
Renders frames 1-100 only

### Render Single Frame
```bash
blender -b alter_logo_animation.blend -f 150
```
Renders frame 150 (mid-animation with fire)

### Render with Custom Output
```bash
blender -b alter_logo_animation.blend -o "/path/to/output/frame_####" -a
```
Renders to custom path with frame numbers

### Override Sample Count
```bash
blender -b alter_logo_animation.blend \
  --python-expr "import bpy; bpy.context.scene.cycles.samples = 512" \
  -a
```
Renders with 512 samples (ultra quality)

### Render Single Frame to Test
```bash
blender -b alter_logo_animation.blend -f 150 -o test.png
```
Quick test render of interesting frame

## Advanced Customization

### Example 1: Change Logo Position
Edit `logo_animation.py`, modify `animate_logo()`:
```python
def animate_logo(self):
    # Start from left side
    start_pos = Vector((-10, 15, 0))
    # End at center
    end_pos = Vector((0, -5, 0))

    self.logo_obj.location = start_pos
    self.logo_obj.keyframe_insert(data_path="location", frame=1)

    self.logo_obj.location = end_pos
    self.logo_obj.keyframe_insert(data_path="location", frame=self.total_frames)
```

### Example 2: Add Logo Rotation
Edit `logo_animation.py`, modify `animate_logo()`:
```python
# Add continuous rotation
self.logo_obj.rotation_euler = (0, 0, 0)
self.logo_obj.keyframe_insert(data_path="rotation_euler", frame=1)

# Two full rotations
self.logo_obj.rotation_euler = (0, 0, math.radians(720))
self.logo_obj.keyframe_insert(data_path="rotation_euler", frame=self.total_frames)
```

### Example 3: Multiple Fire Emitters
Edit `logo_animation.py`, modify `create_fire_simulation()`:
```python
def create_fire_simulation(self):
    domain, emitter1 = super().create_fire_simulation()

    # Add second emitter (smaller, at top)
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 2),
        major_radius=2.0,
        minor_radius=0.4
    )
    emitter2 = bpy.context.active_object
    emitter2.parent = self.logo_obj

    # Add fluid modifier
    bpy.ops.object.modifier_add(type='FLUID')
    emitter2.modifiers["Fluid"].fluid_type = 'FLOW'
    flow = emitter2.modifiers["Fluid"].flow_settings
    flow.flow_type = 'FIRE'
    flow.fuel_amount = 1.5

    emitter2.hide_render = True

    return domain, [emitter1, emitter2]
```

### Example 4: Color-Changing Material
Edit `logo_animation.py`, add after `create_golden_material()`:
```python
def animate_material_color(self):
    mat = self.logo_obj.data.materials[0]

    # Find principled BSDF
    principled = None
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled = node
            break

    if principled:
        # Start gold
        principled.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
        principled.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=1)

        # End platinum
        principled.inputs['Base Color'].default_value = (0.9, 0.89, 0.88, 1.0)
        principled.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=self.total_frames)
```

## Preset Combinations

### Maximum Impact
```bash
--timing cinematic --render ultra --color classic_gold --fire extreme --camera dramatic --lighting dramatic
```
**Use case:** Hero trailer reveal

### Elegant Presentation
```bash
--timing standard --render production --color platinum --fire subtle --camera telephoto --lighting soft
```
**Use case:** Corporate presentation

### Fast Social Media
```bash
--timing quick --render preview --color rose_gold --fire moderate --camera wide --lighting studio
```
**Use case:** Instagram/TikTok teaser

### Retro Style
```bash
--timing extended --render production --color bronze --fire intense --camera standard --lighting cinematic
```
**Use case:** Vintage/retro branding

## Interactive Blender Usage

### Open and Modify
```bash
blender alter_logo_animation.blend
```

**Useful shortcuts:**
- `Spacebar`: Play animation
- `Shift+Left/Right Arrow`: Jump 10 frames
- `0` (numpad): Camera view
- `Z`: Shading mode menu
- `F12`: Render current frame
- `Ctrl+F12`: Render animation

### Adjust Fire in GUI
1. Select `FireDomain` object
2. Physics Properties tab → Fluid → Domain
3. Adjust:
   - Resolution Max (higher = more detail)
   - Time Scale (higher = faster)
   - Vorticity (higher = more turbulence)

### Adjust Material in GUI
1. Select logo object
2. Shading workspace (top tabs)
3. Open Shader Editor (bottom)
4. Modify nodes:
   - Base Color (gold color)
   - Roughness (0-1, lower = shinier)
   - Emission Strength (glow intensity)

### Change Camera
1. Select camera
2. Press `N` for properties panel
3. Camera tab:
   - Focal Length (mm)
   - F-Stop (DOF blur)
4. `Ctrl+Alt+0`: Move camera to current view

## Troubleshooting Examples

### Problem: Fire too weak
**Solution 1 - Increase fuel:**
```python
flow_settings.fuel_amount = 3.0  # Default: 2.0
```

**Solution 2 - Increase emission:**
Edit fire material emission multiply node: `35.0` instead of `25.0`

### Problem: Animation too slow
**Solution - Reduce frames:**
```python
animation.total_frames = 150  # 5 seconds instead of 10
```

### Problem: Logo too small in frame
**Solution - Bring camera closer:**
```python
end_pos = Vector((0, -3, 0))  # Was: (0, -5, 0)
```

### Problem: Render too dark
**Solution - Increase lighting:**
```python
# In setup_lighting()
key_light.data.energy = 800  # Was: 500
```

### Problem: Out of memory
**Solution - Reduce settings:**
```bash
blender -b alter_logo_animation.blend \
  --python-expr "
import bpy
scene = bpy.context.scene
scene.cycles.samples = 128
scene.render.resolution_percentage = 50
domain = bpy.data.objects['FireDomain']
domain.modifiers['Fluid'].domain_settings.resolution_max = 128
" -a
```

## Production Pipeline

### Step 1: Preview
```bash
./scripts/render_animation.sh preview
```
Review in video player, verify timing/composition

### Step 2: Test Frame
```bash
blender -b alter_logo_animation.blend -f 150 -o test_frame.png
```
Check quality at key moment

### Step 3: Production Render
```bash
./scripts/render_animation.sh production
```
Final render overnight

### Step 4: Post-Processing (Optional)
```bash
ffmpeg -i output/alter_logo_animation_0001.png -i audio.mp3 \
  -c:v libx264 -preset slow -crf 18 -c:a aac \
  final_with_audio.mp4
```
Add audio and re-encode

## Performance Comparison

| Configuration | Render Time (RTX 3080) | Quality | Use Case |
|---------------|------------------------|---------|----------|
| `--render preview` | ~10 min | Good | Quick review |
| `--render draft` | ~20 min | Better | Client preview |
| `--render production` | ~45 min | Excellent | Final delivery |
| `--render ultra` (4K) | ~3 hours | Outstanding | Cinema/broadcast |

## Tips & Tricks

### Speed Up Preview
- Use `--render preview` preset
- Reduce frame range: `-s 1 -e 150`
- Disable motion blur in GUI
- Lower domain resolution to 128

### Better Fire
- Increase domain resolution to 384
- Add more noise: `noise_strength = 2.0`
- Multiple emitters at different sizes
- Custom color ramp (orange → yellow → white)

### Smoother Animation
- Increase FPS to 60
- Enable motion blur
- Longer duration (more frames)
- Ease in/out keyframe interpolation

### Professional Look
- Add camera shake (subtle)
- Lens distortion (chromatic aberration)
- Film grain in compositor
- Color LUT for mood

## Additional Resources

**Blender Docs:**
- Cycles: https://docs.blender.org/manual/en/latest/render/cycles/
- Fluid: https://docs.blender.org/manual/en/latest/physics/fluid/
- Compositing: https://docs.blender.org/manual/en/latest/compositing/

**Community:**
- Blender Artists: https://blenderartists.org/
- BlenderNation: https://www.blendernation.com/
- r/blender: https://reddit.com/r/blender
