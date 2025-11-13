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


def create_fast_fire_material():
    """
    Create fire material using EMISSION shader with noise
    NO FLUID SIMULATION - instant, no baking needed
    """
    mat = bpy.data.materials.new(name="FastFire")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Mix shader for transparency
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (600, 0)
    links.new(mix.outputs[0], output.inputs[0])

    # Transparent for areas without fire
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (400, -100)
    links.new(transparent.outputs[0], mix.inputs[1])

    # Emission for fire glow (BRIGHT so it's visible!)
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (400, 100)
    emission.inputs['Strength'].default_value = 20.0  # Increased from 5.0 to 20.0 for visibility
    links.new(emission.outputs[0], mix.inputs[2])

    # ColorRamp for fire colors (black to red to orange to yellow)
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (200, 100)
    links.new(colorramp.outputs[0], emission.inputs['Color'])
    links.new(colorramp.outputs[1], mix.inputs[0])  # Alpha for transparency

    # Set fire color gradient
    colorramp.color_ramp.elements[0].position = 0.0
    colorramp.color_ramp.elements[0].color = (0, 0, 0, 1)  # Black
    colorramp.color_ramp.elements.new(0.3)
    colorramp.color_ramp.elements[1].color = (0.8, 0.1, 0.0, 1)  # Red
    colorramp.color_ramp.elements.new(0.6)
    colorramp.color_ramp.elements[2].color = (1.0, 0.4, 0.0, 1)  # Orange
    colorramp.color_ramp.elements.new(0.9)
    colorramp.color_ramp.elements[3].color = (1.0, 0.9, 0.3, 1)  # Yellow

    # Noise texture for fire animation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (0, 100)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.6
    links.new(noise.outputs['Fac'], colorramp.inputs[0])

    # Texture coordinate for noise
    texcoord = nodes.new('ShaderNodeTexCoord')
    texcoord.location = (-400, 100)

    # Mapping for animation
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-200, 100)
    links.new(texcoord.outputs['Object'], mapping.inputs[0])
    links.new(mapping.outputs[0], noise.inputs['Vector'])

    # Add driver for animation - move noise up over time
    driver = mapping.inputs['Location'].driver_add('default_value', 2)  # Z axis
    driver.driver.expression = "frame * 0.1"

    print("✓ Fast fire material created (NO baking needed)")

    return mat


def create_fire_for_element(element, index):
    """
    Create fast fire effect using wireframe + emission shader
    NO FLUID - instant setup, no baking
    """
    # Duplicate element for fire emitter
    bpy.ops.object.select_all(action='DESELECT')
    element.select_set(True)
    bpy.context.view_layer.objects.active = element
    bpy.ops.object.duplicate()

    emitter = bpy.context.active_object
    emitter.name = f"FireEmitter_{index}"

    # Wireframe modifier - fire along edges
    wireframe = emitter.modifiers.new(name="Wireframe", type='WIREFRAME')
    wireframe.thickness = 0.15
    wireframe.use_replace = True
    wireframe.use_boundary = True

    # Apply wireframe modifier so emission shader works on the geometry
    bpy.ops.object.select_all(action='DESELECT')
    emitter.select_set(True)
    bpy.context.view_layer.objects.active = emitter
    bpy.ops.object.modifier_apply(modifier="Wireframe")

    # Parent to element
    emitter.parent = element
    emitter.matrix_parent_inverse = element.matrix_world.inverted()

    # Apply fast fire material
    fire_mat = bpy.data.materials.get("FastFire")
    if not fire_mat:
        fire_mat = create_fast_fire_material()

    if len(emitter.data.materials):
        emitter.data.materials[0] = fire_mat
    else:
        emitter.data.materials.append(fire_mat)

    # DON'T hide emitter - we want to see the fire!
    # The emission shader creates the glow effect
    emitter.hide_render = False  # VISIBLE in render
    emitter.hide_viewport = False  # VISIBLE in viewport

    print(f"    ✓ Fire emitter created (visible, wireframe applied)")

    return emitter


def animate_sequential(elements):
    """
    Animate elements arriving one by one
    Elements start FAR on Y axis, arrive at current position
    Only Y axis moves - X and Z stay as imported from SVG
    """
    start_y_offset = -50.0  # How far to push elements back
    duration = 40  # Frames for each element to arrive
    gap = 25  # Gap between element starts

    print("\n✓ Animating elements sequentially:")

    for i, element in enumerate(elements):
        # Get current position (where SVG import placed it)
        current_x = element.location.x
        current_y = element.location.y
        current_z = element.location.z

        # Frame timing
        start_frame = 1 + (i * gap)
        end_frame = start_frame + duration

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

    return total_frames


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
    print("NO FLUID BAKING - Fast emission shader fire")
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
    total_frames = animate_sequential(elements)

    # Add fast fire to each element
    print("\nStep 5: Adding FAST fire effects (no baking)...")
    fire_mat = create_fast_fire_material()

    for i, elem in enumerate(elements):
        emitter = create_fire_for_element(elem, i)
        print(f"  ✓ Fire emitter {i} created (instant, no baking)")

    # Setup scene
    print("\nStep 6: Setting up camera, lights, render...")
    setup_scene(total_frames)

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "alter_logo_sequential_FAST.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)

    print("\n" + "="*60)
    print("✨ SUCCESS - SEQUENTIAL ANIMATION READY!")
    print("="*60)
    print(f"\n📁 Saved: {output_path}")
    print(f"🎬 Total frames: {total_frames}")
    print(f"⏱️  Duration: ~{total_frames/30:.1f} seconds at 30fps")
    print("\n🔥 FIRE: Emission shader - NO BAKING NEEDED!")
    print("   Emission strength: 20.0 (VERY visible)")
    print("   Material: FastFire (applied to all emitters)")
    print("   Wireframe: Applied (fire along element edges)")
    print()
    print("⚠️  IMPORTANT - TO SEE FIRE IN BLENDER:")
    print("   1. Open the .blend file")
    print("   2. Press 'Z' key in viewport")
    print("   3. Select 'Rendered' mode")
    print("   4. Fire should be visible immediately!")
    print()
    print("   OR just render with F12 - fire will be in render!")
    print()
    print("\n✨ Features:")
    print("   • Elements preserve EXACT SVG positions")
    print("   • Only Y axis (depth) animates")
    print("   • X and Z stay at original positions")
    print("   • Fast fire with animated noise texture")
    print("   • Fire emitters are VISIBLE (not hidden)")
    print("   • Emission strength: 20.0 for high visibility")
    print()
    print("💡 Press SPACEBAR to preview animation")
    print("   Press F12 to render (fire will be visible!)")
    print()


if __name__ == "__main__":
    main()
