from player import *

main_win = tk.Tk()
rules_button = tk.Button(main_win, text='rules')
rules_button.pack()

tile = Tile(0, 0, main_win)

main_label = tk.Label(main_win, text=tile.description)
main_label.pack()

play_screen = tk.Toplevel()

outer_layer = tk.Frame(play_screen)
outer_layer.grid(row=0, column=0, rowspan=12, columnspan=12)

g_board = GameBoard(outer_layer)
g_board.grid(row=1, column=1)
g_board.set_up_board(verbose=False)

top_left = tk.Button(outer_layer, text="Jump")
top_left.grid(row=0, column=0)

top_right = tk.Button(outer_layer)
top_right.grid(row=0, column=12)

bottom_left = tk.Button(outer_layer,text='End')
bottom_left.grid(row=12, column=0)

bottom_right = tk.Button(outer_layer)
bottom_right.grid(row=12, column=12)

new_player = Player(1, 1, g_board, outer_layer)
new_player.grid(row=1, column=1)
new_player.score_board.grid(row=0, column=1)


player_two = Player(10, 10, g_board, outer_layer)
player_two.grid(row=10, column=10)
player_two.score_board.grid(row=12, column=1)

#g_board.reveal_all_mines()
main_win.withdraw()
# ---------------------------------------------------Player 1 Controls--------------------------------------------------
play_screen.bind('<Right>', lambda event: new_player.move_player('right', g_board))
play_screen.bind('<Left>', lambda event: new_player.move_player('left', g_board))
play_screen.bind('<Down>', lambda event: new_player.move_player('down', g_board))
play_screen.bind('<Up>', lambda event: new_player.move_player('up', g_board))
# ---------------------------------------------------Player 2 Controls--------------------------------------------------
play_screen.bind('<d>', lambda event: player_two.move_player('right', g_board))
play_screen.bind('<a>', lambda event: player_two.move_player('left', g_board))
play_screen.bind('<s>', lambda event: player_two.move_player('down', g_board))
play_screen.bind('<w>', lambda event: player_two.move_player('up', g_board))
# -------------------------------------------------Exits Game-----------------------------------------------------------
play_screen.bind('<Escape>', lambda event: main_win.destroy())

main_win.mainloop()


# ------------------------------------Ideas for upcoming features-------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------------
# Ideas for game modes.
# PVP-a 2 player game in which each player battles to turn more of the board into their color, time
# based or until the whole board is filled, have to be careful not to die, or you cant turn any more tiles.
# Campaign - navigating a dungeon
# Minesweeper mode - Single player only your tile detects mines not the tiles around the mines.
# ----------------------------------------------------------------------------------------------------------------------
