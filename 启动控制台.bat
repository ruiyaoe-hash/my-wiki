@echo off
chcp 65001 >nul
cd /d %~dp0

where agent-runtime >nul 2>nul
if %errorlevel%==0 goto use_cmd
where python >nul 2>nul
if %errorlevel%==0 goto use_py
where py >nul 2>nul
if %errorlevel%==0 goto use_pylauncher
goto no_runtime

:use_cmd
set CMD=agent-runtime
goto start

:use_py
set CMD=python agents\cli.py
goto start

:use_pylauncher
set CMD=py -3 agents\cli.py
goto start

:no_runtime
echo [错误] 没找到 agent-runtime 或 Python。
echo 请确认已安装 Python，并在本目录执行过 pip install -e . 后重试。
pause
exit /b 1

:start
echo ============================================================
echo   Agent Runtime 控制台启动中，浏览器会自动打开页面。
echo.
echo   【这个黑窗口要一直开着】
echo   它在，控制台就在；关了它，控制台网页就打不开了。
echo   不用控制台的时候，直接关掉这个窗口就行。
echo ============================================================
echo.
%CMD% console
echo.
echo 控制台已退出。如果一打开就退出，请把本窗口内容拍照发给维护者。
pause
