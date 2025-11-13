"""
DOUBLE-CLICK TO START SEQUENTIAL ANIMATION!

This creates the alternative version where:
- Treble key and each letter comes separately
- Each element has its own fire
- BANJA LUKA comes at the end
"""

import subprocess
import sys
import os
import platform


def find_blender():
    """Find Blender installation"""
    # Try PATH
    try:
        result = subprocess.run(['blender', '--version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            return 'blender'
    except:
        pass

    system = platform.system()

    if system == 'Windows':
        base = r"C:\Program Files\Blender Foundation"
        if os.path.exists(base):
            for folder in os.listdir(base):
                path = os.path.join(base, folder, "blender.exe")
                if os.path.exists(path):
                    return path

    elif system == 'Darwin':
        paths = ['/Applications/Blender.app/Contents/MacOS/Blender']
        for path in paths:
            if os.path.exists(path):
                return path

    elif system == 'Linux':
        paths = ['/usr/bin/blender', '/usr/local/bin/blender']
        for path in paths:
            if os.path.exists(path):
                return path

    return None


def main():
    """Run sequential animation generation"""
    print("=" * 70)
    print(" " * 15 + "ALTER LOGO SEQUENTIAL ANIMATION")
    print("=" * 70)
    print()

    # Check for alter.svg
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, 'alter.svg')

    print("🔍 Checking for alter.svg...")
    if not os.path.exists(svg_path):
        print()
        print("❌ ERROR: alter.svg not found!")
        print(f"Expected location: {svg_path}")
        print()
        input("Press Enter to exit...")
        return 1

    print(f"✓ Found alter.svg: {svg_path}")
    print()

    print("🔍 Looking for Blender...")
    blender = find_blender()

    if not blender:
        print()
        print("❌ ERROR: Blender not found!")
        print("Install from: https://www.blender.org/download/")
        print()
        input("Press Enter to exit...")
        return 1

    print(f"✓ Found Blender: {blender}")
    print()
    print("=" * 70)
    print("  STARTING SEQUENTIAL ANIMATION GENERATION (V2)")
    print("=" * 70)
    print()
    print("This will create sequential version where:")
    print("  • Each logo element comes separately with fire")
    print("  • Elements PRESERVE EXACT original SVG layout positions")
    print("  • Animation goes TOWARD camera (from far to near)")
    print("  • X and Z coordinates NEVER change - stay aligned")
    print("  • BANJA LUKA text positioned below logo")
    print()
    print("🔥 FIRE - FLUID SIMULATION:")
    print("  • FLUID fire (Mantaflow) - same as ALTER_LOGO_COMPLETE.py")
    print("  • Fire ONLY in LAST 2 SECONDS of animation")
    print("  • Principled Volume shader for realistic fire")
    print("  • Resolution: 256 for high quality")
    print("  • NOTE: Requires baking in Blender before rendering")
    print()
    print("🎨 ALPHA CHANNEL:")
    print("  • Transparent background (film transparent enabled)")
    print("  • PNG output with RGBA")
    print("  • Ready for compositing in Premiere Pro")
    print()
    print("⚡ RENDERING:")
    print("  • OptiX/CUDA GPU rendering")
    print("  • Uses ALL CPU cores")
    print("  • Output: ./output/frame_####.png")
    print()
    print("⏱️  Setup time: ~1 minute (then baking required)")
    print()
    print("Starting in 3 seconds...")
    print("(Press Ctrl+C to cancel)")
    print()

    try:
        import time
        time.sleep(3)
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        return 0

    # Run ALTER_LOGO_SEQUENTIAL.py through Blender
    script_path = os.path.join(script_dir, 'ALTER_LOGO_SEQUENTIAL.py')

    cmd = [blender, '--background', '--python', script_path]

    print("Running...")
    print()

    try:
        result = subprocess.run(cmd)

        print()
        if result.returncode == 0:
            print("=" * 70)
            print(" " * 25 + "🎉 SUCCESS! 🎉")
            print("=" * 70)
            print()
            print("Your sequential animation is ready!")
            print()
            print("📂 Generated file:")
            print(f"   • alter_logo_sequential_v2.blend")
            print()
            print("🎬 Next steps (IMPORTANT - READ CAREFULLY):")
            print()
            print("   1. Open in Blender:")
            print(f"      {blender} alter_logo_sequential_v2.blend")
            print()
            print("   2. BAKE fluid simulation (REQUIRED):")
            print("      → Press SPACEBAR to play animation")
            print("      → Blender will bake fire simulation automatically")
            print("      → Wait for baking to complete (check timeline progress)")
            print("      → Fire will appear during last 2 seconds only")
            print()
            print("   3. Preview animation:")
            print("      → Press 'Z' key, select 'Rendered' mode")
            print("      → Fire should be visible during last 2 seconds")
            print()
            print("   4. Render animation:")
            print("      → Press Ctrl+F12 (after baking completes)")
            print("      → Outputs to: ./output/frame_####.png (PNG with alpha)")
            print()
            print("✨ Animation features:")
            print("   • Elements PRESERVE EXACT SVG positions (X,Z)")
            print("   • Only Y axis animates TOWARD camera (far to near)")
            print("   • X and Z stay LOCKED at original positions")
            print("   • Each element arrives separately with fire")
            print("   • Fire = FLUID simulation (Mantaflow)")
            print("   • Fire ONLY in last 2 seconds, then blank")
            print("   • BANJA LUKA appears below logo at the end")
            print("   • TRANSPARENT background (alpha channel)")
            print()
            print("🔥 Fire technology:")
            print("   • FLUID simulation (same as ALTER_LOGO_COMPLETE.py)")
            print("   • Principled Volume shader for realistic fire")
            print("   • Fire timed to last 2 seconds only")
            print("   • Resolution: 256 (high quality)")
            print()
            print("💡 Ready for Premiere Pro compositing!")
            print()
        else:
            print("=" * 70)
            print(" " * 25 + "❌ FAILED")
            print("=" * 70)
            print()
            print("Something went wrong. Check errors above.")
            print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 0
    except Exception as e:
        print(f"\n\nError: {e}")
        return 1

    input("\nPress Enter to exit...")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
