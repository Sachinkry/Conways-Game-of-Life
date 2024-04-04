import pygame
import sys
import time
from pygame.locals import QUIT

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_SIZE = 20  # Set cell size to 10 for a 50x20 grid

# Grid dimensions
GRID_WIDTH = 50
GRID_HEIGHT = 20

# Window size
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Define the grid line color
GRID_LINE_COLOR = (40, 40, 40)  # A dark gray color for the grid lines

# Set up the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

def draw_board(board, offset_x, offset_y):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            color = WHITE if board[i][j] == 1 else BLACK
            rect = pygame.Rect(offset_x + j * CELL_SIZE, offset_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

    # Draw horizontal grid lines
    for i in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (offset_x, offset_y + i * CELL_SIZE), (offset_x + GRID_WIDTH * CELL_SIZE, offset_y + i * CELL_SIZE))

    # Draw vertical grid lines
    for j in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (offset_x + j * CELL_SIZE, offset_y), (offset_x + j * CELL_SIZE, offset_y + GRID_HEIGHT * CELL_SIZE))



def count_live_neighbors(board, row, col, grid_width, grid_height):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < grid_height and 0 <= c < grid_width and board[r][c] == 1:
                count += 1
    return count

def next_board_state(board, grid_width, grid_height):
    new_board = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for i in range(grid_height):
        for j in range(grid_width):
            live_neighbors = count_live_neighbors(board, i, j, grid_width, grid_height)
            if board[i][j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_board[i][j] = 0
                else:
                    new_board[i][j] = 1
            else:
                if live_neighbors == 3:
                    new_board[i][j] = 1
    return new_board

def load_board_state(file_path):
  with open(file_path, 'r') as file:
      lines = file.readlines()

  board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

  # Calculate offset to center the board state from the file
  lines_height = len(lines)
  lines_width = max(len(line.strip()) for line in lines)
  offset_x = (GRID_WIDTH - lines_width) // 2
  offset_y = (GRID_HEIGHT - lines_height) // 2

  for i, line in enumerate(lines):
      for j, cell in enumerate(line.strip()):
          board[offset_y + i][offset_x + j] = int(cell)

  return board

# Load the initial board state from a file and calculate offsets
initial_state = load_board_state("./beacon.txt")
# initial_state = load_board_state("./toad.txt")

# Calculate offsets to center the grid in the window
offset_x = (WINDOW_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
offset_y = (WINDOW_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2

# Game loop
board = initial_state
running = True
while running:
  for event in pygame.event.get():
      if event.type == QUIT:
          running = False

  screen.fill(BLACK)
  draw_board(board, offset_x, offset_y)
  board = next_board_state(board, GRID_WIDTH, GRID_HEIGHT)
  pygame.display.flip()
  time.sleep(0.2)

pygame.quit()
sys.exit()