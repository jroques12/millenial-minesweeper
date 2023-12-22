from tkinter import *
import tkinter as tk


def view_rules():
    rules_window = tk.Tk()
    rules_window.title(string='Rules')
    rules_text = tk.Label(rules_window, text="Welcome to Millennial Minesweeper. You may be familiar with the older \n"
                                             "version of Minesweeper if you grew up with computers before the internet.\n"
                                             "In the old version you could choose any square you wish, much like it was\n"
                                             "back in our parents time. However as a Millenial, we can only move one\n"
                                             "square at a time and only select adjacent squares to progress. As times\n"
                                             "have gotten harder so has the game and the view you get for not blowing\n"
                                             "yourself up on a tile is reduced. Time to pull yourself up by your bootstraps\n"
                                             "and best of luck not blowing yourself up!", padx=20, pady=20)
    rules_text.pack(padx=30, pady=20)

    rules_close_button = tk.Button(rules_window, text="Close", command=rules_window.destroy, padx=5, pady=10)
    rules_close_button.pack()

    rules_window.mainloop()
