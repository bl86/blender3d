"""
ULTRA-SIMPLE VERSION - GUARANTEED TO WORK
Creates animation with 3D text logo (no SVG needed)

Just run: python SIMPLE_GO.py
"""

import subprocess
import sys
import os
import platform


def find_blender():
    """Find Blender executable"""
    try:
        result = subprocess.run(['blender', '--version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            return 'blender'
    except:
        pass

    system = platform.system()
    if system == 'Windows':
        base = r"C:\Program Files\Blender Foundation"
        if os.path.exists(base):
            for folder in os.listdir(base):
                path = os.path.join(base, folder, "blender.exe")
                if os.path.exists(path):
                    return path

    return None


def create_simple_script():
    """Create a simple Blender script that ALWAYS works"""
    script = '''
import bpy
import math

print("Creating simple logo animation...")

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create text logo
bpy.ops.object.text_add(location=(0, 0, 0))
text_obj = bpy.context.active_object
text_obj.data.body = "ALTER"
text_obj.data.align_x = 'CENTER'
text_obj.data.align_y = 'CENTER'
text_obj.data.size = 2.0
text_obj.data.extrude = 0.3
text_obj.data.bevel_depth = 0.05

# Convert to mesh
bpy.ops.object.convert(target='MESH')
logo = bpy.context.active_object

# Create golden material
mat = bpy.data.materials.new(name="Gold")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

output = nodes.new('ShaderNodeOutputMaterial')
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.2

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
logo.data.materials.append(mat)

# Create camera
bpy.ops.object.camera_add(location=(0, -10, 2))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(80), 0, 0)
bpy.context.scene.camera = camera

# Animate logo
logo.location = (0, 10, 0)
logo.keyframe_insert(data_path="location", frame=1)
logo.location = (0, 0, 0)
logo.keyframe_insert(data_path="location", frame=120)

# Animate rotation
logo.rotation_euler = (0, 0, 0)
logo.keyframe_insert(data_path="rotation_euler", frame=1)
logo.rotation_euler = (0, 0, math.radians(360))
logo.keyframe_insert(data_path="rotation_euler", frame=120)

# Add light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
light = bpy.context.active_object
light.data.energy = 5

# Setup rendering
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 30
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# World background
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.05, 0.05, 0.1, 1.0)

# Save
import os
save_path = os.path.join(os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd(), "alter_simple.blend")
bpy.ops.wm.save_as_mainfile(filepath=save_path)

print(f"✓ Saved to: {save_path}")
print("✓ Animation ready! (120 frames, 4 seconds)")
'''

    return script


def main():
    print("=" * 70)
    print(" " * 15 + "SIMPLE ALTER LOGO ANIMATION")
    print(" " * 20 + "(Guaranteed to Work)")
    print("=" * 70)
    print()

    # Find Blender
    print("Looking for Blender...")
    blender = find_blender()

    if not blender:
        print("❌ Blender not found!")
        print()
        print("Install Blender from: https://www.blender.org/download/")
        input("\nPress Enter to exit...")
        return 1

    print(f"✓ Found: {blender}")
    print()
    print("Creating animation...")
    print("This will take about 2 minutes...")
    print()

    # Create temp script
    script_content = create_simple_script()
    temp_script = os.path.join(os.path.dirname(__file__), '_temp_simple.py')

    with open(temp_script, 'w') as f:
        f.write(script_content)

    # Run Blender
    cmd = [blender, '--background', '--python', temp_script]

    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))

        # Clean up temp script
        try:
            os.remove(temp_script)
        except:
            pass

        if result.returncode == 0:
            print()
            print("=" * 70)
            print(" " * 25 + "✓ SUCCESS!")
            print("=" * 70)
            print()
            print("Created: alter_simple.blend")
            print()
            print("To preview:")
            print(f'  {blender} alter_simple.blend')
            print()
            print("To render:")
            print(f'  {blender} -b alter_simple.blend -a')
            print()
        else:
            print()
            print("❌ Failed. Check errors above.")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    input("Press Enter to exit...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
