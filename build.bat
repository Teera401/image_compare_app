@echo off
echo =========================================
echo  Starting PyInstaller Build Process
echo =========================================

python -m PyInstaller --noconsole --onefile --name "Images-Compare" main.py
::python -m PyInstaller --onefile --name "AbbottTesting" start.py

echo.
echo =========================================
echo  Build Finished! 
echo  Check your executable in the "dist" folder.
echo =========================================
pause