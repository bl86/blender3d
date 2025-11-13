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

REM First, try blender in PATH
where blender >nul 2>nul
if %errorlevel% equ 0 (
    set "BLENDER_EXE=blender"
    goto :blender_found
)

REM Search for any Blender installation in Program Files
set "BLENDER_BASE=C:\Program Files\Blender Foundation"
if exist "%BLENDER_BASE%" (
    REM Look for the newest version by checking folders
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
echo.
echo Or add your Blender installation to PATH
pause
exit /b 1

:blender_found
echo Found Blender: !BLENDER_EXE!
echo.

REM Check if SVG exists
if not exist "%PROJECT_ROOT%\alter.svg" (
    echo ERROR: alter.svg not found in project root
    echo Expected location: %PROJECT_ROOT%\alter.svg
    pause
    exit /b 1
)

echo Generating Blender scene...
echo This may take a few minutes...
echo.

REM Run the Python script in Blender
cd /d "%PROJECT_ROOT%"
"!BLENDER_EXE!" --background --python "%SCRIPT_DIR%logo_animation.py"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Scene generation failed!
    echo.
    echo Troubleshooting:
    echo   1. Make sure Blender is properly installed
    echo   2. Check that alter.svg exists in project root
    echo   3. Try running: python scripts\check_system.py
    pause
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
echo   1. Open in Blender: "!BLENDER_EXE!" alter_logo_animation.blend
echo   2. Or render: scripts\render_animation.bat production
echo.
pause
