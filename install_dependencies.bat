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

pip install -e .

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   依赖安装完成！
echo ========================================
echo.
echo 下一步：双击 start.bat 启动服务
echo.
pause
