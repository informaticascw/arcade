#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # screensize in x-direction in pixels
SCREEN_HEIGHT = 720 # screensize in y-direction in pixels
BALL_WIDTH = 16 # ballsize in x-direction in pixels
BALL_HEIGHT = 16 # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
SCORE_WIDTH = 121.5
SCORE_HEIGHT = 32

ball_x = 0 # ball position in x-direction
ball_speed_x = 6 # speed of ball in x-direction in pixels per frame

ball_y = 100
ball_speed_y = 6

paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100

popup_x = 0
popup_y = 0
popup_time = 0
popup_type = " "

score = 0
highscore = 0

level = 1

# define global variables
game_status_msg = "press b to start"
game_status = "start"

bricks_x = [96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056] * 3

bricks_y = [32] * 11 + [64] * 11 + [96] * 11

teller_bricks_x = [2] * 33

brick_animating = [False] * len(bricks_x)

level1_x = [96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056] * 3
level1_y = [32] * 11 + [64] * 11 + [96] * 11
level1_teller = [2] * len(level1_x)

level2_x = level1_x.copy()
level2_y = level1_y.copy()
level2_teller = [2] * 11 + [3] * 11 + [2] * 11

level3_x = [96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056] * 4
level3_y = [32] * 11 + [64] * 11 + [96] * 11 + [128] * 11
level3_teller = [3] * len(level3_x)

# for checking

#level1_x = [96]
#level1_y = [32]
#level1_teller = [2] * len(level1_x)
#
#level2_x = level1_x.copy()
#level2_y = level1_y.copy()
#level2_teller = [3] * len(level2_x)
#
#level3_x = [96]
#level3_y = [32]
#level3_teller = [3] * len(level3_x)

original_bricks_x = bricks_x.copy()
original_bricks_y = bricks_y.copy()
original_teller_bricks_x = teller_bricks_x.copy()

#
# init game
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()


# read images
# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

# create empty image of 64 x 64 pixels SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (0, 130, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img2 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img2.blit(spritesheet, (0, 0), (0, 260, 384, 128))
brick_img2 = pygame.transform.scale(brick_img2, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img3 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img3.blit(spritesheet, (0, 0), (386, 130, 384, 128))
brick_img3 = pygame.transform.scale(brick_img3, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img4 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img4.blit(spritesheet, (0, 0), (386, 0, 384, 128))
brick_img4 = pygame.transform.scale(brick_img4, (BRICK_WIDTH, BRICK_HEIGHT))

score50_img = pygame.Surface((243, 64), pygame.SRCALPHA)
score50_img.blit(spritesheet, (0, 0), (1403, 66, 243, 64))
score50_img = pygame.transform.scale(score50_img, (SCORE_WIDTH, SCORE_HEIGHT))

score100_img = pygame.Surface((243, 65), pygame.SRCALPHA)
score100_img.blit(spritesheet, (0, 0), (1084, 912, 243, 65))
score100_img = pygame.transform.scale(score100_img, (SCORE_WIDTH, SCORE_HEIGHT))

if level == 1:
  bricks_x = level1_x.copy()
  bricks_y = level1_y.copy()
  teller_bricks_x = level1_teller.copy()
if level == 2:
  bricks_x = level2_x.copy()
  bricks_y = level2_y.copy()
  teller_bricks_x = level2_teller.copy()
if level == 3:
  bricks_x = level3_x.copy()
  bricks_y = level3_y.copy()
  teller_bricks_x = level3_teller.copy()

#
# game loop
print('mygame is running')
running = True
while running:
  # read events
  # move everything
  # handle collisions
  # draw everything
  # wait until next frame


  for event in pygame.event.get(): 
    if event.type == pygame.QUIT:  
      running = False 
    if event.type == pygame.KEYDOWN: # any key is down
      if game_status == "start" and event.key == pygame.K_b: # key b is down
        game_status = "playing"
        game_status_msg = " "
        print("game started")
      elif game_status == "lost" and event.key == pygame.K_r:
        game_status = "playing"
        ball_x = 0
        ball_y = 100

        ball_speed_y = 6
        ball_speed_x = 6

        score = 0
        game_status_msg = "press b to start"
        game_status = "start"

        bricks_x = original_bricks_x.copy()
        bricks_y = original_bricks_y.copy()
        teller_bricks_x = original_teller_bricks_x.copy()
  keys = pygame.key.get_pressed() 

  if game_status == "playing":
    if keys[pygame.K_d] : # key d is down
      paddle_x += 10
      screen.blit(paddle_img, (paddle_x, paddle_y))

    if keys[pygame.K_a] : # key a is down
      paddle_x -= 10
      screen.blit(paddle_img, (paddle_x, paddle_y))
    
    # 
    # move everything
  
  if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
    paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

  if paddle_x < 0:
    paddle_x = 0

#ball bounces against paddle
  if (ball_x + BALL_WIDTH > paddle_x and 
      ball_x < paddle_x + PADDLE_WIDTH and
      ball_y < paddle_y + PADDLE_HEIGHT and
      ball_y + BALL_HEIGHT > paddle_y) :
    ball_speed_y = abs(ball_speed_y) * -1

    ball_center = ball_x + BALL_WIDTH / 2
    paddle_center = paddle_x + PADDLE_WIDTH / 2

    # value +1 (right) to -1 (left)
    hit_pos = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)

    # horizontal speed
    ball_speed_x += hit_pos * 1.5

  if game_status == "playing": # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y
  # bounce ball against the edges of screen
    
  # bounce ball
  if ball_x < 0 : #left edge
    ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
  if ball_x + BALL_WIDTH > SCREEN_WIDTH: #right edge
    ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left
  if ball_y < 0 : #top edge
     ball_speed_y = abs(ball_speed_y)
  if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: #bottom edge
     ball_speed_y = abs(ball_speed_y) * -1


  # 
  # handle collisions
  #
  
  for i in range(0, len(bricks_x)) : 
    if (ball_x + BALL_WIDTH > bricks_x[i] and 
      ball_x + BALL_WIDTH < bricks_x[i] + BRICK_WIDTH and
      ball_y + BALL_HEIGHT > bricks_y[i] and
      ball_y < bricks_y[i] + BRICK_HEIGHT) :
      print("text")
      ball_speed_y *= 1.005
      ball_speed_x *= 1.005
      if (ball_speed_y > 0 and
          ball_y < bricks_y[i]) :
        ball_speed_y = abs(ball_speed_y) * -1  
        teller_bricks_x[i] -= 1
        score += 50
        popup_time = 30 # 1 second = 30 FPS
        popup_type = "50"
      if teller_bricks_x[i] == 0:
        brick_animating[i] = True
        score += 100
        popup_time = 30
        popup_type = "100"
      if brick_animating[i]:
        continue
        
      elif (ball_speed_y < 0 and
            ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT):
        ball_speed_y = abs(ball_speed_y)
        teller_bricks_x[i] -= 1
        score += 50
        popup_time = 30
        popup_type = "50"
      if teller_bricks_x[i] == 0:
        brick_animating[i] = True
        score += 100
        popup_time = 30
        popup_type = "100"
          
      elif (ball_speed_x > 0 and
            ball_x < bricks_x[i]) :
        ball_speed_x = abs(ball_speed_x) * -1
      if teller_bricks_x[i] == 0:
        brick_animating[i] = True
        score += 100
        popup_time = 30
        popup_type = "100"
        
      elif (ball_speed_x < 0 and
            ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH):
        ball_speed_x = abs(ball_speed_x)
        teller_bricks_x[i] -= 1
      if teller_bricks_x[i] == 0:
        brick_animating[i] = True
        score += 100
        popup_time = 30
        popup_type = "100"
        
  if len(bricks_x) == 0:
    level += 1
    if level == 3:
      ball_speed_x = 0
      ball_speed_y = 0
      # if won
      game_status_msg = "You win!"
      game_status = "win"
    elif level == 2:
      bricks_x = level2_x.copy()
      bricks_y = level2_y.copy()
      teller_bricks_x = level2_teller.copy()
      ball_x = 0
      ball_y = 100
    elif level == 1:
      bricks_x = level1_x.copy()
      bricks_y = level1_y.copy()
      teller_bricks_x = level1_teller.copy()
      ball_x = 0
      ball_y = 100

  
  if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
    ball_speed_x = 0
    ball_speed_y = 0
    # if dead
    game_status = "lost"

  if score > highscore:
    highscore = score

  for i in range(len(bricks_x)):
    if brick_animating[i]:
        bricks_y[i] -= 15

        i = 0
  while i < len(bricks_x):
    if brick_animating[i] and bricks_y[i] < -BRICK_HEIGHT:
        bricks_x.pop(i)
        bricks_y.pop(i)
        teller_bricks_x.pop(i)
        brick_animating.pop(i)
    else:
        i += 1
  # 
  # draw everything
  #
 # clear screen
  screen.fill('pink') # background has the color pink
  # draw ball
  screen.blit(ball_img, (ball_x, ball_y))
  # draw paddle
  screen.blit(paddle_img, (paddle_x, paddle_y))
  # draw score+50
  if popup_time > 0:
    if popup_type == "50":  
      screen.blit(score50_img, (popup_x, popup_y))
    elif popup_type == "100":
      screen.blit(score100_img, (popup_x, popup_y))
    popup_time -= 1
# draw brick

  for i in range(len(bricks_x)):
    if level == 1:
      if teller_bricks_x[i] >= 2:
          screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
      elif teller_bricks_x[i] == 1:
          screen.blit(brick_img2, (bricks_x[i], bricks_y[i]))
    elif level == 2:
      if bricks_y[i] == 64 and teller_bricks_x[i] >= 2:
        screen.blit(brick_img3, (bricks_x[i], bricks_y[i]))
      elif bricks_y[i] == 64 and teller_bricks_x[i] == 1:
        screen.blit(brick_img4, (bricks_x[i], bricks_y[i]))
      elif bricks_y[i] == 32 or bricks_y[i] == 96 and teller_bricks_x[i] >= 2:
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
      elif bricks_y[i] == 32 or bricks_y[i] == 96 and teller_bricks_x[i] == 1:
        screen.blit(brick_img2, (bricks_x[i], bricks_y[i]))
    elif level == 3:
      if teller_bricks_x[i] >= 2:
        screen.blit(brick_img3, (bricks_x[i], bricks_y[i]))
      elif teller_bricks_x[i] == 1:
          screen.blit(brick_img4, (bricks_x[i], bricks_y[i]))


  for i in range(len(bricks_x)):

    if brick_animating[i]:
        # animatie tekenen
        screen.blit(brick_img2, (bricks_x[i], bricks_y[i]))

    elif teller_bricks_x[i] == 2:
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))

    elif teller_bricks_x[i] == 1:
        screen.blit(brick_img2, (bricks_x[i], bricks_y[i]))
        
  if game_status == "lost":
    screen.fill('black')
    game_status_msg = "You lost! Press R to restart."


  # draw game status message
  game_status_img = font.render(game_status_msg, True, 'green')
  screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.get_width() / 2), (SCREEN_HEIGHT / 2) - 100)) # (0, 0) is top left corner of screen
  
  score_img = font.render("Score: " + str(score), True, 'green')
  screen.blit(score_img, ((SCREEN_WIDTH - score_img.get_width()), 8))

  if game_status == "start" or game_status == "lost":
    highscore_img = font.render("highscore: " + str(highscore), True, 'green')
    screen.blit(highscore_img, (SCREEN_WIDTH / 2 - (game_status_img.get_width() / 2), (SCREEN_HEIGHT / 2) - 50))
  # show screen
  pygame.display.flip() 
 
  # wait until next frame
  fps_clock.tick(FPS) # Sleep the remaining time of this frame



print('mygame stopt running')
