# build 2048 in python using pygame!!
import pygame
import random
import sys

import tkinter as tk

def set_a_value(value):
    global a
    a = value
    print(f"Value of 'a' set to {a}")

# Create the main window
root = tk.Tk()
root.title("Game 2048")
root.geometry("500x600")
# Initialize the variable 'a'
a = None

# Create buttons A and B
button_a1 = tk.Button(root, text=" RULES: \n In this game \n, the player must combine tiles \n containing the same numbers . \n The tiles can contain only integer\n values starting from 2,\n and that are a power \nof two, like 2, 4, 8, 16, 32, and so on")
button_a = tk.Button(root, text="powers of 2", command=lambda: set_a_value(2))
button_a.configure(bg="blue", fg="red")
button_b1 = tk.Button(root, text=" RULES: \n In this game \n, the player must combine tiles \n containing the same numbers . \n The tiles can contain only integer\n values starting from 3,\n and that are a power \nof two, like 3, 9, 27, 81, 243, and so on")
button_b = tk.Button(root, text="powers of 3", command=lambda: set_a_value(3))
button_b.configure(bg="blue", fg="red")

# Pack the buttons into the window
button_a1.pack(pady = 30)
button_a.pack(pady=10)
button_b1.pack(pady = 30)
button_b.pack(pady=10)

# Start the main loop
root.mainloop()

pygame.init()
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)


# take your turn based on direction
def take_turn(direc, board):
		global score
		merged = [[False for _ in range(4)] for _ in range(4)]
		if direc == 'UP':
			for i in range(4):
				for j in range(4):
					shift = 0
					if i > 0:
						for q in range(i):
							if board[q][j] == 0:
								shift += 1
						if shift > 0:
							board[i - shift][j] = board[i][j]
							board[i][j] = 0
						if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
								and not merged[i - shift - 1][j]:
							board[i - shift - 1][j] *= 2
							score += board[i - shift - 1][j]
							board[i - shift][j] = 0
							merged[i - shift - 1][j] = True

		elif direc == 'DOWN':
			for i in range(3):
				for j in range(4):
					shift = 0
					for q in range(i + 1):
						if board[3 - q][j] == 0:
							shift += 1
					if shift > 0:
						board[2 - i + shift][j] = board[2 - i][j]
						board[2 - i][j] = 0
					if 3 - i + shift <= 3:
						if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
								and not merged[2 - i + shift][j]:
							board[3 - i + shift][j] *= 2
							score += board[3 - i + shift][j]
							board[2 - i + shift][j] = 0
							merged[3 - i + shift][j] = True

		elif direc == 'LEFT':
			for i in range(4):
				for j in range(4):
					shift = 0
					for q in range(j):
						if board[i][q] == 0:
							shift += 1
					if shift > 0:
						board[i][j - shift] = board[i][j]
						board[i][j] = 0
					if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
							and not merged[i][j - shift]:
						board[i][j - shift - 1] *= 2
						score += board[i][j - shift - 1]
						board[i][j - shift] = 0
						merged[i][j - shift - 1] = True

		elif direc == 'RIGHT':
			for i in range(4):
				for j in range(4):
					shift = 0
					for q in range(j):
						if board[i][3 - q] == 0:
							shift += 1
					if shift > 0:
						board[i][3 - j + shift] = board[i][3 - j]
						board[i][3 - j] = 0
					if 4 - j + shift <= 3:
						if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
								and not merged[i][3 - j + shift]:
							board[i][4 - j + shift] *= 2
							score += board[i][4 - j + shift]
							board[i][3 - j + shift] = 0
							merged[i][4 - j + shift] = True
		return board
if a == 2:
    # 2048 game color library
	colors = {0: (204, 192, 179),
			2: (238, 228, 218),
			4: (237, 224, 200),
			8: (242, 177, 121),
			16: (245, 149, 99),
			32: (246, 124, 95),
			64: (246, 94, 59),
			128: (237, 207, 114),
			256: (237, 204, 97),
			512: (237, 200, 80),
			1024: (237, 197, 63),
			2048: (237, 194, 46),
			'light text': (249, 246, 242),
			'dark text': (119, 110, 101),
			'other': (0, 0, 0),
			'bg': (187, 173, 160)}



	# game variables initialize
	board_values = [[0 for _ in range(4)] for _ in range(4)]
	game_over = False
	spawn_new = True
	init_count = 0
	direction = ''

	#STORING SCORES
	score = 0
	file = open('/Users/anushka/Codes/python/mini project/high_score .txt', 'r')
	init_high = int(file.readline())
	file.close()
	high_score = init_high


	# RESTART the game ones over
	def draw_over():
		pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
		game_over_text1 = font.render('Game Over!', True, 'white')
		game_over_text2 = font.render('Press Enter to Restart', True, 'white')
		screen.blit(game_over_text1, (130, 65))
		screen.blit(game_over_text2, (70, 105))

	# spawn in new pieces randomly when turns start
	def new_pieces(board):
		count = 0
		full = False
		while any(0 in row for row in board) and count < 1:
			row = random.randint(0, 3)
			col = random.randint(0, 3)
			if board[row][col] == 0:
				count += 1
				if random.randint(1, 10) == 10:
					board[row][col] = 4
				else:
					board[row][col] = 2
		if count < 1:
			full = True
		return board, full


	# draw background for the board
	def draw_board():
		pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
		score_text = font.render(f'Score: {score}', True, 'black')
		high_score_text = font.render(f'High Score: {high_score}', True, 'black')
		screen.blit(score_text, (10, 410))
		screen.blit(high_score_text, (10, 450))
		pass


	# draw tiles for game
	def draw_pieces(board):
		for i in range(4):
			for j in range(4):
				value = board[i][j]
				if value > 8:
					value_color = colors['light text']
				else:
					value_color = colors['dark text']
				if value <= 2048:
					color = colors[value]
				else:
					color = colors['other']
				pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
				if value > 0:
					value_len = len(str(value))
					font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
					value_text = font.render(str(value), True, value_color)
					text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
					screen.blit(value_text, text_rect)
					pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


	# main game loop
	run = True
	while run:
		timer.tick(fps)
		screen.fill('gray')
		draw_board()
		draw_pieces(board_values)
		if spawn_new or init_count < 2:
			board_values, game_over = new_pieces(board_values)
			spawn_new = False
			init_count += 1
		if direction != '':
			board_values = take_turn(direction, board_values)
			direction = ''
			spawn_new = True
		if game_over:
			draw_over()
			if high_score > init_high:
				file = open('/Users/anushka/Codes/python/mini project/high_score .txt', 'w')
				file.write(f'{high_score}')
				file.close()
				init_high = high_score

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					direction = 'UP'
				elif event.key == pygame.K_DOWN:
					direction = 'DOWN'
				elif event.key == pygame.K_LEFT:
					direction = 'LEFT'
				elif event.key == pygame.K_RIGHT:
					direction = 'RIGHT'

				if game_over:
					if event.key == pygame.K_RETURN:
						board_values = [[0 for _ in range(4)] for _ in range(4)]
						spawn_new = True
						init_count = 0
						score = 0
						direction = ''
						game_over = False

		if score > high_score:
			high_score = score
		pygame.display.flip()


elif a==3:
	# 2048 game color library
	colors = {0: (242, 230, 255),
			3: (255, 230, 242),
			9: (255, 204, 229),
			27: (255, 179, 215),
			81: (255, 153, 201),
			243: (255, 128, 187),
			729: (255, 77, 160),
			2187: (255, 26, 133),
			6561: (230, 0, 107),
			19683:(179, 0, 83),
			59049: (128, 0, 60),
			177147: (77, 0, 36),
			'light text': (249, 246, 242),
			'dark text': (119, 110, 101),
			'other': (64, 0, 128),
			'bg': (0, 0, 0)}

	# game variables initialize
	board_values =[[0 for _ in range(4)] for _ in range(4)] 
	game_over = False
	spawn_new = True
	init_count = 0
	direction = ''

	#STORING SCORES
	score = 0
	file = open('/Users/anushka/Codes/python/mini project/high_score .txt', 'r')
	init_high = int(file.readline())
	file.close()
	high_score = init_high


	# RESTART the game ones over
	def draw_over():
		pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
		game_over_text1 = font.render('Game Over!', True, 'white')
		game_over_text2 = font.render('Press Enter to Restart', True, 'white')
		screen.blit(game_over_text1, (130, 65))
		screen.blit(game_over_text2, (70, 105))


	# take your turn based on direction
	def take_turn(direc, board):
		global score
		merged = [[False for _ in range(4)] for _ in range(4)]
		match direc:
			case 'UP':
				for i in range(4):
					for j in range(4):
						shift = 0
						if i > 0:
							for q in range(i):
								if board[q][j] == 0:
									shift += 1
							if shift > 0:
								board[i - shift][j] = board[i][j]
								board[i][j] = 0
							if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
									and not merged[i - shift - 1][j]:
								board[i - shift - 1][j] *= 3
								score += board[i - shift - 1][j]
								board[i - shift][j] = 0
								merged[i - shift - 1][j] = True

			case 'DOWN':
				for i in range(3):
					for j in range(4):
						shift = 0
						for q in range(i + 1):
							if board[3 - q][j] == 0:
								shift += 1
						if shift > 0:
							board[2 - i + shift][j] = board[2 - i][j]
							board[2 - i][j] = 0
						if 3 - i + shift <= 3:
							if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
									and not merged[2 - i + shift][j]:
								board[3 - i + shift][j] *= 3
								score += board[3 - i + shift][j]
								board[2 - i + shift][j] = 0
								merged[3 - i + shift][j] = True

			case 'LEFT':
				for i in range(4):
					for j in range(4):
						shift = 0
						for q in range(j):
							if board[i][q] == 0:
								shift += 1
						if shift > 0:
							board[i][j - shift] = board[i][j]
							board[i][j] = 0
						if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
								and not merged[i][j - shift]:
							board[i][j - shift - 1] *= 3
							score += board[i][j - shift - 1]
							board[i][j - shift] = 0
							merged[i][j - shift - 1] = True

			case 'RIGHT':
				for i in range(4):
					for j in range(4):
						shift = 0
						for q in range(j):
							if board[i][3 - q] == 0:
								shift += 1
						if shift > 0:
							board[i][3 - j + shift] = board[i][3 - j]
							board[i][3 - j] = 0
						if 4 - j + shift <= 3:
							if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
									and not merged[i][3 - j + shift]:
								board[i][4 - j + shift] *= 3
								score += board[i][4 - j + shift]
								board[i][3 - j + shift] = 0
								merged[i][4 - j + shift] = True
		return board


	# spawn in new pieces randomly when turns start
	def new_pieces(board):
		count = 0
		full = False
		while any(0 in row for row in board) and count < 1:
			row = random.randint(0, 3)
			col = random.randint(0, 3)
			if board[row][col] == 0:
				count += 1
				if random.randint(1, 10) == 10:
					board[row][col] = 9
				else:
					board[row][col] = 3
		if count < 1:
			full = True
		return board, full


	# draw background for the board
	def draw_board():
		pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
		score_text = font.render(f'Score: {score}', True, 'black')
		high_score_text = font.render(f'High Score: {high_score}', True, 'black')
		screen.blit(score_text, (10, 410))
		screen.blit(high_score_text, (10, 450))
		pass


	# draw tiles for game
	def draw_pieces(board):
		for i in range(4):
			for j in range(4):
				value = board[i][j]
				if value > 27:
					value_color = colors['light text']
				else:
					value_color = colors['dark text']
				if value <= 177147 :
					color = colors[value]
				else:
					color = colors['other']
				pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
				if value > 0:
					value_len = len(str(value))
					font = pygame.font.Font('freesansbold.ttf', 48 - (8 * value_len))
					value_text = font.render(str(value), True, value_color)
					text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
					screen.blit(value_text, text_rect)
					pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


	# main game loop
	run = True
	while run:
		timer.tick(fps)
		screen.fill('white')
		draw_board()
		draw_pieces(board_values)
		if spawn_new or init_count < 3:
			board_values, game_over = new_pieces(board_values)
			spawn_new = False
			init_count += 1
		if direction != '':
			board_values = take_turn(direction, board_values)
			direction = ''
			spawn_new = True
		if game_over:
			draw_over()
			if high_score > init_high:
				file = open('/Users/anushka/Codes/python/mini project/high_score .txt', 'w')
				file.write(f'{high_score}')
				file.close()
				init_high = high_score

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					direction = 'UP'
				elif event.key == pygame.K_DOWN:
					direction = 'DOWN'
				elif event.key == pygame.K_LEFT:
					direction = 'LEFT'
				elif event.key == pygame.K_RIGHT:
					direction = 'RIGHT'

				if game_over:
					if event.key == pygame.K_RETURN:
						board_values = [[0 for _ in range(4)] for _ in range(4)]
						spawn_new = True
						init_count = 0
						score = 0
						direction = ''
						game_over = False

		if score > high_score:
			high_score = score

		pygame.display.flip()
	sys.exit()
