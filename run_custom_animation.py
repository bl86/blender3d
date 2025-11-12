"""
Custom animation setup with presets
Create animations with different styles and configurations

Usage:
  Command line: blender --background --python run_custom_animation.py -- [options]

Options:
  --timing PRESET       quick, standard, cinematic, extended
  --color PRESET        classic_gold, rose_gold, silver, platinum, bronze, white_gold
  --fire PRESET         subtle, moderate, intense, extreme
  --camera PRESET       standard, wide, telephoto, dramatic
  --lighting PRESET     studio, dramatic, soft, cinematic
  --render PRESET       preview, draft, production, ultra

Examples:
  blender --background --python run_custom_animation.py
  blender --background --python run_custom_animation.py -- --color rose_gold --fire intense
  blender --background --python run_custom_animation.py -- --timing cinematic --render ultra
"""

import sys
import os

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(script_dir, 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from advanced_setup import AdvancedAnimationSetup, parse_arguments
from animation_config import get_preset, print_presets


def main():
    """Main execution with preset support"""
    print("\n" + "=" * 70)
    print("CUSTOM ANIMATION SETUP - With Presets")
    print("=" * 70)
    print()

    # Parse arguments
    args = parse_arguments()

    # If list requested, show presets and exit
    if args.list:
        print_presets()
        return True

    # Setup paths
    project_root = script_dir
    svg_path = os.path.join(project_root, "alter.svg")
    output_path = os.path.join(project_root, "output")

    # Validate SVG
    if not os.path.exists(svg_path):
        print(f"ERROR: SVG file not found at {svg_path}")
        return False

    # Create output directory
    os.makedirs(output_path, exist_ok=True)

    # Load presets
    presets = {
        'timing': get_preset('timing', args.timing),
        'render': get_preset('render', args.render),
        'color': get_preset('color', args.color),
        'fire': get_preset('fire', args.fire),
        'camera': get_preset('camera', args.camera),
        'lighting': get_preset('lighting', args.lighting),
    }

    # Print configuration
    print("Selected presets:")
    print(f"  Timing:   {args.timing:15s} - {presets['timing']['description']}")
    print(f"  Render:   {args.render:15s} - {presets['render']['description']}")
    print(f"  Color:    {args.color:15s} - {presets['color']['description']}")
    print(f"  Fire:     {args.fire:15s} - {presets['fire']['description']}")
    print(f"  Camera:   {args.camera:15s} - {presets['camera']['description']}")
    print(f"  Lighting: {args.lighting:15s} - {presets['lighting']['description']}")
    print()

    try:
        # Create and run animation setup
        animation = AdvancedAnimationSetup(svg_path, output_path, presets)
        animation.setup_animation()

        # Save with preset info in filename
        import bpy
        blend_filename = f"alter_{args.timing}_{args.color}_{args.fire}.blend"
        blend_path = os.path.join(project_root, blend_filename)
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)

        print()
        print("=" * 70)
        print("CUSTOM ANIMATION COMPLETE!")
        print("=" * 70)
        print()
        print(f"Blend file saved: {blend_filename}")
        print()
        print("Animation settings:")
        print(f"  Total frames: {presets['timing']['total_frames']}")
        print(f"  Fire ends at: frame {presets['timing']['fire_end_frame']}")
        print(f"  Resolution: {presets['render']['resolution_x']}x{presets['render']['resolution_y']}")
        print(f"  Samples: {presets['render']['samples']}")
        print()
        print("To render:")
        print(f"  blender -b {blend_filename} --python render_production.py")
        print()

        return True

    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR: Setup failed!")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
