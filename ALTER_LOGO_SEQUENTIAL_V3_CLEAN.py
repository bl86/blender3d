"""
═══════════════════════════════════════════════════════════════════════════════
ALTER LOGO SEQUENTIAL V3 - FINAL CLEAN VERSION
═══════════════════════════════════════════════════════════════════════════════

STRATEGY:
1. Use EXACT fire setup from ALTER_LOGO_COMPLETE.py (ONE emitter, proven to work)
2. Separate logo for animation AFTER fire emitter is created
3. Each element gets animated separately
4. ONE unified emitter stays at final position, elements move through it

This ensures fire setup is EXACTLY like working version.
═══════════════════════════════════════════════════════════════════════════════
"""

import bpy
import os
import math


def clean_scene():
    """Remove everything"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.curves:
        if block.users == 0:
            bpy.data.curves.remove(block)


def import_and_join_svg(svg_path):
    """
    Import SVG and join into ONE object
    EXACT same as ALTER_LOGO_COMPLETE.py
    """
    print(f"\nImporting SVG: {svg_path}")

    objects_before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=svg_path)
    objects_after = set(bpy.data.objects)

    imported = list(objects_after - objects_before)
    curves = [obj for obj in imported if obj.type == 'CURVE']

    if not curves:
        print("ERROR: No curves imported")
        return None

    print(f"  Imported {len(curves)} curves")

    # Select all and join
    bpy.ops.object.select_all(action='DESELECT')
    for obj in curves:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = curves[0]

    if len(curves) > 1:
        bpy.ops.object.join()

    logo = bpy.context.active_object
    logo.name = "AlterLogo"

    # Geometry settings - EXACT same as COMPLETE
    logo.data.extrude = 0.005
    logo.data.bevel_depth = 0.0
    logo.data.bevel_resolution = 0

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')

    logo = bpy.context.active_object
    logo.name = "AlterLogo"

    # Center, scale, rotate - EXACT same as COMPLETE
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    logo.location = (0, 0, 0)
    logo.scale = (2.5, 2.5, 2.5)
    bpy.ops.object.transform_apply(scale=True)
    logo.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    print(f"  ✓ Logo imported and prepared")

    return logo


def create_fire_emitters_for_elements(elements):
    """
    Create ONE emitter PER element, PARENTED to element
    So emitter moves WITH element as it travels
    """
    print("\nCreating fire emitters...")

    emitters = []

    for i, elem in enumerate(elements):
        # Duplicate element for emitter
        bpy.ops.object.select_all(action='DESELECT')
        elem.select_set(True)
        bpy.context.view_layer.objects.active = elem
        bpy.ops.object.duplicate()

        emitter = bpy.context.active_object
        emitter.name = f"FireEmitter_{i:02d}"

        # Wireframe modifier
        wireframe_mod = emitter.modifiers.new(name="Wireframe", type='WIREFRAME')
        wireframe_mod.thickness = 0.08
        wireframe_mod.use_replace = True
        wireframe_mod.use_boundary = True
        wireframe_mod.use_even_offset = True

        # Apply wireframe
        bpy.ops.object.convert(target='MESH')

        # PARENT to element so it moves WITH element
        emitter.parent = elem
        emitter.matrix_parent_inverse = elem.matrix_world.inverted()

        # Add fluid flow
        bpy.ops.object.modifier_add(type='FLUID')
        emitter.modifiers["Fluid"].fluid_type = 'FLOW'
        flow = emitter.modifiers["Fluid"].flow_settings
        flow.flow_type = 'FIRE'
        flow.flow_behavior = 'INFLOW'

        try:
            flow.fuel_amount = 2.0
        except AttributeError:
            pass

        try:
            flow.temperature = 3.0
        except AttributeError:
            pass

        # Animate fire - ON from start, OFF at frame 180
        try:
            flow.density = 1.0
            emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=1)
            flow.density = 1.0
            emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=180)
            flow.density = 0.0
            emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=210)
        except (AttributeError, TypeError):
            pass

        # Hide emitter
        emitter.hide_render = True
        emitter.hide_viewport = True
        emitter.display_type = 'WIRE'

        emitters.append(emitter)

    print(f"  ✓ Created {len(emitters)} emitters (parented to elements)")

    return emitters


def create_fire_domain():
    """
    Create fire domain - EXACT copy from ALTER_LOGO_COMPLETE.py
    """
    print("\nCreating fire domain...")

    # Domain covers Y: 20 to -2 (elements path) = size 25, center at Y=9
    bpy.ops.mesh.primitive_cube_add(size=25, location=(0, 9, 0))
    domain = bpy.context.active_object
    domain.name = "FireDomain"
    domain.display_type = 'WIRE'

    # Add fluid modifier
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    # Settings - EXACT same as COMPLETE
    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 128  # Lower for speed

    try:
        domain_settings.use_noise = False  # Faster
    except:
        pass

    try:
        domain_settings.use_fire = True
    except AttributeError:
        pass

    try:
        domain_settings.vorticity = 0.3
    except AttributeError:
        pass

    # Cache
    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = 240

    # Fire material - EXACT same as COMPLETE
    mat = bpy.data.materials.new(name="FireMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (200, 0)

    flame_attr = nodes.new('ShaderNodeAttribute')
    flame_attr.location = (-200, 200)
    flame_attr.attribute_name = 'flame'

    density_attr = nodes.new('ShaderNodeAttribute')
    density_attr.location = (-200, -100)
    density_attr.attribute_name = 'density'

    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 200)
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].color = (1, 0.8, 0.1, 1)
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = (1, 0.3, 0.05, 1)

    links.new(flame_attr.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], volume.inputs['Color'])
    links.new(flame_attr.outputs['Fac'], volume.inputs['Emission Strength'])
    links.new(density_attr.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    volume.inputs['Density'].default_value = 2.0
    volume.inputs['Emission Strength'].default_value = 10.0
    volume.inputs['Blackbody Intensity'].default_value = 1.0

    domain.data.materials.append(mat)

    print("  ✓ Fire domain created")

    return domain


def separate_logo(logo):
    """
    Separate logo into elements (but don't animate yet)
    """
    print("\nSeparating logo into elements...")

    # Make sure logo is selected
    bpy.ops.object.select_all(action='DESELECT')
    logo.select_set(True)
    bpy.context.view_layer.objects.active = logo

    # Separate by loose parts
    bpy.ops.mesh.separate(type='LOOSE')

    elements = list(bpy.context.selected_objects)

    print(f"  Separated into {len(elements)} elements")

    return elements


def animate_elements_sequential(elements):
    """
    Animate elements sequentially
    """
    print("\nAnimating elements sequentially...")

    num_elements = len(elements)
    frames_per_element = 30
    last_arrival = 200

    first_start = 1
    last_start = last_arrival - frames_per_element
    gap = (last_start - first_start) / (num_elements - 1) if num_elements > 1 else 0

    # Create golden material
    mat = bpy.data.materials.new(name="GoldenMetal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (200, 0)
    mix.inputs[0].default_value = 0.85

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 100)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.1

    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, -100)
    emission.inputs['Color'].default_value = (1.0, 0.85, 0.4, 1.0)
    emission.inputs['Strength'].default_value = 0.8

    links.new(bsdf.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])

    # Apply material and animate
    for i, elem in enumerate(elements):
        # Apply material
        if elem.data.materials:
            elem.data.materials[0] = mat
        else:
            elem.data.materials.append(mat)

        # Animate
        start_frame = first_start + int(i * gap)
        end_frame = start_frame + frames_per_element

        final_x = elem.location.x
        final_y = elem.location.y
        final_z = elem.location.z

        # Start position (far from camera)
        elem.location.y = 20.0
        elem.keyframe_insert(data_path='location', frame=start_frame)

        # End position (near camera at final Y)
        elem.location.y = final_y
        elem.keyframe_insert(data_path='location', frame=end_frame)

        # Smooth interpolation
        if elem.animation_data:
            for fcurve in elem.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'

        print(f"    Element {i}: frames {start_frame}-{end_frame}, Y: 20.0→{final_y:.2f}")

    print(f"  ✓ All {num_elements} elements animated")

    return elements


def setup_camera():
    """Setup camera for 2/3 screen logo"""
    print("\nSetting up camera...")

    bpy.ops.object.camera_add(location=(0, -6, 1))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (math.radians(90), 0, 0)
    camera.data.clip_end = 12
    bpy.context.scene.camera = camera

    print("  ✓ Camera at (0, -6, 1), clip_end=12")

    return camera


def setup_lights():
    """Setup 3-point lighting"""
    print("\nSetting up lights...")

    bpy.ops.object.light_add(type='AREA', location=(5, -8, 6))
    key = bpy.context.active_object
    key.data.energy = 800
    key.data.size = 6

    bpy.ops.object.light_add(type='AREA', location=(-4, -6, 3))
    fill = bpy.context.active_object
    fill.data.energy = 300
    fill.data.size = 5

    bpy.ops.object.light_add(type='AREA', location=(0, 4, 4))
    rim = bpy.context.active_object
    rim.data.energy = 400
    rim.data.size = 4

    print("  ✓ Lights ready")


def setup_render():
    """Setup render with alpha"""
    print("\nSetting up render...")

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 240
    scene.render.fps = 30

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    scene.render.film_transparent = True

    try:
        scene.cycles.volume_step_rate = 0.5
        scene.cycles.volume_bounces = 2
        scene.cycles.volume_max_steps = 256
    except:
        pass

    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    output_dir = os.path.join(blend_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "frame_")
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    print("  ✓ Render configured (alpha channel)")


def set_viewport_camera():
    """Set viewport to camera, rendered mode"""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.region_3d.view_perspective = 'CAMERA'
                    space.shading.type = 'RENDERED'
                    space.lock_camera = True
                    break


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("ALTER LOGO SEQUENTIAL V3 - CLEAN FINAL VERSION")
    print("="*80)

    svg_path = os.path.join(os.path.dirname(__file__), "alter.svg")
    if not os.path.exists(svg_path):
        print(f"ERROR: alter.svg not found")
        return False

    print(f"✓ SVG: {svg_path}")

    # Clean
    clean_scene()

    # Import and join
    logo = import_and_join_svg(svg_path)
    if not logo:
        return False

    # Separate into elements (BEFORE creating emitters)
    elements = separate_logo(logo)

    # Animate elements (BEFORE creating emitters so they're in final position)
    elements = animate_elements_sequential(elements)

    # Create fire emitters (ONE per element, parented)
    emitters = create_fire_emitters_for_elements(elements)

    # Create fire domain
    domain = create_fire_domain()

    # Camera and lights
    setup_camera()
    setup_lights()

    # Render
    setup_render()

    # Viewport
    set_viewport_camera()

    # Set to frame 1
    bpy.context.scene.frame_set(1)

    # Save
    blend_dir = os.path.dirname(__file__)
    blend_path = os.path.join(blend_dir, "alter_logo_sequential_v3_clean.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    print("\n" + "="*80)
    print("✓ SETUP COMPLETE!")
    print("="*80)
    print("\nKEY POINTS:")
    print("  • Fire emitter at Y=0 (final position)")
    print("  • Elements move from Y=20 to Y=0 through emitter")
    print("  • As elements pass through emitter, they ignite")
    print("  • Fire setup EXACT copy from ALTER_LOGO_COMPLETE.py")
    print("\nNEXT:")
    print("  1. Press SPACEBAR to bake fire")
    print("  2. Play animation")
    print(f"\nSaved: {blend_path}")
    print("="*80 + "\n")

    return True


if __name__ == "__main__":
    main()
