@echo off
set "script_dir=%~dp0"
cd /d "%script_dir%"
start /wait cmd /c "pyarmor gen main.py Arduino.py linstion.py macro.py utils.py globals.py -e 30 --period 1 --assert-import --assert-call --enable-jit"

echo F | xcopy requirements.txt dist\requirements.txt /H /C /I /Y
echo F | xcopy README.md dist\README.md /H /C /I /Y
echo F | xcopy ApexScriptStart.bat dist\ApexScriptStart.bat /H /C /I /Y
xcopy imgs\* dist\imgs\ /E /H /C /I /Y
echo build is over
pause