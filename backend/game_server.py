"""
Flask server with WebSocket support for Connect 5 game
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from game_board import GameBoard
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'connect5-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Game sessions storage
games = {}
players = {}

class GameSession:
    def __init__(self, host_name):
        self.id = str(uuid.uuid4())[:8]
        self.host_name = host_name
        self.players = {host_name: None}
        self.board = GameBoard()
        self.started = False
        self.created_at = datetime.now()
        self.current_player_name = host_name
        self.is_free_play = False
        
    def add_player(self, player_name):
        if len(self.players) >= 2:
            return False
        if player_name in self.players:
            return False
        self.players[player_name] = None
        return True
    
    def start_game(self):
        if len(self.players) != 2:
            return False
        self.started = True
        # First player is random (could be improved to be first join)
        player_list = list(self.players.keys())
        self.players[player_list[0]] = 1  # Player 1
        self.players[player_list[1]] = 2  # Player 2
        self.current_player_name = player_list[0]
        return True
    
    def place_block(self, player_name, line, height, orientation='v'):
        if not self.started:
            return False, "Game not started"
        
        if player_name != self.current_player_name:
            return False, "Not your turn"
        
        player_id = self.players[player_name]
        
        if self.board.place_block(line, height, player_id, orientation):
            # Switch to next player
            player_list = list(self.players.keys())
            current_idx = player_list.index(player_name)
            self.current_player_name = player_list[1 - current_idx]
            return True, "Block placed successfully"
        else:
            return False, "Invalid move"
    
    def get_state(self):
        board_state = self.board.get_board_state()
        return {
            'id': self.id,
            'host': self.host_name,
            'players': self.players,
            'started': self.started,
            'current_player': self.current_player_name,
            'board': board_state['board'],
            'orientations': board_state['orientations'],
            'game_over': board_state['game_over'],
            'winner': board_state['winner'],
            'valid_moves': self.board.get_valid_moves(),
            'is_free_play': self.is_free_play
        }


class FreePlayGameSession:
    """Game session for single-player free play mode"""
    def __init__(self, player_name):
        self.id = str(uuid.uuid4())[:8]
        self.host_name = player_name
        self.players = {player_name: 1}  # Single player as player 1
        self.board = GameBoard()
        self.started = False
        self.created_at = datetime.now()
        self.current_player_name = player_name
        self.is_free_play = True
    
    def start_game(self):
        """Start the free play game"""
        self.started = True
        return True
    
    def place_block(self, player_name, line, height, orientation='v'):
        """Place a block in free play mode (no turn restrictions)"""
        if not self.started:
            return False, "Game not started"
        
        # In free play, always allow moves from the single player
        player_id = self.players[player_name]
        
        if self.board.place_block(line, height, player_id, orientation):
            return True, "Block placed successfully"
        else:
            return False, "Invalid move"
    
    def get_state(self):
        board_state = self.board.get_board_state()
        return {
            'id': self.id,
            'host': self.host_name,
            'players': self.players,
            'started': self.started,
            'current_player': self.current_player_name,
            'board': board_state['board'],
            'orientations': board_state['orientations'],
            'game_over': board_state['game_over'],
            'winner': board_state['winner'],
            'valid_moves': self.board.get_valid_moves(),
            'is_free_play': self.is_free_play
        }


# REST API Endpoints

@app.route('/api/games', methods=['GET'])
def list_games():
    """List available games"""
    available_games = []
    for game_id, game in games.items():
        if not game.started and len(game.players) < 2:
            available_games.append({
                'id': game.id,
                'host': game.host_name,
                'players_count': len(game.players),
                'created_at': game.created_at.isoformat()
            })
    return jsonify(available_games)


@app.route('/api/games', methods=['POST'])
def create_game():
    """Create a new game"""
    data = request.json
    host_name = data.get('host_name', 'Player')
    
    if not host_name or len(host_name) == 0:
        return jsonify({'error': 'Invalid host name'}), 400
    
    game = GameSession(host_name)
    games[game.id] = game
    players[host_name] = game.id
    
    return jsonify({
        'game_id': game.id,
        'host': host_name,
        'message': 'Game created successfully'
    })


@app.route('/api/games/free-play', methods=['POST'])
def create_free_play_game():
    """Create a free play game for single player"""
    data = request.json
    player_name = data.get('player_name', 'Player')
    
    if not player_name or len(player_name) == 0:
        return jsonify({'error': 'Invalid player name'}), 400
    
    game = FreePlayGameSession(player_name)
    games[game.id] = game
    players[player_name] = game.id
    
    # Auto-start free play games
    game.start_game()
    
    return jsonify({
        'game_id': game.id,
        'host': player_name,
        'message': 'Free play game created successfully'
    })


@app.route('/api/games/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get game state"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    return jsonify(game.get_state())


@app.route('/api/games/<game_id>/join', methods=['POST'])
def join_game(game_id):
    """Join a game"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    player_name = data.get('player_name', 'Player')
    
    if not player_name or len(player_name) == 0:
        return jsonify({'error': 'Invalid player name'}), 400
    
    game = games[game_id]
    
    if game.started:
        return jsonify({'error': 'Game already started'}), 400
    
    if not game.add_player(player_name):
        return jsonify({'error': 'Cannot join game'}), 400
    
    players[player_name] = game_id
    socketio.emit('game_state_updated', game.get_state(), room=game_id)
    
    return jsonify({
        'game_id': game.id,
        'players': list(game.players.keys()),
        'message': 'Joined successfully'
    })


@app.route('/api/games/<game_id>/start', methods=['POST'])
def start_game(game_id):
    """Start a game"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if not game.start_game():
        return jsonify({'error': 'Cannot start game'}), 400
    
    state = game.get_state()
    socketio.emit('game_started', state, room=game_id)
    return jsonify(state)


@app.route('/api/games/<game_id>/move', methods=['POST'])
def make_move(game_id):
    """Make a move in the game"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    player_name = data.get('player_name')
    line = data.get('line')
    height = data.get('height')
    orientation = data.get('orientation', 'v')  # Default to vertical
    
    if player_name is None or line is None or height is None:
        return jsonify({'error': 'Invalid move data'}), 400
    
    game = games[game_id]
    
    success, message = game.place_block(player_name, line, height, orientation)
    
    if not success:
        return jsonify({'error': message}), 400
    
    state = game.get_state()
    # Broadcast move to all players
    socketio.emit('board_updated', state, room=game_id)
    return jsonify(state)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


# WebSocket Events (for real-time updates)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected to server'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join_game_room')
def handle_join_room(data):
    game_id = data.get('game_id')
    player_name = data.get('player_name')
    join_room(game_id)
    emit('player_joined', {
        'player_name': player_name,
        'game_id': game_id
    }, room=game_id)


@socketio.on('game_move')
def handle_game_move(data):
    game_id = data.get('game_id')
    player_name = data.get('player_name')
    line = data.get('line')
    height = data.get('height')
    orientation = data.get('orientation', 'v')  # Default to vertical
    
    if game_id not in games:
        emit('error', {'message': 'Game not found'})
        return
    
    game = games[game_id]
    success, message = game.place_block(player_name, line, height, orientation)
    
    if success:
        emit('board_updated', game.get_state(), room=game_id)
    else:
        emit('error', {'message': message})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
