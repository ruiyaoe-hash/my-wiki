@echo off
chcp 65001 >nul
cd /d %~dp0
where agent-runtime >nul 2>nul
if %errorlevel%==0 (set CMD=agent-runtime) else (set CMD=python agents\cli.py)
echo ============================================================
echo   Agent Runtime 控制台启动中，浏览器会自动打开页面。
echo.
echo   【这个黑窗口要一直开着】
echo   它在，控制台就在；你把它关了，控制台网页就打不开了。
echo   不用控制台的时候，直接关掉这个窗口就行。
echo ============================================================
echo.
%CMD% console
pause
