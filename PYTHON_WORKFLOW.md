# Python-Only Workflow Guide

Complete guide for using pure Python scripts without batch/shell files.
Perfect for advanced users and automation.

## Overview

This workflow uses **pure Python scripts** that work directly with Blender:
- No .bat or .sh files needed
- Works on Windows, Linux, and macOS identically
- Can be automated and integrated into pipelines
- Easy to customize and extend

## Quick Start

### 1. Generate Animation (Standard Settings)

```bash
blender --background --python run_animation.py
```

This creates `alter_logo_animation.blend` with:
- Golden logo from alter.svg
- Realistic fire simulation
- Camera animation
- Professional lighting
- 300 frames (10 seconds at 30fps)

### 2. Render Preview (Fast - 10 minutes)

```bash
blender -b alter_logo_animation.blend --python render_preview.py
```

Output: `output/preview_*.png` (64 samples, 720p)

### 3. Render Production (High Quality - 45+ minutes)

```bash
blender -b alter_logo_animation.blend --python render_production.py
```

Output: `output/production_*.png` (256 samples, 1080p)

### 4. Create Video from Frames

```bash
blender --background --python create_video.py
```

Output: `output/animation.mp4`

## Custom Animations with Presets

### Basic Custom Animation

```bash
blender --background --python run_custom_animation.py -- --color rose_gold --fire intense
```

### Advanced Custom Animation

```bash
blender --background --python run_custom_animation.py -- \
  --timing cinematic \
  --color platinum \
  --fire extreme \
  --camera dramatic \
  --lighting cinematic \
  --render ultra
```

### List All Available Presets

```bash
blender --background --python run_custom_animation.py -- --list
```

## Available Scripts

### Core Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `run_animation.py` | Generate standard animation | `blender -b --python run_animation.py` |
| `run_custom_animation.py` | Generate with custom presets | `blender -b --python run_custom_animation.py -- [options]` |
| `render_preview.py` | Fast preview render | `blender -b file.blend --python render_preview.py` |
| `render_production.py` | High quality render | `blender -b file.blend --python render_production.py` |
| `create_video.py` | Convert frames to video | `blender -b --python create_video.py` |

### Helper Scripts (in scripts/ folder)

| Script | Purpose |
|--------|---------|
| `logo_animation.py` | Core animation system |
| `advanced_setup.py` | Preset-based setup |
| `animation_config.py` | Preset definitions |
| `check_system.py` | System requirements check |

## Detailed Examples

### Example 1: Complete Workflow (Standard)

```bash
# Step 1: Generate scene
blender --background --python run_animation.py

# Step 2: Preview render
blender -b alter_logo_animation.blend --python render_preview.py

# Step 3: If satisfied, production render
blender -b alter_logo_animation.blend --python render_production.py

# Step 4: Create video
blender --background --python create_video.py
```

### Example 2: Custom Rose Gold with Intense Fire

```bash
# Generate custom animation
blender --background --python run_custom_animation.py -- \
  --color rose_gold \
  --fire intense

# Render (uses preset name in filename)
blender -b alter_standard_rose_gold_intense.blend --python render_production.py

# Create video
blender --background --python create_video.py -- \
  --output rose_gold_animation.mp4
```

### Example 3: Quick 5-Second Teaser

```bash
# Generate quick animation
blender --background --python run_custom_animation.py -- \
  --timing quick \
  --render preview

# Render
blender -b alter_quick_classic_gold_intense.blend --python render_preview.py

# Create video
blender --background --python create_video.py -- \
  --fps 30 \
  --output teaser.mp4
```

### Example 4: Ultra Quality 4K

```bash
# Generate ultra quality setup
blender --background --python run_custom_animation.py -- \
  --timing cinematic \
  --render ultra \
  --color platinum \
  --fire extreme

# Render (will take hours!)
blender -b alter_cinematic_platinum_extreme.blend --python render_production.py

# Create 4K video
blender --background --python create_video.py -- \
  --output 4k_animation.mp4
```

## Preset Options

### Timing Presets

| Preset | Frames | Duration | Description |
|--------|--------|----------|-------------|
| `quick` | 150 | 5s | Quick teaser |
| `standard` | 300 | 10s | Standard animation (default) |
| `cinematic` | 450 | 18s | Slow cinematic reveal |
| `extended` | 600 | 20s | Extended showcase |

### Color Presets

| Preset | Description |
|--------|-------------|
| `classic_gold` | Rich golden metal (default) |
| `rose_gold` | Elegant rose gold |
| `white_gold` | Bright white gold |
| `silver` | Polished silver |
| `platinum` | Premium platinum |
| `bronze` | Ancient bronze |

### Fire Intensity Presets

| Preset | Description |
|--------|-------------|
| `subtle` | Gentle flames |
| `moderate` | Moderate fire |
| `intense` | Strong inferno (default) |
| `extreme` | Extreme blaze |

### Camera Presets

| Preset | Lens | Description |
|--------|------|-------------|
| `standard` | 50mm | Standard lens (default) |
| `wide` | 35mm | Wide angle |
| `telephoto` | 85mm | Telephoto with shallow DOF |
| `dramatic` | 24mm | Dramatic wide with bokeh |

### Lighting Presets

| Preset | Description |
|--------|-------------|
| `studio` | Professional studio (default) |
| `dramatic` | High contrast dramatic |
| `soft` | Soft even lighting |
| `cinematic` | Cinematic mood |

### Render Quality Presets

| Preset | Samples | Resolution | Time (est.) |
|--------|---------|------------|-------------|
| `preview` | 64 | 720p | ~10 min |
| `draft` | 64 | 1080p 75% | ~20 min |
| `production` | 256 | 1080p | ~45 min |
| `ultra` | 512 | 4K | ~3 hours |

## Advanced Usage

### Using Inside Blender GUI

1. Open Blender
2. Switch to Scripting workspace
3. Open script: Text → Open → Select `run_animation.py`
4. Press **Alt+P** or click **Run Script**

The scene will be generated in the current Blender session.

### Automation and Batch Processing

Create a script to generate multiple variants:

```bash
#!/bin/bash
# render_all_variants.sh

COLORS=("classic_gold" "rose_gold" "silver" "platinum")
FIRES=("subtle" "moderate" "intense" "extreme")

for color in "${COLORS[@]}"; do
    for fire in "${FIRES[@]}"; do
        echo "Rendering: $color with $fire fire"

        # Generate
        blender --background --python run_custom_animation.py -- \
            --color $color \
            --fire $fire \
            --render preview

        # Render
        blend_file="alter_standard_${color}_${fire}.blend"
        blender -b $blend_file --python render_preview.py

        # Create video
        blender --background --python create_video.py -- \
            --output "output/${color}_${fire}.mp4"
    done
done
```

### Python API Direct Usage

You can also import and use the classes directly:

```python
import sys
sys.path.insert(0, 'scripts')

from logo_animation import LogoAnimationSetup
from animation_config import get_preset

# Create custom animation
animation = LogoAnimationSetup('alter.svg', 'output')

# Customize settings
animation.total_frames = 450
animation.fire_end_frame = 300

# Generate
animation.setup_animation()
```

### Render Single Frame for Testing

```bash
# Render frame 150 (mid-animation with fire)
blender -b alter_logo_animation.blend -f 150 -o test_frame.png
```

### Render Specific Frame Range

```bash
# Render only frames 100-200
blender -b alter_logo_animation.blend -s 100 -e 200 -a
```

## Integration with Other Tools

### CI/CD Pipeline Example

```yaml
# .github/workflows/render.yml
name: Render Animation

on: [push]

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install Blender
        run: |
          wget https://download.blender.org/release/Blender3.6/blender-3.6-linux-x64.tar.xz
          tar -xf blender-3.6-linux-x64.tar.xz

      - name: Generate Animation
        run: |
          ./blender-3.6-linux-x64/blender --background --python run_animation.py

      - name: Render Preview
        run: |
          ./blender-3.6-linux-x64/blender -b alter_logo_animation.blend --python render_preview.py

      - name: Upload Artifact
        uses: actions/upload-artifact@v2
        with:
          name: preview-frames
          path: output/
```

### Docker Usage

```dockerfile
FROM ubuntu:22.04

# Install Blender
RUN apt-get update && apt-get install -y \
    wget xz-utils \
    && wget https://download.blender.org/release/Blender3.6/blender-3.6-linux-x64.tar.xz \
    && tar -xf blender-3.6-linux-x64.tar.xz -C /opt/ \
    && ln -s /opt/blender-3.6-linux-x64/blender /usr/local/bin/blender

# Copy project
COPY . /app
WORKDIR /app

# Generate and render
CMD blender --background --python run_animation.py && \
    blender -b alter_logo_animation.blend --python render_production.py
```

## Troubleshooting

### Script Not Found Error

Make sure you're in the project directory:
```bash
cd path/to/blender3d
blender --background --python run_animation.py
```

### Import Error

Scripts depend on each other. Ensure directory structure is intact:
```
blender3d/
├── run_animation.py
├── scripts/
│   ├── logo_animation.py
│   └── ...
```

### Blender Not in PATH

Use full path to Blender:
```bash
# Windows
"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe" --background --python run_animation.py

# Linux
/path/to/blender --background --python run_animation.py

# macOS
/Applications/Blender.app/Contents/MacOS/Blender --background --python run_animation.py
```

### Out of Memory

Reduce settings in render scripts:
```python
# In render_production.py, change:
scene.cycles.samples = 128  # Instead of 256
scene.render.resolution_percentage = 75  # Instead of 100
```

## Performance Tips

1. **Use GPU**: Edit `logo_animation.py`:
   ```python
   scene.cycles.device = 'GPU'
   ```

2. **Lower Fire Resolution**: Edit `logo_animation.py`:
   ```python
   domain_settings.resolution_max = 128  # Instead of 256
   ```

3. **Render Overnight**: Use task scheduler or cron jobs

4. **Render in Parts**: Split frame range:
   ```bash
   blender -b file.blend -s 1 -e 100 -a
   blender -b file.blend -s 101 -e 200 -a
   blender -b file.blend -s 201 -e 300 -a
   ```

## Benefits of Python Workflow

✅ **Cross-platform**: Same commands on Windows/Linux/macOS
✅ **Automation-friendly**: Easy to integrate in scripts
✅ **No shell dependencies**: Pure Python + Blender
✅ **Extensible**: Easy to modify and customize
✅ **Pipeline-ready**: Perfect for render farms and CI/CD
✅ **Version control**: Python scripts are easy to track in git

## Next Steps

- Modify `scripts/animation_config.py` to add custom presets
- Edit `scripts/logo_animation.py` to change animation behavior
- Create your own render script with custom settings
- Integrate into your production pipeline

## Support

For more information:
- **README.md** - General project documentation
- **PROJECT_INFO.md** - Technical details
- **USAGE_EXAMPLES.md** - More examples
- **WINDOWS_INSTALL.md** - Windows-specific guide
