import pygame
import sys
import json
import xml
import Menu
from bs4 import BeautifulSoup

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
GRID_SIZE = 32

with open('Bricks.xml', 'r') as f:
    brick_data = f.read()

# Holds the last saved bricks data when Ctrl+S is pressed
saved_bricks_data = []


def main(screen, debug=True):
    global SCREEN, CLOCK, brick_data, brick_rect, saved_bricks_data
    pygame.init()
    if debug == True:
        SCREEN = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    else:
        SCREEN = screen
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    key_pressed = pygame.key.get_pressed()
    spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
    Bs_data = BeautifulSoup(brick_data, "xml")
    bricks = Bs_data.find_all('SubTexture', {'cracked': 'false'})
    placed_bricks = []
    # create a palette brick from the first available texture
    if bricks:
        first = bricks[0]
        y = int(first.get('y'))
        x = int(first.get('x'))
    else:
        x, y = 772, 390
    brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
    brick_img.blit(spritesheet, (0, 0), (x, y, 384, 128))
    brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
    brick_rect = brick_img.get_rect(topleft=(0, 0))
    brick_img_draging = False
    dragging_placed = None

    while True:
        SCREEN.fill(BLACK)
        drawGrid()
        # draw placed bricks
        for b in placed_bricks:
            SCREEN.blit(b['surf'], b['rect'])
        # draw the draggable palette brick on top

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    # check placed bricks from topmost to bottom
                    for i in range(len(placed_bricks) - 1, -1, -1):
                        if placed_bricks[i]['rect'].collidepoint(event.pos):
                            # bring this brick to top
                            placed_bricks.append(placed_bricks.pop(i))
                            dragging_placed = len(placed_bricks) - 1
                            offset_x = placed_bricks[dragging_placed]['rect'].x - mouse_x
                            offset_y = placed_bricks[dragging_placed]['rect'].y - mouse_y
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # stop dragging either placed brick or palette
                    if dragging_placed is not None:
                        # snap placed brick to grid
                        placed_bricks[dragging_placed]['rect'].x = round(
                            placed_bricks[dragging_placed]['rect'].x / GRID_SIZE) * GRID_SIZE
                        placed_bricks[dragging_placed]['rect'].y = round(
                            placed_bricks[dragging_placed]['rect'].y / GRID_SIZE) * GRID_SIZE
                        dragging_placed = None
                    if brick_img_draging:
                        brick_img_draging = False
                        brick_rect.x = round(
                            brick_rect.x / GRID_SIZE) * GRID_SIZE
                        brick_rect.y = round(
                            brick_rect.y / GRID_SIZE) * GRID_SIZE

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if dragging_placed is not None:
                    placed_bricks[dragging_placed]['rect'].x = mouse_x + offset_x
                    placed_bricks[dragging_placed]['rect'].y = mouse_y + offset_y
                elif brick_img_draging:
                    brick_rect.x = mouse_x + offset_x
                    brick_rect.y = mouse_y + offset_y

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                saved = []
                for b in placed_bricks:
                    bx = b['rect'].x
                    by = b['rect'].y
                    bid = b.get('id', None)
                    sprite_x = None
                    sprite_y = None
                    if bid is not None:
                        try:
                            n = int(bid)
                            idx = (n - 1) if n > 0 else 9
                            if 0 <= idx < len(bricks):
                                sprite_y = int(bricks[idx].get('y'))
                                sprite_x = int(bricks[idx].get('x'))
                        except Exception:
                            pass
                    saved.append({'x': bx, 'y': by, 'id': bid,
                                 'sprite_x': sprite_x, 'sprite_y': sprite_y})
                saved_bricks_data = saved
                # write to JSON file
                file_name = "/workspaces/2526-v4in2-pygame-haoxuan-simon-1/levels/" + \
                    input("data file name: ")+".json"
                try:
                    with open(file_name, 'w') as data_file:
                        json.dump(saved_bricks_data, data_file, indent=2)
                    print(
                        f"Saved {len(saved_bricks_data)} bricks to '{file_name}'")
                except Exception as e:
                    print(f"Failed to save JSON: {e}")

            elif event.type == pygame.KEYDOWN and event.unicode.isdigit():

                n = int(event.unicode)

                idx = (n - 1) if n > 0 else 9
                if 0 <= idx < len(bricks):
                    by = int(bricks[idx].get('y'))
                    bx = int(bricks[idx].get('x'))
                    surf = pygame.Surface((384, 128), pygame.SRCALPHA)
                    surf.blit(spritesheet, (0, 0), (bx, by, 384, 128))
                    surf = pygame.transform.scale(
                        surf, (BRICK_WIDTH, BRICK_HEIGHT))

                    mx, my = pygame.mouse.get_pos()
                    new_rect = surf.get_rect(
                        topleft=(round(mx / GRID_SIZE) * GRID_SIZE, round(my / GRID_SIZE) * GRID_SIZE))
                    placed_bricks.append(
                        {'id': n, 'surf': surf, 'rect': new_rect})

        pygame.display.update()


def drawGrid():
    blockSize = 32  # Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
