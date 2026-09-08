@echo off
setlocal
cd /d "%~dp0"

if not exist "%~dp0lib\cpu\FaceLivenessSDK.dll" goto :need_lib
if not exist "%~dp0lib\cpu\fal-eng.dll" goto :need_lib
if not exist "%~dp0lib\cpu\fal.fpk" goto :need_lib
goto :ready

:need_lib
echo ERROR: .\lib\cpu\ is empty.
echo.
echo Download all files from Google Drive into .\lib\cpu\:
echo   https://drive.google.com/drive/folders/11xD987eHT00NUGiJZCNYSvwRadi0Nue5
echo.
echo Need:
echo   .\lib\cpu\FaceLivenessSDK.dll
echo   .\lib\cpu\fal-eng.dll
echo   .\lib\cpu\fal.fpk
echo.
exit /b 1

:ready

if not defined LICENSE set "LICENSE=%~dp0license.txt"
set "PATH=%~dp0lib\cpu;%PATH%"
if not defined PORT set "PORT=8084"
echo Starting Face Liveness API on port %PORT% ...
python app.py
exit /b %ERRORLEVEL%
