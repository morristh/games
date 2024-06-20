from tkinter import *
from tkinter import ttk
from devtools.snakeGame import SnakeGame


def __main__():
    root = Tk()
    SnakeGame(root, 20)
    root.mainloop()


__main__()