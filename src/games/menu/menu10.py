import os
import json
import math
import subprocess
import pygame

# --- CONFIGURATION ---
TITLE = "STANISLAS ARCADE"
FONT_SIZE = 32
TITLE_FONT_SIZE = 64
TILE_WIDTH, TILE_HEIGHT = 300, 160
TILE_MARGIN = 30
COLUMNS = 3
VISIBLE_ROWS = 3
SCROLL_SPEED = 20
START_FILE = "main.py"
GAMES_DIR = "."
KEYS_TO_START_GAMES = list("qerzxcuopbnm")
NAV_KEYS = {
    pygame.K_w: (-1, 0), pygame.K_s: (1, 0),
    pygame.K_a: (0, -1), pygame.K_d: (0, 1),
    pygame.K_i: (-1, 0), pygame.K_k: (1, 0),
    pygame.K_j: (0, -1), pygame.K_l: (0, 1),
}

# --- GAME DISCOVERY ---
def find_games(base_path):
    games = []
    for name in os.listdir(base_path):
        folder = os.path.join(base_path, name)
        meta = os.path.join(folder, "metadata.json")
        start = os.path.join(folder, START_FILE)
        if os.path.isdir(folder) and os.path.isfile(meta) and os.path.isfile(start):
            with open(meta) as f:
                data = json.load(f)
            data["path"] = start
            games.append(data)
    return games

# --- GAME LAUNCH ---
def launch_game(path):
    cwd = os.path.dirname(path)
    cmd = f'cd "{cwd}" && python3 "{os.path.basename(path)}"'
    subprocess.run(cmd, shell=True)

# --- MENU LOGIC ---
def get_rows(game_count):
    return math.ceil(game_count / COLUMNS)

def get_scroll_offset(selected_row, total_rows):
    mid = VISIBLE_ROWS // 2
    max_offset = max(0, (total_rows - VISIBLE_ROWS) * (TILE_HEIGHT + TILE_MARGIN))
    if selected_row <= mid:
        return 0
    elif selected_row >= total_rows - VISIBLE_ROWS + mid:
        return max_offset
    else:
        return (selected_row - mid) * (TILE_HEIGHT + TILE_MARGIN)

# --- DRAWING ---
def draw_menu(screen, fonts, games, selected, scroll_offset, dims):
    screen.fill((0, 0, 0))
    title_font, font = fonts
    width, top_margin, max_menu_height = dims

    # Draw title
    title = title_font.render(TITLE, True, (255, 255, 255))
    screen.blit(title, (width // 2 - title.get_width() // 2, 20))

    # Draw game tiles
    for idx, game in enumerate(games):
        row, col = divmod(idx, COLUMNS)
        y = row * (TILE_HEIGHT + TILE_MARGIN) + top_margin - scroll_offset
        if y + TILE_HEIGHT < top_margin or y > top_margin + max_menu_height:
            continue
        x = col * (TILE_WIDTH + TILE_MARGIN) + (width - (COLUMNS * TILE_WIDTH + (COLUMNS - 1) * TILE_MARGIN)) // 2
        color = (100, 100, 255) if [row, col] == selected else (50, 50, 50)
        pygame.draw.rect(screen, color, (x, y, TILE_WIDTH, TILE_HEIGHT))
        name = font.render(game.get("name", "Unnamed"), True, (255, 255, 255))
        screen.blit(name, (x + TILE_WIDTH // 2 - name.get_width() // 2, y + TILE_HEIGHT // 2 - name.get_height() // 2))

    # Draw scrollbar
    total_rows = get_rows(len(games))
    content_height = total_rows * (TILE_HEIGHT + TILE_MARGIN)
    if content_height > max_menu_height:
        bar_x = width - 40
        view_height = max_menu_height
        scrollbar_height = view_height * (view_height / content_height)
        max_scroll = content_height - view_height
        scroll_ratio = scroll_offset / max_scroll if max_scroll else 0
        scrollbar_y = top_margin + scroll_ratio * (view_height - scrollbar_height)
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, top_margin, 10, view_height))
        pygame.draw.rect(screen, (180, 180, 180), (bar_x, scrollbar_y, 10, scrollbar_height))

    pygame.display.flip()

# --- MAIN LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(TITLE)
    font = pygame.font.SysFont(None, FONT_SIZE)
    title_font = pygame.font.SysFont(None, TITLE_FONT_SIZE)
    clock = pygame.time.Clock()
    width, height = screen.get_size()
    top_margin = TITLE_FONT_SIZE + 40
    max_menu_height = VISIBLE_ROWS * TILE_HEIGHT + (VISIBLE_ROWS - 1) * TILE_MARGIN

    games = find_games(GAMES_DIR)
    selected = [0, 0]
    scroll_offset = 0
    target_scroll_offset = 0
    total_rows = get_rows(len(games))

    running = True
    while running:
        draw_menu(screen, (title_font, font), games, selected, scroll_offset, (width, top_margin, max_menu_height))

        # Smooth scroll
        if scroll_offset < target_scroll_offset:
            scroll_offset = min(scroll_offset + SCROLL_SPEED, target_scroll_offset)
        elif scroll_offset > target_scroll_offset:
            scroll_offset = max(scroll_offset - SCROLL_SPEED, target_scroll_offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode in KEYS_TO_START_GAMES:
                    idx = KEYS_TO_START_GAMES.index(event.unicode)
                    if idx < len(games):
                        launch_game(games[idx]["path"])
                elif event.key in NAV_KEYS:
                    dr, dc = NAV_KEYS[event.key]
                    nr = max(0, min(total_rows - 1, selected[0] + dr))
                    nc = max(0, min(COLUMNS - 1, selected[1] + dc))
                    if nr * COLUMNS + nc < len(games):
                        selected = [nr, nc]
                        target_scroll_offset = get_scroll_offset(nr, total_rows)
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
