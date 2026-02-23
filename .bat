@echo off
REM
for /f %%d in ('powershell -NoProfile -Command "(Get-Date).Day"') do set DAY=%%d
if NOT "%DAY%"=="1" (
  echo %DATE% %TIME% - Não é dia 1: %DAY% >> "%~dp0logs\renew_budgets.log"
  exit /b 0
)

REM
call C:\Users\walli\WALLISON-DEV\financial_flow\.venv\Scripts\activate.bat

cd /d C:\Users\walli\WALLISON-DEV\financial_flow
python manage.py renew_budgets >> C:\Users\walli\WALLISON-DEV\financial_flow\logs\renew_budgets.log 2>&1