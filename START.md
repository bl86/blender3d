# 🚀 QUICK START GUIDE

## Simplest Way - Just Double-Click!

### Windows / Linux / macOS:
1. **Double-click** `GO.py`
2. Wait ~1-2 minutes
3. Done! Scene created: `alter_logo_fire_animation.blend`

### Alternative - Menu Options:
1. **Double-click** `start.py`
2. Choose what you want to do
3. Follow the prompts

## That's It!

The scripts will:
- ✅ Find Blender automatically (even 4.5+)
- ✅ Find and import your alter.svg logo
- ✅ Create fire simulation around logo
- ✅ Generate complete animation scene

## Files Explained

| File | What It Does | When To Use |
|------|--------------|-------------|
| **GO.py** | Creates scene automatically (1-2 min) | When you want the fastest setup |
| **start.py** | Interactive menu with options | When you want to choose generation/rendering/custom |
| **ALTER_LOGO_COMPLETE.py** | Single-file Blender script | Run directly in Blender's Scripting tab |

## Troubleshooting

### "Blender not found"
**Solution:** Install Blender from https://www.blender.org/download/

### "alter.svg not found"
**Solution:** Make sure `alter.svg` is in the same folder as GO.py

### "Permission denied" (Linux/Mac)
**Solution:**
```bash
chmod +x GO.py start.py
python3 GO.py
```

### Want faster preview?
Use `start.py` and choose option 2 (Quick Preview)

## Advanced Users

If you want to run specific scripts directly:

```bash
# Complete scene with fire (RECOMMENDED - uses exact SVG)
blender --background --python ALTER_LOGO_COMPLETE.py

# All-in-one with rendering
blender --background --python make_animation.py

# Quick preview
blender --background --python make_animation.py -- --quick

# Custom colors/fire
blender --background --python run_custom_animation.py -- --color rose_gold --fire intense
```

See [PYTHON_WORKFLOW.md](PYTHON_WORKFLOW.md) for all options.

### Run in Blender GUI

1. Open Blender
2. Go to **Scripting** tab
3. Click **Open** → Select `ALTER_LOGO_COMPLETE.py`
4. Click **Run Script** (or Alt+P)
5. Done! Scene is ready to preview

## Output

**After running GO.py or start.py option 1:**
- `alter_logo_fire_animation.blend` - Complete scene with fire simulation
- Ready to open and preview in Blender

**After rendering (start.py option 2 or manual render):**
- `output/production_*.png` - Rendered frames (300 files)
- `output/alter_animation_production.mp4` - Video (if you use create_video.py)

## Next Steps

1. **Preview Animation:**
   - Open `alter_logo_fire_animation.blend` in Blender
   - Press SPACEBAR in viewport to play
   - See the logo move forward with fire!

2. **Render Full Quality:**
   - In Blender: Press Ctrl+F12
   - Or from command line:
   ```bash
   blender -b alter_logo_fire_animation.blend -a
   ```

3. **Create Video from Frames:**
   ```bash
   python start.py
   # Choose option 2 (All-in-One)
   ```

4. **Customize:**
   - Edit colors, fire intensity, timing
   - Use `start.py` → Option 5 (Custom)

## Time Estimates

| Task | Time (any GPU) | Time (CPU only) |
|------|----------------|-----------------|
| **Generate Scene** (GO.py) | ~1-2 min | ~1-2 min |
| **Render Preview** (option 3) | ~10 min | ~1 hour |
| **Render Production** (option 2) | ~45 min | ~6 hours |

*Scene generation is fast - rendering takes time!*

## Need Help?

- **General guide:** README.md
- **Python workflow:** PYTHON_WORKFLOW.md
- **Windows specific:** WINDOWS_INSTALL.md
- **Technical details:** PROJECT_INFO.md
- **Examples:** USAGE_EXAMPLES.md

---

**TL;DR: Double-click GO.py, wait 1-2 minutes, open .blend file in Blender!** 🎉

The scene includes:
- ✨ Golden metallic ALTER logo (from your exact SVG)
- 🔥 Realistic fire simulation (fades at frame 200)
- 📹 Professional camera tracking
- 💡 3-point lighting setup
- 🎬 300 frames (10 seconds at 30 fps)
