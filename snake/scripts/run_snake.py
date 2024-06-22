from tkinter import *
from tkinter import ttk
from snake.devtools import game_logic, game_gui

def main():
    root = Tk()
    logic = game_logic.GameLogic()
    game_gui.GameGUI(root, logic)
    root.mainloop() 
 
if __name__ == "__main__":
    main()
