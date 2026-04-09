# ============================================
# Qwen Code - Auto Launch with All Skills
# Loads all skills and commands automatically
# ============================================

Write-Host "🚀 Launching Qwen Code with all skills enabled..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
& D:\Generator\env\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Change to carousel_generator directory
Set-Location D:\Generator\carousel_generator

Write-Host "📚 Auto-loading skills:" -ForegroundColor Cyan
Write-Host "   ✓ docs-audit-and-refresh" -ForegroundColor Green
Write-Host "   ✓ docs-update-from-diff" -ForegroundColor Green
Write-Host "   ✓ pr-review" -ForegroundColor Green
Write-Host "   ✓ qwen-code-claw" -ForegroundColor Green
Write-Host "   ✓ terminal-capture" -ForegroundColor Green
Write-Host ""
Write-Host "🛠️  Auto-loading commands:" -ForegroundColor Cyan
Write-Host "   ✓ qc/code-review" -ForegroundColor Green
Write-Host "   ✓ qc/commit" -ForegroundColor Green
Write-Host "   ✓ qc/create-issue" -ForegroundColor Green
Write-Host "   ✓ qc/create-pr" -ForegroundColor Green
Write-Host ""

# Launch Qwen Code with the project context
qwen
