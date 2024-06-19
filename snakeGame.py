from tkinter import *
from tkinter import ttk

class Board:
    def __init__(self, root, size: int):
        self.parent = root
        self.boardFrame = ttk.Frame(self.parent).grid()
        self.snakeColor = '#12db41'
        self.bgColor = '#012409'
        self.snakeX = [1,1,1]
        self.snakeY = [1,2,3]
        self.boardSize = 10
        self.squareSize = 25
        self.board = self.createBoard(board_size=self.boardSize, 
                                      square_size=self.squareSize)
        self.drawSnake()
        self.parent.after(1000, self.moveSnake)
        

    def createBoard(self, board_size, square_size):
        board = []
        for row in range(board_size):
            board_row = []
            for col in range(board_size):
                square = Frame(self.boardFrame, 
                               width=square_size, 
                               height=square_size, 
                               background=self.bgColor,
                               borderwidth=1,
                               relief='groove')
                square.grid(column=col, row=row)
                board_row.append(square)
            board.append(board_row)
        return board
    
    def drawSnake(self, status='alive'):
        if status == 'alive': 
            color=self.snakeColor
        else:
            color= '#f02222'
        for i in range(1, len(self.snakeX)):
            self.board[self.snakeY[i]][self.snakeX[i]].configure(background=color)
    
    def moveSnake(self):

        # Move snake
        newY = self.snakeY[0] + 0
        self.snakeY.insert(0, newY)
        newX = self.snakeX[0] + 1
        self.snakeX.insert(0, newX)

        # Check if new position is valid
        validPosition = True
        if self.snakeY[0] >= self.boardSize or self.snakeX[0] >= self.boardSize or self.snakeY[0] < 0 or self.snakeX[0] < 0:
            validPosition = False

        # Draw new head
        if validPosition:
            self.board[self.snakeY[0]][self.snakeX[0]].configure(background=self.snakeColor)

            # Remove tail of snake if valid position
            self.board[self.snakeY[-1]][self.snakeX[-1]].configure(background=self.bgColor)
            self.snakeY.pop()
            self.snakeX.pop()

            # Move again
            self.parent.after(300, self.moveSnake)
        else:
            self.drawSnake('dead')



    


root = Tk()
Board(root, 20)
root.mainloop()
