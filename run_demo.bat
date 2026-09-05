@echo off
setlocal
cd /d "%~dp0"
if exist "%~dp0lib\cpu\FaceLivenessSDK.dll" goto ok
echo Run the API first after filling .\lib\cpu\
exit /b 1
:ok
set "DEMO_PORT=9004"
set "API_BASE=http://127.0.0.1:8084"
python demo.py
exit /b %ERRORLEVEL%
