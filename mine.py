import pygame
import random
import sys

# Oyun parametrləri
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 15
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 30

# Rənglər
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 128)
GOLD = (255, 215, 0)
DARK_GRAY = (50, 50, 50)

# Retro rənglər
RETRO_COLORS = [(200, 30, 30), (30, 200, 30), (30, 30, 200), (200, 200, 30), (200, 30, 200), (30, 200, 200)]

# Şəkilləri yüklə
BOMB_IMAGE = pygame.image.load(r'c:\Users\user\Pictures\Screenshots\Ekran görüntüsü 2024-09-01 192415.png')  # Şəkil yolunu dəyişdirin
BOMB_IMAGE = pygame.transform.scale(BOMB_IMAGE, (TILE_SIZE, TILE_SIZE))
BACKGROUND_IMAGE = pygame.image.load(r'c:\Users\user\Pictures\Screenshots\Ekran görüntüsü 2024-09-01 193657.png')  # Şəkil yolunu dəyişdirin
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Çətinlik səviyyələrinə görə mina sayıları
DIFFICULTY_LEVELS = {
    'Easy': 10,
    'Medium': 20,
    'Hard': 35
}

def create_grid(num_mines):
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < num_mines:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[y][x] = -1
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= x + i < GRID_SIZE and 0 <= y + j < GRID_SIZE and grid[y + j][x + i] != -1:
                        grid[y + j][x + i] += 1
    return grid

def draw_grid(screen, grid, revealed, mines=None):
    current_time = pygame.time.get_ticks()
    color_index = (current_time // 500) % len(RETRO_COLORS)
    color = RETRO_COLORS[color_index]

    font = pygame.font.SysFont('courier', 24, bold=True)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x, y) in revealed:
                pygame.draw.rect(screen, WHITE, rect)
                if grid[y][x] == -1:
                    screen.blit(BOMB_IMAGE, rect.topleft)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, color)
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
    if mines:
        for (x, y) in mines:
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(BOMB_IMAGE, rect.topleft)
            pygame.draw.rect(screen, BLACK, rect, 2)

def draw_start_menu(screen):
    screen.fill(DARK_GRAY)
    font_title = pygame.font.Font(None, 74)
    font_button = pygame.font.Font(None, 50)

    title = font_title.render('Minesweeper', True, GOLD)
    
    easy_text = font_button.render('Easy', True, WHITE)
    medium_text = font_button.render('Medium', True, WHITE)
    hard_text = font_button.render('Hard', True, WHITE)
    settings_text = font_button.render('Settings', True, WHITE)
    
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    easy_rect = easy_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    medium_rect = medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    hard_rect = hard_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    
    pygame.draw.rect(screen, DARK_BLUE, easy_rect.inflate(20, 20))
    pygame.draw.rect(screen, DARK_BLUE, medium_rect.inflate(20, 20))
    pygame.draw.rect(screen, DARK_BLUE, hard_rect.inflate(20, 20))
    pygame.draw.rect(screen, DARK_BLUE, settings_rect.inflate(20, 20))
    
    screen.blit(title, title_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    screen.blit(settings_text, settings_rect)
    
    return {'Easy': easy_rect, 'Medium': medium_rect, 'Hard': hard_rect, 'Settings': settings_rect}

def draw_settings_menu(screen):
    screen.fill(DARK_GRAY)
    font_title = pygame.font.Font(None, 50)
    font_button = pygame.font.Font(None, 40)

    title = font_title.render('Settings', True, GOLD)
    back_text = font_button.render('Back', True, WHITE)
    volume_text = font_button.render('Volume: 50%', True, WHITE)
    developer_text = font_button.render('Developed by Valeh & Sedi', True, WHITE)
    
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    volume_rect = volume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    developer_rect = developer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    pygame.draw.rect(screen, DARK_BLUE, back_rect.inflate(20, 20))
    
    screen.blit(title, title_rect)
    screen.blit(volume_text, volume_rect)
    screen.blit(developer_text, developer_rect)
    screen.blit(back_text, back_rect)

    return back_rect

def draw_game_over(screen, revealed, grid, mines):
    font = pygame.font.SysFont('courier', 48, bold=True)
    game_over_text = font.render('Game Over', True, WHITE)
    restart_text = font.render('Restart', True, WHITE)
    exit_text = font.render('Exit', True, WHITE)
    
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2))
    
    draw_grid(screen, grid, revealed, mines)
    
    pygame.draw.rect(screen, BLACK, game_over_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, restart_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, exit_rect.inflate(20, 20))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(exit_text, exit_rect)
    
    return restart_rect, exit_rect

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    def reset_game(difficulty='Medium'):
        nonlocal grid, revealed, mines, game_started, game_over, in_settings
        num_mines = DIFFICULTY_LEVELS[difficulty]
        grid = create_grid(num_mines)
        mines = {(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[y][x] == -1}
        revealed = set()
        game_started = True
        game_over = False
        in_settings = False

    game_started = False
    game_over = False
    revealed = set()
    mines = set()
    grid = create_grid(DIFFICULTY_LEVELS['Medium'])
    in_settings = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if in_settings:
                    back_rect = draw_settings_menu(screen)
                    if back_rect.collidepoint(pos):
                        in_settings = False
                elif not game_started:
                    difficulty_rects = draw_start_menu(screen)
                    for difficulty, rect in difficulty_rects.items():
                        if rect.collidepoint(pos):
                            if difficulty == 'Settings':
                                in_settings = True
                            else:
                                reset_game(difficulty)
                else:
                    if game_over:
                        restart_rect, exit_rect = draw_game_over(screen, revealed, grid, mines)
                        if restart_rect.collidepoint(pos):
                            reset_game()
                        elif exit_rect.collidepoint(pos):
                            game_started = False
                    else:
                        x, y = pos[0] // TILE_SIZE, pos[1] // TILE_SIZE
                        if grid[y][x] == -1:
                            game_over = True
                        else:
                            to_reveal = [(x, y)]
                            while to_reveal:
                                cx, cy = to_reveal.pop()
                                if (cx, cy) in revealed:
                                    continue
                                revealed.add((cx, cy))
                                if grid[cy][cx] == 0:
                                    for i in range(-1, 2):
                                        for j in range(-1, 2):
                                            if 0 <= cx + i < GRID_SIZE and 0 <= cy + j < GRID_SIZE:
                                                to_reveal.append((cx + i, cy + j))

        screen.fill(WHITE)
        if in_settings:
            draw_settings_menu(screen)
        elif not game_started:
            draw_start_menu(screen)
        else:
            if game_over:
                draw_game_over(screen, revealed, grid, mines)
            else:
                draw_grid(screen, grid, revealed)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
























