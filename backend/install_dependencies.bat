@echo off
echo Installing dependencies for Connect 5 Backend...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Install dependencies
echo Installing packages from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Trying manual installation...
    pip install Flask==2.3.3
    pip install Flask-CORS==4.0.0
    pip install Flask-SocketIO==5.3.4
    pip install python-socketio==5.9.0
    pip install python-engineio==4.7.1
)

echo.
echo Verifying installation...
python -c "from flask_socketio import SocketIO; print('✓ All dependencies installed successfully!')"

if errorlevel 1 (
    echo.
    echo ERROR: Dependencies not properly installed
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Setup complete! You can now run: python game_server.py
pause
