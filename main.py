import tkinter as tk
from tkinter import ttk, messagebox
import random
from game_logic import TicTacToeLogic
from ai_player import AIPlayer
from gomoku_logic import GomokuLogic
from gomoku_ai import GomokuAI

class DifficultySelector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cờ Ca-rô")
        self.window.geometry("300x400")
        self.window.resizable(False, False)  # Không cho phép thay đổi kích thước
        self.window.configure(bg='#f0f0f0')
        
        # Căn giữa cửa sổ
        self.center_window(self.window, 300, 400)
        
        self.selected_difficulty = None
        
        # Title
        title_label = tk.Label(self.window, text="Cờ Ca-rô",
                             font=('Arial', 24, 'bold'),
                             bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(self.window, text="Chọn độ khó",
                                font=('Arial', 16),
                                bg='#f0f0f0', fg='#666666')
        subtitle_label.pack(pady=10)
        
        # Difficulty buttons
        difficulties = [("Dễ", "#4CAF50"),
                       ("Trung bình", "#FFA500"),
                       ("Khó", "#f44336")]
        
        for diff, color in difficulties:
            btn = tk.Button(self.window, text=diff,
                          font=('Arial', 14),
                          width=15, height=2,
                          bg=color, fg='white',
                          command=lambda d=diff: self.select_difficulty(d))
            btn.pack(pady=10)
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#666666'))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def select_difficulty(self, difficulty):
        difficulty_map = {
            "Dễ": "Easy",
            "Trung bình": "Medium",
            "Khó": "Hard"
        }
        self.selected_difficulty = difficulty_map[difficulty]
        self.window.destroy()
    
    def get_difficulty(self):
        self.window.mainloop()
        return self.selected_difficulty

class TicTacToe:
    def __init__(self, difficulty):
        self.window = tk.Tk()
        self.window.title("Cờ Ca-rô")
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(False, False)  # Không cho phép thay đổi kích thước
        
        # Căn giữa cửa sổ
        window_width = 400
        window_height = 500
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.game_logic = TicTacToeLogic()
        self.ai_player = AIPlayer()
        self.current_player = 'X'
        self.difficulty = difficulty
        difficulty_map = {
            "Easy": "Dễ",
            "Medium": "Trung bình",
            "Hard": "Khó"
        }
        # Game info frame
        self.info_frame = tk.Frame(self.window, bg='#f0f0f0', height=50)
        self.info_frame.pack(pady=10)
        
        # Tạo frame riêng cho turn indicator
        self.turn_frame = tk.Frame(self.window, bg='#f0f0f0', height=40)
        self.turn_frame.pack(pady=5)
        
        self.difficulty_label = tk.Label(self.info_frame,
                                       text=f"Độ khó: {difficulty_map[difficulty]}",
                                       font=('Arial', 12),
                                       bg='#f0f0f0')
        self.difficulty_label.pack()
        
        # Turn indicator với thông báo rõ ràng hơn
        self.turn_indicator = tk.Label(self.turn_frame,
                                     text="Đến lượt người chơi (X)",
                                     font=('Arial', 14, 'bold'),
                                     bg='#f0f0f0', fg='#333333')
        self.turn_indicator.pack()
        
        # Game board frame
        self.game_frame = tk.Frame(self.window, bg='#666666')
        self.game_frame.pack(padx=10, pady=10)
        
        # Tạo và cấu hình các nút với kích thước cố định
        button_size = 80  # Kích thước cố định cho mỗi nút
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.game_frame, width=button_size, height=button_size)
                frame.grid(row=i, column=j, padx=2, pady=2)
                frame.pack_propagate(False)  # Giữ kích thước cố định
                
                self.buttons[i][j] = tk.Button(frame,
                                             text='',
                                             font=('Arial', 24, 'bold'),
                                             bg='white',
                                             command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].pack(expand=True, fill='both')
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.window, bg='#f0f0f0', height=50)
        self.control_frame.pack(pady=10)
        
        # Tạo frame con cho các nút điều khiển
        button_frame = tk.Frame(self.control_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        # Style cho các nút
        button_style = {
            'font': ('Arial', 12),
            'width': 12,
            'height': 2,
            'relief': tk.RAISED,
            'borderwidth': 2
        }
        
        self.reset_button = tk.Button(button_frame,
                                    text="Chơi lại",
                                    bg='#4CAF50', fg='white',
                                    command=self.reset_game,
                                    **button_style)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.home_button = tk.Button(button_frame,
                                   text="Trang chủ",
                                   bg='#2196F3', fg='white',
                                   command=self.return_home,
                                   **button_style)
        self.home_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(button_frame,
                                   text="Thoát",
                                   bg='#f44336', fg='white',
                                   command=self.window.destroy,
                                   **button_style)
        self.quit_button.pack(side=tk.LEFT, padx=5)
        
        # Thêm hover effect cho các nút
        for button in [self.reset_button, self.home_button, self.quit_button]:
            button.bind('<Enter>', lambda e, b=button: self.on_button_hover(b, True))
            button.bind('<Leave>', lambda e, b=button: self.on_button_hover(b, False))

    def return_home(self):
        self.window.destroy()
        difficulty_selector = DifficultySelector()
        selected_difficulty = difficulty_selector.get_difficulty()
        if selected_difficulty:
            game = TicTacToe(selected_difficulty)
            game.run()

    def make_move(self, row, col):
        if self.game_logic.make_move(row, col, self.current_player):
            self.buttons[row][col].config(text=self.current_player,
                                        fg='#333333' if self.current_player == 'X' else '#f44336')
            
            if self.game_logic.check_winner(self.current_player):
                winner = "Bạn" if self.current_player == 'X' else "Máy"
                messagebox.showinfo("Kết thúc", f"{winner} thắng!")
                self.reset_game()
                return
            
            if self.game_logic.is_board_full():
                messagebox.showinfo("Kết thúc", "Hòa!")
                self.reset_game()
                return
            
            self.current_player = 'O'
            self.turn_indicator.config(text="Đến lượt máy tính (O)", fg='#f44336')
            
            # Vô hiệu hóa các nút khi máy đang suy nghĩ
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(state='disabled')
            
            self.window.after(500, self.make_computer_move)

    def make_computer_move(self):
        if self.difficulty == "Easy":
            row, col = self.ai_player.get_easy_move(self.game_logic.board)
        elif self.difficulty == "Medium":
            if random.random() < 0.7:
                row, col = self.ai_player.get_best_move(self.game_logic.board)
            else:
                row, col = self.ai_player.get_easy_move(self.game_logic.board)
        else:  # Hard
            row, col = self.ai_player.get_best_move(self.game_logic.board)
        
        if row is not None and col is not None:
            self.game_logic.make_move(row, col, self.current_player)
            self.buttons[row][col].config(text=self.current_player,
                                        fg='#333333' if self.current_player == 'X' else '#f44336')
            
            if self.game_logic.check_winner(self.current_player):
                messagebox.showinfo("Kết thúc", "Máy thắng!")
                self.reset_game()
                return
            
            if self.game_logic.is_board_full():
                messagebox.showinfo("Kết thúc", "Hòa!")
                self.reset_game()
                return
            
            self.current_player = 'X'
            self.turn_indicator.config(text="Đến lượt người chơi (X)", fg='#333333')
            
            # Kích hoạt lại các nút sau khi máy đã đi
            for i in range(3):
                for j in range(3):
                    if self.game_logic.board[i][j] == '':
                        self.buttons[i][j].config(state='normal')

    def reset_game(self):
        self.game_logic.reset()
        self.current_player = 'X'
        self.turn_indicator.config(text="Đến lượt người chơi (X)", fg='#333333')
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')

    def on_button_hover(self, button, entering):
        """Xử lý hiệu ứng hover cho nút"""
        original_colors = {
            'Chơi lại': '#4CAF50',
            'Trang chủ': '#2196F3',
            'Thoát': '#f44336'
        }
        if entering:
            button.config(bg='#666666')
        else:
            button.config(bg=original_colors[button.cget('text')])

    def run(self):
        self.window.mainloop()

class GameModeSelector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cờ Ca-rô")
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        self.center_window(self.window, 300, 400)
        self.selected_mode = None
        
        title_label = tk.Label(self.window, text="Cờ Ca-rô",
                             font=('Arial', 24, 'bold'),
                             bg='#f0f0f0', fg='#333333')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.window, text="Chọn chế độ chơi",
                                font=('Arial', 16),
                                bg='#f0f0f0', fg='#666666')
        subtitle_label.pack(pady=10)
        
        modes = [("3x3 (3 ô)", "#4CAF50"),
                ("9x9 (5 ô)", "#2196F3")]
        
        for mode, color in modes:
            btn = tk.Button(self.window, text=mode,
                          font=('Arial', 14),
                          width=15, height=2,
                          bg=color, fg='white',
                          command=lambda m=mode: self.select_mode(m))
            btn.pack(pady=10)
            
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#666666'))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def select_mode(self, mode):
        self.selected_mode = "3x3" if "3x3" in mode else "9x9"
        self.window.destroy()
    
    def get_mode(self):
        self.window.mainloop()
        return self.selected_mode

class GomokuGame:
    def __init__(self, difficulty):
        self.window = tk.Tk()
        self.window.title("Cờ Ca-rô 9x9")
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(False, False)
        
        # Căn giữa cửa sổ với kích thước lớn hơn cho bàn 9x9
        window_width = 800
        window_height = 900
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.game_logic = GomokuLogic()
        self.ai_player = GomokuAI()
        self.current_player = 'X'
        self.difficulty = difficulty
        
        difficulty_map = {
            "Easy": "Dễ",
            "Medium": "Trung bình",
            "Hard": "Khó"
        }
        
        # Game info frame
        self.info_frame = tk.Frame(self.window, bg='#f0f0f0', height=50)
        self.info_frame.pack(pady=10)
        
        # Turn indicator frame
        self.turn_frame = tk.Frame(self.window, bg='#f0f0f0', height=40)
        self.turn_frame.pack(pady=5)
        
        self.difficulty_label = tk.Label(self.info_frame,
                                       text=f"Độ khó: {difficulty_map[difficulty]}",
                                       font=('Arial', 12),
                                       bg='#f0f0f0')
        self.difficulty_label.pack()
        
        self.turn_indicator = tk.Label(self.turn_frame,
                                     text="Đến lượt người chơi (X)",
                                     font=('Arial', 14, 'bold'),
                                     bg='#f0f0f0', fg='#333333')
        self.turn_indicator.pack()
        
        # Game board frame
        self.game_frame = tk.Frame(self.window, bg='#666666')
        self.game_frame.pack(padx=10, pady=10)
        
        # Tạo bàn cờ 9x9
        button_size = 60  # Kích thước nhỏ hơn cho bàn 9x9
        self.buttons = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                frame = tk.Frame(self.game_frame, width=button_size, height=button_size)
                frame.grid(row=i, column=j, padx=1, pady=1)
                frame.pack_propagate(False)
                
                self.buttons[i][j] = tk.Button(frame,
                                             text='',
                                             font=('Arial', 16, 'bold'),
                                             bg='white',
                                             command=lambda row=i, col=j: self.make_move(row, col))
                self.buttons[i][j].pack(expand=True, fill='both')
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.window, bg='#f0f0f0', height=50)
        self.control_frame.pack(pady=10)
        
        button_frame = tk.Frame(self.control_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        button_style = {
            'font': ('Arial', 12),
            'width': 12,
            'height': 2,
            'relief': tk.RAISED,
            'borderwidth': 2
        }
        
        self.reset_button = tk.Button(button_frame,
                                    text="Chơi lại",
                                    bg='#4CAF50', fg='white',
                                    command=self.reset_game,
                                    **button_style)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.home_button = tk.Button(button_frame,
                                   text="Trang chủ",
                                   bg='#2196F3', fg='white',
                                   command=self.return_home,
                                   **button_style)
        self.home_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = tk.Button(button_frame,
                                   text="Thoát",
                                   bg='#f44336', fg='white',
                                   command=self.window.destroy,
                                   **button_style)
        self.quit_button.pack(side=tk.LEFT, padx=5)
        
        for button in [self.reset_button, self.home_button, self.quit_button]:
            button.bind('<Enter>', lambda e, b=button: self.on_button_hover(b, True))
            button.bind('<Leave>', lambda e, b=button: self.on_button_hover(b, False))

    def return_home(self):
        self.window.destroy()
        mode_selector = GameModeSelector()
        selected_mode = mode_selector.get_mode()
        if selected_mode:
            difficulty_selector = DifficultySelector()
            selected_difficulty = difficulty_selector.get_difficulty()
            if selected_difficulty:
                if selected_mode == "3x3":
                    game = TicTacToe(selected_difficulty)
                else:
                    game = GomokuGame(selected_difficulty)
                game.run()

    def make_move(self, row, col):
        if self.game_logic.make_move(row, col, self.current_player):
            self.buttons[row][col].config(text=self.current_player,
                                        fg='#333333' if self.current_player == 'X' else '#f44336')
            
            if self.game_logic.check_winner(self.current_player):
                winner = "Bạn" if self.current_player == 'X' else "Máy"
                messagebox.showinfo("Kết thúc", f"{winner} thắng!")
                self.reset_game()
                return
            
            if self.game_logic.is_board_full():
                messagebox.showinfo("Kết thúc", "Hòa!")
                self.reset_game()
                return
            
            self.current_player = 'O'
            self.turn_indicator.config(text="Đến lượt máy tính (O)", fg='#f44336')
            
            # Vô hiệu hóa các nút khi máy đang suy nghĩ
            for i in range(9):
                for j in range(9):
                    self.buttons[i][j].config(state='disabled')
            
            self.window.after(500, self.make_computer_move)

    def make_computer_move(self):
        if self.difficulty == "Easy":
            row, col = self.ai_player.get_easy_move(self.game_logic.board)
        elif self.difficulty == "Medium":
            if random.random() < 0.7:
                row, col = self.ai_player.get_best_move(self.game_logic.board)
            else:
                row, col = self.ai_player.get_easy_move(self.game_logic.board)
        else:  # Hard
            row, col = self.ai_player.get_best_move(self.game_logic.board)
        
        if row is not None and col is not None:
            self.game_logic.make_move(row, col, self.current_player)
            self.buttons[row][col].config(text=self.current_player,
                                        fg='#333333' if self.current_player == 'X' else '#f44336')
            
            if self.game_logic.check_winner(self.current_player):
                messagebox.showinfo("Kết thúc", "Máy thắng!")
                self.reset_game()
                return
            
            if self.game_logic.is_board_full():
                messagebox.showinfo("Kết thúc", "Hòa!")
                self.reset_game()
                return
            
            self.current_player = 'X'
            self.turn_indicator.config(text="Đến lượt người chơi (X)", fg='#333333')
            
            # Kích hoạt lại các nút sau khi máy đã đi
            for i in range(9):
                for j in range(9):
                    if self.game_logic.board[i][j] == '':
                        self.buttons[i][j].config(state='normal')

    def reset_game(self):
        self.game_logic.reset()
        self.current_player = 'X'
        self.turn_indicator.config(text="Đến lượt người chơi (X)", fg='#333333')
        for i in range(9):
            for j in range(9):
                self.buttons[i][j].config(text='', state='normal')

    def on_button_hover(self, button, entering):
        original_colors = {
            'Chơi lại': '#4CAF50',
            'Trang chủ': '#2196F3',
            'Thoát': '#f44336'
        }
        if entering:
            button.config(bg='#666666')
        else:
            button.config(bg=original_colors[button.cget('text')])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    mode_selector = GameModeSelector()
    selected_mode = mode_selector.get_mode()
    
    if selected_mode:
        difficulty_selector = DifficultySelector()
        selected_difficulty = difficulty_selector.get_difficulty()
        
        if selected_difficulty:
            if selected_mode == "3x3":
                game = TicTacToe(selected_difficulty)
            else:
                game = GomokuGame(selected_difficulty)
            game.run()
