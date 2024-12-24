class GomokuLogic:
    def __init__(self, size=9):  # Mặc định bàn cờ 9x9
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        
    def make_move(self, row, col, player):
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self, player):
        """
        Args:
            player (str): Người chơi cần kiểm tra ('X' hoặc 'O')
            
        Returns:
            bool: True nếu người chơi đã thắng, False nếu chưa
        """
        # player là người chơi
        # Kiểm tra hàng ngang
        for i in range(self.size):
            for j in range(self.size - 4):
                if all(self.board[i][j+k] == player for k in range(5)):
                    return True
        
        # Kiểm tra hàng dọc
        for i in range(self.size - 4):
            for j in range(self.size):
                if all(self.board[i+k][j] == player for k in range(5)):
                    return True
        
        # Kiểm tra đường chéo xuống
        for i in range(self.size - 4):
            for j in range(self.size - 4):
                if all(self.board[i+k][j+k] == player for k in range(5)):
                    return True
        
        # Kiểm tra đường chéo lên
        for i in range(4, self.size):
            for j in range(self.size - 4):
                if all(self.board[i-k][j+k] == player for k in range(5)):
                    return True
        
        return False

    def is_board_full(self):
        return all(self.board[i][j] != '' for i in range(self.size) 
                  for j in range(self.size))

    def reset(self):
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)] 