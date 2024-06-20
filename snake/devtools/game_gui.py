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
            start = 0                   # start exists to not color frame that does not exist when snake is out of bounds
        else: 
            color = self.dead_snake_color
            start = 1

        for i in range(start, len(snakeX)): 
            self.board[snakeY[i]][snakeX[i]].configure(background=color)

    def _move_snake(self):

        self.game_logic.move_snake()

        if self.game_logic.is_alive():
            remove_tail = self.game_logic.remove_tail()

            self._update_snake(remove_tail=remove_tail)
            self._draw_fruit() # TODO kanske bara rita frukten om man ätit den

            self.parent.after(self.game_speed, self._move_snake)

        else: 
            self._draw_snake(alive=False)
            self._game_lost()
        

    def _update_snake(self, remove_tail):
        ... # TODO
    
    def _draw_fruit(self):
        fruitX, fruitY = self.game_logic.get_fruit_coords()
        self.board[fruitY][fruitX].configure(background=self.fruit_color)

    def _game_lost(self):
        ... # TODO



