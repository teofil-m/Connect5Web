"""
3D Connect 5 Game Board Logic
Board is 1x9x9: x=1 (width), y=9 (depth/lines), z=9 (height)
Blocks are 1x2 in size: 1 unit wide, 2 units in another dimension

Matrix representation: Each brick is tracked as an entity with:
- player_id: 1, 2, or None (owner of the brick)
- orientation: 'v' for vertical, 'h' for horizontal
- position: (line, height) - the starting position
"""

class GameBoard:
    def __init__(self):
        # Store bricks as a list of {'player_id', 'orientation', 'line', 'height'}
        self.bricks = []
        
        # Grid for quick lookup: grid[line][height] = brick_index or None
        # This helps us quickly check if a position is occupied
        self.grid = [[None for _ in range(9)] for _ in range(9)]
        
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def place_block(self, line, height, player_id, orientation='v'):
        """
        Place a 1x2 block at a position
        line: 0-8 (position on the 1x9 line)
        height: 0-8 (bottom position of the block)
        player_id: 1 or 2
        orientation: 'v' for vertical (occupies height and height+1), 'h' for horizontal (occupies line and line+1)
        """
        # Validate move
        if not self._is_valid_move(line, height, player_id, orientation):
            return False
        
        # Create brick
        brick = {
            'player_id': player_id,
            'orientation': orientation,
            'line': line,
            'height': height
        }
        
        # Add brick to list
        brick_index = len(self.bricks)
        self.bricks.append(brick)
        
        # Update grid
        if orientation == 'v':
            # Vertical: occupies (line, height) and (line, height+1)
            self.grid[line][height] = brick_index
            self.grid[line][height + 1] = brick_index
        else:  # orientation == 'h'
            # Horizontal: occupies (line, height) and (line+1, height)
            self.grid[line][height] = brick_index
            self.grid[line + 1][height] = brick_index
        
        # Check for win
        if self._check_win(line, height, player_id, orientation):
            self.game_over = True
            self.winner = player_id
            
        # Switch player
        self.current_player = 3 - player_id  # Toggle between 1 and 2
        return True
    
    def _is_valid_move(self, line, height, player_id, orientation='v'):
        """Check if a move is valid"""
        if orientation == 'v':
            # Vertical block: check bounds
            if line < 0 or line >= 9 or height < 0 or height > 7:
                return False
            
            # Check if cells are empty
            if self.grid[line][height] is not None or self.grid[line][height + 1] is not None:
                return False
            
            # Check support: either at ground or on another brick
            if height > 0:
                # Must have support below
                if self.grid[line][height - 1] is None:
                    return False
            
            # Check adjacency rule: no same-player bricks on left/right faces
            if line > 0:
                brick_left = self._get_brick_at(line - 1, height)
                if brick_left and brick_left['player_id'] == player_id:
                    return False
                brick_left_top = self._get_brick_at(line - 1, height + 1)
                if brick_left_top and brick_left_top['player_id'] == player_id:
                    return False
            
            if line < 8:
                brick_right = self._get_brick_at(line + 1, height)
                if brick_right and brick_right['player_id'] == player_id:
                    return False
                brick_right_top = self._get_brick_at(line + 1, height + 1)
                if brick_right_top and brick_right_top['player_id'] == player_id:
                    return False
            
            # Prevent vertical stacking of same player AND same orientation
            if height > 0:
                brick_below = self._get_brick_at(line, height - 1)
                if brick_below and brick_below['player_id'] == player_id and brick_below['orientation'] == 'v':
                    return False
            
            return True
            
        else:  # orientation == 'h'
            # Horizontal block: check bounds
            if line < 0 or line > 7 or height < 0 or height >= 9:
                return False
            
            # Check if cells are empty
            if self.grid[line][height] is not None or self.grid[line + 1][height] is not None:
                return False
            
            # Check support: either at ground or on another brick
            if height > 0:
                # Must have support below both cells
                if self.grid[line][height - 1] is None or self.grid[line + 1][height - 1] is None:
                    return False
            
            # Check adjacency rule: no same-player bricks on front/back faces
            if height > 0:
                brick_front = self._get_brick_at(line, height - 1)
                if brick_front and brick_front['player_id'] == player_id:
                    return False
                brick_front_right = self._get_brick_at(line + 1, height - 1)
                if brick_front_right and brick_front_right['player_id'] == player_id:
                    return False
            
            if height < 8:
                brick_back = self._get_brick_at(line, height + 1)
                if brick_back and brick_back['player_id'] == player_id:
                    return False
                brick_back_right = self._get_brick_at(line + 1, height + 1)
                if brick_back_right and brick_back_right['player_id'] == player_id:
                    return False
            
            # Check adjacency rule: no same-player bricks on left/right sides with same orientation
            if line > 0:
                brick_left = self._get_brick_at(line - 1, height)
                if brick_left and brick_left['player_id'] == player_id and brick_left['orientation'] == 'h':
                    return False
            
            if line < 7:
                brick_right = self._get_brick_at(line + 2, height)
                if brick_right and brick_right['player_id'] == player_id and brick_right['orientation'] == 'h':
                    return False
            
            # Prevent vertical stacking of same player
            if height > 0:
                brick_below_left = self._get_brick_at(line, height - 1)
                brick_below_right = self._get_brick_at(line + 1, height - 1)
                if (brick_below_left and brick_below_left['player_id'] == player_id) or \
                   (brick_below_right and brick_below_right['player_id'] == player_id):
                    return False
            
            return True
    
    def _get_brick_at(self, line, height):
        """Get the brick occupying this cell, or None"""
        if line < 0 or line >= 9 or height < 0 or height >= 9:
            return None
        brick_idx = self.grid[line][height]
        if brick_idx is None:
            return None
        return self.bricks[brick_idx]
    
    def _check_win(self, line, height, player_id, orientation):
        """Check if placing a block creates a winning condition (5 in a row)"""
        # Check all four directions for 5 in a row
        
        # For vertical blocks, check at both height and height+1
        heights_to_check = [height] if orientation == 'h' else [height, height + 1]
        
        for check_height in heights_to_check:
            # Direction 1: Horizontal (along the line)
            if self._count_consecutive_horizontal(line, check_height, player_id) >= 5:
                return True
            
            # Direction 2: Vertical (along height)
            if self._count_consecutive_vertical(line, check_height, player_id) >= 5:
                return True
            
            # Direction 3: Diagonal (line increases, height increases)
            if self._count_consecutive_diagonal_lr(line, check_height, player_id) >= 5:
                return True
            
            # Direction 4: Diagonal (line increases, height decreases)
            if self._count_consecutive_diagonal_lr_inv(line, check_height, player_id) >= 5:
                return True
        
        return False
    
    def _count_consecutive_horizontal(self, line, height, player_id):
        """Count consecutive blocks horizontally at a given height"""
        count = 1
        
        # Check left
        check_line = line - 1
        while check_line >= 0:
            brick = self._get_brick_at(check_line, height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_line -= 1
            else:
                break
        
        # Check right
        check_line = line + 1
        while check_line < 9:
            brick = self._get_brick_at(check_line, height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_line += 1
            else:
                break
        
        return count
    
    def _count_consecutive_vertical(self, line, height, player_id):
        """Count consecutive blocks vertically (stacked)"""
        count = 1
        
        # Check up
        check_height = height + 1
        while check_height < 9:
            brick = self._get_brick_at(line, check_height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_height += 1
            else:
                break
        
        # Check down
        check_height = height - 1
        while check_height >= 0:
            brick = self._get_brick_at(line, check_height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_height -= 1
            else:
                break
        
        return count
    
    def _count_consecutive_diagonal_lr(self, line, height, player_id):
        """Count diagonal: line increases, height increases"""
        count = 1
        
        # Check up-right
        check_line = line + 1
        check_height = height + 1
        while check_line < 9 and check_height < 9:
            brick = self._get_brick_at(check_line, check_height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_line += 1
                check_height += 1
            else:
                break
        
        # Check down-left
        check_line = line - 1
        check_height = height - 1
        while check_line >= 0 and check_height >= 0:
            brick = self._get_brick_at(check_line, check_height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_line -= 1
                check_height -= 1
            else:
                break
        
        return count
    
    def _count_consecutive_diagonal_lr_inv(self, line, height, player_id):
        """Count diagonal: line increases, height decreases"""
        count = 1
        
        # Check up-left
        check_line = line - 1
        check_height = height + 1
        while check_line >= 0 and check_height < 9:
            brick = self._get_brick_at(check_line, check_height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_line -= 1
                check_height += 1
            else:
                break
        
        # Check down-right
        check_line = line + 1
        check_height = height - 1
        while check_line < 9 and check_height >= 0:
            brick = self._get_brick_at(check_line, check_height)
            if brick and brick['player_id'] == player_id:
                count += 1
                check_line += 1
                check_height -= 1
            else:
                break
        
        return count
    
    def get_board_state(self):
        """Return current board state - convert bricks back to matrix format for frontend"""
        # Create board matrix for frontend (matches expected format)
        board = [[None for _ in range(9)] for _ in range(9)]
        orientations = [[None for _ in range(9)] for _ in range(9)]
        
        # Fill in board and orientations from bricks
        for brick in self.bricks:
            player_id = brick['player_id']
            line = brick['line']
            height = brick['height']
            orientation = brick['orientation']
            
            if orientation == 'v':
                board[line][height] = player_id
                board[line][height + 1] = player_id
                orientations[line][height] = 'v'
                orientations[line][height + 1] = 'v'
            else:  # 'h'
                board[line][height] = player_id
                board[line + 1][height] = player_id
                orientations[line][height] = 'h'
                orientations[line + 1][height] = 'h'
        
        return {
            'board': board,
            'orientations': orientations,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner
        }
    
    def get_valid_moves(self):
        """Return list of valid moves with orientations"""
        valid_moves = []
        for line in range(9):
            for height in range(9):
                # Check vertical placement
                if self._is_valid_move(line, height, self.current_player, 'v'):
                    valid_moves.append({'line': line, 'height': height, 'orientation': 'v'})
                # Check horizontal placement
                if self._is_valid_move(line, height, self.current_player, 'h'):
                    valid_moves.append({'line': line, 'height': height, 'orientation': 'h'})
        return valid_moves
