@echo off
REM Quick start script for ALTER Logo Fire Convergence Animation (Windows)

echo ===============================================================================
echo   ALTER LOGO FIRE CONVERGENCE ANIMATION - QUICK START
echo ===============================================================================
echo.

REM Step 1: Run tests
echo Step 1/2: Running tests...
python test_fire_convergence.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo X Tests failed! Please fix issues before proceeding.
    exit /b 1
)

echo.
echo √ All tests passed!
echo.

REM Step 2: Generate animation scene
echo Step 2/2: Generating Blender scene...
echo.

blender --background --python ALTER_LOGO_FIRE_CONVERGENCE.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo X Scene generation failed!
    exit /b 1
)

echo.
echo ===============================================================================
echo   √ SUCCESS! Animation scene created:
echo      alter_logo_fire_convergence.blend
echo.
echo   Next steps:
echo     1. Open the .blend file in Blender
echo     2. Press SPACEBAR to preview animation
echo     3. Press Ctrl+F12 to render full animation
echo ===============================================================================
echo.

pause
