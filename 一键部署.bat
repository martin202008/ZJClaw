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

echo 下载地址: %PYTHON_URL%
powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_EXE%'"

if not exist "%PYTHON_EXE%" (
    echo.
    echo [错误] Python 下载失败，请检查网络连接
    echo 或手动下载 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [OK] Python 下载完成
echo.

REM 静默安装Python
echo 正在安装 Python（自动添加到系统PATH）...
echo 这可能需要几分钟，请耐心等待...

start /wait "" "%PYTHON_EXE%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM 验证安装
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [错误] Python 安装失败
    echo 请手动安装 Python: https://www.python.org/downloads/
    del "%PYTHON_EXE%" 2>nul
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

pip install -e . --quiet

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
