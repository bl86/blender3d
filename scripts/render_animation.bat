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
echo.

"!BLENDER_EXE!" --background "%BLEND_FILE%" --python-expr "import bpy; bpy.context.scene.cycles.samples = %SAMPLES%; bpy.context.scene.render.resolution_percentage = %RESOLUTION%" --render-anim

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Render failed!
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
pause
