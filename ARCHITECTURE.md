# Architecture & Technical Deep Dive

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PLAYER 1 & 2 BROWSERS                    │
│                  (http://localhost:4200)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Angular Application (SPA)                     │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────┐       │  │
│  │  │        AppComponent (Router Outlet)         │       │  │
│  │  │                                             │       │  │
│  │  │  ┌──────────────────────────────────────┐  │       │  │
│  │  │  │   LobbyComponent                    │  │       │  │
│  │  │  │  - Game Creation                    │  │       │  │
│  │  │  │  - Game Discovery                   │  │       │  │
│  │  │  │  - Player Names                     │  │       │  │
│  │  │  └──────────────────────────────────────┘  │       │  │
│  │  │                 ↓ Routes                    │       │  │
│  │  │  ┌──────────────────────────────────────┐  │       │  │
│  │  │  │   GameComponent                     │  │       │  │
│  │  │  │  ┌───────────────────────────────┐  │  │       │  │
│  │  │  │  │  Three.js 3D Renderer        │  │  │       │  │
│  │  │  │  │  - Board Visualization       │  │  │       │  │
│  │  │  │  │  - Block Rendering           │  │  │       │  │
│  │  │  │  │  - Grid Display              │  │  │       │  │
│  │  │  │  └───────────────────────────────┘  │  │       │  │
│  │  │  │  ┌───────────────────────────────┐  │  │       │  │
│  │  │  │  │  Game Panel                  │  │  │       │  │
│  │  │  │  │  - Move Buttons              │  │  │       │  │
│  │  │  │  │  - Turn Indicator            │  │  │       │  │
│  │  │  │  │  - Game Status               │  │  │       │  │
│  │  │  │  └───────────────────────────────┘  │  │       │  │
│  │  │  └──────────────────────────────────────┘  │       │  │
│  │  │                                             │       │  │
│  │  └─────────────────────────────────────────────┘       │  │
│  │                                                         │  │
│  │  GameService (Injectable)                             │  │
│  │  ├─ HTTP Client (REST API calls)                       │  │
│  │  ├─ Socket.IO Client (Real-time updates)              │  │
│  │  └─ BehaviorSubject (State management)                │  │
│  │                                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP + WebSocket
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                   FLASK BACKEND SERVER                          │
│              (http://0.0.0.0:5000 or localhost:5000)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Flask Application                             │  │
│  │                                                         │  │
│  │  REST API Routes:                                      │  │
│  │  ├─ GET  /api/health              → Health check       │  │
│  │  ├─ GET  /api/games                → List games        │  │
│  │  ├─ POST /api/games                → Create game       │  │
│  │  ├─ GET  /api/games/<id>           → Get state         │  │
│  │  ├─ POST /api/games/<id>/join      → Join game         │  │
│  │  ├─ POST /api/games/<id>/start     → Start game        │  │
│  │  └─ POST /api/games/<id>/move      → Make move         │  │
│  │                                                         │  │
│  │  WebSocket Events:                                     │  │
│  │  ├─ connect                → Connection established    │  │
│  │  ├─ join_game_room         → Player joins room         │  │
│  │  ├─ game_move              → Player makes move         │  │
│  │  └─ board_updated          → Broadcast to all players  │  │
│  │                                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Game Session Management                         │  │
│  │                                                         │  │
│  │  games = {}  # Store active game sessions              │  │
│  │  ├─ game_id → GameSession                              │  │
│  │  │   ├─ host_name                                       │  │
│  │  │   ├─ players {name: id}                             │  │
│  │  │   ├─ board (GameBoard instance)                      │  │
│  │  │   ├─ current_player_name                            │  │
│  │  │   └─ started (bool)                                 │  │
│  │  │                                                     │  │
│  │  players = {}  # Track which game each player is in    │  │
│  │  └─ player_name → game_id                              │  │
│  │                                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Game Logic Engine (GameBoard)                   │  │
│  │                                                         │  │
│  │  board[line][height] = player_id                        │  │
│  │  ├─ line: 0-8 (position on 1×9 line)                    │  │
│  │  ├─ height: 0-8 (vertical position)                    │  │
│  │  └─ value: 1, 2, or None                               │  │
│  │                                                         │  │
│  │  Methods:                                              │  │
│  │  ├─ place_block(line, height, player_id)               │  │
│  │  │  └─ Occupies 2 height levels (h and h+1)            │  │
│  │  ├─ _is_valid_move(line, height, player_id)            │  │
│  │  │  └─ Validates both cells empty                      │  │
│  │  ├─ _check_win(line, height, player_id)                │  │
│  │  │  ├─ Count horizontal → Count per height level       │  │
│  │  │  ├─ Count vertical → Count stacked blocks           │  │
│  │  │  ├─ Count diagonal (↗↙)                             │  │
│  │  │  └─ Count diagonal (↘↖)                             │  │
│  │  ├─ _count_consecutive_*(...)                          │  │
│  │  │  └─ Count blocks in a direction                     │  │
│  │  └─ get_valid_moves()                                  │  │
│  │     └─ Return list of all valid placements            │  │
│  │                                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Game Creation Flow
```
Player 1 (Browser)
      ↓
LobbyComponent: "Create Game"
      ↓
GameService: POST /api/games
      ↓
Flask: @app.route('/api/games', methods=['POST'])
      ↓
Create GameSession(host_name)
      ↓
Store in games[game_id] = GameSession
      ↓
Return game_id to frontend
      ↓
Router navigates to GameComponent
      ↓
GameService: joinGameRoom(gameId, playerName)
      ↓
Socket.IO: emit('join_game_room')
      ↓
Backend: handle_join_room()
      ↓
Broadcast player_joined event
      ↓
GameComponent: Subscribe to gameState$
```

### Move Making Flow
```
Player 1: Click position button
      ↓
GameComponent: makeMove(line, height)
      ↓
GameService: POST /api/games/{id}/move
      ↓
Flask: @app.route('/api/games/<id>/move', methods=['POST'])
      ↓
GameSession.place_block(playerName, line, height)
      ↓
GameBoard.place_block(line, height, player_id)
      ↓
_is_valid_move() ← Validates
      ↓
Place in board[line][h] and board[line][h+1]
      ↓
_check_win() ← Check for 5-in-a-row
      ↓
Switch current_player
      ↓
Return updated game state
      ↓
HTTP response with new board
      ↓
GameService: updateGameState()
      ↓
BehaviorSubject emits new state
      ↓
GameComponent subscribes: Updates 3D visualization
      ↓
Socket.IO: Broadcast board_updated to all players in room
      ↓
Other player's GameComponent: Updates visualization
```

### Real-Time Sync Flow
```
Player 1 Makes Move
      ↓
Flask: emit('board_updated', state, room=gameId)
      ↓
Socket.IO: Broadcasts to all in game room
      ↓
┌─────────────────────────────────────────┐
│ Player 1 (Host)       │ Player 2 (Client)
│ Receives update       │ Receives update
│ Updates visualization │ Updates visualization
└─────────────────────────────────────────┘
      ↓
Both see same board state
      ↓
Turn indicator shows Player 2's turn
      ↓
Player 2 can now make move
```

## Component Communication

### Angular Services & Components
```
AppComponent (Root)
    ↓
    ├─ Router
    │   ├─ LobbyComponent → GameComponent
    │   └─ GameComponent → LobbyComponent
    │
    └─ GameService (Singleton)
        ├─ HTTP: Communicate with Flask API
        ├─ Socket: Real-time updates
        └─ State: BehaviorSubject<GameState>
            ├─ Subscribed by: LobbyComponent
            └─ Subscribed by: GameComponent

LobbyComponent
    ├─ Uses: GameService
    │   ├─ listGames()
    │   ├─ createGame()
    │   └─ joinGame()
    └─ Emits: Route to GameComponent with state

GameComponent
    ├─ Uses: GameService
    │   ├─ getGameState()
    │   ├─ startGame()
    │   ├─ makeMove()
    │   └─ joinGameRoom()
    ├─ Renders: Three.js 3D scene
    │   ├─ Blocks (Mesh objects)
    │   ├─ Grid
    │   └─ Lights
    └─ Subscribes: gameState$ updates
        └─ Re-renders blocks on update
```

## State Management

### Frontend State (GameState Object)
```typescript
{
  id: string,                    // Game session ID
  host: string,                  // Host player name
  players: {                      // Player mapping
    [name: string]: number|null  // 1, 2, or null (not started)
  },
  started: boolean,              // Game has started
  current_player: string,        // Current player name
  board: (number|null)[][],      // 9×9 board state
  game_over: boolean,            // Winner determined
  winner: number|null,           // 1 or 2 if won
  valid_moves: [                 // Available positions
    {line: number, height: number}
  ]
}
```

### Backend State (GameSession)
```python
GameSession {
  id: str              # Session ID
  host_name: str       # Host player name
  players: {           # Player to ID mapping
    name: id
  }
  board: GameBoard     # Game logic object
  started: bool        # Game started
  current_player_name: str
  created_at: datetime
}

GameBoard {
  board: list[list]    # 9×9 grid
  current_player: int  # 1 or 2
  game_over: bool
  winner: int|None
}
```

## Key Algorithms

### Block Placement Validation
```
Input: line, height, player_id
1. Check line: 0 ≤ line < 9
2. Check height: 0 ≤ height ≤ 7 (height+1 must be < 9)
3. Check both cells empty:
   - board[line][height] is None
   - board[line][height+1] is None
4. If all valid: place block (occupies both cells)
5. Else: return False
```

### Win Detection
```
Input: line, height, player_id
1. Check horizontal (along different height levels)
2. Check vertical (stacked)
3. Check diagonal (↗↙ direction)
4. Check diagonal (↘↖ direction)
For each direction:
   - Count consecutive blocks in both directions
   - If total ≥ 5: return True (win)
Return False
```

### Move Enumeration
```
For each line (0-8):
  For each height (0-7):
    If board[line][height] is None AND board[line][height+1] is None:
      Add {line, height} to valid_moves
Return valid_moves
```

## Communication Protocols

### REST API
```
HTTP Request/Response format:

GET /api/games
→ Response: [GamePreview, ...]

POST /api/games
← Body: {host_name: string}
→ Response: {game_id: string, ...}

POST /api/games/{gameId}/move
← Body: {player_name: string, line: int, height: int}
→ Response: GameState
```

### WebSocket Events
```
Client → Server:
  emit('join_game_room', {game_id, player_name})
  emit('game_move', {game_id, player_name, line, height})

Server → Clients:
  emit('board_updated', GameState)
  emit('error', {message: string})
  emit('player_joined', {player_name, game_id})
```

## Performance Characteristics

### Board Operations
```
place_block(): O(1)      # Direct array access
_is_valid_move(): O(1)   # Direct array access
_check_win(): O(1)       # Fixed number of directions
get_valid_moves(): O(81) # 9×8 positions max
```

### Network Operations
```
Create game: ~50-100ms (HTTP)
Join game: ~50-100ms (HTTP)
Place move: ~50-100ms (HTTP) + WebSocket broadcast
State update broadcast: <10ms (WebSocket)
Board render: <50ms (Three.js frame)
```

### Memory Usage
```
One game session:
  - Board: 72 integers (1KB)
  - Game session object: ~1KB
  - Connected player sockets: ~2KB each
  Total per game: ~5KB

Frontend:
  - GameState object: ~2KB
  - Three.js scene: ~10-20MB
  - Total: ~20-30MB
```

## Scalability Considerations

### Current Limitations
- Single backend process (no clustering)
- In-memory game storage (no persistence)
- Max 2 players per game

### Future Improvements
- Add database (PostgreSQL/MongoDB)
- Implement Redis for session storage
- Add Gunicorn workers for horizontal scaling
- Implement game history/replay

---

This architecture provides:
✅ Real-time multiplayer over network
✅ Reliable turn-based game state
✅ Simple yet extensible design
✅ Good separation of concerns
✅ Clear communication protocols
