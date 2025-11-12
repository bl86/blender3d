"""
SIMPLE START - Double-click to run animation!

This wrapper finds Blender and runs the animation scripts automatically.
No need to type commands - just run this file!

Usage:
  Double-click this file, or:
  python start.py
"""

import subprocess
import sys
import os
import platform


def find_blender():
    """Find Blender executable on system"""
    print("Looking for Blender...")

    # Try PATH first
    try:
        result = subprocess.run(
            ['blender', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Found Blender in PATH")
            return 'blender'
    except:
        pass

    # Platform-specific search
    system = platform.system()

    if system == 'Windows':
        # Search in Program Files
        base = r"C:\Program Files\Blender Foundation"
        if os.path.exists(base):
            # Find any Blender folder
            for folder in os.listdir(base):
                blender_path = os.path.join(base, folder, "blender.exe")
                if os.path.exists(blender_path):
                    print(f"✓ Found Blender: {blender_path}")
                    return blender_path

        # Try specific versions
        versions = ['4.5', '4.4', '4.3', '4.2', '4.1', '4.0', '3.6', '3.5', '3.4']
        for ver in versions:
            path = rf"C:\Program Files\Blender Foundation\Blender {ver}\blender.exe"
            if os.path.exists(path):
                print(f"✓ Found Blender {ver}")
                return path

    elif system == 'Darwin':  # macOS
        paths = [
            '/Applications/Blender.app/Contents/MacOS/Blender',
            os.path.expanduser('~/Applications/Blender.app/Contents/MacOS/Blender')
        ]
        for path in paths:
            if os.path.exists(path):
                print(f"✓ Found Blender: {path}")
                return path

    elif system == 'Linux':
        # Try common Linux paths
        paths = [
            '/usr/bin/blender',
            '/usr/local/bin/blender',
            os.path.expanduser('~/blender/blender')
        ]
        for path in paths:
            if os.path.exists(path):
                print(f"✓ Found Blender: {path}")
                return path

    print("✗ Blender not found!")
    print("\nPlease install Blender from: https://www.blender.org/download/")
    print("\nOr specify the path manually:")
    print("  python start.py /path/to/blender")
    return None


def print_menu():
    """Print menu options"""
    print("\n" + "=" * 60)
    print("  ALTER LOGO ANIMATION - Quick Start")
    print("=" * 60)
    print()
    print("What would you like to do?")
    print()
    print("  1. Make Animation (All-in-One) - RECOMMENDED")
    print("     → Generates scene + renders animation")
    print("     → Takes ~45 minutes")
    print()
    print("  2. Quick Preview (Fast)")
    print("     → Generates + renders preview quality")
    print("     → Takes ~10 minutes")
    print()
    print("  3. Just Generate Scene")
    print("     → Creates .blend file only")
    print("     → You can open it in Blender later")
    print()
    print("  4. Custom Animation (Advanced)")
    print("     → Choose colors, fire intensity, etc.")
    print()
    print("  0. Exit")
    print()


def run_blender_script(blender_exe, script_name, args=None):
    """Run a Python script through Blender"""
    cmd = [blender_exe, '--background', '--python', script_name]

    if args:
        cmd.append('--')
        cmd.extend(args)

    print(f"\nRunning: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running Blender: {e}")
        return False


def main():
    """Main menu and execution"""
    # Check if Blender path was provided as argument
    if len(sys.argv) > 1:
        blender_exe = sys.argv[1]
        if not os.path.exists(blender_exe):
            print(f"Error: Blender not found at {blender_exe}")
            return 1
    else:
        blender_exe = find_blender()
        if not blender_exe:
            return 1

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print_menu()

        try:
            choice = input("Enter your choice (0-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            return 0

        if choice == '0':
            print("\nGoodbye!")
            return 0

        elif choice == '1':
            # All-in-one
            print("\n" + "=" * 60)
            print("  ALL-IN-ONE ANIMATION")
            print("=" * 60)
            print("\nThis will generate the scene and render the animation.")
            print("Estimated time: ~45 minutes")
            print()
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm == 'y':
                script = os.path.join(script_dir, 'make_animation.py')
                success = run_blender_script(blender_exe, script)
                if success:
                    print("\n✓ Animation complete!")
                    print("Check the 'output' folder for your files.")
                else:
                    print("\n✗ Animation failed. Check errors above.")
                input("\nPress Enter to continue...")

        elif choice == '2':
            # Quick preview
            print("\n" + "=" * 60)
            print("  QUICK PREVIEW")
            print("=" * 60)
            print("\nThis will generate and render a quick preview.")
            print("Estimated time: ~10 minutes")
            print()
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm == 'y':
                script = os.path.join(script_dir, 'make_animation.py')
                success = run_blender_script(blender_exe, script, ['--quick'])
                if success:
                    print("\n✓ Preview complete!")
                    print("Check the 'output' folder for your files.")
                else:
                    print("\n✗ Preview failed. Check errors above.")
                input("\nPress Enter to continue...")

        elif choice == '3':
            # Just generate scene
            print("\n" + "=" * 60)
            print("  GENERATE SCENE")
            print("=" * 60)
            print("\nThis will create the .blend file.")
            print("You can open it in Blender later.")
            print()
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm == 'y':
                script = os.path.join(script_dir, 'run_animation.py')
                success = run_blender_script(blender_exe, script)
                if success:
                    print("\n✓ Scene generated!")
                    print("Open 'alter_logo_animation.blend' in Blender")
                else:
                    print("\n✗ Scene generation failed. Check errors above.")
                input("\nPress Enter to continue...")

        elif choice == '4':
            # Custom animation
            print("\n" + "=" * 60)
            print("  CUSTOM ANIMATION")
            print("=" * 60)
            print()
            print("Available options:")
            print("  Colors: classic_gold, rose_gold, silver, platinum, bronze, white_gold")
            print("  Fire: subtle, moderate, intense, extreme")
            print("  Timing: quick (5s), standard (10s), cinematic (18s), extended (20s)")
            print()

            color = input("Color (default: classic_gold): ").strip() or "classic_gold"
            fire = input("Fire intensity (default: intense): ").strip() or "intense"
            timing = input("Timing (default: standard): ").strip() or "standard"

            args = [
                '--color', color,
                '--fire', fire,
                '--timing', timing
            ]

            script = os.path.join(script_dir, 'run_custom_animation.py')
            success = run_blender_script(blender_exe, script, args)
            if success:
                print("\n✓ Custom animation created!")
                print(f"Blend file: alter_{timing}_{color}_{fire}.blend")
            else:
                print("\n✗ Custom animation failed. Check errors above.")
            input("\nPress Enter to continue...")

        else:
            print("\nInvalid choice. Please enter 0-4.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
