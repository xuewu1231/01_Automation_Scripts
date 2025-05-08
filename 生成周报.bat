@echo off
chcp 65001 > nul
title 智能周报生成系统 V1.3

:check_python
python --version > nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python环境！
    echo 请安装Python并确保已将Python添加到系统环境变量中。
    echo.
    pause
    exit
)

:check_requirements
if not exist requirements.txt (
    echo [错误] 未找到requirements.txt文件！
    echo 请确保文件存在并包含所需的依赖包。
    echo.
    pause
    exit
)

:menu
cls
echo ============================================
echo             智能周报生成系统
echo ============================================
echo.
echo   [1] 生成新周报
echo   [2] 导出PDF版本
echo   [3] 生成统计分析
echo   [4] 查看使用说明
echo   [5] 检查环境依赖
echo   [6] 退出程序
echo.
echo ============================================
echo.

set /p choice=请选择功能（输入数字）：

if "%choice%"=="1" goto generate
if "%choice%"=="2" goto export_pdf
if "%choice%"=="3" goto analyze
if "%choice%"=="4" goto help
if "%choice%"=="5" goto check_deps
if "%choice%"=="6" goto end

echo.
echo [错误] 无效的选择，请重试...
timeout /t 2 >nul
goto menu

:generate
cls
echo ============================================
echo              生成新周报
echo ============================================
echo.
python weekly_report_generator.py
echo.
echo ============================================
pause
goto menu

:export_pdf
cls
echo ============================================
echo              导出PDF版本
echo ============================================
echo.
python weekly_report_generator.py --pdf
echo.
echo ============================================
pause
goto menu

:analyze
cls
echo ============================================
echo              生成统计分析
echo ============================================
echo.
python report_analyzer.py
echo.
echo ============================================
pause
goto menu

:check_deps
cls
echo ============================================
echo              检查环境依赖
echo ============================================
echo.
echo 正在检查并安装必要的依赖包...
echo.
pip install -r requirements.txt
echo.
echo ============================================
pause
goto menu

:help
cls
echo ============================================
echo              使用说明
echo ============================================
echo.
echo  功能说明：
echo  [1] 生成新周报：创建新的周报文件
echo  [2] 导出PDF：将周报转换为PDF格式
echo  [3] 统计分析：生成数据分析报告
echo  [4] 使用说明：显示本帮助信息
echo  [5] 检查环境：安装必要的依赖包
echo.
echo  文件说明：
echo  - 所有周报保存在 reports 目录
echo  - 分析报告保存在 statistics 目录
echo  - PDF文件与原文件保存在同一目录
echo.
echo  注意事项：
echo  - 首次使用请先运行[5]检查环境
echo  - 生成PDF需要安装相关依赖
echo  - 统计分析需要已有周报文件
echo.
echo ============================================
pause
goto menu

:end
cls
echo ============================================
echo              感谢使用
echo ============================================
echo.
echo    欢迎下次继续使用智能周报生成系统！
echo.
echo ============================================
timeout /t 3 >nul 