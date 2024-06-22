from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from snake.devtools import game_logic, game_gui
import json


# def main():
#     root = Tk()
#     GameSettings(root)
#     root.mainloop()

class GameSettings:
    def __init__(self, parent):
        self.parent = parent

        self.speed_var = IntVar()
        self.speed_var.set('100')
        ttk.Label(self.parent, textvariable=self.speed_var).grid(row=2, column=2)

        ttk.Label(self.parent, text='Snake speed:').grid(row=0, column=2)
        s = ttk.Scale(self.parent, orient=HORIZONTAL, variable=self.speed_var, length=100, from_=50, to=1000)
        s.grid(row=1, column=2)
        s.set(300)

        ttk.Button(self.parent, text='set', command=self.update_speed).grid(row=3, column=2)

        for child in self.parent.winfo_children():
            child.grid_configure(padx=35, pady=5)

        with open('../settings/settings.json', 'r+') as file:
            data = json.load(file)
            data['speed'] = 100
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    
    def update_speed(self):
        print(f'speed set to: {self.speed_var.get()}')

        with open('../settings/settings.json', 'r+') as file:
            data = json.load(file)
            print(f'old speed was: {data["speed"]}')
            data['speed'] = self.speed_var.get()
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

# if __name__ == '__main__':
#     main()
