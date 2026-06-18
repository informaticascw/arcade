#
# BREAKOUT GAME
#

import pygame
import time

#
# definitions
#

FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16

PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

BRICK_WIDTH = 96
BRICK_HEIGHT = 32

MAX_SPEED = 15
START_BALL_X = 100
START_BALL_Y = 30
START_BALL_SPEED_X = 6 * 1.4
START_BALL_SPEED_Y = -3 * 1.4
START_PADDLE_X = SCREEN_WIDTH / 2
PADDLE_Y = SCREEN_HEIGHT - 100
 
# startwaarden gebruikt om het spel te resetten bij een nieuwe poging
BRICKS_X_INIT = [70, 166, 262, 358, 454, 550, 646, 742, 838, 934,
                  100, 196, 292, 388, 484, 580, 676, 772,
                  130, 226, 322, 418, 514, 610]
BRICKS_Y_INIT = [70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                  102, 102, 102, 102, 102, 102, 102, 102,
                  134, 134, 134, 134, 134, 134]
BRICKS_COLOR_INIT = ["red", "red", "red", "red", "red", "red", "red", "red", "red", "red",
                      "green", "green", "green", "green", "green", "green", "green", "green",
                      "blue", "blue", "blue", "blue", "blue", "blue"]


# de originele stenen-layout
bricks_x = [70, 166, 262, 358, 454, 550, 646, 742, 838, 934,
                  100, 196, 292, 388, 484, 580, 676, 772,
                  130, 226, 322, 418, 514, 610]
bricks_y = [70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                  102, 102, 102, 102, 102, 102, 102, 102,
                  134, 134, 134, 134, 134, 134]
bricks_color = ["red", "red", "red", "red", "red", "red", "red", "red", "red", "red",
                      "green", "green", "green", "green", "green", "green", "green", "green",
                      "blue", "blue", "blue", "blue", "blue", "blue"]

# define global variables
game_status = "uitleg"

ball_x = 100
ball_speed_x = 6

ball_y = 30
ball_speed_y = -3

ball_speed_x *= 1.4
ball_speed_y *= 1.4

paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100

 
def reset_game():
    """Bal, paddle en stenen terug naar de startsituatie, voor een nieuwe poging."""
    global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x
    global bricks_x, bricks_y, bricks_color

    ball_x = START_BALL_X
    ball_y = START_BALL_Y
    ball_speed_x = START_BALL_SPEED_X
    ball_speed_y = START_BALL_SPEED_Y
    paddle_x = START_PADDLE_X
    bricks_x = list(BRICKS_X_INIT)
    bricks_y = list(BRICKS_Y_INIT)
    bricks_color = list(BRICKS_COLOR_INIT)


#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
background = pygame.image.load('achtergrond.jpg').convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  # resize image

# Rode steen
brick_red = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_red.blit(spritesheet, (0, 0), (772, 260, 384, 128))
brick_red = pygame.transform.scale(
    brick_red, (BRICK_WIDTH, BRICK_HEIGHT))

# Groene steen
brick_green = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_green.blit(spritesheet, (0, 0), (386, 130, 384, 128))
brick_green = pygame.transform.scale(
    brick_green, (BRICK_WIDTH, BRICK_HEIGHT))

# Blauwe steen
brick_blue = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_blue.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_blue = pygame.transform.scale(
    brick_blue, (BRICK_WIDTH, BRICK_HEIGHT))


# game loop

print('mygame is running')
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # uitlegscherm
    if game_status == "uitleg":
        if keys[pygame.K_SPACE]:
            reset_game()
            game_status = "spelen"

    # SPELEN
    elif game_status == "spelen":

        # move everything
        # move ball
        ball_x = ball_x + ball_speed_x
        ball_y = ball_y + ball_speed_y

        # move paddle
        if keys[pygame.K_d]:  # key d is down
            paddle_x = paddle_x + 10
        if keys[pygame.K_a]:  # key a is down
            paddle_x = paddle_x - 10
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  # Dit stopt de plank dat die rechts uit het scherm loopt
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
        if paddle_x < 0:
            paddle_x = 0  # dit zorgt ervoor dat hij links niet uit het scherm loopt

        # bounce ball
        if ball_x < 0:
            ball_speed_x = abs(ball_speed_x)
        if ball_x + BALL_WIDTH > SCREEN_WIDTH:
            ball_speed_x = abs(ball_speed_x) * -1

        if ball_y < 0:
            ball_speed_y = abs(ball_speed_y)

        # Game over
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
            game_status = "verloren"

        # handle collisions
        if (ball_x + BALL_WIDTH > paddle_x and  # als rechter_kant_bal is groter dan linker_kant_paddle en
                ball_x < paddle_x + PADDLE_WIDTH and  # linker_kant_bal is kleiner dan rechter_kant_paddle en
                ball_y + BALL_HEIGHT > paddle_y and  # onderkant_kant_bal is groter dan boven_kant_paddle en
                ball_y < paddle_y + PADDLE_HEIGHT):  # boven_kant_bal is kleiner dan onder_kant_paddle dan
            # bal_snelheid_y = de positieve waarde van bal_snelheid_y keer -1
            ball_speed_y = abs(ball_speed_y) * -1

        for i in range(0, len(bricks_x)):
            if (ball_x + BALL_WIDTH > bricks_x[i] and  # als rechter_kant_bal is groter dan linker_kant_brick en
                    ball_x < bricks_x[i] + BRICK_WIDTH and  # linker_kant_bal is kleiner dan rechter_kant_paddle en
                    ball_y + BALL_HEIGHT > bricks_y[i] and  # onderkant_kant_bal is groter dan boven_kant_paddle en
                    ball_y < bricks_y[i] + BRICK_HEIGHT):  # boven_kant_bal is kleiner dan onder_kant_paddle dan
                if ball_speed_y > 0 and ball_y < bricks_y[i]:
                    ball_speed_y = abs(ball_speed_y) * -1
                elif ball_speed_y < 0 and ball_y < bricks_y[i] + BRICK_HEIGHT:
                    ball_speed_y = abs(ball_speed_y)
                elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                    ball_speed_x = abs(ball_speed_x)
                elif ball_speed_x > 0 and ball_x < bricks_x[i]:
                    ball_speed_x = abs(ball_speed_x) * -1
                bricks_x.pop(i)
                bricks_y.pop(i)
                bricks_color.pop(i)
                ball_speed_x = max(-MAX_SPEED, min(MAX_SPEED, ball_speed_x))
                ball_speed_y = max(-MAX_SPEED, min(MAX_SPEED, ball_speed_y))
                break

        # Winnen
        if len(bricks_x) == 0:
            ball_speed_y = 0
            ball_speed_x = 0
            game_status = "gewonnen"

    # GEWONNEN
    elif game_status == "gewonnen":
        if keys[pygame.K_SPACE]:
            game_status = "uitleg"

    # GAME OVER
    elif game_status == "verloren":
        if keys[pygame.K_SPACE]:
            game_status = "uitleg"

    #
    # draw everything
    #

    # clear screen
    screen.fill('pink')

    # draw background
    screen.blit(background, (0, 0))

    if game_status == "uitleg":
        titel = font.render("BREAKOUT", True, "white")
        uitleg1 = font.render("A = links", True, "white")
        uitleg2 = font.render("D = rechts", True, "white")
        uitleg3 = font.render("SPACE = start", True, "yellow")

        screen.blit(titel, (450, 150))
        screen.blit(uitleg1, (350, 250))
        screen.blit(uitleg2, (350, 300))
        screen.blit(uitleg3, (250, 400))

    elif game_status == "spelen":
        # draw ball
        screen.blit(ball_img, (ball_x, ball_y))

        # draw paddle
        screen.blit(paddle_img, (paddle_x, paddle_y))

        # draw bricks
        for i in range(len(bricks_x)):
            if bricks_color[i] == "red":
                screen.blit(brick_red, (bricks_x[i], bricks_y[i]))
            elif bricks_color[i] == "green":
                screen.blit(brick_green, (bricks_x[i], bricks_y[i]))
            elif bricks_color[i] == "blue":
                screen.blit(brick_blue, (bricks_x[i], bricks_y[i]))

    # winscherm
    elif game_status == "gewonnen":
        tekst1 = font.render("GEWONNEN!", True, "green")
        tekst2 = font.render("Level uitgespeeld!", True, "white")
        tekst3 = font.render("SPACE = terug naar menu", True, "yellow")

        screen.blit(tekst1, (300, 250))
        screen.blit(tekst2, (200, 350))
        screen.blit(tekst3, (180, 420))

    # GAME OVER
    elif game_status == "verloren":
        tekst1 = font.render("GAME OVER", True, "red")
        tekst2 = font.render("Je hebt verloren!", True, "white")
        tekst3 = font.render("SPACE = terug naar menu", True, "yellow")

        screen.blit(tekst1, (300, 250))
        screen.blit(tekst2, (200, 350))
        screen.blit(tekst3, (180, 420))

    # show screen
    pygame.display.flip()

    #
    # wait until next frame
    #

    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')