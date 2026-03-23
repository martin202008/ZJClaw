@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo   ZJClaw 全自动部署脚本
echo ========================================
echo.

REM 检查是否已有Python
python --version >nul 2>&1
if not errorlevel 1 (
    echo [OK] Python 已安装
    goto :install_deps
)

echo [提示] 未检测到 Python，开始自动安装...
echo.

REM 下载Python安装包
echo 正在下载 Python 安装包，请稍候...
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
set "PYTHON_EXE=%TEMP%\python-3.12.8-amd64.exe"

powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_EXE%'"

if not exist "%PYTHON_EXE%" (
    echo.
    echo [错误] Python 下载失败
    echo 请手动下载 Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Python 下载完成
echo.

REM 静默安装Python
echo 正在安装 Python...
echo 请在弹出的安装向导中点击"Install Now"...
echo.

start /wait "" "%PYTHON_EXE%" /quiet InstallAllUsers=1 PrependPath=1

REM 刷新环境变量
set PATH=C:\Python312;C:\Python312\Scripts;%PATH%

REM 验证安装
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [错误] Python 安装可能失败，请手动确认
    echo.
    echo 手动安装步骤：
    echo 1. 打开: https://www.python.org/downloads/
    echo 2. 下载 Python 3.12
    echo 3. 运行安装包，勾选 "Add to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python 安装成功
del "%PYTHON_EXE%" 2>nul

:install_deps
echo.
echo ========================================
echo   安装项目依赖
echo ========================================
echo.

pip install -e . 

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [OK] 依赖安装完成
echo.

REM 启动服务
echo ========================================
echo   启动服务中...
echo ========================================
echo.
echo 请在浏览器打开: http://localhost:5000
echo.
echo 按 Ctrl+C 可停止服务
echo.

cd /d "%~dp0webui"
python standalone_app.py

pause
