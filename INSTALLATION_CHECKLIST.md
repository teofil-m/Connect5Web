# Installation Checklist

## ✅ Project Structure Complete

Your Connect 5 game is fully set up and ready to run!

### Backend Files (Python/Flask)
- ✅ `backend/game_board.py` - Game logic engine
- ✅ `backend/game_server.py` - Flask API server  
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/run_backend.bat` - Windows startup helper

### Frontend Files (Angular/Three.js)
- ✅ `frontend/src/app/services/game.service.ts` - API service
- ✅ `frontend/src/app/components/lobby.component.ts` - Game lobby
- ✅ `frontend/src/app/components/game.component.ts` - 3D game board
- ✅ `frontend/package.json` - npm dependencies
- ✅ `frontend/angular.json` - Angular config
- ✅ `frontend/tsconfig.json` - TypeScript config
- ✅ `frontend/run_frontend.bat` - Windows startup helper

### Configuration Files
- ✅ `README.md` - Full documentation
- ✅ `QUICKSTART.md` - Quick start guide
- ✅ `PROJECT_OVERVIEW.md` - Architecture overview
- ✅ `start.ps1` - PowerShell startup script
- ✅ `INSTALLATION_CHECKLIST.md` - This file!

---

## 📋 Pre-Launch Checklist

Before running the game, verify you have:

### System Requirements
- [ ] Windows, macOS, or Linux
- [ ] Python 3.8 or higher installed
- [ ] Node.js 14 or higher installed
- [ ] npm 6 or higher installed
- [ ] A modern web browser (Chrome, Firefox, Edge, Safari)
- [ ] At least 500MB free disk space

### Verify Installation

**On Windows PowerShell:**
```powershell
# Check Python
python --version

# Check Node.js
node --version

# Check npm
npm --version
```

If any of these show "command not found", install the missing tool.

---

## 🚀 Quick Start Steps

### 1. Initial Setup (Run Once)
```bash
# Using PowerShell (Windows)
.\start.ps1 setup

# Or manually:
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ../frontend
npm install
```

### 2. Start Backend
```bash
# Option A: Using PowerShell
.\start.ps1 run-backend

# Option B: Using batch file
backend\run_backend.bat

# Option C: Manual
cd backend
.\venv\Scripts\activate
python game_server.py
```

You should see: `Running on http://0.0.0.0:5000`

### 3. Start Frontend (in new terminal)
```bash
# Option A: Using PowerShell
.\start.ps1 run-frontend

# Option B: Using batch file
frontend\run_frontend.bat

# Option C: Manual
cd frontend
npm start
```

Browser should open to: `http://localhost:4200`

### 4. Play the Game
- Player 1: Click "Create Game"
- Player 2: Click "Join" on the available game
- Game starts automatically when both players join
- Take turns placing blocks and connect 5 to win!

---

## 🌐 Network/LAN Setup

To play across different computers:

### Server Machine
1. Start backend: `.\start.ps1 run-backend`
2. Note your IP address: Run `ipconfig` in PowerShell
3. Look for "IPv4 Address" (e.g., 192.168.1.100)

### Client Machine
1. Edit `frontend/src/app/services/game.service.ts`
2. Change `localhost:5000` to your server's IP
3. Rebuild frontend: `npm run build`
4. Access via `http://<server-ip>:4200`

---

## 🔍 Verification Steps

### Test Backend
```bash
# Should return {"status": "healthy"}
curl http://localhost:5000/api/health
```

### Test Frontend
- Navigate to `http://localhost:4200`
- Should see Connect 5 game lobby
- Should see "No games available" message

### Test Two-Player
1. Player 1: Create game
2. Player 2: See game in list and join
3. Both should see game started with player names
4. Take a turn to verify sync

---

## 📊 Project Statistics

- **Backend**: ~300 lines of Python code
- **Frontend**: ~600 lines of TypeScript/HTML/CSS
- **Total**: ~1000 lines of code
- **Dependencies**: 7 Python packages, 8 npm packages
- **Build time**: ~1-2 minutes (first time)
- **Runtime**: Minimal resources needed

---

## 🎯 What Each Component Does

### Game Logic (`game_board.py`)
```
Manages the 3D board state
↓
Validates block placements
↓
Checks for 5-in-a-row win conditions
↓
Provides list of valid moves
```

### Backend Server (`game_server.py`)
```
Accepts HTTP requests from frontend
↓
Creates and manages game sessions
↓
Broadcasts updates via WebSocket
↓
Handles player turns and moves
```

### Game Service (`game.service.ts`)
```
Communicates with Python backend
↓
Manages game state in frontend
↓
Handles real-time WebSocket updates
↓
Provides methods for game operations
```

### UI Components
```
Lobby Component
↓
Shows available games
↓
Allows creating/joining games
↓
Routes to Game Component

Game Component
↓
Renders 3D board using Three.js
↓
Shows game status and turn info
↓
Provides move placement interface
↓
Updates in real-time via WebSocket
```

---

## ⚙️ Configuration Files

All configuration is pre-set and ready to use. To customize:

### Change Ports
- Backend port: Edit `game_server.py` line with `port=5000`
- Frontend port: Edit `angular.json` serve configuration

### Change Board Size
- Edit `GameBoard.__init__()` in `game_board.py`
- Update frontend visualization accordingly

### Change AI/Difficulty
- Extend `GameBoard` class with AI player
- Add AI opponent selection in lobby

---

## 🐛 If Something Goes Wrong

### Reset Everything
```bash
# Clean up
rm -r backend/venv
rm -r frontend/node_modules
rm -r frontend/dist

# Start over
.\start.ps1 setup
.\start.ps1 run-all
```

### Check Port Conflicts
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Find what's using port 4200
netstat -ano | findstr :4200
```

### Enable Debug Mode
- Add `debug=True` to Flask (`game_server.py`)
- Open browser DevTools (F12) for frontend errors
- Check server terminal for backend errors

---

## 📞 Support & Troubleshooting

**See the following files for more help:**
- `README.md` - Comprehensive documentation
- `QUICKSTART.md` - Detailed quick start
- `PROJECT_OVERVIEW.md` - Architecture & technical details

**Common Issues:**
- Dependencies not installed → Run setup again
- Ports already in use → Close other apps or change ports
- CORS errors → Check API URLs match
- WebSocket errors → Check firewall/network settings

---

## ✨ You're All Set!

Your Connect 5 3D game is ready to run. Choose your start method:

**Easiest (Windows):**
```powershell
.\start.ps1 run-all
```

**Manual:**
1. Open Terminal 1: `backend\run_backend.bat`
2. Open Terminal 2: `frontend\run_frontend.bat`
3. Browser opens to `http://localhost:4200`

**Enjoy your game! 🎮**

---

*Last Updated: November 2025*
*Connect 5 - 3D Block Game*
