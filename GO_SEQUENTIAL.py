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
    print("  STARTING SEQUENTIAL ANIMATION GENERATION")
    print("=" * 70)
    print()
    print("This will create alternative version where:")
    print("  • Each logo element comes separately with fire")
    print("  • Elements PRESERVE original SVG layout positions")
    print("  • Only Y axis (depth) animates - toward camera")
    print("  • Treble key, wings, letters stay properly aligned")
    print("  • BANJA LUKA text positioned below logo")
    print("  • Fire follows contours of each element")
    print()
    print("⚡ OPTIMIZED FOR SPEED:")
    print("  • Resolution 128 (3-5x faster baking)")
    print("  • Uses ALL CPU cores")
    print("  • OptiX/CUDA for GPU rendering")
    print()
    print("⏱️  Estimated time: ~1-3 minutes (optimized baking)")
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
            print(f"   • alter_logo_sequential.blend")
            print()
            print("🎬 Next steps:")
            print("   1. Open in Blender:")
            print(f"      {blender} alter_logo_sequential.blend")
            print()
            print("   2. Preview animation:")
            print("      → Press SPACEBAR to see sequential entrance")
            print()
            print("   3. Render animation:")
            print("      → Press Ctrl+F12")
            print("      → Outputs to: output_sequential/seq_####.png")
            print()
            print("✨ Animation features:")
            print("   • Each element arrives separately with fire")
            print("   • PRESERVES original SVG layout (correct positions)")
            print("   • Fire follows contours of each element")
            print("   • Elements build up maintaining proper alignment")
            print("   • BANJA LUKA appears below logo at the end")
            print("   • Transparent background (ready for compositing)")
            print()
            print("⚡ Performance:")
            print("   • 3-5x faster baking (1-3 minutes)")
            print("   • ALL CPU cores utilized")
            print("   • OptiX/CUDA GPU acceleration")
            print()
            print("💡 Compare with alter_logo_fire_animation.blend!")
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
