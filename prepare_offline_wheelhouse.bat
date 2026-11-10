@echo off
setlocal
cd /d "%~dp0"
if not exist wheelhouse mkdir wheelhouse
py -3 -m pip download --only-binary=:all: -r requirements.txt -d wheelhouse
if errorlevel 1 (echo Wheel download failed. Check Python version and Windows architecture.& pause & exit /b 1)
echo Wheelhouse prepared. Copy the approved PaddleOCR model directories into models\paddleocr before making the offline bundle.
pause
