#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

# screen
FPS = 60 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16

PADDLE_WIDTH = 122
PADDLE_HEIGHT = 32

BRICK_WIDTH = 122
BRICK_HEIGHT = 52

#Bricks
bricks_x = [350, 475, 600, 725, 850, 975,
            350, 475, 600, 725, 850, 975,
            350, 475, 600, 725, 850, 975,
            350, 475, 600, 725, 850, 975]
bricks_y = [150, 150, 150, 150, 150, 150,
            200, 200, 200, 200, 200, 200,
            250, 250, 250, 250, 250, 250,
            300, 300, 300, 300, 300, 300]

brick_speed_y = [0] * len(bricks_x)

game_status_msg = ""

game_started = False

# ball speed
ball_x = 0
ball_speed_x = 3
ball_y = 0
ball_speed_y = 5

# paddle speed
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
paddle_speed = 6
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

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) 

brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (386, 650, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

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

      if event.type == pygame.KEYDOWN:
        game_started = True
    
    keys = pygame.key.get_pressed()
            
    # 
    # move everything
    #

    # move ball
    if game_started:
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x) 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1
    if ball_y < 0:
       ball_speed_y = abs(ball_speed_y)
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
       ball_speed_y = abs(ball_speed_y) * -1


    # 
    # handle collisions
  
    #
    
    ball_right = ball_x + BALL_WIDTH
    ball_left = ball_x
    paddle_left = paddle_x
    paddle_right = paddle_x + PADDLE_WIDTH
    ball_top = ball_y
    ball_bottom = ball_y + BALL_HEIGHT
    paddle_top = paddle_y
    paddle_bottom = paddle_y + PADDLE_HEIGHT

    if ball_right > paddle_left and ball_left < paddle_right and ball_y == paddle_y:
      ball_speed_y *= -1

    # player lost
    if ball_bottom > paddle_bottom:
      ball_speed_x = 0
      ball_speed_y = 0
      paddle_speed = 0
      game_status_msg = "You lost!"

    for i in range(len(bricks_y)):
      if brick_speed_y[i] != 0:
        bricks_y[i] += brick_speed_y[i]
    for i in range(len(bricks_x)-1, -1, -1):
      if bricks_y[i] + BRICK_HEIGHT < 0:
        bricks_x.pop(i)
        bricks_y.pop(i)
        brick_speed_y.pop(i)
    
    
    # check collision block
    for i in range(len(bricks_x)):

     #pase through already hit block
     if brick_speed_y[i] != 0:
        continue

     brick_left = bricks_x[i]
     brick_right = bricks_x[i] + BRICK_WIDTH
     brick_top = bricks_y[i]
     brick_bottom = bricks_y[i] + BRICK_HEIGHT
 
     if (ball_right > brick_left and
        ball_left < brick_right and
        ball_bottom > brick_top and
        ball_top < brick_bottom):
      
      print('brick 2 touched at ball_x =' +str(ball_x) + 
            ' and ball_y = ' + str(ball_y))
      
      
      ball_speed_y *= -1
      #blockbreak
      brick_speed_y[i] = -10
      break
    # level finish
    if len(bricks_x) == 0:
      ball_speed_x = 0
      ball_speed_y = 0
      game_status_msg = "Level uitgespeeld!"
    
  
      # bounce top side
      if ball_speed_y > 0 and ball_top < brick_top:
        ball_speed_y = -abs(ball_speed_y)

      # bounce bottom side
      elif ball_speed_y < 0 and ball_bottom > brick_bottom:
        ball_speed_y = abs(ball_speed_y)

      # bounce left side
      elif ball_speed_x > 0 and ball_left < brick_left:
        ball_speed_x = -abs(ball_speed_x)

      # bounce right side
      elif ball_speed_x < 0 and ball_right > brick_right:
        ball_speed_x = abs(ball_speed_x)


    # 
    # draw everything
    #

    # clear screen
    screen.fill('black') 

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw brick(s)
    for i in range(len(bricks_x)) :
      screen.blit(brick_img, (bricks_x[i], bricks_y[i]))

    # move paddle
    if keys[pygame.K_d] : # move right
      paddle_x += paddle_speed
    elif keys[pygame.K_a] : # move left
      paddle_x -= paddle_speed

    # cheat keys
    if keys[pygame.K_c]:
      paddle_x = ball_x - 61
    if keys[pygame.K_x]:
      FPS = 180
    else:
      FPS = 60

    # stop paddle at edges screen
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
      paddle_x = 0

    # draw game status message
    game_status_img = font.render(game_status_msg, True, 'red')
    screen.blit(game_status_img, (SCREEN_WIDTH/2-100,SCREEN_HEIGHT/2)) # (0, 0) is top left corner of screen

    if not game_started:
      start_img = font.render("PRESS ANY KEY TO START | A/D TO MOVE", True, 'yellow')
      screen.blit(
        start_img,
        ((SCREEN_WIDTH - start_img.get_width()) / 2,
         SCREEN_HEIGHT / 2 - 100)
      )

    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
