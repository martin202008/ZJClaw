@echo off
chcp 65001 >nul
echo ========================================
echo   ZJClaw 环境安装脚本
echo ========================================
echo.

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 已安装

echo.
echo [2/3] 检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] pip 未安装，请重新安装 Python 并勾选 pip
    pause
    exit /b 1
)
echo [OK] pip 已安装

echo.
echo [3/3] 安装项目依赖...
echo 这可能需要几分钟，请耐心等待...
echo.

pip install -e . --quiet

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 下一步：
echo   1. 运行 start.bat 启动服务
echo   2. 浏览器打开 http://localhost:5000
echo.
pause
