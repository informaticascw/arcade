# Shimon + Deef
# BREAKOUT GAME 
#

import pygame, time # importing the pygame and time libraries
from random import randint
#
# definitions 
#

global currentLevel
currentLevel = 1     


FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # Active game screen width
SCREEN_HEIGHT = 720 # Active game screen height
BALL_WIDTH = 16 # Ball width
BALL_HEIGHT = 16 # Ball Height
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 32

BRICK_WIDTH = 96
BRICK_HEIGHT = 32





def setupGame():

    global ball_x
    global ball_speed_x
    global ball_y
    global ball_speed_y
    global ball_speed

    global paddle_x
    global paddle_y
    global paddle_speed
    global paddle_targetspeed
    global paddle_currentspeed

    global paddle2_x
    global paddle2_y
    global paddle2_speed
    global paddle2_targetspeed
    global paddle2_currentspeed

    global bricks_x
    global bricks_y

    global game_status_msg
    global game_state

    ball_x = 0 # Starting position of ball (X-direction)
    ball_speed_x = 6 # Speed of the ball (X-direction)
    ball_y = 300
    ball_speed_y = 6
    ball_speed = 1

    paddle_x = (SCREEN_WIDTH / 2) - (PADDLE_WIDTH/2)
    paddle_y = SCREEN_HEIGHT - (SCREEN_HEIGHT/10)
    paddle_speed = 12
    paddle_targetspeed = 0
    paddle_currentspeed = 0

    paddle2_x = (SCREEN_WIDTH / 2) - (PADDLE_WIDTH/2)
    paddle2_y = (SCREEN_HEIGHT/10) - PADDLE_HEIGHT
    paddle2_speed = 12
    paddle2_targetspeed = 0
    paddle2_currentspeed = 0

    if(currentLevel>15) and currentLevel (+1):
        ball_speed_x + 0,5
        ball_speed_y = 0,5
    
    if(currentLevel==1):
        bricks_x = [1, 2, 3, 9, 10, 11, 1, 2, 3, 9, 10, 11]
        bricks_y = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2] # Two rows of bricks
        ball_speed_x = 3
        ball_speed_y = 3

    elif(currentLevel==2):
        bricks_x = [1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 12, 1, 3, 5, 7, 9, 11, 0]
        bricks_y = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1] # Staggered rows
        ball_speed_x = 3.5
        ball_speed_y = 3.5

    elif(currentLevel==3):
        bricks_x = [6, 6, 6, 6, 6, 5, 7, 4, 8, 3, 9, 2, 10, 1, 11]
        bricks_y = [0, 1, 2, 3, 4, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5] # Pyramid/V-shape
        ball_speed_x = 4
        ball_speed_y = 4

    elif(currentLevel==4):
        bricks_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 12, 1, 11, 2, 10, 0]
        bricks_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 4, 4, 6, 6, 0] # Outer frame with some inner blocks
        ball_speed_x = 4.5
        ball_speed_y = 4.5

    elif(currentLevel==5):
        bricks_x = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
        bricks_y = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2] # Solid rectangle (first 5 columns)
        ball_speed_x = 5
        ball_speed_y = 5

    elif(currentLevel==6):
        bricks_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 0]
        bricks_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4] # Top and bottom rows
        ball_speed_x = 5.5
        ball_speed_y = 5.5

    elif(currentLevel==7):
        bricks_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 12, 2, 11, 3, 10, 4, 9, 5, 8, 6, 7]
        bricks_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6] # Diagonal lines meeting in middle
        ball_speed_x = 6
        ball_speed_y = 6

    elif(currentLevel==8):
        bricks_x = [1, 3, 5, 7, 9, 11, 1, 3, 5, 7, 9, 11, 1, 3, 5, 7, 9, 11, 1, 3, 5, 7, 9, 11]
        bricks_y = [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6] # Checkerboard pattern
        ball_speed_x = 6.5
        ball_speed_y = 6.5

    elif(currentLevel==9):
        bricks_x = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]
        bricks_y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5] # Cross shape
        ball_speed_x = 7
        ball_speed_y = 7

    elif(currentLevel==10):
        bricks_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bricks_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1] # Solid top two rows
        ball_speed_x = 7.5
        ball_speed_y = 7.5

    elif(currentLevel==11):
        bricks_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        bricks_y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 10, 19, 8, 7, 6, 5, 4, 3, 2, 1, 0] # Two diagonal lines
        ball_speed_x = 8
        ball_speed_y = 8

    elif(currentLevel==12):
        bricks_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bricks_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] # Two full rows, separated
        ball_speed_x = 8.5
        ball_speed_y = 8.5

    elif(currentLevel==13):
        bricks_x = [1, 1, 1, 1, 1, 1, 12, 12, 12, 12, 12, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        bricks_y = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Two vertical lines, one horizontal at the top
        ball_speed_y = 9
        ball_speed_x = 9
    elif(currentLevel==14):
        bricks_x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bricks_y = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4] # Two central rows
        ball_speed_x = 9.5
        ball_speed_y = 9.5

    elif(currentLevel==15):
        bricks_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12]
        bricks_y = [0, 1, 2, 3, 2, 1, 2, 3, 4, 5, 4,  1,  0,  6, 5, 4, 4, 5, 6, 5, 4, 4,  5,  6]
        ball_speed_x = 10
        ball_speed_y = 10
    elif(currentLevel>15):
        bricks_x = [randint(0, 12) for p in range(0, 30)]
        bricks_y = [randint(0, 9) for p in range(0, 30)]
    game_status_msg = "" 
    
    
    
    game_status_msg = ""



#
# init game
#
setupGame()

pygame.init() # initating pygame library
font = pygame.font.SysFont('default', 64) #setting the font of the game's text elements
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) # Applying the screen resolution and scaling to full screen
fps_clock = pygame.time.Clock() # Setting up the clock for the FPS
background_img = pygame.image.load("wolk.png").convert() # Loading the background image
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Scaling the background image to the screen's resolution

game_status_img = font.render(game_status_msg, True, 'green')
screen.blit(game_status_img, (SCREEN_WIDTH/2-(game_status_img.get_width()/2), SCREEN_HEIGHT/2-(game_status_img.get_height()/2+200)))
  
#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() # Applying the background transparency of the tiles
basketbal = pygame.image.load('basketbal.png').convert_alpha()
brick = pygame.image.load('brick.png').convert_alpha()

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA) # Initiating object fo the bal
ball_img.blit(basketbal, (0, 0), (0, 0, 64, 64)) # Loading the image for the ball
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) # Resizing the ball to the specified size

paddle_img = pygame.Surface((243,64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0,0), (1158, 396, 243,64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384,128), pygame.SRCALPHA)
brick_img.blit(brick, (0,0), (0, 0, 384,128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

game_state = "menu"

#
# game loop
#

def draw_menu():
    screen.fill((0,0,0))
    title = font.render("Bijzonder slechte game",True,"white")
    prompt = font.render("druk op q voor singleplayer", True,"white")
    prompt2 = font.render("druk op e voor multiplayer", True,"white")

    screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 200))
    screen.blit(prompt, (SCREEN_WIDTH/2 - prompt.get_width()/2, 300))
    screen.blit(prompt2, (SCREEN_WIDTH/2 - prompt.get_width()/2, 350))
    pygame.display.flip()

print('mygame is running') # Report that the game is running
running = True # Let the code know the game is running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    #
    # read events
    # 
    if game_state == "menu" and keys[pygame.K_q]:
        currentLevel = 1
        setupGame()
        game_state = "playing_single"
        mode = "single"
    if game_state == "menu" and keys[pygame.K_e]:
        currentLevel = 1
        setupGame()
        game_state = "playing_multi"
        mode = "multi"
    elif game_state == "Lost" and keys[pygame.K_r]:
        currentLevel = 1
        setupGame()
        game_state = "menu"
    elif game_state == "Won" and keys[pygame.K_r]:
        currentLevel = 1
        setupGame()
        game_state = "menu"
    elif game_state == "level" and keys[pygame.K_e]:
        setupGame()
        game_state = "playing_" + mode

    elif game_state == "menu":
        draw_menu()
        pygame.display.flip()
        fps_clock.tick(FPS)
    elif game_state == "Lost":
        screen.fill((0,0,0))
        game_status_msg = "Het is niet zo moeilijk"
        game_status_img = font.render(game_status_msg, True, 'red')
        screen.blit(game_status_img, (SCREEN_WIDTH/2-(game_status_img.get_width()/2), SCREEN_HEIGHT/2-(game_status_img.get_height()/2+100)))
        game_restart_msg = "Probeer opnieuw met \'R\'"
        game_restart_img = font.render(game_restart_msg, True, 'red')
        screen.blit(game_restart_img, (SCREEN_WIDTH/2-(game_restart_img.get_width()/2), SCREEN_HEIGHT/2-(game_restart_img.get_height()/2))) # (0, 0) is top left corner of screen
        pygame.display.flip()
        fps_clock.tick(FPS)
    elif game_state == "level":
        screen.fill((0,0,0))
        game_status_msg = "klinkt als weekend (level gehaald)"
        game_status_img = font.render(game_status_msg, True, 'white')
        screen.blit(game_status_img, (SCREEN_WIDTH/2-(game_status_img.get_width()/2), SCREEN_HEIGHT/2-(game_status_img.get_height()/2+100)))
        game_restart_msg = "Ga door met \'E\'"
        game_restart_img = font.render(game_restart_msg, True, 'white')
        screen.blit(game_restart_img, (SCREEN_WIDTH/2-(game_restart_img.get_width()/2), SCREEN_HEIGHT/2-(game_restart_img.get_height()/2))) # (0, 0) is top left corner of screen
        pygame.display.flip()
        fps_clock.tick(FPS)
    else:
 
        if keys[pygame.K_r]:
            setupGame()
            game_state = "menu"
        if keys[pygame.K_m]:
            bricks_x.pop(0)
            bricks_y.pop(0)

        # draw background
        screen.blit(background_img, (0, 0))

        # edge of screen bounce
        if ball_x < 0 : 
            ball_speed_x = abs(ball_speed_x) 
        if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
            ball_speed_x = abs(ball_speed_x) * -1 
        if ball_y < 0 : 
            ball_speed_y = abs(ball_speed_y) 
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
            ball_speed_y = abs(ball_speed_y) * -1 

        # 
        # handle collisions
        #

        # Paddle collision
        if (ball_x+BALL_WIDTH > paddle_x and 
            ball_x < paddle_x+PADDLE_WIDTH and 
            ball_y+BALL_HEIGHT > paddle_y and 
            ball_y < paddle_y+PADDLE_HEIGHT):
            
            overlap_left = (paddle_x + PADDLE_WIDTH) - ball_x
            overlap_right = (ball_x + BALL_WIDTH) - paddle_x
            overlap_top = (paddle_y + PADDLE_HEIGHT) - ball_y
            overlap_bottom = (ball_y + BALL_HEIGHT) - paddle_y

            # Check welke overlap de kleinste is (waar hij vandaan komt)
            if min(overlap_left, overlap_right) < min(overlap_top, overlap_bottom):
                # Horizontale botsing
                ball_speed_x *= -1
            else:
                # Verticale botsing
                pc = paddle_x + PADDLE_WIDTH/2
                bc = ball_x + BALL_WIDTH / 2

                # #segments of bounce: (relative to paddle's center)
                # -60>-40
                # -40>-20
                # -20>0
                # 0>20
                # 20>40
                # 40>60

                if(ball_speed_x > 0):
                    if(bc>pc-60 and bc<pc-40):
                        ball_speed_x = 1*2
                        ball_speed_y = -5*2
                    if(bc>pc-40 and bc<pc-20):
                        ball_speed_x = 2*2
                        ball_speed_y = -4*2
                    if(bc>pc-20 and bc<pc):
                        ball_speed_x = 3*2
                        ball_speed_y = -3*2
                    if(bc>pc and bc<pc+20):
                        ball_speed_x = 3*2
                        ball_speed_y = -3*2
                    if(bc>pc+20 and bc<pc+40):
                        ball_speed_x = 4*2
                        ball_speed_y = -2*2
                    if(bc>pc+40 and bc<pc+60):
                        ball_speed_x = 5*2
                        ball_speed_y = -1*2


                if(ball_speed_x < 0):
                    if(bc>pc-60 and bc<pc-40):
                        ball_speed_x = -1*2
                        ball_speed_y = -5*2
                    if(bc>pc-40 and bc<pc-20):
                        ball_speed_x = -2*2
                        ball_speed_y = -4*2
                    if(bc>pc-20 and bc<pc):
                        ball_speed_x = -3*2
                        ball_speed_y = -3*2
                    if(bc>pc and bc<pc+20):
                        ball_speed_x = -3*2
                        ball_speed_y = -3*2
                    if(bc>pc+20 and bc<pc+40):
                        ball_speed_x = -4*2
                        ball_speed_y = -2*2
                    if(bc>pc+40 and bc<pc+60):
                        ball_speed_x = -5*2
                        ball_speed_y = -1*2

        if (ball_x+BALL_WIDTH > paddle2_x and 
            ball_x < paddle2_x+PADDLE_WIDTH and 
            ball_y+BALL_HEIGHT > paddle2_y and 
            ball_y < paddle2_y+PADDLE_HEIGHT and game_state == "playing_multi"):
            
            overlap_left = (paddle2_x + PADDLE_WIDTH) - ball_x
            overlap_right = (ball_x + BALL_WIDTH) - paddle2_x
            overlap_top = (paddle2_y + PADDLE_HEIGHT) - ball_y
            overlap_bottom = (ball_y + BALL_HEIGHT) - paddle2_y

            # Check welke overlap de kleinste is (waar hij vandaan komt)
            if min(overlap_left, overlap_right) < min(overlap_top, overlap_bottom):
                # Horizontale botsing
                ball_speed_x *= -1
            else:
                # Verticale botsing
                pc = paddle2_x + PADDLE_WIDTH/2
                bc = ball_x + BALL_WIDTH / 2

                # #segments of bounce: (relative to paddle's center)
                # -60>-40
                # -40>-20
                # -20>0
                # 0>20
                # 20>40
                # 40>60

                if(ball_speed_x > 0):
                    if(bc>pc-60 and bc<pc-40):
                        ball_speed_x = 1*2
                        ball_speed_y = 5*2
                    if(bc>pc-40 and bc<pc-20):
                        ball_speed_x = 2*2
                        ball_speed_y = 4*2
                    if(bc>pc-20 and bc<pc):
                        ball_speed_x = 3*2
                        ball_speed_y = 3*2
                    if(bc>pc and bc<pc+20):
                        ball_speed_x = 3*2
                        ball_speed_y = 3*2
                    if(bc>pc+20 and bc<pc+40):
                        ball_speed_x = 4*2
                        ball_speed_y = 2*2
                    if(bc>pc+40 and bc<pc+60):
                        ball_speed_x = 5*2
                        ball_speed_y = 1*2


                if(ball_speed_x < 0):
                    if(bc>pc-60 and bc<pc-40):
                        ball_speed_x = -1*2
                        ball_speed_y = 5*2
                    if(bc>pc-40 and bc<pc-20):
                        ball_speed_x = -2*2
                        ball_speed_y = 4*2
                    if(bc>pc-20 and bc<pc):
                        ball_speed_x = -3*2
                        ball_speed_y = 3*2
                    if(bc>pc and bc<pc+20):
                        ball_speed_x = -3*2
                        ball_speed_y = 3*2
                    if(bc>pc+20 and bc<pc+40):
                        ball_speed_x = -4*2
                        ball_speed_y = 2*2
                    if(bc>pc+40 and bc<pc+60):
                        ball_speed_x = -5*2
                        ball_speed_y = 1*2

        #Brick Collision
        for i in range(0, len(bricks_x)):
            if (ball_x + BALL_WIDTH > ((bricks_x[i]*96)+16) and 
            ball_x < ((bricks_x[i]*96)+16) + BRICK_WIDTH and 
            ball_y + BALL_HEIGHT > ((bricks_y[i]*32)+168) and 
            ball_y < ((bricks_y[i]*32)+168) + BRICK_HEIGHT):

            # Bereken overlappen aan elke kant
                overlap_left = (((bricks_x[i]*96)+16) + BRICK_WIDTH) - ball_x
                overlap_right = (ball_x + BALL_WIDTH) - ((bricks_x[i]*96)+16)
                overlap_top = (((bricks_y[i]*32)+168) + BRICK_HEIGHT) - ball_y
                overlap_bottom = (ball_y + BALL_HEIGHT) - ((bricks_y[i]*32)+168)

                # Check welke overlap de kleinste is (waar hij vandaan komt)
                if min(overlap_left, overlap_right) < min(overlap_top, overlap_bottom):
                    # Horizontale botsing
                    ball_speed_x *= -1
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break
                else:
                    # Verticale botsing
                    ball_speed_y *= -1
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break

                

        # move ball
        ball_x = ball_x + ball_speed_x*ball_speed
        ball_y = ball_y + ball_speed_y*ball_speed

        # move paddle

        if keys[pygame.K_d]:
            paddle_targetspeed = paddle_speed
        elif keys[pygame.K_a]:
            paddle_targetspeed = -paddle_speed
        else:
            paddle_targetspeed = 0

        paddle_x += paddle_targetspeed
        paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))

        if keys[pygame.K_l]:
            paddle2_targetspeed = paddle2_speed
        elif keys[pygame.K_j]:
            paddle2_targetspeed = -paddle2_speed
        else:
            paddle2_targetspeed = 0

        paddle2_x += paddle2_targetspeed
        paddle2_x = max(0, min(paddle2_x, SCREEN_WIDTH - PADDLE_WIDTH))

        if keys[pygame.K_m]:
            paddle_x = ball_x - PADDLE_WIDTH/2
            paddle2_x = ball_x - PADDLE_WIDTH/2
                
        # draw objects
        screen.blit(ball_img, (ball_x, ball_y))
        screen.blit(paddle_img, (paddle_x, paddle_y))
        if game_state == "playing_multi":
            screen.blit(paddle_img, (paddle2_x, paddle2_y))

        for i in range(0, len(bricks_x)):
            screen.blit(brick_img, (((bricks_x[i]*96)+16), ((bricks_y[i]*32)+168)))

        game_status_msg = "Level: " +str(currentLevel)
        game_status_img = font.render(game_status_msg, True, 'white')
        screen.blit(game_status_img, (25, SCREEN_HEIGHT-25-game_status_img.get_height()))

        if (ball_y+BALL_HEIGHT > SCREEN_HEIGHT):
            ball_speed_x = 0
            ball_speed_y = 0
            paddle_speed = 0
            paddle2_speed = 0
            game_state = "Lost"
        if (ball_y < 0 and game_state == "playing_multi"):
            ball_speed_x = 0
            ball_speed_y = 0
            paddle_speed = 0
            paddle2_speed = 0
            game_state = "Lost"

        if (len(bricks_x) < 1 and len(bricks_y) < 1):
            currentLevel += 1
            game_state = "level"
        
        # show screen
        pygame.display.flip() 

        # 
        # wait until next frame
        #

        fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
