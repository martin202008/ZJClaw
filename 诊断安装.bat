@echo off
chcp 65001 >nul
echo ========================================
echo   ZJClaw 诊断安装脚本
echo ========================================
echo.

echo [1/5] 检查 Python...
python --version
if errorlevel 1 (
    echo [错误] Python 未安装！
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python 已安装
echo.

echo [2/5] 检查 pip...
pip --version
if errorlevel 1 (
    echo [错误] pip 未安装！
    pause
    exit /b 1
)
echo [OK] pip 正常
echo.

echo [3/5] 检查项目目录...
if not exist "pyproject.toml" (
    echo [错误] 请将本脚本放在 ZJClaw 项目根目录运行！
    echo 当前目录: %CD%
    pause
    exit /b 1
)
echo [OK] 项目目录正确
echo.

echo [4/5] 安装依赖...
echo 正在安装 zjclaw 包...
echo.
pip install -e . --verbose
echo.

if errorlevel 1 (
    echo.
    echo [错误] 安装失败！
    pause
    exit /b 1
)
echo.

echo [5/5] 验证安装...
pip show zjclaw-ai
if errorlevel 1 (
    echo.
    echo [错误] zjclaw 未安装成功！
    echo 请手动运行以下命令查看错误信息：
    echo pip install -e .
    pause
    exit /b 1
)
echo.

echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以运行 start.bat 启动服务
echo.
pause
