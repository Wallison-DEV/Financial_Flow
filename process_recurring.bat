@echo off

REM
if not exist "C:\Users\walli\WALLISON-DEV\financial_flow\logs" (
    mkdir "C:\Users\walli\WALLISON-DEV\financial_flow\logs"
)

REM
call C:\Users\walli\WALLISON-DEV\financial_flow\.venv\Scripts\activate.bat

REM
cd /d C:\Users\walli\WALLISON-DEV\financial_flow

REM
python manage.py process_recurring >> logs\process_recurring.log 2>&1