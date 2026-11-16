@echo off
setlocal
set "WEB_TEST_PYTHON=%ProgramFiles%\Unity\Hub\Editor\6000.6.8f1\Editor\Data\PlaybackEngines\WebGLSupport\BuildTools\Emscripten\python\python.exe"
if not exist "%WEB_TEST_PYTHON%" set "WEB_TEST_PYTHON=python.exe"
"%WEB_TEST_PYTHON%" "%~dp0Serve Game.py" --open
if errorlevel 1 pause
