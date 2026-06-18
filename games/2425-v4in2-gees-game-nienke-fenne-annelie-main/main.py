#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 #screensize in x-direction in pixels
SCREEN_HEIGHT = 720 #screensize in y-direction in pixels
BALL_WIDTH = 16 #ballsize in x-direction in pixels
BALL_HEIGHT = 16 #ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

def variabelenResetten():
  global ball_x, ball_y, ball_speed_y, ball_speed_x
  global paddle_x, paddle_y, paddle1_x, paddle1_y
  global bricks_x, bricks_y, bricks_plaatje
  global game_state, game_status_img

  ball_x = 320
  ball_speed_x = 0 #6 
  ball_y = 600
  ball_speed_y = 0 #10
  paddle_x = SCREEN_WIDTH / 4 - PADDLE_WIDTH / 2
  paddle_y = SCREEN_HEIGHT - 100
  paddle1_x = SCREEN_WIDTH * 3 / 4 - PADDLE_WIDTH / 2
  paddle1_y = SCREEN_HEIGHT - 100

  # bricks opnieuw instellen
  bricks_x = [64,160,160,256,352,448,544,640,640,736,832,928,928,1024,1120,1024,928,832,736,736,640,544,448,352,352,256,160,160]
  bricks_y = [200,232,232,264,296,328,360,360,360,328,296,264,264,232,200,168,136,104,72,72,40,40,72,104,104,136,168,168]
  bricks_plaatje = [0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1]

  game_status_msg = ""


PLAY = 1
GAMEOVER = 2
game_state = PLAY

ball_x = 320 #x-postion of ball in pixels 
ball_speed_x = 0 #6 #speed of ball in X-direction in pixels per frame 
ball_y = 600
ball_speed_y = 0 #10 
# position paddle
paddle_x = SCREEN_WIDTH / 4 - PADDLE_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
paddle1_x= SCREEN_WIDTH * 3 / 4 - PADDLE_WIDTH / 2
paddle1_y = SCREEN_HEIGHT - 100 
#position brick
bricks_x = [64,160,160,256,352,448,544,640,640,736,832,928,928,1024,1120,1024,928,832,736,736,640,544,448,352,352,256,160,160]
bricks_y = [200,232,232,264,296,328,360,360,360,328,296,264,264,232,200,168,136,104,72,72,40,40,72,104,104,136,168,168]
bricks_plaatje = [0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1]
#init game
#define global variables
game_status_msg = "left joystick up to start"

pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# read images
# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transaprency of .png

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

#create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
# copy part (x-left=1403, y-top=652, width=64, heigt=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
#paddle
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
#brick
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
brick1_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick1_img.blit(spritesheet, (0, 0), (386, 520, 384, 128))
brick1_img = pygame.transform.scale(brick1_img, (BRICK_WIDTH, BRICK_HEIGHT))

# game loop

print('mygame is running')
running = True
while running:
  # wait until nest frame
  for event in pygame.event.get(): # read all events
    if event.type == pygame.QUIT:  # GUI is closed
      running = False # end programm
  keys = pygame.key.get_pressed() # read which keys are down

  if keys[pygame.K_w]:
    ball_speed_x = 6
    ball_speed_y = -10

  if game_state == GAMEOVER:
    game_status_img = font.render(game_status_msg, True, 'blue')
    game_status_msg = ""
    screen.blit(game_status_img, (400, 200))
    pygame.display.flip()
    
    if keys[pygame.K_z]:
      game_state = PLAY
      variabelenResetten()

   
  if game_state == PLAY:        
    #move paddle
    if keys[pygame.K_d]: 
      paddle_x = paddle_x + 10
    if keys[pygame.K_a]:
      paddle_x = paddle_x - 10
    if keys[pygame.K_l]: 
      paddle1_x = paddle1_x + 10
    if keys[pygame.K_j]:
      paddle1_x = paddle1_x - 10   
    
    # move everything
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH / 2:
      paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH
    if paddle_x < 0:
      paddle_x = 0 + 1

    if paddle1_x + PADDLE_WIDTH > SCREEN_WIDTH:
      paddle1_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle1_x < SCREEN_WIDTH / 2:
      paddle1_x = SCREEN_WIDTH / 2

    
    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball against edge of the screen
    if ball_x < 0: #left edge
      ball_speed_x = abs(ball_speed_x) #positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: #right edge
      ball_speed_x = abs(ball_speed_x) * -1 #negative x-speed = move left

    if ball_y < 0: 
      ball_speed_y = abs(ball_speed_y) 
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
      ball_speed_y = abs(ball_speed_y) * -1 

    # handle collisions paddle
    if (ball_x < paddle_x + PADDLE_WIDTH and
        ball_x + BALL_WIDTH > paddle_x and
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT):
          ball_middle_x = ball_x + BALL_WIDTH / 2
          paddle_middle_x = paddle_x+ PADDLE_WIDTH / 2
          verschil = ball_middle_x - paddle_middle_x
          ball_speed_x = ball_speed_x + verschil / 20
          ball_speed_y = abs(ball_speed_y) * -1

    if (ball_x < paddle1_x + PADDLE_WIDTH and
      ball_x + BALL_WIDTH > paddle1_x and
      ball_y + BALL_HEIGHT > paddle1_y and
      ball_y < paddle1_y + PADDLE_HEIGHT):
        ball_middle_x = ball_x + BALL_WIDTH / 2
        paddle_middle_x = paddle1_x+ PADDLE_WIDTH / 2
        verschil = ball_middle_x - paddle_middle_x
        ball_speed_x = ball_speed_x + verschil / 20
        ball_speed_y = abs(ball_speed_y) * -1        

          
    # handle collisions brick

    for i in range(0,len(bricks_x)):
      if (ball_x < bricks_x[i] + BRICK_WIDTH and
        ball_x + BALL_WIDTH > bricks_x[i] and
        ball_y + BALL_HEIGHT > bricks_y[i] and
        ball_y < bricks_y[i] + BRICK_HEIGHT):
          if ball_speed_y > 0 and ball_y < bricks_y[i]:
            ball_speed_y = abs(ball_speed_y) *-1
            bricks_x.pop(i)
            bricks_y.pop(i)
            bricks_plaatje.pop(i)
            break
          elif (ball_speed_y < 0 and 
            ball_y + BALL_HEIGHT > BRICK_HEIGHT + bricks_y[i]):
            ball_speed_y = abs(ball_speed_y) 
            bricks_x.pop(i)
            bricks_y.pop(i)
            bricks_plaatje.pop(i)
            break
          elif(ball_speed_x > 0 and ball_x < bricks_x[i]):
            ball_speed_x = abs(ball_speed_x) * -1
            bricks_x.pop(i)
            bricks_y.pop(i)
            bricks_plaatje.pop(i)
            break
          elif (ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH):
            ball_speed_x = abs(ball_speed_x) 
            bricks_x.pop(i)
            bricks_y.pop(i)
            bricks_plaatje.pop(i)
            break

    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
        ball_speed_x = 0 
        ball_speed_y = 0
        game_status_msg = "YOU LOST! (z to restart)"
        game_state = GAMEOVER
        
    if len(bricks_x) == 0 and len(bricks_y) == 0:
      ball_speed_x = 0 
      ball_speed_y = 0
      game_status_msg = "YOU WON! (z to restart)"
      game_state = GAMEOVER
    # draw everything

    # clear screen
    screen.fill('violet') 

    # draw ball
    screen.blit(ball_img, (ball_x,ball_y))
    
    #draw paddle
    screen.blit(paddle_img,(paddle_x,paddle_y))
    screen.blit(paddle_img,(paddle1_x,paddle1_y))
    
    #draw brick
    for i in range(len(bricks_x)-1,-1,-1):
      if bricks_plaatje[i] == 1:
        screen.blit(brick1_img,(bricks_x[i], bricks_y[i]))      
      else:   
        screen.blit(brick_img,(bricks_x[i], bricks_y[i]))
    
    #draw tekst
    game_status_img = font.render(game_status_msg, True, 'blue')
    screen.blit(game_status_img, (400, 200))
  
    # show screen
    pygame.display.flip() 

    # wait until next frame
    fps_clock.tick(FPS) # Sleep the remaining time of this frame
print('mygame stopt running')
