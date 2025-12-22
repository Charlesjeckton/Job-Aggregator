@echo off
title Job Aggregator Runner
cd /d "%~dp0"

:: Check if PyCharm's virtual environment exists
if exist venv\Scripts\python.exe (
    echo 🐍 Using Virtual Environment...
    venv\Scripts\python.exe main.py
) else if exist .venv\Scripts\python.exe (
    echo 🐍 Using .venv Environment...
    .venv\Scripts\python.exe main.py
) else (
    echo 🐍 Using Global Python...
    python main.py
)

pause