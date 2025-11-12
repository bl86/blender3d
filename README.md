# Alter Logo Fire Animation

Professional 3D animation of the Alter logo with realistic fire effects, created in Blender.

## Overview

This project contains a complete Blender animation setup featuring:
- **Golden logo** with photorealistic metallic material, reflections and glow effects
- **Realistic fire simulation** using Mantaflow fluid dynamics
- **Dynamic camera movement** with depth of field
- **Professional lighting** setup (3-point lighting)
- **Advanced compositing** with bloom, color grading and lens effects
- **High-quality rendering** using Cycles engine with GPU acceleration

## Animation Details

- **Duration**: 300 frames (~10 seconds at 30fps)
- **Resolution**: 1920x1080 (Full HD)
- **Key Features**:
  - Logo starts far from camera, surrounded by fire
  - Smooth movement towards camera with subtle rotation
  - Fire gradually fades out around frame 200
  - Logo fills frame with golden glow and reflections
  - Professional color grading and post-processing

## Requirements

- **Blender** 3.0 or higher (tested with 3.6+)
- **GPU** with CUDA or OptiX support (recommended for faster rendering)
- **Python** 3.9+ (comes with Blender)
- **Disk Space**: ~5GB for cache and output files
- **RAM**: 8GB minimum, 16GB+ recommended
- **OS**: Windows 10/11, Linux, or macOS

## 🎬 SIMPLEST WAY - Just Double-Click!

### ⭐ **Absolute Easiest** (No Commands, No Typing!)

**Windows/Mac/Linux:**
1. **Double-click** `GO.py`
2. Wait ~45 minutes
3. Done! Check `output/` folder

**Want Options?** Double-click `start.py` for interactive menu.

**📖 Full guide:** [START.md](START.md)

---

## Quick Start (Command Line)

### 🐍 Python Workflow (For Terminal Users)

**One Command - Does Everything:**
```bash
blender --background --python make_animation.py
```
↳ Generates scene + renders animation (~45 min)

**Quick Preview (10 min):**
```bash
blender --background --python make_animation.py -- --quick
```

**With Video File:**
```bash
blender --background --python make_animation.py -- --production --video
```

**📖 For detailed Python workflow:** See [PYTHON_WORKFLOW.md](PYTHON_WORKFLOW.md)

---

### Windows Users

#### One-Command Setup (Recommended)

**Option 1: Batch Script**
```cmd
quickstart.bat
```

**Option 2: PowerShell** (if you prefer PowerShell)
```powershell
.\quickstart.ps1
```

This will automatically:
1. Check system requirements
2. Generate the Blender scene
3. Open Blender with the animation

#### Manual Steps

**1. Generate Scene**
```cmd
scripts\setup_scene.bat
```

**2. Preview in Blender**
```cmd
"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" alter_logo_animation.blend
```
Or if Blender is in PATH:
```cmd
blender alter_logo_animation.blend
```

**3. Render Animation**

Quick preview (faster):
```cmd
scripts\render_animation.bat preview
```

Production quality:
```cmd
scripts\render_animation.bat production
```

### Linux / macOS Users

#### One-Command Setup (Recommended)
```bash
chmod +x quickstart.sh scripts/*.sh
./quickstart.sh
```

#### Manual Steps

**1. Generate Scene**
```bash
chmod +x scripts/*.sh
./scripts/setup_scene.sh
```

**2. Preview in Blender**
```bash
blender alter_logo_animation.blend
```

**3. Render Animation**

Quick preview:
```bash
./scripts/render_animation.sh preview
```

Production quality:
```bash
./scripts/render_animation.sh production
```

Or render directly with Blender:
```bash
blender -b alter_logo_animation.blend -a
```

### Tips for All Platforms

- Press **Spacebar** in Blender to play/pause animation preview
- Press **F12** to render current frame
- Press **Ctrl+F12** to render full animation
- Animation is 300 frames (10 seconds at 30fps)
- Fire fades out around frame 200

## Project Structure

```
blender3d/
├── alter.svg                      # Source logo file
├── alter_logo_animation.blend     # Generated Blender scene (after setup)
├── quickstart.sh                  # Linux/Mac one-command setup
├── quickstart.bat                 # Windows batch one-command setup
├── quickstart.ps1                 # Windows PowerShell one-command setup
├── scripts/
│   ├── logo_animation.py          # Main animation setup script
│   ├── advanced_setup.py          # Animation with customizable presets
│   ├── animation_config.py        # Preset configuration system
│   ├── check_system.py            # System requirements validator
│   ├── setup_scene.sh             # Linux/Mac scene generation
│   ├── setup_scene.bat            # Windows batch scene generation
│   ├── setup_scene.ps1            # Windows PowerShell scene generation
│   ├── render_animation.sh        # Linux/Mac rendering helper
│   ├── render_animation.bat       # Windows batch rendering helper
│   └── render_animation.ps1       # Windows PowerShell rendering helper
├── assets/                        # Additional assets (textures, etc.)
├── output/                        # Rendered output files
├── README.md                      # This file
├── PROJECT_INFO.md                # Technical documentation
└── USAGE_EXAMPLES.md              # Practical examples and recipes
```

## Technical Details

### Fire Simulation
- **Engine**: Mantaflow (Blender's built-in fluid solver)
- **Domain Resolution**: 256 voxels
- **Flow Type**: Fire with smoke
- **Emitter**: Torus shape parented to logo
- **Animation**: Density keyframed to fade out

### Materials

#### Golden Logo Material
- Base: Principled BSDF with metallic workflow
- Color: Rich gold (#FFB456)
- Metallic: 1.0 (full metal)
- Roughness: 0.15 (polished)
- Emission: Subtle warm glow
- Anisotropic reflections for realism

#### Fire Material
- Volumetric shader with emission
- Color gradient: Dark red → Orange → Yellow → White
- Emission strength: 25x
- Smoke absorption and scattering

### Lighting Setup
1. **Key Light**: Area light (500W) - main illumination
2. **Fill Light**: Area light (200W) - soften shadows
3. **Rim Light**: Spot light (300W) - edge highlighting
4. **Environment**: Dark blue ambient (0.5 strength)

### Render Settings
- **Engine**: Cycles (path tracing)
- **Samples**: 256 (production) / 64 (preview)
- **Denoising**: OpenImageDenoise
- **Volume Steps**: 1024 max
- **Motion Blur**: Enabled (0.5 shutter)
- **Color Space**: Filmic with High Contrast look

### Compositing
- Fog glow bloom effect
- Color correction (saturation +20%, gain +10%)
- Lens distortion for cinematic look
- Chromatic aberration

## Customization

### Adjust Animation Timing

Edit `scripts/logo_animation.py`:

```python
self.total_frames = 300        # Total animation length
self.fire_end_frame = 200      # When fire fades out
```

### Change Logo Color

Modify the golden material base color:

```python
principled.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
# Change to your desired RGB values (0-1 range)
```

### Adjust Fire Intensity

Modify emitter settings:

```python
flow_settings.fuel_amount = 2.0      # Fire intensity
flow_settings.temperature = 3.0       # Fire heat
flow_settings.velocity_factor = 1.5   # Fire movement speed
```

### Camera Distance

Adjust start and end positions:

```python
start_pos = Vector((0, 15, 0))   # Starting distance
end_pos = Vector((0, -5, 0))     # Ending distance (closer)
```

## Performance Tips

1. **Preview Mode**: Use preview quality for testing
2. **GPU Rendering**: Enable GPU compute in Blender preferences
3. **Cache Management**: Fluid cache is stored in `blendcache_alter_logo_animation/`
4. **Resolution**: Reduce resolution percentage for faster renders
5. **Samples**: Lower samples for previews (64 is usually enough)

## Troubleshooting

### Windows: Blender Not Found
If scripts can't find Blender:
1. **Add to PATH**: Add Blender installation directory to Windows PATH
   - Search "Environment Variables" in Windows
   - Edit System PATH variable
   - Add: `C:\Program Files\Blender Foundation\Blender 3.6\`
2. **Or use full path** in commands:
   ```cmd
   "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" --background --python scripts\logo_animation.py
   ```

### Windows: PowerShell Execution Policy
If `.ps1` scripts don't run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows: Script won't run from double-click
Right-click `.bat` file → **Run as administrator** (if in protected folder)
Or run from Command Prompt/PowerShell instead.

### Fire Not Visible
- Ensure fluid cache is baked (Cache → Bake All)
- Check domain viewport display settings
- Verify fire material is assigned to domain

### Slow Rendering
- Enable GPU rendering in preferences
- Reduce sample count
- Lower domain resolution
- Disable motion blur for preview

### Out of Memory
- Reduce domain resolution (128 instead of 256)
- Lower volume max steps
- Reduce render resolution

### Logo Not Importing
- Verify alter.svg is in project root
- Check SVG is valid and not corrupted
- Try opening SVG in Inkscape first

## Output

Rendered files are saved to `output/` directory:
- **Format**: MP4 (H.264)
- **Quality**: High (low compression)
- **Frame Rate**: 30 fps
- **Resolution**: 1920x1080

Individual frames are named: `alter_logo_animation_0001.png`, etc.

## Performance Benchmarks

Approximate render times (will vary based on hardware):

| Hardware | Quality | Time |
|----------|---------|------|
| RTX 3080 | Production | ~45 min |
| RTX 3060 | Production | ~75 min |
| GTX 1080 | Production | ~120 min |
| CPU Only | Production | ~6 hours |

Preview mode is approximately 4x faster.

## Credits

Animation system designed for professional 3D production workflows.
Fire simulation powered by Mantaflow.
Rendering by Blender Cycles engine.

## License

Proprietary - Alter Logo Animation Project
