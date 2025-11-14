#!/usr/bin/env python3
"""
Run ALTER_LOGO_SEQUENTIAL_V3_CLEAN.py
"""

import subprocess
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
main_script = os.path.join(script_dir, "ALTER_LOGO_SEQUENTIAL_V3_CLEAN.py")

print("="*80)
print("ALTER LOGO SEQUENTIAL V3 CLEAN - FINAL VERSION")
print("="*80)
print(f"\nScript: {main_script}\n")

result = subprocess.run([
    "blender",
    "--python", main_script
], cwd=script_dir)

sys.exit(result.returncode)
