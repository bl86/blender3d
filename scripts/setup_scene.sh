#!/bin/bash
# Setup script to generate the Blender scene
# This will create alter_logo_animation.blend in the project root

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Alter Logo Scene Setup${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if Blender is installed
if ! command -v blender &> /dev/null; then
    echo -e "${RED}ERROR: Blender is not installed or not in PATH${NC}"
    echo "Please install Blender 3.0 or higher"
    exit 1
fi

# Check if SVG exists
if [ ! -f "$PROJECT_ROOT/alter.svg" ]; then
    echo -e "${RED}ERROR: alter.svg not found in project root${NC}"
    exit 1
fi

echo -e "${YELLOW}Generating Blender scene...${NC}"
echo ""

# Run the Python script in Blender
cd "$PROJECT_ROOT"
blender --background --python "$SCRIPT_DIR/logo_animation.py"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Scene Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Blend file created: alter_logo_animation.blend"
echo ""
echo "Next steps:"
echo "  1. Open in Blender: blender alter_logo_animation.blend"
echo "  2. Or render: ./scripts/render_animation.sh"
echo ""
