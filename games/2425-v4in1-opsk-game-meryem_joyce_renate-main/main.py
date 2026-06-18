#
# BREAKOUT GAME 
#

import pygame, time
import random

#
# definitions 
#

def resetGame_levelOne():            # Gedefineerde functie voor het restarten van de game
  global ball_x, ball_y, ball_speed_x, ball_speed_y, ballFrozen
  global paddle_x, paddle_y 
  global game_status_msg, level_status_msg, speed_status_msg, difficulty_status_msg, powerup_status_msg
  global bricks_x_yellow, bricks_y_yellow, bricks_x_dBlue, bricks_y_dBlue
  global hearts_x, hearts_y, heart_active, heart_x, heart_y, heart_speed_y
  global sniper_pu_spawned, sniper_pu_active, sniper_msg_active, sniper_pu_x, sniper_pu_y, powerups_x, powerups_y
  global debugFlag

  ball_x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
  ball_y = SCREEN_HEIGHT / 2 + 250
  ball_speed_x = 8
  ball_speed_y = -8
  ballFrozen = False
  debugFlag = False
  
  paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
  paddle_y = SCREEN_HEIGHT - 80
  
  heart_active = False
  heart_x = 0
  heart_y = 0
  heart_speed_y = 4

  sniper_pu_active = False
  sniper_pu_spawned = False
  sniper_msg_active = False
  sniper_pu_x = 0
  sniper_pu_y = 0

  # All yellow bricks
  bricks_x_yellow = [SCREEN_WIDTH - 252, SCREEN_WIDTH - 252 + BRICK_WIDTH, SCREEN_WIDTH - 252, 
                     SCREEN_WIDTH - 252 + BRICK_WIDTH, SCREEN_WIDTH - 252, SCREEN_WIDTH - 252 + BRICK_WIDTH, 
                     SCREEN_WIDTH - 252, SCREEN_WIDTH - 252 + BRICK_WIDTH]

  bricks_y_yellow = [130, 130, 130 - BRICK_HEIGHT, 130 - BRICK_HEIGHT, 130 - BRICK_HEIGHT * 2, 130 - BRICK_HEIGHT * 2, 
                     130 - BRICK_HEIGHT * 3, 130 - BRICK_HEIGHT * 3]

  # All dark blue bricks
  bricks_x_dBlue = [54, 150, 246, SCREEN_WIDTH / 2 + 100, SCREEN_WIDTH / 2 + 4, SCREEN_WIDTH / 2 + 196, SCREEN_WIDTH / 2 - 320, 
                    SCREEN_WIDTH / 2 - 416, SCREEN_WIDTH / 2 - 512, SCREEN_WIDTH / 2 - 179, SCREEN_WIDTH / 2 - 275, SCREEN_WIDTH / 2 - 83, 
                    SCREEN_WIDTH - 246, SCREEN_WIDTH - 150, SCREEN_WIDTH - 342]

  bricks_y_dBlue = [48, 80, 48, SCREEN_HEIGHT - 420, SCREEN_HEIGHT - 452, SCREEN_HEIGHT - 452, SCREEN_HEIGHT / 2, 
                    SCREEN_HEIGHT / 2 + 32, SCREEN_HEIGHT / 2, SCREEN_HEIGHT / 2 - 170, SCREEN_HEIGHT / 2 - 202, SCREEN_HEIGHT / 2 - 202, 
                    SCREEN_HEIGHT - 250, SCREEN_HEIGHT - 282, SCREEN_HEIGHT - 282]

  hearts_x = [SCREEN_WIDTH - HEART_WIDTH - 20]
  hearts_y = [10]

  powerups_x = []
  powerups_y = []

  game_status_msg = ""
  speed_status_msg = "BALL SPEED: " + str(abs(ball_speed_x))
  level_status_msg = ""
  difficulty_status_msg = ""
  powerup_status_msg = ""

def angledBouncingBall_levelOne():         # Gedefineerde functie voor het stuiteren van de bal wanneer het op bepaalde plekken op de plank landt
  global ball_x, paddle_x, ball_speed_x, ball_speed_y, speed_status_msg
  ball_center_x = ball_x + BALL_WIDTH / 2
  paddle_center_x = paddle_x + PADDLE_WIDTH / 2

  offset = ball_center_x - paddle_center_x
  relative_position = offset / PADDLE_WIDTH / 2

  MAX_SPEED = 8.75
  MIN_SPEED = 7.75

  # Bal versnellen of vertragen, hangt van positie af
  ball_speed_x += relative_position * BOUNCE_ANGLE_LEVEL_ONE

  if ball_speed_x < 0:    # Wanneer de bal naar links beweegt
    ball_speed_x = max(-MAX_SPEED, min(-MIN_SPEED, ball_speed_x))
    
  else:                   # Wanneer de bal naar rechts beweegt
    ball_speed_x = min(MAX_SPEED, max(MIN_SPEED, ball_speed_x))

  speed_status_msg = "BALL SPEED: " + str(round(abs(ball_speed_x), 2))

  # Het stuiteren
  ball_speed_y = abs(ball_speed_y) * -1

def setupGame_levelTwo():       # Gedefineerde functie voor het opzetten van de game
  global ball_x, ball_y, ball_speed_x, ball_speed_y, ballFrozen, paddle_x, paddle_y
  global bricks_x_yellow2, bricks_y_yellow2, blobs_x_yGreen, blobs_y_yGreen, bricks_x_white, bricks_y_white, bricks_yellow2_hp
  global bricks_x_brown, bricks_y_brown, bricks_x_dBrown, bricks_y_dBrown
  global heart_active, heart_x, heart_y, heart_speed_y, hearts_x, hearts_y
  global sniper_pu_active, sniper_pu_spawned, sniper_msg_active, sniper_pu_x, sniper_pu_y
  global speed_status_msg, game_status_msg, level_status_msg, difficulty_status_msg, powerup_status_msg
  global powerup_x, powerup_y, brick_got_hit, debugFlag, lasers_x_left, lasers_x_right, lasers_y_left, lasers_y_right
  global startTime

  startTime = pygame.time.get_ticks()

  ball_x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
  ball_speed_x = 8
  ball_y = SCREEN_HEIGHT / 2 + 250
  ball_speed_y = 8
  ballFrozen = False
  debugFlag = False
  
  paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
  paddle_y = SCREEN_HEIGHT - 80
  
  heart_active = False
  heart_x = 0
  heart_y = 0
  heart_speed_y = 4

  brick_got_hit = False
  sniper_pu_active = False
  sniper_pu_spawned = False
  sniper_msg_active = False
  sniper_pu_x = 0
  sniper_pu_y = 0

  # All yellow bricks
  bricks_x_yellow2 = [SCREEN_WIDTH / 2 - BRICK_WIDTH, SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, 
                      SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5 + 15, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2 - 15]

  bricks_y_yellow2 = [SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 136, 
                      SCREEN_HEIGHT / 2 + 56, SCREEN_HEIGHT / 2 + 56]
  
  bricks_yellow2_hp = []
  for i in range(len(bricks_x_yellow2)):
    bricks_yellow2_hp.append(2)
  
  # Bald eagle eyes
  blobs_x_yGreen = [SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 - EYEBALL_WIDTH, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 + BRICK_WIDTH]
  blobs_y_yGreen = [SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200]

  # All white bricks
  bricks_x_white = [SCREEN_WIDTH / 2 - BRICK_WIDTH - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2,
                  SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 - EYEBALL_WIDTH - BRICK_WIDTH, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2 + EYEBALL_WIDTH,
                  SCREEN_WIDTH / 2 - BRICK_WIDTH, SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 - EYEBALL_WIDTH - BRICK_WIDTH + 15, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2 + EYEBALL_WIDTH - 15,
                  SCREEN_WIDTH / 2 - BRICK_WIDTH, SCREEN_WIDTH / 2]

  bricks_y_white = [SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232,
                  SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 264,
                  SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 104, 
                  SCREEN_HEIGHT / 2 - 104]

  # All brown bricks
  bricks_x_brown = [SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 2 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - BRICK_WIDTH, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 3 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 + 20, SCREEN_WIDTH / 2 - BRICK_WIDTH * 4 - 20, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - BRICK_WIDTH / 2 + 15, SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 + BRICK_WIDTH / 2 - 15, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 + 20, SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 - 20, SCREEN_WIDTH / 2 + BRICK_WIDTH * 5 - 12, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 6 + 10, SCREEN_WIDTH / 2 + BRICK_WIDTH * 5 - BRICK_WIDTH / 2 + 15, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 6 + BRICK_WIDTH / 2 - 15, SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 4 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 3 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH + 10, SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - 10, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2]

  bricks_y_brown = [SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 136, 
                  SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, 
                  SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 264, 
                  SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, 
                  SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 + 24, SCREEN_HEIGHT / 2 + 24]

  # All dark brown bricks
  bricks_x_dBrown = [SCREEN_WIDTH / 2 - BRICK_WIDTH * 2, SCREEN_WIDTH / 2 + BRICK_WIDTH, SCREEN_WIDTH / 2 - BRICK_WIDTH - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 2 - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - BRICK_WIDTH / 2 - 20, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 3 - BRICK_WIDTH / 2 + 20, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - 15, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 4 + 15, SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - BRICK_WIDTH / 2 - 10, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 + BRICK_WIDTH / 2 + 10, SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - 5, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 + 5, SCREEN_WIDTH / 2 + BRICK_WIDTH * 5 - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 6 + BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5, 
                   SCREEN_WIDTH / 2 + BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2]

  bricks_y_dBrown = [SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, 
                   SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 - 8, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 136, 
                   SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, 
                   SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 296, 
                   SCREEN_HEIGHT / 2 - 296, SCREEN_HEIGHT / 2 + 24, SCREEN_HEIGHT / 2 - 8, SCREEN_HEIGHT / 2 - 8, SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 - 40]

  powerup_x = SCREEN_WIDTH - BLOB_WIDTH - 20
  powerup_y = SCREEN_HEIGHT - BLOB_HEIGHT - 10

  lasers_x_left = []
  lasers_x_right = []
  lasers_y_left = []
  lasers_y_right = []

  game_status_msg = ""
  speed_status_msg = "BALL SPEED: " + str(abs(ball_speed_x))
  level_status_msg = ""
  difficulty_status_msg = ""
  powerup_status_msg = ""

def resetGame_levelTwo():       # Gedefineerde functie voor het restarten van de game
  global hearts_x, hearts_y, startTime
  startTime = pygame.time.get_ticks() # code dubbel-op, want anders geen laser power-up na restarten level 2

  setupGame_levelTwo()
  
  hearts_x = [SCREEN_WIDTH - HEART_WIDTH - 20]
  hearts_y = [10]

def angledBouncingBall_levelTwo():         # Gedefineerde functie voor het stuiteren van de bal wanneer het op bepaalde plekken op de plank landt
  global ball_x, paddle_x, ball_speed_x, ball_speed_y, speed_status_msg
  ball_center_x = ball_x + BALL_WIDTH / 2
  paddle_center_x = paddle_x + PADDLE_WIDTH / 2

  offset = ball_center_x - paddle_center_x
  relative_position = offset / PADDLE_WIDTH / 2

  MAX_SPEED = 9.75
  MIN_SPEED = 8.75

  # Bal versnellen of vertragen, hangt van positie af
  ball_speed_x += relative_position * BOUNCE_ANGLE_LEVEL_TWO

  if ball_speed_x < 0:    # Wanneer de bal naar links beweegt
    ball_speed_x = max(-MAX_SPEED, min(-MIN_SPEED, ball_speed_x))
    
  else:                   # Wanneer de bal naar rechts beweegt
    ball_speed_x = min(MAX_SPEED, max(MIN_SPEED, ball_speed_x))

  speed_status_msg = "BALL SPEED: " + str(round(abs(ball_speed_x), 2))

  # Het stuiteren
  ball_speed_y = abs(ball_speed_y) * -1

def checksIfSniperPU_shouldSpawn():
  global sniper_pu_y, sniper_pu_x, sniper_pu_spawned, sniper_pu_startTime
  
  if not sniper_pu_active and not sniper_pu_spawned and (len(bricks_x_yellow2) + len(bricks_x_dBrown) + len(bricks_x_white) + len(bricks_x_brown) + len(blobs_x_yGreen) == 3 or 
    len(bricks_x_yellow2) + len(bricks_x_dBrown) + len(bricks_x_white) + len(bricks_x_brown) + len(blobs_x_yGreen) == 15 or 
    len(bricks_x_yellow2) + len(bricks_x_dBrown) + len(bricks_x_white) + len(bricks_x_brown) + len(blobs_x_yGreen) == 35):
      
      sniper_pu_y = paddle_y + PADDLE_HEIGHT / 2 - BLOB_HEIGHT / 2  # spawns it on the horizontal line of the paddle
      
      while True: # checks if the spawned power-up blob overlaps with the paddle
        sniper_pu_x = random.randint(50, SCREEN_WIDTH - 50 - BLOB_WIDTH)  # spawns it in a random place between given parameters
        if not (sniper_pu_x + BLOB_WIDTH > paddle_x and sniper_pu_x < paddle_x + PADDLE_WIDTH):
            break
      
      sniper_pu_spawned = True
      sniper_pu_startTime = pygame.time.get_ticks()

def laserBrickCollisions_levelTwo(): # Gedefineerde functie voor de collisies tussen lasers en bricks
  global lasers_x_left, lasers_x_right, lasers_y_left, lasers_y_right, laser_x_left, laser_x_right, laser_y
  global bricks_x_yellow2, bricks_yellow2_hp, bricks_x_brown, bricks_x_white, bricks_x_dBrown, blobs_x_yGreen, brick_got_hit
  global bricks_y_yellow2, bricks_y_brown, bricks_y_white, bricks_y_dBrown, blobs_y_yGreen
  global heart_x, heart_y, heart_active
  
  # All yellow bricks
  # Check left lasers
  for i in range(len(lasers_x_left) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_yellow2) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_left[i] + LASER_WIDTH > bricks_x_yellow2[j] and 
        lasers_x_left[i] < bricks_x_yellow2[j] + BRICK_WIDTH and 
        lasers_y_left[i] + LASER_HEIGHT > bricks_y_yellow2[j] and 
        lasers_y_left[i] < bricks_y_yellow2[j] + BRICK_HEIGHT):

        lasers_x_left.pop(i)
        lasers_y_left.pop(i)

        bricks_yellow2_hp[i] -= 1
        brick_got_hit = True
          
        if bricks_yellow2_hp[i] <= 0:
          bricks_x_yellow2.pop(j)   
          bricks_y_yellow2.pop(j)
          bricks_yellow2_hp.pop(j)
          brick_got_hit = True

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # Check right lasers
  for i in range(len(lasers_x_right) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_yellow2) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_right[i] + LASER_WIDTH > bricks_x_yellow2[j] and 
        lasers_x_right[i] < bricks_x_yellow2[j] + BRICK_WIDTH and 
        lasers_y_right[i] + LASER_HEIGHT > bricks_y_yellow2[j] and 
        lasers_y_right[i] < bricks_y_yellow2[j] + BRICK_HEIGHT):

        lasers_x_right.pop(i)
        lasers_y_right.pop(i)

        bricks_yellow2_hp[i] -= 1
        brick_got_hit = True
          
        if bricks_yellow2_hp[i] <= 0:
          bricks_x_yellow2.pop(j)   
          bricks_y_yellow2.pop(j)
          bricks_yellow2_hp.pop(j)
          brick_got_hit = True

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # Eagle eyes
  # Check left lasers
  for i in range(len(lasers_x_left) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(blobs_x_yGreen) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_left[i] + LASER_WIDTH > blobs_x_yGreen[j] and 
        lasers_x_left[i] < blobs_x_yGreen[j] + BLOB_WIDTH and 
        lasers_y_left[i] + LASER_HEIGHT > blobs_y_yGreen[j] and 
        lasers_y_left[i] < blobs_y_yGreen[j] + BLOB_HEIGHT):

        lasers_x_left.pop(i)
        lasers_y_left.pop(i)
          
        blobs_x_yGreen.pop(j)   
        blobs_y_yGreen.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # Check right lasers
  for i in range(len(lasers_x_right) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(blobs_x_yGreen) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_right[i] + LASER_WIDTH > blobs_x_yGreen[j] and 
        lasers_x_right[i] < blobs_x_yGreen[j] + BLOB_WIDTH and 
        lasers_y_right[i] + LASER_HEIGHT > blobs_y_yGreen[j] and 
        lasers_y_right[i] < blobs_y_yGreen[j] + BLOB_HEIGHT):

        lasers_x_right.pop(i)
        lasers_y_right.pop(i)

          
        blobs_x_yGreen.pop(j)   
        blobs_y_yGreen.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break

  # All white bricks
  # Check left lasers
  for i in range(len(lasers_x_left) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_white) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_left[i] + LASER_WIDTH > bricks_x_white[j] and 
        lasers_x_left[i] < bricks_x_white[j] + BRICK_WIDTH and 
        lasers_y_left[i] + LASER_HEIGHT > bricks_y_white[j] and 
        lasers_y_left[i] < bricks_y_white[j] + BRICK_HEIGHT):

        lasers_x_left.pop(i)
        lasers_y_left.pop(i)
          
        bricks_x_white.pop(j)   
        bricks_y_white.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # Check right lasers
  for i in range(len(lasers_x_right) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_white) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_right[i] + LASER_WIDTH > bricks_x_white[j] and 
        lasers_x_right[i] < bricks_x_white[j] + BRICK_WIDTH and 
        lasers_y_right[i] + LASER_HEIGHT > bricks_y_white[j] and 
        lasers_y_right[i] < bricks_y_white[j] + BRICK_HEIGHT):

        lasers_x_right.pop(i)
        lasers_y_right.pop(i)

          
        bricks_x_white.pop(j)   
        bricks_y_white.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # All brown bricks
  # Check left lasers
  for i in range(len(lasers_x_left) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_brown) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_left[i] + LASER_WIDTH > bricks_x_brown[j] and 
        lasers_x_left[i] < bricks_x_brown[j] + BRICK_WIDTH and 
        lasers_y_left[i] + LASER_HEIGHT > bricks_y_brown[j] and 
        lasers_y_left[i] < bricks_y_brown[j] + BRICK_HEIGHT):

        lasers_x_left.pop(i)
        lasers_y_left.pop(i)
          
        bricks_x_brown.pop(j)   
        bricks_y_brown.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # Check right lasers
  for i in range(len(lasers_x_right) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_brown) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_right[i] + LASER_WIDTH > bricks_x_brown[j] and 
        lasers_x_right[i] < bricks_x_brown[j] + BRICK_WIDTH and 
        lasers_y_right[i] + LASER_HEIGHT > bricks_y_brown[j] and 
        lasers_y_right[i] < bricks_y_brown[j] + BRICK_HEIGHT):

        lasers_x_right.pop(i)
        lasers_y_right.pop(i)

          
        bricks_x_brown.pop(j)   
        bricks_y_brown.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break

  # All dark brown bricks
  # Check left lasers
  for i in range(len(lasers_x_left) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_dBrown) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_left[i] + LASER_WIDTH > bricks_x_dBrown[j] and 
        lasers_x_left[i] < bricks_x_dBrown[j] + BRICK_WIDTH and 
        lasers_y_left[i] + LASER_HEIGHT > bricks_y_dBrown[j] and 
        lasers_y_left[i] < bricks_y_dBrown[j] + BRICK_HEIGHT):

        lasers_x_left.pop(i)
        lasers_y_left.pop(i)
          
        bricks_x_dBrown.pop(j)   
        bricks_y_dBrown.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
  
  # Check right lasers
  for i in range(len(lasers_x_right) -1, -1, -1):            # Splitst indexes for lasers en bricks, voorkomt index error
    for j in range(len(bricks_x_dBrown) - 1, -1, -1):      # Zorgt ervoor dat er meerdere bricks per frame gebroken kunnen worden
      if (lasers_x_right[i] + LASER_WIDTH > bricks_x_dBrown[j] and 
        lasers_x_right[i] < bricks_x_dBrown[j] + BRICK_WIDTH and 
        lasers_y_right[i] + LASER_HEIGHT > bricks_y_dBrown[j] and 
        lasers_y_right[i] < bricks_y_dBrown[j] + BRICK_HEIGHT):

        lasers_x_right.pop(i)
        lasers_y_right.pop(i)

          
        bricks_x_dBrown.pop(j)   
        bricks_y_dBrown.pop(j)

        checksIfSniperPU_shouldSpawn()
        
        # Hearts/HP
        if not heart_active and random.randint(1, 35) == 1:
          heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
          heart_y = random.randint(200, SCREEN_HEIGHT - 380)
          heart_active = True

        break
    
def setupGame_levelThree():       # Gedefineerde functie voor het opzetten van de game
  global game_status_msg, level_status_msg, difficulty_status_msg

  game_status_msg = ""
  level_status_msg = ""
  difficulty_status_msg = ""

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BOUNCE_ANGLE_LEVEL_ONE = 5 # Factor waarmee de snelheid wordt verandert
BOUNCE_ANGLE_LEVEL_TWO = 5

BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

LASER_WIDTH = 8
LASER_HEIGHT = 25
LASER_SPEED_Y = -25
LASER_COOLDOWN_TIME = 15

BRICK_WIDTH = 96
BRICK_HEIGHT = 32

HEART_WIDTH = 28
HEART_HEIGHT = 26

BLOB_WIDTH = 24
BLOB_HEIGHT = 24

EYEBALL_WIDTH = 32
EYEBALL_HEIGHT = 32

# variabelen met hoofdletters: constant, kleine letters: veranderbaar
startTime = None
laser_pu_startTime = None
checkpoint_progress = {
  "c_levelone" : "one", 
  "c_leveltwo" : "two", 
  "c_levelthree" : "three", 
  "c_levelfour" : "four", 
  "c_levelfive" : "five",
  "c_winscreen" : "win"
}                             # ik weet dat het makkelijker kan, maar ik wilde gewoon een dict uitproberen
checkpoint = ""

subtitle = ""
subtitle2 = ""
subtitle3 = ""

game_status_msg = ""
level_status_msg = ""
difficulty_status_msg = ""
powerup_status_msg = ""

ball_x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
ball_speed_x = 8
ball_y = SCREEN_HEIGHT / 2 + 250
ball_speed_y = -8
speed_status_msg = "BALL SPEED: " + str(abs(ball_speed_x))

debugFlag = False
ballFrozen = False
heart_active = False
heart_x = 0
heart_y = 0
heart_speed_y = 4

paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 80

brick_got_hit = False
sniper_pu_active = False
sniper_pu_spawned = False
sniper_msg_active = False
sniper_pu_x = 0
sniper_pu_y = 0

laser_pu_active = False
laser_pu_spawned = False
oneTimeLaserFlag = False
laser_msg_active = False
laser_cooldown = 0
laser_pu_fallSpeed_y = 4
laser_pu_x = 0
laser_pu_y = 0
laser_x_left = 0
laser_x_right = 0
laser_y = 0
laser_spawn_y = 0

# All yellow bricks
bricks_x_yellow = [SCREEN_WIDTH - 252, SCREEN_WIDTH - 252 + BRICK_WIDTH, SCREEN_WIDTH - 252, 
                   SCREEN_WIDTH - 252 + BRICK_WIDTH, SCREEN_WIDTH - 252, SCREEN_WIDTH - 252 + BRICK_WIDTH, 
                   SCREEN_WIDTH - 252, SCREEN_WIDTH - 252 + BRICK_WIDTH]

bricks_y_yellow = [130, 130, 130 - BRICK_HEIGHT, 130 - BRICK_HEIGHT, 130 - BRICK_HEIGHT * 2, 130 - BRICK_HEIGHT * 2, 
                   130 - BRICK_HEIGHT * 3, 130 - BRICK_HEIGHT * 3]

bricks_x_yellow2 = [SCREEN_WIDTH / 2 - BRICK_WIDTH, SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, 
                    SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5 + 15, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2 - 15]

bricks_y_yellow2 = [SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 136, 
                    SCREEN_HEIGHT / 2 + 56, SCREEN_HEIGHT / 2 + 56]

bricks_x_yellow3 = [360, SCREEN_WIDTH - BRICK_WIDTH - 264]

bricks_y_yellow3 = [370, 172]

# All light blue bricks
bricks_x_blue = [SCREEN_WIDTH - BRICK_WIDTH - 264, SCREEN_WIDTH - BRICK_WIDTH * 2 - 264, 
                 SCREEN_WIDTH - 264, SCREEN_WIDTH - BRICK_WIDTH - 264]

bricks_y_blue = [140, 172, 172, 204]

# All pink bricks
bricks_x_pink = [264, 456, 360, 360]

bricks_y_pink = [370, 370, 338, 402]

# All magenta bricks
bricks_x_magenta = [264, 264, 456, 456, 360, 360, 198, 522]

bricks_y_magenta = [402, 338, 402, 338, 316, 424, 370, 370]

# All dark blue bricks
bricks_x_dBlue = [54, 150, 246, SCREEN_WIDTH / 2 + 100, SCREEN_WIDTH / 2 + 4, SCREEN_WIDTH / 2 + 196, SCREEN_WIDTH / 2 - 320, 
                  SCREEN_WIDTH / 2 - 416, SCREEN_WIDTH / 2 - 512, SCREEN_WIDTH / 2 - 179, SCREEN_WIDTH / 2 - 275, SCREEN_WIDTH / 2 - 83, 
                  SCREEN_WIDTH - 246, SCREEN_WIDTH - 150, SCREEN_WIDTH - 342]

bricks_y_dBlue = [48, 80, 48, SCREEN_HEIGHT - 420, SCREEN_HEIGHT - 452, SCREEN_HEIGHT - 452, SCREEN_HEIGHT / 2, 
                  SCREEN_HEIGHT / 2 + 32, SCREEN_HEIGHT / 2, SCREEN_HEIGHT / 2 - 170, SCREEN_HEIGHT / 2 - 202, SCREEN_HEIGHT / 2 - 202, 
                  SCREEN_HEIGHT - 250, SCREEN_HEIGHT - 282, SCREEN_HEIGHT - 282]

bricks_x_dBlue2 = [SCREEN_WIDTH - BRICK_WIDTH * 2 - 264, SCREEN_WIDTH - BRICK_WIDTH * 2 - 264, 
                   SCREEN_WIDTH - 264, SCREEN_WIDTH - 264, SCREEN_WIDTH - BRICK_WIDTH - 264, 
                   SCREEN_WIDTH - BRICK_WIDTH - 264, SCREEN_WIDTH - BRICK_WIDTH * 3 - 234, 
                   SCREEN_WIDTH + BRICK_WIDTH - 294]

bricks_y_dBlue2 = [140, 204, 140, 204, 118, 226, 172, 172]

# Bald eagle eyes
blobs_x_yGreen = [SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 - EYEBALL_WIDTH, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 + BRICK_WIDTH]
blobs_y_yGreen = [SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200]

# All white bricks
bricks_x_white = [SCREEN_WIDTH / 2 - BRICK_WIDTH - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2,
                  SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 - EYEBALL_WIDTH - BRICK_WIDTH, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2 + EYEBALL_WIDTH,
                  SCREEN_WIDTH / 2 - BRICK_WIDTH, SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH / 2 - EYEBALL_WIDTH - BRICK_WIDTH + 15, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2 + EYEBALL_WIDTH - 15,
                  SCREEN_WIDTH / 2 - BRICK_WIDTH, SCREEN_WIDTH / 2]

bricks_y_white = [SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232,
                  SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 264,
                  SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 104, 
                  SCREEN_HEIGHT / 2 - 104]

# All brown bricks
bricks_x_brown = [SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 2 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - BRICK_WIDTH, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 3 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 + 20, SCREEN_WIDTH / 2 - BRICK_WIDTH * 4 - 20, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - BRICK_WIDTH / 2 + 15, SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 + BRICK_WIDTH / 2 - 15, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 + 20, SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 - 20, SCREEN_WIDTH / 2 + BRICK_WIDTH * 5 - 12, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 6 + 10, SCREEN_WIDTH / 2 + BRICK_WIDTH * 5 - BRICK_WIDTH / 2 + 15, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 6 + BRICK_WIDTH / 2 - 15, SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 4 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 3 - BRICK_WIDTH / 2, 
                  SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH + 10, SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - 10, 
                  SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2]

bricks_y_brown = [SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 136, 
                  SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, 
                  SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 264, 
                  SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, 
                  SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 + 24, SCREEN_HEIGHT / 2 + 24]

# All dark brown bricks
bricks_x_dBrown = [SCREEN_WIDTH / 2 - BRICK_WIDTH * 2, SCREEN_WIDTH / 2 + BRICK_WIDTH, SCREEN_WIDTH / 2 - BRICK_WIDTH - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 2 - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - BRICK_WIDTH / 2 - 20, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 3 - BRICK_WIDTH / 2 + 20, SCREEN_WIDTH / 2 + BRICK_WIDTH * 3 - 15, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 4 + 15, SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - BRICK_WIDTH / 2 - 10, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 + BRICK_WIDTH / 2 + 10, SCREEN_WIDTH / 2 + BRICK_WIDTH * 4 - 5, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 5 + 5, SCREEN_WIDTH / 2 + BRICK_WIDTH * 5 - BRICK_WIDTH / 2, 
                   SCREEN_WIDTH / 2 - BRICK_WIDTH * 6 + BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5, 
                   SCREEN_WIDTH / 2 + BRICK_WIDTH / 2, SCREEN_WIDTH / 2 - BRICK_WIDTH * 1.5, SCREEN_WIDTH / 2 + BRICK_WIDTH / 2]

bricks_y_dBrown = [SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 104, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, SCREEN_HEIGHT / 2 - 72, 
                   SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 - 8, SCREEN_HEIGHT / 2 - 136, SCREEN_HEIGHT / 2 - 136, 
                   SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 168, SCREEN_HEIGHT / 2 - 200, SCREEN_HEIGHT / 2 - 200, 
                   SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 232, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 264, SCREEN_HEIGHT / 2 - 296, 
                   SCREEN_HEIGHT / 2 - 296, SCREEN_HEIGHT / 2 + 24, SCREEN_HEIGHT / 2 - 8, SCREEN_HEIGHT / 2 - 8, SCREEN_HEIGHT / 2 - 40, SCREEN_HEIGHT / 2 - 40]

# Brick HP lists

bricks_yellow2_hp = []
for i in range(len(bricks_x_yellow2)):
  bricks_yellow2_hp.append(2)

# Hearts list
hearts_x = [SCREEN_WIDTH - HEART_WIDTH - 20]
hearts_y = [10]

# Power-up list
powerups_x = []
powerups_y = []

# Lasers list
lasers_x_left = []
lasers_x_right = []
lasers_y_left = []
lasers_y_right = []

#
# init game
#

pygame.init()

normalfont = pygame.font.SysFont('default', 64)    # lettertype binnen de game
dejavuseriffont = pygame.font.SysFont('dejavuseriffont', 36)
fixedsysfont = pygame.font.Font('fonts/fixedsys.ttf', 32) 
terminalfont = pygame.font.Font('fonts/terminal.ttf', 36)
biggerterminalfont = pygame.font.Font('fonts/terminal.ttf', 42)
smallerterminalfont = pygame.font.Font('fonts/terminal.ttf', 28)
orbitronfont = pygame.font.Font('fonts/orbitronmedium.ttf', 32)
ocraextendedfont = pygame.font.Font('fonts/ocraext.ttf', 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()         # Zorgt ervoor dat de 'images' gelezen worden elke 1/30e seconde

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
custombrick_pink = pygame.image.load('customimages/Breakout_Tile_Pink.png').convert()
custombrick_cracked_pink = pygame.image.load('customimages/Breakout_Tile_CrackedPink.png').convert()
custombrick_white = pygame.image.load('customimages/Breakout_Tile_White.png').convert_alpha()
custombrick_cracked_white = pygame.image.load('customimages/Breakout_Tile_CrackedWhite.png').convert()
custombrick_dark_brown = pygame.image.load('customimages/Breakout_Tile_DarkBrown.png').convert()
custombrick_cracked_dark_brown = pygame.image.load('customimages/Breakout_Tile_CrackedDarkBrown.png').convert()
customimg_laser = pygame.image.load('customimages/Breakout_LaserBeam.png').convert_alpha()

level1_bg_image = pygame.image.load('backgrounds/sky.png').convert()
level2_bg_image = pygame.image.load('backgrounds/mountains.jpg').convert()
level3_bg_image = pygame.image.load('backgrounds/meadow.png').convert()

breakout_title_image = pygame.image.load('BREAKOUT1.png').convert_alpha()
breakout_win_image = pygame.image.load('winmessage.png').convert_alpha()
titlescreen_bg_image = pygame.image.load('titlescreen.png').convert()
winscreen_bg_image = pygame.image.load('winscreen.png').convert()

titlescreen_bg_image = pygame.transform.scale(titlescreen_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
winscreen_bg_image = pygame.transform.scale(winscreen_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
level1_bg_image = pygame.transform.scale(level1_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
level2_bg_image = pygame.transform.scale(level2_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
level3_bg_image = pygame.transform.scale(level3_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)          # create empty image of 64 x 64 pixels (SRCALPHA supports transparency)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))       # copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))          # resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)          # create empty image of 243 x 64 pixels (SRCALPHA supports transparency)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))       # copy part (x-left=1158, y-top=396, width=243, height=64) from spritesheet to paddle_img at (0,0)
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))          # resize paddle_img from 243 x 64 pixels to PADDLE_WIDTH x PADDLE_HEIGHT

# Shooting lasers paddle
paddle_img_shooter = pygame.Surface((243, 64), pygame.SRCALPHA)          
paddle_img_shooter.blit(spritesheet, (0, 0), (1158, 660, 243, 64))  
paddle_img_shooter = pygame.transform.scale(paddle_img_shooter, (PADDLE_WIDTH, PADDLE_HEIGHT))

# Lasers
laser_img = pygame.Surface((9, 39), pygame.SRCALPHA)
laser_img.blit(customimg_laser, (0, 0))
laser_img = pygame.transform.scale(laser_img, (LASER_WIDTH, LASER_HEIGHT))

# Yellow brick
brick_img_yellow = pygame.Surface((384, 128), pygame.SRCALPHA)          # create empty image of 384 x 128 pixels (SRCALPHA supports transparency)
brick_img_yellow.blit(spritesheet, (0, 0), (386, 390, 384, 128))       # copy part (x-left=386, y-top=390, width=384, height=128) from spritesheet to brick_img_yellow at (0,0)
brick_img_yellow = pygame.transform.scale(brick_img_yellow, (BRICK_WIDTH, BRICK_HEIGHT))          # resize brick_img_yellow from 384 x 128 pixels to BRICK_WIDTH x BRICK_HEIGHT

# Cracked yellow brick
brick_img_crackedYellow = pygame.Surface((384, 128), pygame.SRCALPHA)  
brick_img_crackedYellow.blit(spritesheet, (0, 0), (386, 260, 384, 128))
brick_img_crackedYellow = pygame.transform.scale(brick_img_crackedYellow, (BRICK_WIDTH, BRICK_HEIGHT))

# Dark blue brick
brick_img_dBlue = pygame.Surface((384, 128), pygame.SRCALPHA)          # create empty image of 384 x 128 pixels (SRCALPHA supports transparency)
brick_img_dBlue.blit(spritesheet, (0, 0), (772, 390, 384, 128))       # copy part (x-left=772, y-top=390, width=384, height=128) from spritesheet to brick_img_dBlue at (0,0)
brick_img_dBlue = pygame.transform.scale(brick_img_dBlue, (BRICK_WIDTH, BRICK_HEIGHT))          # resize brick_img_dBlue from 384 x 128 pixels to BRICK_WIDTH x BRICK_HEIGHT

# Blue brick
brick_img_blue = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_blue.blit(spritesheet, (0, 0), (386, 650, 384, 128))
brick_img_blue = pygame.transform.scale(brick_img_blue, (BRICK_WIDTH, BRICK_HEIGHT))

# Magenta brick
brick_img_magenta = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_magenta.blit(spritesheet, (0, 0), (0, 390, 384, 128))
brick_img_magenta = pygame.transform.scale(brick_img_magenta, (BRICK_WIDTH, BRICK_HEIGHT))

# Heart
heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0,0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

# Grey power-up
blob_img_grey = pygame.Surface((128, 128), pygame.SRCALPHA)
blob_img_grey.blit(spritesheet, (0,0), (1574, 782, 128, 128))
blob_img_grey = pygame.transform.scale(blob_img_grey, (BLOB_WIDTH, BLOB_HEIGHT))

# Green power-up
blob_img_green = pygame.Surface((128, 128), pygame.SRCALPHA)
blob_img_green.blit(spritesheet, (0,0), (1533, 262, 128, 128))
blob_img_green = pygame.transform.scale(blob_img_green, (BLOB_WIDTH, BLOB_HEIGHT))

# Yellow-green blob
blob_img_yGreen = pygame.Surface((128, 128), pygame.SRCALPHA)
blob_img_yGreen.blit(spritesheet, (0,0), (1403, 132, 128, 128))
blob_img_yGreen = pygame.transform.scale(blob_img_yGreen, (EYEBALL_WIDTH, EYEBALL_HEIGHT))

# Brown brick
brick_img_brown = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_brown.blit(spritesheet, (0, 0), (386, 780, 384, 128))
brick_img_brown = pygame.transform.scale(brick_img_brown, (BRICK_WIDTH, BRICK_HEIGHT))  

# White brick
brick_img_white = pygame.Surface((383, 128), pygame.SRCALPHA)
brick_img_white.blit(custombrick_white, (0, 0))
brick_img_white = pygame.transform.scale(brick_img_white, (BRICK_WIDTH, BRICK_HEIGHT))

# Cracked white brick
brick_img_crackedWhite = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_crackedWhite.blit(custombrick_cracked_white, (0, 0))
brick_img_crackedWhite = pygame.transform.scale(brick_img_crackedWhite, (BRICK_WIDTH, BRICK_HEIGHT))

# Pink brick
brick_img_pink = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_pink.blit(custombrick_pink, (0, 0))
brick_img_pink = pygame.transform.scale(brick_img_pink, (BRICK_WIDTH, BRICK_HEIGHT))

# Cracked pink brick
brick_img_crackedPink = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_crackedPink.blit(custombrick_cracked_pink, (0, 0))
brick_img_crackedPink = pygame.transform.scale(brick_img_crackedPink, (BRICK_WIDTH, BRICK_HEIGHT))

# Dark brown brick
brick_img_dBrown = pygame.Surface((383, 127), pygame.SRCALPHA)
brick_img_dBrown.blit(custombrick_dark_brown, (0, 0))
brick_img_dBrown = pygame.transform.scale(brick_img_dBrown, (BRICK_WIDTH, BRICK_HEIGHT))

# Cracked dark brown brick
brick_img_CrackeddBrown = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_CrackeddBrown.blit(custombrick_cracked_dark_brown, (0, 0))
brick_img_CrackeddBrown = pygame.transform.scale(brick_img_CrackeddBrown, (BRICK_WIDTH, BRICK_HEIGHT))


#
# game loop
#

print('mygame is running')
current_level = "start"
running = True
while running:
    #
    # read events
    #
    if current_level == "start":
      for event in pygame.event.get(): 
          if event.type == pygame.QUIT:  
              running = False
      keys = pygame.key.get_pressed()
      
      screen.blit(titlescreen_bg_image, (0, 0)) # Achtergrond

      bo_text_width = breakout_title_image.get_width()
      screen.blit(breakout_title_image, (SCREEN_WIDTH / 2 - bo_text_width / 2, 150))
      
      subtitle = "Hold B to start the game"
      subtitle2 = "Hold Q to resume where you left off (only this session's progress is saved)"
      subtitle3 = "During the game, hold E to return to this homescreen"

      subtitle = terminalfont.render(subtitle, True, "#FFFFFFF0")
      s_text_width = subtitle.get_width()
      screen.blit(subtitle, (SCREEN_WIDTH / 2 - s_text_width / 2, 360))

      subtitle2 = smallerterminalfont.render(subtitle2, True, "#FFFFFFCE")
      s2_text_width = subtitle2.get_width()
      screen.blit(subtitle2, (SCREEN_WIDTH / 2 - s2_text_width / 2, 560))

      subtitle3 = smallerterminalfont.render(subtitle3, True, "#FFFFFFBE")
      s3_text_width = subtitle3.get_width()
      screen.blit(subtitle3, (SCREEN_WIDTH / 2 - s3_text_width / 2, 600))

      # show screen
      pygame.display.flip() 

      # go to next level
      if keys[pygame.K_b]:
        resetGame_levelOne()
        current_level = "one"
        pygame.time.delay(360)

      if keys[pygame.K_q]:
        if checkpoint != checkpoint_progress["c_winscreen"]:
          current_level = checkpoint
        else:
          current_level = "win"

        if checkpoint == "one":
          resetGame_levelOne()
        elif checkpoint == "two":
          resetGame_levelTwo()
          laser_pu_spawned = False
          laser_pu_active = False
          oneTimeLaserFlag = False

        elif checkpoint == "three":
          laser_pu_spawned = False
          laser_pu_active = False
          oneTimeLaserFlag = False

        pygame.time.delay(360)
      
      # Shortcut
      if keys[pygame.K_0] or keys[pygame.K_KP_0]:
        setupGame_levelTwo()
        laser_pu_spawned = False
        laser_pu_active = False
        oneTimeLaserFlag = False
        current_level = "two"
        pygame.time.delay(360)

    # level one
    elif current_level == "one": 
      for event in pygame.event.get(): 
          if event.type == pygame.QUIT:  
              running = False 
      keys = pygame.key.get_pressed()

      checkpoint = checkpoint_progress["c_levelone"]

      if keys[pygame.K_e]:
        current_level = "start"
        pygame.time.delay(360)
      
      #
      # store variables
      #

      previous_ball_y = ball_y
      previous_ball_x = ball_x

      level_status_msg = "Level One: "
      difficulty_status_msg = "Cloud Nine"

      # 
      # move everything
      #

      # move ball
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y

      # bounce ball
      if ball_x <= 0 :                            # Linkerkant scherm
        ball_speed_x = abs(ball_speed_x)
      if ball_x + BALL_WIDTH > SCREEN_WIDTH:      # Rechterkant scherm (botsen)
        ball_speed_x = abs(ball_speed_x) * -1

      if ball_y <= 0 :                            # Bovenkant scherm
        ball_speed_y = abs(ball_speed_y)
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:      # Onderkant scherm (botsen)
        ball_speed_y = abs(ball_speed_y) * -1

      # move paddle
      if ball_speed_x != 0 or ball_speed_y != 0 or game_status_msg == "Hold C to shoot":
        if keys[pygame.K_d]: # als D-toets ingedrukt is
          paddle_x += 12
        if keys[pygame.K_a]: # als A-toets ingedrukt is
          paddle_x -= 12
        if keys[pygame.K_LEFT]: # als <-toets ingedrukt is
          paddle_x -= 12
        if keys[pygame.K_RIGHT]: # als >-toets ingedrukt is
          paddle_x += 12

      # stop paddle at edges of screen
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:          # Rechterkant scherm
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

      if paddle_x < 0:          # Linkerkant scherm
        paddle_x = 0

      # 
      # handle collisions
      #

      # Ball-paddle collisions

      # Stuiteren bovenkant plank
      if (ball_x + BALL_WIDTH > paddle_x and 
          ball_x < paddle_x + PADDLE_WIDTH and 
          ball_y + BALL_HEIGHT >= paddle_y and
          previous_ball_y + BALL_HEIGHT <= paddle_y and 
          ball_speed_y > 0):          # Laat het alleen stuiteren wanneer de bal naar beneden gaat, zo gaat de bal niet door de paddle heen
        ball_y = paddle_y - BALL_HEIGHT         # Bal kan nooit in de paddle komen
        angledBouncingBall_levelOne()

      # Stuiteren linkerkant plank
      elif (ball_y + BALL_HEIGHT > paddle_y and 
          ball_y < paddle_y + PADDLE_HEIGHT and 
          ball_x + BALL_WIDTH >= paddle_x and 
          ball_x + BALL_WIDTH <= paddle_x + 12 and 
          ball_speed_x > 0):
        if ball_y + BALL_HEIGHT >= paddle_y and ball_y <= paddle_y + PADDLE_HEIGHT: # Voorkomt merendeels dat de bal door de plank gaat aan de zijkanten
          ball_x = paddle_x - BALL_WIDTH
          ball_speed_x = abs(ball_speed_x) * -1

      # Stuiteren rechterkant plank
      elif (ball_y + BALL_HEIGHT > paddle_y and 
          ball_y < paddle_y + PADDLE_HEIGHT and 
          ball_x >= paddle_x + PADDLE_WIDTH - 12 and 
          ball_x <= paddle_x + PADDLE_WIDTH and 
          ball_speed_x < 0):
        if ball_y + BALL_HEIGHT >= paddle_y and ball_y <= paddle_y + PADDLE_HEIGHT:     # Voorkomt merendeels dat de bal door de plank gaat aan de zijkanten
          ball_x = paddle_x + PADDLE_WIDTH
          ball_speed_x = abs(ball_speed_x)

      # Ball-brick collisions
      
      # All yellow bricks
      for i in range(len(bricks_x_yellow) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x_yellow[i] and 
            ball_x < bricks_x_yellow[i] + BRICK_WIDTH and 
            ball_y <= bricks_y_yellow[i] + BRICK_HEIGHT and 
            ball_y + BALL_HEIGHT >= bricks_y_yellow[i]):
        
          if ball_speed_y > 0 and ball_y  <= bricks_y_yellow[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y_yellow[i] + BRICK_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= bricks_x_yellow[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= bricks_x_yellow[i] + BRICK_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          bricks_x_yellow.pop(i)   
          bricks_y_yellow.pop(i)
          
          # Hearts/HP
          if not heart_active and random.randint(1, 18) == 1: # Als heart_active = True (want het is vastgesteld als False) en de kans van 5.56% dat een hartje 'spawned' aan wordt voldoen, dan 'spawned' een hartje
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH) # Geeft een willekeurige positie voor heart_x tussen de twee parameters
            heart_y = random.randint(200, SCREEN_HEIGHT - 380) # Geeft een willekeurige positie voor heart_y tussen de twee parameters
            heart_active = True

          break    

      # All dark blue bricks
      for i in range(len(bricks_x_dBlue) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x_dBlue[i] and 
          ball_x < bricks_x_dBlue[i] + BRICK_WIDTH and 
          ball_y <= bricks_y_dBlue[i] + BRICK_HEIGHT and 
          ball_y + BALL_HEIGHT >= bricks_y_dBlue[i]):
        
          if ball_speed_y > 0 and ball_y  <= bricks_y_dBlue[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y_dBlue[i] + BRICK_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= bricks_x_dBlue[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= bricks_x_dBlue[i] + BRICK_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          bricks_x_dBlue.pop(i)   
          bricks_y_dBlue.pop(i)        
          
          # Hearts/HP
          if not heart_active and random.randint(1, 18) == 1: # Als heart_active = True (want het is vastgesteld als False) en de kans van 5.56% dat een hartje 'spawned' aan wordt voldoen, dan 'spawned' een hartje
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH) # Geeft een willekeurige positie voor heart_x tussen de twee parameters
            heart_y = random.randint(200, SCREEN_HEIGHT - 380) # Geeft een willekeurige positie voor heart_y tussen de twee parameters
            heart_active = True
          
          break

      # Sniper power-up
      if not sniper_pu_active and not sniper_pu_spawned and len(bricks_x_yellow) + len(bricks_x_dBlue) == 3:
        sniper_pu_y = paddle_y + PADDLE_HEIGHT / 2 - BLOB_HEIGHT / 2  # spawns it on the horizontal line of the paddle
        
        while True: # checks if the spawned power-up blob overlaps with the paddle
          sniper_pu_x = random.randint(50, SCREEN_WIDTH - 50 - BLOB_WIDTH)  # spawns it in a random place between given parameters
          if not (sniper_pu_x + BLOB_WIDTH > paddle_x and sniper_pu_x < paddle_x + PADDLE_WIDTH):
              break
        
        sniper_pu_spawned = True
        sniper_pu_startTime = pygame.time.get_ticks()

      if ballFrozen and sniper_pu_active:
          ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
          ball_y = paddle_y - BALL_HEIGHT - 5

      if debugFlag: # soms wordt ball_speed_x toch nog positief, doordat er een ball-brick collision gebeurt terwijl je de power-up int. dit zorgt ervoor dat dat niet gebeurt
        ball_speed_x = 0
        ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
        ball_y = paddle_y - BALL_HEIGHT - 5

      if keys[pygame.K_c] and ballFrozen:
        ball_speed_y = -8
        ballFrozen = False
        debugFlag = False
        
        game_status_msg = ""
      
      currentBrickCount = len(bricks_x_yellow) + len(bricks_x_dBlue)

      if sniper_pu_active and currentBrickCount < previousBrickCount:      # when the ball is shot, checks if the mode is still active. then once 1 (or more) brick(s) breaks (/ break), the ball shoots in a random direction (left or right)
        powerups_x.pop(0)
        powerups_y.pop(0)
        ball_speed_x = random.choice([8, -8])

        sniper_pu_active = False
      
      previousBrickCount = currentBrickCount

      # Checkt wanneer je af bent
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT and len(hearts_x) <= 1:
        ball_speed_y = 0
        ball_speed_x = 0
        hearts_x.clear() # Een hart (alle harten) wordt (worden) verwijderd
        hearts_y.clear()
        
        game_status_msg = "You lost! Hold R to restart"

        # Game restart wanneer er op R gedrukt wordt
        if keys[pygame.K_r]:
          resetGame_levelOne()

      
      elif ball_y + BALL_HEIGHT > SCREEN_HEIGHT and len(hearts_x) > 1:        
        ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
        ball_y = paddle_y - BALL_HEIGHT - 30
        
        ball_speed_x = 0
        ball_speed_y = 0

        ballFrozen = True # Voorkomt dat de game vastloopt wanneer het hartje de plank en de bal de onderkant tegelijkertijd raken
 
        hearts_x.pop(0) # Een hart wordt verwijderd
        hearts_y.pop(0)
        hearts_x.sort()
        hearts_y.sort()
        
        game_status_msg = "Hold M to resume"
        
      if keys[pygame.K_m] and ballFrozen:
        ball_speed_x = 8
        ball_speed_y = 8

        ballFrozen = False # Zie boven ^

        game_status_msg = ""

      # Checkt of alle blokken weg zijn
      if len(bricks_x_yellow) == 0 and len(bricks_x_dBlue) == 0:
        ball_speed_y = 0
        ball_speed_x = 0
        game_status_msg = "You win! Hold O to continue"

      # 
      # draw everything
      #

      # clear screen 
      screen.blit(level1_bg_image, (0, 0))          # Achtergrond 

      # draw ball
      screen.blit(ball_img, (ball_x, ball_y))

      # draw paddle
      screen.blit(paddle_img, (paddle_x, paddle_y))

      # draw bricks
      
      # draw yellow bricks
      for i in range(0, len(bricks_x_yellow)):
          screen.blit(brick_img_yellow, (bricks_x_yellow[i], bricks_y_yellow[i]))

      # draw dark blue bricks
      for i in range(0, len(bricks_x_dBlue)):
        screen.blit(brick_img_dBlue, (bricks_x_dBlue[i], bricks_y_dBlue[i]))

      # draw hearts
      if heart_active:
        screen.blit(heart_img, (heart_x, heart_y))
        previous_heart_y = heart_y
        heart_y = heart_y + heart_speed_y

        if (heart_x + HEART_WIDTH > paddle_x and 
          heart_x < paddle_x + PADDLE_WIDTH and 
          heart_y + HEART_HEIGHT >= paddle_y and
          previous_heart_y + HEART_HEIGHT <= paddle_y):
          
          hearts_x.append(SCREEN_WIDTH - HEART_WIDTH - 20)
          hearts_y.append(10)
          
          heart_active = False
          
        elif heart_y + HEART_HEIGHT > SCREEN_HEIGHT:
          heart_active = False
        
      for i in range(0, len(hearts_x)):
        screen.blit(heart_img, (hearts_x[i] - (HEART_WIDTH + 5) * i, hearts_y[i]))
        
      if len(hearts_x) > 5:
        hearts_x.pop(5)
        hearts_y.pop(5)

      # draw sniper power-up block
      if sniper_pu_spawned:
        screen.blit(blob_img_grey, (sniper_pu_x, sniper_pu_y))

        # collision paddle and power-up block
        if (sniper_pu_x + BLOB_WIDTH >= paddle_x and 
          sniper_pu_x <= paddle_x + PADDLE_WIDTH):
          
          sniper_pu_active = True
          sniper_msg_active = True
          sniper_activeTime = pygame.time.get_ticks()

          ball_speed_x = 0
          ball_speed_y = 0
          ballFrozen = True
          debugFlag = True

          game_status_msg = "Hold C to shoot"
          
          powerups_x.append(SCREEN_WIDTH - BLOB_WIDTH - 20)
          powerups_y.append(SCREEN_HEIGHT - BLOB_HEIGHT - 10)
            
          sniper_pu_spawned = False
        
        currentTime = pygame.time.get_ticks()
        if currentTime - sniper_pu_startTime > 7000: # power-up disappears after 7 seconds (in other words, you have 7 seconds to obtain it)
          sniper_pu_spawned = False

      if sniper_pu_active:  # power-up active
        
        # power-up active message pops up
        powerup_status_msg = "[SNIPER MODE] Move your paddle to aim"
        powerup_status_img = ocraextendedfont.render(powerup_status_msg, True, '#59727E')
        psi_text_width = powerup_status_img.get_width()
        gsi_text_height = game_status_img.get_height()

        if sniper_msg_active:
          currentTime = pygame.time.get_ticks()
          if currentTime - sniper_activeTime < 2500:  # the active message lasts for 2.5 seconds
            screen.blit(powerup_status_img, (SCREEN_WIDTH / 2 - psi_text_width / 2, 46 + gsi_text_height))
          else:
            sniper_msg_active = False                   # then disappears

      # draw equipped power-up
      for i in range(0, len(powerups_x)):
        screen.blit(blob_img_grey, (powerups_x[i] - (BLOB_WIDTH + 5) * i, powerups_y[i]))

      # draw status message
      game_status_img = normalfont.render(game_status_msg, True, '#FFFFFF')
      gsi_text_width = game_status_img.get_width()
      screen.blit(game_status_img, (SCREEN_WIDTH / 2 - gsi_text_width / 2, 46))

      speed_status_img = fixedsysfont.render(speed_status_msg, True, "#4D9CBE")
      ssi_text_height = speed_status_img.get_height()
      screen.blit(speed_status_img, (20, SCREEN_HEIGHT - ssi_text_height - 10))

      level_status_img = fixedsysfont.render(level_status_msg, True, "#317da0")
      lsi_text_width = level_status_img.get_width()
      screen.blit(level_status_img, (20, 10))

      difficulty_status_img = dejavuseriffont.render(difficulty_status_msg, True, "#AEFFC5")
      screen.blit(difficulty_status_img, (15 + lsi_text_width, 16))

      # show screen
      pygame.display.flip() 

      # go to next level
      if keys[pygame.K_o]:
        current_level = "two"
              
        setupGame_levelTwo()
        laser_pu_spawned = False
        laser_pu_active = False
        oneTimeLaserFlag = False

        pygame.time.delay(360)

    # level two
    elif current_level == "two":
      for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
          running = False 
      keys = pygame.key.get_pressed()

      checkpoint = checkpoint_progress["c_leveltwo"]
      
      if keys[pygame.K_e]:
        current_level = "start"
        pygame.time.delay(360)

      #
      # store variables
      #
      
      previous_ball_y = ball_y
      previous_ball_x = ball_x
      
      level_status_msg = "Level Two: "
      difficulty_status_msg = "Summit"

      # 
      # move everything
      #

      # move ball
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y

      # bounce ball
      if ball_x <= 0 :                            # Linkerkant scherm
        ball_speed_x = abs(ball_speed_x)
      if ball_x + BALL_WIDTH > SCREEN_WIDTH:      # Rechterkant scherm (botsen)
        ball_speed_x = abs(ball_speed_x) * -1

      if ball_y <= 0 :                            # Bovenkant scherm
        ball_speed_y = abs(ball_speed_y)
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:      # Onderkant scherm (botsen)
        ball_speed_y = abs(ball_speed_y) * -1

      # move paddle
      if ball_speed_x != 0 or ball_speed_y != 0 or laser_pu_active or sniper_pu_active:
        if keys[pygame.K_d]: # als D-toets ingedrukt is
          paddle_x += 14
        if keys[pygame.K_a]: # als A-toets ingedrukt is
          paddle_x -= 14
        if keys[pygame.K_LEFT]: # als <-toets ingedrukt is
          paddle_x -= 14
        if keys[pygame.K_RIGHT]: # als >-toets ingedrukt is
          paddle_x += 14

      # stop paddle at edges of screen
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:          # Rechterkant scherm
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

      if paddle_x < 0:          # Linkerkant scherm
        paddle_x = 0

      # 
      # handle collisions
      #

      # Ball-paddle collisions

      # Stuiteren bovenkant plank
      if (ball_x + BALL_WIDTH > paddle_x and 
          ball_x < paddle_x + PADDLE_WIDTH and 
          ball_y + BALL_HEIGHT >= paddle_y and
          previous_ball_y + BALL_HEIGHT <= paddle_y and 
          ball_speed_y > 0):          # Laat het alleen stuiteren wanneer de bal naar beneden gaat, zo gaat de bal niet door de paddle heen
        ball_y = paddle_y - BALL_HEIGHT         # Bal kan nooit in de paddle komen
        angledBouncingBall_levelTwo()

      # Stuiteren linkerkant plank
      elif (ball_y + BALL_HEIGHT > paddle_y and 
          ball_y < paddle_y + PADDLE_HEIGHT and 
          ball_x + BALL_WIDTH >= paddle_x and 
          ball_x + BALL_WIDTH <= paddle_x + 10 and 
          ball_speed_x > 0):
        if ball_y + BALL_HEIGHT >= paddle_y and ball_y <= paddle_y + PADDLE_HEIGHT: # Voorkomt merendeels dat de bal door de plank gaat aan de zijkanten
          ball_x = paddle_x - BALL_WIDTH
          ball_speed_x = abs(ball_speed_x) * -1

      # Stuiteren rechterkant plank
      elif (ball_y + BALL_HEIGHT > paddle_y and 
          ball_y < paddle_y + PADDLE_HEIGHT and 
          ball_x >= paddle_x + PADDLE_WIDTH - 10 and 
          ball_x <= paddle_x + PADDLE_WIDTH and 
          ball_speed_x < 0):
        if ball_y + BALL_HEIGHT >= paddle_y and ball_y <= paddle_y + PADDLE_HEIGHT:     # Voorkomt merendeels dat de bal door de plank gaat aan de zijkanten
          ball_x = paddle_x + PADDLE_WIDTH
          ball_speed_x = abs(ball_speed_x)

      # Ball-brick collisions
      
      # All yellow bricks
      for i in range(len(bricks_x_yellow2) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x_yellow2[i] and 
            ball_x < bricks_x_yellow2[i] + BRICK_WIDTH and 
            ball_y <= bricks_y_yellow2[i] + BRICK_HEIGHT and 
            ball_y + BALL_HEIGHT >= bricks_y_yellow2[i]):
        
          if ball_speed_y > 0 and ball_y <= bricks_y_yellow2[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y_yellow2[i] + BRICK_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= bricks_x_yellow2[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= bricks_x_yellow2[i] + BRICK_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          bricks_yellow2_hp[i] -= 1
          brick_got_hit = True
          
          if bricks_yellow2_hp[i] <= 0:
            bricks_x_yellow2.pop(i)   
            bricks_y_yellow2.pop(i)
            bricks_yellow2_hp.pop(i)
            brick_got_hit = True

          checksIfSniperPU_shouldSpawn()
          
          # Hearts/HP
          if not heart_active and random.randint(1, 35) == 1:
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
            heart_y = random.randint(200, SCREEN_HEIGHT - 380)
            heart_active = True

          break
      
      # Eagle eyes
      for i in range(len(blobs_x_yGreen) - 1, -1, -1):
        if (ball_x + BLOB_WIDTH > blobs_x_yGreen[i] and 
            ball_x < blobs_x_yGreen[i] + BLOB_WIDTH and 
            ball_y <= blobs_y_yGreen[i] + BLOB_HEIGHT and 
            ball_y + BALL_HEIGHT >= blobs_y_yGreen[i]):
        
          if ball_speed_y > 0 and ball_y <= blobs_y_yGreen[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= blobs_y_yGreen[i] + BLOB_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= blobs_x_yGreen[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= blobs_x_yGreen[i] + BLOB_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          blobs_x_yGreen.pop(i)   
          blobs_y_yGreen.pop(i)
          
          checksIfSniperPU_shouldSpawn()

          # Hearts/HP
          if not heart_active and random.randint(1, 35) == 1:
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
            heart_y = random.randint(200, SCREEN_HEIGHT - 380)
            heart_active = True

          break

      # All white bricks
      for i in range(len(bricks_x_white) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x_white[i] and 
            ball_x < bricks_x_white[i] + BRICK_WIDTH and 
            ball_y <= bricks_y_white[i] + BRICK_HEIGHT and 
            ball_y + BALL_HEIGHT >= bricks_y_white[i]):
        
          if ball_speed_y > 0 and ball_y <= bricks_y_white[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y_white[i] + BRICK_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= bricks_x_white[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= bricks_x_white[i] + BRICK_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          bricks_x_white.pop(i)   
          bricks_y_white.pop(i)

          checksIfSniperPU_shouldSpawn()
          
          # Hearts/HP
          if not heart_active and random.randint(1, 35) == 1:
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
            heart_y = random.randint(200, SCREEN_HEIGHT - 380)
            heart_active = True

          break
      
      # All brown bricks
      for i in range(len(bricks_x_brown) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x_brown[i] and 
          ball_x < bricks_x_brown[i] + BRICK_WIDTH and 
          ball_y <= bricks_y_brown[i] + BRICK_HEIGHT and 
          ball_y + BALL_HEIGHT >= bricks_y_brown[i]):
        
          if ball_speed_y > 0 and ball_y <= bricks_y_brown[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y_brown[i] + BRICK_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= bricks_x_brown[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= bricks_x_brown[i] + BRICK_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          bricks_x_brown.pop(i)   
          bricks_y_brown.pop(i)

          checksIfSniperPU_shouldSpawn()        
          
          # Hearts/HP
          if not heart_active and random.randint(1, 35) == 1:
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
            heart_y = random.randint(200, SCREEN_HEIGHT - 380)
            heart_active = True
          
          break    

      # All dark brown bricks
      for i in range(len(bricks_x_dBrown) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x_dBrown[i] and 
          ball_x < bricks_x_dBrown[i] + BRICK_WIDTH and 
          ball_y <= bricks_y_dBrown[i] + BRICK_HEIGHT and 
          ball_y + BALL_HEIGHT >= bricks_y_dBrown[i]):
        
          if ball_speed_y > 0 and ball_y <= bricks_y_dBrown[i]:     # Stuiteren bovenkant blok
            ball_speed_y = abs(ball_speed_y) * -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y_dBrown[i] + BRICK_HEIGHT:     # Stuiteren onderkant blok
            ball_speed_y = abs(ball_speed_y) * 1
        
          elif ball_speed_x > 0 and ball_x <= bricks_x_dBrown[i]:     # Stuiteren linkerkant blok
            ball_speed_x = abs(ball_speed_x) * -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= bricks_x_dBrown[i] + BRICK_WIDTH:     # Stuiteren rechterkant blok
            ball_speed_x = abs(ball_speed_x) * 1

          bricks_x_dBrown.pop(i)   
          bricks_y_dBrown.pop(i)

          checksIfSniperPU_shouldSpawn()        
          
          # Hearts/HP
          if not heart_active and random.randint(1, 35) == 1:
            heart_x = random.randint(100, SCREEN_WIDTH - 100 - HEART_WIDTH)
            heart_y = random.randint(200, SCREEN_HEIGHT - 380)
            heart_active = True
          
          break
      
      # Lasers power-up
      now = pygame.time.get_ticks()

      if not oneTimeLaserFlag and now - startTime >= 20000: # na 20 seconden na het starten van level 2 wordt de laser power-up 'gedropped'
        laser_pu_x = random.randint(120, SCREEN_WIDTH - 120 - BLOB_WIDTH)
        laser_pu_y = random.randint(100, SCREEN_HEIGHT - 480)
        laser_pu_spawned = True
        oneTimeLaserFlag = True

      # Sniper power-up
      if ballFrozen and sniper_pu_active:
          ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
          ball_y = paddle_y - BALL_HEIGHT - 5

      if debugFlag: # soms wordt ball_speed_x toch nog positief, doordat er een ball-brick collision gebeurt terwijl je de power-up int. dit zorgt ervoor dat dat niet gebeurt
        ball_speed_x = 0
        ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
        ball_y = paddle_y - BALL_HEIGHT - 5

      if keys[pygame.K_c] and ballFrozen: # dit zou je dus kunnen activeren wanneer het 'Hold M to resume' zegt, maar had geen tijd meer om het te fixen
        ball_speed_y = -8
        ballFrozen = False
        debugFlag = False
        
        game_status_msg = ""
      
      currentBrickCount = len(bricks_x_yellow2) + len(bricks_x_dBrown) + len(bricks_x_white) + len(bricks_x_brown) + len(blobs_x_yGreen)

      if sniper_pu_active and (currentBrickCount < previousBrickCount or brick_got_hit):      # when the ball is shot, checks if the mode is still active. then once 1 (or more) brick(s) breaks (/ break), the ball shoots in a random direction (left or right)
        powerups_x.pop(0)
        powerups_y.pop(0)
        ball_speed_x = random.choice([8, -8])

        sniper_pu_active = False
        brick_got_hit = False
      
      previousBrickCount = currentBrickCount

      # Checkt wanneer je af bent
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT and len(hearts_x) <= 1:
        ball_speed_y = 0
        ball_speed_x = 0
        hearts_x.clear() # Een hart (alle harten) wordt (worden) verwijderd
        hearts_y.clear()
        
        game_status_msg = "You lost! Hold R to restart"

        # Game restart wanneer er op R gedrukt wordt
        if keys[pygame.K_r]:
          resetGame_levelTwo()
          laser_pu_active = False
          laser_pu_spawned = False
          oneTimeLaserFlag = False

      elif ball_y + BALL_HEIGHT > SCREEN_HEIGHT and len(hearts_x) > 1:        
        ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
        ball_y = paddle_y - BALL_HEIGHT - 30
        
        ball_speed_x = 0
        ball_speed_y = 0

        ballFrozen = True # Voorkomt dat de game vastloopt wanneer het hartje de plank en de bal de onderkant tegelijkertijd raken
 
        hearts_x.pop(0) # Een hart wordt verwijderd
        hearts_y.pop(0)
        hearts_x.sort()
        hearts_y.sort()
        
        game_status_msg = "Hold M to resume"
        
      if keys[pygame.K_m] and ballFrozen:
        ball_speed_x = 8
        ball_speed_y = 8

        ballFrozen = False # Zie boven ^

        game_status_msg = ""

      # Checkt of alle blokken weg zijn
      if len(bricks_x_yellow2) == 0 and len(bricks_x_dBrown) == 0 and len(bricks_x_brown) == 0 and len(bricks_x_white) == 0 and len(blobs_x_yGreen) == 0:
        ball_speed_y = 0
        ball_speed_x = 0
        game_status_msg = "You win! Hold P to continue"

      # 
      # draw everything
      #

      # clear screen 
      screen.blit(level2_bg_image, (0, 0))          # Achtergrond 

      # draw ball
      screen.blit(ball_img, (ball_x, ball_y))

      # draw bricks

      # draw brown bricks
      for i in range(0, len(bricks_x_brown)):
        screen.blit(brick_img_brown, (bricks_x_brown[i], bricks_y_brown[i]))

      # draw dark brown bricks
      for i in range(0, len(bricks_x_dBrown)):
        screen.blit(brick_img_dBrown, (bricks_x_dBrown[i], bricks_y_dBrown[i]))

      # draw white bricks
      for i in range(0, len(bricks_x_white)):
        screen.blit(brick_img_white, (bricks_x_white[i], bricks_y_white[i]))

      # draw yellow bricks
      for i in range(0, len(bricks_x_yellow2)):
          if bricks_yellow2_hp[i] == 2:
            screen.blit(brick_img_yellow, (bricks_x_yellow2[i], bricks_y_yellow2[i]))
          elif bricks_yellow2_hp[i] == 1:
            screen.blit(brick_img_crackedYellow, (bricks_x_yellow2[i], bricks_y_yellow2[i]))

      # draw eyes
      for i in range(0, len(blobs_x_yGreen)):
        screen.blit(blob_img_yGreen, (blobs_x_yGreen[i], blobs_y_yGreen[i]))

      # draw hearts
      if heart_active:
        screen.blit(heart_img, (heart_x, heart_y))
        previous_heart_y = heart_y
        heart_y = heart_y + heart_speed_y

        if (heart_x + HEART_WIDTH > paddle_x and 
          heart_x < paddle_x + PADDLE_WIDTH and 
          heart_y + HEART_HEIGHT >= paddle_y and
          previous_heart_y + HEART_HEIGHT <= paddle_y):
          
          hearts_x.append(SCREEN_WIDTH - HEART_WIDTH - 20)
          hearts_y.append(10)
          
          heart_active = False
          
        elif heart_y + HEART_HEIGHT > SCREEN_HEIGHT:
          heart_active = False
        
      for i in range(0, len(hearts_x)):
        screen.blit(heart_img, (hearts_x[i] - (HEART_WIDTH + 5) * i, hearts_y[i]))
        
      if len(hearts_x) > 5:
        hearts_x.pop(5)
        hearts_y.pop(5)
              
      # draw laser power-up block
      if laser_pu_spawned:
        screen.blit(blob_img_green, (laser_pu_x, laser_pu_y))
        previous_laser_pu_y = laser_pu_y
        laser_pu_y = laser_pu_y + laser_pu_fallSpeed_y

        # collision paddle and power-up block
        if (laser_pu_x + BLOB_WIDTH > paddle_x and 
          laser_pu_x < paddle_x + PADDLE_WIDTH and 
          laser_pu_y + BLOB_HEIGHT >= paddle_y and
          previous_laser_pu_y + BLOB_HEIGHT <= paddle_y):

          laser_pu_active = True
          laser_activeTime = pygame.time.get_ticks()
          laser_pu_startTime = pygame.time.get_ticks()
          laser_msg_active = True

          game_status_msg = "You have 7 seconds"
          
          powerups_x.append(SCREEN_WIDTH - BLOB_WIDTH - 20)
          powerups_y.append(SCREEN_HEIGHT - BLOB_HEIGHT - 10)
            
          laser_pu_spawned = False

        elif laser_pu_y + BLOB_HEIGHT > SCREEN_HEIGHT:
          laser_pu_spawned = False

      if laser_pu_active:  # power-up active
        currentTime = pygame.time.get_ticks()

        # power-up active message pops up
        powerup_status_msg = "[LASER MODE] Move your paddle to aim"
        powerup_status_img = orbitronfont.render(powerup_status_msg, True, '#2A8558')
        psi_text_width = powerup_status_img.get_width()
        gsi_text_height = game_status_img.get_height()
        
        if laser_msg_active and currentTime - laser_activeTime < 2500:  # the active message lasts for 2.5 seconds
            screen.blit(powerup_status_img, (SCREEN_WIDTH / 2 - psi_text_width / 2, 46 + gsi_text_height))
        else:
          laser_msg_active = False                   # then disappears
          game_status_msg = ""

        # timed laser power-up
        if currentTime - laser_pu_startTime >= 7000 or (ball_y + BALL_HEIGHT > SCREEN_HEIGHT and len(hearts_x) <= 1):
          laser_pu_active = False
          print('power-up de-activated')
        
        else:
          if laser_cooldown > 0:
            laser_cooldown -= 1

          if laser_cooldown == 0:
            laser_x_left = paddle_x + 3
            laser_x_right = paddle_x + PADDLE_WIDTH - LASER_WIDTH - 3
            laser_spawn_y = paddle_y + 15

            lasers_x_left.append(laser_x_left)
            lasers_x_right.append(laser_x_right)
            lasers_y_left.append(laser_spawn_y)
            lasers_y_right.append(laser_spawn_y)

            laser_cooldown = LASER_COOLDOWN_TIME

          # move lasers
          for i in range(len(lasers_y_left)):
            lasers_y_left[i] += LASER_SPEED_Y

          for i in range(len(lasers_y_right)):
            lasers_y_right[i] += LASER_SPEED_Y

          # check if they are off-screen or not
          for i in range(len(lasers_y_left) - 1, -1, -1):
            if lasers_y_left[i] < 0:      # 1 lijst is genoeg, ze bewegen in paren, dus y is gelijk
              lasers_x_left.pop(i)
              lasers_y_left.pop(i)
              lasers_x_right.pop(i)
              lasers_y_right.pop(i)

          # draw lasers
          for i in range(len(lasers_x_left)):
            print('lasers shooting')
            screen.blit(laser_img, (lasers_x_left[i], lasers_y_left[i]))
            
          for i in range(len(lasers_x_right)):
            print('lasers 2 shooting')
            screen.blit(laser_img, (lasers_x_right[i], lasers_y_right[i]))
        
          laserBrickCollisions_levelTwo()
        
      # draw paddle
      if laser_pu_active:
        screen.blit(paddle_img_shooter, (paddle_x, paddle_y))
        print('paddle changed')

      else:
        screen.blit(paddle_img, (paddle_x, paddle_y))
      
      # draw sniper power-up block
      if sniper_pu_spawned:
        screen.blit(blob_img_grey, (sniper_pu_x, sniper_pu_y))

        # collision paddle and power-up block
        if (sniper_pu_x + BLOB_WIDTH >= paddle_x and 
          sniper_pu_x <= paddle_x + PADDLE_WIDTH):
          
          sniper_pu_active = True
          sniper_msg_active = True
          sniper_activeTime = pygame.time.get_ticks()

          ball_speed_x = 0
          ball_speed_y = 0
          ballFrozen = True
          debugFlag = True

          game_status_msg = "Hold C to shoot"
      
          powerups_x.append(SCREEN_WIDTH - BLOB_WIDTH - 20)
          powerups_y.append(SCREEN_HEIGHT - BLOB_HEIGHT - 10)
          
          sniper_pu_spawned = False
        
        currentTime = pygame.time.get_ticks()
        if currentTime - sniper_pu_startTime > 7000: # power-up disappears after 7 seconds (in other words, you have 7 seconds to obtain it)
          sniper_pu_spawned = False

      if sniper_pu_active:  # power-up active
        
        # power-up active message pops up
        powerup_status_msg = "[SNIPER MODE] Move your paddle to aim"
        powerup_status_img = ocraextendedfont.render(powerup_status_msg, True, '#59727E')
        psi_text_width = powerup_status_img.get_width()
        gsi_text_height = game_status_img.get_height()

        if sniper_msg_active:
          currentTime = pygame.time.get_ticks()
          if currentTime - sniper_activeTime < 2500:  # the active message lasts for 2.5 seconds
            screen.blit(powerup_status_img, (SCREEN_WIDTH / 2 - psi_text_width / 2, 46 + gsi_text_height))
          else:
            sniper_msg_active = False                   # then disappears

      # draw equipped sniper power-up
      if sniper_pu_active:
        screen.blit(blob_img_grey, (powerup_x, powerup_y))

      # draw equipped laser power-up
      if laser_pu_active:
        print('activation blitted')
        screen.blit(blob_img_green, (powerup_x - (BLOB_WIDTH + 5), powerup_y))

      # draw status message
      game_status_img = normalfont.render(game_status_msg, True, '#FFFFFF')
      gsi_text_width = game_status_img.get_width()
      screen.blit(game_status_img, (SCREEN_WIDTH / 2 - gsi_text_width / 2, 46))

      speed_status_img = fixedsysfont.render(speed_status_msg, True, "#345B6C")
      ssi_text_height = speed_status_img.get_height()
      screen.blit(speed_status_img, (20, SCREEN_HEIGHT - ssi_text_height - 10))

      level_status_img = fixedsysfont.render(level_status_msg, True, "#5399b7")
      lsi_text_width = level_status_img.get_width()
      screen.blit(level_status_img, (20, 10))

      difficulty_status_img = dejavuseriffont.render(difficulty_status_msg, True, "#FFFAA5")
      screen.blit(difficulty_status_img, (15 + lsi_text_width, 16))

      # show screen
      pygame.display.flip()

      # go to next level
      if keys[pygame.K_p]:
        current_level = "three"
              
        setupGame_levelThree()

        pygame.time.delay(360)

    # level three
    elif current_level == "three":
      for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
          running = False 
      keys = pygame.key.get_pressed()

      checkpoint = checkpoint_progress["c_levelthree"]
      
      if keys[pygame.K_e]:
        current_level = "start"
        pygame.time.delay(360)

      #
      # store variables
      #
      
      subtitle = "Hold U to continue"

      game_status_msg = "Coming Soon (probably never) T-T"
      level_status_msg = "Level Three: "
      difficulty_status_msg = "Down to Earth"

      # clear screen 
      screen.blit(level3_bg_image, (0, 0))          # Achtergrond 

      # draw bricks

      # draw dark blue bricks
      for i in range(0, len(bricks_x_dBlue2)):
        screen.blit(brick_img_dBlue, (bricks_x_dBlue2[i], bricks_y_dBlue2[i]))

      # draw blue bricks
      for i in range(0, len(bricks_x_blue)):
        screen.blit(brick_img_blue, (bricks_x_blue[i], bricks_y_blue[i]))

      # draw yellow bricks
      for i in range(0, len(bricks_x_yellow3)):
        screen.blit(brick_img_yellow, (bricks_x_yellow3[i], bricks_y_yellow3[i]))

      # draw magenta bricks
      for i in range(0, len(bricks_x_magenta)):
        screen.blit(brick_img_magenta, (bricks_x_magenta[i], bricks_y_magenta[i]))

      # draw pink bricks
      for i in range(0, len(bricks_x_pink)):
        screen.blit(brick_img_pink, (bricks_x_pink[i], bricks_y_pink[i]))

      # draw status message
      subtitle = terminalfont.render(subtitle, True, "#559844")
      s_text_width = subtitle.get_width()
      screen.blit(subtitle, (SCREEN_WIDTH / 2 - s_text_width / 2, 250))

      game_status_img = normalfont.render(game_status_msg, True, '#FFFFFF')
      gsi_text_width = game_status_img.get_width()
      screen.blit(game_status_img, (SCREEN_WIDTH / 2 - gsi_text_width / 2, 46))

      level_status_img = fixedsysfont.render(level_status_msg, True, "#3A98BB")
      lsi_text_width = level_status_img.get_width()
      screen.blit(level_status_img, (20, 10))

      difficulty_status_img = dejavuseriffont.render(difficulty_status_msg, True, "#FFCD90")
      screen.blit(difficulty_status_img, (15 + lsi_text_width, 16))

      # show screen
      pygame.display.flip() 

      # go to next level
      if keys[pygame.K_u]:
        current_level = "win"
        
        pygame.time.delay(360)

    elif current_level == "win":
      for event in pygame.event.get(): 
          if event.type == pygame.QUIT:  
              running = False
      keys = pygame.key.get_pressed()

      checkpoint = checkpoint_progress["c_winscreen"]

      if keys[pygame.K_e]:
        current_level = "start"
        pygame.time.delay(360)
      
      screen.blit(winscreen_bg_image, (0, 0)) # Achtergrond

      bwi_text_width = breakout_win_image.get_width()
      screen.blit(breakout_win_image, (SCREEN_WIDTH / 2 - bwi_text_width / 2, 150))
      
      subtitle = "Thanks for playing!"
      subtitle3 = "Hold E to play again"

      subtitle = biggerterminalfont.render(subtitle, True, "#FFFFFFF0")
      s_text_width = subtitle.get_width()
      screen.blit(subtitle, (SCREEN_WIDTH / 2 - s_text_width / 2, 360))

      subtitle3 = smallerterminalfont.render(subtitle3, True, "#FFFFFFBE")
      s3_text_width = subtitle3.get_width()
      screen.blit(subtitle3, (SCREEN_WIDTH / 2 - s3_text_width / 2, 600))

      # show screen
      pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')