@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist all_in_one_file.py (
    echo [ERROR] all_in_one_file.py not found. Put this file in the same folder as fridge_manager.py
    pause
    exit /b 1
)

set PY=python
where python >nul 2>nul
if errorlevel 1 set PY=py

echo.
echo === Step 1/2: Installing packages (customtkinter, pillow, pyinstaller) ===
%PY% -m pip install --upgrade customtkinter pillow pyinstaller
if errorlevel 1 goto :error

echo.
echo === Step 2/2: Building all_in_one_file.exe (this takes 1-3 minutes) ===
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name all_in_one_file --collect-all customtkinter fridge_manager.py
if errorlevel 1 goto :error

echo.
echo ================================================================
echo  DONE!  Your program is here:
echo  %~dp0dist\all_in_one_file.exe
echo ================================================================
pause
exit /b 0

:error
echo.
echo [ERROR] Build failed. Check that Python 3.10+ is installed and "Add Python to PATH" was ticked.
pause
exit /b 1
