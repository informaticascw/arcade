#
# BREAKOUT GAME 
# 
# Teun & Lars
# 

import pygame, time
import math as ma
import random as ra

#
# define constants 
#

FPS = 60 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
HEART_WIDTH = 32
HEART_HEIGHT = 32
STAR_WIDTH = 16
STAR_HEIGHT = 16
BULLET_WIDTH = 15
BULLET_HEIGHT = 24

#
# define global variables
#

running = True
pause = True
game_status = "start"

level = 1
score = 0
hearts = 3

text_color = 'white'

game_status_msg = 'TEUN & LARS'
continue_msg = 'Press space to begin'
score_msg = ''
level_msg = ''
uitleg_msg = 'move left [a]      [d] move right'

fireball = False
fireball_counter = 0
fireball_time = 5 #s

guns = False
guns_counter = 0
guns_time = 5 #s

ball_x = (SCREEN_WIDTH - BALL_WIDTH) / 2
ball_y = SCREEN_HEIGHT - 150
balls_x = [ball_x]
balls_y = [ball_y]

ball_speed_xy = 8
balls_speed_x = []
balls_speed_y = []

bricks_x = []
bricks_y = []
bricks_status = []

bricks_spritesheet_x = [772, 772, 0, 772, 0, 772, 0, 0, 386, 386] #[roodcrack, rood, blauwcrack, blauw, geelcrack, geel, paarscrack, paars, groencrack, groen]
bricks_spritesheet_y = [130, 260, 0, 390, 650, 520, 520, 390, 0, 130] #[roodcrack, rood, blauwcrack, blauw, geelcrack, geel, paarscrack, paars, groencrack, groen]


level_size_difficulty = 0
level_brick_difficulty = 6
poplist_difficulty = 0

bricks = 0
rows = 0

hearts_x = []
hearts_y = 12

stars_x = []
stars_y = []
stars_feature = [] #0 = xtra ball; 1 = lasermode; 2 = guns

bullets_x = []
bullets_y = []

paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) / 2 
paddle_y = SCREEN_HEIGHT - 100

paddle_appearance = 0
paddle_appearance_start = 0
paddle_x_direction = 1
paddle_spritesheet_x = [1158, 1158, 1158, 1262, 1329, 1329, 1158, 1017, 772]
paddle_spritesheet_y = [594, 528, 462, 726, 792, 858, 660, 780, 780]

#
# init game
#

pygame.init()
font = pygame.font.Font("Text_font.ttf", 32)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Spritesheet.png').convert_alpha() # convert_alpha increases speed of blit and keeps transparancy of .png
background = pygame.image.load('Background.png').convert_alpha()

background_img = pygame.Surface((1280, 720))
background_img.blit(background, (0, 0), (0, 0, 1280, 720))  # copy part of sheet to image
background_img = pygame.transform.scale(background_img, (1280, 720))

heart_img = pygame.Surface((64, 58))
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))  # copy part of sheet to image
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT)) # resize image

star_img = pygame.Surface((64, 64)) # create new image
star_img.blit(spritesheet, (0, 0), (772, 846, 64, 64))  # copy part of sheet to image
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT)) # resize image

bullet_img = pygame.Surface((10, 21)) # create new image
bullet_img.blit(spritesheet, (0, 0), (0, 990, 10, 21))  # copy part of sheet to image
bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT)) # resize image

#
# functions
# 

# random
def random(percentage): 
   if percentage / 100 >= ra.random(): return True

# bricks maker
def brick_maker(level):
   global level_size_difficulty, level_brick_difficulty, poplist_difficulty
   global bricks_x, bricks_y
   global bricks_status
   global bricks, rows

   bricks_x = []
   bricks_y = []
   bricks_status = []

   if level == 1:
      bricks = 12
      rows = 6

      x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
      y_spot_brick = 2 * BRICK_HEIGHT
      bricks_status_spot = 1

      for i in range(0, rows):
         for x in range(0, bricks):
            bricks_x.append(x_spot_brick)
            bricks_y.append(y_spot_brick) 
            bricks_status.append(bricks_status_spot) 
            x_spot_brick += BRICK_WIDTH 
         x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
         y_spot_brick += BRICK_HEIGHT
      
      poplist = [0, 2, 3, 4, 7, 8, 9, 11, 12, 14, 15, 20, 21, 23, 24, 25, 26, 29, 30, 33, 34, 35, 36, 37, 38, 41, 42, 45, 46, 47, 48, 50, 51, 56, 57, 59, 60, 62, 63, 64, 67, 68, 69, 71]
      levenlist = [1, 10, 13, 22, 49, 58, 61, 70]

      for i in range(len(levenlist) -1, -1, -1):
         bricks_status[levenlist[i]] += 2

      for i in range(len(poplist) -1, -1, -1):
         bricks_x.pop(poplist[i])
         bricks_y.pop(poplist[i])
         bricks_status.pop(poplist[i])

   elif level == 2:
      bricks = 12
      rows = 8

      x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
      y_spot_brick = 2 * BRICK_HEIGHT
      bricks_status_spot = 1

      for i in range(0, rows):
         for x in range(0, bricks):
            bricks_x.append(x_spot_brick)
            bricks_y.append(y_spot_brick) 
            bricks_status.append(bricks_status_spot) 
            x_spot_brick += BRICK_WIDTH 
         x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
         y_spot_brick += BRICK_HEIGHT
      
      poplist = [0, 4, 9, 12, 16, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 39, 44, 49, 51, 56, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 75, 77, 82, 87, 89, 94]
      
      levenlist = [1, 2, 3, 13, 14, 15, 45, 46, 47, 57, 58, 59, 71, 76, 83, 88, 95]

      for i in range(len(levenlist) -1, -1, -1):
         bricks_status[levenlist[i]] += 2

      levenlist = [10, 11, 22, 23, 36, 48]

      for i in range(len(levenlist) -1, -1, -1):
         bricks_status[levenlist[i]] += 4

      for i in range(len(poplist) -1, -1, -1):
         bricks_x.pop(poplist[i])
         bricks_y.pop(poplist[i])
         bricks_status.pop(poplist[i])

   elif level == 3:
      bricks = 10
      rows = 8

      x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
      y_spot_brick = 2 * BRICK_HEIGHT
      bricks_status_spot = 9

      for i in range(0, rows):
         for x in range(0, bricks):
            bricks_x.append(x_spot_brick)
            bricks_y.append(y_spot_brick) 
            bricks_status.append(bricks_status_spot) 
            x_spot_brick += BRICK_WIDTH 
         x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
         y_spot_brick += BRICK_HEIGHT
         if bricks_status_spot >= 3: bricks_status_spot -= 2

      poplist = [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 24, 25, 27, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 52, 53, 54, 55, 56, 57, 60, 69, 70, 71, 78, 79]

      for i in range(len(poplist) -1, -1, -1):
         bricks_x.pop(poplist[i])
         bricks_y.pop(poplist[i])
         bricks_status.pop(poplist[i])

   elif level == 4 or level == 5: 
      bricks = 11
      rows = 5

      x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
      y_spot_brick = 2 * BRICK_HEIGHT

      for i in range(0, rows):
         for x in range(0, bricks):
            bricks_x.append(x_spot_brick)
            bricks_y.append(y_spot_brick) 
            bricks_status.append(((rows * 2) - 1) - (i*2))

            x_spot_brick += BRICK_WIDTH 

         x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
         y_spot_brick += BRICK_HEIGHT

      if level == 4:
         poplist = [1, 7, 12, 14, 17, 20, 21, 23, 25, 34, 39, 41, 42, 47, 50]
      if level == 5:
         poplist = [6, 11, 13, 15, 17, 20, 22, 24, 28, 31, 33, 35, 37, 39, 42, 44, 46, 53]

      for i in range(len(poplist) -1, -1, -1):
         bricks_x.pop(poplist[i])
         bricks_y.pop(poplist[i])
         bricks_status.pop(poplist[i])

   else: 
      if level_size_difficulty >= 100:
         if bricks != 13:
            bricks += 1
         if rows != 11:
            rows += 1
         if level < 20:
            poplist_difficulty += 5
         level_size_difficulty = 0 
         if level_brick_difficulty != 11:
            level_brick_difficulty += 1

      x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
      y_spot_brick = 2 * BRICK_HEIGHT
      bricks_status_spot = ra.randrange((level_brick_difficulty - 4), level_brick_difficulty)
      while bricks_status_spot%2 != 1: bricks_status_spot = ra.randrange(1, level_brick_difficulty)

      for i in range(0, rows):
         for x in range(0, bricks):
            bricks_x.append(x_spot_brick)
            bricks_y.append(y_spot_brick) 
            bricks_status.append(bricks_status_spot)
            bricks_status_spot = ra.randrange((level_brick_difficulty-4), level_brick_difficulty)
            while bricks_status_spot%2 != 1: bricks_status_spot = ra.randrange(1, level_brick_difficulty)
            x_spot_brick += BRICK_WIDTH 

         x_spot_brick = (SCREEN_WIDTH - (bricks * BRICK_WIDTH)) / 2
         y_spot_brick += BRICK_HEIGHT

      poplist = []
      for i in range(0, len(bricks_x)):
         poplist.append(i)
      ra.shuffle(poplist)
      if poplist_difficulty < ((bricks * rows)/2) and level < 100:
         for i in range(len(poplist) -1, int((len(poplist)/2) - poplist_difficulty) -1, -1):
            poplist.pop(i)
      poplist.sort()

      for i in range(len(poplist) -1, -1, -1):
         bricks_x.pop(poplist[i])
         bricks_y.pop(poplist[i])
         bricks_status.pop(poplist[i])

# set beginwaardes
def set_beginwaardes(reset_score):
   global ball_x, ball_y, balls_x, balls_y
   balls_x = []
   balls_y = []
   balls_x.append(ball_x)
   balls_y.append(ball_y)

   global paddle_x, paddle_y
   paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) / 2 
   paddle_y = SCREEN_HEIGHT - 100

   global score
   if reset_score:
      score = 0

   global level_size_difficulty, level_brick_difficulty
   if reset_score:
      level_size_difficulty = 0
      level_brick_difficulty = 4

   global game_status_msg, continue_msg, uitleg_msg
   game_status_msg = ''
   continue_msg = ''
   uitleg_msg = ''

   global hearts
   if reset_score:
      hearts = 3
      
   global balls_speed_x, balls_speed_y, ball_speed_xy
   balls_speed_x = []
   balls_speed_y = []
   balls_speed_x.append( (ma.cos( 45 * (ma.pi/180) )) * ball_speed_xy )
   balls_speed_y.append( -abs((ma.sin( 45 * (ma.pi/180) )) * ball_speed_xy ))

   global level
   if reset_score:
      level = 1

# ball paddle bounce algorithm
def ball_paddle_angle(list_spot):
   global balls_speed_x
   global balls_speed_y
   global balls_x
   global paddle_x
   global ball_speed_xy
   global PADDLE_WIDTH
   global BALL_WIDTH
   global paddle_x_direction

   multiplier = 6

   x_spot = (balls_x[list_spot] + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)
   if x_spot == 0: x_spot += 1

   rico_ball = -balls_speed_y[list_spot] / balls_speed_x[list_spot]
   hoek_ball = ma.atan(rico_ball)

   rico_spiegellijn = (PADDLE_WIDTH*multiplier)/x_spot
   hoek_spiegellijn = ma.atan(rico_spiegellijn)

   hoek_uit = -(ma.pi - (2*hoek_spiegellijn - hoek_ball))

   ball_x_direction = balls_speed_x[list_spot] / abs(balls_speed_x[list_spot])
   ball_vs_paddle_x_direction = ball_x_direction / paddle_x_direction

   balls_speed_x[list_spot] = ball_x_direction * ball_vs_paddle_x_direction * (abs(ma.cos( hoek_uit ))) * (ball_speed_xy) 
   balls_speed_y[list_spot] = (-abs(ma.sin( hoek_uit )) * (ball_speed_xy))

  
#
# game loop
#

brick_maker(1)

print('mygame is running')
running = True
while running:
    # read all events
    # to end programme when GUI is closed and to read keys using pygame.get.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move ball
    if not pause:
      for i in range(0, len(balls_x)):
         balls_x[i] += balls_speed_x[i]
         balls_y[i] += balls_speed_y[i]

         # bounce ball against edges of screen
         if balls_x[i] < 0 or balls_x[i] + BALL_WIDTH > SCREEN_WIDTH:
            balls_speed_x[i] *= -1
         if balls_y[i] < 0 or balls_y[i] + BALL_HEIGHT > SCREEN_HEIGHT:
            balls_speed_y[i] *= -1
    
    # move paddle
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not pause: # key d is pressed
       if score < 100000: paddle_x += (10 + (0.00002 * score))
       else: paddle_x += 12
       paddle_x_direction = 1
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not pause: # key a is pressed
       if score < 100000: paddle_x -= (10 + (0.00002 * score))
       else: paddle_x -= 12
       paddle_x_direction = -1

    # pause game
    if keys[pygame.K_p]:
       if not pause: pause = True
       elif pause: pause = False
       time.sleep(0.5)

    # powerups calling
    if keys[pygame.K_1]:
       fireball = True

    if keys[pygame.K_2]:
       hoekje = ra.randint(40, 140)
       balls_speed_x.append((ma.cos( hoekje * (ma.pi/180) )) * (ball_speed_xy))
       balls_speed_y.append( -abs( ma.sin( hoekje * (ma.pi/180) ) * (ball_speed_xy)) )
       balls_x.append(paddle_x + PADDLE_WIDTH/2)
       balls_y.append(ball_y)
   
    if keys[pygame.K_3]:
       guns = True

    if keys[pygame.K_4]:
       hearts += 1

    # stop paddle at end of screen
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH: # helemaal rechts
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0: # helemaal links
       paddle_x = 0

    # update ball speed
    if ball_speed_xy < 10:
      ball_speed_xy = 8 + (0.00002 * score)

    # balls bouncing
    for q in range(0, len(balls_x)):

      # ball bounces of paddle
      if (balls_x[q] + BALL_WIDTH > paddle_x and
         balls_x[q] < paddle_x + PADDLE_WIDTH and
         balls_y[q] + BALL_HEIGHT > paddle_y and
         balls_y[q] < paddle_y + PADDLE_HEIGHT): 
            
            # ball bounces against top of paddle
            if balls_speed_y[q] > 0 and balls_y[q] < paddle_y:
               ball_paddle_angle(q)
            # ball bounces against bottom of paddle
            elif balls_speed_y[q] < 0 and balls_y[q] + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
               balls_speed_y[q] *= -1
            # ball bounces against right of paddle
            elif balls_speed_x[q] > 0 and balls_x[q] < paddle_x:
               balls_speed_x[q] *= -1
            # ball bounces against left of paddle
            elif balls_speed_x[q] < 0 and balls_x[q] + BALL_WIDTH > paddle_x + PADDLE_WIDTH:
               balls_speed_x[q] *= -1

      # ball bounces of brick 
      for i in range(len(bricks_x) -1, -1, -1):
         if (balls_x[q] + BALL_WIDTH > bricks_x[i] and
            balls_x[q] < bricks_x[i] + BRICK_WIDTH and
            balls_y[q] + BALL_HEIGHT > bricks_y[i] and
            balls_y[q] < bricks_y[i] + BRICK_HEIGHT): 
            #print('brick touched at ball_x =', balls_x[q], 'and ball_y =', balls_y[q])

            if fireball == False: 
            # ball bounces against top of brick
               if balls_speed_y[q] > 0 and balls_y[q] < bricks_y[i]:
                  balls_speed_y[q] *= -1
            # ball bounces against bottom of brick
               elif balls_speed_y[q] < 0 and balls_y[q] + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                  balls_speed_y[q] *= -1
            # ball bounces against right of brick
               elif balls_speed_x[q] > 0 and balls_x[q] < bricks_x[i]:
                  balls_speed_x[q] *= -1
            # ball bounces against left of brick
               elif balls_speed_x[q] < 0 and balls_x[q] + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                  balls_speed_x[q] *= -1
               
            # powerups falling out of bricks
            if bricks_status[i] == 3 and random(25): #xtra ball, feature 0
               stars_x.append(balls_x[q])
               stars_y.append(balls_y[q])
               stars_feature.append(0)
            if bricks_status[i] == 5 and random(50): #lasermode, feature 1
               stars_x.append(balls_x[q])
               stars_y.append(balls_y[q])
               stars_feature.append(1)
            if bricks_status[i] == 7 and random(50): #guns, feature 2
               stars_x.append(balls_x[q])
               stars_y.append(balls_y[q])
               stars_feature.append(2)
            if bricks_status[i] == 1 and random(10): #hartje, feature 3
               stars_x.append(balls_x[q])
               stars_y.append(balls_y[q])
               stars_feature.append(3)

            # change appearance of blocks
            if bricks_status[i]%2 == 1:
               if random(40): 
                  bricks_status[i] -= 1
               else:
                  bricks_status[i] -= 2
            elif bricks_status[i]%2 == 0:
               bricks_status[i] -= 1
            
            # update score
            score += 100
            if level > 2:
               level_size_difficulty += 1

            # delete blocks from lists
            if bricks_status[i] == -1:
               bricks_x.pop(i)
               bricks_y.pop(i)
               bricks_status.pop(i)

            break

    # stars
    for i in range(len(stars_x) -1, -1, -1):
       # move stars
       if not pause: stars_y[i] += 5
       if pause:
          stars_x.clear()
          stars_y.clear()
          stars_feature.clear()
          break
   
       # stars hit paddle
       if (stars_x[i] + STAR_WIDTH > paddle_x and
         stars_x[i] < paddle_x + PADDLE_WIDTH and
         stars_y[i] + STAR_HEIGHT > paddle_y and
         stars_y[i] < paddle_y + PADDLE_HEIGHT): 
          if stars_feature[i] == 0:
             hoekje = ra.randint(40, 140)
             balls_speed_x.append((ma.cos( hoekje * (ma.pi/180) )) * (ball_speed_xy))
             balls_speed_y.append( -abs( ma.sin( hoekje * (ma.pi/180) )  * (ball_speed_xy)) )
             balls_x.append(stars_x[i])
             balls_y.append(stars_y[i])
          if stars_feature[i] == 1:
             fireball = True
          if stars_feature[i] == 2:
             guns = True
          if stars_feature[i] == 3:
             hearts += 1
          stars_x.pop(i)
          stars_y.pop(i)
          stars_feature.pop(i)
          break
            
       # stars hit bottom     
       if stars_y[i] + STAR_HEIGHT > SCREEN_HEIGHT:
          stars_x.pop(i)
          stars_y.pop(i)
          stars_feature.pop(i)

    # bullets
    for q in range(len(bullets_x) -1, -1, -1):
       bullets_y[q] -= 10

       # bullets hit bricks 
       for i in range(len(bricks_x) -1, -1, -1):
         if (bullets_x[q] + BULLET_WIDTH > bricks_x[i] and
            bullets_x[q] < bricks_x[i] + BRICK_WIDTH and
            bullets_y[q] + BULLET_HEIGHT > bricks_y[i] and
            bullets_y[q] < bricks_y[i] + BRICK_HEIGHT): 
            bricks_status[i] -= 1
            bullets_x.pop(q)
            bullets_y.pop(q)
            if bricks_status[i] == -1:
               bricks_x.pop(i)
               bricks_y.pop(i)
               bricks_status.pop(i)
            break

    for q in range(len(bullets_x) -1, -1, -1):
       if bullets_y[q] <= 0:
         bullets_x.pop(q)
         bullets_y.pop(q)

    # powerups 
    if fireball == True:
       fireball_counter += 1
       ball_img = pygame.Surface((74, 74)) # create new image
       ball_img.blit(spritesheet, (0, 0), (1470, 650, 74, 74))  # copy part of sheet to image
       ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) # resize image
    else:
       ball_img = pygame.Surface((64, 64)) # create new image
       ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))  # copy part of sheet to image
       ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) # resize image

    if fireball_counter >= (fireball_time * FPS):
       fireball = False
       fireball_counter = 0

    if guns == True:
       guns_counter += 1
       if guns_counter%10 == 0 and not pause:
          bullets_x.append(paddle_x)
          bullets_x.append(paddle_x + PADDLE_WIDTH - BULLET_WIDTH)
          bullets_y.append(paddle_y)
          bullets_y.append(paddle_y)
    
    if guns_counter >= (guns_time * FPS):
       guns = False
       guns_counter = 0

    # clear screen
    screen.blit(background_img, (0,0))

    # draw ball
    for q in range(0, len(balls_x)):
      screen.blit(ball_img, (balls_x[q], balls_y[q]))

    # draw stars
    for i in range(0, len(stars_x)):
       screen.blit(star_img, (stars_x[i], stars_y[i]))

    # draw bullets
    for i in range(0, len(bullets_x)):
       screen.blit(bullet_img, (bullets_x[i], bullets_y[i]))

    # draw hearts
    hearts_x = []
    hearts_y = 12
    for i in range(1, hearts + 1):
       hearts_x.append(SCREEN_WIDTH - i*(HEART_WIDTH + 12))
    for i in range(len(hearts_x) -1, -1, -1):
       screen.blit(heart_img, (hearts_x[i], hearts_y))

    # draw paddle with animation
    if guns:
      paddle_appearance_start = 6
    elif fireball:
      paddle_appearance_start = 3
    else:
      paddle_appearance_start = 0

    paddle_appearance += 1

    if paddle_appearance >= paddle_appearance_start + 3:
      paddle_appearance = paddle_appearance_start

    paddle_img = pygame.Surface((243, 64))
    paddle_img.blit(spritesheet, (0, 0), (paddle_spritesheet_x[paddle_appearance], paddle_spritesheet_y[paddle_appearance], 243, 64))
    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw bricks
    for i in range(len(bricks_x) -1, -1, -1):
       brick_img = pygame.Surface((384, 128))
       brick_img.blit(spritesheet, (0, 0), (bricks_spritesheet_x[bricks_status[i]], bricks_spritesheet_y[bricks_status[i]], 384, 128))
       brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
       screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
    
    # delete balls from list
    for q in range(len(balls_x) -1, -1, -1):
      if balls_y[q] + BALL_HEIGHT >= SCREEN_HEIGHT:
         balls_x.pop(q)
         balls_y.pop(q)
         balls_speed_x.pop(q)
         balls_speed_y.pop(q)

    # update ball speed
    if ball_speed_xy < 10:
      ball_speed_xy = 8 + (0.00002 * score)

    # check if you won
    if len(bricks_x) == 0 and not pause:
      game_status_msg = "You won!"
      continue_msg = "Press space for the next level"
      game_status = "won"
      pause = True
      level += 1

    # check if you lost
    if len(balls_x) == 0 and not pause:
       hearts -= 1
       if hearts <= 0:
          game_status_msg = "You lost!"
          continue_msg = "Press space to play again"
          pause = True
          game_status = "died"
       else: 
          game_status_msg = "You lost a heart"
          continue_msg = "Press space to continue"
          pause = True
          game_status = "lost"

    # continue game
    if pause == True and keys[pygame.K_SPACE]:
      if game_status == "lost" or game_status == "won":
         set_beginwaardes(False)
      if game_status == "died" or game_status == "start":
         set_beginwaardes(True)
      if game_status == "died" or game_status == "won" or game_status == "start":
         brick_maker(level)
      pause = False

    # print text
    game_status_img = font.render(game_status_msg, True, text_color)
    screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) / 2, (SCREEN_HEIGHT - game_status_img.get_height()) / 2))

    continue_img = font.render(continue_msg, True, text_color)
    screen.blit(continue_img, ((SCREEN_WIDTH - continue_img.get_width()) / 2, ((SCREEN_HEIGHT - continue_img.get_height()) / 2) + (2 * game_status_img.get_height() )))

    uitleg_img = font.render(uitleg_msg, True, text_color)
    screen.blit(uitleg_img, ((SCREEN_WIDTH - uitleg_img.get_width()) / 2, paddle_y))


    score_msg = str(score)
    score_img = font.render(score_msg, True, text_color)
    screen.blit(score_img, (12, 12))

    level_msg = "level " + str(level)
    level_img = font.render(level_msg, True, text_color)
    screen.blit(level_img, ((SCREEN_WIDTH - level_img.get_width()) / 2, 12))

    # show screen
    pygame.display.flip() 

    # Sleep the remaining time of this frame
    fps_clock.tick(FPS) 

print('mygame stopt running')


    # OUDE BOUNCE CODE
    # ball_speed_y = ball_speed_y * -1
    # ball_speed_x = ((ball_x + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)) * (10 / (PADDLE_WIDTH / 2))
    #                 midden van de bal            midden van de paddle             maximale x speed is 10
    # de relatieve positie van de bal ten opichte van de paddle wordt berekend en deze wordt vermenigvuldigd met een getal
    # dit getal is zo gesteld dat de max x speed uitkomt op tien, en de min waarde 0 is.