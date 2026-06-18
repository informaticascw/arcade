from pathlib import Path

content = '''#
# BREAKOUT GAME
#

import pygame

FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 122
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

PADDLE_Y = 640
PADDLE_SPEED = 10
INITIAL_BALL_SPEED_X = 6
INITIAL_BALL_SPEED_Y = -10

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption('Breakout')
fps_clock = pygame.time.Clock()

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))


def create_bricks():
    bricks = []
    for row in range(2):
        for col in range(12):
            x = 96 + col * BRICK_WIDTH
            y = 32 + row * BRICK_HEIGHT
            bricks.append(pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks


def reset_game():
    paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
    ball_x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
    ball_y = PADDLE_Y - BALL_HEIGHT - 4
    ball_speed_x = INITIAL_BALL_SPEED_X
    ball_speed_y = INITIAL_BALL_SPEED_Y
    return paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y


bricks = create_bricks()
paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y = reset_game()
game_started = False
game_status_msg = ""

print('mygame is running')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                if game_status_msg:
                    bricks = create_bricks()
                    paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y = reset_game()
                    game_status_msg = ""
                game_started = True

    keys = pygame.key.get_pressed()

    if game_started and not game_status_msg:
        ball_x += ball_speed_x
        ball_y += ball_speed_y

    if not game_started and not game_status_msg:
        ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
        ball_y = PADDLE_Y - BALL_HEIGHT - 4

    ball_rect = pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_HEIGHT)
    paddle_rect = pygame.Rect(paddle_x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

    if ball_rect.left < 0:
        ball_rect.left = 0
        ball_speed_x = abs(ball_speed_x)
    if ball_rect.right > SCREEN_WIDTH:
        ball_rect.right = SCREEN_WIDTH
        ball_speed_x = -abs(ball_speed_x)
    if ball_rect.top < 0:
        ball_rect.top = 0
        ball_speed_y = abs(ball_speed_y)

    if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
        ball_rect.bottom = paddle_rect.top
        ball_speed_y = -abs(ball_speed_y)

    for brick in bricks[:]:
        if ball_rect.colliderect(brick):
            overlap_x = min(ball_rect.right, brick.right) - max(ball_rect.left, brick.left)
            overlap_y = min(ball_rect.bottom, brick.bottom) - max(ball_rect.top, brick.top)
            if overlap_x < overlap_y:
                ball_speed_x = -ball_speed_x
            else:
                ball_speed_y = -ball_speed_y
            bricks.remove(brick)
            break

    if ball_rect.top > SCREEN_HEIGHT:
        game_status_msg = 'You lost!'
        game_started = False
        ball_speed_x = 0
        ball_speed_y = 0

    if not bricks and not game_status_msg:
        game_status_msg = 'You won!'
        game_started = False

    if keys[pygame.K_d]:
        paddle_x += PADDLE_SPEED
    elif keys[pygame.K_a]:
        paddle_x -= PADDLE_SPEED

    paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))

    screen.fill('blue')
    screen.blit(ball_img, (ball_rect.x, ball_rect.y))
    screen.blit(paddle_img, (paddle_rect.x, paddle_rect.y))
    for brick in bricks:
        screen.blit(brick_img, (brick.x, brick.y))

    if game_status_msg:
        status_img = font.render(game_status_msg, True, 'red')
        screen.blit(status_img, ((SCREEN_WIDTH - status_img.get_width()) / 2, SCREEN_HEIGHT / 2))

    if not game_started and not game_status_msg:
        start_img = font.render('PRESS ANY KEY', True, 'white')
        screen.blit(start_img, ((SCREEN_WIDTH - start_img.get_width()) / 2, SCREEN_HEIGHT / 2 - 100))
    elif game_status_msg:
        restart_img = font.render('PRESS ANY KEY TO RESTART', True, 'white')
        screen.blit(restart_img, ((SCREEN_WIDTH - restart_img.get_width()) / 2, SCREEN_HEIGHT / 2 + 60))

    pygame.display.flip()
    fps_clock.tick(FPS)

pygame.quit()
print('mygame stopt running')
'''
Path('main.py').write_text(content, encoding='utf-8')
