import random
#Thuật toán mimmax
class AIPlayer:
    @staticmethod
    def get_easy_move(board):
        # Độ khó DỄ: Đi ngẫu nhiên
        empty_cells = [(i, j) for i in range(3) for j in range(3) 
                      if board[i][j] == '']
        return random.choice(empty_cells) if empty_cells else None

    @staticmethod
    def get_best_move(board):
        # Độ khó KHÓ: Sử dụng minimax để tìm nước đi tối ưu
        best_score = float('-inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = AIPlayer.minimax(board, 0, False)
                    board[i][j] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move

    @staticmethod
    def minimax(board, depth, is_maximizing):
        """
        Thuật toán minimax để tính điểm cho mỗi trạng thái bàn cờ
        
        Đầu vào:
            board: Trạng thái bàn cờ hiện tại
            depth: Độ sâu của đệ quy
            is_maximizing: True nếu là lượt của máy (O), False nếu là lượt của người chơi (X)
        
        Đầu ra:
            int: Điểm số của trạng thái bàn cờ
                1: nếu O thắng
                -1: nếu X thắng
                0: nếu hòa
        """
        def check_winner(player):
            # Kiểm tra hàng và cột
            for i in range(3):
                if all(board[i][j] == player for j in range(3)) or \
                   all(board[j][i] == player for j in range(3)):
                    return True
            # Kiểm tra đường chéo
            if all(board[i][i] == player for i in range(3)) or \
               all(board[i][2-i] == player for i in range(3)):
                return True
            return False

        # Kiểm tra điều kiện dừng
        if check_winner('O'):
            return 1  # Máy thắng
        if check_winner('X'):
            return -1  # Người chơi thắng
        if all(board[i][j] != '' for i in range(3) for j in range(3)):
            return 0  # Hòa
        
        if is_maximizing:
            # Lượt của máy (O) - tìm nước đi có điểm cao nhất
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        score = AIPlayer.minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            # Lượt của người chơi (X) - tìm nước đi có điểm thấp nhất
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        score = AIPlayer.minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score 