import numpy as np
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
AI_PIECE = "O"
PLAYER_PIECE = "X"

def minimax(matrice, profondeur, alpha, beta, isIA):
	valid_locations = get_valid_locations(matrice)
	is_terminal = is_terminal_node(matrice)
	if profondeur == 0 or is_terminal:
		if is_terminal:
			if winning_move(matrice, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(matrice, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # profondeur is zero
			return (None, score_position(matrice, AI_PIECE))
	if isIA:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(matrice, col)
			b_copy = matrice.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, profondeur-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(matrice, col)
			b_copy = matrice.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, profondeur-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(matrice):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(matrice, col):
			valid_locations.append(col)
	return valid_locations

def get_next_open_row(matrice, col):
	for r in range(ROW_COUNT):
		if matrice[r][col] == 0:
			return r

def is_valid_location(matrice, col):
	return matrice[ROW_COUNT-1][col] == "."

def is_terminal_node(matrice):
	return winning_move(matrice, PLAYER_PIECE) or winning_move(matrice, AI_PIECE) or len(get_valid_locations(matrice)) == 0

def winning_move(matrice, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if matrice[r][c] == piece and matrice[r][c+1] == piece and matrice[r][c+2] == piece and matrice[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if matrice[r][c] == piece and matrice[r+1][c] == piece and matrice[r+2][c] == piece and matrice[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if matrice[r][c] == piece and matrice[r+1][c+1] == piece and matrice[r+2][c+2] == piece and matrice[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if matrice[r][c] == piece and matrice[r-1][c+1] == piece and matrice[r-2][c+2] == piece and matrice[r-3][c+3] == piece:
				return True

def score_position(matrice, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(matrice[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(matrice[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(matrice[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [matrice[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [matrice[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def drop_piece(matrice, row, col, piece):
	matrice[row][col] = piece

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score





