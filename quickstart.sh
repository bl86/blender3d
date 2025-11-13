#!/bin/bash
# Quickstart script - sets up and previews animation in one command
# Usage: ./quickstart.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
    _    _ _            _
   / \  | | |_ ___ _ __| |    ___   __ _  ___
  / _ \ | | __/ _ \ '__| |   / _ \ / _` |/ _ \
 / ___ \| | ||  __/ |  | |__| (_) | (_| | (_) |
/_/   \_\_|\__\___|_|  |_____\___/ \__, |\___/
                                    |___/
    ___          _                 _   _
   / _ \        / \   _ __  (_)_ __ ___   __ _| |_(_) ___  _ __
  | | | |___   / _ \ | '_ \ | | '_ ` _ \ / _` | __| |/ _ \| '_ \
  | |_| |___| / ___ \| | | || | | | | | | (_| | |_| | (_) | | | |
   \__\_\    /_/   \_\_| |_|/ |_| |_| |_|\__,_|\__|_|\___/|_| |_|
                           |__/
EOF
echo -e "${NC}"

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Quickstart Setup${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Step 1: System check
echo -e "${YELLOW}[1/3] Running system check...${NC}"
echo ""
python3 "$SCRIPT_DIR/scripts/check_system.py"
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}Fix the issues above and run again.${NC}"
    exit 1
fi

echo ""
read -p "Press Enter to continue to scene setup..."
clear

# Step 2: Setup scene
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Scene Setup${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}[2/3] Generating Blender scene...${NC}"
echo ""
chmod +x "$SCRIPT_DIR/scripts/"*.sh
"$SCRIPT_DIR/scripts/setup_scene.sh"

echo ""
read -p "Press Enter to open in Blender..."
clear

# Step 3: Open in Blender
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Opening in Blender${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}[3/3] Launching Blender...${NC}"
echo ""
echo "Tips:"
echo "  • Press SPACEBAR to play animation"
echo "  • Press F12 to render current frame"
echo "  • Press CTRL+F12 to render full animation"
echo "  • Timeline shows 300 frames (10 seconds)"
echo "  • Fire fades out around frame 200"
echo ""
sleep 2

blender "$SCRIPT_DIR/alter_logo_animation.blend"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Session Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "To render from command line:"
echo "  ./scripts/render_animation.sh preview     # Fast preview"
echo "  ./scripts/render_animation.sh production  # High quality"
echo ""
