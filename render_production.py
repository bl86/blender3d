"""
Production render script - High quality rendering
Use for final output and deliverables

Usage:
  Command line: blender -b alter_logo_animation.blend --python render_production.py
  Or: blender alter_logo_animation.blend --python render_production.py (with GUI)
"""

import bpy
import os
import sys

def main():
    """Setup and render production quality"""
    print("\n" + "=" * 70)
    print("PRODUCTION RENDER - High Quality")
    print("=" * 70)
    print()

    scene = bpy.context.scene

    # Production settings - high quality
    print("Configuring production settings:")
    print("  • Samples: 256 (high quality)")
    print("  • Resolution: 100% (1920x1080)")
    print("  • Denoising: Enabled")
    print("  • Motion blur: Enabled")
    print()

    # Render settings
    scene.cycles.samples = 256
    scene.render.resolution_percentage = 100
    scene.cycles.use_denoising = True
    scene.render.use_motion_blur = True

    # Ensure output is set
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    scene.render.filepath = os.path.join(output_dir, "production_")

    print(f"Output directory: {output_dir}")
    print(f"Output pattern: production_####.png")
    print()
    print("Starting render...")
    print("Estimated time: ~45-90 minutes on RTX 3080")
    print("                ~2-4 hours on GTX 1080")
    print("                ~6+ hours on CPU only")
    print()
    print("Frames: 1-300 (10 seconds at 30fps)")
    print()
    print("You can monitor progress in terminal output.")
    print("Press Ctrl+C to cancel if needed.")
    print()

    # Render animation
    bpy.ops.render.render(animation=True)

    print()
    print("=" * 70)
    print("PRODUCTION RENDER COMPLETE!")
    print("=" * 70)
    print(f"\nOutput files: {output_dir}/production_*.png")
    print()
    print("Post-processing suggestions:")
    print("  • Combine frames to video with FFmpeg")
    print("  • Add audio/music")
    print("  • Color grade in video editor")
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
