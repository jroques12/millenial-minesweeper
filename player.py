import random
from tkinter import messagebox
from tkinter import Frame
from tkinter import Button
from tkinter import Label
import tkinter as tk


class GameBoard(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.num_of_rows = 10
        self.num_of_columns = 10
        self.game_piece_list = []
        self.mine_list = []
        self.tile_list = []
        self.tile_count = 0

    def set_up_board(self, verbose=True):
        # first need to set up the mines by determining their coordinates. Will use randomization. Will set up the coordinates for 10 mines.

        random.seed()
        mine_coordinate_list = []

        while len(mine_coordinate_list) < 5:

            temp_x_coordinate = random.randint(1, 10)
            temp_y_coordinate = random.randint(1, 10)

            if not [temp_x_coordinate, temp_y_coordinate] in mine_coordinate_list and [temp_x_coordinate, temp_y_coordinate] != [1, 1]:
                mine_coordinate_list.append([temp_x_coordinate, temp_y_coordinate])
                if verbose:
                    print(f"New mine created at {temp_x_coordinate}, {temp_y_coordinate}")

        for coordinate in mine_coordinate_list:
            self.mine_list.append(Mine(coordinate[0], coordinate[1], self))

        for row in range(1, self.num_of_rows+1):
            for column in range(1, self.num_of_columns+1):
                is_mine = False
                for mine in self.mine_list:
                    if [row, column] == [mine.x_coordinate, mine.y_coordinate]:
                        mine.grid(row=row, column=column)
                        self.game_piece_list.append(mine)
                        is_mine = True

                if not is_mine:
                    self.game_piece_list.append(Tile(row, column, self))
                    self.tile_list.append(self.game_piece_list[-1])
                    self.game_piece_list[-1].grid(row=row, column=column)

        # Determine Proximity to other mines and change tile color to orange if it borders a mine.
        for tile in self.tile_list:
            for mine in self.mine_list:
                if abs(tile.x_coordinate - mine.x_coordinate) <= 1 and abs(tile.y_coordinate - mine.y_coordinate) <= 1:
                    tile.color = 'orange'

    def reveal_all_mines(self, verbose=True):
        for mine in self.mine_list:
            mine.reveal_color()
            if verbose:
                print(f"Mine revealed at location {mine.x_coordinate}, {mine.y_coordinate}!")

    def reveal_tile(self, player):
        all_tiles_visited = True

        for tile in self.game_piece_list:

            if [player.x_coordinate, player.y_coordinate] == [tile.x_coordinate, tile.y_coordinate]:
                tile.reveal_color()
                tile.is_visited = True
                if isinstance(tile, Mine):
                    tile.detonate(player, self)

                if tile.color == 'orange':
                    player.score_board.hp_label.configure(background='orange')

                elif tile.color == 'green':
                    player.score_board.hp_label.configure(background=tile.default_color)

        for tile in self.tile_list:

            if tile.is_visited:
                pass
            else:
                all_tiles_visited = False

        if all_tiles_visited:
            player.disabled = True
            messagebox.showinfo("You Won!", "You have visited all tiles!\nYou Win!\nPress Esc to exit.")

    def reveal_all_tiles(self):
        for tile in self.game_piece_list:
            print(tile)
            tile.reveal_color()


class Tile(tk.Button):
    def __init__(self, x_coordinate, y_coordinate, window):
        Button.__init__(self, window)
        self.default_color = self.cget('bg')
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.is_visited = False
        self.color = 'green'
        self.description = "This is a tile on the game board. It has an x-coordinate(x_coordinate),\n" \
                           "a y-coordinate(y_coordinate), and a color.\n" \
                           "Blue means no mines in the adjacent tiles\n" \
                           "Yellow means there is a mine in one of the adjacent tiles.\n" \
                           "Red means you have landed on a mine and possibly lost HP.\n"
        self.bind("<Enter>", func=lambda e: self.configure(activebackground=self.cget('bg')))

    def reveal_color(self):
        self.configure(background=self.color)


class Mine(Tile):
    def __init__(self, x_coordinate, y_coordinate, game_board):
        Tile.__init__(self, x_coordinate=x_coordinate, y_coordinate=y_coordinate, window=game_board)
        # Purpose of has_charge is to ensure that a mine only damages the player the first time they go over the mine.
        self.has_charge = True
        # Not yet going to utilize the did_damage variable but want a way to track it regardless.
        self.did_damage = False
        self.color = "red"

    def detonate(self, player_obj, game_board, verbose=True):
        player_obj.score_board.hp_label.configure(background='red')
        if self.has_charge:
            self.has_charge = False
            player_obj.hp -= 1
            self.reveal_color()
            self.did_damage = True
            if player_obj.hp <= 0:
                player_obj.configure(background='black')
                player_obj.lost(gb=game_board)
            if verbose:
                print(f"Player has {player_obj.hp} HP left!")


class Player(Tile):
    def __init__(self, x_coordinate, y_coordinate, gb, outer_layer):
        Tile.__init__(self, x_coordinate=x_coordinate, y_coordinate=y_coordinate, window=gb)
        self.player_name = "Scrantonius"
        self.hp = 3
        self.color = 'blue'
        self.configure(background=self.color)
        self.tile_count = 0
        self.disabled = False
        self.owner = "None"
        self.score_board = ScoreBoard(outer_layer, self)

    # the move_player function is the bread and butter of the whole game, it handles all the updates for the GUI info such
    # as HP remaining, adjacent mines, number of tiles converted, etc. Additionally, the trail functionality is partially
    # linked here as well as the GameBoard class.

    def move_player(self, direction, gb):
        if self.disabled:
            return
        if direction == 'down':
            if self.grid_info()['row'] >= 10:
                self.x_coordinate = self.grid_info()['row']

            else:
                self.grid(row=self.grid_info()['row']+1)
                self.x_coordinate = self.grid_info()['row']
                gb.reveal_tile(player=self)

        if direction == 'up':
            if self.grid_info()['row'] <= 1:
                self.x_coordinate = self.grid_info()['row']
                pass
            else:
                self.grid(row=self.grid_info()['row']-1)
                self.x_coordinate = self.grid_info()['row']
                gb.reveal_tile(player=self)

        if direction == 'right':
            if self.grid_info()['column'] >= 10:
                self.y_coordinate = self.grid_info()['column']
                pass
            else:
                self.grid(column=self.grid_info()['column']+1)
                self.y_coordinate = self.grid_info()['column']
                gb.reveal_tile(player=self)

        if direction == 'left':
            if self.grid_info()['column'] <= 1:
                self.y_coordinate = self.grid_info()['column']
                pass
            else:
                self.grid(column=self.grid_info()['column'] - 1)
                self.y_coordinate = self.grid_info()['column']
                gb.reveal_tile(player=self)

        self.score_board.update_scoreboard(self)

    # Function to call when the player has lost/died.
    def lost(self, gb):
        self.disabled = True
        messagebox.showinfo("Lost", "Player is out of HP!\nPress Esc to exit")
        gb.reveal_all_mines()


# Frame class to keep track of player information on the outer layer
class ScoreBoard(Frame):
    def __init__(self, outer_layer, player):
        Frame.__init__(self, outer_layer)
        self.linked_player = player.player_name
        self.player_hp_info = player.hp
        self.adjacent_warning = False
        self.hp_label = Label(self, text=f"{self.linked_player} HP: {self.player_hp_info}")
        self.hp_label.grid(row=0, column=0)

    def update_scoreboard(self, player):
        self.player_hp_info = player.hp
        self.hp_label.configure(text=f"{self.linked_player} HP: {self.player_hp_info}")


# ---------------------------------Change_Log_Notes---------------------------------------------------------------------
# left off messing around with revealing all mines at once
#
# redid the game board object as a Frame instead of TopLevel so that I could build a border around it.
# Was able to do a faux border by creating buttons in the corners of the border
#
# Got the player to move by calling the grid method again and just changing the row/column. Set up an if statement to
# ensure the player cannot move beyond the border.
#
# Going to attempt to add a "trail" of visited tiles to mark where the player has been and what color the revealed tile is
#
# class method in game board not activating Tiles class method to reveal color. Figured out that this was due to the game
# tile list being appended with a tile that was being put into the grid at the same time. Fixed by first appending a Tile
# instance into the tile list and then putting them to grid from the list directly instead of gridding at time of instantiation.
#
# Fixed the hovering so it no longer changes color sometimes causing confusion when the cursor is highlighting a button
#
# Created an "owner" property for tiles for possible multiplayer PVP in upcoming future. Property will store the owner
# of the tile to both change color according to owner, and track tile ownership at the end of a duel. 8/22/2023 JR
# Altered the trail to color code based on the proximity to mines on the field.n 8/22/2023
#
# Creating a scoreboard class to keep track of player stats on the screen. Want to have this class be instantiated inside
# player class for simplicity of updating and linking player info
#
# Was able to instantiate the scoreboard class object into the player class to streamline and make updating much easier.
# Put them on the grid in their appropriate spot. Tracks HP but not whether adjacent to a mine or not.
#
# Added a feature so the background of a players scoreboard so that it turns red when adjacent to a mine.
#
