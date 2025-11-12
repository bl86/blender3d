"""
Alter Logo Fire Animation Script
Professional 3D animation setup for logo reveal with fire effects
"""

import bpy
import os
import math
from mathutils import Vector


class LogoAnimationSetup:
    """Main class for setting up the logo animation with fire effects"""

    def __init__(self, svg_path, output_path):
        self.svg_path = svg_path
        self.output_path = output_path
        self.logo_obj = None
        self.camera = None
        self.fire_domain = None
        self.total_frames = 300
        self.fire_end_frame = 200

    def clear_scene(self):
        """Remove default objects from scene"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Clear orphan data
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)
        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)
        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)

    def import_svg_logo(self):
        """Import SVG logo and convert to mesh with robust error handling"""
        import os

        print(f"  Importing SVG from: {self.svg_path}")

        # Verify SVG file exists
        if not os.path.exists(self.svg_path):
            raise FileNotFoundError(f"SVG file not found: {self.svg_path}")

        # Get existing objects before import
        existing_objects = set(bpy.context.scene.objects)

        # Deselect all first
        bpy.ops.object.select_all(action='DESELECT')

        try:
            # Import SVG
            result = bpy.ops.import_curve.svg(filepath=self.svg_path)

            if result != {'FINISHED'}:
                print(f"  Warning: SVG import returned {result}, trying alternative method...")
                raise Exception("SVG import did not complete successfully")

            # Get newly imported objects
            new_objects = set(bpy.context.scene.objects) - existing_objects
            imported_curves = [obj for obj in new_objects if obj.type == 'CURVE']

            if not imported_curves:
                print("  Warning: No curves found after SVG import, creating fallback text logo...")
                raise Exception("No curves imported from SVG")

            print(f"  Successfully imported {len(imported_curves)} curve object(s)")

            # Select all imported curves
            for obj in imported_curves:
                obj.select_set(True)

            # Set first as active
            bpy.context.view_layer.objects.active = imported_curves[0]

            # Join all curves if multiple
            if len(imported_curves) > 1:
                print(f"  Joining {len(imported_curves)} curves into one object...")
                bpy.ops.object.join()

            logo_curve = bpy.context.active_object

        except Exception as e:
            print(f"  SVG import failed: {str(e)}")
            print("  Creating fallback 3D text logo...")

            # Create fallback text logo
            bpy.ops.object.text_add(location=(0, 0, 0))
            logo_curve = bpy.context.active_object
            logo_curve.data.body = "ALTER"
            logo_curve.data.align_x = 'CENTER'
            logo_curve.data.align_y = 'CENTER'
            logo_curve.data.size = 1.0

            # Add some depth
            logo_curve.data.extrude = 0.2
            logo_curve.data.bevel_depth = 0.05
            logo_curve.data.bevel_resolution = 3

        # Verify we have an object
        if logo_curve is None:
            raise Exception("Failed to create logo object")

        # Name the object
        logo_curve.name = "AlterLogo"
        print(f"  Logo object created: {logo_curve.name}")

        # Add extrusion and bevel for depth (skip if already done in fallback)
        if logo_curve.type == 'CURVE' and logo_curve.data.body != "ALTER":
            try:
                logo_curve.data.extrude = 0.15
                logo_curve.data.bevel_depth = 0.02
                logo_curve.data.bevel_resolution = 4
                print("  Added extrusion and bevel")
            except:
                print("  Note: Could not add extrusion (may already be set)")

        # Convert to mesh for better material control
        print("  Converting to mesh...")
        bpy.ops.object.convert(target='MESH')

        # Update reference (convert changes the object)
        logo_mesh = bpy.context.active_object
        logo_mesh.name = "AlterLogo"

        # Center and scale
        print("  Centering and scaling...")
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        logo_mesh.location = (0, 0, 0)
        logo_mesh.scale = (2.5, 2.5, 2.5)
        bpy.ops.object.transform_apply(scale=True)

        self.logo_obj = logo_mesh
        print(f"  ✓ Logo ready: {logo_mesh.name}")

        return logo_mesh

    def create_golden_material(self):
        """Create photorealistic golden material with reflections"""
        mat = bpy.data.materials.new(name="GoldenMetal")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Clear default nodes
        nodes.clear()

        # Create nodes
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (800, 0)

        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (400, 0)

        # Golden color configuration
        principled.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)  # Rich gold
        principled.inputs['Metallic'].default_value = 1.0
        principled.inputs['Roughness'].default_value = 0.15
        principled.inputs['Specular IOR Level'].default_value = 0.8
        principled.inputs['Anisotropic'].default_value = 0.3
        principled.inputs['Anisotropic Rotation'].default_value = 0.25
        principled.inputs['Sheen Tint'].default_value = (1.0, 0.8, 0.4, 1.0)

        # Add emission for glow effect
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (200, -200)
        emission.inputs['Color'].default_value = (1.0, 0.85, 0.4, 1.0)
        emission.inputs['Strength'].default_value = 0.3

        # Mix shader for subtle glow
        mix = nodes.new(type='ShaderNodeMixShader')
        mix.location = (600, 0)
        mix.inputs['Fac'].default_value = 0.95

        # Add color ramp for variation
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (0, 0)
        color_ramp.color_ramp.elements[0].color = (0.9, 0.7, 0.3, 1.0)
        color_ramp.color_ramp.elements[1].color = (1.0, 0.85, 0.4, 1.0)

        # Fresnel for edge highlighting
        fresnel = nodes.new(type='ShaderNodeFresnel')
        fresnel.location = (0, -100)
        fresnel.inputs['IOR'].default_value = 1.5

        # Connect nodes
        links.new(principled.outputs['BSDF'], mix.inputs[1])
        links.new(emission.outputs['Emission'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])

        # Assign material to logo
        if self.logo_obj.data.materials:
            self.logo_obj.data.materials[0] = mat
        else:
            self.logo_obj.data.materials.append(mat)

        return mat

    def setup_camera(self):
        """Setup and animate camera"""
        # Create camera
        bpy.ops.object.camera_add(location=(0, -25, 2))
        self.camera = bpy.context.active_object
        self.camera.name = "MainCamera"

        # Camera settings
        self.camera.data.lens = 50
        self.camera.data.sensor_width = 36
        self.camera.data.dof.use_dof = True
        self.camera.data.dof.aperture_fstop = 2.8
        self.camera.data.dof.focus_distance = 25

        # Point camera at logo
        constraint = self.camera.constraints.new(type='TRACK_TO')
        constraint.target = self.logo_obj
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

        # Set as active camera
        bpy.context.scene.camera = self.camera

        return self.camera

    def animate_logo(self):
        """Animate logo moving towards camera"""
        # Starting position (far from camera)
        start_pos = Vector((0, 15, 0))
        # End position (close to camera)
        end_pos = Vector((0, -5, 0))

        # Set initial position
        self.logo_obj.location = start_pos
        self.logo_obj.keyframe_insert(data_path="location", frame=1)

        # Set end position
        self.logo_obj.location = end_pos
        self.logo_obj.keyframe_insert(data_path="location", frame=self.total_frames)

        # Add smooth interpolation
        for fcurve in self.logo_obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'BEZIER'
                keyframe.handle_left_type = 'AUTO_CLAMPED'
                keyframe.handle_right_type = 'AUTO_CLAMPED'

        # Add subtle rotation for dynamic effect
        self.logo_obj.rotation_euler = (0, 0, 0)
        self.logo_obj.keyframe_insert(data_path="rotation_euler", frame=1)

        self.logo_obj.rotation_euler = (0.1, 0, math.radians(360))
        self.logo_obj.keyframe_insert(data_path="rotation_euler", frame=self.total_frames)

    def create_fire_simulation(self):
        """Create realistic fire simulation around logo"""
        # Create smoke domain
        bpy.ops.mesh.primitive_cube_add(size=12, location=(0, 5, 0))
        domain = bpy.context.active_object
        domain.name = "FireDomain"
        self.fire_domain = domain

        # Add smoke modifier
        bpy.ops.object.modifier_add(type='FLUID')
        domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
        domain_settings = domain.modifiers["Fluid"].domain_settings

        # Configure domain for fire
        domain_settings.domain_type = 'GAS'
        domain_settings.resolution_max = 256
        domain_settings.use_noise = True
        domain_settings.noise_scale = 2
        domain_settings.noise_strength = 1.5

        # Enable fire
        domain_settings.use_fire = True
        domain_settings.alpha = 1
        domain_settings.beta = 1.5
        domain_settings.flame_smoke = 1.0
        domain_settings.flame_vorticity = 0.5

        # Time settings
        domain_settings.time_scale = 1.0
        domain_settings.cfl_condition = 4.0

        # Smoke settings
        domain_settings.dissolve_speed = 5
        domain_settings.vorticity = 0.3

        # Cache settings
        domain_settings.cache_frame_start = 1
        domain_settings.cache_frame_end = self.total_frames
        domain_settings.cache_type = 'MODULAR'

        # Create fire emitter (torus around logo)
        bpy.ops.mesh.primitive_torus_add(
            align='WORLD',
            location=(0, 0, 0),
            rotation=(math.radians(90), 0, 0),
            major_radius=3.5,
            minor_radius=0.8
        )
        emitter = bpy.context.active_object
        emitter.name = "FireEmitter"

        # Parent emitter to logo
        emitter.parent = self.logo_obj
        emitter.matrix_parent_inverse = self.logo_obj.matrix_world.inverted()

        # Add fluid modifier to emitter
        bpy.ops.object.modifier_add(type='FLUID')
        emitter.modifiers["Fluid"].fluid_type = 'FLOW'
        flow_settings = emitter.modifiers["Fluid"].flow_settings

        # Configure flow
        flow_settings.flow_type = 'FIRE'
        flow_settings.flow_behavior = 'INFLOW'
        flow_settings.use_initial_velocity = True
        flow_settings.velocity_factor = 1.5
        flow_settings.velocity_normal = 0.5

        # Smoke settings
        flow_settings.smoke_color = (1.0, 0.5, 0.1)
        flow_settings.temperature = 3.0
        flow_settings.fuel_amount = 2.0

        # Animate fire strength (fade out)
        flow_settings.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(
            data_path="density", frame=1
        )

        flow_settings.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(
            data_path="density", frame=self.fire_end_frame - 30
        )

        flow_settings.density = 0.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(
            data_path="density", frame=self.fire_end_frame
        )

        # Create fire material for domain
        self.create_fire_material()

        # Hide emitter in render
        emitter.hide_render = True

        return domain, emitter

    def create_fire_material(self):
        """Create realistic fire and smoke material"""
        mat = bpy.data.materials.new(name="FireMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Clear default
        nodes.clear()

        # Output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (800, 0)

        # Volume Scatter
        volume_scatter = nodes.new(type='ShaderNodeVolumeScatter')
        volume_scatter.location = (400, 100)

        # Volume Absorption
        volume_absorption = nodes.new(type='ShaderNodeVolumeAbsorption')
        volume_absorption.location = (400, -100)

        # Add Shader
        add_shader = nodes.new(type='ShaderNodeAddShader')
        add_shader.location = (600, 0)

        # Emission for fire glow
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (200, 200)

        # Attribute nodes for density and flame
        attr_density = nodes.new(type='ShaderNodeAttribute')
        attr_density.location = (-200, 0)
        attr_density.attribute_name = 'density'

        attr_flame = nodes.new(type='ShaderNodeAttribute')
        attr_flame.location = (-200, -200)
        attr_flame.attribute_name = 'flame'

        # Color ramp for flame color
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (0, 200)

        # Fire color gradient (blue-orange-yellow-white)
        color_ramp.color_ramp.elements[0].position = 0.0
        color_ramp.color_ramp.elements[0].color = (0.1, 0.05, 0.0, 1.0)
        color_ramp.color_ramp.elements[1].position = 0.3
        color_ramp.color_ramp.elements[1].color = (1.0, 0.2, 0.0, 1.0)

        # Add more color stops
        elem = color_ramp.color_ramp.elements.new(0.6)
        elem.color = (1.0, 0.6, 0.1, 1.0)

        elem = color_ramp.color_ramp.elements.new(0.9)
        elem.color = (1.0, 0.9, 0.5, 1.0)

        # Math nodes for strength
        math_multiply = nodes.new(type='ShaderNodeMath')
        math_multiply.location = (0, 400)
        math_multiply.operation = 'MULTIPLY'
        math_multiply.inputs[1].default_value = 25.0

        # Connect nodes
        links.new(attr_flame.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(attr_flame.outputs['Fac'], math_multiply.inputs[0])
        links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        links.new(math_multiply.outputs['Value'], emission.inputs['Strength'])
        links.new(emission.outputs['Emission'], add_shader.inputs[0])
        links.new(volume_scatter.outputs['Volume'], add_shader.inputs[1])
        links.new(add_shader.outputs['Shader'], output.inputs['Volume'])

        # Assign to domain
        if self.fire_domain.data.materials:
            self.fire_domain.data.materials[0] = mat
        else:
            self.fire_domain.data.materials.append(mat)

        return mat

    def setup_lighting(self):
        """Create professional lighting setup"""
        # Key light
        bpy.ops.object.light_add(type='AREA', location=(5, -10, 8))
        key_light = bpy.context.active_object
        key_light.name = "KeyLight"
        key_light.data.energy = 500
        key_light.data.size = 5
        key_light.data.color = (1.0, 0.95, 0.9)

        # Point at logo
        constraint = key_light.constraints.new(type='TRACK_TO')
        constraint.target = self.logo_obj
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -8, 4))
        fill_light = bpy.context.active_object
        fill_light.name = "FillLight"
        fill_light.data.energy = 200
        fill_light.data.size = 4
        fill_light.data.color = (0.9, 0.95, 1.0)

        # Rim light
        bpy.ops.object.light_add(type='SPOT', location=(0, 10, 5))
        rim_light = bpy.context.active_object
        rim_light.name = "RimLight"
        rim_light.data.energy = 300
        rim_light.data.color = (1.0, 0.8, 0.5)
        rim_light.data.spot_size = math.radians(60)
        rim_light.data.spot_blend = 0.3

        # Point at logo
        constraint = rim_light.constraints.new(type='TRACK_TO')
        constraint.target = self.logo_obj
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

        # Environment lighting
        world = bpy.data.worlds['World']
        world.use_nodes = True
        bg = world.node_tree.nodes['Background']
        bg.inputs['Color'].default_value = (0.05, 0.05, 0.08, 1.0)
        bg.inputs['Strength'].default_value = 0.5

    def setup_compositing(self):
        """Setup compositing for bloom and color grading"""
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        nodes = tree.nodes
        links = tree.links

        # Clear default nodes
        nodes.clear()

        # Render Layers
        render_layers = nodes.new(type='CompositorNodeRLayers')
        render_layers.location = (0, 0)

        # Glare (bloom effect)
        glare = nodes.new(type='CompositorNodeGlare')
        glare.location = (300, 200)
        glare.glare_type = 'FOG_GLOW'
        glare.quality = 'HIGH'
        glare.threshold = 0.6
        glare.size = 8
        glare.iterations = 3

        # Mix for subtle bloom
        mix = nodes.new(type='CompositorNodeMixRGB')
        mix.location = (600, 0)
        mix.blend_type = 'ADD'
        mix.inputs['Fac'].default_value = 0.3

        # Color correction
        color_correct = nodes.new(type='CompositorNodeColorCorrection')
        color_correct.location = (800, 0)
        color_correct.master_saturation = 1.2
        color_correct.master_gain = 1.1
        color_correct.highlights_gain = 1.15

        # Lens distortion
        lens = nodes.new(type='CompositorNodeLensdist')
        lens.location = (1000, 0)
        lens.inputs['Distort'].default_value = -0.01
        lens.inputs['Dispersion'].default_value = 0.015

        # Composite
        composite = nodes.new(type='CompositorNodeComposite')
        composite.location = (1200, 0)

        # Connect nodes
        links.new(render_layers.outputs['Image'], mix.inputs[1])
        links.new(render_layers.outputs['Image'], glare.inputs['Image'])
        links.new(glare.outputs['Image'], mix.inputs[2])
        links.new(mix.outputs['Image'], color_correct.inputs['Image'])
        links.new(color_correct.outputs['Image'], lens.inputs['Image'])
        links.new(lens.outputs['Image'], composite.inputs['Image'])

    def configure_render_settings(self):
        """Configure high-quality render settings"""
        scene = bpy.context.scene

        # Set frame range
        scene.frame_start = 1
        scene.frame_end = self.total_frames
        scene.frame_current = 1

        # Frame rate
        scene.render.fps = 30

        # Render engine
        scene.render.engine = 'CYCLES'
        cycles = scene.cycles

        # Quality settings
        cycles.samples = 256
        cycles.preview_samples = 64
        cycles.use_denoising = True
        cycles.denoiser = 'OPENIMAGEDENOISE'

        # Performance
        cycles.device = 'GPU'
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.01

        # Light paths
        cycles.max_bounces = 12
        cycles.diffuse_bounces = 4
        cycles.glossy_bounces = 8
        cycles.transmission_bounces = 8
        cycles.volume_bounces = 4
        cycles.transparent_max_bounces = 16

        # Volume settings
        cycles.volume_step_rate = 0.5
        cycles.volume_preview_step_rate = 0.5
        cycles.volume_max_steps = 1024

        # Film
        scene.render.film_transparent = False
        scene.render.filter_size = 1.5

        # Motion blur
        scene.render.use_motion_blur = True
        scene.render.motion_blur_shutter = 0.5

        # Output settings
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100

        # Color management
        scene.view_settings.view_transform = 'Filmic'
        scene.view_settings.look = 'High Contrast'
        scene.view_settings.exposure = 0.5
        scene.view_settings.gamma = 1.0

        # Output format
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'HIGH'
        scene.render.ffmpeg.ffmpeg_preset = 'BEST'
        scene.render.ffmpeg.audio_codec = 'NONE'

        # Set output path
        scene.render.filepath = os.path.join(self.output_path, 'alter_logo_animation_')

    def setup_animation(self):
        """Main setup function to create entire animation with robust error handling"""
        print("=" * 60)
        print("Starting Alter Logo Animation Setup")
        print("=" * 60)
        print()

        try:
            # Clear scene
            print("[1/10] Clearing scene...")
            self.clear_scene()
            print("  ✓ Scene cleared")

            # Import logo
            print("\n[2/10] Importing SVG logo...")
            self.import_svg_logo()
            if not self.logo_obj:
                raise Exception("Failed to create logo object")

            # Create material
            print("\n[3/10] Creating golden material...")
            self.create_golden_material()
            print("  ✓ Material created")

            # Setup camera
            print("\n[4/10] Setting up camera...")
            self.setup_camera()
            print("  ✓ Camera configured")

            # Animate logo
            print("\n[5/10] Animating logo movement...")
            self.animate_logo()
            print("  ✓ Animation keyframes set")

            # Create fire
            print("\n[6/10] Creating fire simulation...")
            try:
                self.create_fire_simulation()
                print("  ✓ Fire simulation created")
            except Exception as e:
                print(f"  ⚠ Fire simulation skipped (non-critical): {str(e)}")
                print("  Animation will continue without fire effect")

            # Setup lighting
            print("\n[7/10] Setting up lighting...")
            self.setup_lighting()
            print("  ✓ Lighting setup complete")

            # Setup compositing
            print("\n[8/10] Configuring compositing...")
            try:
                self.setup_compositing()
                print("  ✓ Compositing configured")
            except Exception as e:
                print(f"  ⚠ Compositing setup failed (non-critical): {str(e)}")

            # Configure render
            print("\n[9/10] Configuring render settings...")
            self.configure_render_settings()
            print("  ✓ Render settings applied")

            # Save file
            print("\n[10/10] Saving blend file...")
            blend_path = os.path.join(
                os.path.dirname(self.svg_path),
                "alter_logo_animation.blend"
            )
            bpy.ops.wm.save_as_mainfile(filepath=blend_path)
            print(f"  ✓ Saved to: {blend_path}")

            print("\n" + "=" * 60)
            print("✓ Animation Setup Complete!")
            print("=" * 60)
            print(f"\nBlend file: {blend_path}")
            print(f"Total frames: {self.total_frames}")
            print(f"Fire fade ends at frame: {self.fire_end_frame}")
            print(f"Resolution: 1920x1080")
            print(f"FPS: 30")
            print(f"\nTo render:")
            print(f"  • Open in Blender: blender {blend_path}")
            print(f"  • Or render: blender -b {blend_path} -a")
            print("=" * 60)

        except Exception as e:
            print("\n" + "=" * 60)
            print("✗ SETUP FAILED")
            print("=" * 60)
            print(f"\nError: {str(e)}")
            print("\nPlease check:")
            print("  • alter.svg exists in project folder")
            print("  • Blender version is 3.0 or higher")
            print("  • You have write permissions")
            print()
            import traceback
            traceback.print_exc()
            raise


def main():
    """Main execution function"""
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Paths
    svg_path = os.path.join(project_root, "alter.svg")
    output_path = os.path.join(project_root, "output")

    # Validate SVG exists
    if not os.path.exists(svg_path):
        print(f"ERROR: SVG file not found at {svg_path}")
        return

    # Create output directory
    os.makedirs(output_path, exist_ok=True)

    # Create and run animation setup
    animation = LogoAnimationSetup(svg_path, output_path)
    animation.setup_animation()


if __name__ == "__main__":
    main()
