# 🚀 Quick Start - Both Servers Running

After fixing the npm error, follow these steps to run your game:

## Terminal 1: Backend Server

```powershell
cd d:\AI-training\Blocks\backend
python game_server.py
```

**Expected output:**
```
 * Serving Flask app 'game_server'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.0.2.168:5000
 * Press CTRL+C to quit
```

✅ Backend is ready when you see the "Running on" messages.

---

## Terminal 2: Frontend Server (NEW WINDOW)

**Important: Open a NEW PowerShell window!**

```powershell
cd d:\AI-training\Blocks\frontend
npm start
```

**Expected output:**
```
✔ Compiled successfully.

✔ Compiled successfully.
Angular Live Development Server is listening on localhost:4200
Open your browser on http://localhost:4200/
```

✅ Frontend is ready when you see the "listening on localhost:4200" message.

---

## Step 3: Open Browser

1. Open your web browser
2. Go to: **http://localhost:4200**
3. You should see the Connect 5 game lobby

---

## Playing the Game

### Player 1 (Host)
1. Enter your player name
2. Click "Create Game"
3. Wait for Player 2

### Player 2 (Guest)
1. Enter your player name
2. Click "Join" on Player 1's game
3. Game starts automatically!

### During Gameplay
- Take turns placing 1×2 blocks
- First to 5 in a row wins
- Click position buttons: "L# H#" (Line and Height)

---

## Troubleshooting

### Backend won't start
```powershell
cd d:\AI-training\Blocks\backend
pip install -r requirements.txt
python game_server.py
```

### Frontend won't start
```powershell
cd d:\AI-training\Blocks\frontend
npm install
npm start
```

### Can't access http://localhost:4200
- Make sure frontend terminal says "listening on localhost:4200"
- Try refreshing the page (Ctrl+F5)
- Check firewall isn't blocking port 4200

### Blank page or errors
- Press F12 to open DevTools
- Check Console tab for errors
- Make sure backend is running on port 5000

---

## Quick Command Reference

| Task | Command |
|------|---------|
| **Backend** | `cd backend` → `python game_server.py` |
| **Frontend** | `cd frontend` → `npm start` |
| **Install backend deps** | `cd backend` → `pip install -r requirements.txt` |
| **Install frontend deps** | `cd frontend` → `npm install` |
| **Clear frontend cache** | `cd frontend` → `rm -r node_modules -Force` → `npm install` |
| **Clear npm cache** | `npm cache clean --force` |

---

## Game Board

- **Size:** 1×9×9 (1 wide, 9 deep, 9 tall)
- **Blocks:** 1×2 (occupies 2 vertical spaces)
- **Win:** 5 blocks in a row (horizontal, vertical, or diagonal)
- **Rule:** Can't connect on 1×1 faces, only on 1×2 faces

---

## Files

```
d:\AI-training\Blocks\
├── backend/
│   ├── game_board.py ← Game logic
│   ├── game_server.py ← API server (runs on port 5000)
│   └── run_backend.bat ← Easy launcher
│
└── frontend/
    ├── src/app/components/ ← Game UI
    ├── package.json ← Dependencies (FIXED ✓)
    └── run_frontend.bat ← Easy launcher
```

---

## Using Helper Scripts (Easier)

Instead of typing commands, you can use the batch files:

**Terminal 1:**
```bash
backend\run_backend.bat
```

**Terminal 2:**
```bash
frontend\run_frontend.bat
```

Or use PowerShell:
```powershell
.\start.ps1 run-backend
.\start.ps1 run-frontend
```

---

**Both servers running? Visit http://localhost:4200 and play! 🎮**
