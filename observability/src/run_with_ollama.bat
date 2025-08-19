@echo off
setlocal

REM Add Ollama to PATH
set PATH=%PATH%;C:\Users\ksfma\AppData\Local\Programs\Ollama

REM Run the Python script
python test_run.py

pause