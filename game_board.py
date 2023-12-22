import tkinter as tk
from tkinter import *
from mines import *
from audio import blow_up_sound

hp = 5
adjacent_mines = 0
active_mines = IntVar


def game_start(main_menu):
    global hp
    main_menu.withdraw()
    mine_tiles = []
    print(f'Number of mines before generation are {len(mine_tiles)}')

    if len(mine_tiles) == 0:
        mine_tiles = create_mines(10)

    game_window = tk.Toplevel()
    game_window.title('Millennial Minesweeper')
    button_list = []
    counter = 0
    hp = 5

    for row in range(1, 11):
        for col in range(1, 11):
            button_list.append(tk.Button(game_window, padx=20, pady=10, relief="sunken"))
            button_list[counter].grid(row=row, column=col)
            counter += 1

    # for buttona in button_list:
    #     buttona.configure(command=lambda xc=buttona.grid_info()['column'], yc=buttona.grid_info()['row']: click_tile(xc, yc, mine_tiles, button_list))

    def mine_vision():
        for mine in mine_tiles:
            for buttond in button_list:
                if mine.xcoordinate == buttond.grid_info()['column'] and mine.ycoordinate == buttond.grid_info()['row']:
                    buttond.configure(bg="red")

    def check_tile(cursor_obj):
        for i in mine_tiles:
            if cursor_obj.grid_info()['row'] == i.ycoordinate and cursor_obj.grid_info()['column'] == i.xcoordinate and i.has_charge:
                global hp
                hp -= 1
                blow_up_sound()
                cursor_obj.configure(bg='red')
                i.has_charge = False
                i.did_damage = True
                left_edge_label['text'] = f'S\nA\nF\nE\n{hp}'

                if hp <= 0:
                    lose_window = tk.Toplevel()
                    lose_message = tk.Label(lose_window, text='Your HP has gone to 0. You lose.')
                    lose_message.pack()
                    lose_button = tk.Button(lose_window, text="Exit", command=lambda: quit_game(lose_window))
                    lose_button.pack()
                    mine_vision()

                    # for child in game_window.winfo_children():
                    #     child.configure(stat)

                    lose_window.grab_set()

            elif cursor_obj.grid_info()['row'] == i.ycoordinate and cursor_obj.grid_info()['column'] == i.xcoordinate and not i.has_charge and i.did_damage:
                cursor_obj.configure(bg='red')

            elif cursor_obj.grid_info()['row'] == i.ycoordinate and cursor_obj.grid_info()['column'] == i.xcoordinate and not i.has_charge and not i.did_damage:
                cursor_obj.configure(bg='green')

    def area_check(cursor_obj):
        for j in mine_tiles:
            if 1 >= j.ycoordinate - cursor_obj.grid_info()['row'] >= -1 and 1 >= j.xcoordinate - cursor_obj.grid_info()['column'] >= -1 and j.has_charge:
                cursor_obj.configure(bg="yellow")
                break
            else:
                cursor_obj.configure(bg='blue')

    def adjacent_check(cursor_obj):
        global adjacent_mines
        adjacent_mines = 0
        for i in mine_tiles:
            if 1 >= i.ycoordinate - cursor_obj.grid_info()['row'] >= -1 and 1 >= i.xcoordinate - cursor_obj.grid_info()['column'] >= -1 and i.has_charge:
                adjacent_mines += 1
                mine_info.configure(text=f"Adjacent Mines: {adjacent_mines}")
            else:
                mine_info.configure(text=f"Adjacent Mines: {adjacent_mines}")

    def active_mines_left():
        global active_mines
        active_mines = 0
        for mine in mine_tiles:
            if mine.has_charge:
                active_mines += 1
        active_mine_info.configure(text=f"Mines Left: {active_mines}")

        if active_mines == 0:
            victory_window = tk.Toplevel()
            victory_message = tk.Label(victory_window, text="You cleared all mines and Won!")
            victory_message.pack()
            victory_button = tk.Button(victory_window, text='Close', command=lambda: quit_game(victory_window))
            victory_button.pack()

    def trail():
        adjacent_check(cursor)
        active_mines_left()
        for button in button_list:
            if cursor.grid_info()['row'] == button.grid_info()['row'] and cursor.grid_info()['column'] == button.grid_info()['column']:
                for mine in mine_tiles:
                    if (cursor.grid_info()['row'] == mine.ycoordinate and cursor.grid_info()['column'] == mine.xcoordinate and mine.has_charge) or \
                            (cursor.grid_info()['row'] == mine.ycoordinate and cursor.grid_info()['column'] == mine.xcoordinate and mine.did_damage):
                        button.configure(bg='red')
                        return
                    elif cursor.grid_info()['row'] == mine.ycoordinate and cursor.grid_info()['column'] == mine.xcoordinate and not mine.has_charge:
                        button.configure(bg='green')
                        return

                button.configure(bg='blue')

    def move_cursor(cursor_obj, direction):
        if direction == 'right':
            if cursor_obj.grid_info()['column'] == 10:
                pass
            else:
                cursor_obj.grid(column=cursor_obj.grid_info()['column']+1)
                trail()
                area_check(cursor)
                check_tile(cursor)

        elif direction == 'left':
            if cursor_obj.grid_info()['column'] == 0:
                pass
            else:
                cursor_obj.grid(column=cursor_obj.grid_info()['column']-1)
                trail()
                area_check(cursor)
                check_tile(cursor)

        elif direction == 'down':
            if cursor_obj.grid_info()['row'] == 10:
                pass
            else:
                cursor_obj.grid(row=cursor_obj.grid_info()['row'] + 1)
                trail()
                area_check(cursor)
                check_tile(cursor)

        elif direction == 'up':
            if cursor_obj.grid_info()['row'] == 0:
                pass
            else:
                cursor_obj.grid(row=cursor_obj.grid_info()['row'] - 1)
                trail()
                area_check(cursor)
                check_tile(cursor)

        top_edge_label.configure(text=f'SAFE--{cursor.grid_info()["column"]},{cursor.grid_info()["row"]}')

    def quit_game(lwin):
        game_window.destroy()
        if lwin.winfo_exists():
            lwin.destroy()
        main_menu.deiconify()

    top_edge_label = tk.Label(game_window, text=f"SAFE--", padx=100, pady=12)
    top_edge_label.grid(row=0, column=0, columnspan=11)

    left_edge_label = tk.Label(game_window, text=f'S\nA\nF\nE\n{hp}', padx=17, pady=165)
    left_edge_label.grid(row=1, column=0, rowspan=11)

    cursor = tk.Button(game_window, padx=20, pady=10, bg="blue", relief='raised', bd=2)
    cursor.grid(row=0, column=0)

    cursor_frame = tk.Frame(game_window)
    cursor_frame.grid(row=11, column=1, columnspan=11)

    info_frame = tk.Frame(game_window,bg='black', pady=10, padx=10)
    info_frame.grid(row=12, column=1, columnspan=11)

    up_arrow = tk.Button(cursor_frame, text='^', font=20, padx=20, pady=10, command=lambda: move_cursor(cursor, 'up'))
    up_arrow.grid(row=11, column=1, columnspan=11)

    left_arrow = tk.Button(cursor_frame, text='<', padx=20, pady=10, command=lambda: move_cursor(cursor, 'left'))
    left_arrow.grid(columnspan=2, row=12, column=4)

    right_arrow = tk.Button(cursor_frame, text='>', padx=20, pady=10, command=lambda: move_cursor(cursor, 'right'))
    right_arrow.grid(columnspan=2, column=6, row=12)

    down_arrow = tk.Button(cursor_frame, text='V', padx=20, pady=10, command=lambda: move_cursor(cursor, 'down'))
    down_arrow.grid(columnspan=11, row=13, column=1)

    mine_info = tk.Label(info_frame, bg='black', fg='red', text=f"Adjacent Mines: {adjacent_mines}", padx=5, pady=5, bd=4, highlightbackground='red', highlightcolor='red', highlightthickness=2)
    mine_info.pack()

    active_mine_info = tk.Label(info_frame, bg='black', fg='red', text=f"Mines Left: {active_mines}", padx=5, pady=5, bd=4, highlightbackground='red', highlightcolor='red', highlightthickness=2)
    active_mine_info.pack()

    game_window.bind('<Right>', lambda event: move_cursor(cursor, 'right'))
    game_window.bind('<Left>', lambda event: move_cursor(cursor, 'left'))
    game_window.bind('<Down>', lambda event: move_cursor(cursor, 'down'))
    game_window.bind('<Up>', lambda event: move_cursor(cursor, 'up'))
    game_window.bind('<Escape>', lambda event: quit_game(game_window))

    close_button = tk.Button(cursor_frame, text="Close", command=lambda: quit_game(game_window))
    close_button.grid(row=14, columnspan=11, column=1)

    area_check(cursor)
    active_mines_left()