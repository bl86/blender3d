#!/usr/bin/env python3
"""
ALTER Logo Sequential Animation - Elements arrive one by one
NO FLUID BAKING - Uses fast emission shader fire
Preserves exact SVG layout positions
"""

import bpy
import os
import sys
from mathutils import Vector

def clean_scene():
    """Remove all objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clean materials
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

    print("✓ Scene cleaned")


def import_svg_as_one_logo(svg_path):
    """
    Import SVG exactly like ALTER_LOGO_COMPLETE.py does
    Join all curves into ONE object, center it, then separate for sequential
    """
    if not os.path.exists(svg_path):
        print(f"✗ SVG not found: {svg_path}")
        return None

    # Store existing objects
    existing_objects = set(bpy.context.scene.objects)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Import SVG
    result = bpy.ops.import_curve.svg(filepath=svg_path)

    if result != {'FINISHED'}:
        print("✗ SVG import failed")
        return None

    # Find new objects
    new_objects = set(bpy.context.scene.objects) - existing_objects
    curves = [obj for obj in new_objects if obj.type == 'CURVE']

    if not curves:
        print("✗ No curves found after import")
        return None

    print(f"✓ Imported {len(curves)} curve(s)")

    # Select all curves
    for obj in curves:
        obj.select_set(True)

    # Set active
    bpy.context.view_layer.objects.active = curves[0]

    # JOIN all curves into ONE object (like ALTER_LOGO_COMPLETE)
    if len(curves) > 1:
        print(f"  Joining {len(curves)} curves into one logo...")
        bpy.ops.object.join()

    logo = bpy.context.active_object
    logo.name = "AlterLogoUnified"

    # Add minimal extrude
    logo.data.extrude = 0.005
    logo.data.bevel_depth = 0.0
    logo.data.bevel_resolution = 0

    # Convert to mesh
    print("  Converting to mesh...")
    bpy.ops.object.convert(target='MESH')

    logo = bpy.context.active_object
    logo.name = "AlterLogoUnified"

    # Center and scale (like ALTER_LOGO_COMPLETE)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    logo.location = (0, 0, 0)
    logo.scale = (2.5, 2.5, 2.5)
    bpy.ops.object.transform_apply(scale=True)

    # Rotate to face camera
    logo.rotation_euler = (1.5708, 0, 0)  # 90 degrees X
    bpy.ops.object.transform_apply(rotation=True)

    print(f"  ✓ Unified logo ready: {logo.name}")
    return logo


def separate_logo_into_elements(logo):
    """
    Separate the unified logo into individual elements by loose parts
    Each loose part becomes a separate object for sequential animation
    """
    print("\n  Separating logo into elements...")

    # Select and set active
    bpy.ops.object.select_all(action='DESELECT')
    logo.select_set(True)
    bpy.context.view_layer.objects.active = logo

    # Separate by loose parts
    bpy.ops.mesh.separate(type='LOOSE')

    # Get all objects that were created from separation
    elements = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    print(f"  ✓ Separated into {len(elements)} elements")

    # Name them
    for i, elem in enumerate(elements):
        elem.name = f"LogoElement_{i}"
        print(f"    Element {i}: {elem.name} at {elem.location}")

        # Add solidify for better thickness
        solidify = elem.modifiers.new(name="Solidify", type='SOLIDIFY')
        solidify.thickness = 0.05
        solidify.offset = 0

    return elements


def create_fire_domain(total_frames):
    """
    Create FLUID domain for fire simulation
    ONE domain for all sequential elements
    Adapted from ALTER_LOGO_COMPLETE.py
    """
    print("  Creating fire domain...")

    # Domain - large enough to cover all elements
    # Positioned at center (0, 0, 0) to cover all animated elements
    bpy.ops.mesh.primitive_cube_add(size=20, location=(0, 0, 0))
    domain = bpy.context.active_object
    domain.name = "FireDomain"
    domain.display_type = 'WIRE'  # Show as wireframe in viewport

    # Add fluid modifier
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    # Configure domain
    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 128  # Reduced from 256 for faster baking

    # Noise settings (optional - can disable for speed)
    try:
        domain_settings.use_noise = False  # Disabled for faster baking
        domain_settings.noise_scale = 2
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
        domain_settings.vorticity = 0.3
    except AttributeError:
        pass  # vorticity might not be available

    # Cache - bake for entire animation
    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = total_frames

    # Fire material using Principled Volume
    mat = bpy.data.materials.new(name="FireMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Principled Volume - proper fire/smoke rendering
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
    volume.inputs['Density'].default_value = 2.0
    volume.inputs['Emission Strength'].default_value = 10.0
    volume.inputs['Blackbody Intensity'].default_value = 1.0
    volume.inputs['Blackbody Tint'].default_value = (1.0, 0.8, 0.5, 1.0)

    # Apply material to domain
    if domain.data.materials:
        domain.data.materials[0] = mat
    else:
        domain.data.materials.append(mat)

    # Make sure domain is visible in render
    domain.hide_render = False
    domain.hide_viewport = False

    print("  ✓ Fire domain created (FLUID simulation)")
    return domain


def create_fire_emitter_for_element(element, index, start_frame, end_frame):
    """
    Create FLUID fire emitter for one element
    Emitter follows element and has timed fire flow
    Adapted from ALTER_LOGO_COMPLETE.py
    """
    # Duplicate element for fire emitter
    bpy.ops.object.select_all(action='DESELECT')
    element.select_set(True)
    bpy.context.view_layer.objects.active = element
    bpy.ops.object.duplicate()

    emitter = bpy.context.active_object
    emitter.name = f"FireEmitter_{index}"

    # Add Wireframe modifier to emit fire from element edges/contours
    wireframe_mod = emitter.modifiers.new(name="Wireframe", type='WIREFRAME')
    wireframe_mod.thickness = 0.08  # Thin wireframe around element contours
    wireframe_mod.use_replace = True  # Replace mesh with wireframe
    wireframe_mod.use_boundary = True  # Include boundary edges
    wireframe_mod.use_even_offset = True

    # Apply modifiers so fluid system sees the wireframe
    bpy.ops.object.convert(target='MESH')

    # Parent to element so it follows
    emitter.parent = element
    emitter.matrix_parent_inverse = element.matrix_world.inverted()

    # Add FLUID flow (must be done BEFORE hiding the object)
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

    # Animate fire timing - fire appears during element animation
    try:
        # Fire starts when element starts moving
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=start_frame)

        # Fire stays during animation
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=end_frame)

        # Fire fades shortly after element arrives
        flow.density = 0.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=end_frame + 30)
    except (AttributeError, TypeError):
        # Keyframing might not work, fire will stay on throughout
        pass

    # Hide emitter completely - don't want to see wireframe (AFTER adding modifiers)
    emitter.hide_render = True
    emitter.hide_viewport = True
    emitter.display_type = 'WIRE'  # Show only wireframe if visible

    print(f"    ✓ FLUID emitter {index} created (frames {start_frame}-{end_frame+30})")

    return emitter


def animate_sequential(elements):
    """
    Animate elements arriving one by one
    Elements start FAR on Y axis, arrive at current position
    Only Y axis moves - X and Z stay as imported from SVG
    Returns: (total_frames, element_timings)
    """
    start_y_offset = -50.0  # How far to push elements back
    duration = 40  # Frames for each element to arrive
    gap = 25  # Gap between element starts

    print("\n✓ Animating elements sequentially:")

    element_timings = []  # Track (start_frame, end_frame) for each element

    for i, element in enumerate(elements):
        # Get current position (where SVG import placed it)
        current_x = element.location.x
        current_y = element.location.y
        current_z = element.location.z

        # Frame timing
        start_frame = 1 + (i * gap)
        end_frame = start_frame + duration
        element_timings.append((start_frame, end_frame))

        print(f"  Element {i}: frames {start_frame}-{end_frame}")
        print(f"    Current pos: X={current_x:.3f}, Y={current_y:.3f}, Z={current_z:.3f}")
        print(f"    Will move from Y={current_y + start_y_offset:.3f} to Y={current_y:.3f}")

        # START position - pushed back on Y axis only
        element.location.x = current_x  # Keep X
        element.location.y = current_y + start_y_offset  # Push back
        element.location.z = current_z  # Keep Z
        element.keyframe_insert(data_path='location', frame=start_frame)

        # END position - back to where it was after SVG import
        element.location.x = current_x  # Keep X
        element.location.y = current_y  # Return to original Y
        element.location.z = current_z  # Keep Z
        element.keyframe_insert(data_path='location', frame=end_frame)

        # Smooth animation
        if element.animation_data:
            for fcurve in element.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.easing = 'EASE_IN_OUT'

    # Calculate total frames
    total_frames = end_frame + 100
    bpy.context.scene.frame_end = total_frames

    print(f"\n✓ Animation setup complete - {total_frames} frames total")

    return total_frames, element_timings


def create_banja_luka_text():
    """Create BANJA LUKA text at bottom"""
    bpy.ops.object.text_add(location=(0, 0, -4))
    text_obj = bpy.context.active_object
    text_obj.name = "BanjaLuka"
    text_obj.data.body = "BANJA LUKA"
    text_obj.data.size = 1.0
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'

    # Ensure proper selection for convert
    bpy.ops.object.select_all(action='DESELECT')
    text_obj.select_set(True)
    bpy.context.view_layer.objects.active = text_obj

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')

    # Solidify
    solidify = text_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = 0.1

    print("✓ BANJA LUKA text created at (0, 0, -4)")

    return text_obj


def create_logo_material():
    """Create material for logo elements"""
    mat = bpy.data.materials.new(name="LogoMaterial")
    mat.use_nodes = True
    mat.metallic = 0.8
    mat.roughness = 0.2

    # Set base color to silver/chrome
    mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.9, 0.9, 0.95, 1.0)

    return mat


def setup_scene(total_frames):
    """Setup camera, lighting, and render settings"""
    scene = bpy.context.scene

    # Camera
    bpy.ops.object.camera_add(location=(0, -15, 0))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.5708, 0, 0)  # 90 degrees on X
    scene.camera = camera

    # Lights
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 2.0
    sun.data.angle = 0.1

    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    area = bpy.context.active_object
    area.data.energy = 300
    area.data.size = 10

    # World - black background
    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0, 0, 0, 1)
    bg.inputs['Strength'].default_value = 0

    # Render settings
    scene.render.engine = 'CYCLES'
    scene.render.film_transparent = True
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = total_frames

    # Output path - save in 'output' folder next to blend file (Windows compatible)
    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    output_dir = os.path.join(blend_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "frame_")
    scene.render.image_settings.file_format = 'PNG'

    print(f"  ✓ Render output: {output_dir}")
    print("  ✓ Render engine: CYCLES (required for emission shader fire)")

    # Cycles settings - GPU optimization
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 64  # Low for speed
    scene.cycles.use_denoising = True

    # CRITICAL: Set viewport shading to RENDERED to see fire
    # This is important for user to see fire in viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'

    print("  ✓ Viewport shading set to RENDERED (fire will be visible)")

    # Enable GPU
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'CUDA'
    prefs.get_devices()

    for device in prefs.devices:
        if device.type in {'CUDA', 'OPTIX'}:
            device.use = True
            print(f"  ✓ Enabled GPU: {device.name}")

    # CPU threads
    try:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        scene.render.threads_mode = 'FIXED'
        scene.render.threads = cpu_count
        print(f"  ✓ Using {cpu_count} CPU threads")
    except:
        scene.render.threads_mode = 'AUTO'

    print("✓ Scene setup complete")


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("ALTER LOGO - SEQUENTIAL ANIMATION")
    print("FLUID FIRE SIMULATION - Like ALTER_LOGO_COMPLETE")
    print("Preserves exact SVG positions")
    print("="*60 + "\n")

    # Find SVG
    svg_path = os.path.join(os.path.dirname(__file__), "alter.svg")
    if not os.path.exists(svg_path):
        print(f"✗ alter.svg not found at: {svg_path}")
        return

    print(f"✓ Found SVG: {svg_path}\n")

    # Clean scene
    clean_scene()

    # Import SVG as unified logo (like ALTER_LOGO_COMPLETE)
    print("Step 1: Importing and unifying SVG...")
    logo = import_svg_as_one_logo(svg_path)

    if not logo:
        print("✗ Failed to import logo")
        return

    # Separate into individual elements
    print("Step 2: Separating into elements...")
    elements = separate_logo_into_elements(logo)

    if not elements:
        print("✗ Failed to separate elements")
        return

    # Add materials to elements
    logo_mat = create_logo_material()
    for elem in elements:
        if len(elem.data.materials):
            elem.data.materials[0] = logo_mat
        else:
            elem.data.materials.append(logo_mat)

    # Add BANJA LUKA text
    print("\nStep 3: Creating BANJA LUKA text...")
    banja_luka = create_banja_luka_text()
    elements.append(banja_luka)

    if len(banja_luka.data.materials):
        banja_luka.data.materials[0] = logo_mat
    else:
        banja_luka.data.materials.append(logo_mat)

    # Animate elements
    print("\nStep 4: Setting up sequential animation...")
    total_frames, element_timings = animate_sequential(elements)

    # Create FLUID fire domain (ONE for all elements)
    print("\nStep 5: Creating FLUID fire domain...")
    domain = create_fire_domain(total_frames)

    # Add FLUID fire emitter for each element
    print("\nStep 6: Adding FLUID fire emitters for each element...")
    for i, elem in enumerate(elements):
        start_frame, end_frame = element_timings[i]
        emitter = create_fire_emitter_for_element(elem, i, start_frame, end_frame)

    # Setup scene
    print("\nStep 7: Setting up camera, lights, render...")
    setup_scene(total_frames)

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "alter_logo_sequential.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)

    print("\n" + "="*60)
    print("✨ SUCCESS - SEQUENTIAL ANIMATION READY!")
    print("="*60)
    print(f"\n📁 Saved: {output_path}")
    print(f"🎬 Total frames: {total_frames}")
    print(f"⏱️  Duration: ~{total_frames/30:.1f} seconds at 30fps")
    print(f"🔥 Elements with FLUID fire: {len(elements)}")
    print("\n🔥 FIRE: FLUID simulation (Mantaflow)")
    print("   Fire type: FIRE flow on wireframe emitters")
    print("   Domain resolution: 128 (optimized for speed)")
    print("   Noise: Disabled (faster baking)")
    print("   Material: Principled Volume with flame attributes")
    print("   Emitters: Hidden (domain visible)")
    print()
    print("⚠️  IMPORTANT - BAKING REQUIRED:")
    print("   1. Open the .blend file")
    print("   2. Go to frame 1")
    print("   3. Press SPACEBAR to play animation")
    print("   4. Blender will BAKE the fluid simulation automatically")
    print("   5. Wait for baking to complete (progress shown in timeline)")
    print("   6. Fire will appear after baking completes")
    print()
    print("   To see fire during baking:")
    print("   • Press 'Z' key and select 'Rendered' mode")
    print("   • Fire will become visible as frames are baked")
    print()
    print("\n✨ Features:")
    print("   • Elements preserve EXACT SVG positions")
    print("   • Only Y axis (depth) animates")
    print("   • X and Z stay at original positions")
    print("   • FLUID fire simulation (like ALTER_LOGO_COMPLETE)")
    print("   • Fire timed to each element's animation")
    print("   • Fire fades 30 frames after element arrives")
    print()
    print("💡 After baking completes:")
    print("   • Press SPACEBAR to preview animation")
    print("   • Press F12 to render (fire will be visible!)")
    print()


if __name__ == "__main__":
    main()
