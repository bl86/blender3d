@echo off
REM Quickstart script for Windows
REM Usage: quickstart.bat

setlocal enabledelayedexpansion

cls

echo.
echo     _    _ _            _
echo    / \  ^| ^| ^|_ ___ _ __^| ^|    ___   __ _  ___
echo   / _ \ ^| ^| __/ _ \ '__^| ^|   / _ \ / _` ^|/ _ \
echo  / ___ \^| ^| ^|^|  __/ ^|  ^| ^|__^| (_) ^| (_^| ^| (_) ^|
echo /_/   \_\_^\__\___^|_^|  ^|_____\___/ \__, ^\___/
echo                                    ^|___/
echo     ___          _                 _   _
echo    / _ \        / \   _ __  (_)_ __ ___   __ _^| ^|_(_) ___  _ __
echo   ^| ^| ^| ^|___   / _ \ ^| '_ \ ^| ^| '_ ` _ \ / _` ^| __^| ^|/ _ \^| '_ \
echo   ^| ^|_^| ^|___^| / ___ \^| ^| ^| ^|^| ^| ^| ^| ^| ^| ^| (_^| ^| ^|_^| ^| (_) ^| ^| ^| ^|
echo    \__\_\    /_/   \_\_^| ^|_^|/ ^|_^| ^|_^| ^|_^\__,_^\__^|_^\___/^|_^| ^|_^|
echo                          ^|__/
echo.
echo ================================
echo   Windows Quickstart Setup
echo ================================
echo.

REM Step 1: System check
echo [1/3] Running system check...
echo.
python scripts\check_system.py
if errorlevel 1 (
    echo.
    echo Fix the issues above and run again.
    pause
    exit /b 1
)

echo.
echo Press any key to continue to scene setup...
pause >nul
cls

REM Step 2: Setup scene
echo ================================
echo   Scene Setup
echo ================================
echo.
echo [2/3] Generating Blender scene...
echo.
call scripts\setup_scene.bat
if errorlevel 1 (
    echo Scene setup failed!
    pause
    exit /b 1
)

echo.
echo Press any key to open in Blender...
pause >nul
cls

REM Step 3: Open in Blender
echo ================================
echo   Opening in Blender
echo ================================
echo.
echo [3/3] Launching Blender...
echo.
echo Tips:
echo   * Press SPACEBAR to play animation
echo   * Press F12 to render current frame
echo   * Press CTRL+F12 to render full animation
echo   * Timeline shows 300 frames (10 seconds)
echo   * Fire fades out around frame 200
echo.
timeout /t 2 >nul

REM Find Blender installation
set "BLENDER_EXE="

REM First, try blender in PATH
where blender >nul 2>nul
if %errorlevel% equ 0 (
    set "BLENDER_EXE=blender"
    goto :found_blender
)

REM Search for any Blender installation in Program Files
set "BLENDER_BASE=C:\Program Files\Blender Foundation"
if exist "%BLENDER_BASE%" (
    REM Look for any version by checking folders
    for /d %%i in ("%BLENDER_BASE%\Blender*") do (
        if exist "%%i\blender.exe" (
            set "BLENDER_EXE=%%i\blender.exe"
            goto :found_blender
        )
    )
)

REM If still not found, try specific version paths (newest first)
for %%v in (4.5 4.4 4.3 4.2 4.1 4.0 3.6 3.5 3.4 3.3) do (
    if exist "C:\Program Files\Blender Foundation\Blender %%v\blender.exe" (
        set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender %%v\blender.exe"
        goto :found_blender
    )
)

REM Try without version number
if exist "C:\Program Files\Blender Foundation\Blender\blender.exe" (
    set "BLENDER_EXE=C:\Program Files\Blender Foundation\Blender\blender.exe"
    goto :found_blender
)

REM Not found
echo ERROR: Blender not found!
echo.
echo Searched in:
echo   - System PATH
echo   - C:\Program Files\Blender Foundation\
echo.
echo Please install Blender from:
echo   https://www.blender.org/download/
echo.
echo Or add Blender to your system PATH
pause
exit /b 1

:found_blender
echo Using Blender: !BLENDER_EXE!
echo.
start "" "!BLENDER_EXE!" "%~dp0alter_logo_animation.blend"

timeout /t 2 >nul
cls

echo.
echo ================================
echo Session Complete!
echo ================================
echo.
echo Blender is now open with your animation.
echo.
echo To render from command line:
echo   scripts\render_animation.bat preview     # Fast preview (10 min)
echo   scripts\render_animation.bat production  # High quality (45+ min)
echo.
echo For help, see:
echo   README.md           - Quick start guide
echo   WINDOWS_INSTALL.md  - Detailed Windows guide
echo   USAGE_EXAMPLES.md   - Practical examples
echo.
pause
