@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (echo Python 3.10-3.12 is required. Install Python first.& pause & exit /b 1)
py -3 -m venv .venv
if errorlevel 1 (echo Could not create virtual environment.& pause & exit /b 1)
if exist wheelhouse\ (
  .venv\Scripts\python.exe -m pip install --no-index --find-links=wheelhouse -r requirements.txt
) else (
  echo No offline wheelhouse found. This setup step needs internet to download packages.
  echo After installation, FieldSense core workflows operate offline.
  .venv\Scripts\python.exe -m pip install --upgrade pip
  .venv\Scripts\python.exe -m pip install -r requirements.txt
)
if errorlevel 1 (echo Installation failed. See messages above.& pause & exit /b 1)
echo Installation completed. Add local PaddleOCR models under models\paddleocr\det and models\paddleocr\rec.
pause
