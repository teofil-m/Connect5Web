# 🎮 START HERE - Connect 5 3D Block Game

## Welcome! 👋

You have a **complete, production-ready Connect 5 3D block game** ready to play!

This is your starting point. Choose your path:

---

## 🚀 I Just Want to Play (5 minutes)

### Step 1: Open PowerShell
- Windows: Press `Win + R`, type `powershell`, press Enter
- Or: Open Windows Terminal

### Step 2: Navigate to Project
```powershell
cd d:\AI-training\Blocks
```

### Step 3: Setup (First Time Only)
```powershell
.\start.ps1 setup
```
Wait for it to complete (you'll see checkmarks ✓)

### Step 4: Start Game
```powershell
.\start.ps1 run-all
```

### Step 5: Play!
- Browser opens automatically to `http://localhost:4200`
- Player 1: Click "Create Game"
- Player 2: Click "Join" on available game
- Take turns, first to 5 in a row wins!

**Done! You're playing! 🎉**

---

## 📚 I Want to Understand Everything

Read the documentation in this order:

1. **[INDEX.md](INDEX.md)** ← All documentation explained
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** ← Complete overview
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** ← How it works technically
4. **[README.md](README.md)** ← Full API reference

---

## 🔧 I'm Having Setup Issues

1. Check: **[INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md)**
   - System requirements
   - Verification steps
   - Troubleshooting guide

2. Check: **[QUICKSTART.md](QUICKSTART.md)**
   - Step-by-step setup
   - Common issues & solutions
   - Multiple setup methods

---

## 💻 I Want to Play on Another Computer

1. Read: **[QUICKSTART.md - LAN Setup](QUICKSTART.md#accessing-game-from-another-computer-lan)**
2. Read: **[GETTING_STARTED.md - Network Access](GETTING_STARTED.md#playing-on-your-network-lan)**

Quick version:
1. Start backend on computer A
2. Find computer A's IP: Open PowerShell, type `ipconfig`
3. On computer B, edit `frontend/src/app/services/game.service.ts`
4. Change `localhost:5000` to the IP from step 2
5. Rebuild frontend and access

---

## 🎮 Game Rules (Quick Version)

- **Board**: 1×9×9 (1 wide, 9 deep, 9 tall)
- **Blocks**: 1×2 size (occupies 2 vertical spaces)
- **Place**: Click position buttons in the "Place Block" panel
- **Win**: Connect 5 blocks in any direction
- **Rule**: Only connect via 1×2 faces, not 1×1 faces
- **Turns**: Players alternate automatically

---

## 📂 What You Have

```
Blocks/
├── Backend (Python Flask)
│   ├── game_board.py ← Game logic
│   ├── game_server.py ← REST API & WebSocket
│   └── requirements.txt
├── Frontend (Angular + Three.js)
│   ├── components/ ← UI & 3D board
│   ├── services/ ← API communication
│   └── styles.css
├── Documentation (7 guides)
│   ├── INDEX.md ← Start here for docs
│   ├── GETTING_STARTED.md
│   ├── QUICKSTART.md
│   ├── README.md
│   ├── INSTALLATION_CHECKLIST.md
│   ├── PROJECT_OVERVIEW.md
│   └── ARCHITECTURE.md
└── start.ps1 ← Launcher script
```

---

## 🎯 Four Ways to Start

### Method 1: Easiest (All at Once)
```powershell
.\start.ps1 run-all
```

### Method 2: Separate Terminals
```powershell
# Terminal 1
.\start.ps1 run-backend

# Terminal 2 (new PowerShell window)
.\start.ps1 run-frontend
```

### Method 3: Using Batch Files
```powershell
# Terminal 1
backend\run_backend.bat

# Terminal 2 (new PowerShell window)
frontend\run_frontend.bat
```

### Method 4: Manual
```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python game_server.py

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## ✅ Quick Verification

Run these commands to verify everything works:

```powershell
# Check Python
python --version

# Check Node.js
node --version

# Check npm
npm --version
```

All three should show version numbers.

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.8+ from python.org |
| "Node not found" | Install Node.js from nodejs.org |
| "Port already in use" | Close other apps or change port in code |
| "Can't see other player's moves" | Refresh browser, check backend is running |
| "Board not showing" | Press F12 to check browser console for errors |

For more help: **[QUICKSTART.md - Troubleshooting](QUICKSTART.md#troubleshooting)**

---

## 📊 What's Inside

### Backend (Python)
- REST API for game operations
- WebSocket for real-time updates
- Game board logic (1×9×9)
- Win condition detection
- Turn management

### Frontend (Angular)
- Game lobby (create/join)
- 3D board visualization (Three.js)
- Move interface (position buttons)
- Real-time status display
- API communication

---

## 🎮 Playing the Game

### Player 1 (Host)
1. Enter your name
2. Click "Create Game"
3. Wait for Player 2 to join
4. Game starts automatically

### Player 2 (Guest)
1. Enter your name
2. Click "Join" on Player 1's game
3. Game starts automatically when both players join

### During Play
- **You can move** when it says "YOUR TURN"
- **Click a position** like "L2 H3" (Line 2, Height 3)
- **Block occupies** 2 height levels (H and H+1)
- **Take turns** until someone gets 5 in a row
- **Winner announced** when 5+ blocks are connected

---

## 🌟 Cool Features

✅ **3D Real-Time Board** - See blocks in 3D as they're placed
✅ **Turn-Based** - Players take turns, no time pressure
✅ **Network Play** - Play with anyone on your LAN
✅ **Auto-Sync** - All moves update instantly
✅ **Move Validation** - Impossible moves blocked automatically
✅ **Win Detection** - Automatic winner detection
✅ **Responsive UI** - Works on any screen size

---

## 📖 Documentation Map

| Need | Read |
|------|------|
| Quick overview | [GETTING_STARTED.md](GETTING_STARTED.md) |
| Setup instructions | [QUICKSTART.md](QUICKSTART.md) |
| Game rules | [README.md](README.md) |
| Pre-launch check | [INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md) |
| Code structure | [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) |
| Technical details | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Navigation guide | [INDEX.md](INDEX.md) |

---

## 🚀 Next Steps

### Option A: I'm Ready Now
```powershell
.\start.ps1 setup
.\start.ps1 run-all
```
Then open `http://localhost:4200`

### Option B: I Want More Info First
1. Read [GETTING_STARTED.md](GETTING_STARTED.md)
2. Then run the commands above

### Option C: I'm Setting Up on Another Computer
1. Read [QUICKSTART.md - LAN Setup](QUICKSTART.md#accessing-game-from-another-computer-lan)
2. Follow the network configuration steps
3. Then run the commands above

---

## ⚡ TL;DR

```powershell
cd d:\AI-training\Blocks
.\start.ps1 setup          # First time only
.\start.ps1 run-all        # Start both servers
# Opens http://localhost:4200
# Player 1: Create game
# Player 2: Join game
# Play and win! 🎉
```

---

## 💡 Pro Tips

1. **Fullscreen** - Play in fullscreen for best 3D rendering
2. **Chrome/Edge** - Recommended for best performance
3. **LAN Play** - Works great on local network
4. **Multiple Games** - Run multiple backends on different ports for multiple games
5. **Browser DevTools** - Press F12 if something seems wrong

---

## 🎓 Learn More

Once you're playing and want to customize:

1. **Add Features**: [PROJECT_OVERVIEW.md - How to Extend](PROJECT_OVERVIEW.md#customization-examples)
2. **Understand Code**: [ARCHITECTURE.md - System Architecture](ARCHITECTURE.md#system-architecture)
3. **Deploy**: [README.md - Deployment](README.md#deployment)
4. **Optimize**: [ARCHITECTURE.md - Performance](ARCHITECTURE.md#performance-characteristics)

---

## 🎉 You're Ready!

Everything is set up and ready to go. Choose your path above and get playing!

**Questions?** Check the documentation files listed above.

**Stuck?** See [QUICKSTART.md - Troubleshooting](QUICKSTART.md#troubleshooting)

---

# 🚀 START PLAYING NOW

Pick one:
- **[Play Now (5 min)](#-i-just-want-to-play-5-minutes)** ← Click here to start
- **[Learn First](#-i-want-to-understand-everything)** ← Read documentation
- **[Setup Help](#-im-having-setup-issues)** ← Troubleshoot setup
- **[Network Setup](#-i-want-to-play-on-another-computer)** ← Play over LAN

---

**Enjoy your Connect 5 game! 🎮**

*Questions? See [INDEX.md](INDEX.md) for complete navigation.*
