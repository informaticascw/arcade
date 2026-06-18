#
# BREAKOUT GAME
#

import pygame
import time

#
# definitions
#

FPS = 60  # Frames per seconde
SCREEN_WIDTH = 1280  # schermgrootte x in pixels
SCREEN_HEIGHT = 720  # schermgrootte y in pixels
BALL_WIDTH = 16  # balgrootte x in pixels
BALL_HEIGHT = 16  # balgrootte y in pixels
PADDLE_WIDTH = 144  # plankgrootte x in pixels
PADDLE_HEIGHT = 32  # plankgrootte y in pixels
PADDLE_SPEED = 6
BRICK_WIDTH = 96  # blokgrootte x in pixels
BRICK_HEIGHT = 32  # blokgrootte y in pixels
SPEED_INCREASE = 1.02
MAX_SPEED = 12
LIVES = 3
LEVEL = 1
MAX_LEVEL = 5

bricks_x = [
    236, 332, 428, 524, 620, 716, 812, 908,
    236, 332, 428, 524, 620, 716, 812, 908,
    236, 332, 428, 524, 620, 716, 812, 908
]

bricks_y = [
    80, 80, 80, 80, 80, 80, 80, 80,
    112, 112, 112, 112, 112, 112, 112, 112,
    144, 144, 144, 144, 144, 144, 144, 144
]


def load_level(level):

    global bricks_x
    global bricks_y

    if level == 1:

        bricks_x = [
            236, 332, 428, 524, 620, 716, 812, 908,
            236, 332, 428, 524, 620, 716, 812, 908,
            236, 332, 428, 524, 620, 716, 812, 908
        ]

        bricks_y = [
            80, 80, 80, 80, 80, 80, 80, 80,
            112, 112, 112, 112, 112, 112, 112, 112,
            144, 144, 144, 144, 144, 144, 144, 144
        ]

    elif level == 2:

        bricks_x = [
            524,
            428, 524, 620,
            332, 428, 524, 620, 716,
            236, 332, 428, 524, 620, 716, 812
        ]

        bricks_y = [
            80,
            112, 112, 112,
            144, 144, 144, 144, 144,
            176, 176, 176, 176, 176, 176, 176
        ]

    elif level == 3:

        bricks_x = [
            236, 908,
            332, 812,
            428, 716,
            524, 620
        ]

        bricks_y = [
            80, 80,
            112, 112,
            144, 144,
            176, 176
        ]


load_level(LEVEL)

paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2

paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 20

ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2  # ballocatie x in pixels
ball_speed_x = 3.5  # balsnelheid in pixels per frame

ball_y = paddle_y - BALL_HEIGHT - 10
ball_speed_y = 3.5


#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
titel_font = pygame.font.Font('PressStart2P-Regular.ttf', 48)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  # invoegen van plaatje
# plaatje invoegen links boven
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(  # plaatje anders maken
    paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (0, 390, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

#
# startmenu
#


game_started = False

while not game_started:

    #
    # lees events
    #

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        GAME_MODE = 1
        game_started = True

    if keys[pygame.K_r]:
        GAME_MODE = 2
        game_started = True

    #
    # teken menu
    #

    screen.fill('#f0c5e9')

    titel_img = titel_font.render('BREAKOUT', True, 'purple')

    uitleg1_img = font.render('Breek alle blokken', True, 'purple')
    uitleg2_img = font.render('Je hebt 3 levens', True, 'purple')

    besturing1_img = font.render('A = naar links', True, 'purple')
    besturing2_img = font.render('D = naar recht', True, 'purple')

    start_img = font.render('Druk op Q om te starten', True, 'purple')

    screen.blit(
        titel_img,
        ((SCREEN_WIDTH - titel_img.get_width()) / 2, 120)
    )

    screen.blit(
        uitleg1_img,
        ((SCREEN_WIDTH - uitleg1_img.get_width()) / 2, 250)
    )

    screen.blit(
        uitleg2_img,
        ((SCREEN_WIDTH - uitleg2_img.get_width()) / 2, 300)
    )

    screen.blit(
        besturing1_img,
        ((SCREEN_WIDTH - besturing1_img.get_width()) / 2, 400)
    )

    screen.blit(
        besturing2_img,
        ((SCREEN_WIDTH - besturing2_img.get_width()) / 2, 450)
    )

    screen.blit(
        start_img,
        ((SCREEN_WIDTH - start_img.get_width()) / 2, 580)
    )

    pygame.display.flip()

    fps_clock.tick(FPS)

#
# game loop
#

print('mygame is running')
running = True
while running:
    #
    # read events
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    #
    # move everything
    #

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0:
        ball_speed_x = abs(ball_speed_x)
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:
        ball_speed_x = abs(ball_speed_x) * -1

    if ball_y < 0:
        ball_speed_y = abs(ball_speed_y)
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        ball_speed_y = abs(ball_speed_y) * -1

    # handle collisions
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        LIVES -= 1

        # reset bal
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_speed_x = 3.5
        ball_speed_y = -3.5

        time.sleep(0.3)

    # if dead or alive
    if ball_y + BALL_HEIGHT >= SCREEN_HEIGHT:
        game_status_msg = "You lost!"
    elif len(bricks_x) == 0:
        game_status_msg = "You won!"
    else:
        game_status_msg = "Spel is bezig"

    if LIVES <= 0:
        game_status_msg = "GAME OVER"
        ball_speed_x = 0
        ball_speed_y = 0

    # draw everything

    # clear screen
    screen.fill('#f0c5e9')

    # teken bal
    screen.blit(ball_img, (ball_x, ball_y))

    # draw game status message

    game_status_img = font.render(game_status_msg, True, 'purple')
    screen.blit(game_status_img,
                ((SCREEN_WIDTH - game_status_img.get_width()) / 2, 20))

    if len(bricks_x) == 0:

        LEVEL += 1

        if LEVEL <= MAX_LEVEL:

            load_level(LEVEL)

            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2

            ball_speed_x *= 1.2
            ball_speed_y *= 1.2

            time.sleep(1)

        else:

            ball_speed_x = 0
            ball_speed_y = 0

    lives_img = font.render("Lives: " + str(LIVES), True, 'purple')
    screen.blit(lives_img, (10, 10))

    level_img = font.render("Level: " + str(LEVEL), True, 'purple')
    screen.blit(level_img, (10, 50))

    # teken paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    for i in range(0, len(bricks_x)):  # teken alle blokken
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))

    paddle_x += (keys[pygame.K_d] - keys[pygame.K_a]) * PADDLE_SPEED

    if paddle_x < 0:  # paddle blijft in spel
        paddle_x = 0

    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
            ball_y < paddle_y + PADDLE_HEIGHT):

        # positie op paddle (-1 links, +1 rechts)
        hit_pos = ((ball_x + BALL_WIDTH / 2) -
                   (paddle_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)

        # sterkere hoeken
        ball_speed_x = hit_pos * abs(ball_speed_y) * 2

        # altijd omhoog stuiteren
        ball_speed_y = -abs(ball_speed_y)

    for i in range(0, len(bricks_x)):

        if (ball_x + BALL_WIDTH > bricks_x[i] and
            ball_x < bricks_x[i] + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > bricks_y[i] and
                ball_y < bricks_y[i] + BRICK_HEIGHT):

            print('brick touched at ball_x = ' + str(ball_x) +
                  ' and ball_y = ' + str(ball_y))

            # bounce richting
            if (ball_speed_y > 0 and ball_y < bricks_y[i]):
                ball_speed_y = -abs(ball_speed_y)

            elif (ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT):
                ball_speed_y = abs(ball_speed_y)

            elif (ball_speed_x > 0 and ball_x < bricks_x[i]):
                ball_speed_x = -abs(ball_speed_x)

            elif (ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH):
                ball_speed_x = abs(ball_speed_x)

            # blok verwijderen + snelheid verhogen
            bricks_x.pop(i)
            bricks_y.pop(i)

            ball_speed_x *= SPEED_INCREASE
            ball_speed_y *= SPEED_INCREASE

            # max speed
            if abs(ball_speed_x) > MAX_SPEED:
                ball_speed_x = MAX_SPEED if ball_speed_x > 0 else -MAX_SPEED

            if abs(ball_speed_y) > MAX_SPEED:
                ball_speed_y = MAX_SPEED if ball_speed_y > 0 else -MAX_SPEED

            break

    # show screen
    pygame.display.flip()

    #
    # wait until next frame
    #

    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
