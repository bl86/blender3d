#!/usr/bin/env python3
"""
Simple wrapper to run ALTER_LOGO_SEQUENTIAL_V3.py in Blender
"""

import subprocess
import sys
import os

# Get directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(script_dir, "ALTER_LOGO_SEQUENTIAL_V3.py")

print("="*80)
print("RUNNING ALTER LOGO SEQUENTIAL V3")
print("="*80)
print(f"\nScript: {main_script}")
print("\nStarting Blender...\n")

# Run Blender with script
result = subprocess.run([
    "blender",
    "--python", main_script
], cwd=script_dir)

sys.exit(result.returncode)
