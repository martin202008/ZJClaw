@echo off
chcp 65001 >nul
echo ========================================
echo   ZJClaw 依赖安装脚本
echo ========================================
echo.

echo 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [错误] 未检测到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python 已安装
echo.
echo 正在安装项目依赖...
echo.

REM 先尝试安装完整依赖
pip install -e .

if not errorlevel 1 goto :success

echo.
echo [提示] 完整依赖安装失败，尝试安装最小依赖...
echo.
pip install -r requirements_webui.txt

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

:success
echo.
echo ========================================
echo   依赖安装完成！
echo ========================================
echo.
echo 下一步：双击 start.bat 启动服务
echo.
pause
