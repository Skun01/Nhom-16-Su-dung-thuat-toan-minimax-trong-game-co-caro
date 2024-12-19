class TicTacToeLogic:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        
    def make_move(self, row, col, player):
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self, player):
        # Kiểm tra hàng
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        
        # Kiểm tra cột
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        
        # Kiểm tra đường chéo
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False

    def is_board_full(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))

    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)] 