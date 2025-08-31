@echo off
setlocal enabledelayedexpansion

rem === 自動產生 commit message ===
for /f "tokens=2 delims==." %%I in ('"wmic os get localdatetime /value"') do set dt=%%I
set msg=post: update notes %dt:~0,4%-%dt:~4,2%-%dt:~6,2% %dt:~8,2%:%dt:~10,2%

echo =======================================
echo Commit Message: %msg%
echo =======================================

rem === 執行 Python 更新 index.md ===
if exist tools\update_index.py (
    python tools\update_index.py
)

rem === 執行 PowerShell 版本推送 ===
powershell -ExecutionPolicy Bypass -File tools\blog_push.ps1 -Message "%msg%"

endlocal
