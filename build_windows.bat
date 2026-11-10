@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (echo Run install_windows.bat first.& pause & exit /b 1)
.venv\Scripts\python.exe -m pip install pyinstaller
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onedir --name FieldSenseAI ^
 --add-data "fieldsense\schema.sql;fieldsense" ^
 --add-data "models;models" ^
 --collect-all PySide6 --collect-all paddleocr --collect-all paddle --collect-all fitz ^
 --collect-all reportlab --collect-all openpyxl --collect-all PIL main.py
if errorlevel 1 (echo Build failed. Review the PyInstaller output.& pause & exit /b 1)
echo Build created in dist\FieldSenseAI\
echo Copy the complete dist\FieldSenseAI folder to the target offline Windows computer.
pause
