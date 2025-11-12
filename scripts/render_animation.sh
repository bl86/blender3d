#!/bin/bash
# Render script for Alter logo animation
# Usage: ./render_animation.sh [quality]
# Quality options: preview, production (default: production)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BLEND_FILE="$PROJECT_ROOT/alter_logo_animation.blend"
OUTPUT_DIR="$PROJECT_ROOT/output"

QUALITY="${1:-production}"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Alter Logo Animation Renderer${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if Blender is installed
if ! command -v blender &> /dev/null; then
    echo -e "${RED}ERROR: Blender is not installed or not in PATH${NC}"
    echo "Please install Blender 3.0 or higher"
    exit 1
fi

# Check if blend file exists
if [ ! -f "$BLEND_FILE" ]; then
    echo -e "${YELLOW}Blend file not found. Generating...${NC}"
    echo ""
    blender --background --python "$SCRIPT_DIR/logo_animation.py"
    echo ""
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Set render settings based on quality
if [ "$QUALITY" == "preview" ]; then
    echo -e "${YELLOW}Rendering in PREVIEW mode (faster, lower quality)${NC}"
    SAMPLES=64
    RESOLUTION=50
elif [ "$QUALITY" == "production" ]; then
    echo -e "${GREEN}Rendering in PRODUCTION mode (slower, high quality)${NC}"
    SAMPLES=256
    RESOLUTION=100
else
    echo -e "${RED}Invalid quality option: $QUALITY${NC}"
    echo "Use 'preview' or 'production'"
    exit 1
fi

echo ""
echo "Settings:"
echo "  Samples: $SAMPLES"
echo "  Resolution: $RESOLUTION%"
echo "  Output: $OUTPUT_DIR"
echo ""

# Render animation
echo -e "${GREEN}Starting render...${NC}"
echo ""

blender --background "$BLEND_FILE" \
    --python-expr "import bpy; bpy.context.scene.cycles.samples = $SAMPLES; bpy.context.scene.render.resolution_percentage = $RESOLUTION" \
    --render-anim

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Render Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Output files: $OUTPUT_DIR"
echo ""
