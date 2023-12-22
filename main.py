from tkinter import *
import tkinter as tk

import game_board
import main_window_menu
from game_board import *


main_window = tk.Tk()

main_greeting = tk.Label(main_window, text='Welcome to Millennial Minesweeper')
main_greeting.grid(row=0, column=0)

main_window_rules_button = tk.Button(main_window, text='View Rules', command=main_window_menu.view_rules)
main_window_rules_button.grid(row=1, column=0)

main_window_start_button = tk.Button(main_window, text='Start Game', command=lambda: game_board.game_start(main_window))
main_window_start_button.grid(row=2, column=0)

main_window_exit_button = tk.Button(main_window, text="Close", command=main_window.quit)
main_window_exit_button.grid(row=3, column=0)

main_window.mainloop()
