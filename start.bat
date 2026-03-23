@echo off
chcp 65001 >nul
echo ========================================
echo   ZJClaw 启动脚本
echo ========================================
echo.
echo 正在启动服务...
echo.

cd /d "%~dp0webui"
python standalone_app.py

echo.
echo 服务已停止
pause
