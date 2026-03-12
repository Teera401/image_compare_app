@echo off
echo =========================================
echo  Starting PyInstaller Build Process
echo =========================================

::python -m PyInstaller --noconsole --onefile --name "AbbottTesting" start.py
python -m PyInstaller --onefile --name "Images-Compare" main.py

echo.
echo =========================================
echo  Build Finished! 
echo  Check your executable in the "dist" folder.
echo =========================================
pause