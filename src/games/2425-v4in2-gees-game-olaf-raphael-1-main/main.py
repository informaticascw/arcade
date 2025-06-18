# BREAKOUT GAME 
#

import pygame, time, math, random

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 150
BRICK_HEIGHT = 45

paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100

balls = [{
    'x': paddle_x + (PADDLE_WIDTH / 2),
    'y': paddle_y - 20,
    'speed_x': 0,
    'speed_y': 0,
    'speed': 0
}]

heart_x = SCREEN_WIDTH - 84
heart_y = 20

rijenBricks = random.randint(4,12) # hoeveelheid bricks horizontaal
kolommenBricks = random.randint(2,7) # hoeveelheid bricks verticaal

bricks = []


def brick_Generation(rijenBricks, kolommenBricks):
    global bricks
    bricks = []
    brick_x = 30
    brick_y = 70
    for g in range(kolommenBricks):
        for j in range(rijenBricks):
            bricks.append({'x': brick_x, 'y': brick_y, 'hits': 0})
            brick_x += BRICK_WIDTH
        brick_x = 30
        brick_y += BRICK_HEIGHT



level_Status = False
level_Counter = 0
game_status_msg = ''
game_status_msg2 = ''
game_status_msg3 = ''
health_Status = 3
cheated_Status = False
victory_Reported = False
frame_counter = 0
frame_counter2 = 0
paddle_frame = 0


def reset_Level_State():
    global balls
    balls.clear()
    balls = [{
       'x': paddle_x + (PADDLE_WIDTH / 2) - (BALL_WIDTH / 2),
       'y': paddle_y - BALL_HEIGHT,
       'speed_x': 0,
       'speed_y': 0,
       'speed': 0
    }]

 

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

spritesheet = pygame.image.load('images/Breakout_Tile_Free.png').convert_alpha()   

background = pygame.image.load('images/4394259_91657.jpg').convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH,SCREEN_HEIGHT))  


ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img1 = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img1.blit(spritesheet, (0,0), (1158, 462, 243, 64)) # copy part of sheet to image
paddle_img1 = pygame.transform.scale(paddle_img1, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

paddle_img2 = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img2.blit(spritesheet, (0,0), (1158, 528, 243, 64)) # copy part of sheet to image
paddle_img2 = pygame.transform.scale(paddle_img2, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

paddle_img3 = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img3.blit(spritesheet, (0,0), (1158, 594, 243, 64)) # copy part of sheet to image
paddle_img3 = pygame.transform.scale(paddle_img3, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

paddles_img = [paddle_img1, paddle_img2, paddle_img3]

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  # create new image

# eerste kleur
brick_img.blit(spritesheet, (0, 0), (772, 520, 384, 128))
brick_img1 = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

# tweede kleur (bij 1x geraakt)
brick_img.blit(spritesheet, (0, 0), (0, 390, 384, 128))
brick_img2 = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

brickscolors = [brick_img1, brick_img2]

heart_img = pygame.Surface((64, 58), pygame.SRCALPHA) # create new image
heart_img.blit(spritesheet, (0,0), (1637, 652, 64, 58)) # copy part of sheet to image
heart_img = pygame.transform.scale(heart_img, (64, 58)) # resize image

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
           # Cheats
           if event.key == pygame.K_x:
              bricks.clear()
              print('Level skipped')
              level_Counter += 1
              cheated_Status = True
              level_Status = True
           if event.key == pygame.K_z:
              health_Status += 1
              print('You\'re on ' + str(health_Status) + ' hearts.')
              cheated_Status = True
           if event.key == pygame.K_c:
            cheated_Status = True
            new_ball2 = {
               'x': paddle_x + (PADDLE_WIDTH / 2),
               'y': paddle_y - 20,
               'speed_x': random.choice([-5,5]),
               'speed_y': random.choice([-5,5]),
               'speed': 10
            }
            balls.append(new_ball2)
              
    # Paddle movement 
    keys = pygame.key.get_pressed()
    if paddle_x + PADDLE_WIDTH < SCREEN_WIDTH:
      if keys[pygame.K_d]:
        paddle_x = paddle_x + 15
    if paddle_x > 0:
      if keys[pygame.K_a]:
        paddle_x = paddle_x - 15

    # 
    # move everything
    #

    # move ball
    if not game_status_msg == 'Victory Royale':
      for ball in balls:
        ball['x'] += ball['speed_x']
        ball['y'] += ball['speed_y']

    # 
    # handle collisions
    #
   
    # bounce ball
    if not game_status_msg == 'Victory Royale':
      for ball in balls:
        if ball['x'] < 0:
          ball['speed_x'] = abs(ball['speed_x']) 
       
      for ball in balls:
        if ball['x'] + BALL_WIDTH > SCREEN_WIDTH:
          ball['speed_x'] = -abs(ball['speed_x'])

      for ball in balls:
        if ball['y'] < 0:
          ball['speed_y'] = abs(ball['speed_y'])

    
      for ball in balls:
        if (ball['x'] + BALL_WIDTH > paddle_x and 
          ball['x'] < paddle_x + PADDLE_WIDTH and
          ball['y'] + BALL_HEIGHT > paddle_y and 
          ball['y'] < paddle_y + PADDLE_HEIGHT):
           
           offset = (ball['x'] + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)
           ball['speed_x'] = offset * 0.1
           ball['speed_y'] = -math.sqrt(ball['speed']**2 - ball['speed_x']**2)
           # clamp speed
           if -2 < ball['speed_x'] < 2:
              ball['speed_x'] = 2 if ball['speed_x'] >= 0 else -2
           if ball['speed_x'] > 20:
              ball['speed_x'] = 20
           elif ball['speed_x'] < -20:
              ball['speed_x'] = -20
           ball['speed_y'] = abs(ball['speed_y']) * -1

       
    # brick bounce
   
      for ball in balls:
        i = 0
        while i < len(bricks):
            brick = bricks[i]
            bx = brick['x']
            by = brick['y']

            if (ball['x'] + BALL_WIDTH > bx and
                ball['x'] < bx + BRICK_WIDTH and
                ball['y'] + BALL_HEIGHT > by and
                ball['y'] < by + BRICK_HEIGHT):

                print('brick touched at ball_x = ' + str(ball['x']) + ' and ball_y = ' + str(ball['y']))

                # van boven geraakt
                if ball['speed_y'] > 0 and ball['y'] + BALL_HEIGHT - ball['speed_y'] <= by:
                    ball['speed_y'] = -abs(ball['speed_y'])

                # van onder geraakt
                elif ball['speed_y'] < 0 and ball['y'] - ball['speed_y'] >= by + BRICK_HEIGHT:
                    ball['speed_y'] = abs(ball['speed_y'])

                # van links geraakt
                elif ball['speed_x'] > 0 and ball['x'] + BALL_WIDTH - ball['speed_x'] <= bx:
                    ball['speed_x'] = -abs(ball['speed_x'])

                # van rechts geraakt
                elif ball['speed_x'] < 0 and ball['x'] - ball['speed_x'] >= bx + BRICK_WIDTH:
                    ball['speed_x'] = abs(ball['speed_x'])

                brick['hits'] += 1
                print(f"Brick hit at ({bx},{by}), hits: {brick['hits']}")

                if brick['hits'] >= 2:
                    bricks.pop(i)
                    # Systeem om een ball toe te voegen
                    if random.randint(1, 4) == 1:
                      if brick['hits'] >= 2:
                          new_ball = {
                            'x': ball['x'],
                            'y': ball['y'],
                            'speed_x': random.choice([-5, 5]),
                            'speed_y': -7,
                            'speed': 10
                            }
                          balls.append(new_ball)
                else:
                    i += 1  # Alleen verder tellen als brick blijft

                ball['speed'] *= 1.005
                break  # per bal maar 1 brick per frame raken
            else:
                i += 1
        

    #
    # Game logic
    #
    if not game_status_msg == 'Victory Royale':
      # ball counter text
      game_status_msg3 = str(len(balls))
      # start message       
      for ball in balls:
        if ball['speed_x']  == 0 and ball['speed_y'] == 0 and health_Status != 0:
            game_status_msg = "Speel met [A] en [D]"
      # game over
      balls = [ball for ball in balls if ball['y'] <= SCREEN_HEIGHT]    # Bal buiten scherm check
      if len(balls) == 0:
        health_Status -= 1
        reset_Level_State()
        if health_Status > 0:
          print('Youre on ' + str(health_Status) + ' hearts.')
      if health_Status == 0:
        game_status_msg = "Game over"

      # start function
      for ball in balls:
        if level_Counter == 0 and ball['speed_x'] == 0 and ball['speed_y'] == 0 and health_Status == 3:
          level_Status = True
          level_Counter += 1
          reset_Level_State()

        
      # restart function
      for ball in balls:
        if ball['speed_x'] == 0 and ball['speed_y'] == 0 and health_Status != 0:
          if keys[pygame.K_d]:
            ball['speed'] = 10
            ball['speed_x'] = 7
            ball['speed_y'] = -7
          if keys[pygame.K_a]:
            ball['speed'] = 10
            ball['speed_x'] = -7
            ball['speed_y'] = -7
      
      # Brick generation
      if level_Counter == 1 and level_Status == True:
        brick_Generation(8,2)
        reset_Level_State()
        level_Status = False
      elif level_Counter == 2 and level_Status == True:
        brick_Generation(8,3)
        reset_Level_State()
        for ball in balls:
          ball['speed'] *= 1.1
        level_Status = False
      elif level_Counter == 3 and level_Status == True:
        brick_Generation(8,4)
        reset_Level_State()
        for ball in balls:
          ball['speed'] *= 1.1
        level_Status = False

      # level systeem
      if level_Counter == 1:
        game_status_msg2 = 'Level 1'
      elif level_Counter == 2:
        game_status_msg2 = 'Level 2'
      elif level_Counter == 3:
        game_status_msg2 = 'Level 3'
      
      # you won
      if len(bricks) == 0:
        for ball in balls:
          ball['speed_x'] = 0
          ball['speed_y'] = 0
        level_Counter += 1
        level_Status = True
        if level_Counter >= 3:
          game_status_msg = "Victory Royale"
          game_status_msg2 = ''
          ball.clear()
          if cheated_Status and not victory_Reported:
              print('maar je hebt wel gecheat stommerik')
              victory_Reported = True

    # 
    # draw everything
    #

    # clear screen
    
    screen.blit(background, (0,0)) 

    # draw ball
    if not game_status_msg == 'Victory Royale':
      for ball in balls:
        screen.blit(ball_img, (ball['x'], ball['y']))

    # draw paddle
    # wissel om de 10 frames van paddle afbeelding
    frame_counter += 1
    if frame_counter >= 2:
       paddle_frame = (paddle_frame + 1) % len(paddles_img)
       frame_counter = 0

    # teken de juiste paddle afbeelding
    screen.blit(paddles_img[paddle_frame], (paddle_x, paddle_y))

    # draw level status message
    if game_status_msg2 != "":
         game_status_img2 = font.render(game_status_msg2, True, 'White')
         screen.blit(game_status_img2, (30, 20))

    # draw ball counter text
    game_status_img3 = font.render(game_status_msg3, True, 'White')
    screen.blit(game_status_img3, (30, SCREEN_HEIGHT - 60))

    # draw brick
    for brick in bricks:
      img_index = brick['hits']
      if img_index >= len(brickscolors):
         img_index = len(brickscolors) - 1  #teveel hits
      screen.blit(brickscolors[img_index], (brick['x'], brick['y']))
      
    # draw heart
    for o in range(health_Status):
      screen.blit(heart_img, ((heart_x - o * 64), heart_y))

    # draw game status message
    if game_status_msg != "":
      if game_status_msg == 'Victory Royale':
         game_status_img = font.render(game_status_msg, True, 'Green')
         screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - 200, SCREEN_HEIGHT / 2))
      if game_status_msg == 'Game over':
         game_status_img = font.render(game_status_msg, True, 'red')
         screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - 130, SCREEN_HEIGHT / 2))
      if game_status_msg == 'Speel met [A] en [D]':
         game_status_img = font.render(game_status_msg, True, 'white')
         screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - 200, SCREEN_HEIGHT - 50))

    
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')