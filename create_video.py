"""
Convert rendered frames to video using Blender's built-in video sequencer
No external tools required!

Usage:
  blender --background --python create_video.py -- [options]

Options:
  --input DIR       Input directory with frames (default: output/)
  --output FILE     Output video file (default: output/animation.mp4)
  --pattern PATTERN Frame pattern (default: *_*.png)
  --fps FPS         Frames per second (default: 30)

Examples:
  blender --background --python create_video.py
  blender --background --python create_video.py -- --output final.mp4
  blender --background --python create_video.py -- --fps 60
"""

import bpy
import os
import sys
import glob


def parse_args():
    """Parse command line arguments"""
    # Default values
    args = {
        'input': 'output',
        'output': 'output/animation.mp4',
        'pattern': '*_*.png',
        'fps': 30
    }

    # Get arguments after '--'
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]

        i = 0
        while i < len(argv):
            if argv[i] == '--input' and i + 1 < len(argv):
                args['input'] = argv[i + 1]
                i += 2
            elif argv[i] == '--output' and i + 1 < len(argv):
                args['output'] = argv[i + 1]
                i += 2
            elif argv[i] == '--pattern' and i + 1 < len(argv):
                args['pattern'] = argv[i + 1]
                i += 2
            elif argv[i] == '--fps' and i + 1 < len(argv):
                args['fps'] = int(argv[i + 1])
                i += 2
            else:
                i += 1

    return args


def create_video(input_dir, output_file, pattern, fps):
    """Create video from image sequence using Blender VSE"""

    print("\n" + "=" * 70)
    print("VIDEO CREATION - From Image Sequence")
    print("=" * 70)
    print()

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Make paths absolute
    if not os.path.isabs(input_dir):
        input_dir = os.path.join(script_dir, input_dir)
    if not os.path.isabs(output_file):
        output_file = os.path.join(script_dir, output_file)

    # Find frames
    frame_pattern = os.path.join(input_dir, pattern)
    frames = sorted(glob.glob(frame_pattern))

    if not frames:
        print(f"ERROR: No frames found matching: {frame_pattern}")
        return False

    print(f"Found {len(frames)} frames")
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_file}")
    print(f"FPS: {fps}")
    print()

    # Clear existing scene
    bpy.ops.wm.read_homefile(use_empty=True)

    # Setup scene
    scene = bpy.context.scene
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = len(frames)

    # Setup render output
    scene.render.filepath = output_file
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'

    # Get first frame dimensions
    import bpy
    test_image = bpy.data.images.load(frames[0])
    width = test_image.size[0]
    height = test_image.size[1]
    bpy.data.images.remove(test_image)

    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100

    # Create sequencer
    if not scene.sequence_editor:
        scene.sequence_editor_create()

    seq_editor = scene.sequence_editor

    # Add image sequence
    strip = seq_editor.sequences.new_image(
        name="ImageSequence",
        filepath=frames[0],
        channel=1,
        frame_start=1
    )

    # Add all frames
    for frame_path in frames[1:]:
        strip.elements.append(frame_path)

    print("Rendering video...")
    print("This may take a few minutes...")
    print()

    # Render
    bpy.ops.render.render(animation=True, write_still=False)

    print()
    print("=" * 70)
    print("VIDEO CREATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print(f"Output: {output_file}")
    print(f"Frames: {len(frames)}")
    print(f"Duration: {len(frames) / fps:.1f} seconds")
    print()

    return True


def main():
    """Main execution"""
    args = parse_args()

    try:
        success = create_video(
            args['input'],
            args['output'],
            args['pattern'],
            args['fps']
        )
        return success
    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR: Video creation failed!")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
