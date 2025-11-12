"""
ALTER Logo Sequential Animation - Each element comes separately with fire
Treble key, then each letter (A-L-T-E-R), then "BANJA LUKA" text
"""

import bpy
import math
import os
import sys


def find_svg_file():
    """Find alter.svg in various locations"""
    search_paths = []

    # Blend file directory
    if bpy.data.filepath:
        blend_dir = os.path.dirname(bpy.data.filepath)
        search_paths.append(os.path.join(blend_dir, "alter.svg"))

    # Script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    search_paths.append(os.path.join(script_dir, "alter.svg"))

    # Current working directory
    search_paths.append(os.path.join(os.getcwd(), "alter.svg"))

    # Parent directory
    parent_dir = os.path.dirname(script_dir)
    search_paths.append(os.path.join(parent_dir, "alter.svg"))

    for path in search_paths:
        if os.path.exists(path):
            return path

    return None


def clear_scene():
    """Clear default scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear materials
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)


def import_and_separate_logo(svg_path):
    """Import SVG and keep original layout - preserve X,Z positions"""
    print("  Importing logo with original layout...")

    # Get existing objects before import
    existing_objects = set(bpy.context.scene.objects)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Import SVG
    bpy.ops.import_curve.svg(filepath=svg_path)

    # Get newly imported objects
    new_objects = set(bpy.context.scene.objects) - existing_objects
    imported_curves = [obj for obj in new_objects if obj.type == 'CURVE']

    if not imported_curves:
        raise Exception("No curves imported from SVG")

    print(f"  Found {len(imported_curves)} curve objects")

    # Process each curve - PRESERVE original X,Z positions!
    elements = []

    for i, curve_obj in enumerate(imported_curves):
        # Store original location BEFORE any operations
        original_loc = curve_obj.location.copy()

        # Select only this curve
        bpy.ops.object.select_all(action='DESELECT')
        curve_obj.select_set(True)
        bpy.context.view_layer.objects.active = curve_obj

        # Add minimal depth
        curve_obj.data.extrude = 0.005
        curve_obj.data.bevel_depth = 0.0

        # Convert to mesh
        bpy.ops.object.convert(target='MESH')

        mesh_obj = bpy.context.active_object
        mesh_obj.name = f"LogoElement_{i}"

        # Set origin to geometry BUT keep world location
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        # CRITICAL: Restore original X and Z, only reset Y to 0
        mesh_obj.location.x = original_loc.x
        mesh_obj.location.z = original_loc.z
        mesh_obj.location.y = 0  # Start at Y=0, will animate along Y axis

        # Rotate to face camera
        mesh_obj.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True)

        elements.append(mesh_obj)
        print(f"    Element {i}: X={mesh_obj.location.x:.2f}, Z={mesh_obj.location.z:.2f}")

    print(f"  ✓ Created {len(elements)} elements preserving layout")
    return elements


def create_banja_luka_text():
    """Create BANJA LUKA text positioned below logo"""
    print("  Creating BANJA LUKA text...")

    bpy.ops.object.text_add(location=(0, 0, -4))  # Below logo
    text_obj = bpy.context.active_object
    text_obj.name = "BanjaLukaText"

    # Set text
    text_obj.data.body = "BANJA LUKA"
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'

    # Font size - smaller than main logo
    text_obj.data.size = 1.0
    text_obj.data.extrude = 0.005

    # Convert to mesh
    bpy.ops.object.convert(target='MESH')
    text_obj = bpy.context.active_object

    # Set origin but keep location
    original_loc = text_obj.location.copy()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    text_obj.location = original_loc

    # Orient to camera
    text_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    print("  ✓ BANJA LUKA text created")
    return text_obj


def create_golden_material(obj, name="GoldenMetal"):
    """Create reflective golden material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.08
    bsdf.inputs['Specular IOR Level'].default_value = 1.0

    try:
        bsdf.inputs['Anisotropic'].default_value = 0.3
    except:
        pass

    emission = nodes.new('ShaderNodeEmission')
    emission.location = (200, -200)
    emission.inputs['Color'].default_value = (1.0, 0.85, 0.4, 1.0)
    emission.inputs['Strength'].default_value = 0.3

    mix = nodes.new('ShaderNodeMixShader')
    mix.location = (600, 0)
    mix.inputs[0].default_value = 0.95

    links.new(bsdf.outputs['BSDF'], mix.inputs[1])
    links.new(emission.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def animate_element_sequence(elements, banja_luka):
    """Animate elements - ONLY Y axis, preserve X,Z layout"""
    print("  Setting up sequential animation (preserving layout)...")

    frame_offset = 30  # Frames between each element
    start_y = 20  # Start position (far)
    end_y = -2   # End position (close to camera)
    hold_frames = 60  # How long each element holds at end

    current_frame = 1

    # Animate each element - ONLY Y AXIS!
    for i, element in enumerate(elements):
        element_start = current_frame
        element_arrive = element_start + 40  # 40 frames to arrive

        # Store original X,Z - CRITICAL!
        original_x = element.location.x
        original_z = element.location.z

        # Start far - ONLY change Y
        element.location.y = start_y
        element.keyframe_insert(data_path='location', index=1, frame=element_start)  # Y only

        # Arrive close - ONLY change Y
        element.location.y = end_y
        element.keyframe_insert(data_path='location', index=1, frame=element_arrive)  # Y only

        # Hold position
        element.keyframe_insert(data_path='location', index=1, frame=element_arrive + hold_frames)  # Y only

        # Ensure X,Z never change - keyframe them at start
        element.location.x = original_x
        element.location.z = original_z
        element.keyframe_insert(data_path='location', index=0, frame=element_start)  # X
        element.keyframe_insert(data_path='location', index=2, frame=element_start)  # Z
        element.keyframe_insert(data_path='location', index=0, frame=element_arrive + hold_frames)  # X
        element.keyframe_insert(data_path='location', index=2, frame=element_arrive + hold_frames)  # Z

        # Smooth interpolation
        if element.animation_data:
            for fcurve in element.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO_CLAMPED'
                    kf.handle_right_type = 'AUTO_CLAMPED'

        current_frame += frame_offset
        print(f"    Element {i}: X={original_x:.2f}, Z={original_z:.2f}, Y: {start_y}→{end_y}")

    # Animate BANJA LUKA after all logo elements
    bl_start = current_frame
    bl_arrive = bl_start + 40

    bl_x = banja_luka.location.x
    bl_z = banja_luka.location.z

    banja_luka.location.y = start_y
    banja_luka.keyframe_insert(data_path='location', index=1, frame=bl_start)

    banja_luka.location.y = end_y
    banja_luka.keyframe_insert(data_path='location', index=1, frame=bl_arrive)

    # Lock X,Z
    banja_luka.keyframe_insert(data_path='location', index=0, frame=bl_start)
    banja_luka.keyframe_insert(data_path='location', index=2, frame=bl_start)
    banja_luka.keyframe_insert(data_path='location', index=0, frame=bl_arrive)
    banja_luka.keyframe_insert(data_path='location', index=2, frame=bl_arrive)

    if banja_luka.animation_data:
        for fcurve in banja_luka.animation_data.action.fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'BEZIER'
                kf.handle_left_type = 'AUTO_CLAMPED'
                kf.handle_right_type = 'AUTO_CLAMPED'

    total_frames = bl_arrive + hold_frames
    print(f"  ✓ Total animation: {total_frames} frames")
    print(f"  ✓ All elements keep original X,Z positions!")

    return total_frames


def create_fire_for_element(element, index):
    """Create fire simulation for one element"""
    # Duplicate element for fire emitter
    bpy.ops.object.select_all(action='DESELECT')
    element.select_set(True)
    bpy.context.view_layer.objects.active = element
    bpy.ops.object.duplicate()

    emitter = bpy.context.active_object
    emitter.name = f"FireEmitter_{index}"

    # Wireframe for contour fire
    wireframe_mod = emitter.modifiers.new(name="Wireframe", type='WIREFRAME')
    wireframe_mod.thickness = 0.08
    wireframe_mod.use_replace = True
    wireframe_mod.use_boundary = True

    bpy.ops.object.convert(target='MESH')

    # Parent to element
    emitter.parent = element
    emitter.matrix_parent_inverse = element.matrix_world.inverted()

    # Hide emitter
    emitter.hide_render = True
    emitter.hide_viewport = True

    # Add fluid flow
    bpy.ops.object.modifier_add(type='FLUID')
    emitter.modifiers["Fluid"].fluid_type = 'FLOW'
    flow = emitter.modifiers["Fluid"].flow_settings
    flow.flow_type = 'FIRE'
    flow.flow_behavior = 'INFLOW'

    try:
        flow.fuel_amount = 2.0
        flow.temperature = 3.0
    except:
        pass

    # Animate fire to appear/fade with element timing
    # Fire active when element is moving, fades when it stops
    try:
        flow.density = 0.0
        emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=1)

        # Get element animation timing from its keyframes
        if element.animation_data and element.animation_data.action:
            keyframes = []
            for fcurve in element.animation_data.action.fcurves:
                if 'location' in fcurve.data_path:
                    for kf in fcurve.keyframe_points:
                        keyframes.append(int(kf.co[0]))

            if keyframes:
                keyframes = sorted(set(keyframes))
                start_frame = keyframes[0]
                end_frame = keyframes[-1] if len(keyframes) > 1 else start_frame + 40

                # Fire starts slightly before element
                flow.density = 1.0
                emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=max(1, start_frame - 5))

                # Fire fades as element arrives
                flow.density = 0.0
                emitter.modifiers["Fluid"].flow_settings.keyframe_insert(data_path="density", frame=end_frame + 10)
    except:
        pass

    return emitter


def create_shared_fire_domain(total_frames):
    """Create one large fire domain for all elements - OPTIMIZED for speed"""
    print("  Creating shared fire domain (optimized for fast baking)...")

    bpy.ops.mesh.primitive_cube_add(size=25, location=(0, 10, 0))
    domain = bpy.context.active_object
    domain.name = "FireDomain"
    domain.display_type = 'WIRE'

    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain_settings = domain.modifiers["Fluid"].domain_settings

    domain_settings.domain_type = 'GAS'
    domain_settings.resolution_max = 128  # Reduced for MUCH faster baking (was 200)

    # Noise - disable for faster baking
    try:
        domain_settings.use_noise = False  # Disabled = faster baking
    except:
        pass

    try:
        domain_settings.use_fire = True
    except:
        pass

    # Cache type - modular for speed
    try:
        domain_settings.cache_type = 'MODULAR'  # Faster than ALL
        domain_settings.cache_data_format = 'OPENVDB'  # Compressed
    except:
        pass

    domain_settings.cache_frame_start = 1
    domain_settings.cache_frame_end = total_frames

    # Time settings for faster simulation
    try:
        domain_settings.time_scale = 1.5  # Faster simulation time
        domain_settings.cfl_condition = 4.0  # Higher = fewer steps = faster
    except:
        pass

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
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].position = 1.0
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

    if domain.data.materials:
        domain.data.materials[0] = mat
    else:
        domain.data.materials.append(mat)

    domain.hide_render = False

    print("  ✓ Fire domain created")
    return domain


def setup_camera():
    """Setup camera to frame sequential animation"""
    print("  Setting up camera...")

    bpy.ops.object.camera_add(location=(0, -10, 1))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    camera.data.lens = 50
    camera.data.dof.use_dof = False  # Disable DOF to keep everything sharp

    bpy.context.scene.camera = camera

    # Point at center area
    camera.rotation_euler = (math.radians(90), 0, 0)

    # Align viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.region_3d.view_perspective = 'CAMERA'
                    break

    bpy.context.scene.frame_set(1)

    print("  ✓ Camera configured")
    return camera


def setup_lighting():
    """Setup lighting with reflective ground"""
    print("  Setting up lights...")

    # Ground plane
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 10, -3))
    ground = bpy.context.active_object
    ground.name = "GroundPlane"

    ground_mat = bpy.data.materials.new(name="GroundMaterial")
    ground_mat.use_nodes = True
    ground_nodes = ground_mat.node_tree.nodes
    ground_links = ground_mat.node_tree.links
    ground_nodes.clear()

    ground_output = ground_nodes.new('ShaderNodeOutputMaterial')
    ground_bsdf = ground_nodes.new('ShaderNodeBsdfPrincipled')
    ground_bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.03, 1.0)
    ground_bsdf.inputs['Metallic'].default_value = 1.0
    ground_bsdf.inputs['Roughness'].default_value = 0.05
    ground_links.new(ground_bsdf.outputs['BSDF'], ground_output.inputs['Surface'])

    if ground.data.materials:
        ground.data.materials[0] = ground_mat
    else:
        ground.data.materials.append(ground_mat)

    # Lights
    bpy.ops.object.light_add(type='AREA', location=(5, 5, 8))
    key = bpy.context.active_object
    key.data.energy = 1500
    key.data.size = 5

    bpy.ops.object.light_add(type='AREA', location=(-5, 5, 4))
    fill = bpy.context.active_object
    fill.data.energy = 600
    fill.data.size = 4

    bpy.ops.object.light_add(type='AREA', location=(0, 0, 10))
    top = bpy.context.active_object
    top.data.energy = 800
    top.data.size = 6

    # Sky environment
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True

    world_nodes = world.node_tree.nodes
    world_links = world.node_tree.links
    for node in world_nodes:
        if node.type != 'OUTPUT_WORLD':
            world_nodes.remove(node)

    output = None
    for node in world_nodes:
        if node.type == 'OUTPUT_WORLD':
            output = node
            break

    sky = world_nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'NISHITA'
    sky.sun_elevation = math.radians(45)

    bg = world_nodes.new('ShaderNodeBackground')
    bg.inputs['Strength'].default_value = 1.5

    mix_rgb = world_nodes.new('ShaderNodeMixRGB')
    mix_rgb.blend_type = 'MULTIPLY'
    mix_rgb.inputs[0].default_value = 0.3
    mix_rgb.inputs[2].default_value = (0.05, 0.05, 0.08, 1.0)

    world_links.new(sky.outputs['Color'], mix_rgb.inputs[1])
    world_links.new(mix_rgb.outputs[0], bg.inputs['Color'])
    world_links.new(bg.outputs[0], output.inputs[0])

    print("  ✓ Lighting complete")


def configure_render(total_frames):
    """Configure render settings with full system resource utilization"""
    print("  Configuring render with maximum performance...")

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.fps = 30

    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.cycles.preview_samples = 64
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    scene.cycles.device = 'GPU'

    # CPU thread settings - USE ALL CORES for baking and rendering
    try:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        scene.render.threads_mode = 'FIXED'
        scene.render.threads = cpu_count  # Use all CPU threads
        print(f"  ✓ Using {cpu_count} CPU threads for baking/rendering")
    except:
        scene.render.threads_mode = 'AUTO'
        print("  ✓ Using AUTO thread mode")

    # Enable GPU - OptiX/CUDA for RTX 3090
    try:
        prefs = bpy.context.preferences
        cycles_prefs = prefs.addons['cycles'].preferences
        available_types = cycles_prefs.get_device_types(bpy.context)

        if 'OPTIX' in [t[0] for t in available_types]:
            cycles_prefs.compute_device_type = 'OPTIX'
            print("  ✓ Using OptiX (optimal for RTX 3090)")
        elif 'CUDA' in [t[0] for t in available_types]:
            cycles_prefs.compute_device_type = 'CUDA'
            print("  ✓ Using CUDA")

        cycles_prefs.get_devices()
        enabled_gpus = []
        for device in cycles_prefs.devices:
            if device.type in {'CUDA', 'OPTIX'}:
                device.use = True
                enabled_gpus.append(device.name)

        if enabled_gpus:
            print(f"  ✓ Enabled GPU(s): {', '.join(enabled_gpus)}")
    except:
        pass

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'

    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'High Contrast'

    # PNG sequence with transparency
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '16'
    scene.render.film_transparent = True

    output_dir = os.path.join(bpy.path.abspath("//"), "output_sequential")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "seq_####")

    # Volume settings
    scene.cycles.volume_bounces = 2
    scene.cycles.volume_preview_step_rate = 1
    scene.cycles.volume_step_rate = 0.5
    scene.cycles.volume_max_steps = 2048

    print("  ✓ Render configured")


def bake_fire():
    """Bake fire simulation with progress info"""
    print("  Baking fire simulation...")
    print("  ⚠️  This will take 1-3 minutes with optimizations")
    print("  💡 Resolution: 128 (optimized for speed)")
    print("  💡 Noise: DISABLED for faster baking")
    print("  💡 Cache: MODULAR + OpenVDB compression")
    print("  💡 Using ALL CPU cores")
    print()

    try:
        domain = None
        for obj in bpy.context.scene.objects:
            if obj.name == "FireDomain":
                domain = obj
                break

        if not domain:
            print("  ⚠️  No fire domain found, skipping bake")
            return

        bpy.ops.object.select_all(action='DESELECT')
        domain.select_set(True)
        bpy.context.view_layer.objects.active = domain

        # Get frame range
        domain_settings = domain.modifiers["Fluid"].domain_settings
        frame_count = domain_settings.cache_frame_end - domain_settings.cache_frame_start + 1
        print(f"  🔥 Baking {frame_count} frames...")
        print(f"  ⏱️  Estimated: ~{frame_count * 0.5:.0f}-{frame_count * 1.5:.0f} seconds")
        print()

        bpy.ops.fluid.bake_all()

        print()
        print("  ✓ Fire baked successfully!")
        print("  ✓ All CPU threads were utilized during baking")
    except Exception as e:
        print(f"  ⚠️  Baking failed: {e}")
        print("  💡 You can bake manually in Blender: Physics Properties → Fluid → Bake All")


def main():
    """Main setup function"""
    print("\n" + "=" * 75)
    print(" " * 15 + "ALTER LOGO SEQUENTIAL ANIMATION")
    print("=" * 75)
    print()

    # Find SVG
    print("[Step 1] Finding alter.svg...")
    svg_path = find_svg_file()

    if not svg_path:
        print("\n❌ ERROR: alter.svg not found!")
        return False

    print(f"  ✓ Found: {svg_path}")

    try:
        # Clear scene
        print("\n[Step 2] Clearing scene...")
        clear_scene()

        # Import and separate
        print("\n[Step 3] Importing logo elements...")
        elements = import_and_separate_logo(svg_path)

        # Create BANJA LUKA
        print("\n[Step 4] Creating BANJA LUKA text...")
        banja_luka = create_banja_luka_text()

        # Materials
        print("\n[Step 5] Applying golden materials...")
        for i, elem in enumerate(elements):
            create_golden_material(elem, f"Gold_{i}")
        create_golden_material(banja_luka, "Gold_BL")

        # Animation
        print("\n[Step 6] Setting up sequential animation...")
        total_frames = animate_element_sequence(elements, banja_luka)

        # Camera
        print("\n[Step 7] Setting up camera...")
        setup_camera()

        # Fire for each element
        print("\n[Step 8] Creating fire for each element...")
        for i, elem in enumerate(elements):
            create_fire_for_element(elem, i)
        create_fire_for_element(banja_luka, len(elements))

        # Fire domain
        print("\n[Step 9] Creating shared fire domain...")
        create_shared_fire_domain(total_frames)

        # Lighting
        print("\n[Step 10] Setting up lighting...")
        setup_lighting()

        # Render
        print("\n[Step 11] Configuring render...")
        configure_render(total_frames)

        # Bake
        print("\n[Step 12] Baking fire...")
        bake_fire()

        # Save
        print("\n[Step 13] Saving file...")
        save_dir = os.path.dirname(svg_path)
        save_path = os.path.join(save_dir, "alter_logo_sequential.blend")
        bpy.ops.wm.save_as_mainfile(filepath=save_path)

        print("\n" + "=" * 75)
        print(" " * 25 + "✅ SUCCESS!")
        print("=" * 75)
        print(f"\n📁 Saved: {save_path}")
        print(f"🎬 Animation: {total_frames} frames (sequential)")
        print(f"🔥 Fire: Each element has its own fire trail")
        print(f"📐 Resolution: 1920x1080 @ 100% (PNG)")
        print()
        print("✨ Animation sequence:")
        print("   • Each logo element comes separately with fire")
        print("   • Elements hold position as next one arrives")
        print("   • BANJA LUKA comes last")
        print("   • Fire follows each element's contours")
        print()
        print("🎥 To render:")
        print("   • Ctrl+F12 - Renders to output_sequential/seq_####.png")
        print("   • Transparent background enabled")
        print()
        print("💡 TIP: Compare with alter_logo_fire_animation.blend")
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
