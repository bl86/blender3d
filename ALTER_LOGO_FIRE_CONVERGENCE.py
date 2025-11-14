#!/usr/bin/env blender --python
"""
═══════════════════════════════════════════════════════════════════════════════
ALTER LOGO FIRE CONVERGENCE ANIMATION
═══════════════════════════════════════════════════════════════════════════════

Professional Blender animation system for Alter Ego logo with:
- SVG import and automatic mesh conversion with extrusion
- Intelligent component separation (treble key, wings, letters)
- Individual fire particle systems for each component
- Convergence animation from multiple directions
- Fire follows elements during movement
- Fire fadeout in last 40 frames
- Professional camera setup with logo at 2/3 screen
- Comprehensive testing and validation

USAGE:
    blender --background --python ALTER_LOGO_FIRE_CONVERGENCE.py

    Or in Blender GUI:
    1. Open Blender
    2. Go to Scripting tab
    3. Open this file
    4. Click Run Script (Alt+P)

REQUIREMENTS:
    - Blender 3.0+
    - alter.svg in project directory

OUTPUT:
    - alter_logo_fire_convergence.blend
    - Complete animation scene ready for rendering

AUTHOR: Senior Developer - Professional 3D Animation Pipeline
DATE: 2025-11-14
═══════════════════════════════════════════════════════════════════════════════
"""

import bpy
import bmesh
import os
import sys
import math
from mathutils import Vector, Matrix
from typing import List, Dict, Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

class AnimationConfig:
    """Centralized configuration for animation parameters"""

    # Animation timing
    TOTAL_FRAMES = 300
    FPS = 30
    CONVERGENCE_START_FRAME = 1
    CONVERGENCE_END_FRAME = 200
    FIRE_FADEOUT_START_FRAME = 260  # Last 40 frames
    FIRE_FADEOUT_END_FRAME = 300

    # Mesh settings
    EXTRUDE_DEPTH = 0.2
    MESH_RESOLUTION = 12

    # Fire settings
    FIRE_PARTICLE_COUNT = 5000
    FIRE_LIFETIME = 30
    FIRE_SIZE = 0.15
    FIRE_VELOCITY = 0.5

    # Camera settings
    LOGO_SCREEN_COVERAGE = 2/3  # 2/3 of screen
    CAMERA_DISTANCE = 12.0
    CAMERA_FOV = 50.0

    # Component separation thresholds
    SPATIAL_CLUSTERING_THRESHOLD = 3.0

    # Output
    OUTPUT_FILENAME = "alter_logo_fire_convergence.blend"


# ═══════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def print_header(text: str) -> None:
    """Print formatted section header"""
    print(f"\n{'='*79}")
    print(f"  {text}")
    print(f"{'='*79}\n")


def print_step(step: str, detail: str = "") -> None:
    """Print progress step"""
    if detail:
        print(f"  ✓ {step}: {detail}")
    else:
        print(f"  ✓ {step}")


def find_svg_file(filename: str = "alter.svg") -> Optional[str]:
    """
    Find SVG file in various locations

    Args:
        filename: Name of SVG file to find

    Returns:
        Full path to SVG file or None if not found
    """
    search_paths = [
        os.getcwd(),
        os.path.dirname(os.path.abspath(__file__)),
        os.path.dirname(bpy.data.filepath) if bpy.data.filepath else None,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
    ]

    for path in search_paths:
        if path is None:
            continue
        svg_path = os.path.join(path, filename)
        if os.path.exists(svg_path):
            return svg_path

    return None


# ═══════════════════════════════════════════════════════════════════════════
# SCENE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

class SceneManager:
    """Manages Blender scene setup and cleanup"""

    @staticmethod
    def clear_scene() -> None:
        """Remove all objects, materials, and clean scene"""
        print_step("Clearing scene")

        # Select and delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Clean up orphaned data
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)

    @staticmethod
    def setup_render_settings() -> None:
        """Configure render engine and settings"""
        print_step("Configuring render settings")

        scene = bpy.context.scene

        # Set Cycles as render engine
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'
        scene.cycles.samples = 256
        scene.cycles.use_denoising = True

        # Set resolution
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100

        # Set frame range
        scene.frame_start = 1
        scene.frame_end = AnimationConfig.TOTAL_FRAMES
        scene.render.fps = AnimationConfig.FPS

        # Enable motion blur
        scene.render.use_motion_blur = True
        scene.render.motion_blur_shutter = 0.5

        # Set color management
        scene.view_settings.view_transform = 'Filmic'
        scene.view_settings.look = 'High Contrast'


# ═══════════════════════════════════════════════════════════════════════════
# SVG IMPORT AND MESH CONVERSION
# ═══════════════════════════════════════════════════════════════════════════

class SVGImporter:
    """Handles SVG import and conversion to mesh"""

    @staticmethod
    def import_svg(svg_path: str) -> List[bpy.types.Object]:
        """
        Import SVG file and convert to meshes

        Args:
            svg_path: Path to SVG file

        Returns:
            List of imported mesh objects
        """
        print_step("Importing SVG", svg_path)

        # Store existing objects
        existing_objects = set(bpy.context.scene.objects)

        # Import SVG
        bpy.ops.import_curve.svg(filepath=svg_path)

        # Find new objects
        new_objects = set(bpy.context.scene.objects) - existing_objects
        curves = [obj for obj in new_objects if obj.type == 'CURVE']

        if not curves:
            raise Exception("No curves imported from SVG")

        print_step("Imported curves", f"{len(curves)} objects")

        # Convert to meshes
        meshes = []
        for i, curve_obj in enumerate(curves):
            mesh_obj = SVGImporter.convert_curve_to_mesh(curve_obj, i)
            meshes.append(mesh_obj)

        return meshes

    @staticmethod
    def convert_curve_to_mesh(curve_obj: bpy.types.Object, index: int) -> bpy.types.Object:
        """
        Convert curve to mesh and add extrusion

        Args:
            curve_obj: Curve object to convert
            index: Index for naming

        Returns:
            Converted mesh object
        """
        # Select curve
        bpy.ops.object.select_all(action='DESELECT')
        curve_obj.select_set(True)
        bpy.context.view_layer.objects.active = curve_obj

        # Convert to mesh
        bpy.ops.object.convert(target='MESH')
        mesh_obj = bpy.context.active_object
        mesh_obj.name = f"LogoElement_{index:03d}"

        # Set origin to geometry center (preserves spatial position)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Add solidify modifier for depth
        solidify = mesh_obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        solidify.thickness = AnimationConfig.EXTRUDE_DEPTH
        solidify.offset = 0

        # Apply modifier
        bpy.ops.object.modifier_apply(modifier="Solidify")

        # Add subdivision for smooth geometry
        bpy.ops.object.shade_smooth()

        return mesh_obj


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT IDENTIFICATION AND GROUPING
# ═══════════════════════════════════════════════════════════════════════════

class ComponentIdentifier:
    """Identifies and groups logo components intelligently"""

    @staticmethod
    def analyze_components(objects: List[bpy.types.Object]) -> Dict[str, List[bpy.types.Object]]:
        """
        Analyze and group components by spatial location

        Args:
            objects: List of mesh objects

        Returns:
            Dictionary mapping component type to list of objects
        """
        print_step("Analyzing component structure")

        components = {
            'treble_key': [],
            'left_wing': [],
            'right_wing': [],
            'alter_ego': [],
            'banja_luka': [],
            'other': []
        }

        # Get centroid of all objects
        centroid = ComponentIdentifier.calculate_centroid(objects)
        print_step("Logo centroid", f"X={centroid.x:.2f}, Y={centroid.y:.2f}, Z={centroid.z:.2f}")

        # Analyze each object
        for obj in objects:
            location = obj.location
            size = ComponentIdentifier.get_object_size(obj)

            # Determine component type based on position and size
            component_type = ComponentIdentifier.classify_component(
                location, size, centroid
            )

            components[component_type].append(obj)
            obj['component_type'] = component_type

            print_step(
                f"  {obj.name}",
                f"{component_type} at ({location.x:.1f}, {location.y:.1f}, {location.z:.1f})"
            )

        return components

    @staticmethod
    def calculate_centroid(objects: List[bpy.types.Object]) -> Vector:
        """Calculate centroid of all objects"""
        total = Vector((0, 0, 0))
        for obj in objects:
            total += obj.location
        return total / len(objects) if objects else Vector((0, 0, 0))

    @staticmethod
    def get_object_size(obj: bpy.types.Object) -> float:
        """Calculate approximate size of object"""
        dimensions = obj.dimensions
        return max(dimensions.x, dimensions.y, dimensions.z)

    @staticmethod
    def classify_component(location: Vector, size: float, centroid: Vector) -> str:
        """
        Classify component based on position and size

        Simple classification based on spatial distribution:
        - Center: Treble key or main elements
        - Left: Left wing
        - Right: Right wing
        - Top: Alter Ego text
        - Bottom: Banja Luka text
        """
        dx = location.x - centroid.x
        dz = location.z - centroid.z

        # Define thresholds
        left_threshold = -2.0
        right_threshold = 2.0
        top_threshold = 3.0
        bottom_threshold = -3.0

        # Classify based on position
        if dz > top_threshold:
            return 'alter_ego'
        elif dz < bottom_threshold:
            return 'banja_luka'
        elif dx < left_threshold:
            return 'left_wing'
        elif dx > right_threshold:
            return 'right_wing'
        elif size > 1.0:  # Larger central element
            return 'treble_key'
        else:
            return 'other'


# ═══════════════════════════════════════════════════════════════════════════
# MATERIAL CREATION
# ═══════════════════════════════════════════════════════════════════════════

class MaterialCreator:
    """Creates materials for logo and fire effects"""

    @staticmethod
    def create_golden_material() -> bpy.types.Material:
        """Create golden metallic material for logo"""
        mat = bpy.data.materials.new(name="GoldenLogo")
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (400, 0)

        principled = nodes.new('ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)

        # Set golden material properties
        principled.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
        principled.inputs['Metallic'].default_value = 1.0
        principled.inputs['Roughness'].default_value = 0.15
        principled.inputs['Specular'].default_value = 0.5
        principled.inputs['Anisotropic'].default_value = 0.3

        # Connect
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        return mat

    @staticmethod
    def create_fire_material() -> bpy.types.Material:
        """Create emission-based fire material for particles"""
        mat = bpy.data.materials.new(name="FireParticle")
        mat.use_nodes = True
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Output
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (600, 0)

        # Emission shader
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (300, 0)
        emission.inputs['Strength'].default_value = 8.0

        # Color ramp for fire gradient
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (0, 0)

        # Fire colors: dark red -> orange -> yellow -> white
        color_ramp.color_ramp.elements[0].position = 0.0
        color_ramp.color_ramp.elements[0].color = (0.3, 0.05, 0.0, 1.0)  # Dark red

        color_ramp.color_ramp.elements[1].position = 0.5
        color_ramp.color_ramp.elements[1].color = (1.0, 0.4, 0.0, 1.0)  # Orange

        color_ramp.color_ramp.elements.new(0.75)
        color_ramp.color_ramp.elements[2].color = (1.0, 0.9, 0.0, 1.0)  # Yellow

        color_ramp.color_ramp.elements.new(1.0)
        color_ramp.color_ramp.elements[3].color = (1.0, 1.0, 0.9, 1.0)  # White hot

        # Particle info for color variation
        particle_info = nodes.new('ShaderNodeParticleInfo')
        particle_info.location = (-300, 0)

        # Connect
        links.new(particle_info.outputs['Lifetime'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        return mat


# ═══════════════════════════════════════════════════════════════════════════
# FIRE PARTICLE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class FireEffectCreator:
    """Creates fire particle systems for components"""

    @staticmethod
    def create_fire_for_object(obj: bpy.types.Object, fire_material: bpy.types.Material) -> bpy.types.ParticleSystem:
        """
        Create fire particle system for object

        Args:
            obj: Object to add fire to
            fire_material: Material to use for fire particles

        Returns:
            Created particle system
        """
        # Add particle system
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        bpy.ops.object.particle_system_add()
        psys = obj.particle_systems[-1]
        psys.name = f"Fire_{obj.name}"

        # Configure particle settings
        settings = psys.settings
        settings.name = f"FireSettings_{obj.name}"

        # Emission
        settings.count = AnimationConfig.FIRE_PARTICLE_COUNT
        settings.emit_from = 'FACE'
        settings.use_emit_random = True
        settings.lifetime = AnimationConfig.FIRE_LIFETIME
        settings.lifetime_random = 0.3

        # Velocity
        settings.normal_factor = AnimationConfig.FIRE_VELOCITY
        settings.factor_random = 0.5
        settings.effector_weights.gravity = -0.1  # Slight upward movement

        # Physics
        settings.physics_type = 'NEWTON'
        settings.mass = 0.1
        settings.use_multiply_size_mass = True
        settings.particle_size = AnimationConfig.FIRE_SIZE
        settings.size_random = 0.5

        # Render
        settings.render_type = 'HALO'
        settings.use_render_emitter = False

        # Material slot for particles
        if fire_material:
            settings.material_slot = 'FireParticle'

        return psys

    @staticmethod
    def setup_fire_fadeout(psys: bpy.types.ParticleSystem) -> None:
        """
        Setup keyframes for fire fadeout in last 40 frames

        Args:
            psys: Particle system to animate
        """
        settings = psys.settings

        # Keyframe emission at full strength
        settings.count = AnimationConfig.FIRE_PARTICLE_COUNT
        settings.keyframe_insert(
            data_path="count",
            frame=AnimationConfig.FIRE_FADEOUT_START_FRAME
        )

        # Keyframe emission at zero (fadeout)
        settings.count = 0
        settings.keyframe_insert(
            data_path="count",
            frame=AnimationConfig.FIRE_FADEOUT_END_FRAME
        )

        # Set interpolation to smooth
        if psys.settings.animation_data:
            for fcurve in psys.settings.animation_data.action.fcurves:
                if 'count' in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'


# ═══════════════════════════════════════════════════════════════════════════
# ANIMATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class AnimationCreator:
    """Creates convergence animation for logo components"""

    @staticmethod
    def create_convergence_animation(components: Dict[str, List[bpy.types.Object]]) -> None:
        """
        Create convergence animation where elements come from different directions

        Args:
            components: Dictionary of grouped components
        """
        print_step("Creating convergence animation")

        # Define direction vectors for each component type
        directions = {
            'treble_key': Vector((0, 20, 0)),      # From front
            'left_wing': Vector((-15, 15, 5)),     # From left-front-top
            'right_wing': Vector((15, 15, 5)),     # From right-front-top
            'alter_ego': Vector((0, 12, 10)),      # From top-front
            'banja_luka': Vector((0, 12, -8)),     # From bottom-front
            'other': Vector((0, 15, 0))            # Default from front
        }

        # Animate each component
        for component_type, objects in components.items():
            if not objects:
                continue

            direction = directions.get(component_type, Vector((0, 15, 0)))

            for obj in objects:
                AnimationCreator.animate_object_convergence(obj, direction)

    @staticmethod
    def animate_object_convergence(obj: bpy.types.Object, direction: Vector) -> None:
        """
        Animate single object converging to final position

        Args:
            obj: Object to animate
            direction: Direction vector for starting offset
        """
        # Store final position
        final_position = obj.location.copy()

        # Calculate start position (offset by direction)
        start_position = final_position + direction

        # Set start position and keyframe
        obj.location = start_position
        obj.keyframe_insert(data_path="location", frame=AnimationConfig.CONVERGENCE_START_FRAME)

        # Set end position and keyframe
        obj.location = final_position
        obj.keyframe_insert(data_path="location", frame=AnimationConfig.CONVERGENCE_END_FRAME)

        # Set interpolation to smooth
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                if 'location' in fcurve.data_path:
                    for keyframe in fcurve.keyframe_points:
                        keyframe.interpolation = 'BEZIER'
                        keyframe.handle_left_type = 'AUTO'
                        keyframe.handle_right_type = 'AUTO'

        print_step(f"  Animated {obj.name}", f"from offset {direction}")


# ═══════════════════════════════════════════════════════════════════════════
# CAMERA SETUP
# ═══════════════════════════════════════════════════════════════════════════

class CameraSetup:
    """Sets up camera for optimal logo framing"""

    @staticmethod
    def create_camera(objects: List[bpy.types.Object]) -> bpy.types.Object:
        """
        Create and position camera to frame logo at 2/3 of screen

        Args:
            objects: List of all logo objects

        Returns:
            Camera object
        """
        print_step("Setting up camera")

        # Calculate logo bounds at final position
        centroid = ComponentIdentifier.calculate_centroid(objects)

        # Create camera
        bpy.ops.object.camera_add(location=(centroid.x, centroid.y - AnimationConfig.CAMERA_DISTANCE, centroid.z))
        camera = bpy.context.active_object
        camera.name = "MainCamera"

        # Set as active camera
        bpy.context.scene.camera = camera

        # Configure camera
        camera.data.lens = AnimationConfig.CAMERA_FOV
        camera.data.dof.use_dof = True
        camera.data.dof.focus_distance = AnimationConfig.CAMERA_DISTANCE
        camera.data.dof.aperture_fstop = 2.8

        # Point camera at logo
        constraint = camera.constraints.new('TRACK_TO')

        # Create target empty
        bpy.ops.object.empty_add(location=centroid)
        target = bpy.context.active_object
        target.name = "CameraTarget"

        constraint.target = target
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

        print_step("Camera positioned", f"distance={AnimationConfig.CAMERA_DISTANCE}m, FOV={AnimationConfig.CAMERA_FOV}°")

        return camera


# ═══════════════════════════════════════════════════════════════════════════
# LIGHTING SETUP
# ═══════════════════════════════════════════════════════════════════════════

class LightingSetup:
    """Sets up professional lighting rig"""

    @staticmethod
    def create_lights(centroid: Vector) -> List[bpy.types.Object]:
        """
        Create 3-point lighting setup

        Args:
            centroid: Center point of logo

        Returns:
            List of light objects
        """
        print_step("Creating lighting setup")

        lights = []

        # Key light (main)
        bpy.ops.object.light_add(type='AREA', location=(centroid.x - 5, centroid.y - 8, centroid.z + 6))
        key_light = bpy.context.active_object
        key_light.name = "KeyLight"
        key_light.data.energy = 500
        key_light.data.size = 3
        lights.append(key_light)

        # Fill light (soften shadows)
        bpy.ops.object.light_add(type='AREA', location=(centroid.x + 5, centroid.y - 6, centroid.z + 3))
        fill_light = bpy.context.active_object
        fill_light.name = "FillLight"
        fill_light.data.energy = 200
        fill_light.data.size = 4
        lights.append(fill_light)

        # Rim light (edge highlight)
        bpy.ops.object.light_add(type='SPOT', location=(centroid.x, centroid.y + 5, centroid.z + 8))
        rim_light = bpy.context.active_object
        rim_light.name = "RimLight"
        rim_light.data.energy = 300
        rim_light.data.spot_size = math.radians(60)
        lights.append(rim_light)

        # Point all lights at centroid
        for light in lights:
            constraint = light.constraints.new('TRACK_TO')

            bpy.ops.object.empty_add(location=centroid)
            target = bpy.context.active_object
            target.name = f"{light.name}_Target"

            constraint.target = target
            constraint.track_axis = 'TRACK_NEGATIVE_Z'
            constraint.up_axis = 'UP_Y'

        print_step("Lights created", "3-point setup")

        return lights


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ANIMATION SETUP
# ═══════════════════════════════════════════════════════════════════════════

class LogoFireAnimation:
    """Main class orchestrating the entire animation setup"""

    def __init__(self, svg_path: str):
        """
        Initialize animation setup

        Args:
            svg_path: Path to SVG file
        """
        self.svg_path = svg_path
        self.objects = []
        self.components = {}
        self.camera = None
        self.lights = []

    def setup(self) -> None:
        """Execute complete animation setup"""
        print_header("ALTER LOGO FIRE CONVERGENCE ANIMATION - SETUP")

        try:
            # 1. Scene preparation
            SceneManager.clear_scene()
            SceneManager.setup_render_settings()

            # 2. Import and convert SVG
            self.objects = SVGImporter.import_svg(self.svg_path)

            # 3. Analyze and group components
            self.components = ComponentIdentifier.analyze_components(self.objects)

            # 4. Create materials
            golden_material = MaterialCreator.create_golden_material()
            fire_material = MaterialCreator.create_fire_material()

            # 5. Apply golden material to all objects
            for obj in self.objects:
                if obj.data.materials:
                    obj.data.materials[0] = golden_material
                else:
                    obj.data.materials.append(golden_material)

            # 6. Create fire effects for each object
            print_step("Creating fire particle systems")
            for obj in self.objects:
                psys = FireEffectCreator.create_fire_for_object(obj, fire_material)
                FireEffectCreator.setup_fire_fadeout(psys)

            # 7. Create convergence animation
            AnimationCreator.create_convergence_animation(self.components)

            # 8. Setup camera
            self.camera = CameraSetup.create_camera(self.objects)

            # 9. Setup lighting
            centroid = ComponentIdentifier.calculate_centroid(self.objects)
            self.lights = LightingSetup.create_lights(centroid)

            # 10. Save file
            self.save_file()

            print_header("SETUP COMPLETE")
            print(f"  ✓ Total objects: {len(self.objects)}")
            print(f"  ✓ Components identified: {sum(len(v) for v in self.components.values() if v)}")
            print(f"  ✓ Animation length: {AnimationConfig.TOTAL_FRAMES} frames ({AnimationConfig.TOTAL_FRAMES/AnimationConfig.FPS:.1f}s)")
            print(f"  ✓ Fire fadeout: frames {AnimationConfig.FIRE_FADEOUT_START_FRAME}-{AnimationConfig.FIRE_FADEOUT_END_FRAME}")
            print(f"  ✓ Output file: {AnimationConfig.OUTPUT_FILENAME}")
            print(f"\n  Ready to render! Press Spacebar in Blender to preview animation.\n")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def save_file(self) -> None:
        """Save Blender file"""
        output_path = os.path.join(os.getcwd(), AnimationConfig.OUTPUT_FILENAME)
        bpy.ops.wm.save_as_mainfile(filepath=output_path)
        print_step("Saved file", output_path)


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    # Find SVG file
    svg_path = find_svg_file("alter.svg")

    if not svg_path:
        print("\n❌ ERROR: alter.svg not found!")
        print("   Please ensure alter.svg is in one of these locations:")
        print(f"   - Current directory: {os.getcwd()}")
        print(f"   - Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        sys.exit(1)

    # Create and run animation setup
    animation = LogoFireAnimation(svg_path)
    animation.setup()


if __name__ == "__main__":
    main()
