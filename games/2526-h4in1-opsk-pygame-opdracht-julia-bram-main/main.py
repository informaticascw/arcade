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
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
game_over = False

ball_x = 250 # x-position of ball in pixels
ball_speed_x = 6 # speed of ball in x-direction in pixels per frame
ball_y = 150
ball_speed_y = 12
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
bricks_x = [888, 792, 696, 600, 504, 408, 312, 792, 696, 504, 408, 888, 792, 696, 600, 504, 408, 312, 792, 696, 600, 504, 408, 312, 888, 792, 696, 600, 504, 408, 408, 504, 600, 696, 792, 600, 696, 504, 600, 504, 696, 600]
bricks_y = [96, 96, 96, 96, 96, 96, 96, 64, 64, 64, 64, 128, 128, 128, 128, 128, 128, 128, 160, 160, 160, 160, 160, 160, 160, 192, 192, 192, 192, 192, 224, 224, 224, 224, 224, 256, 256, 256, 288, 288, 288 ,320]
brick_hits = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
Background = pygame.image.load('IvanTill.jpg').convert_alpha()  
Background = pygame.transform.scale(
    Background,
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
brick_img.blit(spritesheet, (0, 0), (772, 260, 384, 128))   
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

cracked_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
cracked_brick_img.blit(spritesheet, (0, 0), (0, 650, 384, 128))
cracked_brick_img = pygame.transform.scale(
    cracked_brick_img,
    (BRICK_WIDTH, BRICK_HEIGHT)
)
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
    # move paddle
    if not game_over:
      if keys[pygame.K_d] : # key d is down
         paddle_x += 10
      if keys[pygame.K_a] :
         paddle_x -= 10
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH :
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0 :
       paddle_x = 0
    # bounce ball
    if ball_y < 0 : #
      ball_speed_y = abs(ball_speed_y) 
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
      ball_speed_y = abs(ball_speed_y) * -1 
  
    if ball_x < 0 : # left edge
       ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: # right edge
       ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left
    # 
    # handle collisions
    #

    # ball colliding with block
    for i in range(0, len(bricks_x)) : 
      if ball_x + BALL_WIDTH > bricks_x[i] and ball_x < bricks_x[i] + BRICK_WIDTH and ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT:
         print('brick touched at: ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
         if ball_speed_y > 0 and ball_y + BALL_HEIGHT > bricks_y[i]: 
            ball_speed_y = abs(ball_speed_y) * -1
         elif ball_speed_y < 0 and ball_y < bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y) *1
         elif ball_speed_x > 0 and ball_x + BALL_WIDTH > bricks_x[i]:
            ball_speed_x = abs(ball_speed_x) * -1
         elif ball_speed_x < 0 and ball_x < bricks_x + BRICK_WIDTH:
            ball_speed_x = abs(ball_speed_x) * 1
         brick_hits[i] = brick_hits[i] - 1
         if brick_hits[i] < 0:
            bricks_x.pop(i)
            bricks_y.pop(i)
            brick_hits.pop(i)
         break
    # ball colliding with paddle
    if ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT :
      # ball_speed_y = abs(ball_speed_y) * -1
        ball_speed_y = -abs(ball_speed_y) 
        paddle_center = paddle_x + PADDLE_WIDTH / 2
        ball_center = ball_x + BALL_WIDTH / 2
        difference = ball_center - paddle_center
        ball_speed_x = difference * 0.1
    # ball colliding with bottom of screen
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT :
       ball_speed_y = 0 
       ball_speed_x = 0
       game_status_msg = "You lost!" # death message
       game_over = True
    # ball breaks all blocks
    if len(bricks_x) == 0 and len(bricks_y) == 0 :
       ball_speed_y = 0 
       ball_speed_x = 0
       game_status_msg = "You Win!"
       game_over = True
    # 
    # draw everything
    #

    # draw background
    screen.blit(Background, (0, 0)) 

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))
    
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw brick
    for i in range(0, len(bricks_x)) : 
      if brick_hits[i] == 1:
         screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
      else :
         screen.blit(cracked_brick_img, (bricks_x[i], bricks_y[i]))
    # draw game status message
    game_status_img = font.render(game_status_msg, True, 'green')
    screen.blit(game_status_img, (SCREEN_WIDTH / 2 - game_status_img.get_width() / 2 , SCREEN_HEIGHT / 2 - game_status_img.get_height())) # (0, 0) is top left corner of the screen

    # show screen
    pygame.display.flip() 

    # wait until next frame
    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
