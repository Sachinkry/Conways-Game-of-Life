import pygame
import sys
import time
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
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

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
button_start_stop = pygame.Rect((WINDOW_WIDTH - BUTTON_WIDTH) // 2, WINDOW_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)

# Game variables
running = True
simulation_running = False
board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(offset_x, offset_y):
    # Draw horizontal grid lines
    for i in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (offset_x, offset_y + i * CELL_SIZE), (offset_x + GRID_WIDTH * CELL_SIZE, offset_y + i * CELL_SIZE))

    # Draw vertical grid lines
    for j in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRID_LINE_COLOR, (offset_x + j * CELL_SIZE, offset_y), (offset_x + j * CELL_SIZE, offset_y + GRID_HEIGHT * CELL_SIZE))

def draw_board(offset_x, offset_y):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            color = WHITE if board[i][j] == 1 else BLACK
            rect = pygame.Rect(offset_x + j * CELL_SIZE, offset_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_button(button, text):
    pygame.draw.rect(screen, GRAY, button)  # Draw the button
    font = pygame.font.SysFont(None, 24)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button.center)
    screen.blit(text_surf, text_rect)

def toggle_cell(pos, offset_x, offset_y):
    x, y = pos
    x -= offset_x
    y -= offset_y
    if 0 <= x < GRID_WIDTH * CELL_SIZE and 0 <= y < GRID_HEIGHT * CELL_SIZE:
        j, i = x // CELL_SIZE, y // CELL_SIZE
        board[i][j] ^= 1  # XOR to toggle the cell state

def check_button_click(pos, button):
    return button.collidepoint(pos)

# ... [rest of your functions]
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

# Calculate offsets to center the grid in the window
offset_x = (WINDOW_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
offset_y = (WINDOW_HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if check_button_click(pos, button_start_stop):
                simulation_running = not simulation_running  # Toggle simulation
            else:
                toggle_cell(pos, offset_x, offset_y)

    screen.fill(BLACK)
    draw_board(offset_x, offset_y)
    draw_grid(offset_x, offset_y)
    draw_button(button_start_stop, "Start" if not simulation_running else "Stop")

    if simulation_running:
        board = next_board_state(board, GRID_WIDTH, GRID_HEIGHT)
        time.sleep(0.2)

    pygame.display.flip()

pygame.quit()
sys.exit()
