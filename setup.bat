@echo off
title MCP Docs Reader - Full Setup

echo [1/4] Checking if uv is installed...
pip show uv >nul 2>&1
if %errorlevel% neq 0 (
    echo uv is not installed. Installing now...
    pip install uv
) else (
    echo uv is already installed.
)

echo.
echo [2/4] Creating virtual environment...
uv venv

echo.
echo [3/4] Activating virtual environment...
call .venv\Scripts\activate

echo.
echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo [✔] Setup complete!
pause