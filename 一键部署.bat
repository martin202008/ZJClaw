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
    echo.
    goto :check_pip
)

echo [提示] 未检测到 Python，开始自动安装...
echo.

REM 下载Python安装包
echo 正在下载 Python 3.12 安装包...
echo.

set "PYTHON_URL=https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
set "PYTHON_EXE=%TEMP%\python-3.12.8-amd64.exe"

powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_EXE%'"

if not exist "%PYTHON_EXE%" (
    echo [错误] Python 下载失败！
    echo.
    echo 请检查网络连接，或手动下载 Python:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python 下载完成
echo.

REM 静默安装Python
echo 正在安装 Python（需要管理员权限）...
echo 安装过程可能需要1-3分钟，请耐心等待...
echo.

start /wait mshta.exe "javascript:var sh=new ActiveXObject('shell.application');sh.ShellExecute('%PYTHON_EXE%','/quiet InstallAllUsers=1 PrependPath=1','runas');close();"

timeout /t 30 /nobreak >nul

REM 刷新环境变量并验证
set PATH=C:\Python312;C:\Python312\Scripts;%PATH%

for /f "delims=" %%i in ('where python 2^>nul') do set PYTHON_PATH=%%i

if not defined PYTHON_PATH (
    echo.
    echo [错误] Python 安装失败！
    echo.
    echo 请手动安装 Python:
    echo 1. 下载: https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe
    echo 2. 运行安装包，勾选 "Add to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python 安装成功
del "%PYTHON_EXE%" 2>nul

:check_pip
echo.
echo 检查 pip...

pip --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [警告] pip 未检测到，尝试修复...
    python -m ensurepip --upgrade
)

echo.
echo ========================================
echo   安装项目依赖
echo ========================================
echo.

pip install -e .

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败！
    pause
    exit /b 1
)

echo.
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
