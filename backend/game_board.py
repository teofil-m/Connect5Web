"""
3D Connect 5 Game Board Logic
Board is 1x9x9: x=1 (width), y=9 (depth/lines), z=9 (height)
Blocks are 1x2 in size: 1 unit wide, 2 units in another dimension
"""

class GameBoard:
    def __init__(self):
        # Board[line][height] = player_id (1 or 2) or None
        # line: 0-8 (represents positions along the 1x9 line)
        # height: 0-8 (represents height from 0 to 8)
        self.board = [[None for _ in range(9)] for _ in range(9)]
        # Store orientation: 'v' for vertical (2 high), 'h' for horizontal (2 wide along line)
        self.orientations = [[None for _ in range(9)] for _ in range(9)]
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
            
        # Place the block
        if orientation == 'v':
            # Vertical: occupies height and height+1 at same line
            self.board[line][height] = player_id
            self.board[line][height + 1] = player_id
            self.orientations[line][height] = 'v'
            self.orientations[line][height + 1] = 'v'
        else:  # orientation == 'h'
            # Horizontal: occupies line and line+1 at same height
            self.board[line][height] = player_id
            self.board[line + 1][height] = player_id
            self.orientations[line][height] = 'h'
            self.orientations[line + 1][height] = 'h'
        
        # Check for win
        if self._check_win(line, height, player_id):
            self.game_over = True
            self.winner = player_id
            
        # Switch player
        self.current_player = 3 - player_id  # Toggle between 1 and 2
        return True
    
    def _is_valid_move(self, line, height, player_id, orientation='v'):
        """Check if a move is valid"""
        if orientation == 'v':
            # Vertical block: check bounds and space
            if line < 0 or line >= 9 or height < 0 or height > 7:
                return False
            if self.board[line][height] is not None or self.board[line][height + 1] is not None:
                return False
            # Check if block is supported: either at ground level or on top of another block
            if height == 0:
                # At ground level - valid
                return True
            # Must have support below (something at height-1)
            return self.board[line][height - 1] is not None
        else:  # orientation == 'h'
            # Horizontal block: check bounds and space
            if line < 0 or line > 7 or height < 0 or height >= 9:
                return False
            if self.board[line][height] is not None or self.board[line + 1][height] is not None:
                return False
            # Check if block is supported: either at ground level or on top of another block
            if height == 0:
                # At ground level - valid
                return True
            # Must have support below (something at height-1)
            return self.board[line][height - 1] is not None and self.board[line + 1][height - 1] is not None
    
    def _check_win(self, line, height, player_id):
        """Check if placing a block creates a winning condition (5 in a row)"""
        # Check all four directions: horizontal (along line), vertical (up/down), and diagonals
        
        # Direction 1: Horizontal (along the line)
        if self._count_consecutive_horizontal(line, height, player_id) >= 5:
            return True
            
        # Direction 2: Vertical (along height)
        if self._count_consecutive_vertical(line, height, player_id) >= 5:
            return True
            
        # Direction 3: Diagonal (line increases, height increases)
        if self._count_consecutive_diagonal_lr(line, height, player_id) >= 5:
            return True
            
        # Direction 4: Diagonal (line increases, height decreases)
        if self._count_consecutive_diagonal_lr_inv(line, height, player_id) >= 5:
            return True
            
        return False
    
    def _count_consecutive_horizontal(self, line, height, player_id):
        """Count consecutive blocks horizontally along a line at a given height"""
        # This counts blocks at this specific height level that are adjacent horizontally
        # But since board is only 1 unit wide (x=1), this checks same line but different heights
        # Actually, "horizontal" means along the line (y-axis): same height, check both heights of the block
        
        count = 0
        # Check height (bottom of block)
        count += self._count_in_direction(line, height, 0, player_id)
        # Check height+1 (top of block)
        count += self._count_in_direction(line, height + 1, 0, player_id)
        
        return count
    
    def _count_consecutive_vertical(self, line, height, player_id):
        """Count consecutive blocks vertically (stacked)"""
        count = 0
        # Count upward
        count += self._count_in_direction(line, height, 1, player_id)
        # Count downward
        count += self._count_in_direction(line, height, -1, player_id)
        
        return count
    
    def _count_consecutive_diagonal_lr(self, line, height, player_id):
        """Count diagonal: line increases, height increases"""
        count = 0
        # Count up-right
        count += self._count_in_direction_diagonal(line, height, 1, 1, player_id)
        # Count down-left
        count += self._count_in_direction_diagonal(line, height, -1, -1, player_id)
        
        return count
    
    def _count_consecutive_diagonal_lr_inv(self, line, height, player_id):
        """Count diagonal: line increases, height decreases"""
        count = 0
        # Count up-left
        count += self._count_in_direction_diagonal(line, height, -1, 1, player_id)
        # Count down-right
        count += self._count_in_direction_diagonal(line, height, 1, -1, player_id)
        
        return count
    
    def _count_in_direction(self, line, height, direction, player_id):
        """
        Count consecutive blocks in a direction
        direction: 0 = horizontal (along line), 1 = up, -1 = down
        For horizontal, we actually stay in same line but check height values
        """
        count = 1  # Include the current position
        
        if direction == 0:  # Horizontal check along different heights
            # This doesn't make sense for our board. Skip.
            return 1
        else:  # Vertical (direction is 1 or -1 for height)
            pos = height + direction
            while 0 <= pos < 9 and self.board[line][pos] == player_id:
                count += 1
                pos += direction
                
        return count
    
    def _count_in_direction_diagonal(self, line, height, line_dir, height_dir, player_id):
        """Count consecutive blocks in a diagonal direction"""
        count = 1  # Include the current position
        
        line_pos = line + line_dir
        height_pos = height + height_dir
        
        while 0 <= line_pos < 9 and 0 <= height_pos < 9 and self.board[line_pos][height_pos] == player_id:
            count += 1
            line_pos += line_dir
            height_pos += height_dir
            
        return count
    
    def get_board_state(self):
        """Return current board state"""
        return {
            'board': self.board,
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
