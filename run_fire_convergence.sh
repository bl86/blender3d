#!/bin/bash
# Quick start script for ALTER Logo Fire Convergence Animation

set -e  # Exit on error

echo "═══════════════════════════════════════════════════════════════════════════"
echo "  ALTER LOGO FIRE CONVERGENCE ANIMATION - QUICK START"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Run tests
echo "Step 1/2: Running tests..."
python3 test_fire_convergence.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Tests failed! Please fix issues before proceeding."
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo ""

# Step 2: Generate animation scene
echo "Step 2/2: Generating Blender scene..."
echo ""

blender --background --python ALTER_LOGO_FIRE_CONVERGENCE.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Scene generation failed!"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "  ✅ SUCCESS! Animation scene created:"
echo "     alter_logo_fire_convergence.blend"
echo ""
echo "  Next steps:"
echo "    1. Open the .blend file in Blender"
echo "    2. Press SPACEBAR to preview animation"
echo "    3. Press Ctrl+F12 to render full animation"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
