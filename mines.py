import random
from itertools import count
from tkinter import messagebox
import tkinter as tk


class Mine:

    mine_count = count(1)

    def __init__(self, x_coordinate, y_coordinate):
        self.xcoordinate = x_coordinate  # column
        self.ycoordinate = y_coordinate  # row
        self.count = next(self.mine_count)  # internal count
        self.has_charge = True  # to ensure doubling back does not blow up the same mine
        self.did_damage = False # to track whether the mine did damage to the user
        self.description = 'This is a space on the game board that has a mine and will blow up your character ' \
                           'either causing damage, power down, or both.'

    def print_coordinates(self):
        print(f'The coordinates of this mine are {self.xcoordinate},{self.ycoordinate}')

    def print_count(self):
        print(f'Mine number {self.count} was created.')

    def release_charge(self):
        self.has_charge = False # Use this to disarm the bomb


def click_tile(xc, yc, mine_set, list_of_buttons, verbose=True):
    # xc is X-Coordinate of the button, yc is Y-Coordinate of the button, mine_set is the list of mines that were created, list_of_buttons are the list of game tiles on the board
    # Default set to false unless the clicked button coordinates overlap a mine coordinate
    mine_in_space = False

    # This next line of code is optional for checking what coordinates are being passed by the clicked game button
    if verbose:
        print(f"The coordinates the button is passing are:{xc}, {yc} ")

    # Checks if the passed button coordinates overlap a mine
    for mine in mine_set:
        if xc == mine.xcoordinate and yc == mine.ycoordinate:
            mine.release_charge()
            mine_in_space = True

            # After checking if the click coordinates overlap a mine button,changes the button green to indicate mine was disarmed
            for buttons in list_of_buttons:
                for mines in mine_set:
                    if buttons.grid_info()['column'] == mines.xcoordinate and buttons.grid_info()['row'] == mines.ycoordinate and not mines.has_charge and not mines.did_damage:
                        buttons.configure(bg='green')
                        print(f"This mine at {mines.xcoordinate}, {mines.ycoordinate} is disarmed")

    # Pops up a window that confirms whether an active mine was disarmed
    if mine_in_space:
        tk.messagebox("Congrats", f"Nice job! Mine Disabled at: {xc},{yc} !")
        disarm_window = tk.Toplevel()
        disarm_label = tk.Label(disarm_window, text=f"Nice job! Mine Disabled at: {xc},{yc} !", pady=10, padx=10)
        disarm_label.pack()
        disarm_button = tk.Button(disarm_window, text="Continue", pady=10, padx=10, command=disarm_window.destroy)
        disarm_button.pack()

    # Pops up a window letting the user know they clicked on a blank tile with no active mine being disarmed.
    else:
        no_mine = tk.Toplevel()
        no_mine_label = tk.Label(no_mine, text="Sorry there was no mine in this space", padx=10, pady=10)
        no_mine_label.pack()
        no_mine_button = tk.Button(no_mine, text="Close", command=no_mine.destroy)
        no_mine_button.pack()

    active_mines = 0
    for mine in mine_set:
        if mine.has_charge:
            active_mines += 1

    if active_mines == 0:
        victory_window = tk.Toplevel()
        victory_message = tk.Label(victory_window, text="You cleared all mines and Won!")
        victory_message.pack()
        victory_button = tk.Button(victory_window, text='Close', command=exit)
        victory_button.pack()


# Function to create mine tiles at random X and Y coordinates
def create_mines(mine_number):
    random.seed()
    game_mines = []
    for mine in range(0, mine_number):
        game_mines.append(Mine(random.randint(1, 10), random.randint(1, 10)))
        game_mines[mine].print_count()
        game_mines[mine].print_coordinates()

    return game_mines


def create_unique_mines(game_x, game_y, mine_number=1):
    random.seed()
    game_mines = []
    xc = []
    yc = []
    xyc = []

    for xcoor in range(0, mine_number):
        xc.append(random.randint(1, game_x))

    for ycoor in range(0, mine_number):
        yc.append(random.randint(1, game_y))

    for count in range(0, mine_number):
        while count + 1 != len(xyc):
            if [xc[count], yc[count]] not in xyc:
                xyc.append([xc[count], yc[count]])
            else:
                xc[count] = random.randint(1, game_x)
                yc[count] = random.randint(1, game_y)

    for mtc in range(0, mine_number):
        game_mines.append(Mine(xc[mtc], yc[mtc]))
        game_mines[mtc].print_count()
        game_mines[mtc].print_coordinates()


