import pygame
import random
import time
import json

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)  # Color for the grid lines

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("start.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))



# Font setup
font = pygame.font.Font(None, 36)

def create_grid():
    return [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[i][j], (j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def new_piece(fall_speed):
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {
        'shape': shape,
        'color': color,
        'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0,
        'fall_time': 0,
        'fall_speed': fall_speed
    }

def valid_move(grid, piece, x, y):
    for i, row in enumerate(piece['shape']):
        for j, cell in enumerate(row):
            if cell:
                if (x + j < 0 or x + j >= GRID_WIDTH or
                    y + i >= GRID_HEIGHT or
                    grid[y + i][x + j] != BLACK):
                    return False
    return True

def merge_piece(grid, piece):
    for i, row in enumerate(piece['shape']):
        for j, cell in enumerate(row):
            if cell:
                grid[piece['y'] + i][piece['x'] + j] = piece['color']

def remove_full_rows(grid):
    full_rows = [i for i, row in enumerate(grid) if all(cell != BLACK for cell in row)]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    return len(full_rows)

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_start_screen():
    # Display the background image
    screen.blit(background_image, (0, 0))

    draw_text("TETRIS", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Press any key to begin", 22, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

def show_game_over_screen(score):
    screen.fill(BLACK)
    draw_text("GAME OVER", 64, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(f"Score: {score}", 22, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press any key to play again", 22, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

def get_player_name():
    name = ""
    done = False
    while not done:
        screen.fill(BLACK)
        draw_text("Enter your name:", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(name, 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press ENTER when done", 22, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name

def load_high_score():
    try:
        with open('high_score.json', 'r') as f:
            data = json.load(f)
            return data['score'], data['name']
    except FileNotFoundError:
        return 0, ""

def save_high_score(score, name):
    with open('high_score.json', 'w') as f:
        json.dump({'score': score, 'name': name}, f)

def draw_fancy_square(x, y, color):
    """Draw a fancier square with rounded corners and a gradient effect."""
    # Draw the base square
    pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 0, border_radius=8)
    
    # Draw a lighter border around the square to give a 3D effect
    border_color = tuple(min(255, c + 50) for c in color)  # Lighter shade
    pygame.draw.rect(screen, border_color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 2, border_radius=8)
    
    # Draw a darker border inside the square to enhance the 3D effect
    inner_rect = (x + 4, y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8)
    inner_border_color = tuple(max(0, c - 50) for c in color)  # Darker shade
    pygame.draw.rect(screen, inner_border_color, inner_rect, 2, border_radius=8)

def main():
    high_score, high_score_name = load_high_score()

    while True:
        if not show_start_screen():
            return

        grid = create_grid()
        base_fall_speed = 0.5  # Starting fall speed
        current_piece = new_piece(base_fall_speed)
        score = 0
        last_fall_time = time.time()
        fast_fall = False
        last_speed_increase = 0  # Track when we last increased the speed
        
        while True:
            current_time = time.time()
            delta_time = current_time - last_fall_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if valid_move(grid, current_piece, current_piece['x'] - 1, current_piece['y']):
                            current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT:
                        if valid_move(grid, current_piece, current_piece['x'] + 1, current_piece['y']):
                            current_piece['x'] += 1
                    if event.key == pygame.K_DOWN:
                        fast_fall = True
                    if event.key == pygame.K_UP:
                        rotated = list(zip(*current_piece['shape'][::-1]))
                        if valid_move(grid, {'shape': rotated, 'x': current_piece['x'], 'y': current_piece['y']}, current_piece['x'], current_piece['y']):
                            current_piece['shape'] = rotated
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        fast_fall = False

            # Calculate current fall speed
            current_fall_speed = 0.05 if fast_fall else current_piece['fall_speed']

            current_piece['fall_time'] += delta_time
            if current_piece['fall_time'] >= current_fall_speed:
                if valid_move(grid, current_piece, current_piece['x'], current_piece['y'] + 1):
                    current_piece['y'] += 1
                    current_piece['fall_time'] = 0
                else:
                    merge_piece(grid, current_piece)
                    rows_cleared = remove_full_rows(grid)
                    score += rows_cleared * 100
                    
                    # Increase fall speed every 1000 points
                    if score // 1000 > last_speed_increase:
                        base_fall_speed = max(0.1, base_fall_speed * 0.9)  # Increase speed by 10%, but not faster than 0.1
                        last_speed_increase = score // 1000
                    
                    current_piece = new_piece(base_fall_speed)
                    fast_fall = False
                    if not valid_move(grid, current_piece, current_piece['x'], current_piece['y']):
                        if score > high_score:
                            high_score = score
                            high_score_name = get_player_name()
                            save_high_score(high_score, high_score_name)
                        if not show_game_over_screen(score):
                            return
                        break

            screen.fill(BLACK)
            draw_grid(grid)
            for i, row in enumerate(current_piece['shape']):
                for j, cell in enumerate(row):
                    if cell:
                        draw_fancy_square(
                            (current_piece['x'] + j) * BLOCK_SIZE,
                            (current_piece['y'] + i) * BLOCK_SIZE,
                            current_piece['color']
                        )

            # Draw score
            draw_text(f"Score: {score}", 22, WHITE, SCREEN_WIDTH // 2, 10)
            
            # Draw high score
            if high_score > 0:
                draw_text(f"High Score: {high_score} ({high_score_name})", 22, WHITE, SCREEN_WIDTH // 2, 40)

            pygame.display.flip()
            clock.tick(60)  # Maintain 60 FPS for smooth animation
            last_fall_time = current_time

if __name__ == '__main__':
    main()