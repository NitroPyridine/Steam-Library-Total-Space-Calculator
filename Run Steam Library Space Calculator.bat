@echo off
chcp 65001 >nul
title Steam Library Space Calculator

python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден. Установите Python и добавьте его в PATH.
    pause
    exit /b
)

echo Установка зависимостей...
python -m ensurepip --upgrade >nul 2>&1
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt

echo Запуск программы...
python main.py

echo.
echo Работа завершена. Нажмите любую клавишу для выхода...
pause >nul
