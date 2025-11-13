# Windows Installation & Setup Guide

Complete guide for setting up and running the Alter Logo Animation on Windows.

## Prerequisites

### 1. Install Blender

**Download Blender:**
- Visit: https://www.blender.org/download/
- Download latest version (3.6+ recommended, 4.0+ supported)
- Choose "Windows Installer (.msi)" for easiest installation

**Installation:**
1. Run the installer
2. Accept default installation path: `C:\Program Files\Blender Foundation\Blender X.X\`
3. Check "Add to PATH" option if available (recommended)
4. Complete installation

**Verify Installation:**
Open Command Prompt and type:
```cmd
blender --version
```

If you see version info, Blender is correctly installed.

### 2. Install Python (Optional)

Python comes with Blender, but for running check scripts separately:

- Download from: https://www.python.org/downloads/
- Install Python 3.9 or higher
- Check "Add Python to PATH" during installation

### 3. Enable GPU Rendering (Recommended)

For NVIDIA GPUs:
1. Download latest drivers from: https://www.nvidia.com/drivers
2. In Blender: Edit → Preferences → System → Cycles Render Devices
3. Select CUDA or OptiX
4. Check your GPU in the list

For AMD GPUs:
1. Download latest drivers from: https://www.amd.com/drivers
2. In Blender: Edit → Preferences → System → Cycles Render Devices
3. Select HIP (if available in your Blender version)
4. Check your GPU in the list

## Running the Animation

### Method 1: Batch Script (Easiest)

1. Open File Explorer
2. Navigate to project folder
3. Double-click `quickstart.bat`
4. Follow on-screen instructions

### Method 2: Command Prompt

```cmd
cd path\to\blender3d
quickstart.bat
```

### Method 3: PowerShell

```powershell
cd path\to\blender3d
.\quickstart.ps1
```

**Note:** If you get "execution policy" error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Method 4: Manual Steps

**Generate Scene:**
```cmd
cd path\to\blender3d
scripts\setup_scene.bat
```

**Open in Blender:**
```cmd
blender alter_logo_animation.blend
```

**Render:**
```cmd
scripts\render_animation.bat production
```

## Troubleshooting

### "Blender is not recognized"

**Solution 1 - Add to PATH:**
1. Press `Win + X`, select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find and select "Path"
5. Click "Edit"
6. Click "New"
7. Add: `C:\Program Files\Blender Foundation\Blender 3.6\`
8. Click OK on all dialogs
9. **Restart Command Prompt**

**Solution 2 - Use Full Path:**
Edit batch scripts to use full path:
```cmd
"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" --background --python scripts\logo_animation.py
```

### Python Not Found

If `check_system.py` doesn't run:
1. Install Python from python.org
2. Or use Blender's Python:
```cmd
"C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin\python.exe" scripts\check_system.py
```

### Permission Denied

**Solution 1:**
Right-click script → **Run as administrator**

**Solution 2:**
Move project to non-protected location (e.g., `C:\Users\YourName\Documents\blender3d`)

### Slow Rendering

1. **Enable GPU:**
   - In Blender: Edit → Preferences → System
   - Cycles Render Devices → Select CUDA/OptiX/HIP
   - Check your GPU

2. **Use Preview Mode:**
```cmd
scripts\render_animation.bat preview
```

3. **Reduce Settings:**
   - Open .blend file in Blender
   - Render Properties → Samples → Lower to 128

### Out of Disk Space

The project needs ~5GB for:
- Fluid simulation cache: ~2-3GB
- Rendered frames: ~1-2GB
- Working files: ~500MB

**Free up space:**
1. Delete old caches: Delete `blendcache_*` folders
2. Delete old renders: Delete files in `output\` folder
3. Move project to drive with more space

### Fire Not Appearing

1. **Bake Fluid Cache:**
   - Open .blend file
   - Select FireDomain object
   - Physics Properties → Fluid → Cache
   - Click "Bake All"
   - Wait for completion (5-15 minutes)

2. **Check Visibility:**
   - Click eye icon next to FireDomain in Outliner
   - In viewport shading, switch to "Rendered" mode (Z key → select Rendered)

### GPU Rendering Not Working

**For NVIDIA Cards:**
1. Update GPU drivers
2. Install CUDA Toolkit (optional): https://developer.nvidia.com/cuda-downloads
3. In Blender Preferences, select OptiX (newer) or CUDA

**For AMD Cards:**
1. Update GPU drivers
2. Blender 3.3+ required for HIP support
3. May have limited support compared to NVIDIA

**For Intel iGPU:**
- Integrated graphics are much slower
- Recommended to use CPU rendering instead
- Or render on a machine with discrete GPU

## Performance Tips

### Faster Preview Rendering
```cmd
scripts\render_animation.bat preview
```
- 64 samples instead of 256
- 720p instead of 1080p
- ~4x faster

### Render Specific Frame Range
```cmd
blender -b alter_logo_animation.blend -s 1 -e 100 -a
```
Renders only frames 1-100

### Test Single Frame
```cmd
blender -b alter_logo_animation.blend -f 150 -o output\test.png
```
Renders only frame 150

### Background Rendering (Free Up PC)
Use Task Scheduler to render during off-hours:
1. Open Task Scheduler
2. Create Basic Task
3. Action: Start a program
4. Program: `blender`
5. Arguments: `-b "C:\path\to\alter_logo_animation.blend" -a`
6. Schedule for night/weekend

## Advanced Usage

### Custom Presets (Windows)

```cmd
blender --background --python scripts\advanced_setup.py -- --timing cinematic --color rose_gold --fire intense
```

### Render Quality Comparison

| Quality | Command | Samples | Time (RTX 3080) |
|---------|---------|---------|-----------------|
| Preview | `render_animation.bat preview` | 64 | ~10 min |
| Production | `render_animation.bat production` | 256 | ~45 min |
| Ultra | Manual (see below) | 512 | ~2 hours |

**Ultra Quality (Manual):**
```cmd
blender -b alter_logo_animation.blend --python-expr "import bpy; bpy.context.scene.cycles.samples = 512" -a
```

## Batch Operations

### Render Multiple Variants
Create `render_all.bat`:
```batch
@echo off
blender --background --python scripts\advanced_setup.py -- --color classic_gold --fire intense
scripts\render_animation.bat production

blender --background --python scripts\advanced_setup.py -- --color rose_gold --fire moderate
scripts\render_animation.bat production

blender --background --python scripts\advanced_setup.py -- --color silver --fire subtle
scripts\render_animation.bat production

echo All renders complete!
pause
```

## File Locations

### Default Paths
- **Blender Executable**: `C:\Program Files\Blender Foundation\Blender X.X\blender.exe`
- **Blender Python**: `C:\Program Files\Blender Foundation\Blender X.X\X.X\python\bin\python.exe`
- **Project Root**: Where you extracted/cloned the repository
- **Output Files**: `[Project Root]\output\`
- **Cache Files**: `[Project Root]\blendcache_alter_logo_animation\`

### Moving Project
You can move the entire `blender3d` folder anywhere:
- `C:\Users\[Username]\Documents\blender3d\` ✓ Recommended
- `D:\Projects\blender3d\` ✓ Good for storage
- `C:\Program Files\blender3d\` ✗ Needs admin rights

## Video Editing (Post-Processing)

After rendering, you can:

### Add Audio (using FFmpeg)
Download FFmpeg: https://ffmpeg.org/download.html

```cmd
ffmpeg -i output\alter_logo_animation_0001.png -i music.mp3 -c:v libx264 -c:a aac final.mp4
```

### Re-encode for Social Media
**Instagram/TikTok:**
```cmd
ffmpeg -i output\render.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy vertical.mp4
```

**Twitter/X:**
```cmd
ffmpeg -i output\render.mp4 -vf "scale=1280:720" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 192k twitter.mp4
```

## Support & Resources

- **Blender Manual**: https://docs.blender.org/manual/en/latest/
- **Blender Artists Forum**: https://blenderartists.org/
- **r/blender**: https://reddit.com/r/blender
- **Project Issues**: Check PROJECT_INFO.md and USAGE_EXAMPLES.md

## Quick Reference Commands

```cmd
REM Full workflow
quickstart.bat

REM Individual steps
scripts\setup_scene.bat
blender alter_logo_animation.blend
scripts\render_animation.bat production

REM System check only
python scripts\check_system.py

REM Preview animation (no render)
blender alter_logo_animation.blend

REM Background render (no GUI)
blender -b alter_logo_animation.blend -a

REM Render frame 150 only
blender -b alter_logo_animation.blend -f 150

REM Custom quality
blender -b alter_logo_animation.blend --python-expr "import bpy; bpy.context.scene.cycles.samples=128" -a
```

---

**Need Help?**
- Check README.md for general usage
- Check USAGE_EXAMPLES.md for practical examples
- Check PROJECT_INFO.md for technical details
