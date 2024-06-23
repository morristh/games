from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from snake.devtools import game_logic, game_gui, game_settings


def main():
    root = Tk()
    GameMenu(root)
    root.mainloop()

class GameMenu:
    def __init__(self, parent):
        self.parent = parent

        # Title and icon
        self.parent.title('Snake')
        self.parent.iconbitmap(default='../icons/snake_icon3.ico')
  
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.grid(column=0, row=0, sticky='nwes')

        # Title and image
        # title_frame = ttk.Frame(main_frame).grid(row=1, column=1)

        ttk.Label(self.main_frame, 
                  text='Snake', 
                  font=('Arial', 50), 
                  foreground='green',
                  padding=(0,10,10,35)
                  ).grid(row=0, column=3, sticky='se')

        my_img = Image.open("../icons/snake_icon3.png")
        my_img = my_img.resize((64,64))
        logoImage = ImageTk.PhotoImage(my_img)
        logoLabel =  ttk.Label(self.main_frame, 
                               image = logoImage, 
                               padding=(0,10,20,35))
        logoLabel.image = logoImage # Stop garbage collector from deleting image
        logoLabel.grid(row=0, column=2)

        # Buttons
        # btn_frame = ttk.Frame(main_frame).grid(row=2, column=1)
        ttk.Button(self.main_frame, 
                   text='Start',
                   command=self._start_btn, 
                   width=15).grid(row=1, column=2, sticky='se')
        
        ttk.Button(self.main_frame, 
                   text='Settings',
                   command=self._settings_btn,
                   width=15).grid(row=1, column=3, sticky='se')
        
        ttk.Button(self.main_frame, 
                   text='Quit',
                   command=self.parent.destroy,
                   width=15).grid(row=1, column=4, sticky='se')
        
        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def _start_btn(self):
        # root = Tk()
        self.main_frame.destroy()
        logic = game_logic.GameLogic()
        game_gui.GameGUI(self.parent, logic)
        # root.mainloop() 

    def _settings_btn(self):

        # settings = Toplevel(self.parent, background='gray').grid()
        game_settings.GameSettings(self.parent)

if __name__ == '__main__':
    main()
