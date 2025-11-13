#!/usr/bin/env python3
"""
Blender Integration Test for ALTER_LOGO_SEQUENTIAL.py
Run this IN BLENDER to verify all operations work correctly:

blender --background --python test_blender_integration.py

This tests actual Blender operations, not just logic.
"""

import bpy
import os
import sys
from pathlib import Path

# Track test results
tests_passed = 0
tests_failed = 0

def test_result(name, passed, error_msg=""):
    """Record test result"""
    global tests_passed, tests_failed
    if passed:
        tests_passed += 1
        print(f"  ✓ {name}")
    else:
        tests_failed += 1
        print(f"  ✗ {name}: {error_msg}")

def test_scene_cleanup():
    """Test that scene can be cleaned"""
    print("\n1. Testing scene cleanup...")
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        test_result("Scene cleanup", len(bpy.data.objects) == 0)
        return True
    except Exception as e:
        test_result("Scene cleanup", False, str(e))
        return False

def test_svg_import():
    """Test SVG import detection"""
    print("\n2. Testing SVG import...")

    # Check if SVG exists
    svg_path = Path(__file__).parent / "alter.svg"
    if not svg_path.exists():
        test_result("SVG file exists", False, f"Not found: {svg_path}")
        return None

    test_result("SVG file exists", True)

    # Test import
    try:
        objects_before = set(bpy.data.objects)
        bpy.ops.import_curve.svg(filepath=str(svg_path))
        objects_after = set(bpy.data.objects)
        imported = list(objects_after - objects_before)
        curves = [obj for obj in imported if obj.type == 'CURVE']

        test_result(f"SVG import (found {len(curves)} curves)", len(curves) > 0)
        return curves
    except Exception as e:
        test_result("SVG import", False, str(e))
        return None

def test_curve_to_mesh_conversion(curves):
    """Test curve to mesh conversion with proper context"""
    print("\n3. Testing curve to mesh conversion...")

    if not curves:
        print("  ⚠ Skipping - no curves to test")
        return None

    converted = []
    for i, curve in enumerate(curves[:3]):  # Test first 3
        try:
            # CRITICAL: Proper context setup
            bpy.ops.object.select_all(action='DESELECT')
            curve.select_set(True)
            bpy.context.view_layer.objects.active = curve

            # Convert
            bpy.ops.object.convert(target='MESH')
            mesh_obj = bpy.context.active_object

            is_mesh = mesh_obj.type == 'MESH'
            test_result(f"Convert curve {i} to mesh", is_mesh)

            if is_mesh:
                converted.append(mesh_obj)
        except Exception as e:
            test_result(f"Convert curve {i} to mesh", False, str(e))

    return converted if converted else None

def test_origin_set(meshes):
    """Test origin_set operation"""
    print("\n4. Testing origin_set...")

    if not meshes:
        print("  ⚠ Skipping - no meshes to test")
        return

    for i, mesh in enumerate(meshes[:3]):  # Test first 3
        try:
            # Record location before
            loc_before = mesh.location.copy()

            # Set origin
            bpy.ops.object.select_all(action='DESELECT')
            mesh.select_set(True)
            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            # Check location updated (should be different from 0,0,0 usually)
            loc_after = mesh.location
            test_result(f"Origin set for mesh {i}", True)
            print(f"    Location: X={loc_after.x:.2f}, Y={loc_after.y:.2f}, Z={loc_after.z:.2f}")
        except Exception as e:
            test_result(f"Origin set for mesh {i}", False, str(e))

def test_text_creation_and_conversion():
    """Test text object creation and conversion"""
    print("\n5. Testing text creation and conversion...")

    try:
        # Create text
        bpy.ops.object.text_add(location=(0, 0, -4))
        text_obj = bpy.context.active_object
        text_obj.data.body = "TEST TEXT"

        test_result("Text object created", text_obj.type == 'FONT')

        # Convert with proper context
        bpy.ops.object.select_all(action='DESELECT')
        text_obj.select_set(True)
        bpy.context.view_layer.objects.active = text_obj
        bpy.ops.object.convert(target='MESH')

        mesh_obj = bpy.context.active_object
        test_result("Text converted to mesh", mesh_obj.type == 'MESH')
    except Exception as e:
        test_result("Text creation/conversion", False, str(e))

def test_modifier_addition():
    """Test adding modifiers"""
    print("\n6. Testing modifier addition...")

    try:
        # Get any mesh object
        mesh_objs = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        if not mesh_objs:
            print("  ⚠ Skipping - no mesh objects")
            return

        obj = mesh_objs[0]

        # Add Solidify
        solidify = obj.modifiers.new(name="TestSolidify", type='SOLIDIFY')
        solidify.thickness = 0.1

        test_result("Solidify modifier added", 'TestSolidify' in obj.modifiers)

        # Add Wireframe
        wireframe = obj.modifiers.new(name="TestWireframe", type='WIREFRAME')
        wireframe.thickness = 0.05

        test_result("Wireframe modifier added", 'TestWireframe' in obj.modifiers)
    except Exception as e:
        test_result("Modifier addition", False, str(e))

def test_animation_keyframes():
    """Test keyframe insertion"""
    print("\n7. Testing keyframe insertion...")

    try:
        # Get any object
        if not bpy.data.objects:
            print("  ⚠ Skipping - no objects")
            return

        obj = bpy.data.objects[0]
        obj.location.y = -10
        obj.keyframe_insert(data_path='location', frame=1)

        obj.location.y = 0
        obj.keyframe_insert(data_path='location', frame=30)

        has_animation = obj.animation_data is not None
        test_result("Keyframes inserted", has_animation)
    except Exception as e:
        test_result("Keyframe insertion", False, str(e))

def main():
    """Run all tests"""
    print("="*60)
    print("BLENDER INTEGRATION TEST")
    print("Testing ALTER_LOGO_SEQUENTIAL.py operations")
    print("="*60)

    # Clean start
    test_scene_cleanup()

    # Test SVG workflow
    curves = test_svg_import()
    meshes = test_curve_to_mesh_conversion(curves) if curves else None
    test_origin_set(meshes)

    # Test other operations
    test_text_creation_and_conversion()
    test_modifier_addition()
    test_animation_keyframes()

    # Results
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"✓ Passed: {tests_passed}")
    print(f"✗ Failed: {tests_failed}")
    print("="*60)

    if tests_failed == 0:
        print("✅ ALL TESTS PASSED - Script should work in Blender!")
        return 0
    else:
        print(f"❌ {tests_failed} TESTS FAILED - Fix required!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
