# ============================================
# Carousel Generator - Auto Startup Script
# Installs deps, activates env, launches app
# ============================================

Write-Host "🚀 Starting Carousel Generator with all skills enabled..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
& D:\Generator\env\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Check if dependencies are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
if (-not (pip show flask 2>$null)) {
    Write-Host "⚙️  Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    playwright install chromium
} else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎨 Available skills:" -ForegroundColor Cyan
Write-Host "   - docs-audit-and-refresh" -ForegroundColor White
Write-Host "   - docs-update-from-diff" -ForegroundColor White
Write-Host "   - pr-review" -ForegroundColor White
Write-Host "   - qwen-code-claw" -ForegroundColor White
Write-Host "   - terminal-capture" -ForegroundColor White
Write-Host ""
Write-Host "🛠️  Available commands:" -ForegroundColor Cyan
Write-Host "   - qc/code-review" -ForegroundColor White
Write-Host "   - qc/commit" -ForegroundColor White
Write-Host "   - qc/create-issue" -ForegroundColor White
Write-Host "   - qc/create-pr" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Starting Flask app at http://localhost:5000" -ForegroundColor Green
Write-Host ""

# Start the Flask app
python app.py
