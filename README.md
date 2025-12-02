# Connect 5 - 3D Block Game

A turn-based 3D Connect 5 game where players stack 1x2 blocks on a 1x9x9 board. Win by connecting 5 blocks horizontally, vertically, or diagonally. Play over LAN with a Flask backend and Angular frontend.

## Game Rules

- **Board**: 1x9x9 (1 unit wide, 9 units deep/lines, 9 units high)
- **Blocks**: 1x2 size (occupies 2 vertical units)
- **Max per line**: 9 blocks (fills the entire 1x9 depth)
- **Max height**: 9 units
- **Win condition**: 5 connected blocks in a row (horizontal, vertical, or diagonal)
- **Important**: Players CANNOT connect blocks on the 1x1 small side face

## Project Structure

```
Blocks/
├── backend/
│   ├── requirements.txt
│   ├── game_board.py       # Game logic
│   └── game_server.py      # Flask API server
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── services/
    │   │   │   └── game.service.ts
    │   │   └── components/
    │   │       ├── lobby.component.ts/html/css
    │   │       └── game.component.ts/html/css
    │   ├── main.ts
    │   ├── styles.css
    │   └── index.html
    ├── package.json
    ├── angular.json
    └── tsconfig.json
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate # On Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python game_server.py
   ```

   The server will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The application will open at `http://localhost:4200`

## How to Play

### Creating a Game

1. Enter your player name in the lobby
2. Click "Create Game"
3. Enter your host name and click "Create"
4. Share the game ID or IP address with another player

### Joining a Game

1. Enter your player name
2. See "Available Games" list
3. Click "Join" on the desired game
4. Wait for the game to start once 2 players are present

### During Gameplay

1. **3D Board**: The game board is displayed in 3D with:
   - Blocks colored by player (Red = Player 1, Teal = Player 2)
   - Grid showing available positions
   - Wireframe edges on blocks

2. **Making Moves**: 
   - The "Place Block" section shows valid moves
   - Click a position button (L# H#) where L = Line (0-8), H = Height (0-7)
   - Blocks automatically occupy 2 height levels (H and H+1)
   - Wait for the other player to take their turn

3. **Winning**:
   - Connect 5 blocks in a row (horizontally, vertically, or diagonally)
   - Blocks on the 1x1 face do NOT count as connected
   - Game ends and winner is declared

## API Endpoints

### REST Endpoints

- `GET /api/health` - Health check
- `GET /api/games` - List available games
- `POST /api/games` - Create a new game
- `GET /api/games/<id>` - Get game state
- `POST /api/games/<id>/join` - Join a game
- `POST /api/games/<id>/start` - Start a game
- `POST /api/games/<id>/move` - Make a move

### WebSocket Events

- `connect` - Client connects
- `join_game_room` - Join a game room
- `game_move` - Make a move (broadcasts `board_updated` to all players)
- `board_updated` - Receive board state updates

## Technical Details

### Backend (Python/Flask)

- **GameBoard class**: Manages 3D board state and win condition checking
- **GameSession class**: Manages game instances, players, and turn management
- **Flask routes**: RESTful API for game operations
- **Socket.IO**: Real-time updates for simultaneous gameplay

### Frontend (Angular + Three.js)

- **Lobby Component**: Game discovery and creation
- **Game Component**: 3D visualization and gameplay
- **Game Service**: API communication and game state management
- **Three.js**: 3D rendering of board and blocks

## LAN Network Access

To access the game from another computer on your local network:

1. Find your computer's IP address:
   - Windows: Run `ipconfig` and look for IPv4 Address
   - Linux/Mac: Run `ifconfig` or `hostname -I`

2. On the backend server machine, modify `game_server.py`:
   - Change `0.0.0.0` to allow external connections (already set)

3. On client machines, update the API URL in `game.service.ts`:
   - Change `localhost` to the server machine's IP address
   - Example: `http://192.168.1.100:5000/api`

4. Access from another computer:
   - Navigate to `http://<server-ip>:4200` in a browser

## Troubleshooting

### Cannot connect to backend
- Ensure Flask server is running on `localhost:5000`
- Check firewall settings allow port 5000 and 4200
- Verify backend dependencies are installed

### Board not rendering
- Check browser console for errors (F12)
- Ensure Three.js is properly installed (`npm list three`)
- Try refreshing the page

### Game state not syncing
- Ensure both players are connected to the same game session
- Check that WebSocket connections are established
- Look at network requests in browser DevTools

## Future Enhancements

- Persistent game replay/history
- AI opponent
- Spectator mode
- Game chat
- Elo rating system
- Different game modes (time attack, handicap)
- Mobile responsive UI improvements

## License

MIT License - Feel free to use and modify!
