@echo off
echo Starting Connect 5 Game - Frontend Development Server
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Install npm packages if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install
)

REM Start Angular development server
echo.
echo Starting Angular development server on http://localhost:4200
echo Press Ctrl+C to stop the server
echo.
call npm start

pause
