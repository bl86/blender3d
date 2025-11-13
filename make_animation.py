"""
ALL-IN-ONE Animation Script
Simplest way to create the complete animation - generates scene and renders in one go

Usage:
  blender --background --python make_animation.py

Options (add after --):
  --quick         Fast preview quality (10 min)
  --production    High quality (default, 45+ min)
  --video         Also create MP4 video at the end

Examples:
  blender --background --python make_animation.py
  blender --background --python make_animation.py -- --quick
  blender --background --python make_animation.py -- --production --video
"""

import sys
import os
import time

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(script_dir, 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)


def parse_args():
    """Parse command line arguments"""
    args = {
        'quality': 'production',
        'create_video': False
    }

    # Get arguments after '--'
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
        if '--quick' in argv:
            args['quality'] = 'quick'
        if '--production' in argv:
            args['quality'] = 'production'
        if '--video' in argv:
            args['create_video'] = True

    return args


def print_banner():
    """Print nice banner"""
    print("\n" + "=" * 70)
    print(" " * 15 + "ALTER LOGO ANIMATION - ALL-IN-ONE")
    print("=" * 70)
    print()


def step_generate_scene():
    """Step 1: Generate Blender scene"""
    print("┌" + "─" * 68 + "┐")
    print("│" + " STEP 1: GENERATING SCENE ".center(68) + "│")
    print("└" + "─" * 68 + "┘")
    print()

    from logo_animation import LogoAnimationSetup

    project_root = script_dir
    svg_path = os.path.join(project_root, "alter.svg")
    output_path = os.path.join(project_root, "output")

    if not os.path.exists(svg_path):
        print(f"❌ ERROR: alter.svg not found at {svg_path}")
        return False

    os.makedirs(output_path, exist_ok=True)

    print("Creating animation scene...")
    print("  • Importing SVG logo")
    print("  • Setting up golden material")
    print("  • Creating fire simulation")
    print("  • Configuring camera and lighting")
    print("  • Setting up compositing")
    print()

    try:
        animation = LogoAnimationSetup(svg_path, output_path)
        animation.setup_animation()
        print("✓ Scene generated successfully!")
        return True
    except Exception as e:
        print(f"❌ Scene generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def step_render(quality='production'):
    """Step 2: Render animation"""
    print()
    print("┌" + "─" * 68 + "┐")
    print("│" + f" STEP 2: RENDERING ({quality.upper()} QUALITY) ".center(68) + "│")
    print("└" + "─" * 68 + "┘")
    print()

    import bpy

    scene = bpy.context.scene

    if quality == 'quick':
        print("Quick render settings:")
        print("  • Samples: 64")
        print("  • Resolution: 50% (720p)")
        print("  • Estimated time: ~10-15 minutes")
        scene.cycles.samples = 64
        scene.render.resolution_percentage = 50
        output_prefix = "quick_"
    else:
        print("Production render settings:")
        print("  • Samples: 256")
        print("  • Resolution: 100% (1080p)")
        print("  • Estimated time: ~45-90 minutes")
        scene.cycles.samples = 256
        scene.render.resolution_percentage = 100
        output_prefix = "production_"

    scene.cycles.use_denoising = True

    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, output_prefix)

    print()
    print("Starting render...")
    print("Progress will be shown below:")
    print()

    start_time = time.time()

    try:
        bpy.ops.render.render(animation=True)
        elapsed = time.time() - start_time
        print()
        print(f"✓ Render complete! (took {elapsed/60:.1f} minutes)")
        return True
    except Exception as e:
        print(f"❌ Render failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def step_create_video(quality='production'):
    """Step 3: Create video from frames"""
    print()
    print("┌" + "─" * 68 + "┐")
    print("│" + " STEP 3: CREATING VIDEO ".center(68) + "│")
    print("└" + "─" * 68 + "┘")
    print()

    import bpy
    import glob

    output_dir = os.path.join(script_dir, "output")
    prefix = "quick_" if quality == 'quick' else "production_"

    # Find frames
    frame_pattern = os.path.join(output_dir, f"{prefix}*.png")
    frames = sorted(glob.glob(frame_pattern))

    if not frames:
        print(f"❌ No frames found matching: {frame_pattern}")
        return False

    print(f"Found {len(frames)} frames")
    print("Creating MP4 video...")
    print()

    # Clear scene and setup VSE
    bpy.ops.wm.read_homefile(use_empty=True)
    scene = bpy.context.scene

    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = len(frames)

    # Output settings
    video_name = f"alter_animation_{quality}.mp4"
    output_file = os.path.join(output_dir, video_name)

    scene.render.filepath = output_file
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

    # Get dimensions
    test_image = bpy.data.images.load(frames[0])
    scene.render.resolution_x = test_image.size[0]
    scene.render.resolution_y = test_image.size[1]
    bpy.data.images.remove(test_image)

    # Create sequencer
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    seq_editor = scene.sequence_editor
    strip = seq_editor.sequences.new_image(
        name="Frames",
        filepath=frames[0],
        channel=1,
        frame_start=1
    )

    for frame_path in frames[1:]:
        strip.elements.append(frame_path)

    try:
        bpy.ops.render.render(animation=True, write_still=False)
        print()
        print(f"✓ Video created: {video_name}")
        print(f"  Duration: {len(frames) / 30:.1f} seconds")
        print(f"  Location: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Video creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main execution"""
    args = parse_args()

    print_banner()

    print("Configuration:")
    print(f"  Quality: {args['quality']}")
    print(f"  Create video: {'Yes' if args['create_video'] else 'No'}")
    print()
    print("This will:")
    print("  1. Generate Blender scene from alter.svg")
    print("  2. Render 300 frames")
    if args['create_video']:
        print("  3. Create MP4 video")
    print()

    start_time = time.time()

    # Step 1: Generate scene
    if not step_generate_scene():
        return False

    # Step 2: Render
    if not step_render(args['quality']):
        return False

    # Step 3: Create video (optional)
    if args['create_video']:
        if not step_create_video(args['quality']):
            print("⚠ Video creation failed, but frames are available")

    # Done!
    total_time = time.time() - start_time

    print()
    print("=" * 70)
    print(" " * 20 + "🎉 ALL DONE! 🎉")
    print("=" * 70)
    print()
    print(f"Total time: {total_time/60:.1f} minutes")
    print()
    print("Output files:")
    print(f"  • Blend file: alter_logo_animation.blend")
    print(f"  • Frames: output/{args['quality']}_*.png")
    if args['create_video']:
        print(f"  • Video: output/alter_animation_{args['quality']}.mp4")
    print()
    print("🔥 Your logo animation is ready! 🔥")
    print()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
