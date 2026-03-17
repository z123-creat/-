@echo off
chcp 65001 >nul
echo.
echo ============================================================================
echo                  Coze API 代理服务器 - 一键启动
echo ============================================================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未检测到 Python 环境
    echo.
    echo 请先安装 Python: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ 检测到 Python 环境
python --version
echo.

:: 检查并安装依赖
echo 📦 检查依赖...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 Flask...
    pip install flask
)
pip show flask-cors >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 Flask-CORS...
    pip install flask-cors
)
pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 Requests...
    pip install requests
)

echo.
echo ✅ 依赖检查完成
echo.
echo ============================================================================
echo 🚀 启动代理服务器...
echo ============================================================================
echo.
echo 代理服务器信息:
echo   - 地址: http://localhost:5000
echo   - 转发到: https://gsn2v3kydv.coze.site
echo.
echo 使用方法:
echo   1. 在浏览器中打开 chat_final.html
echo   2. 将 API 地址改为: http://localhost:5000
echo   3. 输入 API Token
echo   4. 测试连接
echo.
echo 按 Ctrl+C 停止服务器
echo ============================================================================
echo.

:: 启动代理服务器
python "%~dp0proxy_server.py"

pause
