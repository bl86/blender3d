"""
Main runner script for Alter Logo Animation
Can be run from command line or inside Blender

Usage:
  Command line: blender --background --python run_animation.py
  Inside Blender: Load this script and run it (Alt+P)
"""

import sys
import os

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(script_dir, 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

# Import animation setup
from logo_animation import LogoAnimationSetup

def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("ALTER LOGO FIRE ANIMATION - Main Runner")
    print("=" * 70)
    print()

    # Setup paths
    project_root = script_dir
    svg_path = os.path.join(project_root, "alter.svg")
    output_path = os.path.join(project_root, "output")

    # Validate SVG exists
    if not os.path.exists(svg_path):
        print(f"ERROR: SVG file not found at {svg_path}")
        print("Please ensure alter.svg is in the project root directory")
        return False

    # Create output directory
    os.makedirs(output_path, exist_ok=True)

    print("Configuration:")
    print(f"  SVG Logo: {svg_path}")
    print(f"  Output: {output_path}")
    print(f"  Project Root: {project_root}")
    print()

    # Create and run animation setup
    print("Starting animation setup...")
    print("This will create a complete Blender scene with:")
    print("  • Golden logo with metallic material")
    print("  • Realistic fire simulation (Mantaflow)")
    print("  • Camera animation and tracking")
    print("  • Professional lighting setup")
    print("  • Compositing with bloom effects")
    print()

    try:
        animation = LogoAnimationSetup(svg_path, output_path)
        animation.setup_animation()

        print()
        print("=" * 70)
        print("SUCCESS! Animation setup complete!")
        print("=" * 70)
        print()
        print(f"Blend file saved: {os.path.join(project_root, 'alter_logo_animation.blend')}")
        print()
        print("Next steps:")
        print("  1. Open blend file in Blender")
        print("  2. Press SPACEBAR to preview animation")
        print("  3. Press F12 to render single frame")
        print("  4. Press Ctrl+F12 to render full animation")
        print()
        print("Or use render scripts:")
        print("  • render_preview.py - Fast preview (10 min)")
        print("  • render_production.py - High quality (45+ min)")
        print()
        return True

    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR: Animation setup failed!")
        print("=" * 70)
        print(f"\nError details: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run the setup
    success = main()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
