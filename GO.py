"""
DOUBLE-CLICK TO START!

This is the SIMPLEST way to run the animation.
Just double-click this file and wait!

No typing, no commands - it does everything automatically.
"""

import subprocess
import sys
import os
import platform


def find_blender():
    """Find Blender - same logic as start.py"""
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
    """Run animation automatically"""
    print("=" * 70)
    print(" " * 20 + "ALTER LOGO ANIMATION")
    print("=" * 70)
    print()

    # Check for alter.svg first
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, 'alter.svg')

    print("🔍 Checking for alter.svg...")
    if not os.path.exists(svg_path):
        print()
        print("❌ ERROR: alter.svg not found!")
        print()
        print(f"Expected location: {svg_path}")
        print()
        print("Please make sure alter.svg is in the same folder as this script.")
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
        print()
        print("Please install Blender from:")
        print("  https://www.blender.org/download/")
        print()
        print("After installation, run this script again.")
        print()
        input("Press Enter to exit...")
        return 1

    print(f"✓ Found Blender: {blender}")
    print()
    print("=" * 70)
    print("  STARTING ANIMATION GENERATION")
    print("=" * 70)
    print()
    print("This will:")
    print("  1. Find and import alter.svg")
    print("  2. Create golden metallic logo material")
    print("  3. Set up fire simulation around logo")
    print("  4. Generate complete animation scene (300 frames)")
    print()
    print("⏱️  Estimated time: ~1-2 minutes")
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

    # Run ALTER_LOGO_COMPLETE.py through Blender
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'ALTER_LOGO_COMPLETE.py')

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
            print("Your animation scene is ready!")
            print()
            print("📂 Generated file:")
            print(f"   • alter_logo_fire_animation.blend")
            print()
            print("🎬 Next steps:")
            print("   1. Open in Blender:")
            print(f"      {blender} alter_logo_fire_animation.blend")
            print()
            print("   2. Preview animation:")
            print("      → Press SPACEBAR in viewport")
            print()
            print("   3. Render animation:")
            print("      → Press Ctrl+F12 (or Render → Render Animation)")
            print()
            print("✨ The scene includes:")
            print("   • Golden metallic ALTER logo from SVG")
            print("   • Fire simulation (fades at frame 200)")
            print("   • Professional lighting and camera tracking")
            print("   • 300 frames (10 seconds at 30 fps)")
            print("   • 1920x1080 resolution, 128 samples")
            print()
        else:
            print("=" * 70)
            print(" " * 25 + "❌ FAILED")
            print("=" * 70)
            print()
            print("Something went wrong. Check the errors above.")
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
