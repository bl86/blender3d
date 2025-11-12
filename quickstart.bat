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
    REM Try blender in PATH
    where blender >nul 2>nul
    if !errorlevel! equ 0 (
        set "BLENDER_EXE=blender"
    ) else (
        echo ERROR: Blender not found!
        echo Please install Blender or add it to PATH
        echo Download: https://www.blender.org/download/
        pause
        exit /b 1
    )
)

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
echo To render from command line:
echo   scripts\render_animation.bat preview     # Fast preview
echo   scripts\render_animation.bat production  # High quality
echo.
pause
