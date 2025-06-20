#
# BREAKOUT GAME 
# Dankduck

import pygame, time
import random

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
STAR_WIDTH = 40
STAR_HEIGHT = 38.125
lifes = 3
msg_timer = 0         # The time a message is shown
score = 0

paused = True
game_ended = False
fire_ball = False
wide_paddle = False
wide_paddle_timer = 0

ball_x = 500
ball_speed_x = 7
ball_speed_y = 6 # speed of ball in y-direction in pixels per frame
ball_y = 300  # y-position of ball in pixels
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT / 2 + 300
paddle_speed_1 = 20
paddle_speed_2 = 60
random_1 = -1
random_2 = 1
collision_paddle = False
any_key_pressed = False
level = 1
new_level = False
score_gain = 50

brick_not_broken_x = []
brick_not_broken_y = []
brick_broken_x = []
brick_broken_y = []
broken_bricks = []
brick_colour = []
brick_broken_colour = []
star_positions_x = []
star_positions_y = []
star_speed = 7
removed_stars = []
removed_bricks = []
remove_counter = 0

x = 0
y = 58
for i in range (0, 5):
  for j in range (0, 13):
    brick_not_broken_x.append((x * BRICK_WIDTH) + 16)
    x = x + 1
    brick_not_broken_y.append(y)
    broken_bricks.append(0)
    brick_colour.append(random.randint(0, 9))
  x = 0
  y = y + 32

balls_x = []
ball_speeds_x = []
balls_y = []
ball_speeds_y = []

for i in range(1):
  balls_x.append(paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2)
  balls_y.append(paddle_y - BALL_HEIGHT)
  ball_speeds_x.append(ball_speed_x)
  ball_speeds_y.append(ball_speed_y)

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

#background images
back_ground_img = pygame.image.load('background_space_breakout_game.jpeg')

# reads spritesheet with all of the images

brick_coördinates_x = [772, 0, 0, 386, 386, 386, 386, 772, 772, 772]
brick_coördinates_y = [390, 130, 390, 130, 390, 650, 780, 0, 260, 520]
broken_brick_coördinates_x = [0, 0, 0, 386, 386, 386, 0, 772, 772, 0]
broken_brick_coördinates_y = [0, 260, 520, 0, 260, 520, 780, 650, 130, 650]
brick_imgs_not_broken = []
brick_imgs_broken = []

for i in range(0, len(brick_coördinates_x)):
  brick_imgs_not_broken.append(0)
  brick_imgs_broken.append(0)


spritesheet_1 = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   
spritesheet_2 = pygame.image.load('Paddle_breedv2.png').convert_alpha()
spritesheet_3 = pygame.image.load('Homescreen.png').convert_alpha()     

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)                      # Creates an image of 64 x 64 pixels
ball_img.blit(spritesheet_1, (0, 0), (1403, 652, 64, 64))                   # Gets the image of the ball from x = 1403 pixels and y = 652 pixels
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))    # Changes the width and the height from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT

heart_img = pygame.Surface((64, 58), pygame.SRCALPHA) 
heart_img.blit(spritesheet_1, (0, 0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (64, 58))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet_1, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

for i in range(0, len(brick_coördinates_x)):
  brick_imgs_not_broken[i] = pygame.Surface((384, 128), pygame.SRCALPHA)
  brick_imgs_not_broken[i].blit(spritesheet_1, (0, 0), (brick_coördinates_x[i], brick_coördinates_y[i], (brick_coördinates_x[i] + 384), (brick_coördinates_y[i] + 518)))
  brick_imgs_not_broken[i] = pygame.transform.scale(brick_imgs_not_broken[i], (BRICK_WIDTH, BRICK_HEIGHT))

for i in range(0, len(brick_coördinates_x)):
  brick_imgs_broken[i] = pygame.Surface((384, 128), pygame.SRCALPHA)
  brick_imgs_broken[i].blit(spritesheet_1, (0, 0), (broken_brick_coördinates_x[i], broken_brick_coördinates_y[i], (broken_brick_coördinates_x[i] + 384), (broken_brick_coördinates_y[i] + 518)))
  brick_imgs_broken[i] = pygame.transform.scale(brick_imgs_broken[i], (BRICK_WIDTH, BRICK_HEIGHT))

star_img = pygame.Surface((64, 61), pygame.SRCALPHA)  
star_img.blit(spritesheet_1, (0, 0), (772, 846, 836, 907))
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))

wide_paddle_img = pygame.Surface((732, 128), pygame.SRCALPHA)  
wide_paddle_img.blit(spritesheet_2, (0, 0), (0, 0, 732, 128))
wide_paddle_img = pygame.transform.scale(wide_paddle_img, (PADDLE_WIDTH * 1.5, PADDLE_HEIGHT))

homescreen_img = pygame.Surface((1280, 720), pygame.SRCALPHA)  
homescreen_img.blit(spritesheet_3, (0, 0), (0, 0, 1280, 720))
homescreen_img = pygame.transform.scale(homescreen_img, (1280, 720))

#
#
# game loop
#

print('mygame is running')
running = True
while any_key_pressed == False:
  screen.blit(back_ground_img, (0, 0))
  screen.blit(homescreen_img, (0, 0))
  pygame.display.flip()
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        any_key_pressed = True
while running:
    
    #
    # read events
    # 
    for event in pygame.event.get():   # Reads all events
        if event.type == pygame.QUIT:  # The GUI closes
            running = False            # Stops the program
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_z:
            lifes += 1
            game_status_msg = "extra life"
            msg_timer = FPS * 3
          elif event.key == pygame.K_m and not game_ended:
            for i in range(50):
              balls_x.append(paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2)
              balls_y.append(paddle_y - BALL_HEIGHT - 2)
              ball_speeds_x.append(random.randint(-15, 14) + random.random())
              ball_speeds_y.append(random.randint(10 , 15) + random.random())
            game_status_msg = "50 balls"
            msg_timer = FPS * 3
          elif event.key == pygame.K_c:
            for j in range(len(balls_x)):
              ball_speeds_x[j] = ball_speeds_x[j] * 1.5
              ball_speeds_y[j] = ball_speeds_y[j] * 1.5
            game_status_msg = "speed"
            msg_timer = FPS * 3
          elif event.key == pygame.K_o and not game_ended:
            balls_x.append(paddle_x + (PADDLE_WIDTH / 2))
            balls_y.append(paddle_y)
            ball_speeds_x.append(random.randint(-11, 9) + random.random())
            ball_speeds_y.append(-ball_speed_y * 1.4)
            game_status_msg = "extra ball"
            msg_timer = FPS * 3
          elif event.key == pygame.K_q:
            fire_ball = True
            game_status_msg = "fire ball"
            msg_timer = FPS * 3
          elif event.key != pygame.K_q:
            fire_ball = False
    keys = pygame.key.get_pressed()    # Checks if keys are pressed
    if keys[pygame.K_p]: # checks if p is pressed
      paused = True
    elif any(keys) and not keys[pygame.K_m] and not keys[pygame.K_p] and paused == True:
      paused = False    
    # 
    # move everything
    #

    #move paddle
    if keys[pygame.K_s]:
      if keys[pygame.K_d] and paddle_x + PADDLE_WIDTH < SCREEN_WIDTH:
        paddle_x += paddle_speed_2
      if keys[pygame.K_a] and paddle_x > 0:
        paddle_x -= paddle_speed_2
    else:
      if keys[pygame.K_d] and paddle_x + PADDLE_WIDTH < SCREEN_WIDTH:
        paddle_x += paddle_speed_1
      if keys[pygame.K_a] and paddle_x > 0:
        paddle_x -= paddle_speed_1

    # move ball
    
    
    if paused:
      if new_level == True:  
        game_status_msg = "press any key to start level " + str(level)
      elif new_level == False:
        game_status_msg = "press any key to start"
      star_speed = 0
    elif not paused and not game_ended:
      new_level = False
      star_speed = 6
      if msg_timer > 0 and game_status_msg != "press any key to start" and game_status_msg != "press any key to start level " + str(level):
        msg_timer -= 1
      else:
        game_status_msg = ""
      for j in range(len(balls_x)):
        if ball_speeds_x[j] > BALL_WIDTH - 1:
          ball_speeds_x[j] = BALL_WIDTH - 1
        if ball_speeds_x[j] < -BALL_WIDTH + 1:
          ball_speeds_x[j] = -BALL_WIDTH + 1
        if ball_speeds_y[j] > BALL_HEIGHT - 1:
          ball_speeds_y[j] = BALL_HEIGHT - 1
        if ball_speeds_y[j] < -BALL_WIDTH + 1:
          ball_speeds_y[j] = -BALL_WIDTH + 1
        balls_x[j] += ball_speeds_x[j]
        balls_y[j] += ball_speeds_y[j]

      # bounce ball
        if balls_x[j] < 0 : # left edge
          ball_speeds_x[j] = abs(ball_speeds_x[j]) # positive x-speed = move right
        if balls_x[j] + BALL_WIDTH > SCREEN_WIDTH: # right edge
          ball_speeds_x[j] = abs(ball_speeds_x[j]) * -1 # negative x-speed = move left

        if balls_y[j] < 0: # top edge
          ball_speeds_y[j] = abs(ball_speeds_y[j]) # positive y-speed = move right down
        if balls_y[j] + BALL_HEIGHT > SCREEN_HEIGHT: # bottom edge
          ball_speeds_y[j] = abs(ball_speeds_y[j]) * -1 # negative y-speed = move up
      
        if balls_y[j] + BALL_HEIGHT >= paddle_y and balls_y[j] <= paddle_y + PADDLE_HEIGHT and balls_x[j] > paddle_x and balls_x[j] < paddle_x + PADDLE_WIDTH and collision_paddle == False:
          collision_paddle = True
          if balls_x[j] + BALL_WIDTH > paddle_x + PADDLE_WIDTH and ball_speeds_x[j] < 0:
            ball_speeds_x[j] = abs(ball_speeds_x[j])
            if balls_y[j] + BALL_HEIGHT < paddle_y + (PADDLE_HEIGHT / 2) and ball_speeds_y[j] > 0:
              ball_speeds_y[j] = abs(ball_speeds_y[j]) * -1
          elif balls_x[j]< paddle_x and ball_speeds_x[j] > 0:
            ball_speeds_x[j] = abs(ball_speeds_x[j])
            if balls_y[j] + BALL_HEIGHT < paddle_y + (PADDLE_HEIGHT / 2) and ball_speeds_y[j] > 0:
              ball_speeds_y[j] = abs(ball_speeds_y[j]) * -1
          elif balls_y[j] + BALL_HEIGHT > paddle_y and ball_speeds_y[j] > 0:
            ball_speeds_y[j] = abs(ball_speeds_y[j]) * -1
        else:
          collision_paddle = False
        
        score_gain = level * 50
        if score_gain > 300:
          score_gain = 300
        for i in range (0, len(brick_not_broken_x)):
            if balls_y[j] + BALL_HEIGHT >= brick_not_broken_y[i] and balls_y[j] <= brick_not_broken_y[i] + BRICK_HEIGHT:
              if balls_x[j] + BALL_WIDTH > brick_not_broken_x[i] and balls_x[j] < brick_not_broken_x[i] + BRICK_WIDTH:
                if not fire_ball:
                  ball_speeds_x[j] = ball_speeds_x[j] * 1.04
                  ball_speeds_y[j] = ball_speeds_y[j] * 1.04
                if broken_bricks[i] == 1:
                  if random.randint(1, 2) == 1:
                    star_positions_x.append(brick_not_broken_x[i] + (BRICK_WIDTH / 2) + ((random.random() - 0.5) * BRICK_WIDTH * 0.75))
                    star_positions_y.append(brick_not_broken_y[i] + (BRICK_HEIGHT / 2))
                if ball_speeds_y[j] > 0 and balls_y[j] < brick_not_broken_y[i]:
                  if not fire_ball:
                    ball_speeds_x[j] = ball_speeds_x[j] * (1 + ((random.random() - 0.5) * 0.025))
                    ball_speeds_y[j] = abs(ball_speeds_y[j]) * -1
                  if broken_bricks[i] == 0:
                    broken_bricks[i] = 1
                  else:
                    brick_not_broken_x.pop(i)
                    brick_not_broken_y.pop(i)
                    brick_colour.pop(i)
                    broken_bricks.pop(i)
                    score += score_gain
                  break
                elif ball_speeds_y[j] < 0 and balls_y[j] + BALL_HEIGHT > brick_not_broken_y[i] + BRICK_HEIGHT:
                  if not fire_ball:
                    ball_speeds_x[j] = ball_speeds_x[j] * (1 + ((random.random() - 0.5) * 0.025))
                    ball_speeds_y[j] = abs(ball_speeds_y[j])
                  if broken_bricks[i] == 0:
                    broken_bricks[i] = 1
                  else:
                    brick_not_broken_x.pop(i)
                    brick_not_broken_y.pop(i)
                    brick_colour.pop(i)
                    broken_bricks.pop(i)
                    score += score_gain
                  break
                elif ball_speeds_x[j] > 0 and balls_x[j] + BALL_WIDTH > brick_not_broken_x[i]: 
                  if not fire_ball:
                    ball_speeds_y[j] = ball_speeds_y[j] * (1 + ((random.random() - 0.5) * 0.025))  
                    ball_speeds_x[j] = abs(ball_speeds_x[j]) * -1
                  if broken_bricks[i] == 0:
                    broken_bricks[i] = 1
                  else:
                    brick_not_broken_x.pop(i)
                    brick_not_broken_y.pop(i)
                    brick_colour.pop(i)
                    broken_bricks.pop(i)
                    score += score_gain
                  break
                elif ball_speeds_x[j] < 0 and balls_x[j] + BALL_WIDTH > brick_not_broken_x[i] + BRICK_WIDTH:
                  if not fire_ball:  
                    ball_speeds_y[j] = ball_speeds_y[j] * (1 + ((random.random() - 0.5) * 0.025))
                    ball_speeds_x[j] = abs(ball_speeds_x[j])
                  if broken_bricks[i] == 0:
                    broken_bricks[i] = 1
                  else:
                    brick_not_broken_x.pop(i)
                    brick_not_broken_y.pop(i)
                    brick_colour.pop(i)
                    broken_bricks.pop(i)
                    score += score_gain
                  break
    
    for i in range(0, len(broken_bricks)):
      if broken_bricks[i] == 1 and level <= 2:
        if random.randint(1, 2) == 1:
          star_positions_x.append(brick_not_broken_x[i] + (BRICK_WIDTH / 2) + ((random.random() - 0.5) * BRICK_WIDTH * 0.75))
          star_positions_y.append(brick_not_broken_y[i] + (BRICK_HEIGHT / 2))
        removed_bricks.append(i)
        score += score_gain
    
    remove_counter = 0
    for i in range(0, len(removed_bricks)):
        brick_not_broken_x.pop(removed_bricks[i] - remove_counter)
        brick_not_broken_y.pop(removed_bricks[i] - remove_counter)
        brick_colour.pop(removed_bricks[i] - remove_counter)
        broken_bricks.pop(removed_bricks[i] - remove_counter)
        remove_counter += 1
    
    removed_bricks.clear()
    
    for i in range(0, (len(star_positions_x))):
      if star_positions_y[i] + STAR_HEIGHT > paddle_y + PADDLE_HEIGHT:
        removed_stars.append(i)
      elif star_positions_x[i] < paddle_x + PADDLE_WIDTH and star_positions_x[i] + STAR_WIDTH > paddle_x:
        if star_positions_y[i] + STAR_HEIGHT > paddle_y:
          removed_stars.append(i)
          if wide_paddle == False and lifes <= 4:
            random_powerup = random.randint(1, 4)
          elif lifes >= 4 and wide_paddle == False:
            random_powerup = random.randint(2, 4)
          elif wide_paddle == True and lifes <= 4:
            random_powerup = random.randint(1, 4)
            if random_powerup == 2:
              random_powerup = 1
          else:
            if random.randint(1, 2) == 1:
              random_powerup = 2
            else:
              random_powerup = 4
          if random_powerup == 1:
            lifes += 1
            game_status_msg = "extra life"
            msg_timer = FPS * 3
          elif random_powerup == 2:
            balls_x.append(paddle_x + (PADDLE_WIDTH / 2))
            balls_y.append(paddle_y)
            ball_speeds_x.append(random.randint(-11, 9) + random.random())
            ball_speeds_y.append(-ball_speed_y * 1.4)
            game_status_msg = "extra ball"
            msg_timer = FPS * 3
          elif random_powerup == 3:
            wide_paddle = True
            wide_paddle_timer = 1
            paddle_x -= 36
            game_status_msg = "wide paddle"
            msg_timer = FPS * 3
          elif random_powerup == 4:
            game_status_msg = "500 points"
            score += 500

    remove_counter = 0
    for i in range(0, len(removed_stars)):
        star_positions_x.pop(removed_stars[i] - remove_counter)
        star_positions_y.pop(removed_stars[i] - remove_counter)
        remove_counter += 1

    removed_stars.clear()

    for i in range(len(star_positions_x)):
        star_positions_y[i] += star_speed

    if wide_paddle == True:
      wide_paddle_timer = wide_paddle_timer + 1
      if wide_paddle_timer > 180:
        wide_paddle = False
        wide_paddle_timer = 0
    # 
    # handle collisions
    #
    if len(brick_not_broken_x) == 0 and len(brick_broken_x) == 0:
      ball_speed_y = 7
      ball_speed_x = 6
      #game_ended = True
      #star_speed = 0
      remove_counter = 0
      star_positions_x.clear()
      star_positions_y.clear()
      #game_status_msg = "You Won!"
      #paddle_speed_1 = 0
      #paddle_speed_2 = 0
      remove_counter = 0
      ball_speeds_x.clear()
      ball_speeds_y.clear()
      balls_x.clear()
      balls_y.clear()
      
      x = 0
      y = 58
      for i in range (0, 5):
        for j in range (0, 13):
          brick_not_broken_x.append((x * BRICK_WIDTH) + 16)
          x = x + 1
          brick_not_broken_y.append(y)
          broken_bricks.append(0)
          brick_colour.append(random.randint(0, 9))
        x = 0
        y = y + 32
      balls_x.append(paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2)
      balls_y.append(paddle_y - BALL_HEIGHT)
      ball_speeds_x.append(ball_speed_x)
      ball_speeds_y.append(ball_speed_y)
      paused = True
      new_level = True
      any_key_pressed = False
      game_status_msg = "You completed level " + str(level) + "! Press any key to continue."
      colour = "white"
      while any_key_pressed == False:
        screen.blit(back_ground_img, (0, 0))
        game_status_img = font.render(game_status_msg,True, colour)
        screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) / 2, 230))
        pygame.display.flip()
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            any_key_pressed = True
      while any_key_pressed == True:
        game_status_msg = ""
        for event in pygame.event.get():
          if event.type != pygame.KEYDOWN:
            any_key_pressed = False
      level = level + 1

    # 
    # draw everything
    #

    # clear screen
    screen.blit(back_ground_img, (0, 0)) # Sets background color

    # draw lives
    for i in range(lifes):
      screen.blit(heart_img, (SCREEN_WIDTH - (i + 1) * 64, 0))

    # draw ball
    for i in range(len(balls_x)):
      screen.blit(ball_img, (balls_x[i], balls_y[i])) # Draws the ball
    
    # draw stars
    for i in range(0, len(star_positions_x)):
      screen.blit(star_img, (star_positions_x[i], star_positions_y[i]))

    # draw paddle
    if wide_paddle == True:
      screen.blit(wide_paddle_img, (paddle_x, paddle_y))
      PADDLE_WIDTH = 216
    else:
      screen.blit(paddle_img, (paddle_x, paddle_y))
      PADDLE_WIDTH = 144
    
    # draw brick
    for i in range (-1, len(brick_not_broken_x) - 1):
      if broken_bricks[i] == 0:
        screen.blit(brick_imgs_not_broken[brick_colour[i]], (brick_not_broken_x[i], brick_not_broken_y[i]))
      else:
        screen.blit(brick_imgs_broken[brick_colour[i]], (brick_not_broken_x[i], brick_not_broken_y[i]))
    
    # draw game status message
    if len(balls_x) == 0 and lifes - 1 < 1:
      screen.blit(back_ground_img, (0, 0))
      lifes -= 1
      game_status_msg = "You lost! You got to level " + str(level) + ", with a score of " + str(score)
      paddle_speed_1 = 0
      paddle_speed_2 = 0
      game_ended = True

    elif len(balls_x) == 0 and not game_ended:
      lifes -= 1
      balls_x.append(paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2)
      balls_y.append(paddle_y - BALL_HEIGHT)
      ball_speeds_x.append(ball_speed_x)
      ball_speeds_y.append(-ball_speed_y)
      paused = True

    colour = "yellow"
    if game_status_msg == "You Won!":
      colour = "green"
    elif game_status_msg == "You lost!":
      colour = "red"
    elif game_status_msg == "press any key to start" or game_status_msg == "press any key to start level " + str(level):
      colour = "white"
    game_status_img = font.render(game_status_msg,True, colour)
    screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) / 2, 230))
    
    game_score_msg = "Score: " + str(score)
    game_score_img = font.render(game_score_msg,True, "white")
    screen.blit(game_score_img, (0,0))

    # show screen
    pygame.display.flip() 

    
      

# check if ball is below the paddle
    for i in range(len(balls_x)-1, -1, -1):
      if balls_y[i] > paddle_y + PADDLE_HEIGHT:
        balls_x.pop(i)
        balls_y.pop(i)
        ball_speeds_x.pop(i)
        ball_speeds_y.pop(i)
    
    if keys[pygame.K_e]:
      break
    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')