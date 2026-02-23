@echo off

REM 
if not exist "C:\Users\walli\WALLISON-DEV\financial_flow\logs" (
    mkdir "C:\Users\walli\WALLISON-DEV\financial_flow\logs"
)

REM
for /f %%d in ('powershell -NoProfile -Command "(Get-Date).Day"') do set DAY=%%d
if NOT "%DAY%"=="1" (
  echo %DATE% %TIME% - Não é dia 1: %DAY% >> "C:\Users\walli\WALLISON-DEV\financial_flow\logs\renew_budgets.log"
  exit /b 0
)

REM
call C:\Users\walli\WALLISON-DEV\financial_flow\.venv\Scripts\activate.bat

REM 
cd /d C:\Users\walli\WALLISON-DEV\financial_flow

REM
python manage.py renew_budgets >> logs\renew_budgets.log 2>&1