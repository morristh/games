from tkinter import *
from tkinter import ttk

class GameOverScreen:
    def __init__(self, parent):
        self.parent = parent
        self.game_over_window = Toplevel(parent)
        ttk.Label(self.game_over_window, text='You lost', padding=5).grid(column=0, row=0, columnspan=2)

        retry_btn = ttk.Button(self.game_over_window, text='Retry', padding=5, command=self._retry_button)
        retry_btn.grid(column=0, row=1)

        exit_btn = ttk.Button(self.game_over_window, text='Exit', padding=5, command=self._exit_button)
        exit_btn.grid(column=1, row=1)
        exit_btn.bind('<Return>', self._exit_button)

    def _exit_button(self):
        self.parent.destroy()

    def _retry_button(self):
        self.game_over_window.destroy()
        # TODO Retry button does not work yet