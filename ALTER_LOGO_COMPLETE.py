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

    # Add minimal depth for 3D feel
    logo.data.extrude = 0.03  # Very subtle depth
    logo.data.bevel_depth = 0.01  # Minimal bevel
    logo.data.bevel_resolution = 4

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

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.15
    bsdf.inputs['Specular IOR Level'].default_value = 0.8

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
    """Setup camera with tracking"""
    print("  Setting up camera...")

    bpy.ops.object.camera_add(location=(0, -25, 2))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    camera.data.lens = 50
    camera.data.dof.use_dof = True
    camera.data.dof.aperture_fstop = 2.8
    camera.data.dof.focus_distance = 25

    # Track logo
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = logo
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    bpy.context.scene.camera = camera
    print("  ✓ Camera configured")
    return camera


def animate_logo(logo):
    """Animate logo movement - straight to camera, no rotation"""
    print("  Animating logo...")

    # Start far
    logo.location = (0, 15, 0)
    logo.keyframe_insert(data_path="location", frame=1)

    # End near
    logo.location = (0, -5, 0)
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

    # Domain
    bpy.ops.mesh.primitive_cube_add(size=12, location=(0, 5, 0))
    domain = bpy.context.active_object
    domain.name = "FireDomain"

    # Add fluid modifier
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    # Configure domain
    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 128  # Lower for speed

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

    # Cache
    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = 300

    # Emitter (torus around logo)
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        rotation=(math.radians(90), 0, 0),
        major_radius=3.5,
        minor_radius=0.8
    )
    emitter = bpy.context.active_object
    emitter.name = "FireEmitter"

    # Parent to logo
    emitter.parent = logo
    emitter.matrix_parent_inverse = logo.matrix_world.inverted()

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

    # Animate fire fade
    try:
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=1)
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=170)
        flow.density = 0.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=200)
    except (AttributeError, TypeError):
        # Keyframing might not work, try simple approach
        pass

    emitter.hide_render = True

    # Fire material
    mat = bpy.data.materials.new(name="FireMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs['Strength'].default_value = 20.0
    emission.inputs['Color'].default_value = (1.0, 0.5, 0.1, 1.0)

    links.new(emission.outputs['Emission'], output.inputs['Volume'])

    if domain.data.materials:
        domain.data.materials[0] = mat
    else:
        domain.data.materials.append(mat)

    print("  ✓ Fire simulation created")
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

    # Environment
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.05, 0.05, 0.08, 1.0)
    bg.inputs['Strength'].default_value = 0.5

    print("  ✓ Lighting complete")


def configure_render():
    """Configure render settings"""
    print("  Configuring render...")

    scene = bpy.context.scene

    # Frame range
    scene.frame_start = 1
    scene.frame_end = 300
    scene.render.fps = 30

    # Cycles
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.cycles.device = 'GPU'

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    # Color management
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'High Contrast'

    # Output
    scene.render.image_settings.file_format = 'PNG'

    print("  ✓ Render configured")


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

        # Save
        print("\n[Step 10] Saving file...")
        save_dir = os.path.dirname(svg_path)
        save_path = os.path.join(save_dir, "alter_logo_fire_animation.blend")
        bpy.ops.wm.save_as_mainfile(filepath=save_path)

        print("\n" + "=" * 75)
        print(" " * 25 + "✅ SUCCESS!")
        print("=" * 75)
        print(f"\n📁 Saved: {save_path}")
        print(f"🎬 Frames: 300 (10 seconds)")
        print(f"🔥 Fire: Yes (fades at frame 200)")
        print(f"📐 Resolution: 1920x1080")
        print(f"⚙️  Samples: 128")
        print()
        print("▶️  To preview: Press SPACEBAR in viewport")
        print("🎥 To render: Press Ctrl+F12")
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
