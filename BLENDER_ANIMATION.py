"""
═══════════════════════════════════════════════════════════════════════════════
ALTER LOGO ANIMATION - COMPLETE SETUP SCRIPT
═══════════════════════════════════════════════════════════════════════════════

KAKO KORISTITI:

OPCIJA 1 - Iz Blendera (Najlakše):
1. Otvori Blender
2. Idi na Scripting tab (gore)
3. Open → Izaberi ovaj fajl
4. Klikni "Run Script" (ili pritisni Alt+P)
5. GOTOVO! Animacija je spremna

OPCIJA 2 - Iz komandne linije:
  blender --background --python BLENDER_ANIMATION.py

═══════════════════════════════════════════════════════════════════════════════
"""

import bpy
import math
import os


def clear_scene():
    """Obriši sve iz scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Obriši materijale, teksture
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)


def create_logo():
    """Kreiraj 3D text logo"""
    print("\n📝 Creating logo...")

    bpy.ops.object.text_add(location=(0, 0, 0))
    text_obj = bpy.context.active_object
    text_obj.name = "AlterLogo"

    # Podesi text
    text_obj.data.body = "ALTER"
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    text_obj.data.size = 2.5
    text_obj.data.extrude = 0.4
    text_obj.data.bevel_depth = 0.08
    text_obj.data.bevel_resolution = 4

    # Konvertuj u mesh
    bpy.ops.object.convert(target='MESH')
    logo = bpy.context.active_object

    # Centriraj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    logo.location = (0, 0, 0)

    print("  ✓ Logo created")
    return logo


def create_golden_material(logo):
    """Kreiraj zlatni materijal"""
    print("\n✨ Creating golden material...")

    mat = bpy.data.materials.new(name="GoldenMetal")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Očisti default nodes
    nodes.clear()

    # Output node
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)

    # Zlatna boja i postavke
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)  # Zlatna
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.15
    bsdf.inputs['Specular IOR Level'].default_value = 0.8

    # Poveži nodes
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Dodaj materijal na logo
    if logo.data.materials:
        logo.data.materials[0] = mat
    else:
        logo.data.materials.append(mat)

    print("  ✓ Material applied")


def create_camera(logo):
    """Kreiraj kameru"""
    print("\n📹 Creating camera...")

    bpy.ops.object.camera_add(location=(0, -12, 2.5))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    camera.data.lens = 50

    # Fokusiraj na logo
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = logo
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Postavi kao aktivnu kameru
    bpy.context.scene.camera = camera

    print("  ✓ Camera configured")
    return camera


def animate_logo(logo):
    """Animiraj logo"""
    print("\n🎬 Animating logo...")

    # Početna pozicija (daleko)
    logo.location = (0, 15, 0)
    logo.keyframe_insert(data_path="location", frame=1)

    # Krajnja pozicija (blizu)
    logo.location = (0, -2, 0)
    logo.keyframe_insert(data_path="location", frame=180)

    # Rotacija
    logo.rotation_euler = (0, 0, 0)
    logo.keyframe_insert(data_path="rotation_euler", frame=1)

    logo.rotation_euler = (0.1, 0, math.radians(360))
    logo.keyframe_insert(data_path="rotation_euler", frame=180)

    # Smooth interpolation
    for fcurve in logo.animation_data.action.fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'BEZIER'
            kf.handle_left_type = 'AUTO_CLAMPED'
            kf.handle_right_type = 'AUTO_CLAMPED'

    print("  ✓ Animation keyframes set")


def create_lighting():
    """Kreiraj osvetljenje"""
    print("\n💡 Creating lights...")

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(6, -8, 8))
    key = bpy.context.active_object
    key.data.energy = 600
    key.data.size = 5
    key.data.color = (1.0, 0.95, 0.9)

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, -6, 4))
    fill = bpy.context.active_object
    fill.data.energy = 250
    fill.data.size = 4
    fill.data.color = (0.9, 0.95, 1.0)

    # Rim light
    bpy.ops.object.light_add(type='SPOT', location=(0, 10, 5))
    rim = bpy.context.active_object
    rim.data.energy = 400
    rim.data.spot_size = math.radians(50)

    # Environment
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.05, 0.05, 0.08, 1.0)
        bg_node.inputs['Strength'].default_value = 0.3

    print("  ✓ Lighting setup complete")


def setup_render():
    """Podesi render postavke"""
    print("\n⚙️  Configuring render...")

    scene = bpy.context.scene

    # Frame range
    scene.frame_start = 1
    scene.frame_end = 180  # 6 sekundi na 30fps
    scene.render.fps = 30

    # Render engine
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128  # Srednji kvalitet
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'

    # GPU rendering
    scene.cycles.device = 'GPU'

    # Resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100

    # Color management
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'

    # Output
    scene.render.image_settings.file_format = 'PNG'

    # Output path
    blend_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    output_dir = os.path.join(blend_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    scene.render.filepath = os.path.join(output_dir, "frame_####")

    print("  ✓ Render settings configured")


def main():
    """Glavna funkcija - kreira kompletan setup"""
    print("\n" + "=" * 75)
    print(" " * 20 + "ALTER LOGO ANIMATION SETUP")
    print("=" * 75)

    try:
        # 1. Očisti scenu
        print("\n[1/6] Clearing scene...")
        clear_scene()
        print("  ✓ Scene cleared")

        # 2. Kreiraj logo
        print("\n[2/6] Creating logo...")
        logo = create_logo()

        # 3. Dodaj materijal
        print("\n[3/6] Applying material...")
        create_golden_material(logo)

        # 4. Podesi kameru
        print("\n[4/6] Setting up camera...")
        create_camera(logo)

        # 5. Animiraj
        print("\n[5/6] Creating animation...")
        animate_logo(logo)

        # 6. Dodaj svetla
        print("\n[6/6] Adding lights...")
        create_lighting()

        # 7. Podesi rendering
        setup_render()

        # Sačuvaj fajl
        print("\n💾 Saving file...")
        save_path = os.path.join(
            os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd(),
            "alter_animation.blend"
        )
        bpy.ops.wm.save_as_mainfile(filepath=save_path)

        print("\n" + "=" * 75)
        print(" " * 25 + "✅ SETUP COMPLETE!")
        print("=" * 75)
        print(f"\n📁 Saved to: {save_path}")
        print(f"🎬 Frames: 180 (6 seconds at 30fps)")
        print(f"📐 Resolution: 1920x1080")
        print(f"🎨 Render engine: Cycles (128 samples)")
        print()
        print("▶️  To preview:")
        print("   • Press SPACEBAR in viewport")
        print("   • Or open Timeline and play")
        print()
        print("🎥 To render:")
        print("   • Press F12 for single frame")
        print("   • Press Ctrl+F12 for full animation")
        print("   • Or use: Render → Render Animation")
        print()
        print("📂 Frames will be saved to: output/frame_####.png")
        print("=" * 75)

    except Exception as e:
        print("\n" + "=" * 75)
        print(" " * 30 + "❌ ERROR")
        print("=" * 75)
        print(f"\n{str(e)}")
        import traceback
        traceback.print_exc()
        raise


# ═══════════════════════════════════════════════════════════════════════════
# POKRENI ODMAH
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
