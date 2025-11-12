"""
Advanced animation setup with configurable presets
Usage: blender --background --python advanced_setup.py -- [options]

Options:
  --timing PRESET       Timing preset (quick, standard, cinematic, extended)
  --render PRESET       Render preset (preview, draft, production, ultra)
  --color PRESET        Color preset (classic_gold, rose_gold, white_gold, etc.)
  --fire PRESET         Fire preset (subtle, moderate, intense, extreme)
  --camera PRESET       Camera preset (standard, wide, telephoto, dramatic)
  --lighting PRESET     Lighting preset (studio, dramatic, soft, cinematic)

Example:
  blender -b --python advanced_setup.py -- --timing cinematic --color rose_gold --fire intense
"""

import sys
import os

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import bpy
import argparse
from logo_animation import LogoAnimationSetup
from animation_config import get_preset, print_presets


class AdvancedAnimationSetup(LogoAnimationSetup):
    """Extended animation setup with preset support"""

    def __init__(self, svg_path, output_path, presets=None):
        super().__init__(svg_path, output_path)
        self.presets = presets or {}
        self.apply_presets()

    def apply_presets(self):
        """Apply preset configurations"""
        # Apply timing preset
        if 'timing' in self.presets:
            timing = self.presets['timing']
            self.total_frames = timing['total_frames']
            self.fire_end_frame = timing['fire_end_frame']
            print(f"  Applied timing: {timing['description']}")

    def create_golden_material(self):
        """Create material with color preset"""
        mat = super().create_golden_material()

        # Apply color preset if specified
        if 'color' in self.presets:
            color_config = self.presets['color']
            nodes = mat.node_tree.nodes

            # Find Principled BSDF node
            principled = None
            for node in nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    principled = node
                    break

            if principled:
                principled.inputs['Base Color'].default_value = color_config['base_color']
                principled.inputs['Roughness'].default_value = color_config['roughness']

            # Find emission node
            emission = None
            for node in nodes:
                if node.type == 'EMISSION':
                    emission = node
                    break

            if emission:
                emission.inputs['Color'].default_value = color_config['emission_color']
                emission.inputs['Strength'].default_value = color_config['emission_strength']

            print(f"  Applied color: {color_config['description']}")

        return mat

    def setup_camera(self):
        """Setup camera with preset"""
        camera = super().setup_camera()

        if 'camera' in self.presets:
            cam_config = self.presets['camera']
            camera.data.lens = cam_config['lens']
            camera.data.dof.aperture_fstop = cam_config['fstop']

            print(f"  Applied camera: {cam_config['description']}")

        return camera

    def create_fire_simulation(self):
        """Create fire with intensity preset"""
        domain, emitter = super().create_fire_simulation()

        if 'fire' in self.presets:
            fire_config = self.presets['fire']
            flow_settings = emitter.modifiers["Fluid"].flow_settings

            flow_settings.fuel_amount = fire_config['fuel_amount']
            flow_settings.temperature = fire_config['temperature']
            flow_settings.velocity_factor = fire_config['velocity_factor']

            # Update fire material emission strength
            mat = self.fire_domain.data.materials[0]
            nodes = mat.node_tree.nodes
            for node in nodes:
                if node.type == 'MATH' and node.operation == 'MULTIPLY':
                    node.inputs[1].default_value = fire_config['emission_strength']
                    break

            print(f"  Applied fire: {fire_config['description']}")

        return domain, emitter

    def setup_lighting(self):
        """Setup lighting with preset"""
        super().setup_lighting()

        if 'lighting' in self.presets:
            light_config = self.presets['lighting']

            # Update light energies
            for obj in bpy.data.objects:
                if obj.type == 'LIGHT':
                    if 'Key' in obj.name:
                        obj.data.energy = light_config['key_energy']
                    elif 'Fill' in obj.name:
                        obj.data.energy = light_config['fill_energy']
                    elif 'Rim' in obj.name:
                        obj.data.energy = light_config['rim_energy']

            # Update world strength
            world = bpy.data.worlds['World']
            world.node_tree.nodes['Background'].inputs['Strength'].default_value = \
                light_config['ambient_strength']

            print(f"  Applied lighting: {light_config['description']}")

    def configure_render_settings(self):
        """Configure render with quality preset"""
        super().configure_render_settings()

        if 'render' in self.presets:
            render_config = self.presets['render']
            scene = bpy.context.scene

            scene.cycles.samples = render_config['samples']
            scene.render.resolution_x = render_config['resolution_x']
            scene.render.resolution_y = render_config['resolution_y']
            scene.render.resolution_percentage = render_config['resolution_percentage']
            scene.cycles.use_denoising = render_config['use_denoising']

            # Update domain resolution
            if self.fire_domain:
                self.fire_domain.modifiers["Fluid"].domain_settings.resolution_max = \
                    render_config['volume_resolution']

            print(f"  Applied render: {render_config['description']}")

        # Apply FPS from timing preset
        if 'timing' in self.presets:
            bpy.context.scene.render.fps = self.presets['timing']['fps']


def parse_arguments():
    """Parse command line arguments"""
    # Get arguments after '--'
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
    else:
        argv = []

    parser = argparse.ArgumentParser(
        description='Advanced Blender animation setup with presets'
    )

    parser.add_argument('--timing', type=str, default='standard',
                        choices=['quick', 'standard', 'cinematic', 'extended'],
                        help='Timing preset')
    parser.add_argument('--render', type=str, default='production',
                        choices=['preview', 'draft', 'production', 'ultra'],
                        help='Render quality preset')
    parser.add_argument('--color', type=str, default='classic_gold',
                        choices=['classic_gold', 'rose_gold', 'white_gold',
                                'bronze', 'silver', 'platinum'],
                        help='Material color preset')
    parser.add_argument('--fire', type=str, default='intense',
                        choices=['subtle', 'moderate', 'intense', 'extreme'],
                        help='Fire intensity preset')
    parser.add_argument('--camera', type=str, default='standard',
                        choices=['standard', 'wide', 'telephoto', 'dramatic'],
                        help='Camera preset')
    parser.add_argument('--lighting', type=str, default='studio',
                        choices=['studio', 'dramatic', 'soft', 'cinematic'],
                        help='Lighting preset')
    parser.add_argument('--list', action='store_true',
                        help='List all available presets')

    return parser.parse_args(argv)


def main():
    """Main execution with preset support"""
    args = parse_arguments()

    # List presets if requested
    if args.list:
        print_presets()
        return

    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    svg_path = os.path.join(project_root, "alter.svg")
    output_path = os.path.join(project_root, "output")

    # Validate SVG
    if not os.path.exists(svg_path):
        print(f"ERROR: SVG file not found at {svg_path}")
        return

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
    print("\n" + "=" * 60)
    print("Advanced Animation Setup - Configuration")
    print("=" * 60)
    print(f"\nPresets selected:")
    print(f"  Timing:   {args.timing:15s} - {presets['timing']['description']}")
    print(f"  Render:   {args.render:15s} - {presets['render']['description']}")
    print(f"  Color:    {args.color:15s} - {presets['color']['description']}")
    print(f"  Fire:     {args.fire:15s} - {presets['fire']['description']}")
    print(f"  Camera:   {args.camera:15s} - {presets['camera']['description']}")
    print(f"  Lighting: {args.lighting:15s} - {presets['lighting']['description']}")
    print("=" * 60)
    print()

    # Create and run animation setup
    animation = AdvancedAnimationSetup(svg_path, output_path, presets)
    animation.setup_animation()

    # Save with preset info in filename
    blend_filename = f"alter_logo_{args.timing}_{args.color}_{args.fire}.blend"
    blend_path = os.path.join(project_root, blend_filename)
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    print(f"\nCustom blend file saved: {blend_filename}")


if __name__ == "__main__":
    main()
