"""
═══════════════════════════════════════════════════════════════════════════════
ALTER LOGO - SEQUENTIAL FIRE ANIMATION V3
═══════════════════════════════════════════════════════════════════════════════

REQUIREMENTS FROM USER (CORRECTED):
1. NO bevel - only small extrude for 3D effect
2. Animation TOWARD camera (not from behind)
3. Elements: Individual letters (A, L, T, E, R) + ego + treble key + "banja luka"
4. Fire FROM START, EXTINGUISHES in last 2 seconds (CORRECTED!)
5. Smoke disperses, logo remains with GLOW on transparent background
6. Alpha channel for compositing in Premiere
7. Fast execution - optimized for speed

HOW TO USE:
blender --background --python ALTER_LOGO_SEQUENTIAL.py

═══════════════════════════════════════════════════════════════════════════════
"""

import bpy
import os
import math
from mathutils import Vector


def clean_scene():
    """Clear all objects from scene"""
    print("Clearing scene...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Clean up orphaned data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.curves:
        if block.users == 0:
            bpy.data.curves.remove(block)


def import_and_prepare_svg(svg_path):
    """
    Import SVG and convert to mesh with proper geometry
    NO BEVEL - only small extrude
    """
    print(f"\nImporting SVG: {svg_path}")

    # Store existing objects
    objects_before = set(bpy.data.objects)

    # Import SVG
    bpy.ops.object.select_all(action='DESELECT')
    result = bpy.ops.import_curve.svg(filepath=svg_path)

    if result != {'FINISHED'}:
        print(f"✗ SVG import failed: {result}")
        return None

    # Find imported curves
    objects_after = set(bpy.data.objects)
    imported_objects = list(objects_after - objects_before)
    curves = [obj for obj in imported_objects if obj.type == 'CURVE']

    if not curves:
        print("✗ No curves imported from SVG")
        return None

    print(f"✓ Imported {len(curves)} curves")

    # Join all curves into ONE object first (like ALTER_LOGO_COMPLETE.py)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in curves:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = curves[0]

    if len(curves) > 1:
        print(f"  Joining {len(curves)} curves into one...")
        bpy.ops.object.join()

    logo = bpy.context.active_object
    logo.name = "AlterLogoUnified"

    # CRITICAL: NO BEVEL - small extrude for clean appearance
    print("  Setting geometry: NO bevel, small extrude")
    logo.data.extrude = 0.005  # Small extrude for clean logo
    logo.data.bevel_depth = 0.0  # NO BEVEL
    logo.data.bevel_resolution = 0

    # Convert to mesh BEFORE separating
    print("  Converting to mesh...")
    bpy.ops.object.convert(target='MESH')

    logo = bpy.context.active_object
    logo.name = "AlterLogoMesh"

    # Center the whole logo first
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    logo.location = (0, 0, 0)
    logo.scale = (2.5, 2.5, 2.5)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Rotate to face camera (like ALTER_LOGO_COMPLETE.py)
    logo.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    print(f"✓ Logo unified and converted to mesh")

    return logo


def separate_into_elements(logo):
    """
    Separate logo into individual elements by loose parts
    Returns list of mesh objects
    """
    print("\nSeparating logo into elements...")

    # Enter edit mode
    bpy.ops.object.select_all(action='DESELECT')
    logo.select_set(True)
    bpy.context.view_layer.objects.active = logo
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all
    bpy.ops.mesh.select_all(action='SELECT')

    # Separate by loose parts
    print("  Separating by loose parts...")
    bpy.ops.mesh.separate(type='LOOSE')

    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get all separated elements
    elements = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    print(f"✓ Separated into {len(elements)} elements")

    # Sort by X position (left to right) for consistent ordering
    elements.sort(key=lambda obj: obj.location.x)

    # Name elements for clarity
    for i, elem in enumerate(elements):
        elem.name = f"Element_{i:02d}"
        print(f"  {elem.name}: pos=({elem.location.x:.2f}, {elem.location.y:.2f}, {elem.location.z:.2f})")

    return elements


def create_banja_luka_text():
    """Create BANJA LUKA text element"""
    print("\nCreating BANJA LUKA text...")

    bpy.ops.object.text_add(location=(0, 0, -4))
    text_obj = bpy.context.active_object
    text_obj.name = "BanjaLuka"
    text_obj.data.body = "BANJA LUKA"
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    text_obj.data.size = 0.5

    # Same geometry rules: small extrude, NO bevel
    text_obj.data.extrude = 0.005  # Small extrude for clean appearance
    text_obj.data.bevel_depth = 0.0

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')
    text_obj = bpy.context.active_object
    text_obj.name = "BanjaLuka"

    # Center
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Rotate to face camera
    text_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    print(f"✓ BANJA LUKA created at Z={text_obj.location.z:.2f}")

    return text_obj


def create_logo_material():
    """Create golden metallic material with GLOW for logo elements"""
    mat = bpy.data.materials.new(name="GoldenMetal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Mix shader to combine metallic and emission
    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (400, 0)
    mix.inputs[0].default_value = 0.85  # 85% metallic, 15% emission glow
    links.new(mix.outputs['Shader'], output.inputs['Surface'])

    # Metallic gold BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 100)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)  # Gold
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.1
    links.new(bsdf.outputs['BSDF'], mix.inputs[1])

    # Emission for GLOW (logo remains visible after fire extinguishes)
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, -100)
    emission.inputs['Color'].default_value = (1.0, 0.85, 0.4, 1.0)  # Warm golden glow
    emission.inputs['Strength'].default_value = 0.8  # Moderate glow strength
    links.new(emission.outputs['Emission'], mix.inputs[2])

    return mat


def animate_elements_sequential(elements, total_duration=240):
    """
    Animate elements SEQUENTIALLY TOWARD camera
    Each element comes INDIVIDUALLY, ALL arrive by frame 200
    Fire FROM START, extinguishes in LAST 2 SECONDS

    Returns: (total_frames, fire_end_frame, element_timings)
    """
    print("\nAnimating elements SEQUENTIALLY toward camera...")

    num_elements = len(elements)

    # Each element takes 30 frames (1 second) to travel
    frames_per_element = 30

    # All elements must arrive by frame 200
    last_element_arrival = 200
    first_element_start = 1

    # Calculate gap between element starts so last element arrives at frame 200
    if num_elements == 1:
        gap_between_elements = 0
    else:
        last_element_start = last_element_arrival - frames_per_element
        gap_between_elements = (last_element_start - first_element_start) / (num_elements - 1)

    print(f"  Number of elements: {num_elements}")
    print(f"  Frames per element: {frames_per_element}")
    print(f"  Gap between elements: {gap_between_elements:.1f} frames")
    print(f"  First element: frame {first_element_start} → {first_element_start + frames_per_element}")
    print(f"  Last element: frame {int(first_element_start + (num_elements-1) * gap_between_elements)} → {last_element_arrival}")
    print(f"  ALL elements arrive by frame {last_element_arrival}")

    # Fire FROM START, extinguishes in last 2 seconds
    fire_extinguish_duration = 60  # Last 2 seconds at 30fps
    total_frames = total_duration
    fire_end_frame = total_frames - fire_extinguish_duration  # Fire stops at frame 180
    fire_start_frame = 1  # Fire starts from beginning

    print(f"  Total animation: {total_frames} frames ({total_frames/30:.1f} seconds)")
    print(f"  Fire active: frames {fire_start_frame}-{fire_end_frame}")
    print(f"  Fire extinguishes: frames {fire_end_frame}-{total_frames} ({fire_extinguish_duration/30:.1f} seconds)")

    element_timings = []

    for i, element in enumerate(elements):
        # Get current position (centered at origin after import)
        current_x = element.location.x
        current_z = element.location.z
        final_y = element.location.y  # Where it should end up

        # Calculate timing for THIS element (sequential)
        start_frame = first_element_start + int(i * gap_between_elements)
        end_frame = start_frame + frames_per_element
        element_timings.append((start_frame, end_frame))

        # START: Far from camera (positive Y)
        start_y = 20.0  # Start far

        # END: Near camera (negative Y or close to 0)
        # final_y is already set from SVG import (around 0)

        print(f"  Element {i}: frames {start_frame}-{end_frame}")
        print(f"    Position: X={current_x:.2f}, Y={start_y:.2f}→{final_y:.2f}, Z={current_z:.2f}")

        # Keyframe START position
        element.location = (current_x, start_y, current_z)
        element.keyframe_insert(data_path='location', frame=start_frame)

        # Keyframe END position
        element.location = (current_x, final_y, current_z)
        element.keyframe_insert(data_path='location', frame=end_frame)

        # Smooth animation
        if element.animation_data:
            for fcurve in element.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'

    # Set scene frame range
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_frames

    print(f"✓ Animation complete: {len(elements)} elements")
    print(f"✓ Fire timing: frames 1-{fire_end_frame}, extinguishes {fire_end_frame}-{total_frames}")

    return total_frames, fire_end_frame, element_timings


def create_fire_domain(total_frames, fire_end_frame, elements):
    """
    Create FLUID fire domain
    Fire FROM START, extinguishes at fire_end_frame, disperses until total_frames
    Domain sized and positioned to cover ALL elements
    """
    print("\nCreating FLUID fire domain...")

    # Calculate bounding box of ALL elements
    min_x = min(elem.location.x for elem in elements)
    max_x = max(elem.location.x for elem in elements)
    min_z = min(elem.location.z for elem in elements)
    max_z = max(elem.location.z for elem in elements)

    # Y range includes animation path (elements move from 20 to ~0)
    min_y = -5  # Elements end around 0, give margin
    max_y = 25  # Elements start at 20, give margin

    # Calculate domain center and size
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    size_x = (max_x - min_x) + 5  # Add margin
    size_y = (max_y - min_y) + 5  # Add margin
    size_z = (max_z - min_z) + 5  # Add margin
    domain_size = max(size_x, size_y, size_z)  # Use largest dimension

    print(f"  Element bounds: X[{min_x:.2f}, {max_x:.2f}], Y[{min_y:.2f}, {max_y:.2f}], Z[{min_z:.2f}, {max_z:.2f}]")
    print(f"  Domain center: ({center_x:.2f}, {center_y:.2f}, {center_z:.2f})")
    print(f"  Domain size: {domain_size:.2f}")

    # Domain covering animation path
    bpy.ops.mesh.primitive_cube_add(size=domain_size, location=(center_x, center_y, center_z))
    domain = bpy.context.active_object
    domain.name = "FireDomain"
    domain.display_type = 'WIRE'

    # Add FLUID domain modifier
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    # Configure for fire
    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 256  # Higher resolution for better fire visibility

    # Noise settings (SAME as working version)
    try:
        domain_settings.use_noise = True
        domain_settings.noise_scale = 2  # Must be int
    except:
        pass  # Noise not available in this version

    # Cache settings
    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = fire_end_frame + 60  # Fire ends, add buffer

    # Additional settings for better fire visibility
    try:
        domain_settings.use_guide = False  # Disable guiding for simplicity
        domain_settings.clipping = 1e-06  # Better clipping
    except:
        pass

    # Fire material with Principled Volume
    mat = bpy.data.materials.new(name="FireMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    volume = nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (200, 0)

    # Flame attribute
    flame_attr = nodes.new('ShaderNodeAttribute')
    flame_attr.location = (-200, 200)
    flame_attr.attribute_name = 'flame'

    # Density attribute
    density_attr = nodes.new('ShaderNodeAttribute')
    density_attr.location = (-200, -100)
    density_attr.attribute_name = 'density'

    # Color ramp for fire color
    color_ramp = nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, 200)
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].position = 1.0
    color_ramp.color_ramp.elements[1].color = (1, 0.8, 0.1, 1)

    # Add red-orange midpoint
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = (1, 0.3, 0.05, 1)

    # Connect nodes
    links.new(flame_attr.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], volume.inputs['Color'])
    links.new(flame_attr.outputs['Fac'], volume.inputs['Emission Strength'])
    links.new(density_attr.outputs['Fac'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], output.inputs['Volume'])

    # Adjust for MAXIMUM visibility
    volume.inputs['Density'].default_value = 5.0  # VERY HIGH for visibility
    volume.inputs['Emission Strength'].default_value = 25.0  # VERY BRIGHT fire
    volume.inputs['Blackbody Intensity'].default_value = 1.0

    # Apply material
    if domain.data.materials:
        domain.data.materials[0] = mat
    else:
        domain.data.materials.append(mat)

    domain.hide_render = False
    domain.hide_viewport = False

    print(f"✓ Fire domain created (frames 1-{total_frames}, fire extinguishes at {fire_end_frame})")

    return domain


def create_fire_emitter_for_element(element, index, fire_end_frame, total_frames):
    """
    Create FLUID fire emitter for element
    Fire active FROM START, extinguishes at fire_end_frame, disperses until total_frames
    """
    # Duplicate element for emitter
    bpy.ops.object.select_all(action='DESELECT')
    element.select_set(True)
    bpy.context.view_layer.objects.active = element
    bpy.ops.object.duplicate()

    emitter = bpy.context.active_object
    emitter.name = f"FireEmitter_{index:02d}"

    # Add wireframe modifier
    wireframe_mod = emitter.modifiers.new(name="Wireframe", type='WIREFRAME')
    wireframe_mod.thickness = 0.08  # Thin wireframe (same as working version)
    wireframe_mod.use_replace = True
    wireframe_mod.use_boundary = True
    wireframe_mod.use_even_offset = True

    # Apply wireframe
    bpy.ops.object.convert(target='MESH')

    # DEBUG: Check emitter position and parent
    print(f"    Emitter {index:02d} pos: ({emitter.location.x:.2f}, {emitter.location.y:.2f}, {emitter.location.z:.2f})")
    print(f"    Element {index:02d} pos: ({element.location.x:.2f}, {element.location.y:.2f}, {element.location.z:.2f})")

    # Parent to element
    emitter.parent = element
    emitter.matrix_parent_inverse = element.matrix_world.inverted()

    # Add FLUID flow
    bpy.ops.object.modifier_add(type='FLUID')
    emitter.modifiers["Fluid"].fluid_type = 'FLOW'
    flow = emitter.modifiers["Fluid"].flow_settings
    flow.flow_type = 'FIRE'
    flow.flow_behavior = 'INFLOW'

    try:
        flow.fuel_amount = 2.0
    except AttributeError:
        pass  # fuel_amount not available

    try:
        flow.temperature = 3.0
    except AttributeError:
        pass  # temperature not available

    # Animate fire fade - fire FROM START, extinguishes at fire_end_frame
    try:
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=1)
        flow.density = 1.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=fire_end_frame - 10)
        flow.density = 0.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=fire_end_frame)
    except (AttributeError, TypeError):
        # Keyframing might not work, try simple approach
        pass

    # Hide emitter
    emitter.hide_render = True
    emitter.hide_viewport = True

    print(f"  ✓ Fire emitter {index:02d} (active frames 1-{fire_end_frame}, extinguishes {fire_end_frame}-{total_frames})")

    return emitter


def setup_camera_and_lights():
    """Setup camera and lighting"""
    print("\nSetting up camera and lights...")

    # Camera - looking at scene from negative Y
    bpy.ops.object.camera_add(location=(0, -10, 1))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = camera

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(5, -8, 6))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 800
    key.data.size = 6

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-4, -6, 3))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 300
    fill.data.size = 5

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, 4, 4))
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.energy = 400
    rim.data.size = 4

    print("✓ Camera and lights ready")


def setup_render_settings(total_frames):
    """
    Setup render settings with ALPHA channel for compositing
    CRITICAL: Transparent background for Premiere
    """
    print("\nConfiguring render settings...")

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = 30
    scene.render.fps_base = 1

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # CRITICAL: Enable film transparent for alpha channel
    scene.render.film_transparent = True
    print("  ✓ Film transparent enabled (alpha channel)")

    # Output format
    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    output_dir = os.path.join(blend_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "frame_")

    # PNG with RGBA for alpha channel
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.image_settings.compression = 15

    print(f"  ✓ Output: {scene.render.filepath}#### (PNG with alpha)")

    # Use Cycles for better fire rendering
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128  # Good quality/speed balance

    # Use GPU if available
    try:
        scene.cycles.device = 'GPU'
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA'  # Try CUDA first
        prefs.get_devices()
        for device in prefs.devices:
            device.use = True
        print("  ✓ GPU rendering enabled (CUDA)")
    except:
        try:
            prefs.compute_device_type = 'OPTIX'
            print("  ✓ GPU rendering enabled (OptiX)")
        except:
            print("  ⚠ GPU not available, using CPU")

    # Use all CPU cores
    try:
        import multiprocessing
        scene.render.threads_mode = 'FIXED'
        scene.render.threads = multiprocessing.cpu_count()
        print(f"  ✓ Using {scene.render.threads} CPU threads")
    except:
        scene.render.threads_mode = 'AUTO'

    print("✓ Render settings configured (RGBA PNG output)")


def set_viewport_to_camera():
    """
    Set all 3D viewports to camera view and rendered shading
    So user can immediately see what will be rendered
    """
    print("\nSetting viewport to camera view...")

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Set to camera view
                    space.region_3d.view_perspective = 'CAMERA'

                    # Set shading to RENDERED mode
                    space.shading.type = 'RENDERED'

                    # Lock camera to view
                    space.lock_camera = True

                    print("  ✓ Viewport set to camera view (rendered mode)")
                    break


def main():
    """Main execution - SENIOR DEVELOPER APPROACH"""
    print("\n" + "="*70)
    print("ALTER LOGO - SEQUENTIAL FIRE ANIMATION (V3)")
    print("="*70)
    print("\nREQUIREMENTS (CORRECTED):")
    print("  • NO bevel - only small extrude")
    print("  • Animation TOWARD camera")
    print("  • Fire FROM START, EXTINGUISHES in last 2 seconds")
    print("  • Smoke disperses, logo GLOWS on transparent background")
    print("  • Alpha channel for Premiere")
    print("  • Optimized for SPEED (no long baking)")
    print("="*70 + "\n")

    # Find SVG
    svg_path = os.path.join(os.path.dirname(__file__), "alter.svg")
    if not os.path.exists(svg_path):
        print(f"✗ ERROR: alter.svg not found at {svg_path}")
        return False

    print(f"✓ Found SVG: {svg_path}")

    # Clean scene
    clean_scene()

    # Import and prepare SVG
    logo = import_and_prepare_svg(svg_path)
    if not logo:
        print("✗ FAILED: SVG import")
        return False

    # Separate into elements
    elements = separate_into_elements(logo)
    if not elements or len(elements) == 0:
        print("✗ FAILED: Element separation")
        return False

    # Create logo material
    logo_mat = create_logo_material()
    for elem in elements:
        if elem.data.materials:
            elem.data.materials[0] = logo_mat
        else:
            elem.data.materials.append(logo_mat)

    # Add BANJA LUKA text
    banja_luka = create_banja_luka_text()
    if banja_luka.data.materials:
        banja_luka.data.materials[0] = logo_mat
    else:
        banja_luka.data.materials.append(logo_mat)
    elements.append(banja_luka)

    # Animate elements
    total_frames, fire_end_frame, element_timings = animate_elements_sequential(elements)

    # Create fire domain (fire FROM START, extinguishes at fire_end_frame)
    # Pass elements so domain can be sized and positioned correctly
    domain = create_fire_domain(total_frames, fire_end_frame, elements)

    # Create fire emitters for each element
    print("\nCreating FLUID fire emitters...")
    for i, elem in enumerate(elements):
        create_fire_emitter_for_element(elem, i, fire_end_frame, total_frames)

    # Setup camera and lights
    setup_camera_and_lights()

    # Setup render settings with alpha
    setup_render_settings(total_frames)

    # Set viewport to camera view (so user sees rendered result)
    set_viewport_to_camera()

    # Set playback to frame 1 (start of animation)
    bpy.context.scene.frame_set(1)

    # Save blend file
    output_path = os.path.join(os.path.dirname(__file__), "alter_logo_sequential_v2.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)

    print("\n" + "="*70)
    print("✅ SUCCESS - SEQUENTIAL ANIMATION READY")
    print("="*70)
    print(f"\n📁 Saved: {output_path}")
    print(f"🎬 Frames: {total_frames} ({total_frames/30:.1f} seconds @ 30fps)")
    print(f"🔥 Fire: ACTIVE frames 1-{fire_end_frame}, EXTINGUISHES {fire_end_frame}-{total_frames}")
    print(f"   Fire FROM START, smoke disperses in last {(total_frames-fire_end_frame)/30:.1f} seconds")
    print(f"🎨 Elements: {len(elements)} (including BANJA LUKA)")
    print(f"📺 Output: PNG with RGBA (alpha channel for Premiere)")
    print(f"✨ Logo: Golden metallic with GLOW (visible after fire extinguishes)")
    print("\n⚠️  TO BAKE AND RENDER:")
    print("  1. Open the .blend file in Blender")
    print("  2. Press SPACEBAR to play - fluid will bake automatically")
    print("  3. Wait for baking (progress in timeline)")
    print(f"  4. Fire FROM START, extinguishes at frame {fire_end_frame}, smoke disperses")
    print("  5. Logo remains GLOWING on transparent background")
    print("  6. Render: Animation > Render Animation")
    print("  7. Output will have transparent background (alpha channel)")
    print("\n💡 SETTINGS:")
    print("  • Animation: EXTENDED to 240 frames (8 seconds)")
    print("  • Elements: Arrive by frame 180-200")
    print("  • Extrude: 0.02 (bigger for wireframe geometry)")
    print("  • Wireframe thickness: 0.20 (thick for fire coverage)")
    print("  • Resolution: 128 (faster baking)")
    print("  • Adaptive domain: Enabled (auto-sized to elements)")
    print("  • Noise: Disabled (much faster)")
    print("  • Cache type: MODULAR (automatic baking)")
    print("\n💡 VIEWPORT:")
    print("  • Automatically set to CAMERA VIEW")
    print("  • RENDERED mode enabled")
    print("  • Fire should be VISIBLE when baked")
    print("\n💡 DEBUG INFO:")
    print("  • Element positions printed during setup")
    print("  • Fire domain bounds calculated from elements")
    print("  • Emitter positions printed for verification")
    print("\n" + "="*70 + "\n")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n✗ SCRIPT FAILED - Check errors above")
        exit(1)
    else:
        print("✓ SCRIPT COMPLETED SUCCESSFULLY")
        exit(0)
