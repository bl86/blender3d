# Project Technical Documentation

## Architecture Overview

This project implements a production-ready Blender animation pipeline with modular, reusable components.

### Core Components

#### 1. Logo Animation System (`logo_animation.py`)
Main animation setup class handling:
- SVG import and mesh conversion
- Material creation (Principled BSDF shader network)
- Physics simulation (Mantaflow fluid dynamics)
- Camera tracking and animation
- Lighting rig setup
- Compositing node graph
- Render configuration

**Key Methods:**
```python
LogoAnimationSetup.setup_animation()  # Main entry point
LogoAnimationSetup.create_fire_simulation()  # Mantaflow setup
LogoAnimationSetup.create_golden_material()  # PBR material
```

#### 2. Configuration System (`animation_config.py`)
Preset management for:
- Timing (frames, FPS)
- Render quality (samples, resolution)
- Material colors (PBR parameters)
- Fire intensity (fuel, temperature)
- Camera settings (lens, DOF)
- Lighting (energy levels)

#### 3. Advanced Setup (`advanced_setup.py`)
Extended setup with CLI arguments for preset selection. Inherits from `LogoAnimationSetup` and overrides methods to apply presets.

### Animation Pipeline

```
SVG Import → Mesh Conversion → Material Assignment
     ↓
Camera Setup → Animation Keyframes
     ↓
Fire Domain → Emitter → Flow Settings
     ↓
Lighting Rig → 3-Point Setup
     ↓
Compositing → Bloom + Color Grade
     ↓
Render Settings → Cycles Configuration
     ↓
Output → MP4 Video
```

## Technical Specifications

### Render Engine: Cycles
- **Path Tracing**: Physically accurate light transport
- **GPU Acceleration**: CUDA/OptiX for NVIDIA, HIP for AMD
- **Adaptive Sampling**: Automatic noise reduction
- **Denoising**: OpenImageDenoise AI denoiser

### Fire Simulation: Mantaflow
- **Solver**: Pressure-based Navier-Stokes
- **Grid Resolution**: 256³ voxels (adjustable)
- **Domain Type**: Gas (smoke + fire)
- **Flow Type**: Inflow with initial velocity
- **Physics**:
  - Buoyancy (alpha: 1.0, beta: 1.5)
  - Vorticity: 0.3
  - Dissolve speed: 5
  - Flame smoke: 1.0

### Shader Networks

#### Golden Material
```
Principled BSDF (Metallic: 1.0, Roughness: 0.15)
    ├── Base Color: (1.0, 0.766, 0.336) RGB
    ├── Metallic: 1.0
    ├── Roughness: 0.15
    └── Anisotropic: 0.3
        ↓
Mix Shader (95% BSDF, 5% Emission)
    └── Emission (Strength: 0.3)
        ↓
Material Output
```

#### Fire Material
```
Attribute (flame) → Color Ramp → Emission
                                    ↓
Attribute (density) → Volume Scatter → Add Shader
                                         ↓
                     Volume Absorption ──┘
                                         ↓
                                  Volume Output
```

### Compositing Graph
```
Render Layers
    ├── Image → Glare (Fog Glow) ──┐
    │                                ├→ Mix (Add) → Color Correction
    └────────────────────────────────┘                  ↓
                                              Lens Distortion
                                                      ↓
                                                  Composite
```

## Performance Optimization

### GPU Rendering
Enable in Blender Preferences:
```
Edit → Preferences → System → Cycles Render Devices
Select: CUDA (NVIDIA) or HIP (AMD) or Metal (Apple Silicon)
```

### Memory Management
- **Tile Size**: Auto (optimal for GPU)
- **Volume Sampling**: 0.5 step rate
- **Max Steps**: 1024 (prevents infinite loops)
- **Cache**: Modular fluid cache (can be cleared between renders)

### Render Time Estimates

**Production Quality (256 samples, 1080p, 300 frames):**
- RTX 4090: ~30 minutes
- RTX 3080: ~45 minutes
- RTX 2080 Ti: ~75 minutes
- GTX 1080: ~120 minutes
- CPU (16 cores): ~6 hours

**Preview Quality (64 samples, 720p, 300 frames):**
- Any modern GPU: ~10-15 minutes

## API Usage

### Basic Setup
```python
from logo_animation import LogoAnimationSetup

animation = LogoAnimationSetup(
    svg_path="/path/to/logo.svg",
    output_path="/path/to/output"
)
animation.setup_animation()
```

### Advanced Setup with Presets
```python
from advanced_setup import AdvancedAnimationSetup
from animation_config import get_preset

presets = {
    'timing': get_preset('timing', 'cinematic'),
    'render': get_preset('render', 'ultra'),
    'color': get_preset('color', 'rose_gold'),
    'fire': get_preset('fire', 'extreme'),
}

animation = AdvancedAnimationSetup(
    svg_path="/path/to/logo.svg",
    output_path="/path/to/output",
    presets=presets
)
animation.setup_animation()
```

### Custom Presets
```python
from animation_config import COLOR_PRESETS

# Add custom color
COLOR_PRESETS['custom_copper'] = {
    'base_color': (0.72, 0.45, 0.20, 1.0),
    'emission_color': (0.9, 0.55, 0.25, 1.0),
    'emission_strength': 0.4,
    'roughness': 0.2,
    'description': 'Custom copper finish'
}
```

## File Formats

### Input
- **SVG**: Vector logo (prefer paths over text)
- **Resolution**: Any (vector scales infinitely)
- **Compatibility**: Inkscape-compatible SVG 1.1

### Output
- **Video**: MP4/H.264, 30fps, 1920x1080
- **Images**: PNG sequence (optional)
- **Codec**: H.264 High Profile
- **Container**: MP4/MPEG-4

### Cache
- **Location**: `blendcache_*/`
- **Format**: OpenVDB + proprietary
- **Size**: ~2-5 GB for 300 frames at 256 resolution
- **Cleanup**: Safe to delete (will rebake on next render)

## Extending the System

### Adding New Presets

Edit `animation_config.py`:
```python
TIMING_PRESETS['custom'] = {
    'total_frames': 450,
    'fire_end_frame': 300,
    'fps': 60,
    'description': 'My custom timing'
}
```

### Modifying Fire Behavior

Override `create_fire_simulation()`:
```python
class CustomAnimationSetup(LogoAnimationSetup):
    def create_fire_simulation(self):
        domain, emitter = super().create_fire_simulation()

        # Custom modifications
        domain_settings = domain.modifiers["Fluid"].domain_settings
        domain_settings.use_noise = True
        domain_settings.noise_strength = 2.0

        return domain, emitter
```

### Adding Effects

Add to `setup_compositing()`:
```python
# Add lens flare
flare = nodes.new(type='CompositorNodeLensdist')
flare.location = (400, -200)
flare.inputs['Distort'].default_value = 0.05
```

## Troubleshooting

### Common Issues

**Issue**: Fire not visible in render
**Solution**:
1. Check domain viewport display (eye icon)
2. Bake fluid cache: Domain → Cache → Bake All
3. Verify fire material assigned to domain

**Issue**: Out of GPU memory
**Solution**:
1. Reduce domain resolution (128 instead of 256)
2. Lower render samples (128 instead of 256)
3. Enable adaptive sampling
4. Reduce resolution percentage

**Issue**: Slow fluid baking
**Solution**:
1. Reduce domain resolution
2. Decrease time scale (0.5 instead of 1.0)
3. Reduce noise resolution
4. Use "Replay" cache type instead of "Modular"

**Issue**: Logo not importing correctly
**Solution**:
1. Open SVG in Inkscape
2. Convert text to paths: Path → Object to Path
3. Ungroup all: Object → Ungroup (Ctrl+Shift+G)
4. Save as Plain SVG

### Debug Mode

Enable verbose output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Profiling

Time each setup stage:
```python
import time

start = time.time()
animation.import_svg_logo()
print(f"Import: {time.time() - start:.2f}s")

start = time.time()
animation.create_fire_simulation()
print(f"Fire setup: {time.time() - start:.2f}s")
```

## Dependencies

### Required
- Blender 3.0+ (bundled Python 3.10+)
- OpenImageDenoise (included with Blender)

### Optional
- NVIDIA CUDA Toolkit (for GPU rendering)
- AMD ROCm (for AMD GPU rendering)
- Intel oneAPI (for Intel GPU rendering)

### Python Packages
All required packages included with Blender:
- `bpy` - Blender Python API
- `mathutils` - Vector/Matrix operations
- `os`, `sys`, `math` - Standard library

## License & Attribution

This is a professional animation pipeline. Code follows PEP 8 style guidelines and Blender API best practices.

**Blender Version Compatibility:**
- Tested: 3.3, 3.4, 3.5, 3.6, 4.0
- Minimum: 3.0 (Mantaflow required)

**API References:**
- Blender Python API: https://docs.blender.org/api/
- Mantaflow: http://mantaflow.com/
- Cycles: https://www.cycles-renderer.org/
