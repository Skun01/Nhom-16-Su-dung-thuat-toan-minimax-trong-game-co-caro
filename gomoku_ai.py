import random

class GomokuAI:
    """
    Lớp AI cho trò chơi Gomoku (Cờ Carô)
    Sử dụng thuật toán Minimax với Alpha-Beta Pruning
    """

    # Bảng điểm cho các tình huống khác nhau
    # (số_quân_liên_tiếp, số_đầu_bị_chặn): điểm
    SCORE_TABLE = {
        (4, 0): 10000,  # 4 quân liên tiếp, không bị chặn (cực kỳ nguy hiểm)
        (4, 1): 1000,   # 4 quân liên tiếp, bị chặn 1 đầu (nguy hiểm)
        (3, 0): 1000,   # 3 quân liên tiếp, không bị chặn (nguy hiểm)
        (3, 1): 100,    # 3 quân liên tiếp, bị chặn 1 đầu
        (2, 0): 100,    # 2 quân liên tiếp, không bị chặn
        (2, 1): 10      # 2 quân liên tiếp, bị chặn 1 đầu
    }

    @staticmethod
    def get_easy_move(board):
        """
        Chế độ dễ: Chọn ngẫu nhiên một ô trống trên bàn cờ
        Args:
            board: Mảng 2D đại diện cho bàn cờ
        Returns:
            Tuple (row, col) cho nước đi được chọn, hoặc None nếu không còn ô trống
        """
        size = len(board)
        empty_cells = [(i, j) for i in range(size) for j in range(size) 
                      if board[i][j] == '']
        return random.choice(empty_cells) if empty_cells else None

    @staticmethod
    def evaluate_position(board, row, col, player):
        """
        Đánh giá giá trị của một vị trí cụ thể trên bàn cờ
        
        Đầu vào:
            board: Mảng 2D đại diện cho bàn cờ
            row, col: Tọa độ vị trí cần đánh giá
            player: Người chơi ('O' hoặc 'X')
            
        Returns:
            Số điểm của vị trí đó
        """
        size = len(board)
        score = 0
        # Kiểm tra 4 hướng: ngang, dọc, chéo xuống, chéo lên
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dx, dy in directions:
            count = 1  # Số quân liên tiếp
            blocks = 0  # Số đầu bị chặn
            empty = 0  # Số ô trống
            
            # Kiểm tra cả hai hướng (thuận và ngược)
            for direction in [1, -1]:
                for i in range(1, 5):  # Kiểm tra tối đa 4 ô mỗi hướng
                    new_row = row + dx * i * direction
                    new_col = col + dy * i * direction
                    
                    if 0 <= new_row < size and 0 <= new_col < size:
                        cell = board[new_row][new_col]
                        if cell == player:
                            count += 1
                        elif cell == '':
                            empty += 1
                            break
                        else:  # Quân đối thủ
                            blocks += 1
                            break
                    else:  # Ra ngoài bàn cờ
                        blocks += 1
                        break

            # Tính điểm dựa trên bảng lookup
            if count >= 5:  # Thắng ngay lập tức
                return 100000
            score += GomokuAI.SCORE_TABLE.get((count, blocks), 0)
        
        return score

    @staticmethod
    def evaluate_board(board):
        """
        Đánh giá toàn bộ bàn cờ
        Điểm dương có lợi cho 'O', điểm âm có lợi cho 'X'
        """
        size = len(board)
        score = 0
        
        for i in range(size):
            for j in range(size):
                if board[i][j] == 'O':
                    score += GomokuAI.evaluate_position(board, i, j, 'O')
                elif board[i][j] == 'X':
                    score -= GomokuAI.evaluate_position(board, i, j, 'X')
        
        return score

    @staticmethod
    def get_valid_moves(board):
        """
        Tìm tất cả các nước đi hợp lệ (các ô trống gần với quân cờ hiện có)
        Tối ưu hóa bằng cách chỉ xét các ô xung quanh quân cờ đã có
        """
        size = len(board)
        valid_moves = set()  # Dùng set để tránh trùng lặp
        
        for i in range(size):
            for j in range(size):
                if board[i][j] != '':  # Nếu ô có quân cờ
                    # Xét 8 ô xung quanh
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if (0 <= ni < size and 0 <= nj < size and 
                                board[ni][nj] == ''):
                                valid_moves.add((ni, nj))
        
        return list(valid_moves)

    @staticmethod
    def minimax(board, depth, alpha, beta, is_maximizing):
        """
        Thuật toán Minimax với Alpha-Beta Pruning
        
        Args:
            board: Bàn cờ hiện tại
            depth: Độ sâu còn lại cần tìm kiếm
            alpha, beta: Giới hạn trên và dưới cho alpha-beta pruning
            is_maximizing: True nếu đang tối đa hóa (lượt của 'O')
        
        Returns:
            Giá trị đánh giá tốt nhất cho nước đi
        """
        # Kiểm tra điều kiện dừng
        current_score = GomokuAI.evaluate_board(board)
        if abs(current_score) >= 90000 or depth == 0:
            return current_score
        
        valid_moves = GomokuAI.get_valid_moves(board)
        if not valid_moves:
            return 0
        
        # Sắp xếp nước đi theo tiềm năng để cải thiện alpha-beta pruning
        moves_with_scores = []
        for i, j in valid_moves:
            board[i][j] = 'O' if is_maximizing else 'X'
            score = GomokuAI.evaluate_board(board)
            board[i][j] = ''
            moves_with_scores.append((score, (i, j)))
        
        # Sắp xếp nước đi (giảm dần cho maximizing, tăng dần cho minimizing)
        moves_with_scores.sort(reverse=is_maximizing)
        
        if is_maximizing:
            max_eval = float('-inf')
            for _, (i, j) in moves_with_scores:
                board[i][j] = 'O'
                eval = GomokuAI.minimax(board, depth - 1, alpha, beta, False)
                board[i][j] = ''
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:  # Cắt tỉa alpha-beta
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for _, (i, j) in moves_with_scores:
                board[i][j] = 'X'
                eval = GomokuAI.minimax(board, depth - 1, alpha, beta, True)
                board[i][j] = ''
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:  # Cắt tỉa alpha-beta
                    break
            return min_eval

    @staticmethod
    def get_best_move(board):
        """
        Tìm nước đi tốt nhất cho AI ('O')
        Sử dụng chiến lược:
        1. Tìm tất cả nước đi hợp lệ
        2. Đánh giá nhanh và chọn top 5 nước đi tốt nhất
        3. Áp dụng minimax cho các nước đi này
        """
        valid_moves = GomokuAI.get_valid_moves(board)
        if not valid_moves:
            # Nếu không có nước đi hợp lệ, chọn ngẫu nhiên một ô trống
            empty_cells = [(i, j) for i in range(len(board)) 
                          for j in range(len(board)) if board[i][j] == '']
            return random.choice(empty_cells) if empty_cells else None
        
        # Đánh giá nhanh các nước đi
        moves_with_scores = []
        for i, j in valid_moves:
            board[i][j] = 'O'
            score = GomokuAI.evaluate_board(board)
            board[i][j] = ''
            moves_with_scores.append((score, (i, j)))
        
        # Chọn top 5 nước đi tốt nhất để phân tích sâu hơn
        moves_with_scores.sort(reverse=True)
        top_moves = moves_with_scores[:5]
        
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Áp dụng minimax cho top 5 nước đi
        for _, (i, j) in top_moves:
            board[i][j] = 'O'
            move_value = GomokuAI.minimax(board, 2, alpha, beta, False)
            board[i][j] = ''
            
            if move_value > best_value:
                best_value = move_value
                best_move = (i, j)
        
        return best_move