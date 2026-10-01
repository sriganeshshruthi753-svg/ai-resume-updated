@echo off

echo ========================================
echo AI Resume Updated - Setup
echo ========================================

set "PATH=%LocalAppData%\Programs\Python\Python313;%LocalAppData%\Programs\Python\Python313\Scripts;%PATH%"

python -m venv venv

call venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

echo.
echo ========================================
echo Setup Completed Successfully
echo ========================================

pause