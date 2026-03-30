@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║           🛂 签证办理系统 - 快速启动                    ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo [1/3] 检查 Node.js 安装...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Node.js，请先安装 Node.js
    echo 下载地址：https://nodejs.org/zh-cn/download/
    pause
    exit /b 1
)
echo ✅ Node.js 已安装

echo.
echo [2/3] 安装后端依赖...
cd backend
if not exist node_modules (
    call npm install
) else (
    echo 依赖已安装，跳过
)

echo.
echo [3/3] 启动后端服务...
echo.
start http://localhost:3000/api
start ../frontend/index.html
start ../admin/index.html
call npm start

pause
