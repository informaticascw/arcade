#
# BREAKOUT GAME
#

import pygame
import time
import random
import math

 # definitions
FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

# bal lijsten
balls_x = [SCREEN_WIDTH // 2] # positie van het x coördinaat van de bal 
balls_y = [SCREEN_HEIGHT // 2] # positie van het y coördinaat van de bal

balls_speed_x = [0] # speed of ball in x-direction in pixels per frame
balls_speed_y = [0]   # speed of ball in y-direction in pixels per frame

game_status_msg = ""
game_status = "uitleg"

# alle botsingen hieronder

BRICK_WIDTH = 96
BRICK_HEIGHT = 32
paddle_speed = 10

#levens
lives = 3

# lijsten van bricks
bricks_x = [352, 448, 544, 640, 736, 832,
            352, 448, 544, 640, 736, 832, 
            352, 448, 544, 640, 736, 832,
            352, 448, 544, 640, 736, 832]
bricks_y = [50, 50, 50, 50, 50, 50, 
            92,92,92,92,92,92, 
            134, 134, 134, 134, 134, 134, 
            176, 176, 176, 176, 176, 176]

brick_fly_timer = [0] * len(bricks_x)
brick_fly_speed = [-8] * len(bricks_x)

# lijsten kleuren van de blokken

COLOR_LIST = ['lightblue', 'blue', 'lightgreen', 'green', 'grey', 'purple', 'red', 'orange', 'yellow', 'brown']

# elke brick krijgt een kleur
brick_colors = [random.choice(COLOR_LIST) for _ in range(len(bricks_x))]
#lijst zodat het 2 keer wordt geraakt
brick_teller = [2] * len(bricks_x)

# init game
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()

# read images

# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

def load_brick(x, y):
    img = pygame.Surface((384, 128), pygame.SRCALPHA)
    img.blit(spritesheet, (0, 0), (x, y, 384, 128))
    return pygame.transform.scale(img, (BRICK_WIDTH, BRICK_HEIGHT))

brick_images = {
    "blue": load_brick(772, 390),
    "blue_cracked": load_brick(0, 0),

    "lightgreen": load_brick(0, 130),
    "lightgreen_cracked": load_brick(0, 260),

    "purple": load_brick(0, 390),
    "purple_cracked": load_brick(0, 520),

    "red": load_brick(772, 260),
    "red_cracked": load_brick(772, 130),

    "orange": load_brick(772, 0),
    "orange_cracked": load_brick(772, 650),

    "lightblue": load_brick(386, 650),
    "lightblue_cracked": load_brick(386, 520),

    "yellow": load_brick(386, 390),
    "yellow_cracked": load_brick(386, 260),

    "green": load_brick(386, 130),
    "green_cracked": load_brick(386, 0),

    "grey": load_brick(772, 520),
    "grey_cracked": load_brick(0, 650),

    "brown": load_brick(386, 780),
    "brown_cracked": load_brick(0, 780),
}

paddle_x = SCREEN_WIDTH // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT

# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

#extra ball img
extra_ball_img = pygame.Surface((128, 128), pygame.SRCALPHA)
extra_ball_img.blit(spritesheet, (0, 0), (1533, 522, 128, 128))
extra_ball_img = pygame.transform.scale(extra_ball_img, (32, 32))

#paddle image
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  # create new image
    # copy part of sheet to image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  # resize image

#brick image
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (0, 128, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

#broken brick image
broken_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
broken_brick_img.blit(spritesheet, (0, 0), (0, 260, 384, 128))
broken_brick_img = pygame.transform.scale(broken_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

#heart image
heart_img = pygame.Surface((64, 64), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (32, 29))

#Powerup image
powerup_img = pygame.Surface((128, 128), pygame.SRCALPHA)
powerup_img.blit(spritesheet, (0, 0), (1403, 392, 128, 128))
powerup_img = pygame.transform.scale(powerup_img, (32, 32))

#powerups lijst
POWERUP_TYPES = ["life", "extra_ball"]
powerups_type = []
powerups_x = []
powerups_y = []
powerups_speed = []

#powerup spawn functie
def spawn_powerup(x, y):
    powerups_x.append(x)
    powerups_y.append(y)
    powerups_speed.append(3)
    powerups_type.append(random.choice(POWERUP_TYPES))

# reset functie
def reset_game():
    global paddle_x, paddle_y, paddle_speed
    global bricks_x, bricks_y, brick_teller, brick_colors
    global brick_fly_timer, brick_fly_speed
    global lives
    global powerups_x, powerups_y, powerups_speed
    global balls_x, balls_y
    global balls_speed_x, balls_speed_y
    
    
    powerups_x = []
    powerups_y = []
    powerups_speed = []

    #levens reseten
    lives = 3

    # bal resetten
    balls_x = [SCREEN_WIDTH // 2]
    balls_y = [SCREEN_HEIGHT // 2]

    balls_speed_x = [0]
    balls_speed_y = [0]

    # paddle resetten
    paddle_x = SCREEN_WIDTH // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT
    paddle_speed = 10

    # bricks opnieuw maken
    bricks_x = [352, 448, 544, 640, 736, 832,
                352, 448, 544, 640, 736, 832,
                352, 448, 544, 640, 736, 832,
                352, 448, 544, 640, 736, 832]

    bricks_y = [50, 50, 50, 50, 50, 50,
                92, 92, 92, 92, 92, 92,
                134, 134, 134, 134, 134, 134,
                176, 176, 176, 176, 176, 176]

    brick_teller = [2] * len(bricks_x)
    brick_colors = [random.choice(COLOR_LIST) for _ in range(len(bricks_x))]

    brick_fly_timer = [0] * len(bricks_x)
    brick_fly_speed = [-8] * len(bricks_x)

reset_game()

running = True
while running:
  # read events
  # move everything
  # wait until next frame

  # read events

    for event in pygame.event.get():  # read all events
        if event.type == pygame.QUIT:  # GUI is closed
            running = False  # end programm
    keys = pygame.key.get_pressed()  # read which keys are down

    if game_status == "uitleg":
        if keys[pygame.K_SPACE]:
                    balls_speed_x[0] = 6
                    balls_speed_y[0] = -6
                    game_status = ""

    if game_status == "gewonnen" or game_status == "verloren":
        if keys[pygame.K_r]:
            reset_game()
            game_status = "uitleg"
    
    if keys[pygame.K_d]:  # key d is down
        paddle_x = paddle_x + paddle_speed

    if keys[pygame.K_a]:  # key a is down
        paddle_x = paddle_x - paddle_speed

    # move everything

    # move ball
    for i in range(len(balls_x)):
            balls_x[i] += balls_speed_x[i]
            balls_y[i] += balls_speed_y[i]
    
    #
    # handle collisions

    # paddle moves to other side
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = 0
    
    if paddle_x < 0:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # kaats bal tegen paddle en het maakt uit vanaf welke hoek
    for i in range(len(balls_x)):

        if (balls_x[i] + BALL_WIDTH >= paddle_x and
            balls_x[i] <= paddle_x + PADDLE_WIDTH and
            balls_y[i] + BALL_HEIGHT >= paddle_y and
            balls_y[i] <= paddle_y + PADDLE_HEIGHT and
            balls_speed_y[i] > 0):

            # afstand van paddle midden
            hit_pos = ((balls_x[i] + BALL_WIDTH/2)
                    - (paddle_x + PADDLE_WIDTH/2)) / (PADDLE_WIDTH/2)

            max_angle = math.radians(60)

            speed = math.sqrt(
                balls_speed_x[i]**2 +
                balls_speed_y[i]**2
            )

            balls_speed_x[i] = speed * math.sin(hit_pos * max_angle)
            balls_speed_y[i] = -speed * math.cos(hit_pos * max_angle)

    # powerups bewegen
    i = 0
    while i < len(powerups_x):
        powerups_y[i] += powerups_speed[i]

        # collision met paddle
        if (powerups_x[i] < paddle_x + PADDLE_WIDTH and
            powerups_x[i] + 32 > paddle_x and
            powerups_y[i] < paddle_y + PADDLE_HEIGHT and
            powerups_y[i] + 32 > paddle_y):

            # EFFECTEN
            if powerups_type[i] == "life":
                lives += 1

            elif powerups_type[i] == "extra_ball":
                balls_x.append(paddle_x + PADDLE_WIDTH // 2)
                balls_y.append(paddle_y - 20)

                balls_speed_x.append(random.choice([-4, 4]))
                balls_speed_y.append(-6)

            # verwijderen
            powerups_x.pop(i)
            powerups_y.pop(i)
            powerups_speed.pop(i)
            powerups_type.pop(i)

            continue

        if powerups_y[i] > SCREEN_HEIGHT:
            powerups_x.pop(i)
            powerups_y.pop(i)
            powerups_speed.pop(i)
            powerups_type.pop(i)
        else:
            i += 1

    # verliezen
    i = 0
    while i < len(balls_x):
        if balls_y[i] > SCREEN_HEIGHT:
            balls_x.pop(i)
            balls_y.pop(i)
            balls_speed_x.pop(i)
            balls_speed_y.pop(i)
        else:
            i += 1
        
    if len(balls_x) == 0:
        lives -= 1

        balls_x = [SCREEN_WIDTH // 2]
        balls_y = [SCREEN_HEIGHT // 2]
        balls_speed_x = [0]
        balls_speed_y = [0]

        game_status = "uitleg"

        # game over pas bij 0 levens
        if lives <= 0:
            game_status = "verloren"

    # bovenkant
    for i in range(len(balls_x)):
        if balls_y[i] < 0:
            balls_speed_y[i] = abs(balls_speed_y[i])

    # zijkanten 
    for i in range(len(balls_x)):
        if balls_x[i] < 0:
            balls_speed_x[i] = abs(balls_speed_x[i])
    for i in range(len(balls_x)):
        if balls_x[i] + BALL_WIDTH > SCREEN_WIDTH:
            balls_speed_x[i] = -abs(balls_speed_x[i])

    #bounce ball against brick
    for b in range(len(balls_x)):

        i = len(bricks_x) - 1
        while i >= 0:

            if (balls_x[b] + BALL_WIDTH > bricks_x[i] and
                balls_x[b] < bricks_x[i] + BRICK_WIDTH and
                balls_y[b] + BALL_HEIGHT > bricks_y[i] and
                balls_y[b] < bricks_y[i] + BRICK_HEIGHT):

                # bounce
                if balls_speed_y[b] > 0 and balls_y[b] < bricks_y[i]:
                    balls_speed_y[b] = -abs(balls_speed_y[b])
                elif balls_speed_y[b] < 0 and balls_y[b] + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                    balls_speed_y[b] = abs(balls_speed_y[b])
                elif balls_speed_x[b] > 0 and balls_x[b] < bricks_x[i]:
                    balls_speed_x[b] = -abs(balls_speed_x[b])
                elif balls_speed_x[b] < 0 and balls_x[b] + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                    balls_speed_x[b] = abs(balls_speed_x[b])

                brick_teller[i] -= 1

                # alleen sneller als de brick echt breekt
                if brick_teller[i] <= 0:
                    brick_fly_timer[i] = 20

                    if random.random() < 0.30:
                        spawn_powerup(bricks_x[i], bricks_y[i])

                    if abs(paddle_speed) < 10:
                        balls_speed_x[b] *= 1.05
                        balls_speed_y[b] *= 1.05
                        paddle_speed = min(paddle_speed * 1.03, 20)

                    break

            i -= 1
        
    # winnen
    if len(bricks_x) == 0:
        for i in range(len(balls_x)):
            balls_speed_x[i] = 0
            balls_speed_y[i] = 0
        game_status = "gewonnen"

    #animatie
    i = 0
    while i < len(bricks_x):

        if brick_fly_timer[i] > 0:
            brick_fly_timer[i] -= 1
            bricks_y[i] += brick_fly_speed[i]

        elif brick_fly_timer[i] == 0 and brick_teller[i] <= 0:
            bricks_x.pop(i)
            bricks_y.pop(i)
            brick_teller.pop(i)
            brick_colors.pop(i)
            brick_fly_timer.pop(i)
            brick_fly_speed.pop(i)
            continue

        i += 1
 
    # Stukje code uit gameloop die alles tekent:
    # draw everything

    # clear screen
    screen.fill('PaleGreen')
    # draw ball
    for i in range(len(balls_x)):
        screen.blit(ball_img, (balls_x[i], balls_y[i]))
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))
    #draw heart
    for i in range(lives):
        screen.blit(heart_img, (20 + i * 40, 20))

    #draw bricks
    for i in range(len(bricks_x)):
        kleur = brick_colors[i]

        if brick_teller[i] == 2:
            screen.blit(brick_images[kleur], (bricks_x[i], bricks_y[i]))
        else:
            screen.blit(brick_images[kleur + "_cracked"], (bricks_x[i], bricks_y[i]))
    
    #draw powerups
    for i in range(len(powerups_x)):

        if powerups_type[i] == "life":
            screen.blit(powerup_img, (powerups_x[i], powerups_y[i]))

        elif powerups_type[i] == "extra_ball":
            screen.blit(extra_ball_img, (powerups_x[i], powerups_y[i]))

    #draw game status message
    game_status_img = font.render(game_status_msg, True, 'black') 
    screen.blit(game_status_img, (640, 340)) # (0, 0) is top left corner of screen

    if game_status == "uitleg":
        screen.fill("PaleGreen")

        screen.blit(font.render("BREAKOUT", True, "black"), (450, 200))
        screen.blit(font.render("A = LINKS", True, "black"), (350, 300))
        screen.blit(font.render("D = RECHTS", True, "black"), (350, 350))
        screen.blit(font.render("SPATIE = START", True, "black"), (350, 400))

    elif game_status == "gewonnen":
        screen.fill("PaleGreen")

        screen.blit(font.render("JE HEBT GEWONNEN!", True, "black"), (250, 300))
        screen.blit(font.render("DRUK R OM OPNIEUW TE SPELEN", True, "black"), (180, 400))

    elif game_status == "verloren":
        screen.fill("PaleGreen")

        screen.blit(font.render("GAME OVER!", True, "black"), (380, 300))
        screen.blit(font.render("DRUK R OM OPNIEUW TE SPELEN", True, "black"), (180, 400))

    # show screen
    pygame.display.flip()

    # wait until next frame
    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
