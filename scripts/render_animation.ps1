# PowerShell render script for Alter logo animation
# Usage: .\render_animation.ps1 [-Quality preview|production]

param(
    [ValidateSet('preview', 'production')]
    [string]$Quality = 'production'
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
$blendFile = Join-Path $projectRoot "alter_logo_animation.blend"
$outputDir = Join-Path $projectRoot "output"

Write-Host "================================" -ForegroundColor Green
Write-Host "Alter Logo Animation Renderer" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Find Blender
$blenderExe = $null

# First, try to find in PATH
$blenderExe = (Get-Command blender -ErrorAction SilentlyContinue).Source

if (-not $blenderExe) {
    # Search in Blender Foundation folder for any version
    $blenderBase = "C:\Program Files\Blender Foundation"
    if (Test-Path $blenderBase) {
        $folders = Get-ChildItem -Path $blenderBase -Directory -Filter "Blender*"
        foreach ($folder in $folders) {
            $testPath = Join-Path $folder.FullName "blender.exe"
            if (Test-Path $testPath) {
                $blenderExe = $testPath
                break
            }
        }
    }
}

if (-not $blenderExe) {
    # Fallback to specific version paths (newest first)
    $blenderPaths = @(
        "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 3.5\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 3.4\blender.exe",
        "C:\Program Files\Blender Foundation\Blender 3.3\blender.exe",
        "C:\Program Files\Blender Foundation\Blender\blender.exe"
    )

    foreach ($path in $blenderPaths) {
        if (Test-Path $path) {
            $blenderExe = $path
            break
        }
    }
}

if (-not $blenderExe) {
    Write-Host "ERROR: Blender is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Blender 3.0 or higher"
    Write-Host "Download: https://www.blender.org/download/"
    exit 1
}

# Check if blend file exists
if (-not (Test-Path $blendFile)) {
    Write-Host "Blend file not found. Generating..." -ForegroundColor Yellow
    Write-Host ""
    & "$scriptDir\setup_scene.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Scene generation failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Create output directory
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Set render settings based on quality
if ($Quality -eq 'preview') {
    Write-Host "Rendering in PREVIEW mode (faster, lower quality)" -ForegroundColor Yellow
    $samples = 64
    $resolution = 50
} else {
    Write-Host "Rendering in PRODUCTION mode (slower, high quality)" -ForegroundColor Green
    $samples = 256
    $resolution = 100
}

Write-Host ""
Write-Host "Settings:"
Write-Host "  Samples: $samples"
Write-Host "  Resolution: $resolution%"
Write-Host "  Output: $outputDir"
Write-Host ""

# Render animation
Write-Host "Starting render..." -ForegroundColor Green
Write-Host ""

$pythonExpr = "import bpy; bpy.context.scene.cycles.samples = $samples; bpy.context.scene.render.resolution_percentage = $resolution"

& $blenderExe --background $blendFile --python-expr $pythonExpr --render-anim

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Render failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Render Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Output files: $outputDir"
Write-Host ""
