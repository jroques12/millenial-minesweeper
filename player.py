import random
from tkinter import messagebox
from tkinter import Frame
from tkinter import Button
from tkinter import Label
import tkinter as tk


# setting up the "board" using a frame and buttons as the backdrop and tiles
class GameBoard(Frame):
    # pass in the frame to have the board set up on as "window" upon creation
    def __init__(self, window):
        # Copy initialization from Frame object from tkinter
        Frame.__init__(self, window)
        # Sets up to create a 10x10 game board
        self.num_of_rows = 10
        self.num_of_columns = 10
        # to keep track of all the tiles (buttons) on the board
        self.game_piece_list = []
        # to keep track of all the mines tiles on the board
        self.mine_list = []
        # keeps track of all the neutral tiles on the board
        self.tile_list = []
        # keeps track of the total number of tiles
        self.tile_count = 0

    # Sets up tiles on the board to either be mines or neutral tiles
    def set_up_board(self, verbose=True):
        # first need to set up the mine coordinates by using integer randomization.
        random.seed()

        # to keep track of the coordinates with mines on them
        mine_coordinate_list = []

        #  Will set up the coordinates for 5 mines.
        while len(mine_coordinate_list) < 5:
            # Picks two random integers between 1 and 10 for each x and y coordinate
            temp_x_coordinate = random.randint(1, 10)
            temp_y_coordinate = random.randint(1, 10)

            # Checks whether the coordinates already exist in the ongoing list
            # and makes sure that the mines aren't created
            # on the starting tiles of the player. Need to add a condition to
            # prevent starting tile for player 2 to be a mine.
            if not [temp_x_coordinate, temp_y_coordinate] in mine_coordinate_list and [temp_x_coordinate,
                                                                                       temp_y_coordinate] != [1, 1]:
                # Appends the coordinates to the list of mine coordinates
                mine_coordinate_list.append([temp_x_coordinate, temp_y_coordinate])
                # Toggle verbose for terminal echo of mine coordinates
                if verbose:
                    print(f"New mine created at {temp_x_coordinate}, {temp_y_coordinate}")

        # Creates Mine objects with the coordinates that map to the mine_coordinate_list
        for coordinate in mine_coordinate_list:
            self.mine_list.append(Mine(coordinate[0], coordinate[1], self))

        # iterates over the possible game tile coordinates
        for row in range(1, self.num_of_rows + 1):
            for column in range(1, self.num_of_columns + 1):
                # default behavior is to set tiles to neutral (not Mines)
                is_mine = False

                # iterates over the list of Mine objects to determine if one of the mine's coordinates matches the
                # current coordinate
                for mine in self.mine_list:
                    if [row, column] == [mine.x_coordinate, mine.y_coordinate]:
                        # Situates the mine on the actual gameboard grid and renders a tkinter button to act as a mine
                        mine.grid(row=row, column=column)

                        # Appends the mine to the list of game pieces
                        self.game_piece_list.append(mine)

                        # sets current tile state for whether mine is true for further method modification
                        is_mine = True

                # if the mine check for current coordinate clears with no mines
                # appends a neutral game tile to the board and list
                if not is_mine:
                    # Adds a Tile object to the game piece list and the neutral tile list. Renders the piece as a
                    # tkinter button on the board at this time
                    self.game_piece_list.append(Tile(row, column, self))
                    self.tile_list.append(self.game_piece_list[-1])
                    self.game_piece_list[-1].grid(row=row, column=column)

        # Iterates over each tile in the neutral tile list to compare to whether a mine exists in an adjacent coordinate
        # and if so, changes the hidden color of the tile to orange.
        for tile in self.tile_list:
            for mine in self.mine_list:
                if abs(tile.x_coordinate - mine.x_coordinate) <= 1 and abs(tile.y_coordinate - mine.y_coordinate) <= 1:
                    tile.color = 'orange'

    # To be called when a player dies to reveal all mines on the game board for the opponent to avoid.
    def reveal_all_mines(self, verbose=True):
        for mine in self.mine_list:
            mine.reveal_color()
            if verbose:
                print(f"Mine revealed at location {mine.x_coordinate}, {mine.y_coordinate}!")

    # Method to reveal the color of the current tile the player has landed on
    def reveal_tile(self, player):
        all_tiles_visited = True

        # iterates over each piece of the game board whether mine or neutral tile to reveal color if player coord
        # matches tile coord
        for tile in self.game_piece_list:

            if [player.x_coordinate, player.y_coordinate] == [tile.x_coordinate, tile.y_coordinate]:
                tile.reveal_color()

                if not tile.is_visited:
                    tile.is_visited = True
                    # checks whether the current tile is a mine and detonates if it is
                    if isinstance(tile, Mine):
                        tile.detonate(player)

                    else:
                        player.tile_count += 1
                        print(f"{player.player_name} Score: {player.tile_count}")

                # If the tile color is orange (meaning adjacent to a mine) it will change the players hp label to orange
                # as well to indicate to the player they are within 1 tile of a mine
                # (mine color is obscured by the player until they move off the tile)
                if tile.color == 'orange':
                    player.score_board.hp_label.configure(background='orange')

                # If the tile is neutral and not adjacent to a mine,
                # changes the player hp background back to default color
                elif tile.color == 'green':
                    player.score_board.hp_label.configure(background=tile.default_color)

        # checks if all neutral tiles have been visited to evaluate win condition, disable the players if true, and show
        # messagebox displaying victory message.
        for tile in self.tile_list:

            if tile.is_visited:
                pass
            else:
                all_tiles_visited = False

        if all_tiles_visited:

            messagebox.showinfo("Game Over!",
                                "All tiles have been visited, Calculating Score!\nPress Esc to exit game.")

            # Calculates the winning score
            winning_score = max([player.tile_count for player in Player.player_list])
            winning_player = [player for player in Player.player_list if player.tile_count == winning_score][0]

            # Disables player ability to move and displays each player's score, if the player matches the winning score,
            # displays player name
            for player in Player.player_list:
                player.disabled = True
                print(f"{player.player_name} Has a score of: {player.tile_count}")
                if player.tile_count == winning_score:
                    print("and is the winner!")

            print(f"{winning_player.player_name} is the winning player")

    # Reveals the tile color of each tile on the game board. Used for debugging mainly
    def reveal_all_tiles(self):
        for tile in self.game_piece_list:
            print(tile)
            tile.reveal_color()


# Class for a neutral tile on the gameboard
class Tile(tk.Button):
    # must be initiated with coordinates and which frame it will belong to, be sure not to duplicate tile coordinates
    def __init__(self, x_coordinate, y_coordinate, window: GameBoard):
        # Inherits initiation from tkinter Button
        Button.__init__(self, window)
        self.window = window
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
        self.configure(command=self.end_jump)

    def reveal_color(self):
        self.configure(background=self.color)

    def end_jump(self):
        for player in Player.player_list:
            if player.disabled:
                pass
            if player.in_transit:
                player.x_coordinate = self.x_coordinate
                player.y_coordinate = self.y_coordinate
                player.grid(row=player.x_coordinate, column=player.y_coordinate)
                player.in_transit = False
                self.window.reveal_tile(player)
                player.score_board.update_scoreboard(player)


class Mine(Tile):
    def __init__(self, x_coordinate, y_coordinate, game_board):
        Tile.__init__(self, x_coordinate=x_coordinate, y_coordinate=y_coordinate, window=game_board)
        # Purpose of has_charge is to ensure that a mine only damages the player the first time they go over the mine.
        self.has_charge = True
        # Not yet going to utilize the did_damage variable but want a way to track it regardless.
        self.did_damage = False
        self.color = "red"

    def detonate(self, player_obj, verbose=True):
        player_obj.score_board.hp_label.configure(background='red')
        if self.has_charge:
            self.has_charge = False
            player_obj.hp -= 1
            self.reveal_color()
            self.did_damage = True
            if player_obj.hp <= 0:
                player_obj.configure(background='black')
                player_obj.lost()

            if verbose:
                print(f"{player_obj.player_name} has {player_obj.hp} HP left!")


class Player(Tile):
    player_list = []

    def __init__(self, x_coordinate, y_coordinate, gb, outer_layer, player_number):
        Tile.__init__(self, x_coordinate=x_coordinate, y_coordinate=y_coordinate, window=gb)
        self.player_name = f"Player # {player_number}"
        self.hp = 3
        self.color = 'blue'
        self.configure(background=self.color)
        self.tile_count = 0
        self.disabled = False
        self.in_transit = False
        self.owner = "None"
        self.score_board = ScoreBoard(outer_layer, self)

        # Keeps track of all the players in the game for evaluating certain conditions IE win condition
        Player.player_list.append(self)

    # the move_player function is the bread and butter of the whole game,
    # it handles all the updates for the GUI info such
    # as HP remaining, adjacent mines, number of tiles converted, etc.
    # Additionally, the trail functionality is partially
    # linked here as well as the GameBoard class.

    def move_player(self, direction, gb):
        if self.disabled:
            return
        if direction == 'down':
            if self.grid_info()['row'] >= 10:
                self.x_coordinate = self.grid_info()['row']

            else:
                self.grid(row=self.grid_info()['row'] + 1)
                self.x_coordinate = self.grid_info()['row']
                gb.reveal_tile(player=self)

        if direction == 'up':
            if self.grid_info()['row'] <= 1:
                self.x_coordinate = self.grid_info()['row']
                pass
            else:
                self.grid(row=self.grid_info()['row'] - 1)
                self.x_coordinate = self.grid_info()['row']
                gb.reveal_tile(player=self)

        if direction == 'right':
            if self.grid_info()['column'] >= 10:
                self.y_coordinate = self.grid_info()['column']
                pass
            else:
                self.grid(column=self.grid_info()['column'] + 1)
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

    # Sets up the player jump state to be utilized by tile method
    def player_jump(self):
        if self.disabled:
            return
        self.in_transit = True

    # Function to call when the player has lost/died.
    def lost(self):
        self.disabled = True


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
        if player.hp <= 0:
            self.hp_label.configure(text=f"{self.linked_player} is dead")

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
# instance into the tile list and then putting them to grid from the list directly instead of rendering at time of instantiation.
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
# Added score tracking however once one player dies, they both are unable to move. Need to adjust so that only the dead
# player cannot move.
#
# Got it working to where both players aren't disabled once one of them dies. Next step: Game needs to display a message
# showing the winner of the game.
#
# Added jumping functionality to "teleport" to the tile clicked
