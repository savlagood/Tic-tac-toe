import random
import numpy as np
import tkinter as tk


class GameField:
	"""Represents a field for playing tic tac toe."""

	def __init__(self, size=3, n_players=2, player_list=None):
		"""
		Initialization of basics parameters.
		:param size: size of game field.
		:param n_players: number of players.
		:param player_list: list of players symbols.
		"""
		# Basic parameters
		self.size = size
		self.n_players = n_players

		if player_list:
			self.players = player_list
		else:
			self.players = list(range(self.n_players))

		# Parameters validation
		if not self.n_players > 1:
			raise ValueError(
				f"Number of players (n_players) must be greater than 1. "\
				f"Wrong: {self.n_players} > 1."
			)

		if not self.n_players < self.size:
			raise ValueError(
				f"Number of players (n_players) must be less than size of field (size)! "\
				f"n_players: {self.n_players}, size: {self.size}. "\
				f"Wrong: {self.n_players} < {self.size}."
			)

		if not self.n_players == len(player_list):
			raise ValueError(
				f"Number of players (n_players) must be equal to length of player_list! "\
				f"n_players: {self.n_players}, length of player_list: {len(player_list)}. "\
				f"Wrong: {self.n_players} == {len(player_list)}."
			)

		# Creating an empty (self.size x self.size) matrix
		self.field = np.full((self.size, self.size), None)

		# Creating an iterator by player list
		self.player_list = self.players_chain(self.n_players, player_list)
		
		# Getting a  current player
		self.current_player = next(self.player_list)

	def step(self, row, column):
		"""
		If cell (row, column) is empty then sets the value of current player to it.
		:return number of winner or None
		"""
		if self.field[row][column] is None:
			# Selecting the cell
			self.field[row][column] = self.current_player

			# Getting the winner
			winner = self.get_winner()
			if winner is not None:
				# Returning the winner
				return winner

			# Getting a next player
			self.current_player = next(self.player_list)

			# There is no winner
			return None 

		else:
			raise ValueError(f"Cell ({row}, {column}) is not empty.")

	def get_winner(self):
		"""Searches a winner in rows, columns and diagonals."""
		for index in range(self.size):
			# Searching winner in row[index]
			player = self.field[index, 0]
			if player is not None and (self.field[index] == player).all():
				return player

			# Searching winner in column[index]
			player = self.field[0, index]
			if player is not None and (self.field[:, index] == player).all():
				return player

		# Searching winner in diagonal from left-top to right-bottom
		player = self.field[0, 0]
		if player is not None and (self.field.diagonal() == player).all():
			return player

		# Searching winner in diagonal from right-top to left-bottom
		player = self.field[0, -1]
		if player is not None and (np.fliplr(self.field).diagonal() == player).all():
			return player

		# Field filled
		if None not in self.field:
			return -1

		# There is no winner
		return None

	@staticmethod
	def players_chain(n_players, player_list):
		"""Returns number of next player."""
		while True:
			for player in player_list:
				yield player


class AIPlayer:
	"""Represents a bot with AI for tic tac toe game."""

	def __init__(self, field):
		"""
		Initialization of basics parameters.
		:param field: object of GameField class.
		"""
		self.field = field

	def step(self):
		"""Search position for next step."""
		# Symbol of player
		symbol_1 = self.field.players[0]
		# Symbol of bot
		symbol_2 = self.field.players[1]

		# Indices of free cells
		free_cells = list()

		for index in range(self.field.size):
			# Getting row and column
			row = self.field.field[index]
			column = self.field.field[:, index]

			if None in row:
				# Index of None
				none_index = np.where(row == None)[0][0]
				# If one symbol repeat in the row, then...
				if sum(row == symbol_2) == 2 or sum(row == symbol_1) == 2:
					# Return coords of None
					return index, none_index
				else:
					# Or add None coords to free_cells
					free_cells.append((index, none_index))

			if None in column:
				# Index of None
				none_index = np.where(column == None)[0][0]
				# If one symbol repeat in the column, then...
				if sum(column == symbol_2) == 2 or sum(column == symbol_1) == 2:
					# Return coords of None
					return none_index, index
				else:
					# Or add None coords to free_cells
					free_cells.append((none_index, index))

		# From left-top to right-bottom diagonal
		diag_1 = self.field.field.diagonal()
		# From right-top to left-bottom diagonal
		diag_2 = np.fliplr(self.field.field).diagonal()

		if None in diag_1:
			# Index of None
			none_index = np.where(diag_1 == None)[0][0]
			# If one symbol repeat in the diagonal, then...
			if sum(diag_1 == symbol_2) == 2 or sum(diag_1 == symbol_1) == 2:
				# Return coords of None
				return none_index, none_index
			else:
				# Or add None coords to free_cells
				free_cells.append((none_index, none_index))

		if None in diag_2:
			# Index of None
			none_index = np.where(diag_2 == None)[0][0]
			# If one symbol repeat in the diagonal, then...
			if sum(diag_2 == symbol_2) == 2 or sum(diag_2 == symbol_1) == 2:
				# Return coords of None
				return none_index, self.field.size - none_index - 1
			else:
				# Or add None coords to free_cells
				free_cells.append((index, self.field.size - none_index - 1))

		# Getting random coord from list of best coords
		free_cell = random.choice(free_cells)
		# And returns it!
		return free_cell[0], free_cell[1]


class TicTacToeGame:
	"""Represents a game process in tic tac toe game."""

	def __init__(
			self, n_players, field_size, window, menu_frame=None, using_ai=False, cell_size=100
		):
		"""
		Initialing of basics parameters of playing in tic tac toe.
		:param n_players: number of players.
		:param field_size: size of the game field, number of cells in one row.
		:param window: Tkinter window tk.Tk().
		:param menu_frame: Menu frame.
		:param using_ai: if n_players is 2 then second player can be bot with AI.
		:param cell_size: size of one cell.
		"""
		# tkinter objects
		self.window = window
		self.menu_frame = menu_frame

		# Settings of the players
		self.n_players = n_players
		self.using_ai = using_ai

		# Sizes
		self.cell_size = cell_size
		self.field_size = field_size
		self.figure_size = self.cell_size // 2
		self.line_width = self.cell_size // 10
		self.canvas_size = self.field_size * self.cell_size + (self.field_size-1) * self.line_width

		# Colors
		self.line_color = '#000'

		# Figure and line coords
		self.figures = list()
		self.line_coords = [
			(self.cell_size + self.line_width) * coord - self.line_width // 2
			for coord in range(1, self.field_size)
		]

		# Symbols of the players in the game
		if self.n_players == 2:
			# Classic symbols of tic tac toe game
			self.player_list = ['X', 'O']
		else:
			# Numbers (0, 1, 2, ...)
			self.player_list = list(range(self.n_players))

		# Game field
		self.game_field = GameField(
			size=self.field_size, n_players=self.n_players, player_list=self.player_list
		)

		# AI player
		if self.n_players == 2 and self.field_size == 3 and self.using_ai:
			self.bot = AIPlayer(field=self.game_field)

		# Creating widgets
		# tkinter variables
		self.var_game_state = tk.StringVar(self.window, '')

		# tkinter widgets
		# Main frame which contains all widgets
		self.main_frame = tk.Frame(self.window)

		# Contains the state of the game
		self.game_state_lbl = tk.Label(
			self.main_frame, textvariable=self.var_game_state, font='Raleway 20'
		)
		self.game_state_lbl.pack(pady=10, ipadx=10)

		# Frame with buttons
		self.buttons_frame = tk.Frame(self.main_frame)

		self.button_close = tk.Button(
			self.buttons_frame, text='Закончить игру', font='Arial 10', command=self.close_the_game
		)
		self.button_restart = tk.Button(
			self.buttons_frame, text='Играть заново', font='Arial 10', command=self.restart_the_game
		)
		self.button_close.grid(row=0, column=0, padx=(0, 3))
		self.button_restart.grid(row=0, column=1, padx=(3, 0))

		# Canvas with the game field
		self.canvas = tk.Canvas(
			self.main_frame, width=self.canvas_size, height=self.canvas_size, bg='#fff'
		)
		self.canvas.pack()

		# Binding the clicks by field to self.field_click function
		self.canvas.bind('<Button-1>', self.field_click)

		# Drawing the game grid
		for coord in self.line_coords:
			self.canvas.create_line(
				0, coord, self.canvas_size + 1, coord, width=self.line_width, fill=self.line_color
			)
			self.canvas.create_line(
				coord, 0, coord, self.canvas_size + 1, width=self.line_width, fill=self.line_color
			)

	def start_the_game(self):
		"""Start the game!"""
		# Shows fram with the game
		self.main_frame.pack()
		# Updating info about the game
		self.show_game_state(winner=None)

	def close_the_game(self):
		"""Close the game."""
		# Closes frame with the game
		self.main_frame.pack_forget()

		# If main menu frame exist then...
		if self.menu_frame is not None:
			# Show the main menu
			self.menu_frame.pack(ipadx=10, ipady=10)
		else:
			# Close the window
			self.window.destroy()

	def restart_the_game(self):
		"""Restarts the game."""
		# Hide the buttons frame
		self.buttons_frame.pack_forget()

		# Recreating the game field
		self.game_field = GameField(
			size=self.field_size, n_players=self.n_players, player_list=self.player_list
		)

		# Recreating the AI player
		if self.n_players == 2 and self.field_size == 3 and self.using_ai:
			self.bot = AIPlayer(field=self.game_field)

		# Recreating the canvas with the game field
		self.canvas.pack_forget()
		self.canvas = tk.Canvas(
			self.main_frame, width=self.canvas_size, height=self.canvas_size, bg='#fff'
		)
		self.canvas.pack()

		# Drawing the game grid
		for coord in self.line_coords:
			self.canvas.create_line(
				0, coord, self.canvas_size + 1, coord, width=self.line_width, fill=self.line_color
			)
			self.canvas.create_line(
				coord, 0, coord, self.canvas_size + 1, width=self.line_width, fill=self.line_color
			)

		# Binding the clicks by field to self.field_click function
		self.canvas.bind('<Button-1>', self.field_click)

		# Updating info about the game
		self.show_game_state(winner=None)

	def show_game_state(self, winner=None):
		"""Shows the info of the game or the winner if there is one."""
		# Checking the state of the game
		if winner is not None:
			# Game over
			self.canvas.unbind('<Button-1>')
			self.buttons_frame.pack(after=self.game_state_lbl, pady=(0, 10))

			if winner == -1:
				# Dead heat
				self.var_game_state.set('Ничья!')
			else:
				# We have a winner
				self.var_game_state.set(f'Выиграл игрок: {winner}!')

		else:
			# Updates the text of current player
			self.var_game_state.set(f'Сейчас xодит игрок: {self.game_field.current_player}')

	def bot_step(self):
		"""Does the bot step."""
		ai_row, ai_column = self.bot.step()
		# Drawing bot figure
		self.draw_figure(ai_row, ai_column)
		# Does the game step and gets the winner if there is one
		winner = self.game_field.step(ai_row, ai_column)
		# Player may do his step again
		self.canvas.bind('<Button-1>', self.field_click)
		# Updates info about the game
		self.show_game_state(winner=winner)

	def draw_figure(self, row, column):
		"""Draws a figure in center of defined row and column of the field."""
		# Gets the coords of center of the cell
		x = column * self.cell_size + self.cell_size // 2 + self.line_width * column
		y = row * self.cell_size + self.cell_size // 2 + self.line_width * row

		# Draws the figure
		self.canvas.create_text(
			x, y, font=f'Raleway {self.figure_size} bold',
			text=self.game_field.current_player
		)

	def field_click(self, event):
		"""Handles clicks by field."""
		# Gets mouse coords
		mouse_x = event.x
		mouse_y = event.y

		# Checking that mouse clicked by the dividing lines
		for coord in self.line_coords:
			if coord - self.line_width // 2 <= mouse_x <= coord + self.line_width // 2:
				break
			elif coord - self.line_width // 2 <= mouse_y <= coord + self.line_width // 2:
				break

		else:
			# Gets row and column index of cell
			row = mouse_y // (self.cell_size + self.line_width)
			column = mouse_x // (self.cell_size + self.line_width)

			# Checking that cell is free
			if self.game_field.field[row, column] is None:
				# Drawing player figure
				self.draw_figure(row, column)

				# Does the game step and gets the winner if there is one
				winner = self.game_field.step(row, column)
				# Updates info about the game
				self.show_game_state(winner=winner)

				# Bot step
				if self.using_ai and not winner:
					# Makes a bot step after delay
					self.window.after(900, self.bot_step)
					# Turning off the clicks handling by canvas while bot doing the step
					self.canvas.unbind('<Button-1>')
