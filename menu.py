import tkinter as tk
import time

from game import TicTacToeGame


def show_main_menu():
	"""Shows the main menu frame and hides other frames."""
	main_menu_frame.pack(ipadx=10, ipady=10)
	classic_game_menu_frame.pack_forget()
	extended_game_menu_frame.pack_forget()

def show_classic_menu():
	"""Shows the menu of classic game and hides other frames."""
	main_menu_frame.pack_forget()
	classic_game_menu_frame.pack(ipadx=10, ipady=10)
	extended_game_menu_frame.pack_forget()

def show_extended_menu():
	"""Shows the menu of extended game and hides other frames."""
	main_menu_frame.pack_forget()
	classic_game_menu_frame.pack_forget()
	extended_game_menu_frame.pack(ipadx=10, ipady=10)

def start_the_game(n_players, field_size, cell_size=100, using_ai=False):
	"""Shows the game frame and hides other frames."""
	main_menu_frame.pack_forget()
	classic_game_menu_frame.pack_forget()
	extended_game_menu_frame.pack_forget()
	
	game = TicTacToeGame(
		n_players=n_players, field_size=field_size, window=window,
		menu_frame=main_menu_frame, using_ai=using_ai, cell_size=cell_size
	)
	game.start_the_game()

def start_the_extended_game():
	"""Start the extended game!"""
	# Validating variables
	variables_validator()
	# Updating all entries
	ent_num_players.update()
	ent_field_size.update()
	ent_cell_size.update()
	# Some delay
	time.sleep(0.5)

	# Hiding menues
	main_menu_frame.pack_forget()
	classic_game_menu_frame.pack_forget()
	extended_game_menu_frame.pack_forget()

	# Starting the game
	start_the_game(
		n_players=int(var_num_players.get()),
		field_size=int(var_field_size.get()),
		cell_size=int(var_cell_size.get())
	)	

def variables_validator():
	"""Validates each variable of game settings."""
	num_players = var_num_players.get()
	field_size = var_field_size.get()
	cell_size = var_cell_size.get()

	if not num_players.isdigit() or int(num_players) < 1:
		var_num_players.set('2')
	if not field_size.isdigit() or int(field_size) < 3:
		var_field_size.set('3')
	if not cell_size.isdigit() or int(cell_size) < 10:
		var_cell_size.set('10')

	num_players = int(var_num_players.get())
	field_size = int(var_field_size.get())

	if num_players >= field_size:
		var_num_players.set(field_size - 1)

def decrease_variable(variable):
	"""Decreases the value of variable."""
	variables_validator()
	value = int(variable.get())
	if value > 1:
		variable.set(value - 1)
		variables_validator()

def increase_variable(variable):
	"""Increases the value of variable."""
	variables_validator()
	value = int(variable.get())
	variable.set(value + 1)
	variables_validator()


window = tk.Tk()
window.title('Игра в крестики-нолики')
#window.iconbitmap("D:/Python projects/Tic tac toe/icon.ico")

# MAIN MENU
main_menu_frame = tk.Frame(window)

# Title of menu
lbl = tk.Label(main_menu_frame, text='Крестики-Нолики', font='Arial 30')
lbl.pack(ipadx=50, ipady=20)

# Buttons
btn_classic_game = tk.Button(
	main_menu_frame, text='Классическая игра', font='Arial 10', command=show_classic_menu
)
btn_extended_game = tk.Button(
	main_menu_frame, text='Расширенная игра', font='Arial 10', command=show_extended_menu
)

btn_classic_game.pack(pady=(10, 0), ipadx=10, ipady=5)
btn_extended_game.pack(pady=(10, 0), ipadx=10, ipady=5)


# MENU OF CLASSIC GAME
classic_game_menu_frame = tk.Frame(window)

# Title of menu
lbl_cls_gm = tk.Label(classic_game_menu_frame, text='Классическая игра', font='Arial 30')
lbl_cls_gm.pack(ipadx=50, ipady=20)

# Buttons
btn_gm_with_friend = tk.Button(
	classic_game_menu_frame, text='Играть с другом', font='Arial 10',
	command=lambda: start_the_game(n_players=2, field_size=3)
)
btn_gm_with_ai = tk.Button(
	classic_game_menu_frame, text='Играть с ботом', font='Arial 10',
	command=lambda: start_the_game(n_players=2, field_size=3, using_ai=True)
)
btn_back = tk.Button(classic_game_menu_frame, text='Назад', font='Arial 10', command=show_main_menu)

btn_gm_with_friend.pack(pady=(10, 0), ipadx=10, ipady=5)
btn_gm_with_ai.pack(pady=(10, 0), ipadx=10, ipady=5)
btn_back.pack(pady=(10, 0), ipadx=10, ipady=5)


# MENU OF EXTENDED GAME
extended_game_menu_frame = tk.Frame(window)

# Variables
var_num_players = tk.StringVar(window, '2', name='num_players')
var_field_size = tk.StringVar(window, '3', name='field_size')
var_cell_size = tk.StringVar(window, '100', name='cell_size')

# Title of menu
lbl_ext_gm = tk.Label(extended_game_menu_frame, text='Расширенная игра', font='Arial 30')
lbl_ext_gm.pack(ipadx=50, ipady=20)

# Frame with parameters
frm_params = tk.Frame(extended_game_menu_frame)
frm_params.pack(ipady=10)

# Row with number of players setting
lbl_num_players = tk.Label(frm_params, text='Количество игроков', font='Arial 10')
frm_num_players = tk.Frame(frm_params)

lbl_num_players.grid(row=0, column=0, sticky='w', padx=8, pady=2)
frm_num_players.grid(row=0, column=1, sticky='w', padx=8, pady=2)

btn_dec_num_players = tk.Button(
	frm_num_players, text='-', font='Arial 12', command=lambda: decrease_variable(var_num_players)
)
ent_num_players = tk.Entry(frm_num_players, width=10, bd=0, textvariable=var_num_players)
btn_inc_num_players = tk.Button(
	frm_num_players, text='+', font='Arial 12', command=lambda: increase_variable(var_num_players)
)

btn_dec_num_players.pack(side=tk.LEFT, ipadx=7)
ent_num_players.pack(side=tk.LEFT, fill=tk.BOTH)
btn_inc_num_players.pack(side=tk.LEFT, ipadx=7)

# Row with size of field setting
lbl_field_size = tk.Label(frm_params, text='Размер поля', font='Arial 10')
frm_field_size = tk.Frame(frm_params)

lbl_field_size.grid(row=1, column=0, sticky='w', padx=8, pady=2)
frm_field_size.grid(row=1, column=1, sticky='w', padx=8, pady=2)

btn_dec_field_size = tk.Button(
	frm_field_size, text='-', font='Arial 12', command=lambda: decrease_variable(var_field_size)
)
ent_field_size = tk.Entry(frm_field_size, width=10, bd=0, textvariable=var_field_size)
btn_inc_field_size = tk.Button(
	frm_field_size, text='+', font='Arial 12', command=lambda: increase_variable(var_field_size)
)

btn_dec_field_size.pack(side=tk.LEFT, ipadx=7)
ent_field_size.pack(side=tk.LEFT, fill=tk.BOTH)
btn_inc_field_size.pack(side=tk.LEFT, ipadx=7)

# Row with size of cell setting
lbl_cell_size = tk.Label(frm_params, text='Размер ячейки', font='Arial 10')
frm_cell_size = tk.Frame(frm_params)

lbl_cell_size.grid(row=2, column=0, sticky='w', padx=8, pady=2)
frm_cell_size.grid(row=2, column=1, sticky='w', padx=8, pady=2)

btn_dec_cell_size = tk.Button(
	frm_cell_size, text='-', font='Arial 12', command=lambda: decrease_variable(var_cell_size)
)
ent_cell_size = tk.Entry(frm_cell_size, width=10, bd=0, textvariable=var_cell_size)
btn_inc_cell_size = tk.Button(
	frm_cell_size, text='+', font='Arial 12', command=lambda: increase_variable(var_cell_size)
)

btn_dec_cell_size.pack(side=tk.LEFT, ipadx=7)
ent_cell_size.pack(side=tk.LEFT, fill=tk.BOTH)
btn_inc_cell_size.pack(side=tk.LEFT, ipadx=7)

# Row with buttons
btn_back = tk.Button(frm_params, text='Назад', font='Arial 10', command=show_main_menu)
btn_start = tk.Button(frm_params, text='Играть', font='Arial 10', command=start_the_extended_game)

btn_back.grid(row=3, column=0, sticky='e', pady=(5, 0), padx=(0, 3), ipadx=10, ipady=5)
btn_start.grid(row=3, column=1, sticky='w', pady=(5, 0), padx=(3, 0), ipadx=10, ipady=5)


if __name__ == '__main__':
	show_main_menu()
	window.mainloop()
