# PowerShell Quickstart Script for Alter Logo Animation
# Usage: .\quickstart.ps1

param(
    [switch]$SkipChecks = $false
)

$ErrorActionPreference = "Stop"

function Write-ColorOutput($ForegroundColor, $Message) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $fc
}

Clear-Host

Write-Host @"

    _    _ _            _
   / \  | | |_ ___ _ __| |    ___   __ _  ___
  / _ \ | | __/ _ \ '__| |   / _ \ / _` |/ _ \
 / ___ \| | ||  __/ |  | |__| (_) | (_| | (_) |
/_/   \_\_|\__\___|_|  |_____\___/ \__, |\___/
                                    |___/
    ___          _                 _   _
   / _ \        / \   _ __  (_)_ __ ___   __ _| |_(_) ___  _ __
  | | | |___   / _ \ | '_ \ | | '_ ` _ \ / _` | __| |/ _ \| '_ \
  | |_| |___| / ___ \| | | || | | | | | | (_| | |_| | (_) | | | |
   \__\_\    /_/   \_\_| |_|/ |_| |_| |_|\__,_|\__|_|\___/|_| |_|
                           |__/

"@ -ForegroundColor Cyan

Write-Host "================================" -ForegroundColor Green
Write-Host "  PowerShell Quickstart Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Step 1: System check
if (-not $SkipChecks) {
    Write-Host "[1/3] Running system check..." -ForegroundColor Yellow
    Write-Host ""

    $checkResult = python "$PSScriptRoot\scripts\check_system.py"
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput Red "`nFix the issues above and run again."
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host ""
    Read-Host "Press Enter to continue to scene setup"
    Clear-Host
}

# Step 2: Setup scene
Write-Host "================================" -ForegroundColor Green
Write-Host "  Scene Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "[2/3] Generating Blender scene..." -ForegroundColor Yellow
Write-Host ""

& "$PSScriptRoot\scripts\setup_scene.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-ColorOutput Red "Scene setup failed!"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Read-Host "Press Enter to open in Blender"
Clear-Host

# Step 3: Open in Blender
Write-Host "================================" -ForegroundColor Green
Write-Host "  Opening in Blender" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "[3/3] Launching Blender..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Tips:"
Write-Host "  * Press SPACEBAR to play animation"
Write-Host "  * Press F12 to render current frame"
Write-Host "  * Press CTRL+F12 to render full animation"
Write-Host "  * Timeline shows 300 frames (10 seconds)"
Write-Host "  * Fire fades out around frame 200"
Write-Host ""
Start-Sleep -Seconds 2

# Find Blender
$blenderPaths = @(
    "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.5\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.4\blender.exe",
    "C:\Program Files\Blender Foundation\Blender\blender.exe"
)

$blenderExe = $null
foreach ($path in $blenderPaths) {
    if (Test-Path $path) {
        $blenderExe = $path
        break
    }
}

if (-not $blenderExe) {
    # Try PATH
    $blenderExe = (Get-Command blender -ErrorAction SilentlyContinue).Source
}

if (-not $blenderExe) {
    Write-ColorOutput Red "ERROR: Blender not found!"
    Write-Host "Please install Blender or add it to PATH"
    Write-Host "Download: https://www.blender.org/download/"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Using Blender: $blenderExe" -ForegroundColor Cyan
Write-Host ""

$blendFile = Join-Path $PSScriptRoot "alter_logo_animation.blend"
Start-Process -FilePath $blenderExe -ArgumentList $blendFile

Start-Sleep -Seconds 2
Clear-Host

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Session Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "To render from command line:"
Write-Host "  .\scripts\render_animation.ps1 -Quality preview     # Fast preview"
Write-Host "  .\scripts\render_animation.ps1 -Quality production  # High quality"
Write-Host ""
Read-Host "Press Enter to exit"
