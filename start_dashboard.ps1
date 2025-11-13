# Quick Start Script for Agriculture Dashboard
# ============================================
# This script sets up and launches the dashboard

Write-Host "🌾 Agriculture Production Dashboard - Quick Start" -ForegroundColor Green
Write-Host "=" -ForegroundColor Green

# Check Python installation
Write-Host "`nChecking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`nInstalling required packages..." -ForegroundColor Cyan
Write-Host "(This may take a few minutes on first run)" -ForegroundColor Yellow

pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error installing packages. Please check your internet connection." -ForegroundColor Red
    exit 1
}

# Launch dashboard
Write-Host "`n" -NoNewline
Write-Host "🚀 Launching dashboard..." -ForegroundColor Cyan
Write-Host "`nThe dashboard will open at: " -NoNewline
Write-Host "http://127.0.0.1:8050" -ForegroundColor Yellow
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Gray

python dashboard.py
