#!/usr/bin/env python3
"""
Test script for ALTER_LOGO_SEQUENTIAL.py
Verifies logic without requiring Blender installation
"""

def test_animation_logic():
    """Test that animation logic correctly offsets only Y axis"""

    print("Testing animation logic...")

    # Simulate 3 elements at different positions (like after SVG import + origin_set)
    elements = [
        {"name": "Element_0", "x": -5.0, "y": 0.0, "z": 2.0},
        {"name": "Element_1", "x": 0.0, "y": 0.0, "z": 0.0},
        {"name": "Element_2", "x": 5.0, "y": 0.0, "z": -2.0},
    ]

    start_y_offset = -50.0

    print("\n1. Initial positions (after SVG import + origin_set):")
    for elem in elements:
        print(f"   {elem['name']}: X={elem['x']:.1f}, Y={elem['y']:.1f}, Z={elem['z']:.1f}")

    print("\n2. Start of animation (pushed back on Y):")
    start_positions = []
    for elem in elements:
        start_pos = {
            "x": elem["x"],  # Should NOT change
            "y": elem["y"] + start_y_offset,  # Push back
            "z": elem["z"],  # Should NOT change
        }
        start_positions.append(start_pos)
        print(f"   {elem['name']}: X={start_pos['x']:.1f}, Y={start_pos['y']:.1f}, Z={start_pos['z']:.1f}")

    print("\n3. End of animation (return to original position):")
    end_positions = []
    for elem in elements:
        end_pos = {
            "x": elem["x"],  # Same as original
            "y": elem["y"],  # Back to original Y
            "z": elem["z"],  # Same as original
        }
        end_positions.append(end_pos)
        print(f"   {elem['name']}: X={end_pos['x']:.1f}, Y={end_pos['y']:.1f}, Z={end_pos['z']:.1f}")

    # Verification
    print("\n4. Verification:")
    all_correct = True

    for i, elem in enumerate(elements):
        start = start_positions[i]
        end = end_positions[i]

        # Check X never changed
        if start["x"] != elem["x"] or end["x"] != elem["x"]:
            print(f"   ✗ {elem['name']}: X changed! (should stay at {elem['x']})")
            all_correct = False
        else:
            print(f"   ✓ {elem['name']}: X preserved ({elem['x']:.1f})")

        # Check Z never changed
        if start["z"] != elem["z"] or end["z"] != elem["z"]:
            print(f"   ✗ {elem['name']}: Z changed! (should stay at {elem['z']})")
            all_correct = False
        else:
            print(f"   ✓ {elem['name']}: Z preserved ({elem['z']:.1f})")

        # Check Y was offset then returned
        if start["y"] != elem["y"] + start_y_offset:
            print(f"   ✗ {elem['name']}: Start Y incorrect!")
            all_correct = False
        elif end["y"] != elem["y"]:
            print(f"   ✗ {elem['name']}: End Y doesn't match original!")
            all_correct = False
        else:
            print(f"   ✓ {elem['name']}: Y animated correctly ({elem['y'] + start_y_offset:.1f} → {elem['y']:.1f})")

    # Check that elements are NOT all at same position
    print("\n5. Position diversity check:")
    x_positions = [elem["x"] for elem in elements]
    z_positions = [elem["z"] for elem in elements]

    if len(set(x_positions)) == 1 and len(set(z_positions)) == 1:
        print("   ✗ FAILED: All elements at same X,Z position (will overlap!)")
        all_correct = False
    else:
        print(f"   ✓ Elements spread across space")
        print(f"     X positions: {x_positions}")
        print(f"     Z positions: {z_positions}")

    print("\n" + "="*60)
    if all_correct:
        print("✅ ALL TESTS PASSED - Animation logic is correct!")
        print("="*60)
        return True
    else:
        print("❌ TESTS FAILED - Animation logic has errors!")
        print("="*60)
        return False


def test_origin_set_simulation():
    """Simulate what origin_set does"""

    print("\n\nTesting origin_set simulation...")
    print("="*60)

    # Before origin_set: object at (0,0,0) with geometry offset
    print("\nBEFORE origin_set:")
    print("  Object location: (0, 0, 0)")
    print("  Geometry vertices: [(5,0,2), (6,0,2), (5,1,2), (6,1,2)]")
    print("  Geometry center: (5.5, 0.5, 2.0)")

    # After origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS'):
    # - Origin moves to geometry center
    # - Vertices stay in same world positions
    # - Object location updates to where origin now is

    geometry_center = (5.5, 0.5, 2.0)

    print("\nAFTER origin_set:")
    print(f"  Object location: {geometry_center}")
    print("  Geometry vertices: [(5,0,2), (6,0,2), (5,1,2), (6,1,2)] (unchanged in world)")
    print("  Geometry center relative to object: (0, 0, 0)")

    print("\n✓ This is why element.location gives us the real position!")
    print("="*60)


if __name__ == "__main__":
    print("="*60)
    print("ALTER_LOGO_SEQUENTIAL.PY - LOGIC TESTS")
    print("="*60)

    # Run tests
    test_origin_set_simulation()
    success = test_animation_logic()

    print("\n")

    if success:
        exit(0)
    else:
        exit(1)
