@echo off
chcp 65001 >nul
echo ========================================
echo   ZJClaw 一键部署脚本
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，正在打开下载页面...
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 已安装

echo.
echo [2/4] 检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] pip 未安装
    pause
    exit /b 1
)
echo [OK] pip 已安装

echo.
echo [3/4] 安装项目依赖...
pip install -e . --quiet
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo [OK] 依赖安装完成

echo.
echo [4/4] 启动 WebUI...
echo.
echo ========================================
echo   服务启动中...
echo   请打开浏览器访问 http://localhost:5000
echo ========================================
echo.
cd /d "%~dp0webui"
python standalone_app.py
