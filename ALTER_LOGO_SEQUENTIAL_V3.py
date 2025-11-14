"""
═══════════════════════════════════════════════════════════════════════════════
ALTER LOGO - SEQUENTIAL FIRE ANIMATION V3 (BUILT FROM SCRATCH)
═══════════════════════════════════════════════════════════════════════════════

CLEAN REWRITE using ALL knowledge from ALTER_LOGO_COMPLETE.py

REQUIREMENTS:
- Elements arrive SEQUENTIALLY, all finish by frame 200
- Fire FROM START, extinguishes in last 2 seconds (frame 180-240)
- Logo elements: ALTER EGO BEND + violinski kljuc + krila + BANJA LUKA
- Logo 2/3 screen in final position
- Camera clip_end to hide starting position
- Alpha channel for Premiere

═══════════════════════════════════════════════════════════════════════════════
"""

import bpy
import os
import math


def clean_scene():
    """Remove all objects"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Clean orphaned data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.curves:
        if block.users == 0:
            bpy.data.curves.remove(block)


def import_svg_and_separate(svg_path):
    """
    Import SVG, join all curves, convert to mesh, separate by loose parts
    Returns list of separate elements
    """
    print(f"\nImporting SVG: {svg_path}")

    # Import SVG
    objects_before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=svg_path)
    objects_after = set(bpy.data.objects)

    imported = list(objects_after - objects_before)
    curves = [obj for obj in imported if obj.type == 'CURVE']

    if not curves:
        print("ERROR: No curves imported")
        return []

    print(f"  Imported {len(curves)} curves")

    # Select all curves and join
    bpy.ops.object.select_all(action='DESELECT')
    for obj in curves:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = curves[0]

    if len(curves) > 1:
        bpy.ops.object.join()

    logo = bpy.context.active_object
    logo.name = "LogoUnified"

    # Set geometry - NO bevel, small extrude
    logo.data.extrude = 0.005
    logo.data.bevel_depth = 0.0

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')

    # Center, scale, rotate to face camera
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    logo.location = (0, 0, 0)
    logo.scale = (2.5, 2.5, 2.5)
    bpy.ops.object.transform_apply(scale=True)
    logo.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    # Separate by loose parts
    bpy.ops.mesh.separate(type='LOOSE')

    # Get separated elements
    elements = [obj for obj in bpy.context.selected_objects]

    print(f"  Separated into {len(elements)} elements")

    # Apply golden material to all elements
    mat = create_golden_material()
    for elem in elements:
        if elem.data.materials:
            elem.data.materials[0] = mat
        else:
            elem.data.materials.append(mat)

    return elements


def create_golden_material():
    """Golden metallic material with glow"""
    mat = bpy.data.materials.new(name="GoldenMetal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (200, 0)
    mix.inputs[0].default_value = 0.85  # 85% metallic, 15% emission

    # Metallic gold
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 100)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.1

    # Emission glow
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, -100)
    emission.inputs['Color'].default_value = (1.0, 0.85, 0.4, 1.0)
    emission.inputs['Strength'].default_value = 0.8

    links.new(bsdf.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])

    return mat


def animate_elements_sequential(elements, total_frames=240):
    """
    Animate elements sequentially toward camera
    All arrive by frame 200
    """
    print("\nAnimating elements sequentially...")

    num_elements = len(elements)
    frames_per_element = 30  # Each element takes 1 second to travel
    last_arrival = 200

    # Calculate spacing
    if num_elements > 1:
        first_start = 1
        last_start = last_arrival - frames_per_element
        gap = (last_start - first_start) / (num_elements - 1)
    else:
        first_start = 1
        gap = 0

    print(f"  {num_elements} elements, gap: {gap:.1f} frames")

    for i, elem in enumerate(elements):
        start_frame = first_start + int(i * gap)
        end_frame = start_frame + frames_per_element

        # Get current position
        final_x = elem.location.x
        final_y = elem.location.y
        final_z = elem.location.z

        # Move to starting position (far from camera)
        start_y = 20.0
        elem.location.y = start_y
        elem.keyframe_insert(data_path='location', frame=start_frame)

        # Move to final position (near camera)
        elem.location.y = final_y
        elem.keyframe_insert(data_path='location', frame=end_frame)

        # Smooth interpolation
        if elem.animation_data:
            for fcurve in elem.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'

        print(f"    Element {i}: frames {start_frame}-{end_frame}")

    # Fire timing
    fire_end_frame = 180  # Fire extinguishes at frame 180

    return fire_end_frame


def create_fire_system(elements, fire_end_frame, total_frames):
    """
    Create fire domain + one emitter per element
    EXACT copy of approach from ALTER_LOGO_COMPLETE.py
    """
    print("\nCreating fire system...")

    # DOMAIN - fixed size covering animation path
    bpy.ops.mesh.primitive_cube_add(size=25, location=(0, 9, 0))
    domain = bpy.context.active_object
    domain.name = "FireDomain"
    domain.display_type = 'WIRE'

    # Configure domain
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 128  # Lower for speed

    # Fire settings
    try:
        domain_settings.use_noise = False  # Faster without noise
    except:
        pass

    try:
        domain_settings.use_fire = True
    except:
        pass

    try:
        domain_settings.vorticity = 0.3
    except:
        pass

    # Cache
    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = total_frames

    # Fire material
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

    # EMITTERS - one per element, parented to element
    print(f"  Creating {len(elements)} fire emitters...")

    for i, elem in enumerate(elements):
        # Duplicate element
        bpy.ops.object.select_all(action='DESELECT')
        elem.select_set(True)
        bpy.context.view_layer.objects.active = elem
        bpy.ops.object.duplicate()

        emitter = bpy.context.active_object
        emitter.name = f"FireEmitter_{i:02d}"

        # Add wireframe modifier
        wireframe_mod = emitter.modifiers.new(name="Wireframe", type='WIREFRAME')
        wireframe_mod.thickness = 0.08
        wireframe_mod.use_replace = True
        wireframe_mod.use_boundary = True
        wireframe_mod.use_even_offset = True

        # Apply wireframe
        bpy.ops.object.convert(target='MESH')

        # Parent to element so it moves with it
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
        except:
            pass

        try:
            flow.temperature = 3.0
        except:
            pass

        # Animate fire - ON from start, OFF at fire_end_frame
        try:
            flow.density = 1.0
            emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=1)
            flow.density = 1.0
            emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=fire_end_frame)
            flow.density = 0.0
            emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=fire_end_frame + 30)
        except:
            pass

        # Hide emitter
        emitter.hide_render = True
        emitter.hide_viewport = True
        emitter.display_type = 'WIRE'

    print(f"  ✓ Created {len(elements)} emitters (parented to elements)")


def setup_camera_and_lights():
    """Camera positioned for 2/3 screen logo, clip_end to hide starting position"""
    print("\nSetting up camera and lights...")

    # Camera - closer for 2/3 screen, clip_end to hide start position
    bpy.ops.object.camera_add(location=(0, -6, 1))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (math.radians(90), 0, 0)
    camera.data.clip_end = 12  # Elements start at Y=20, this hides them
    bpy.context.scene.camera = camera

    print(f"  Camera: location=(0, -6, 1), clip_end=12")

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(5, -8, 6))
    key = bpy.context.active_object
    key.data.energy = 800
    key.data.size = 6

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-4, -6, 3))
    fill = bpy.context.active_object
    fill.data.energy = 300
    fill.data.size = 5

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 4, 4))
    rim = bpy.context.active_object
    rim.data.energy = 400
    rim.data.size = 4

    print("  ✓ Camera and lights ready")


def setup_render(total_frames):
    """Render settings with alpha channel"""
    print("\nConfiguring render...")

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = 30

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Alpha channel
    scene.render.film_transparent = True

    # Volume rendering settings
    try:
        scene.cycles.volume_step_rate = 0.5
        scene.cycles.volume_bounces = 2
        scene.cycles.volume_max_steps = 256
    except:
        pass

    # Output
    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    output_dir = os.path.join(blend_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "frame_")
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    print("  ✓ Render configured (1920x1080, alpha channel, PNG)")


def set_viewport_camera():
    """Set viewport to camera view, rendered mode"""
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
    print("ALTER LOGO SEQUENTIAL ANIMATION V3 - CLEAN REWRITE")
    print("="*80)

    # Find SVG
    svg_path = os.path.join(os.path.dirname(__file__), "alter.svg")
    if not os.path.exists(svg_path):
        print(f"ERROR: alter.svg not found at {svg_path}")
        return False

    print(f"✓ SVG found: {svg_path}")

    # Clean scene
    clean_scene()

    # Import and separate
    elements = import_svg_and_separate(svg_path)
    if not elements:
        print("ERROR: No elements created")
        return False

    # Animate elements sequentially
    total_frames = 240
    fire_end_frame = animate_elements_sequential(elements, total_frames)

    # Create fire system
    create_fire_system(elements, fire_end_frame, total_frames)

    # Camera and lights
    setup_camera_and_lights()

    # Render settings
    setup_render(total_frames)

    # Set viewport
    set_viewport_camera()

    # Set to frame 1
    bpy.context.scene.frame_set(1)

    # Save
    blend_dir = os.path.dirname(__file__)
    blend_path = os.path.join(blend_dir, "alter_logo_sequential_v3.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    print("\n" + "="*80)
    print("✓ SETUP COMPLETE!")
    print("="*80)
    print("\nNEXT STEPS:")
    print("1. Press SPACEBAR to bake fire simulation")
    print("2. Wait for baking to complete")
    print("3. Play animation to see fire")
    print("4. Render if satisfied")
    print(f"\nSaved: {blend_path}")
    print("="*80 + "\n")

    return True


if __name__ == "__main__":
    main()
