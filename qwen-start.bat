@echo off
REM ============================================
REM  Qwen Code - Auto Launch with All Skills
REM  Loads all skills and commands automatically
REM ============================================

echo 🚀 Launching Qwen Code with all skills enabled...
echo.

REM Activate virtual environment
call D:\Generator\env\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Change to carousel_generator directory
cd /d D:\Generator\carousel_generator

echo 📚 Auto-loading skills:
echo    ✓ docs-audit-and-refresh
echo    ✓ docs-update-from-diff
echo    ✓ pr-review
echo    ✓ qwen-code-claw
echo    ✓ terminal-capture
echo.
echo 🛠️  Auto-loading commands:
echo    ✓ qc/code-review
echo    ✓ qc/commit
echo    ✓ qc/create-issue
echo    ✓ qc/create-pr
echo.

REM Launch Qwen Code with the project context
qwen
