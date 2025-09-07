@echo off
setlocal enabledelayedexpansion

rem ==== 固定 Python 路徑 ====
set "PYEXE=C:\Users\User\anaconda3\python.exe"

rem ==== 解析使用者自訂訊息（可選）====
set "userMsg=%*"

rem ==== 產生預設訊息（若未提供）====
for /f "tokens=2 delims==." %%I in ('"wmic os get localdatetime /value"') do set dt=%%I
set "autoMsg=post: update notes %dt:~0,4%-%dt:~4,2%-%dt:~6,2% %dt:~8,2%:%dt:~10,2%"

if "%userMsg%"=="" (
  set "msg=%autoMsg%"
) else (
  set "msg=%userMsg%"
)

echo =======================================
echo Commit Message: %msg%
echo =======================================

rem ==== 檢查是否在 repo 根目錄 ====
if not exist ".git" (
  echo [ERROR] 請在 Git repo 根目錄執行本腳本（同層需有 .git 資料夾）。
  exit /b 1
)

rem ==== 自動修正 remote URL（若仍指向舊的 Verilog-Learning）====
for /f "usebackq tokens=*" %%R in (`git remote get-url origin 2^>nul`) do set "REMOTE_URL=%%R"
if not "%REMOTE_URL%"=="" (
  echo Current remote: %REMOTE_URL%
  echo %REMOTE_URL% | find /I "Verilog-Learning.git" >nul
  if not errorlevel 1 (
    echo Detected old remote. Updating to ... Blog.git
    git remote set-url origin https://github.com/Brandon-git-hub/Blog.git
    git remote -v
  )
)

rem ==== 執行 Python 更新 index.md（僅此處執行一次）====
@REM if exist "tools\update_index.py" (
@REM   "%PYEXE%" "tools\update_index.py"
@REM ) else (
@REM   echo [WARN] 找不到 tools\update_index.py，略過首頁更新。
@REM )

@REM pause

rem ==== 呼叫 PowerShell 版推送（由 ps1 來判斷是否要 commit/push）====
if exist "tools\blog_push.ps1" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "tools\blog_push.ps1" -Message "%msg%"
) else (
  echo [ERROR] 找不到 tools\blog_push.ps1
  exit /b 2
)

rem open my github
start "" "https://github.com/Brandon-git-hub/Blog"

endlocal
