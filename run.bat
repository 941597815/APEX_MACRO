@echo off
<<<<<<< HEAD
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
=======
pushd "%~dp0"
python ./main.py  || PAUSE
>>>>>>> 881d98d45ece1f91843bcf15f889cd3430b0eff7
