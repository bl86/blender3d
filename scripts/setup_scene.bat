@echo off
REM Setup script to generate the Blender scene on Windows
REM This will create alter_logo_animation.blend in the project root

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

echo ================================
echo Alter Logo Scene Setup
echo ================================
echo.

REM Check if Blender is installed
set "BLENDER_EXE="
where blender >nul 2>nul
if %errorlevel% equ 0 (
    set "BLENDER_EXE=blender"
    goto :blender_found
)

REM Search common installation paths
if exist "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
) else if exist "C:\Program Files\Blender Foundation\Blender 3.5\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender 3.5\blender.exe"
) else if exist "C:\Program Files\Blender Foundation\Blender 3.4\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender 3.4\blender.exe"
) else if exist "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
) else if exist "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender 4.1\blender.exe"
) else if exist "C:\Program Files\Blender Foundation\Blender\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender\blender.exe"
) else (
    echo ERROR: Blender is not installed or not in PATH
    echo Please install Blender 3.0 or higher
    echo Download: https://www.blender.org/download/
    exit /b 1
)

:blender_found

REM Check if SVG exists
if not exist "%PROJECT_ROOT%\alter.svg" (
    echo ERROR: alter.svg not found in project root
    exit /b 1
)

echo Generating Blender scene...
echo.

REM Run the Python script in Blender
cd /d "%PROJECT_ROOT%"
"!BLENDER_EXE!" --background --python "%SCRIPT_DIR%logo_animation.py"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Scene generation failed!
    exit /b 1
)

echo.
echo ================================
echo Scene Setup Complete!
echo ================================
echo.
echo Blend file created: alter_logo_animation.blend
echo.
echo Next steps:
echo   1. Open in Blender: blender alter_logo_animation.blend
echo   2. Or render: scripts\render_animation.bat
echo.
