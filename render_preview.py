"""
Quick preview render script - Fast rendering with lower quality
Perfect for testing and previewing animation

Usage:
  Command line: blender -b alter_logo_animation.blend --python render_preview.py
  Or: blender alter_logo_animation.blend --python render_preview.py (with GUI)
"""

import bpy
import os
import sys

def main():
    """Setup and render preview quality"""
    print("\n" + "=" * 70)
    print("PREVIEW RENDER - Fast Quality")
    print("=" * 70)
    print()

    scene = bpy.context.scene

    # Preview settings - optimized for speed
    print("Configuring preview settings:")
    print("  • Samples: 64 (fast)")
    print("  • Resolution: 50% (720p)")
    print("  • Denoising: Enabled")
    print()

    # Render settings
    scene.cycles.samples = 64
    scene.render.resolution_percentage = 50
    scene.cycles.use_denoising = True

    # Ensure output is set
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    scene.render.filepath = os.path.join(output_dir, "preview_")

    print(f"Output directory: {output_dir}")
    print(f"Output pattern: preview_####.png")
    print()
    print("Starting render...")
    print("Estimated time: ~10-15 minutes on modern GPU")
    print("Frames: 1-300 (10 seconds at 30fps)")
    print()

    # Render animation
    bpy.ops.render.render(animation=True)

    print()
    print("=" * 70)
    print("PREVIEW RENDER COMPLETE!")
    print("=" * 70)
    print(f"\nOutput files: {output_dir}/preview_*.png")
    print()


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR: Render failed!")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
