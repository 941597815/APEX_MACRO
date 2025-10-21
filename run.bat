@echo off
set "script_dir=%~dp0"
@REM echo %script_dir%
cd /d "%script_dir%"

setlocal enabledelayedexpansion
net session >nul 2>&1

if %errorlevel% == 0 (
    python ./main.py
    @REM echo as admin
    @REM pause
) else (
    echo not as admin
    pause
    exit /b
)
