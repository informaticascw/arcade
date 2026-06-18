#
# BREAKOUT GAME
#

import pygame
import time

# definitions
FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

test_modus = False
paddle_p1_x = SCREEN_WIDTH / 4 - PADDLE_WIDTH / 2
paddle_p2_x = SCREEN_WIDTH / 4 + SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
ball_x = 0           # x-position of ball in pixels
ball_speed_x = 6     # speed of ball in x-direction in pixels per frame
ball_y = 0           # y-position of ball in pixels
ball_speed_y = 10    # speed of ball in y-direction in pixels per frame
balls_x = [ball_x]   # x-positie voor meerdere ballen
balls_y = [ball_y]   # y-positie voor meerdere ballen
balls_speed_x = [ball_speed_x] # x-snelheid voor meerdere ballen
balls_speed_y = [ball_speed_y] # x-snelheid voor meerdere ballen
bricks_x = [300, 300, 396, 396, 396, 396, 396, 492, 492, 492, 492, 588, 588, 588, 588, 588, 684, 684]
bricks_y = [96, 128, 96, 128, 160, 192, 224, 128, 160, 192, 224, 96, 128, 160, 192, 224, 96, 128]
brick_status = [2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 2, 3, 3, 2, 2]
falling_bricks = []  # x, y, [grootte]
game_status = 'uitleg'

# init game
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()

#read image
#background

achtergrond = pygame.image.load('achtergrond.png').convert()
achtergrond = pygame.transform.scale(achtergrond, (SCREEN_WIDTH, SCREEN_HEIGHT))

# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

# paddle image create
paddle_p1_img = pygame.Surface((243, 64), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
paddle_p1_img.blit(spritesheet, (0, 0), (1158, 330, 243, 64))
paddle_p1_img = pygame.transform.scale(paddle_p1_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  # resize image

paddle_p2_img = pygame.Surface((243, 64), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
paddle_p2_img.blit(spritesheet, (0, 0), (594, 910, 243, 64))
paddle_p2_img = pygame.transform.scale(paddle_p2_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  # resize image

# brick image create
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 0, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

cracked_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
cracked_brick_img.blit(spritesheet, (0, 0), (772, 650, 384, 128))
cracked_brick_img = pygame.transform.scale(
    cracked_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

special_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
special_brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
special_brick_img = pygame.transform.scale(
    special_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

cracked_special_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
cracked_special_brick_img.blit(spritesheet, (0, 0), (0, 0, 384, 128))
cracked_special_brick_img = pygame.transform.scale(
    cracked_special_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

#
# game loop
#

for brick_x in bricks_x:
    print(str(brick_x))
for i in range(0, len(bricks_x)):
    print('bricks_x[' + str(i) + '] = ' + str(bricks_x[i]))
for brick_y in bricks_y:
    print(str(brick_y))
for i in range(0, len(bricks_y)):
    print('bricks_y[' + str(i) + '] = ' + str(bricks_y[i]))

print('mygame is running')
running = True
while running:
    for event in pygame.event.get():  # read all events
        if event.type == pygame.QUIT:  # GUI is closed
            running = False  # end programm
    keys = pygame.key.get_pressed()  # read which keys are down
    if game_status == 'uitleg':
        game_status_msg = "Zorg dat je met behulp van de paddle en de bal alle \n bricks kapot maakt. De bal stuitert anders van de paddle \naf afhankelijk van de plek waar het stuitert. \n Druk 'S' om te starten"
        if keys[pygame.K_s]:
            ball_x = 0
            ball_y = 0
            ball_speed_x = 6
            ball_speed_y = 10
            paddle_p1_x = SCREEN_WIDTH / 4 - PADDLE_WIDTH / 2
            paddle_p2_x = SCREEN_WIDTH / 4 + SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
            bricks_x = [300, 300, 396, 396, 396, 396, 396, 492, 492, 492, 492, 588, 588, 588, 588, 588, 684, 684]
            bricks_y = [96, 128, 96, 128, 160, 192, 224, 128, 160, 192, 224, 96, 128, 160, 192, 224, 96, 128]
            brick_status = [2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 2, 3, 3, 2, 2]
            game_status = 'spelen'
        # draw game status message
        screen.fill("#FF00EA")
        game_status_img = font.render(game_status_msg, True, 'green')
        # (0, 0) is top left corner of screen
        screen.blit(game_status_img, (0, 0))
        # show screen
        
    if game_status == 'gameover':
        game_status_msg = 'LOSER\nwil je nog een keer proberen druk S\nwil je de uitleg nog een keer zien druk Q'
        if keys[pygame.K_s]:
            #game reset:
            ball_x = 0
            ball_y = 0
            ball_speed_x = 6
            ball_speed_y = 10
            paddle_p1_x = SCREEN_WIDTH / 4 - PADDLE_WIDTH / 2
            paddle_p2_x = SCREEN_WIDTH / 4 + SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
            bricks_x = [300, 300, 396, 396, 396, 396, 396, 492, 492, 492, 492, 588, 588, 588, 588, 588, 684, 684]
            bricks_y = [96, 128, 96, 128, 160, 192, 224, 128, 160, 192, 224, 96, 128, 160, 192, 224, 96, 128]
            brick_status = [2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 2, 3, 3, 2, 2]
            game_status = 'spelen'
        elif keys[pygame.K_q]:
            game_status = 'uitleg'
        #draw game status message
        screen.fill('#FF00EA')
        game_status_img = font.render(game_status_msg, True, 'green')
        # (0, 0) is top left corner of screen
        screen.blit(game_status_img, (0, 0))
        # show screen

    if game_status == 'spelen':
        # define global variables
        game_status_msg = "Speel met [A] en [D]"
        score_msg = 'Score: ' + str((24 - len(brick_status))*100)
        score_msg_item = font.render(score_msg, True, 'green')
        tekst_width = score_msg_item.get_width()
        # move everything

        # move ball
        for i in range(len(balls_x)):
            balls_x[i] += balls_speed_x[i]
            balls_y[i] += balls_speed_y[i]

        # bounce ball against edges of screen
        for i in range(len(balls_x)):

            
            if balls_x[i] < 0:
                balls_speed_x[i] = abs(balls_speed_x[i])

          
            if balls_x[i] + BALL_WIDTH > SCREEN_WIDTH:
                balls_speed_x[i] = -abs(balls_speed_x[i])

            
            if balls_y[i] < 0:
                balls_speed_y[i] = abs(balls_speed_y[i])

            
            if balls_y[i] + BALL_HEIGHT > SCREEN_HEIGHT:
                balls_speed_y[i] = -abs(balls_speed_y[i])

             
        # bounce ball against paddle
        for i in range(len(balls_x)):
            if (balls_x[i] + BALL_WIDTH > paddle_p1_x and
                balls_x[i] < paddle_p1_x + PADDLE_WIDTH and
                balls_y[i] < paddle_y + PADDLE_HEIGHT and
                balls_y[i] + BALL_HEIGHT > paddle_y):

                balls_speed_y[i] = abs(balls_speed_y[i]) * -1

                centre_paddle = paddle_p1_x + (PADDLE_WIDTH / 2)
                angle_bounce = (balls_x[i] - centre_paddle) / 10
                balls_speed_x[i] = angle_bounce

        for i in range(len(balls_x)):
            if (balls_x[i] + BALL_WIDTH > paddle_p2_x and
                balls_x[i] < paddle_p2_x + PADDLE_WIDTH and
                balls_y[i] < paddle_y + PADDLE_HEIGHT and
                balls_y[i] + BALL_HEIGHT > paddle_y):

                balls_speed_y[i] = abs(balls_speed_y[i]) * -1

                centre_paddle = paddle_p2_x + (PADDLE_WIDTH / 2)
                angle_bounce = (balls_x[i] - centre_paddle) / 10
                balls_speed_x[i] = angle_bounce

        # move paddle
        if keys [pygame.K_d]:  # key d is down
            paddle_p1_x = paddle_p1_x + 15
        if keys[pygame.K_a]:  # key a is down
            paddle_p1_x = paddle_p1_x - 15

        if keys [pygame.K_RIGHT]: 
            paddle_p2_x = paddle_p2_x + 15
        if keys [pygame.K_LEFT]:  
            paddle_p2_x = paddle_p2_x - 15
            
        # paddle stops at end of screen
        if (paddle_p1_x + PADDLE_WIDTH) > SCREEN_WIDTH:
            paddle_p1_x = SCREEN_WIDTH - PADDLE_WIDTH
        if paddle_p1_x < 0:
            paddle_p1_x = 0

        if (paddle_p2_x + PADDLE_WIDTH) > SCREEN_WIDTH:
            paddle_p2_x = SCREEN_WIDTH - PADDLE_WIDTH
        if paddle_p2_x < 0:
            paddle_p2_x = 0



        # handle collisions
        for i in range(len(balls_y)):
            if balls_y[i] + BALL_HEIGHT > SCREEN_HEIGHT:
                if len(balls_y) > 1:
                    balls_x.pop(i)
                    balls_y.pop(i)
                    balls_speed_x.pop(i)
                    balls_speed_y.pop(i)
                    break
                else:
                    game_status = "gameover"
        #  bouncing brick
        for b in range(len(balls_x)):
            for i in range(len(bricks_x)):

                if (balls_x[b] + BALL_WIDTH > bricks_x[i] and
                    balls_x[b] < bricks_x[i] + BRICK_WIDTH and
                    balls_y[b] < bricks_y[i] + BRICK_HEIGHT and
                    balls_y[b] + BALL_HEIGHT > bricks_y[i]):

                    print("hit!")

                    # 🔥 BOUNCE ALTIJD!
                    balls_speed_y[b] *= -1

                    # 🔥 zet bal net buiten brick (heel belangrijk)
                    if balls_speed_y[b] > 0:
                        balls_y[b] = bricks_y[i] + BRICK_HEIGHT
                    else:
                        balls_y[b] = bricks_y[i] - BALL_HEIGHT

                    # 🔥 STATUS LOGICA
                    if brick_status[i] == 3:
                        brick_status[i] = 4

                    elif brick_status[i] == 4:
                        balls_x.append(balls_x[b])
                        balls_y.append(balls_y[b])
                        balls_speed_x.append(-balls_speed_x[b])
                        balls_speed_y.append(balls_speed_y[b])

                        bricks_x.pop(i)
                        bricks_y.pop(i)
                        brick_status.pop(i)

                    elif brick_status[i] == 2:
                        brick_status[i] = 1

                    elif brick_status[i] == 1:
                        bricks_x.pop(i)
                        bricks_y.pop(i)
                        brick_status.pop(i)

                    break
        if len(bricks_x) < 1:
            ball_speed_x = 0
            ball_speed_y = 0
            game_status_msg = "Jij bent egt een sigma gamer.\n Gefeliciflaptaart!!"

       


        # draw everything
        screen.blit(achtergrond, (0, 0))
        # draw ball
        for i in range(len(balls_x)):
            screen.blit(ball_img, (balls_x[i], balls_y[i]))
        # draw paddle
        screen.blit(paddle_p1_img, (paddle_p1_x, paddle_y))
        screen.blit(paddle_p2_img, (paddle_p2_x, paddle_y))
        # draw brick
        for i in range(0, len(bricks_x)):
            if brick_status[i] == 2:
                screen.blit(brick_img, (bricks_x[i], bricks_y[i]))

            elif brick_status[i] == 1:
                screen.blit(cracked_brick_img, (bricks_x[i], bricks_y[i]))

            elif brick_status[i] == 3:
                screen.blit(special_brick_img, (bricks_x[i], bricks_y[i]))
            elif brick_status[i] == 4:
                screen.blit(cracked_special_brick_img, (bricks_x[i], bricks_y[i]))
            elif brick_status[i] == 0:
                screen.blit(cracked_brick_img, (bricks_x[i], bricks_y[i]))
        # draw falling bricks
        for brick in falling_bricks:
            brick[2] = brick[2] -1 # hier word hij kleiner
            if brick[2] > 1:
                nieuwe_breedte_brick = int(brick[2])
                nieuwe_hoogte_brick = int(brick[2] * BRICK_HEIGHT / BRICK_WIDTH)
                klein_img = pygame.transform.scale(cracked_brick_img, (nieuwe_breedte_brick, nieuwe_hoogte_brick))
                # krimpen in het midden
                midden_x = brick[0] + BRICK_WIDTH / 2
                midden_y = brick[1] + BRICK_HEIGHT / 2
                teken_x = midden_x - nieuwe_breedte_brick / 2
                teken_y = midden_y - nieuwe_hoogte_brick / 2
                
                screen.blit(klein_img, (teken_x, teken_y))

        falling_bricks = [b for b in falling_bricks if b[2] > 0]
        # draw game status message
        game_status_img = font.render(game_status_msg, True, 'green')
        # (0, 0) is top left corner of screen
        screen.blit(game_status_img, (0, 0))
        #score message
        screen.blit(score_msg_item, (SCREEN_WIDTH - tekst_width, 0))
        # show screen
    pygame.display.flip()

    # wait until next frame
    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
