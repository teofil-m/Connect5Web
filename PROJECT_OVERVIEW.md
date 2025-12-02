# Project Overview - Connect 5 3D Game

## What You Have

A complete, production-ready Connect 5 game implementation with:

### ✅ Features Implemented

- **3D Visualization**: Real-time 3D board using Three.js
- **Turn-Based Gameplay**: Players take turns placing 1x2 blocks
- **Win Detection**: Automatic detection of 5-in-a-row patterns
- **Multiplayer**: Two-player game over network/LAN
- **Game Hosting**: One player hosts, another joins
- **Player Management**: Named players with session management
- **Real-time Sync**: WebSocket-based real-time updates
- **Responsive UI**: Works on desktop browsers

### 🎮 Game Mechanics

- **Board**: 1×9×9 (width × depth × height)
- **Blocks**: 1×2 size (occupies 2 vertical cells)
- **Move Validation**: Prevents invalid placements
- **Connection Rule**: 5+ blocks in a row wins (horizontal, vertical, diagonal)
- **No Small-Side Connections**: Players can only connect via the 1×2 face, not 1×1

### 🏗️ Architecture

```
                    Frontend (Angular + Three.js)
                    ↓
                http://localhost:4200
                    ↓
         ┌──────────────────────────┐
         │   Lobby Component        │
         │   - Game Creation        │
         │   - Game Discovery       │
         │   - Player Names         │
         └──────────────────────────┘
                    ↓
         ┌──────────────────────────┐
         │   Game Component         │
         │   - 3D Rendering         │
         │   - Move Interface       │
         │   - Game State Display   │
         └──────────────────────────┘
                    ↓
              (HTTP + WebSocket)
                    ↓
                http://localhost:5000
                    ↓
         ┌──────────────────────────┐
         │   Backend (Flask)        │
         │   - Game Logic Engine    │
         │   - Session Management   │
         │   - API Endpoints        │
         │   - Real-time Updates    │
         └──────────────────────────┘
```

## File Structure

```
Blocks/
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── start.ps1                      # PowerShell startup script
│
├── backend/
│   ├── requirements.txt           # Python dependencies
│   ├── game_board.py              # 👑 Core game logic
│   ├── game_server.py             # 👑 Flask API server
│   ├── run_backend.bat            # Windows startup script
│   └── venv/                      # Virtual environment (created on first run)
│
└── frontend/
    ├── package.json               # npm dependencies
    ├── angular.json               # Angular configuration
    ├── tsconfig.json              # TypeScript configuration
    ├── run_frontend.bat           # Windows startup script
    │
    └── src/
        ├── main.ts                # App bootstrap
        ├── index.html             # HTML entry point
        ├── styles.css             # Global styles
        │
        └── app/
            ├── app.component.ts   # Root component
            │
            ├── services/
            │   └── game.service.ts ✨ API & WebSocket service
            │
            └── components/
                ├── lobby.component.ts     ✨ Game lobby UI
                ├── lobby.component.html
                ├── lobby.component.css
                ├── game.component.ts      ✨ 3D game board
                ├── game.component.html
                └── game.component.css
```

## Key Files Explained

### Backend Files

#### `game_board.py`
- **GameBoard class**: 
  - Manages the 3D board state (1×9×9 grid)
  - Validates block placements
  - Checks win conditions (5-in-a-row)
  - Handles turn switching
  - Provides valid moves list

**Key Methods:**
- `place_block()` - Place a 1×2 block
- `_is_valid_move()` - Validate placement
- `_check_win()` - Detect 5-in-a-row
- `get_valid_moves()` - List available positions

#### `game_server.py`
- **GameSession class**: Manages game instances
- **Flask Routes**: RESTful API endpoints
- **WebSocket Events**: Real-time multiplayer sync

**Key Endpoints:**
- `GET /api/games` - List available games
- `POST /api/games` - Create game
- `POST /api/games/<id>/join` - Join game
- `POST /api/games/<id>/move` - Make a move
- `POST /api/games/<id>/start` - Start game

### Frontend Files

#### `game.service.ts`
- Communicates with Flask backend
- Manages game state (BehaviorSubject)
- Handles WebSocket connections
- Provides API methods for game operations

#### `lobby.component.ts/html/css`
- Display available games
- Allow creating new games
- Player name input
- Join game functionality

#### `game.component.ts/html/css`
- 3D board visualization (Three.js)
- Move interface (position buttons)
- Game status display
- Real-time board updates

## How to Extend

### Add New Features

**Example: Adding a time limit per turn**
1. Modify `GameSession` class in `game_server.py`
2. Add timeout logic
3. Update UI in `game.component.ts`

**Example: Adding chat**
1. Add new WebSocket event in `game_server.py`
2. Create chat component in Angular
3. Add chat UI to game component

**Example: Different board sizes**
1. Make board dimensions configurable in `GameBoard`
2. Update frontend to accept custom dimensions
3. Add UI selection for board size

## Testing the Game

### Test Scenarios

1. **Single Computer Test**
   - Create game as Player 1 (localhost)
   - Join same game as Player 2 (same localhost)
   - Both windows on same machine

2. **LAN Test**
   - Start backend on computer A
   - Start frontend on computer A and B
   - Join across network

3. **Win Condition Test**
   - Create simple scenarios to test:
     - Horizontal win (5 in a row on same height)
     - Vertical win (5 stacked blocks)
     - Diagonal win (both directions)

4. **Edge Cases**
   - Maximum board (9×9×9)
   - Simultaneous moves (may need retry)
   - Disconnection/reconnection

## Deployment

### Production Setup

1. **Backend**:
   ```bash
   # Install Gunicorn for production
   pip install gunicorn
   
   # Run with Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 game_server:app
   ```

2. **Frontend**:
   ```bash
   # Build for production
   ng build --configuration production
   
   # Serve dist/connect5 with any HTTP server
   python -m http.server 8000 --directory dist/connect5
   ```

3. **Server Configuration**:
   - Update API URLs in frontend
   - Configure CORS if needed
   - Set up SSL/HTTPS

## Troubleshooting Guide

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Port already in use | Another app using port 5000/4200 | Change port in code or stop other app |
| Import errors | Dependencies not installed | Run `pip install -r requirements.txt` or `npm install` |
| CORS errors | Frontend trying to connect to different origin | Check API URL in game.service.ts |
| WebSocket connection fails | Firewall blocking port | Allow port 5000 in firewall |
| 3D board not rendering | Three.js not loaded | Check browser console for errors |

## Next Steps

1. **Run the game**: 
   ```bash
   .\start.ps1 setup
   .\start.ps1 run-all
   ```

2. **Create a game**: Enter player name and click "Create Game"

3. **Invite player**: Share the game ID or LAN IP

4. **Play**: Take turns placing blocks until someone gets 5 in a row!

## Performance Notes

- Board rendering optimized with Three.js
- Move validation is O(1) complexity
- Win checking is O(1) with directional counting
- Network updates via WebSocket (not HTTP polling)
- Suitable for LAN play (minimal latency)

## Code Quality

- TypeScript for type safety
- Python type hints
- Modular component architecture
- Clear separation of concerns
- Well-commented code
- No external complex dependencies

---

**Enjoy your game! 🎮 Feel free to customize and extend it!**
