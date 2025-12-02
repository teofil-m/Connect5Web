# Connect 5 - Startup Script
# This script helps set up and run the Connect 5 game

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("setup", "run-backend", "run-frontend", "run-all", "help")]
    [string]$Command = "help"
)

function Show-Banner {
    Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║   Connect 5 - 3D Block Game              ║" -ForegroundColor Cyan
    Write-Host "║   Turn-based Strategy Game                ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Show-Banner
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  .\start.ps1 setup          - Set up dependencies (Python & Node.js)" -ForegroundColor Green
    Write-Host "  .\start.ps1 run-backend    - Start the Flask backend server" -ForegroundColor Green
    Write-Host "  .\start.ps1 run-frontend   - Start the Angular frontend server" -ForegroundColor Green
    Write-Host "  .\start.ps1 run-all        - Start both backend and frontend" -ForegroundColor Green
    Write-Host "  .\start.ps1 help           - Show this help message" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Yellow
    Write-Host "  1. Run: .\start.ps1 setup" -ForegroundColor Cyan
    Write-Host "  2. Run: .\start.ps1 run-all (or run-backend and run-frontend separately)" -ForegroundColor Cyan
    Write-Host "  3. Open browser to http://localhost:4200" -ForegroundColor Cyan
    Write-Host ""
}

function Check-Python {
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "✗ Python not found. Install from https://www.python.org/" -ForegroundColor Red
        return $false
    }
}

function Check-Node {
    try {
        $nodeVersion = node --version
        Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "✗ Node.js not found. Install from https://nodejs.org/" -ForegroundColor Red
        return $false
    }
}

function Setup-Backend {
    Write-Host "Setting up backend..." -ForegroundColor Yellow
    Push-Location "backend"
    
    if (-not (Test-Path "venv")) {
        Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
        python -m venv venv
    }
    
    Write-Host "  Activating virtual environment..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
    
    Write-Host "  Installing dependencies..." -ForegroundColor Cyan
    pip install -q -r requirements.txt
    
    Pop-Location
    Write-Host "✓ Backend setup complete" -ForegroundColor Green
}

function Setup-Frontend {
    Write-Host "Setting up frontend..." -ForegroundColor Yellow
    Push-Location "frontend"
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "  Installing npm dependencies..." -ForegroundColor Cyan
        npm install -q
    }
    
    Pop-Location
    Write-Host "✓ Frontend setup complete" -ForegroundColor Green
}

function Run-Backend {
    Show-Banner
    Write-Host "Starting backend server..." -ForegroundColor Yellow
    Push-Location "backend"
    
    if (-not (Test-Path "venv")) {
        Write-Host "Virtual environment not found. Running setup first..." -ForegroundColor Yellow
        Pop-Location
        Setup-Backend
        Push-Location "backend"
    }
    
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
    
    Write-Host ""
    Write-Host "Backend server starting on http://0.0.0.0:5000" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Cyan
    Write-Host ""
    
    python game_server.py
    Pop-Location
}

function Run-Frontend {
    Show-Banner
    Write-Host "Starting frontend development server..." -ForegroundColor Yellow
    Push-Location "frontend"
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "Dependencies not found. Running setup first..." -ForegroundColor Yellow
        Pop-Location
        Setup-Frontend
        Push-Location "frontend"
    }
    
    Write-Host ""
    Write-Host "Frontend server starting on http://localhost:4200" -ForegroundColor Green
    Write-Host "Browser should open automatically" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Cyan
    Write-Host ""
    
    npm start
    Pop-Location
}

# Main execution
switch ($Command) {
    "help" {
        Show-Help
    }
    "setup" {
        Show-Banner
        if (Check-Python -and Check-Node) {
            Write-Host ""
            Setup-Backend
            Setup-Frontend
            Write-Host ""
            Write-Host "Setup complete! Run '.\start.ps1 run-all' to start the game" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "Please install missing dependencies and try again" -ForegroundColor Red
        }
    }
    "run-backend" {
        Run-Backend
    }
    "run-frontend" {
        Run-Frontend
    }
    "run-all" {
        Write-Host "Starting both backend and frontend servers..." -ForegroundColor Yellow
        Write-Host "Note: This will open two separate windows/processes" -ForegroundColor Cyan
        Write-Host ""
        
        # Start backend in a new PowerShell window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start.ps1 run-backend"
        
        Start-Sleep -Seconds 2
        
        # Start frontend in a new PowerShell window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\start.ps1 run-frontend"
        
        Write-Host "Both servers started in separate windows" -ForegroundColor Green
        Write-Host "Backend: http://localhost:5000" -ForegroundColor Green
        Write-Host "Frontend: http://localhost:4200" -ForegroundColor Green
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Run '.\start.ps1 help' for available commands" -ForegroundColor Yellow
    }
}
