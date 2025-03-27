@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ===== 開始安裝程序 =====
echo.

:: 檢查Python是否已安裝
echo 正在檢查Python安裝狀態...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安裝，正在下載Python安裝程式...
    
    :: 下載Python安裝程式
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe', 'python_installer.exe')"
    
    if exist python_installer.exe (
        echo Python安裝程式下載完成
        echo 正在安裝Python...
        start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
        del python_installer.exe
        echo Python安裝完成
    ) else (
        echo 錯誤：Python安裝程式下載失敗
        goto :error
    )
) else (
    echo Python已安裝
)

:: 更新pip
echo 正在更新pip...
python -m pip install --upgrade pip

:: 安裝必要套件
echo 正在安裝必要套件...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 錯誤：套件安裝失敗
    goto :error
)

echo.
echo ===== 安裝完成 =====
echo 所有必要的程式和套件已安裝完成
echo 請按任意鍵關閉視窗
pause >nul
goto :eof

:error
echo.
echo ===== 安裝失敗 =====
echo 安裝過程中發生錯誤，請檢查錯誤訊息
echo 請按任意鍵關閉視窗
pause >nul
exit /b 1