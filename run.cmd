@echo off

echo ========================================
echo AI Resume Updated - Starting Server
echo ========================================

call venv\Scripts\activate

uvicorn app.main:app --reload

pause