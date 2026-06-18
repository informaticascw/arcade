#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH =  1280 # screensize in x-direction in pixels
SCREEN_HEIGHT = 720 # screensize in y-direction in pixels
BALL_WIDTH = 16 # ballsize in x-direction in pixels
BALL_HEIGHT = 16 # ballsize in y-direction in pixels
ball_x = 0 # x-position of ball in pixels
ball_y = 6 # y-position of ball in pixels
ball_speed_x = 6 # speed of ball in x-direction in pixels per frame
ball_speed_y = -10 # speed of ball in y-direction
extra_ball_active = False

ball2_x = 0
ball2_y = 6
ball2_speed_x = 0
ball2_speed_y = 0

ball3_x = 0
ball3_y = 6
ball3_speed_x = 0
ball3_speed_y = 0 
PADDLE_WIDTH = 144   # paddlesize in x-direction in pixels
PADDLE_HEIGHT = 32   # paddlesize in y-direction in pixels
paddle_x = 640       # x-position of paddle in pixels
paddle_speed_x = 10  # speed of paddle in x-direction in pixels per frame
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = SCREEN_HEIGHT - 60 
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
START_BRICKS_X = [ 
    184, 320, 456, 592, 728, 864, 1000, 1136,
    184, 320, 456, 592, 728, 864, 1000, 1136,
    184, 320, 456, 592, 728, 864, 1000, 1136,
    184, 320, 456, 592, 728, 864, 1000, 1136,
    184, 320, 456, 592, 728, 864, 1000, 1136]

START_BRICKS_Y = [ 
    100, 100, 100, 100, 100, 100, 100, 100,
    142, 142, 142, 142, 142, 142, 142, 142,
    184, 184, 184, 184, 184, 184, 184, 184,
    226, 226, 226, 226, 226, 226, 226, 226,
    268, 268, 268, 268, 268, 268, 268, 268]

bricks_x = START_BRICKS_X.copy()
bricks_y = START_BRICKS_Y.copy()
bricks_life = [1] * len(bricks_x)

special_bricks = [False] * len(bricks_x)
multi_ball_added = False

game_status_msg= ""
game_status = "start"
level = 1

#
# init game
#

pygame.init() # start pygame
font = pygame.font.Font('PressStart2P-Regular.ttf', 24) # font for text
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) # create game window
fps_clock = pygame.time.Clock() # clock to control game speed

#
# read images
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# read spritesheet containing all images
#  convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))  
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT 
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

# create brick image
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (0, 128, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

damaged_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
damaged_brick_img.blit(spritesheet, (0, 0), (0, 0, 384, 128))
damaged_brick_img = pygame.transform.scale(damaged_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

#
# game loop
#

print('mygame is running')
game_over = False
running = True
ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_status == "game_completed":

            if event.key == pygame.K_z:
                level = 1

                ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2
                ball_speed_x = 6
                ball_speed_y = -10

                bricks_x = START_BRICKS_X.copy()
                bricks_y = START_BRICKS_Y.copy()
                bricks_life = [1] * len(bricks_x)
                game_status = "playing"
        if event.type == pygame.KEYDOWN:
            if game_status == "next_level":
                if event.key == pygame.K_z:
                    level = 1

                ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2
                ball_speed_x = 6
                ball_speed_y = -10

                bricks_x = START_BRICKS_X.copy()
                bricks_y = START_BRICKS_Y.copy()

                game_status = "playing"

                if event.key == pygame.K_e:
                   level = 2

                ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2
                ball_speed_x = 7
                ball_speed_y = -11
                paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

                bricks_x = START_BRICKS_X.copy()
                bricks_y = START_BRICKS_Y.copy()
                bricks_life = [2] * len(bricks_x)

                game_status = "playing"

                if event.key == pygame.K_r:
                    level = 3

                ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
                ball_y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2

                ball_speed_x = 8
                ball_speed_y = -12

                paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2

                bricks_x = START_BRICKS_X.copy()
                bricks_y = START_BRICKS_Y.copy()
                bricks_life = [4] * len(bricks_x)
                special_bricks = [False] * len(bricks_x)
                special_bricks[10] = True
                multi_ball_added = False

                game_status = "playing" 
            
            if event.key == pygame.K_q:
                game_status = "playing"
    if game_status == "start":
        screen.fill("black")

        titel = font.render("BREAKOUT", True, "white")
        start = font.render("Press Q to start", True, "green")

        screen.blit(titel, (450, 250))
        screen.blit(start, (350, 350))

        pygame.display.flip()
        fps_clock.tick(FPS)

        continue
    if game_status == "next_level":
        screen.fill("black")

        text1 = font.render("LEVEL COMPLETE!", True, "white")

        if level == 1:
            text2 = font.render("Press E for level 2", True, "green")

        elif level == 2:
            text2 = font.render("Press R for level 3", True, "green")

        text3 = font.render("Press Z to replay", True, "red")   

        screen.blit(text1, (300, 200))
        screen.blit(text2, (250, 300))
        screen.blit(text3, (250, 400))
        pygame.display.flip()
        fps_clock.tick(FPS)
        continue

    if game_status == "game_completed":
        screen.fill("black")
        text1 = font.render("YOU BEAT THE GAME!", True, "green")
        text2 = font.render("Press Z to play again", True, "white")
        screen.blit(text1, (250, 250))
        screen.blit(text2, (200, 350))
        pygame.display.flip()
        fps_clock.tick(FPS)

        continue
     
        
    
    #
    # read events
    #  # move everything
  
  

  # wait until next frame
    for event in pygame.event.get(): # read all events
        if event.type == pygame.QUIT: # GUI is closed  
            running = False # end programm
    keys = pygame.key.get_pressed() # read which keys are down

      # 
    # move everything
    #
    if keys[pygame.K_q]:
        ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2
        ball_speed_x = 6
        ball_speed_y = -10
        paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        bricks_x = START_BRICKS_X.copy()
        bricks_y = START_BRICKS_Y.copy()
        
        if level == 1:
            bricks_life = [1] * len(bricks_x)

        if level == 2:
            bricks_life = [2] * len(bricks_x)
       
        if level == 3:
            bricks_life = [4] * len(bricks_x)
            special_bricks = [False] * len(bricks_x)
            special_bricks[10] = True
            multi_ball_added = False    

    # verwijder game over tekst
    game_status_msg = ""

         
    # 
    # move everything
    #
    if keys[pygame.K_d]:
         paddle_x = paddle_x + abs(paddle_speed_x)
    if keys[pygame.K_a]:
         paddle_x = paddle_x + abs(paddle_speed_x) * -1
    # stop paddle at left edge
    if paddle_x < 0:
        paddle_x = 0

    # stop paddle at right edge
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # move ball
   
    old_ball_x = ball_x
    old_ball_y = ball_y

    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    if extra_ball_active:
        ball2_x = ball2_x + ball2_speed_x
        ball2_y = ball2_y + ball2_speed_y

        ball3_x = ball3_x + ball3_speed_x
        ball3_y = ball3_y + ball3_speed_y

    # bounce ball against edges of screen
    if ball_x < 0:                             # left edge
        ball_speed_x = abs(ball_speed_x)       # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:     # right edge
        ball_speed_x = abs(ball_speed_x) * -1  # negative x-speed = move left
    if ball_y < 0:                             # top edge
        ball_speed_y = abs(ball_speed_y)       # positive y-speed = move down
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:   # bottom edge
        ball_speed_y = abs(ball_speed_y) * -1
    
    if extra_ball_active:
        
        if ball2_x < 0:
            ball2_speed_x = abs(ball2_speed_x)

        if ball2_x + BALL_WIDTH > SCREEN_WIDTH:
            ball2_speed_x = abs(ball2_speed_x) * -1

        if ball2_y < 0:
            ball2_speed_y = abs(ball2_speed_y)

        if ball2_y + BALL_HEIGHT > SCREEN_HEIGHT:
            ball2_speed_y = abs(ball2_speed_y) * -1

        if ball3_x < 0:
            ball3_speed_x = abs(ball3_speed_x)

        if ball3_x + BALL_WIDTH > SCREEN_WIDTH:
            ball3_speed_x = abs(ball3_speed_x) * -1

        if ball3_y < 0:
            ball3_speed_y = abs(ball3_speed_y)

        if ball3_y + BALL_HEIGHT > SCREEN_HEIGHT:
            ball3_speed_y = abs(ball3_speed_y) * -1
  
    # 
    # handle collisions

    # check collision with brick
    for i in range(0, len(bricks_x)):
        
        if ball_x + BALL_WIDTH > bricks_x[i] and ball_x < bricks_x[i] + BRICK_WIDTH:
            if ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT:

                # hit from above
                if old_ball_y + BALL_HEIGHT <= bricks_y[i]:
                    ball_speed_y = abs(ball_speed_y) * -1.02

                # hit from below
                elif old_ball_y >= bricks_y[i] + BRICK_HEIGHT:
                    ball_speed_y = abs(ball_speed_y) * 1.02

                # hit from left
                elif old_ball_x + BALL_WIDTH <= bricks_x[i]:
                    ball_speed_x = abs(ball_speed_x) * -1.02

                # hit from right
                elif old_ball_x >= bricks_x[i] + BRICK_WIDTH:
                    ball_speed_x = abs(ball_speed_x) * 1.02

                # backup, zodat hij nooit zonder bounce door een rij gaat
                else:
                    ball_speed_y = ball_speed_y * -1.02

                bricks_life[i] = bricks_life[i] - 1

                if level == 3 and special_bricks[i] and not multi_ball_added:
                    multi_ball_added = True
                    extra_ball_active = True

                    ball2_x = ball_x
                    ball2_y = ball_y
                    ball2_speed_x = -ball_speed_x
                    ball2_speed_y = ball_speed_y

                    ball3_x = ball_x
                    ball3_y = ball_y
                    ball3_speed_x = ball_speed_x
                    ball3_speed_y = -ball_speed_y

                if bricks_life[i] <= 0:
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    bricks_life.pop(i)

                break
    #   
    # win game
    if len(bricks_x) == 0:
        if level == 1:
            game_status = "next_level"

        elif level == 2:
            game_status = "next_level"

        elif level == 3:
            game_status = "game_completed"

    # game over
    # making the game end when ball moves past the paddle
    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "Loser!  Press Q to try again"
        
    
    # check if ball touches brick
    

    # making the ball collide with the paddle
    if ball_x + BALL_WIDTH >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT >= paddle_y:
        ball_speed_y = abs(ball_speed_y) * -1


    
    # 
    # draw everything
    #

    # clear screen
    if level == 1:
        screen.fill((0, 0, 139))

    elif level == 2:
        screen.fill((40, 0, 0))

    elif level == 3:
        screen.fill((35, 0, 60))
        
    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    if extra_ball_active:
        screen.blit(ball_img, (ball2_x, ball2_y))
        screen.blit(ball_img, (ball3_x, ball3_y))
   
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))
    
    #draw bricks
    spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
    for i in range(0, len(bricks_x)):
        if level == 2 and bricks_life[i] == 1:
            screen.blit(damaged_brick_img, (bricks_x[i], bricks_y[i]))
        else:
            screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
  
    game_status_img = font.render(game_status_msg, True, 'red')
    screen.blit(game_status_img, (0, 0))
    # show screen
    level_img = font.render(f"LEVEL {level}", True, "orange")
    screen.blit(level_img, (1000, 20))
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
