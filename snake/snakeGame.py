from tkinter import *
from tkinter import ttk
import random
import game_over


def __main__():
    root = Tk()
    Board(root, 20)
    root.mainloop()

class Board:
    def __init__(self, root, size: int):
        self.parent = root
        
        # Title and icon
        self.parent.title('Snake')
        self.parent.iconbitmap(default='snake_icon3.ico')


        self.board_frame = ttk.Frame(self.parent)
        self.board_frame.grid()
        self.game_speed = 200 # milliseconds per update
        self.bg_color = '#012409'
        self.snake_color = '#12db41'
        self.fruit_color = '#cf8217'
        self.board_size = 11
        self.square_size = 25

        self.snakeX = [2,2,2]           # Snake x-coords
        self.snakeY = [-1,-1,-1]        # Snake y-coords
        self.direction = 'Down'         # Start direction
        self.vertical_direction = 1      # Start going down
        self.horisontal_direction = 0    # Not moving horisontally
        
        self.fruitX = random.randint(0, self.board_size-1)
        self.fruitY = random.randint(0, self.board_size-1)

        self.create_game_window()
        
        self.draw_snake()
        self.parent.after(self.game_speed, self.move_snake)
        
        root.bind('<Up>', lambda e: setattr(self, 'direction', 'Up'))
        root.bind('<Down>', lambda e: setattr(self, 'direction', 'Down'))
        root.bind('<Left>', lambda e: setattr(self, 'direction', 'Left'))
        root.bind('<Right>', lambda e: setattr(self, 'direction', 'Right'))


    def create_game_window(self):
        # Create the game board
        self.board = self.create_board(board_size=self.board_size, 
                                      square_size=self.square_size)
        # Draw the first fruit
        self.board[self.fruitY][self.fruitX].configure(background=self.fruit_color)

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
        

    def create_board(self, board_size, square_size):
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
    

    def draw_snake(self):
        for i in range(0, len(self.snakeX)):
            self.board[self.snakeY[i]][self.snakeX[i]].configure(background=self.snake_color)
    

    def move_snake(self):
        # get new direction and head location
        self.set_directions()
        newY = self.snakeY[0] + self.vertical_direction
        newX = self.snakeX[0] + self.horisontal_direction

        # Check if new position is valid
        validPosition = self.check_valid_position(newY, newX)

        # Check if eaten fruit
        ateFruit = self.check_fruit(newY, newX)

        # Draw new head and add to list
        if validPosition:
            self.snakeY.insert(0, newY)
            self.snakeX.insert(0, newX)

            self.board[self.snakeY[0]][self.snakeX[0]].configure(background=self.snake_color)
            if not ateFruit:
                # Remove tail of snake if valid position
                self.board[self.snakeY[-1]][self.snakeX[-1]].configure(background=self.bg_color)
                self.snakeY.pop()
                self.snakeX.pop()

            # Move again
            self.parent.after(self.game_speed, self.move_snake)
        else:
            self.game_lost()
            print('text')


    def set_directions(self): # TODO controlls are still a bit slow to update. Should have this check when pressing buttons instead
        """Sets direction of snake. Snake is not allowed to turn 180 degrees and
            if the player tries, nothing will happen.
            
            Return:
                Tuple[verticalDirection (int), horisontalDirection (int)]
        """
        match self.direction:
            case 'Up':
                if self.vertical_direction != 1:
                    self.vertical_direction = -1
                    self.horisontal_direction = 0
            case 'Down': 
                if self.vertical_direction != -1:
                    self.vertical_direction = 1
                    self.horisontal_direction = 0
            case 'Left':
                if self.horisontal_direction != 1:
                    self.horisontal_direction = -1
                    self.vertical_direction = 0
            case 'Right':
                if self.horisontal_direction != -1:
                    self.horisontal_direction = 1
                    self.vertical_direction = 0


    def game_lost(self):
        for i in range(0, len(self.snakeX)):
            self.board[self.snakeY[i]][self.snakeX[i]].configure(background='#f02222')
        game_over.GameOverScreen(self.parent)



    def check_valid_position(self, newY, newX):
        # Snake is not allowed outside of game board
        if newY >= self.board_size or newX >= self.board_size or newY < 0 or newX < 0:
            return False
        
        # Snake is not allowed to overlap with itself
        for i in range(len(self.snakeX)):
            if newX == self.snakeX[i] and newY == self.snakeY[i]:
                return False
        return True


    def check_fruit(self, newY, newX):
        if newY == self.fruitY and newX == self.fruitX:
            self.game_score.set(self.game_score.get() + 1)

            # New Fruit is not allowed to be created inside the snake
            make_fruit = True
            while make_fruit:
                self.fruitX = random.randint(0, self.board_size-1)
                self.fruitY = random.randint(0, self.board_size-1)
                make_fruit = False
                for i in range(len(self.snakeX)):
                    if self.fruitX == self.snakeX[i] and self.fruitY == self.snakeY[i]:
                        make_fruit = True
            self.board[self.fruitY][self.fruitX].configure(background=self.fruit_color)
            return True
        return False

__main__()
