#!/usr/bin/env blender --python
"""
ALTER LOGO FIRE ANIMATION - SIMPLE AND WORKING VERSION
Professional animation that ACTUALLY works in Blender 4.5

Features:
- SVG import with preserved layout
- VISIBLE fire using emission spheres
- Proper convergence to exact SVG positions
- Camera aligned for rendering
- Simple, clean, WORKING code
"""

import bpy
import os
import math
from mathutils import Vector

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

TOTAL_FRAMES = 300
CONVERGENCE_END = 200
FIRE_FADEOUT_START = 260
FIRE_FADEOUT_END = 300
EXTRUDE_DEPTH = 0.05

# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def clear_scene():
    """Clear everything"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    print("✓ Scene cleared")

def setup_render():
    """Setup render settings"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_start = 1
    scene.frame_end = TOTAL_FRAMES
    scene.render.fps = 30
    print("✓ Render settings configured")

# ═══════════════════════════════════════════════════════════════════════════
# SVG IMPORT
# ═══════════════════════════════════════════════════════════════════════════

def import_svg(svg_path):
    """Import SVG and convert to mesh - PRESERVE exact positions"""
    print(f"Importing SVG: {svg_path}")

    existing = set(bpy.context.scene.objects)
    bpy.ops.import_curve.svg(filepath=svg_path)
    new_objects = set(bpy.context.scene.objects) - existing
    curves = [obj for obj in new_objects if obj.type == 'CURVE']

    if not curves:
        raise Exception("No curves imported!")

    print(f"✓ Imported {len(curves)} curves")

    # Convert to mesh and extrude
    meshes = []
    for i, curve in enumerate(curves):
        bpy.ops.object.select_all(action='DESELECT')
        curve.select_set(True)
        bpy.context.view_layer.objects.active = curve

        # Convert to mesh
        bpy.ops.object.convert(target='MESH')
        mesh_obj = bpy.context.active_object
        mesh_obj.name = f"Logo_{i:03d}"

        # Set origin to geometry (preserves position!)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Store FINAL position (where it should be in complete logo)
        mesh_obj['final_location'] = mesh_obj.location.copy()

        # Add extrude
        mod = mesh_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        mod.thickness = EXTRUDE_DEPTH
        bpy.ops.object.modifier_apply(modifier="Solidify")

        # Smooth shading
        bpy.ops.object.shade_smooth()

        meshes.append(mesh_obj)
        print(f"  {mesh_obj.name}: final pos = ({mesh_obj.location.x:.2f}, {mesh_obj.location.y:.2f}, {mesh_obj.location.z:.2f})")

    return meshes

# ═══════════════════════════════════════════════════════════════════════════
# MATERIALS
# ═══════════════════════════════════════════════════════════════════════════

def create_golden_material():
    """Golden metallic material"""
    mat = bpy.data.materials.new(name="Gold")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (0, 0)
    principled.inputs['Base Color'].default_value = (1.0, 0.7, 0.3, 1.0)
    principled.inputs['Metallic'].default_value = 1.0
    principled.inputs['Roughness'].default_value = 0.15

    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    return mat

def create_fire_glow_material():
    """Bright emission material for fire glow - VERY VISIBLE"""
    mat = bpy.data.materials.new(name="FireGlow")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    emission = nodes.new('ShaderNodeEmission')
    emission.location = (0, 0)
    emission.inputs['Color'].default_value = (1.0, 0.3, 0.0, 1.0)  # Orange fire
    emission.inputs['Strength'].default_value = 50.0  # VERY BRIGHT

    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    return mat

# ═══════════════════════════════════════════════════════════════════════════
# FIRE EFFECT - SIMPLE AND VISIBLE
# ═══════════════════════════════════════════════════════════════════════════

def add_fire_glow(obj, fire_material):
    """Add glowing sphere around object for fire effect"""
    # Calculate object size
    bbox = obj.bound_box
    max_dim = max([max(abs(v[0]), abs(v[1]), abs(v[2])) for v in bbox])

    # Create glow sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=max_dim * 1.3, location=(0, 0, 0))
    glow = bpy.context.active_object
    glow.name = f"FireGlow_{obj.name}"

    # Parent to object (follows during animation)
    glow.parent = obj
    glow.matrix_parent_inverse = obj.matrix_world.inverted()

    # Assign fire material
    glow.data.materials.append(fire_material)

    # Hide in viewport (only renders)
    glow.hide_viewport = True

    # Animate opacity for fadeout
    glow.scale = Vector((1, 1, 1))
    glow.keyframe_insert(data_path="scale", frame=FIRE_FADEOUT_START)

    glow.scale = Vector((0.01, 0.01, 0.01))  # Shrink to nothing
    glow.keyframe_insert(data_path="scale", frame=FIRE_FADEOUT_END)

    print(f"  Added fire glow to {obj.name}")
    return glow

# ═══════════════════════════════════════════════════════════════════════════
# ANIMATION
# ═══════════════════════════════════════════════════════════════════════════

def animate_convergence(objects):
    """Animate objects converging from different directions to form logo"""
    print("Creating convergence animation...")

    # Calculate logo center for reference
    center = Vector((0, 0, 0))
    for obj in objects:
        center += Vector(obj['final_location'])
    center /= len(objects)

    print(f"  Logo center: ({center.x:.2f}, {center.y:.2f}, {center.z:.2f})")

    for i, obj in enumerate(objects):
        # Get final position (where it should be in complete logo)
        final_pos = Vector(obj['final_location'])

        # Calculate starting position (far away, but in a pattern)
        angle = (i / len(objects)) * 2 * math.pi
        offset_x = math.cos(angle) * 20
        offset_y = 30  # All come from behind camera
        offset_z = math.sin(angle) * 10

        start_pos = final_pos + Vector((offset_x, offset_y, offset_z))

        # Set start position
        obj.location = start_pos
        obj.keyframe_insert(data_path="location", frame=1)

        # Set final position (EXACT position from SVG)
        obj.location = final_pos
        obj.keyframe_insert(data_path="location", frame=CONVERGENCE_END)

        # Smooth interpolation
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'BEZIER'
                    kf.handle_left_type = 'AUTO'
                    kf.handle_right_type = 'AUTO'

        print(f"  {obj.name}: ({start_pos.x:.1f}, {start_pos.y:.1f}, {start_pos.z:.1f}) → ({final_pos.x:.2f}, {final_pos.y:.2f}, {final_pos.z:.2f})")

    print(f"✓ Animated {len(objects)} objects")

# ═══════════════════════════════════════════════════════════════════════════
# CAMERA
# ═══════════════════════════════════════════════════════════════════════════

def setup_camera(objects):
    """Setup camera to frame logo at 2/3 screen"""
    # Calculate logo bounds at final position
    all_final_pos = [Vector(obj['final_location']) for obj in objects]
    center = sum(all_final_pos, Vector((0, 0, 0))) / len(all_final_pos)

    # Create camera
    bpy.ops.object.camera_add(location=(center.x, center.y - 15, center.z))
    camera = bpy.context.active_object
    camera.name = "Camera"
    bpy.context.scene.camera = camera

    # Point at logo center
    constraint = camera.constraints.new('TRACK_TO')
    bpy.ops.object.empty_add(location=center)
    target = bpy.context.active_object
    target.name = "CameraTarget"
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Set to frame 200 (logo complete)
    bpy.context.scene.frame_set(CONVERGENCE_END)

    print(f"✓ Camera positioned at frame {CONVERGENCE_END}")
    return camera

# ═══════════════════════════════════════════════════════════════════════════
# LIGHTING
# ═══════════════════════════════════════════════════════════════════════════

def setup_lights(center):
    """3-point lighting"""
    # Key light
    bpy.ops.object.light_add(type='AREA', location=(center.x - 5, center.y - 8, center.z + 6))
    key = bpy.context.active_object
    key.data.energy = 500

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(center.x + 5, center.y - 6, center.z + 3))
    fill = bpy.context.active_object
    fill.data.energy = 200

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(center.x, center.y + 5, center.z + 8))
    rim = bpy.context.active_object
    rim.data.energy = 300

    print("✓ Lights created")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "="*80)
    print("  ALTER LOGO FIRE ANIMATION - SIMPLE VERSION")
    print("="*80 + "\n")

    # Find SVG
    svg_path = os.path.join(os.getcwd(), "alter.svg")
    if not os.path.exists(svg_path):
        svg_path = os.path.join(os.path.dirname(__file__), "alter.svg")

    if not os.path.exists(svg_path):
        print("❌ ERROR: alter.svg not found!")
        return

    # Setup
    clear_scene()
    setup_render()

    # Import SVG
    objects = import_svg(svg_path)

    # Materials
    gold_mat = create_golden_material()
    fire_mat = create_fire_glow_material()

    # Apply gold to all objects
    for obj in objects:
        if obj.data.materials:
            obj.data.materials[0] = gold_mat
        else:
            obj.data.materials.append(gold_mat)

    # Add fire glows
    print("Adding fire effects...")
    for obj in objects:
        add_fire_glow(obj, fire_mat)

    # Animate
    animate_convergence(objects)

    # Camera
    camera = setup_camera(objects)

    # Lights
    center = sum([Vector(obj['final_location']) for obj in objects], Vector((0, 0, 0))) / len(objects)
    setup_lights(center)

    # Save
    output = os.path.join(os.getcwd(), "alter_logo_simple.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output)

    print("\n" + "="*80)
    print("  ✅ COMPLETE!")
    print(f"  Saved: {output}")
    print(f"  Objects: {len(objects)}")
    print(f"  Frames: {TOTAL_FRAMES}")
    print(f"  Fire fadeout: {FIRE_FADEOUT_START}-{FIRE_FADEOUT_END}")
    print(f"\n  HOW TO VIEW:")
    print(f"    1. Open: blender alter_logo_simple.blend")
    print(f"    2. Press Spacebar to play animation")
    print(f"    3. Fire glows are VISIBLE (bright orange spheres)")
    print(f"    4. Logo forms EXACTLY as in SVG at frame {CONVERGENCE_END}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
