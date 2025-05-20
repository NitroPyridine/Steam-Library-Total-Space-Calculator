@echo off
chcp 65001 >nul
title Steam Library Total Space Calculator

python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Install Python and add it to the PATH.
    pause
    exit /b
)

echo Installing required libraries...
python -m ensurepip --upgrade >nul 2>&1
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt

echo Running the program...
python main.py

echo.
echo Program execution completed. Press any key to exit...
pause >nul
