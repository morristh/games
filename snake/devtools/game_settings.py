from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from snake.devtools import game_logic, game_gui
import json


def main():
    root = Tk()
    GameSettings(root)
    root.mainloop()

class GameSettings:
    def __init__(self, parent):

        self.parent = parent

        self.parent = Toplevel()

        # Title and icon
        self.parent.title('Settings')
        self.parent.iconbitmap(default='../icons/snake_icon3.ico')


        # settings variables
        self.snake_color = 'green'
        self.snake_speed = IntVar()


        # Speed settings
        ttk.Label(self.parent, text='Snake speed').grid(row=1, column=1)

        ttk.Label(self.parent, textvariable=self.snake_speed).grid(row=1, column=5)
        s = ttk.Scale(self.parent, orient=HORIZONTAL, variable=self.snake_speed, length=100, from_=50, to=1000)
        s.grid(row=1, column=2, columnspan=3)
        s.set(200)

        ttk.Button(self.parent, text='set', command=self.update_speed).grid(row=1, column=6)


        # Snake color settings
        ttk.Label(self.parent, text='Snake color').grid(row=2, column=1)

        green_btn = Button(self.parent, command=lambda : self.color_btn('green'),
                           background='green', height=1, width=2)
        green_btn.grid(row=2, column=2)

        blue_btn = Button(self.parent, command=lambda : self.color_btn('blue'),
                          background='blue', height=1, width=2)
        blue_btn.grid(row=2, column=3)
        
        red_btn = Button(self.parent, command=lambda : self.color_btn('red'),
                         background='red', height=1, width=2)
        red_btn.grid(row=2, column=4)


        # Save and close
        ttk.Button(self.parent, text='Save', command=self.save_btn).grid(row=3, column=5)
        ttk.Button(self.parent, text='Close', command=self.parent.destroy).grid(row=3, column=6)


        for child in self.parent.winfo_children():
            child.grid_configure(padx=25, pady=35)

        # with open('../settings/settings.json', 'r+') as file:
        #     data = json.load(file)
        #     data['speed'] = 100
        #     file.seek(0)
        #     json.dump(data, file, indent=4)
        #     file.truncate()
    
    def update_speed(self):
        print(f'speed set to: {self.snake_speed.get()}')

        with open('../settings/settings.json', 'r+') as file:
            data = json.load(file)
            print(f'old speed was: {data["speed"]}')
            data['speed'] = self.snake_speed.get()
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def color_btn(self, color: str):
        print(color)
        self.snake_color = color

    def save_btn(self):
        with open('../settings/settings.json', 'r+') as file:
            data = json.load(file)
            data['speed'] = self.snake_speed.get()
            data['snake_color'] = self.snake_color
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

if __name__ == '__main__':
    main()
