@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo FieldSense virtual environment not found.
  echo Run install_windows.bat first, or use the offline installation instructions in README.md.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m fieldsense.app
if errorlevel 1 pause
