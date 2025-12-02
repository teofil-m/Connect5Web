# Quick Start Guide

## Prerequisites

Before running the game, ensure you have:

1. **Python 3.8+** - Download from https://www.python.org/
2. **Node.js & npm** - Download from https://nodejs.org/
3. A modern web browser (Chrome, Firefox, Edge, Safari)

## Quick Start (Windows)

### Option 1: Using Batch Files (Easiest)

1. **Start Backend Server**:
   - Navigate to `backend` folder
   - Double-click `run_backend.bat`
   - Wait until you see "Running on http://0.0.0.0:5000"

2. **Start Frontend (in a new terminal)**:
   - Navigate to `frontend` folder
   - Double-click `run_frontend.bat`
   - Browser should open to http://localhost:4200

3. **Play the Game**:
   - One player creates a game by entering their name and clicking "Create Game"
   - Second player enters their name and clicks "Join" on the available game
   - Game starts automatically when both players join

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python game_server.py
```

#### Frontend Setup (in a new terminal/PowerShell)
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```

## Accessing Game from Another Computer (LAN)

1. Find the server computer's IP address:
   - Windows: Open PowerShell and run `ipconfig`
   - Look for "IPv4 Address" (usually 192.168.x.x or 10.x.x.x)

2. Edit backend configuration (optional):
   - Backend is already set to `0.0.0.0` which accepts all connections

3. On client computer:
   - Edit `frontend/src/app/services/game.service.ts`
   - Change line with `'http://localhost:5000'` to `'http://<server-ip>:5000'`
   - Also change `'http://localhost:5000'` in socket initialization
   
4. Rebuild frontend:
   ```bash
   npm run build
   ```

5. Access from client:
   - Navigate to `http://<server-ip>:4200`

## Game Controls

### 3D Board
- The 3D board shows:
  - **Red blocks** = Player 1
  - **Teal blocks** = Player 2
  - **Grid** = Available positions

### Placing Blocks
- View "Place Block" section on the right panel
- Click any valid position button (L = Line, H = Height)
- Example: "L2 H3" means Line 2, Height 3

### Turn-Based Play
- Only the current player can place blocks
- "YOUR TURN" indicator shows when it's your turn
- Turn alternates after each move

## Troubleshooting

### Backend won't start
```
Error: "Flask is not installed"
Solution: Make sure you've run: pip install -r requirements.txt
```

### Frontend won't load
```
Error: "Angular CLI not found"
Solution: Make sure you've run: npm install
```

### Cannot see other player's moves
```
Possible issues:
1. Check backend is running on port 5000
2. Verify firewall allows port 5000
3. Check browser console (F12) for connection errors
4. Try refreshing the browser
```

### "Cannot connect to server" on another computer
```
1. Verify backend machine's IP: ipconfig
2. Update game.service.ts with correct IP
3. Check firewall - port 5000 and 4200 should be accessible
4. Rebuild frontend: npm run build
5. Restart both backend and frontend
```

### Board not showing correctly
```
1. Open browser DevTools (F12)
2. Check Console tab for JavaScript errors
3. Make sure Three.js loaded successfully
4. Try hard refresh (Ctrl+F5)
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Game not found" error | Ensure both players are using same network, check IP address |
| Game freezes after move | Refresh page, check backend is still running |
| Cannot join game | Game might be full (2 players max) or already started |
| Slow 3D rendering | Close other applications, check GPU drivers are up to date |

## File Descriptions

- `backend/game_board.py` - Game logic (board state, move validation, win checking)
- `backend/game_server.py` - Flask API server and WebSocket handling
- `frontend/src/app/services/game.service.ts` - API communication
- `frontend/src/app/components/lobby.component.ts` - Game list and joining UI
- `frontend/src/app/components/game.component.ts` - 3D board and gameplay

## Tips for Best Experience

1. **Resolution**: Play in fullscreen or maximized window for best 3D rendering
2. **Browser**: Chrome/Edge recommended for best performance
3. **Network**: LAN play works best with both computers on same Wi-Fi/network
4. **Latency**: If moves aren't syncing, wait 1-2 seconds for network update

Enjoy your game! 🎮
