"""
System check utility for Blender animation project
Verifies all dependencies and system requirements
"""

import sys
import os
import subprocess
import platform


def check_blender():
    """Check if Blender is installed and get version"""
    try:
        result = subprocess.run(
            ['blender', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        version_line = result.stdout.split('\n')[0]
        print(f"✓ Blender found: {version_line}")
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("✗ Blender not found in PATH")
        print("  Install from: https://www.blender.org/download/")
        return False


def check_python():
    """Check Python version"""
    version = sys.version.split()[0]
    major, minor = map(int, version.split('.')[:2])

    if major >= 3 and minor >= 9:
        print(f"✓ Python {version}")
        return True
    else:
        print(f"✗ Python {version} (requires 3.9+)")
        return False


def check_files():
    """Check if required files exist"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    required_files = {
        'alter.svg': os.path.join(project_root, 'alter.svg'),
        'logo_animation.py': os.path.join(script_dir, 'logo_animation.py'),
    }

    all_found = True
    for name, path in required_files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {name} ({size:,} bytes)")
        else:
            print(f"✗ {name} not found at {path}")
            all_found = False

    return all_found


def check_disk_space():
    """Check available disk space"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    try:
        stat = os.statvfs(project_root)
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)

        if free_gb >= 5:
            print(f"✓ Disk space: {free_gb:.1f} GB available")
            return True
        else:
            print(f"⚠ Disk space: {free_gb:.1f} GB (recommended: 5+ GB)")
            return True
    except:
        print("? Could not check disk space")
        return True


def check_gpu():
    """Check for GPU acceleration support"""
    # This is a basic check - actual GPU detection would require
    # running inside Blender's Python environment
    system = platform.system()

    if system == 'Linux':
        # Check for NVIDIA
        try:
            subprocess.run(['nvidia-smi'], capture_output=True, check=True)
            print("✓ NVIDIA GPU detected (nvidia-smi available)")
            return True
        except:
            pass

    print("? GPU check requires running inside Blender")
    print("  Enable GPU in: Edit → Preferences → System → Cycles Render Devices")
    return True


def check_permissions():
    """Check write permissions"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    test_file = os.path.join(project_root, '.write_test')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✓ Write permissions OK")
        return True
    except:
        print("✗ No write permissions in project directory")
        return False


def main():
    """Run all system checks"""
    print("=" * 60)
    print("Alter Logo Animation - System Check")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python),
        ("Blender Installation", check_blender),
        ("Required Files", check_files),
        ("Disk Space", check_disk_space),
        ("GPU Support", check_gpu),
        ("Write Permissions", check_permissions),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        result = check_func()
        results.append(result)

    print()
    print("=" * 60)

    if all(results):
        print("✓ All checks passed! Ready to create animation.")
        print()
        print("Next steps:")
        print("  1. Run: ./scripts/setup_scene.sh")
        print("  2. Open: blender alter_logo_animation.blend")
        print("  3. Render: ./scripts/render_animation.sh")
    else:
        print("⚠ Some checks failed. Please resolve issues above.")
        return 1

    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
