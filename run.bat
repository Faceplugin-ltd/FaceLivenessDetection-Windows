@echo off
setlocal
cd /d "%~dp0"

if not exist "%~dp0lib\cpu\FaceLivenessSDK.dll" goto :need_lib
if not exist "%~dp0lib\cpu\facerec.dll" goto :need_lib
if not exist "%~dp0lib\cpu\fal.fpk" goto :need_lib
goto :ready

:need_lib
echo ERROR: .\lib\cpu\ is empty.
echo.
echo Download runtime.zip and extract it into .\lib\cpu\:
echo   https://github.com/Faceplugin-ltd/FaceLivenessDetection-Windows/releases/tag/latest
echo.
echo Need:
echo   .\lib\cpu\FaceLivenessSDK.dll
echo   .\lib\cpu\facerec.dll
echo   .\lib\cpu\fal.fpk
echo.
exit /b 1

:ready
if not defined LICENSE set "LICENSE=%~dp0license.txt"
if not defined PORT set "PORT=8093"
set "PATH=%~dp0lib\cpu;%PATH%"
rem OpenVINO / idliveface can AV once on a cold load; keep threads modest.
if not defined OMP_NUM_THREADS set "OMP_NUM_THREADS=1"
if not defined OV_CACHE_DIR set "OV_CACHE_DIR=%TEMP%\faceplugin-ov-cache"

echo Starting Face Liveness API on port %PORT% ...
set "ATTEMPT=0"
:run
set /a ATTEMPT+=1
python app.py
set "ERR=%ERRORLEVEL%"
if "%ERR%"=="0" exit /b 0
rem 0xC0000005 STATUS_ACCESS_VIOLATION — intermittent idliveface/OpenVINO DllMain crash
if not "%ERR%"=="-1073741819" if not "%ERR%"=="3221225477" exit /b %ERR%
if %ATTEMPT% geq 3 (
  echo Native SDK crashed on startup %ATTEMPT% times; giving up.
  exit /b %ERR%
)
echo Native SDK crashed during startup ^(access violation^); retrying %ATTEMPT%/3...
goto :run
