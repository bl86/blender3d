# PowerShell script to generate the Blender scene
# Creates alter_logo_animation.blend in the project root

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

Write-Host "================================" -ForegroundColor Green
Write-Host "Alter Logo Scene Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

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
    $blenderExe = (Get-Command blender -ErrorAction SilentlyContinue).Source
}

if (-not $blenderExe) {
    Write-Host "ERROR: Blender is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Blender 3.0 or higher"
    Write-Host "Download: https://www.blender.org/download/"
    exit 1
}

# Check if SVG exists
$svgPath = Join-Path $projectRoot "alter.svg"
if (-not (Test-Path $svgPath)) {
    Write-Host "ERROR: alter.svg not found in project root" -ForegroundColor Red
    exit 1
}

Write-Host "Generating Blender scene..." -ForegroundColor Yellow
Write-Host ""

# Run the Python script in Blender
Push-Location $projectRoot
$pythonScript = Join-Path $scriptDir "logo_animation.py"
& $blenderExe --background --python $pythonScript

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Scene generation failed!" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Scene Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Blend file created: alter_logo_animation.blend"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Open in Blender: blender alter_logo_animation.blend"
Write-Host "  2. Or render: .\scripts\render_animation.ps1"
Write-Host ""
