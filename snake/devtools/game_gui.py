from tkinter import *
from tkinter import ttk


class GameGUI:
    def __init__(self, parent, game_logic):
        self.parent = parent
        self.game_logic = game_logic
        self.setup_gui()

    def setup_gui(self):
        # Title and icon
        self.parent.title('Snake')
        self.parent.iconbitmap(default='../icons/snake_icon3.ico')

        # Game controlls
        self.parent.bind('<Up>', lambda e: self.game_logic.set_new_direction('Up'))
        self.parent.bind('<Down>', lambda e: self.game_logic.set_new_direction('Down'))
        self.parent.bind('<Left>', lambda e: self.game_logic.set_new_direction('Left'))
        self.parent.bind('<Right>', lambda e: self.game_logic.set_new_direction('Right'))

        # Setup game board, snake and fruit
        self.board_frame = ttk.Frame(self.parent)
        self.board_frame.grid()
        self.game_speed = self.game_logic.game_speed # milliseconds per update
        self.bg_color = '#012409'
        self.snake_color = '#12db41'
        self.fruit_color = '#cf8217'
        self.dead_snake_color = '#f02222'
        self.board_size = self.game_logic.board_size
        self.square_size = 25

        self._create_game_window()
        
        self._draw_snake()
        self.parent.after(self.game_speed, self._move_snake)


    def _create_game_window(self):
        # Create the game board
        self.board = self._create_board(board_size=self.board_size, 
                                        square_size=self.square_size)
        # Draw the first fruit
        self._draw_fruit()

        # Create the score counter
        self.game_score = IntVar()
        ttk.Label(self.board_frame, 
                    text='game score:', 
                    padding=5, 
                    background='#061c0d', 
                    foreground='white', 
                    anchor='e'
                    ).grid(column=0, 
                            row=0, 
                            columnspan=round(self.board_size/2),
                            sticky='nswe')
        ttk.Label(self.board_frame, 
                    textvariable=self.game_score, 
                    padding=5, 
                    background='#061c0d', 
                    foreground='white', 
                    anchor='w'
                    ).grid(column=round(self.board_size/2),
                            row=0,
                            columnspan=round(self.board_size/2)-1,
                            sticky='nswe')
        
    def _create_board(self, board_size, square_size):
        board = []
        for row in range(board_size):
            board_row = []
            for col in range(board_size):
                square = Frame(self.board_frame, 
                            width=square_size, 
                            height=square_size, 
                            background=self.bg_color,
                            borderwidth=1,
                            relief='groove')
                square.grid(column=col, row=row+1) # first row is for text
                board_row.append(square)
            board.append(board_row)
        return board

    def _draw_snake(self, alive=True):
        snakeX, snakeY = self.game_logic.get_snake_coords()

        if alive: 
            color = self.snake_color
        else: 
            color = self.dead_snake_color

        for i in range(len(snakeX)): 
            self.board[snakeY[i]][snakeX[i]].configure(background=color)

    def _move_snake(self):
        self.game_logic.move_snake()

        if self.game_logic.is_alive():
            remove_tail = not self.game_logic.check_ate_fruit()

            self._update_snake(remove_tail=remove_tail)

            if self.game_logic.check_ate_fruit():
                self._draw_fruit() # TODO kanske bara rita frukten om man ätit den
                self.game_score.set(self.game_logic.get_game_score())

            self.parent.after(self.game_speed, self._move_snake)

        else: 
            self._draw_snake(alive=False)
            self._game_lost()
        

    def _update_snake(self, remove_tail):
        snakeX, snakeY = self.game_logic.get_snake_coords()

        # Draw new snake head
        self.board[snakeY[0]][snakeX[0]].configure(background=self.snake_color)
        
        # Remove old snake tail
        if remove_tail:
            tailX, tailY = self.game_logic.get_old_tail_coords()
            self.board[tailY][tailX].configure(background=self.bg_color)

    
    def _draw_fruit(self):
        fruitX, fruitY = self.game_logic.get_fruit_coords()
        self.board[fruitY][fruitX].configure(background=self.fruit_color)

    def _game_lost(self):
        self.game_over_window = Toplevel(self.parent)
        ttk.Label(self.game_over_window, text='You lost', padding=5).grid(column=0, row=0, columnspan=4)

        ttk.Label(self.game_over_window, text='Score:', padding=5).grid(column=0, row=1, sticky='e')
        ttk.Label(self.game_over_window, text=str(self.game_score.get()), padding=5).grid(column=1, row=1, sticky='w')
        ttk.Label(self.game_over_window, text='High score:', padding=5).grid(column=2, row=1, sticky='e')

        high_score = self._get_high_score()
        ttk.Label(self.game_over_window, text=high_score, padding=5).grid(column=3, row=1, sticky='w')

        retry_btn = ttk.Button(self.game_over_window, 
                               text='Retry', 
                               padding=5, 
                               command=self._retry_button,
                               width=10)
        retry_btn.grid(column=0, row=2, columnspan=2, padx=5, sticky='e')

        exit_btn = ttk.Button(self.game_over_window, 
                              text='Exit', 
                              padding=5, 
                              command=self.parent.destroy,
                              width=10,)
        exit_btn.grid(column=2, row=2, columnspan=2, padx=5, sticky='w')
        
        self.game_over_window.grid_columnconfigure(0, weight=1)
        self.game_over_window.grid_columnconfigure(1, weight=1)
        self.game_over_window.grid_columnconfigure(2, weight=1)
        self.game_over_window.grid_columnconfigure(3, weight=1)

    def _get_high_score(self):
        file_path = '../settings/high_score.txt'
        with open(file_path, 'r') as file:
            high_score = file.read()
        if self.game_score.get() > int(high_score):
            high_score = str(self.game_score.get())
            with open(file_path, 'w') as file:
                file.write(high_score)
        return high_score


    def _retry_button(self):
        self.game_over_window.destroy()
        self.board_frame.destroy()
        self.game_logic.setup_game()
        self.setup_gui()



