import json
import os
import subprocess
import sys
import pygame

# Instellingen
TITLE = "STANISLAS ARCADE"
KEYS_TO_START_GAMES = list("qerzxcuopbnm")
NAV_KEYS = {
    pygame.K_w: (-1, 0), pygame.K_s: (1, 0),
    pygame.K_a: (0, -1), pygame.K_d: (0, 1),
    pygame.K_i: (-1, 0), pygame.K_k: (1, 0),
    pygame.K_j: (0, -1), pygame.K_l: (0, 1),
}
TILE_WIDTH = 300
TILE_HEIGHT = 120
TILE_MARGIN = 20
FONT_SIZE = 32
COLUMNS = 3
VISIBLE_ROWS = 3
SCROLL_SPEED = 20  # pixels per frame

def find_games(base_path="."):
    games = []
    for item in os.listdir(base_path):
        path = os.path.join(base_path, item)
        meta_path = os.path.join(path, "metadata.json")
        main_path = os.path.join(path, "main.py")
        if os.path.isdir(path) and os.path.isfile(meta_path) and os.path.isfile(main_path):
            with open(meta_path, "r") as f:
                metadata = json.load(f)
            metadata["path"] = main_path
            metadata["cwd"] = path
            games.append(metadata)
    return games

def add_dummy_games(games, count=40):
    for i in range(count):
        games.append({
            "name": f"Demo Game {i+1}",
            "path": __file__,
            "cwd": "."
        })

def launch_game(path, cwd):
    if sys.platform.startswith("win"):
        subprocess.Popen(["python", path], cwd=cwd, shell=True)
    else:
        subprocess.Popen(["python3", path], cwd=cwd)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

games = find_games()
add_dummy_games(games)
rows = (len(games) + COLUMNS - 1) // COLUMNS
selected = [0, 0]
target_scroll_offset = 0
actual_scroll_offset = 0

def update_scroll_offset():
    global target_scroll_offset
    row = selected[0]
    middle_row = VISIBLE_ROWS // 2
    if row <= middle_row:
        target_scroll_offset = 0
    elif row >= rows - VISIBLE_ROWS + middle_row:
        target_scroll_offset = max(0, (rows - VISIBLE_ROWS) * (TILE_HEIGHT + TILE_MARGIN))
    else:
        target_scroll_offset = (row - middle_row) * (TILE_HEIGHT + TILE_MARGIN)

def draw_menu():
    screen.fill((0, 0, 0))
    title_surface = font.render(TITLE, True, (255, 255, 255))
    screen.blit(title_surface, (
        screen.get_width() // 2 - title_surface.get_width() // 2, 20))

    for index, game in enumerate(games):
        row = index // COLUMNS
        col = index % COLUMNS
        y = row * (TILE_HEIGHT + TILE_MARGIN) + 100 - actual_scroll_offset
        if y + TILE_HEIGHT < 100 or y > screen.get_height():
            continue
        x = col * (TILE_WIDTH + TILE_MARGIN) + \
            (screen.get_width() - (COLUMNS * TILE_WIDTH + (COLUMNS - 1) * TILE_MARGIN)) // 2

        color = (100, 100, 255) if [row, col] == selected else (50, 50, 50)
        pygame.draw.rect(screen, color, (x, y, TILE_WIDTH, TILE_HEIGHT))
        name_surface = font.render(game.get("name", "Unnamed"), True, (255, 255, 255))
        text_x = x + TILE_WIDTH // 2 - name_surface.get_width() // 2
        text_y = y + TILE_HEIGHT // 2 - name_surface.get_height() // 2
        screen.blit(name_surface, (text_x, text_y))

    pygame.display.flip()

running = True
while running:
    draw_menu()

    # Smooth scroll
    if actual_scroll_offset < target_scroll_offset:
        actual_scroll_offset = min(actual_scroll_offset + SCROLL_SPEED, target_scroll_offset)
    elif actual_scroll_offset > target_scroll_offset:
        actual_scroll_offset = max(actual_scroll_offset - SCROLL_SPEED, target_scroll_offset)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode in KEYS_TO_START_GAMES:
                index = KEYS_TO_START_GAMES.index(event.unicode)
                if index < len(games):
                    game = games[index]
                    launch_game(game["path"], game["cwd"])
            elif event.key in NAV_KEYS:
                row_offset, col_offset = NAV_KEYS[event.key]
                new_row = max(0, min(rows - 1, selected[0] + row_offset))
                new_col = max(0, min(COLUMNS - 1, selected[1] + col_offset))
                if new_row * COLUMNS + new_col < len(games):
                    selected = [new_row, new_col]
                    update_scroll_offset()
            elif event.key == pygame.K_ESCAPE:
                running = False

    clock.tick(60)

pygame.quit()
