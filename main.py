import tkinter as tk
from tkinter import messagebox
from game_logic import TicTacToeLogic 
from ai_player import AIPlayer
from gomoku_logic import GomokuLogic
from gomoku_ai import GomokuAI

# Lớp cơ bản để tạo cửa sổ giao diện
class BaseWindow:
    def __init__(self, title, size):
        # Khởi tạo cửa sổ chính
        self.window = tk.Tk()
        self.window.title(title)
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        # Căn giữa cửa sổ trên màn hình
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws - size[0]) // 2
        y = (hs - size[1]) // 2
        self.window.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

# Lớp cơ bản để tạo cửa sổ trò chơi với nút điều khiển
class BaseGameWindow(BaseWindow):
    def __init__(self, title, size, btn_size):
        super().__init__(title, size)
        
        # Tạo khung hiển thị thông tin trò chơi
        self.info_frame = tk.Frame(self.window, bg='#f0f0f0')
        self.info_frame.pack(pady=10)
        self.turn_frame = tk.Frame(self.window, bg='#f0f0f0') 
        self.turn_frame.pack(pady=5)
        
        # Tạo khung chứa các nút điều khiển
        btn_style = {'font':('Arial',12), 'width':12, 'height':2}
        ctrl_frame = tk.Frame(self.window, bg='#f0f0f0')
        ctrl_frame.pack(pady=10)
        
        # Màu sắc cho các nút điều khiển
        self.colors = {'Chơi lại':'#4CAF50', 'Trang chủ':'#2196F3', 'Thoát':'#f44336'}
        
        # Tạo và thêm các nút điều khiển vào giao diện
        for text, color in self.colors.items():
            btn = tk.Button(ctrl_frame, text=text, bg=color, fg='white', 
                          command=self.get_command(text), **btn_style)
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hiệu ứng thay đổi màu khi di chuột qua nút
            btn.bind('<Enter>', lambda e,b=btn: b.configure(bg='#666666'))
            btn.bind('<Leave>', lambda e,b=btn,c=color: b.configure(bg=c))
            
    # Phương thức lấy lệnh phù hợp cho từng nút
    def get_command(self, text):
        commands = {
            'Chơi lại': self.reset_game,
            'Trang chủ': self.return_home,
            'Thoát': self.window.destroy
        }
        return commands[text]

# Lớp hiển thị màn hình chọn chế độ
class SelectorWindow(BaseWindow):
    def __init__(self, title, options):
        super().__init__(title, (300, 400))
        
        # Thêm tiêu đề và chỉ dẫn vào cửa sổ
        tk.Label(self.window, text="Cờ Ca-rô", font=('Arial',24,'bold'),
                bg='#f0f0f0').pack(pady=20)
        tk.Label(self.window, text=title, font=('Arial',16),
                bg='#f0f0f0').pack(pady=10)
        
        self.selected = None  # Lưu lựa chọn của người dùng
        # Tạo các nút tùy chọn
        for text, color in options:
            btn = tk.Button(self.window, text=text, bg=color, fg='white',
                          font=('Arial',14), width=15, height=2,
                          command=lambda t=text: self.select(t))
            btn.pack(pady=10)
            
            # Hiệu ứng thay đổi màu khi di chuột qua nút
            btn.bind('<Enter>', lambda e,b=btn: b.configure(bg='#666666'))
            btn.bind('<Leave>', lambda e,b=btn,c=color: b.configure(bg=c))
    
    # Phương thức lưu lựa chọn và đóng cửa sổ
    def select(self, choice):
        self.selected = choice
        self.window.destroy()
        
    # Lấy giá trị lựa chọn của người dùng
    def get_selection(self):
        self.window.mainloop()
        return self.selected

# Lớp chính để tạo bàn cờ và quản lý trò chơi
class GameBoard(BaseGameWindow):
    def __init__(self, size, difficulty):
        # Điều chỉnh kích thước cửa sổ dựa trên kích thước bàn cờ
        window_size = (400, 450) if size == 3 else (600, 650)
        super().__init__("Cờ Ca-rô", window_size, 80 if size == 3 else 60)
        
        self.size = size  # Kích thước bàn cờ
        # Chọn logic trò chơi và AI phù hợp
        self.game_logic = TicTacToeLogic() if size == 3 else GomokuLogic()
        self.ai = AIPlayer() if size == 3 else GomokuAI()
        self.difficulty = difficulty  # Độ khó
        self.current_player = 'X'  # Người chơi đầu tiên
        
        # Hiển thị độ khó và lượt chơi
        tk.Label(self.info_frame, text=f"Độ khó: {difficulty}", 
                font=('Arial',12), bg='#f0f0f0').pack()
        self.turn_label = tk.Label(self.turn_frame, text="Lượt: X",
                                 font=('Arial',14,'bold'), bg='#f0f0f0')
        self.turn_label.pack()
        
        # Tạo khung chứa bàn cờ
        game_frame = tk.Frame(self.window, bg='#666666')
        game_frame.pack(padx=10, pady=10)
        
        # Tạo các nút đại diện cho ô cờ
        self.buttons = []
        for i in range(size):
            row = []
            for j in range(size):
                btn = tk.Button(game_frame, font=('Arial',24 if size == 3 else 16,'bold'),
                              width=3, height=1, command=lambda x=i,y=j: self.make_move(x,y))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
            
    # Xử lý nước đi của người chơi
    def make_move(self, row, col):
        # Kiểm tra nước đi hợp lệ
        if self.buttons[row][col]['text'] != '' or not self.game_logic.make_move(row, col, self.current_player):
            return
        self.buttons[row][col].config(text=self.current_player)
        
        # Kiểm tra nếu trò chơi kết thúc
        if self.check_game_end(self.current_player):
            return
        
        # Chuyển lượt chơi
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.turn_label.config(text=f"Lượt: {self.current_player}")
        
        # Xử lý lượt chơi của AI nếu cần
        if self.current_player == 'O':
            self.disable_board()
            self.window.after(500, lambda: self.computer_move())
        else:
            self.enable_board()
            
    # Xử lý lượt chơi của AI
    def computer_move(self):
        # Lấy nước đi dựa trên độ khó
        if self.difficulty == "Easy":
            move = self.ai.get_easy_move(self.game_logic.board)
        else:
            move = self.ai.get_best_move(self.game_logic.board)
            
        if move:
            row, col = move
            self.game_logic.make_move(row, col, 'O')
            self.buttons[row][col].config(text='O')
            
        if not self.check_game_end('O'):
            self.current_player = 'X'
            self.turn_label.config(text=f"Lượt: {self.current_player}")
            self.enable_board()
    #kiểm tra trò chơi kết thúc
    def check_game_end(self, player):
        if self.game_logic.check_winner(player):
            winner = "Bạn" if player == 'X' else "Máy" 
            messagebox.showinfo("Kết thúc", f"{winner} thắng!")
            self.reset_game()
            return True
        if self.game_logic.is_board_full():
            messagebox.showinfo("Kết thúc", "Hòa!")
            self.reset_game()
            return True
        return False
    #reset trò chơi
    def reset_game(self):
        self.game_logic.reset()
        self.current_player = 'X'
        for row in self.buttons:
            for btn in row:
                btn.config(text='', state='normal')
    #Làm cho bàn cờ không thể ấn được
    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')          
    #Làm cho bàn cờ có thể ấn được          
    def enable_board(self):
        for row in self.buttons:
            for btn in row:
                if btn['text'] == '':
                    btn.config(state='normal')
    #quay trở lại màn hình start game               
    def return_home(self):
        self.window.destroy()
        start_game()
    #khởi chạy vòng lặp chính của cửa sổ làm cho cửa sổ hiển thị liên tục
    def run(self):
        self.window.mainloop()

def start_game():
    # Chọn chế độ chơi
    mode = SelectorWindow("Chọn chế độ chơi", 
                         [("3x3 (3 ô)", "#4CAF50"),
                          ("9x9 (5 ô)", "#2196F3")]).get_selection()
    if mode:
        # Chọn độ khó
        difficulty = SelectorWindow("Chọn độ khó",
                                  [("Dễ", "#4CAF50"),
                                   ("Trung bình", "#FFA500"),
                                   ("Khó", "#f44336")]).get_selection()
        if difficulty:
            # Bắt đầu trò chơi
            size = 3 if "3x3" in mode else 9
            game = GameBoard(size, difficulty)
            game.run()
#khởi chạy trò chơi
start_game()