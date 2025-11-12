"""
System check utility for Blender animation project
Verifies all dependencies and system requirements
Cross-platform: Windows, Linux, macOS
"""

import sys
import os
import subprocess
import platform
import shutil


def check_blender():
    """Check if Blender is installed and get version"""
    blender_exe = None

    # Try to find blender in PATH
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
        pass

    # On Windows, check common installation paths
    if platform.system() == 'Windows':
        # First, try to search in Blender Foundation folder
        blender_base = r"C:\Program Files\Blender Foundation"
        if os.path.exists(blender_base):
            for folder in os.listdir(blender_base):
                blender_path = os.path.join(blender_base, folder, "blender.exe")
                if os.path.exists(blender_path):
                    try:
                        result = subprocess.run(
                            [blender_path, '--version'],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        version_line = result.stdout.split('\n')[0]
                        print(f"✓ Blender found: {version_line}")
                        print(f"  Location: {blender_path}")
                        return True
                    except:
                        pass

        # Fallback to specific version checks
        windows_paths = [
            r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.5\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.4\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender 3.3\blender.exe",
            r"C:\Program Files\Blender Foundation\Blender\blender.exe",
        ]

        for path in windows_paths:
            if os.path.exists(path):
                try:
                    result = subprocess.run(
                        [path, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    version_line = result.stdout.split('\n')[0]
                    print(f"✓ Blender found: {version_line}")
                    print(f"  Location: {path}")
                    return True
                except:
                    pass

    print("✗ Blender not found in PATH or common locations")
    print("  Install from: https://www.blender.org/download/")
    if platform.system() == 'Windows':
        print("  Or add Blender to PATH (see README)")
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
        # Use shutil.disk_usage for cross-platform compatibility
        stat = shutil.disk_usage(project_root)
        free_gb = stat.free / (1024**3)

        if free_gb >= 5:
            print(f"✓ Disk space: {free_gb:.1f} GB available")
            return True
        else:
            print(f"⚠ Disk space: {free_gb:.1f} GB (recommended: 5+ GB)")
            return True
    except Exception as e:
        print(f"? Could not check disk space: {e}")
        return True


def check_gpu():
    """Check for GPU acceleration support"""
    system = platform.system()
    gpu_found = False

    if system == 'Linux' or system == 'Windows':
        # Check for NVIDIA
        try:
            result = subprocess.run(
                ['nvidia-smi'],
                capture_output=True,
                check=True,
                timeout=5
            )
            print("✓ NVIDIA GPU detected (nvidia-smi available)")
            gpu_found = True
        except:
            pass

    if system == 'Windows' and not gpu_found:
        # Check for AMD on Windows using wmic
        try:
            result = subprocess.run(
                ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'AMD' in result.stdout or 'Radeon' in result.stdout:
                print("✓ AMD GPU detected")
                gpu_found = True
            elif 'Intel' in result.stdout and 'NVIDIA' not in result.stdout:
                print("⚠ Intel integrated GPU detected (slower rendering)")
                gpu_found = True
        except:
            pass

    if not gpu_found:
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

        system = platform.system()
        if system == 'Windows':
            print("  1. Run: quickstart.bat  (or quickstart.ps1 for PowerShell)")
            print("  2. Or: scripts\\setup_scene.bat")
            print("  3. Render: scripts\\render_animation.bat production")
        else:
            print("  1. Run: ./quickstart.sh")
            print("  2. Or: ./scripts/setup_scene.sh")
            print("  3. Render: ./scripts/render_animation.sh production")
    else:
        print("⚠ Some checks failed. Please resolve issues above.")
        return 1

    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
