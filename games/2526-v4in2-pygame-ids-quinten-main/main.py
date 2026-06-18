#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#
ball_y = 100
ball_speed_y = 10
FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
ball_x = 0           # x-position of ball in pixels
ball_speed_x = 6     # speed of ball in x-direction in pixels per frame
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
paddle_y = SCREEN_HEIGHT - 100
paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
brick_y = SCREEN_HEIGHT - (SCREEN_HEIGHT * (3/4))
brick_x = SCREEN_WIDTH / 2 - BRICK_WIDTH / 2
speed_bricks_x = [100, 1100, 100, 1100]
speed_bricks_y = [500, 500, 100, 100]
# define global variables
bricks_x = [brick_x, brick_x + BRICK_WIDTH, brick_x + BRICK_WIDTH * 2, brick_x - BRICK_WIDTH, brick_x - BRICK_WIDTH * 2, 
            brick_x, brick_x + BRICK_WIDTH, brick_x + BRICK_WIDTH * 2, brick_x - BRICK_WIDTH, brick_x - BRICK_WIDTH * 2, brick_x + BRICK_WIDTH * 3, brick_x - BRICK_WIDTH * 3, 
            brick_x, brick_x + BRICK_WIDTH, brick_x + BRICK_WIDTH * 2, brick_x - BRICK_WIDTH, brick_x - BRICK_WIDTH * 2, brick_x + BRICK_WIDTH * 3, brick_x - BRICK_WIDTH * 3,
            brick_x, brick_x + BRICK_WIDTH, brick_x + BRICK_WIDTH * 2, brick_x - BRICK_WIDTH, brick_x - BRICK_WIDTH * 2]
bricks_y = [brick_y, brick_y, brick_y, brick_y, brick_y, 
            brick_y + BRICK_HEIGHT, brick_y + BRICK_HEIGHT, brick_y + BRICK_HEIGHT, brick_y + BRICK_HEIGHT, brick_y + BRICK_HEIGHT, 
            brick_y + BRICK_HEIGHT, brick_y + BRICK_HEIGHT, 
            brick_y + BRICK_HEIGHT * 2, brick_y + BRICK_HEIGHT * 2, brick_y + BRICK_HEIGHT * 2, brick_y + BRICK_HEIGHT * 2, brick_y + BRICK_HEIGHT * 2, 
            brick_y + BRICK_HEIGHT * 2, brick_y + BRICK_HEIGHT * 2, 
            brick_y + BRICK_HEIGHT * 3, brick_y + BRICK_HEIGHT * 3, brick_y + BRICK_HEIGHT * 3, brick_y + BRICK_HEIGHT * 3, brick_y + BRICK_HEIGHT * 3, 
            brick_y + BRICK_HEIGHT * 3, brick_y + BRICK_HEIGHT * 3, 
            brick_y + BRICK_HEIGHT * 4,brick_y + BRICK_HEIGHT * 4,brick_y + BRICK_HEIGHT * 4,brick_y + BRICK_HEIGHT * 4,brick_y + BRICK_HEIGHT * 4
            ]

bricks_level = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# define global variables
game_status_msg = "speel met [A] en [D]"
#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transpa
# .onvert_alpha() 
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA) 
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64)) 
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) 

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))  # copy part of sheet to image
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # resize image

broken_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
broken_brick_img.blit(spritesheet, (0, 0), (0, 0, 384, 128))  # copy part of sheet to image
broken_brick_img = pygame.transform.scale(broken_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # resize image

speed_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
speed_brick_img.blit(spritesheet, (0, 0), (772, 260, 384, 128))  # copy part of sheet to image
speed_brick_img = pygame.transform.scale(speed_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # resize image

#
# game loop
#

print('mygame is running')
running = True
while running:
    # read events
    # move everything
    # handle collisions
    # draw everything
    # wait until next frame

    for event in pygame.event.get(): # read all events
      if event.type == pygame.QUIT: # GUI is closed 
            running = False # end programm
    
    keys = pygame.key.get_pressed() # read which keys are down
              
    # 
    # move everything
    #

    ball_y = ball_y + ball_speed_y
    # move everything

    # move ball
    ball_x = ball_x + ball_speed_x
    # bounce ball against edges of screen
    if ball_x < 0 : # left edge
      ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: # right edge
      ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left

    if ball_y < 0 : # top of screen
      ball_speed_y = abs(ball_speed_y) # positive y-speed = move to bottom
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: # bottom of screen
      ball_speed_y = abs(ball_speed_y) * -1 # negative y-speed = move to top  
    
    #move paddle
    if keys[pygame.K_d]:  
       paddle_x = paddle_x + 10
    if keys[pygame.K_a] :
       paddle_x = paddle_x - 10

    #stop paddle at end of screen
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0: 
       paddle_x = 0

    if ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT:
       ball_speed_y = abs(ball_speed_y) * -1
    
    for i in range(0, len(bricks_x)):
      if ball_x + BALL_WIDTH > bricks_x[i] and ball_x < bricks_x[i] + BRICK_WIDTH and ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT:
         print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
         bricks_level[i] = bricks_level[i] + 1
         if ball_speed_y > 0 and ball_y < bricks_y[i]:
          ball_speed_y = abs(ball_speed_y) * -1
       
         elif ball_speed_y < 0 and (ball_y + BALL_HEIGHT) > (bricks_y[i] + BRICK_HEIGHT):
          ball_speed_y = abs(ball_speed_y)   

         elif ball_speed_x > 0 and ball_x < bricks_x[i]:
          ball_speed_x = abs(ball_speed_x) * -1
       
         elif ball_speed_x < 0 and (ball_x + BALL_WIDTH) > (bricks_x[i] + BRICK_WIDTH):
          ball_speed_x = abs(ball_speed_x)
         
         if bricks_level[i] == 2:
          bricks_x.pop(i)
          bricks_y.pop(i)
          bricks_level.pop(i)
          break  
    
    for i in range(0, len(speed_bricks_x)):
      if ball_x + BALL_WIDTH > speed_bricks_x[i] and ball_x < speed_bricks_x[i] + BRICK_WIDTH and ball_y + BALL_HEIGHT > speed_bricks_y[i] and ball_y < speed_bricks_y[i] + BRICK_HEIGHT:
         print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
         ball_speed_x = ball_speed_x + 1
         ball_speed_y = ball_speed_y + 1
         if ball_speed_y > 0 and ball_y < speed_bricks_y[i]:
          ball_speed_y = abs(ball_speed_y) * -1
       
         elif ball_speed_y < 0 and (ball_y + BALL_HEIGHT) > (speed_bricks_y[i] + BRICK_HEIGHT):
          ball_speed_y = abs(ball_speed_y)   

         elif ball_speed_x > 0 and ball_x < speed_bricks_x[i]:
          ball_speed_x = abs(ball_speed_x) * -1
       
         elif ball_speed_x < 0 and (ball_x + BALL_WIDTH) > (speed_bricks_x[i] + BRICK_WIDTH):
          ball_speed_x = abs(ball_speed_x)
         
         speed_bricks_x.pop(i)
         speed_bricks_y.pop(i)
         break


    
    if len(bricks_x) == 0 :
      ball_speed_x = 0
      ball_speed_y = 0 
      game_status_msg = "You won!"
    
    # 
    # handle collisions
    #
    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
      ball_speed_x = 0
      ball_speed_y = 0  
      # if dead
      game_status_msg = "You lost!"
      
      

      # draw everything
    # draw game status message
    game_status_img = font.render(game_status_msg, True, 'green')
    game_status_msgx = SCREEN_WIDTH / 2 - game_status_img.get_width() / 2
    # clear screen
    screen.fill('black') 
  
    # draw ball
    screen.blit(game_status_img, (game_status_msgx, 0)) # (0, 0) is top left corner of screen
    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(paddle_img, (paddle_x, paddle_y))
    for i in range(0, len(bricks_x)): 
       print('bricks_x[' + str(i) + '] = ' + str(bricks_x[i]))
       if bricks_level[i] == 0:
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
       
       elif bricks_level[i] == 1:
         screen.blit(broken_brick_img, (bricks_x[i], bricks_y[i]))
    
    for i in range(0, len(speed_bricks_x)):
      print('speed_bricks_x[' + str(i) + '] = ' + str(speed_bricks_x[i]))
      screen.blit(speed_brick_img, (speed_bricks_x[i], speed_bricks_y[i]))

    # show screen
    pygame.display.flip()  

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
