@echo off

REM Start Redis server
start redis-server.exe

REM Start Celery worker
start cmd /k "celery -A coinmarketcap_project worker --pool=solo --loglevel=info"

REM Wait for Celery worker to close
:waitloop
tasklist /FI "WINDOWTITLE eq Celery Worker" | find ":" >nul
if errorlevel 1 goto end
timeout /t 5 /nobreak >nul
goto waitloop

:end
REM Stop Redis server
taskkill /F /IM redis-server.exe
