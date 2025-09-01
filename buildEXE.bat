@echo off
pyinstaller main.py --onefile --add-data "HIDDevice;HIDDevice" --name ApexMacro
pause
