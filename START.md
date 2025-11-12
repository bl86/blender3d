# 🚀 QUICK START GUIDE

## Simplest Way - Just Double-Click!

### Windows:
1. **Double-click** `GO.py`
2. Wait ~45 minutes
3. Done! Check `output/` folder

### Alternative - Menu Options:
1. **Double-click** `start.py`
2. Choose what you want to do
3. Follow the prompts

## That's It!

The scripts will:
- ✅ Find Blender automatically
- ✅ Generate the animation scene
- ✅ Render everything
- ✅ Save to `output/` folder

## Files Explained

| File | What It Does | When To Use |
|------|--------------|-------------|
| **GO.py** | Does everything automatically | When you want it simple - just run and wait |
| **start.py** | Interactive menu with options | When you want to choose preview/production/custom |

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
# All-in-one (recommended)
blender --background --python make_animation.py

# Quick preview
blender --background --python make_animation.py -- --quick

# Custom colors/fire
blender --background --python run_custom_animation.py -- --color rose_gold --fire intense
```

See [PYTHON_WORKFLOW.md](PYTHON_WORKFLOW.md) for all options.

## Output

After running, you'll find:
- `alter_logo_animation.blend` - Blender scene file
- `output/production_*.png` - Rendered frames (300 files)
- `output/alter_animation_production.mp4` - Video (if you chose that option)

## Next Steps

1. **View Animation:**
   - Open `alter_logo_animation.blend` in Blender
   - Press SPACEBAR to play

2. **Create Video from Frames:**
   ```bash
   python start.py
   # Choose option for video creation
   ```

3. **Customize:**
   - Edit colors, fire intensity, timing
   - Use `start.py` → Option 4 (Custom)

## Time Estimates

| Quality | Resolution | Time (RTX 3080) | Time (GTX 1080) | Time (CPU) |
|---------|------------|-----------------|-----------------|------------|
| Quick | 720p | ~10 min | ~15 min | ~1 hour |
| Production | 1080p | ~45 min | ~90 min | ~6 hours |

## Need Help?

- **General guide:** README.md
- **Python workflow:** PYTHON_WORKFLOW.md
- **Windows specific:** WINDOWS_INSTALL.md
- **Technical details:** PROJECT_INFO.md
- **Examples:** USAGE_EXAMPLES.md

---

**TL;DR: Double-click GO.py and wait. That's it!** 🎉
