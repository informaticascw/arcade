#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # screensize in x-direction in pixels
SCREEN_HEIGHT = 720 # screensize in y-direction in pixels
BALL_WIDTH = 16 # ballsize in x-direction in pixels
BALL_HEIGHT = 16 # ballsize in y-direction in pixels

# paddle size
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

# brick size
BRICK_HEIGHT = 32
BRICK_WIDTH = 96

ball_x = SCREEN_WIDTH / 2 - 72 # x-position of ball in pixels
ball_speed_x = 6 # speed of ball in x-direction in pixels per frame
ball_y = 640
ball_speed_y = -6
paddle_x = SCREEN_WIDTH / 2 - 72
paddle_y = 640
bricks_x = [96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056, 1152, 96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056, 1152]
bricks_y = [96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128]

bricks_lives = [2] * len(bricks_x)

# define global variables
game_status_msg = "" 

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#


spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

achtergrond = pygame.image.load("prachtig.jpeg").convert() 
achtergrond = pygame.transform.scale( achtergrond, (SCREEN_WIDTH, SCREEN_HEIGHT) )

# read ball image
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

# read paddle image
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0,0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# read brick image
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0,0), (772, 0, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

# read damaged brick image
brick_damaged_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_damaged_img.blit(spritesheet, (0,0), (772, 650, 384, 128))
brick_damaged_img = pygame.transform.scale(brick_damaged_img, (BRICK_WIDTH, BRICK_HEIGHT))

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
    if keys[pygame.K_d] : # key d is down
       paddle_x = paddle_x + 10   
    if keys[pygame.K_a] : # key a is down  
      paddle_x = paddle_x - 10
    
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH :
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    if paddle_x < 0:
       paddle_x = 0
    
    # 
    # move everything
    #

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x)
      ball_x = 0 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = -abs(ball_speed_x)
      ball_x = SCREEN_WIDTH - BALL_WIDTH 

    if ball_y < 0 : 
      ball_speed_y = abs(ball_speed_y)
      ball_y = 0 


    # 
    # handle collisions
    #
    if (ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT):
       total_speed = (ball_speed_x**2 + ball_speed_y**2)**0.5
       ball_center_x = ball_x + (BALL_WIDTH / 2)
       paddle_center_x = paddle_x + (PADDLE_WIDTH / 2)
       offset = ball_center_x - paddle_center_x
       direction_x = offset / (PADDLE_WIDTH / 2)
       ball_speed_x = direction_x * (total_speed * 0.7)
       ball_speed_y = -((total_speed**2 - ball_speed_x**2)**0.5)

    if ball_y + BALL_HEIGHT >= SCREEN_HEIGHT:
       ball_speed_x = 0
       ball_speed_y = 0
       game_status_msg = "You lost!"
    
    if len(bricks_x) == 0 :
       ball_speed_x = 0
       ball_speed_y = 0
       game_status_msg = "You Won!"

    for i in range(len(bricks_x) - 1, -1, -1): 
      print('bricks_x[' + str(i) + '] = ' + str(bricks_x[i]))
      if (ball_x + BALL_WIDTH > bricks_x[i] and ball_x < bricks_x[i] + BRICK_WIDTH and ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT):
        print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
        
        

        if ( ball_speed_y > 0 and ball_y < bricks_y[i] ) :
          ball_speed_y = -abs(ball_speed_y)
        elif (ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT):
          ball_speed_y = abs(ball_speed_y)
        elif (ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH):
          ball_speed_x = abs(ball_speed_x) 
        elif (ball_speed_x > 0 and ball_x < bricks_x[i]):
          ball_speed_x = -abs(ball_speed_x)
        
        ball_speed_x *= 1.03
        ball_speed_y *= 1.03

        MAX_SPEED = 16.0
        current_speed = (ball_speed_x**2 + ball_speed_y**2)**0.5
        if current_speed > MAX_SPEED:
          scale_factor = MAX_SPEED / current_speed
          ball_speed_x *= scale_factor
          ball_speed_y *= scale_factor

        bricks_lives[i] -= 1
        
        if bricks_lives[i] <= 0:
          bricks_x.pop(i)
          bricks_y.pop(i)
          bricks_lives.pop(i)
        break
           
    # 
    # draw everything
    #

    # clear screen
    screen.fill('black') 

    # draw custom background
    screen.blit(achtergrond, (0, 0))

    # draw game status message
    game_status_img = font.render(game_status_msg, True, 'green')
    screen.blit(game_status_img, (520, 320)) # (0, 0) is top left corner of screen
    
    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))
   
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw bricks
    for i in range(0, len(bricks_x)): 
      if bricks_lives[i] == 2:
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
      else:
        screen.blit(brick_damaged_img, (bricks_x[i], bricks_y[i]))
   
    # show screen
    pygame.display.flip() 
    
    #
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
