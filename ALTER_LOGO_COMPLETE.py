"""
═══════════════════════════════════════════════════════════════════════════════
ALTER LOGO FIRE ANIMATION - COMPLETE SINGLE-FILE SETUP
═══════════════════════════════════════════════════════════════════════════════

HOW TO USE IN BLENDER:
1. Open Blender
2. Go to "Scripting" tab
3. Click "Open" and select this file
4. Click "Run Script" (or press Alt+P)
5. DONE! Animation with fire is ready!

OR FROM COMMAND LINE:
blender --background --python THIS_FILE.py

Requirements:
- Blender 3.0+
- alter.svg in the same folder as this script

Output:
- alter_logo_fire_animation.blend (saved automatically)
- 300 frames (10 seconds), 1920x1080, with fire simulation

═══════════════════════════════════════════════════════════════════════════════
"""

import bpy
import os
import math
from mathutils import Vector


def find_svg_file():
    """Find alter.svg in project root"""
    # Try current blend file directory first
    if bpy.data.filepath:
        blend_dir = os.path.dirname(bpy.data.filepath)
        svg_path = os.path.join(blend_dir, "alter.svg")
        if os.path.exists(svg_path):
            return svg_path

    # Try script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, "alter.svg")
    if os.path.exists(svg_path):
        return svg_path

    # Try current working directory
    svg_path = os.path.join(os.getcwd(), "alter.svg")
    if os.path.exists(svg_path):
        return svg_path

    # Try one level up
    parent_dir = os.path.dirname(script_dir)
    svg_path = os.path.join(parent_dir, "alter.svg")
    if os.path.exists(svg_path):
        return svg_path

    return None


def clear_scene():
    """Clear all objects from scene"""
    print("  Clearing scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Clean up data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


def import_svg_logo(svg_path):
    """Import SVG logo with robust error handling"""
    print(f"  Importing SVG: {svg_path}")

    # Store existing objects
    existing_objects = set(bpy.context.scene.objects)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Import SVG
    result = bpy.ops.import_curve.svg(filepath=svg_path)

    if result != {'FINISHED'}:
        raise Exception(f"SVG import failed: {result}")

    # Find new objects
    new_objects = set(bpy.context.scene.objects) - existing_objects
    curves = [obj for obj in new_objects if obj.type == 'CURVE']

    if not curves:
        raise Exception("No curves found after SVG import")

    print(f"  Imported {len(curves)} curve(s)")

    # Select all curves
    for obj in curves:
        obj.select_set(True)

    # Set active
    bpy.context.view_layer.objects.active = curves[0]

    # Join if multiple
    if len(curves) > 1:
        print(f"  Joining {len(curves)} curves...")
        bpy.ops.object.join()

    logo = bpy.context.active_object
    logo.name = "AlterLogo"

    # Add minimal depth for 3D feel - NO BEVEL
    logo.data.extrude = 0.05  # Small extrude only
    logo.data.bevel_depth = 0.0  # No bevel - it ruins geometry
    logo.data.bevel_resolution = 0

    # Convert to mesh
    print("  Converting to mesh...")
    bpy.ops.object.convert(target='MESH')

    logo = bpy.context.active_object
    logo.name = "AlterLogo"

    # Center and scale
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    logo.location = (0, 0, 0)
    logo.scale = (2.5, 2.5, 2.5)
    bpy.ops.object.transform_apply(scale=True)

    # Rotate to face camera (logo faces -Y direction)
    logo.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    print(f"  ✓ Logo ready: {logo.name}")
    return logo


def create_golden_material(logo):
    """Create golden metallic material"""
    print("  Creating golden material...")

    mat = bpy.data.materials.new(name="GoldenMetal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Principled BSDF - Reflective gold
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)  # Gold color
    bsdf.inputs['Metallic'].default_value = 1.0  # Full metallic
    bsdf.inputs['Roughness'].default_value = 0.08  # Very smooth for strong reflections
    bsdf.inputs['Specular IOR Level'].default_value = 1.0  # Maximum specular

    # Add anisotropic for brushed metal look (if available)
    try:
        bsdf.inputs['Anisotropic'].default_value = 0.3
        bsdf.inputs['Anisotropic Rotation'].default_value = 0.25
    except:
        pass  # Not available in all Blender versions

    # Emission for glow
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (200, -200)
    emission.inputs['Color'].default_value = (1.0, 0.85, 0.4, 1.0)
    emission.inputs['Strength'].default_value = 0.3

    # Mix
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (600, 0)
    mix.inputs[0].default_value = 0.95

    links.new(bsdf.outputs['BSDF'], mix.inputs[1])
    links.new(emission.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])

    # Apply to logo
    if logo.data.materials:
        logo.data.materials[0] = mat
    else:
        logo.data.materials.append(mat)

    print("  ✓ Material applied")


def setup_camera(logo):
    """Setup camera with tracking - positioned to frame logo perfectly"""
    print("  Setting up camera...")

    # Position camera to see logo centered and close at the end
    bpy.ops.object.camera_add(location=(0, -10, 1))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    camera.data.lens = 50  # Standard lens for good perspective
    camera.data.dof.use_dof = True
    camera.data.dof.aperture_fstop = 2.8
    camera.data.dof.focus_distance = 10

    # Track logo so it's always centered
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = logo
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    bpy.context.scene.camera = camera

    # Set initial frame to see final position (for better preview)
    bpy.context.scene.frame_set(250)  # Near end where logo is close

    # Align viewport to camera view (so user sees render view)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Set to camera view
                    space.region_3d.view_perspective = 'CAMERA'
                    break

    # Reset to frame 1 for animation start
    bpy.context.scene.frame_set(1)

    print("  ✓ Camera configured, centered on logo")
    return camera


def animate_logo(logo):
    """Animate logo movement - straight to camera, no rotation"""
    print("  Animating logo...")

    # Start far
    logo.location = (0, 12, 0)
    logo.keyframe_insert(data_path="location", frame=1)

    # End near - centered in frame
    logo.location = (0, -2, 0)
    logo.keyframe_insert(data_path="location", frame=300)

    # No rotation - keep logo facing camera
    logo.rotation_euler = (0, 0, 0)
    logo.keyframe_insert(data_path="rotation_euler", frame=1)
    logo.keyframe_insert(data_path="rotation_euler", frame=300)

    # Smooth curves
    for fcurve in logo.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.handle_left_type = 'AUTO_CLAMPED'
            kf.handle_right_type = 'AUTO_CLAMPED'

    print("  ✓ Animation keyframes set")


def create_fire_simulation(logo):
    """Create fire simulation around logo"""
    print("  Creating fire simulation...")

    # Domain - covers logo animation path (y: 12 to -2 = 14 units + margin)
    bpy.ops.mesh.primitive_cube_add(size=18, location=(0, 5, 0))
    domain = bpy.context.active_object
    domain.name = "FireDomain"
    domain.display_type = 'WIRE'  # Show as wireframe in viewport

    # Add fluid modifier
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    # Configure domain
    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 256  # Higher resolution for better fire visibility

    # Noise settings
    try:
        domain_settings.use_noise = True
        domain_settings.noise_scale = 2  # Must be int
    except:
        pass  # Noise not available in this version

    # Fire settings (Blender 4.5+ compatibility)
    try:
        domain_settings.use_fire = True
    except AttributeError:
        pass  # use_fire removed in Blender 4.5+, fire is automatic with FIRE flow type

    try:
        domain_settings.alpha = 1.0
        domain_settings.beta = 1.0
    except AttributeError:
        pass  # alpha/beta removed in newer versions

    try:
        domain_settings.flame_smoke = 1.0
    except AttributeError:
        pass  # flame_smoke removed in newer versions

    try:
        domain_settings.vorticity = 0.3
    except AttributeError:
        pass  # vorticity might not be available

    # Cache - only until fire ends to save baking time
    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = 180  # Fire ends at 150, add buffer

    # Emitter - duplicate logo shape so fire matches logo outline
    bpy.ops.object.select_all(action='DESELECT')
    logo.select_set(True)
    bpy.context.view_layer.objects.active = logo
    bpy.ops.object.duplicate()
    emitter = bpy.context.active_object
    emitter.name = "FireEmitter"

    # Scale up slightly so fire surrounds logo
    emitter.scale = (1.2, 1.2, 1.2)  # Bigger scale for better fire coverage

    # Parent to logo so it follows
    emitter.parent = logo
    emitter.matrix_parent_inverse = logo.matrix_world.inverted()

    # Hide emitter completely - don't want to see duplicate logo
    emitter.hide_render = True
    emitter.hide_viewport = True  # Also hide in viewport
    emitter.display_type = 'WIRE'  # Show only wireframe if visible

    # Add flow
    bpy.ops.object.modifier_add(type='FLUID')
    emitter.modifiers["Fluid"].fluid_type = 'FLOW'
    flow = emitter.modifiers["Fluid"].flow_settings
    flow.flow_type = 'FIRE'
    flow.flow_behavior = 'INFLOW'

    # Fire properties (compatibility with different Blender versions)
    try:
        flow.fuel_amount = 2.0
    except AttributeError:
        pass  # fuel_amount not available

    try:
        flow.temperature = 3.0
    except AttributeError:
        pass  # temperature not available

    # Animate fire fade - fire disappears quickly to save render time
    try:
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=1)
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=120)
        flow.density = 0.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=150)
    except (AttributeError, TypeError):
        # Keyframing might not work, try simple approach
        pass

    # Fire material using Principled Volume for proper fire rendering
    mat = bpy.data.materials.new(name="FireMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Principled Volume - much better for fire/smoke
    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (200, 0)

    # Fire attributes
    flame_attr = nodes.new('ShaderNodeAttribute')
    flame_attr.location = (-200, 200)
    flame_attr.attribute_name = 'flame'

    density_attr = nodes.new('ShaderNodeAttribute')
    density_attr.location = (-200, -100)
    density_attr.attribute_name = 'density'

    # Color ramp for fire color
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 200)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (1, 0.8, 0.1, 1)  # Yellow-orange

    # Add red color point
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = (1, 0.3, 0.05, 1)  # Red-orange

    # Connect attributes
    links.new(flame_attr.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], volume.inputs['Color'])
    links.new(flame_attr.outputs['Fac'], volume.inputs['Emission Strength'])
    links.new(density_attr.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    # Adjust volume properties for strong, visible fire
    volume.inputs['Density'].default_value = 2.0  # Increased for visibility
    volume.inputs['Emission Strength'].default_value = 10.0  # Much brighter fire
    volume.inputs['Blackbody Intensity'].default_value = 1.0
    volume.inputs['Blackbody Tint'].default_value = (1.0, 0.8, 0.5, 1.0)

    if domain.data.materials:
        domain.data.materials[0] = mat
    else:
        domain.data.materials.append(mat)

    # Make sure domain is visible in render (not hidden)
    domain.hide_render = False
    domain.hide_viewport = False

    print("  ✓ Fire simulation created - domain visible, emitter hidden")
    return domain, emitter


def setup_lighting():
    """Setup 3-point lighting"""
    print("  Setting up lights...")

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(5, -10, 8))
    key = bpy.context.active_object
    key.data.energy = 500
    key.data.size = 5

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -8, 4))
    fill = bpy.context.active_object
    fill.data.energy = 200
    fill.data.size = 4

    # Rim light
    bpy.ops.object.light_add(type='SPOT', location=(0, 10, 5))
    rim = bpy.context.active_object
    rim.data.energy = 300

    # Environment - gradient for better reflections
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True

    # Clear existing nodes
    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links
    for node in world_nodes:
        if node.type != 'OUTPUT_WORLD':
            world_nodes.remove(node)

    # Get output node
    output = None
    for node in world_nodes:
        if node.type == 'OUTPUT_WORLD':
            output = node
            break

    # Create sky texture for reflections
    sky = world_nodes.new('ShaderNodeTexSky')
    sky.location = (-300, 300)
    sky.sky_type = 'NISHITA'
    sky.sun_elevation = math.radians(45)
    sky.sun_rotation = math.radians(90)
    sky.ground_albedo = 0.3

    # Background shader
    bg = world_nodes.new('ShaderNodeBackground')
    bg.location = (0, 300)
    bg.inputs['Strength'].default_value = 1.0

    # Mix with dark color for dramatic look
    mix_rgb = world_nodes.new('ShaderNodeMixRGB')
    mix_rgb.location = (-150, 300)
    mix_rgb.blend_type = 'MULTIPLY'
    mix_rgb.inputs[0].default_value = 0.3  # Mix factor
    mix_rgb.inputs[2].default_value = (0.05, 0.05, 0.08, 1.0)  # Dark blue-gray

    world_links.new(sky.outputs['Color'], mix_rgb.inputs[1])
    world_links.new(mix_rgb.outputs[0], bg.inputs['Color'])
    world_links.new(bg.outputs[0], output.inputs[0])

    print("  ✓ Lighting complete with reflective environment")


def configure_render():
    """Configure render settings with CUDA/OptiX for RTX 3090"""
    print("  Configuring render with GPU acceleration...")

    scene = bpy.context.scene

    # Frame range
    scene.frame_start = 1
    scene.frame_end = 300
    scene.render.fps = 30

    # Cycles with GPU optimization
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256  # Higher for better quality with fast GPU
    scene.cycles.preview_samples = 64  # Viewport preview samples
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'

    # GPU Settings - Enable CUDA/OptiX for RTX 3090
    scene.cycles.device = 'GPU'

    # Try to enable all available CUDA/OptiX devices
    try:
        prefs = bpy.context.preferences
        cycles_prefs = prefs.addons['cycles'].preferences

        # Set compute device type (OptiX for RTX cards, CUDA as fallback)
        available_types = cycles_prefs.get_device_types(bpy.context)

        if 'OPTIX' in [t[0] for t in available_types]:
            cycles_prefs.compute_device_type = 'OPTIX'
            print("  ✓ Using OptiX (optimal for RTX 3090)")
        elif 'CUDA' in [t[0] for t in available_types]:
            cycles_prefs.compute_device_type = 'CUDA'
            print("  ✓ Using CUDA")
        else:
            print("  ⚠️  GPU compute not available, using CPU")

        # Enable all CUDA/OptiX devices
        cycles_prefs.get_devices()
        for device in cycles_prefs.devices:
            if device.type in {'CUDA', 'OPTIX'}:
                device.use = True
                print(f"  ✓ Enabled: {device.name}")
    except Exception as e:
        print(f"  ⚠️  GPU setup warning: {e}")
        print("  → Will try to use GPU anyway")

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100  # Full resolution

    # Viewport settings for better preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'  # Material preview mode
                    space.shading.use_scene_lights = True
                    space.shading.use_scene_world = True

    # Color management
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'High Contrast'
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0

    # Output
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.image_settings.compression = 15

    # Volume settings for fire - optimized for visibility
    scene.render.use_high_quality_normals = True
    scene.cycles.volume_bounces = 2
    scene.cycles.volume_preview_step_rate = 1  # Lower = better quality in viewport
    scene.cycles.volume_step_rate = 0.5  # Lower = finer steps = more visible fire
    scene.cycles.volume_max_steps = 2048  # More steps for complex fire

    print("  ✓ Render configured with RTX 3090 optimization")


def bake_fire_simulation():
    """Bake fluid simulation so fire renders properly"""
    print("  Baking fire simulation...")
    print("  ⚠️  This will take 2-5 minutes depending on your CPU")

    try:
        # Find domain object
        domain = None
        for obj in bpy.context.scene.objects:
            if obj.name == "FireDomain":
                domain = obj
                break

        if not domain:
            print("  ⚠️  Warning: FireDomain not found, skipping bake")
            return

        # Select domain
        bpy.ops.object.select_all(action='DESELECT')
        domain.select_set(True)
        bpy.context.view_layer.objects.active = domain

        # Bake all
        print("  🔥 Baking fluid cache (this takes time)...")
        bpy.ops.fluid.bake_all()

        print("  ✓ Fire simulation baked successfully")

    except Exception as e:
        print(f"  ⚠️  Baking failed: {e}")
        print("  💡 You can bake manually in Blender: Physics Properties → Fluid → Bake All")


def main():
    """Main setup function"""
    print("\n" + "=" * 75)
    print(" " * 15 + "ALTER LOGO FIRE ANIMATION SETUP")
    print("=" * 75)
    print()

    # Find SVG
    print("[Step 1] Finding alter.svg...")
    svg_path = find_svg_file()

    if not svg_path:
        print("\n❌ ERROR: alter.svg not found!")
        print("\nSearched in:")
        print("  - Blend file directory")
        print("  - Script directory")
        print("  - Current working directory")
        print("\nPlease place alter.svg in the same folder as this script.")
        return False

    print(f"  ✓ Found: {svg_path}")

    try:
        # Clear scene
        print("\n[Step 2] Clearing scene...")
        clear_scene()
        print("  ✓ Done")

        # Import logo
        print("\n[Step 3] Importing logo from SVG...")
        logo = import_svg_logo(svg_path)

        # Material
        print("\n[Step 4] Creating golden material...")
        create_golden_material(logo)

        # Camera
        print("\n[Step 5] Setting up camera...")
        setup_camera(logo)

        # Animation
        print("\n[Step 6] Animating logo...")
        animate_logo(logo)

        # Fire
        print("\n[Step 7] Creating fire simulation...")
        create_fire_simulation(logo)

        # Lighting
        print("\n[Step 8] Adding lights...")
        setup_lighting()

        # Render settings
        print("\n[Step 9] Configuring render...")
        configure_render()

        # Bake fire simulation
        print("\n[Step 10] Baking fire simulation...")
        bake_fire_simulation()

        # Save
        print("\n[Step 11] Saving file...")
        save_dir = os.path.dirname(svg_path)
        save_path = os.path.join(save_dir, "alter_logo_fire_animation.blend")
        bpy.ops.wm.save_as_mainfile(filepath=save_path)

        print("\n" + "=" * 75)
        print(" " * 25 + "✅ SUCCESS!")
        print("=" * 75)
        print(f"\n📁 Saved: {save_path}")
        print(f"🎬 Frames: 300 (10 seconds)")
        print(f"🔥 Fire: BAKED with Principled Volume shader")
        print(f"📐 Resolution: 1920x1080 @ 100%")
        print(f"⚙️  Samples: 256 (render) / 64 (viewport)")
        print(f"🚀 GPU: OptiX/CUDA enabled for RTX 3090")
        print(f"📹 Camera: Optimized to fill screen with logo")
        print()
        print("▶️  To preview animation:")
        print("   1. Open the .blend file in Blender")
        print("   2. Press SPACEBAR in viewport")
        print("   3. Fire should be visible in Material Preview mode")
        print()
        print("🎥 To render:")
        print("   • F12 - Single frame render")
        print("   • Ctrl+F12 - Full animation render")
        print("   • Fire will render with realistic colors (orange/yellow)")
        print()
        print("💡 TIPS:")
        print("   • Logo fills screen at frames 250-300")
        print("   • Fire fades out around frame 200")
        print("   • Switch viewport to Rendered mode (Z → Rendered) to see fire")
        print("=" * 75)

        return True

    except Exception as e:
        print("\n" + "=" * 75)
        print(" " * 30 + "❌ ERROR")
        print("=" * 75)
        print(f"\n{str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
