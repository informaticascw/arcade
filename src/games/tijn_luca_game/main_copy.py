#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280   # Screen width in pixels
SCREEN_HEIGHT = 720   # Screen height in pixels
BALL_WIDTH = 16       # Ball width in pixels
BALL_HEIGHT = 16      # Ball height in pixels
PADDLE_HEIGHT = 32
PADDLE_WIDTH = 144
BRICK_WIDTH = 96      # Brick width in pixels
BRICK_HEIGHT = 32     # Brick height in pixels

ball_x = 500
ball_speed_x = 6
ball_speed_y = 5 # speed of ball in y-direction in pixels per frame
ball_y = 300  # y-position of ball in pixels
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT / 2 + 250
paddle_speed = 10

brick_x = 1100
brick_y = 200

x = 0
y = 16
brick_x = []
brick_y = []
for i in range (0, 5):
  for j in range (0, 13):
    brick_x.append((x * BRICK_WIDTH) + 16)
    x = x + 1
    brick_y.append(y)
  x = 0
  y = y + 32

# define global variables
game_status_msg = ""
#
# init game
#

pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#
# reads spritesheet with all of the images
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)                      # Creates an image of 64 x 64 pixels
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))                   # Gets the image of the ball from x = 1403 pixels and y = 652 pixels
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))    # Changes the width and the height from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 390, 1156, 518))
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
    for event in pygame.event.get():   # Reads all events
        if event.type == pygame.QUIT:  # The GUI closes
            running = False            # Stops the program
    keys = pygame.key.get_pressed()    # Checks if keys are pressed
            
    # 
    # move everything
    #

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0 : # left edge
      ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: # right edge
      ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left

    if ball_y < 0: # top edge
       ball_speed_y = abs(ball_speed_y) # positive y-speed = move right down
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: # bottom edge
       ball_speed_y = abs(ball_speed_y) * -1 # negative y-speed = move up

    #move paddle
    if keys[pygame.K_d] and paddle_x + PADDLE_WIDTH < SCREEN_WIDTH:
       paddle_x += paddle_speed
    if keys[pygame.K_a] and paddle_x > 0:
       paddle_x -= paddle_speed
       
    # 
    # handle collisions
    #
    if ball_y + BALL_HEIGHT >= paddle_y and ball_y <= paddle_y + PADDLE_HEIGHT:
       if ball_x > paddle_x and ball_x < paddle_x + PADDLE_WIDTH:
          ball_speed_y = abs(ball_speed_y) * -1
                    
    for i in range (0, len(brick_x)):
       if ball_y + BALL_HEIGHT >= brick_y[i] and ball_y <= brick_y[i] + BRICK_HEIGHT:
          if ball_x + BALL_WIDTH > brick_x[i] and ball_x < brick_x[i] + BRICK_WIDTH:
            print("brick touched at ball_x = " + str(ball_x) + " and ball_y = " + str(ball_y))
            if ball_speed_y > 0 and ball_y < brick_y[i]:
              ball_speed_y = ball_speed_y * -1
              print(i)
              brick_y.pop(i)
              brick_x.pop(i)
              break
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > brick_y[i] + BRICK_HEIGHT:
              ball_speed_y = ball_speed_y * -1
              print(i)
              brick_y.pop(i)
              brick_x.pop(i)
              break
            elif ball_speed_x > 0 and ball_x + BALL_WIDTH > brick_x[i]: 
              ball_speed_x = ball_speed_x * -1
              print(i)
              brick_x.pop(i)
              brick_y.pop(i)
              break
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH > brick_x[i] + BRICK_WIDTH:
              ball_speed_x = ball_speed_x * -1
              print(i)
              brick_x.pop(i)
              brick_y.pop(i)
              break
    
    if len(brick_x) == 0:
      ball_speed_y = 0
      ball_speed_x = 0
      game_status_msg = "You Won!"
      
    
    # 
    # draw everything
    #

    # clear screen
    screen.fill('lightblue') # Sets background color

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y)) # Draws the ball
    
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))
    
    # draw brick
    for i in range (-1, len(brick_x) - 1):
       screen.blit(brick_img, (brick_x[i], brick_y[i]))
    
    
    # draw game status message
    game_status_img = font.render(game_status_msg,True, "red")
    screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) / 2, 100)) # (0, 0) is top left corner of screen

    # show screen
    pygame.display.flip() 

# check if ball is below the paddle
    if ball_y > paddle_y + PADDLE_HEIGHT:
       ball_speed_y = 0
       ball_speed_x = 0
       game_status_msg = "You lost!"

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
