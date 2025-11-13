@echo off
REM Render script for Alter logo animation on Windows
REM Usage: render_animation.bat [quality]
REM Quality options: preview, production (default: production)

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "BLEND_FILE=%PROJECT_ROOT%\alter_logo_animation.blend"
set "OUTPUT_DIR=%PROJECT_ROOT%\output"

set "QUALITY=%~1"
if "%QUALITY%"=="" set "QUALITY=production"

echo ================================
echo Alter Logo Animation Renderer
echo ================================
echo.

REM Check if Blender is installed
set "BLENDER_EXE="

REM First, try blender in PATH
where blender >nul 2>nul
if %errorlevel% equ 0 (
    set "BLENDER_EXE=blender"
    goto :blender_found
)

REM Search for any Blender installation in Program Files
set "BLENDER_BASE=C:\Program Files\Blender Foundation"
if exist "%BLENDER_BASE%" (
    REM Look for any version by checking folders
    for /d %%i in ("%BLENDER_BASE%\Blender*") do (
        if exist "%%i\blender.exe" (
            set "BLENDER_EXE=%%i\blender.exe"
            goto :blender_found
        )
    )
)

REM If still not found, try specific version paths (newest first)
for %%v in (4.5 4.4 4.3 4.2 4.1 4.0 3.6 3.5 3.4 3.3) do (
    if exist "C:\Program Files\Blender Foundation\Blender %%v\blender.exe" (
        set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender %%v\blender.exe"
        goto :blender_found
    )
)

REM Try without version number
if exist "C:\Program Files\Blender Foundation\Blender\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender\blender.exe"
    goto :blender_found
)

REM Not found
echo ERROR: Blender is not installed or not in PATH
echo.
echo Searched in:
echo   - System PATH
echo   - C:\Program Files\Blender Foundation\
echo.
echo Please install Blender 3.0 or higher from:
echo   https://www.blender.org/download/
pause
exit /b 1

:blender_found
echo Found Blender: !BLENDER_EXE!
echo.

REM Check if blend file exists
if not exist "%BLEND_FILE%" (
    echo Blend file not found. Generating...
    echo.
    call "%SCRIPT_DIR%setup_scene.bat"
    if errorlevel 1 (
        echo Scene generation failed!
        pause
        exit /b 1
    )
    echo.
)

REM Create output directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Set render settings based on quality
if /i "%QUALITY%"=="preview" (
    echo Rendering in PREVIEW mode (faster, lower quality)
    set "SAMPLES=64"
    set "RESOLUTION=50"
) else if /i "%QUALITY%"=="production" (
    echo Rendering in PRODUCTION mode (slower, high quality)
    set "SAMPLES=256"
    set "RESOLUTION=100"
) else (
    echo Invalid quality option: %QUALITY%
    echo Use 'preview' or 'production'
    echo.
    echo Examples:
    echo   render_animation.bat preview
    echo   render_animation.bat production
    pause
    exit /b 1
)

echo.
echo Settings:
echo   Samples: %SAMPLES%
echo   Resolution: %RESOLUTION%%%
echo   Output: %OUTPUT_DIR%
echo.

REM Render animation
echo Starting render...
echo This may take from 10 minutes (preview) to several hours (production)
echo.

"!BLENDER_EXE!" --background "%BLEND_FILE%" --python-expr "import bpy; bpy.context.scene.cycles.samples = %SAMPLES%; bpy.context.scene.render.resolution_percentage = %RESOLUTION%" --render-anim

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Render failed!
    echo.
    echo Troubleshooting:
    echo   1. Check that blend file exists
    echo   2. Make sure you have enough disk space (~5GB)
    echo   3. Try: python scripts\check_system.py
    pause
    exit /b 1
)

echo.
echo ================================
echo Render Complete!
echo ================================
echo.
echo Output files: %OUTPUT_DIR%
echo.
echo To view the animation:
echo   - Open any video player
echo   - Load files from: %OUTPUT_DIR%
echo.
pause
