#
# BREAKOUT GAME 
#

import pygame
import random
#
# definitions 
#
# define global variables
FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # Screen size in X-direction in pixels
SCREEN_HEIGHT = 720 # Screen size in Y-direction in pixels

BALL_WIDTH = 16 # Ballsize in X-direction in pixels
BALL_HEIGHT = 16 # Ballsize in Y-direction in pixels

PADDLE_HEIGHT = 32 # Paddlesize in X-direction in pixels
PADDLE_WIDTH = 144 # Paddlesize in Y-direction in pixels

BRICK_WIDTH = 96   # Bricksize in X-direction in pixels
BRICK_HEIGHT = 32  # Bricksize in Y-direction in pixels

#speed limits
MAX_BALL_SPEED_X = 8
MIN_BALL_SPEED_X = 5
MAX_BALL_SPEED_Y = 12


ball_x = [0] # X-position of the ball in pixels
ball_speed_x = [6] # Speed of ball in X-direction in pixels per frame

ball_y = [100] 
ball_speed_y = [10]
paddle_x = (SCREEN_WIDTH / 2) - (PADDLE_WIDTH / 2)
paddle_y = (SCREEN_HEIGHT) - (PADDLE_HEIGHT)
bricks_x = [96, 192, 288, SCREEN_WIDTH - 192, SCREEN_WIDTH - 288, SCREEN_WIDTH - 384,
            96, 192, 288, SCREEN_WIDTH - 192, SCREEN_WIDTH - 288, SCREEN_WIDTH - 384,
            96, 192, 288, SCREEN_WIDTH - 192, SCREEN_WIDTH - 288, SCREEN_WIDTH - 384,
            96, 192, 288, SCREEN_WIDTH - 192, SCREEN_WIDTH - 288, SCREEN_WIDTH - 384]
bricks_y = [100, 100, 100, 100, 100, 100,
            132, 132, 132, 132, 132, 132,
            164, 164, 164, 164, 164, 164,
            196, 196, 196, 196, 196, 196]
bricks_durability = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
bricks_powerups = []
brick_color_x = [772,0,0,772,772,386,386,386,772,386]
brick_color_y = [390,130,390,260,0,650,390,130,520,780]
brick_imgs = [0,1,2,3,4,5,6,7,8,9]
remove_pop = 0
screen_img_position = 0
day = 0
game_status_msg = ""

#
# init game
#
color_one_time = random.randint(0,9)
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#assign powerups to bricks
for i in range(len(bricks_x)):
   bricks_powerups.append(random.randint(0,1))

print(bricks_powerups)

#
# read images
#

# read spritesheet containing all images
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() 
screen_img = pygame.image.load('pixel-art-stars-pattern-shining-260nw-2633108833__1_-removebg-preview.png').convert_alpha()

# make ball_img
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

# make brick_img
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) 
for i in range(0, len(bricks_x)) :
   color = random.randint(0,9)
   brick_img.blit(spritesheet, (0, 0), (brick_color_x[color], brick_color_y[color], 384, 128)) 
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

#make paddle_img
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) 
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) 

#make screen_img
screen_img = pygame.transform.scale(screen_img, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

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

    #
    # read events
    # 
    for event in pygame.event.get(): # read all events
        if event.type == pygame.QUIT:  # GUI is closed
            running = False # end program
    keys = pygame.key.get_pressed() # read which keys are down

    #move right        
    if keys[pygame.K_d]:
       paddle_x += 10
   
    #move left
    if keys[pygame.K_a]:
       paddle_x -= 10

    #spawn ball cheat
    if keys[pygame.K_q]:
      ball_x.append(random.randint(0,1280))
      ball_y.append(200)
      ball_speed_x.append(6)
      ball_speed_y.append(10) 
    
    #remove ability for ball to despawn
    if keys[pygame.K_e]:
       remove_pop += 1
       print(remove_pop)
      
    # move everything
    
    # make paddle unable to move if hitting edge
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
       paddle_x = 0

    # move ball
    for i in range(len(ball_x)):
      ball_x[i] = ball_x[i] + ball_speed_x[i]
      ball_y[i] = ball_y[i] + ball_speed_y[i]

    # bounce ball against edges of screen
      if ball_x[i] < 0 : # left edge
         ball_speed_x[i] = abs(ball_speed_x[i]) # positive x speed = move right
      if ball_x[i] + BALL_WIDTH > SCREEN_WIDTH: # move right
         ball_speed_x[i] = abs(ball_speed_x[i]) * -1 # negative x speed = move left
      if ball_y[i] < 0 :
         ball_speed_y[i] = abs(ball_speed_y[i])
      if ball_y[i] + BALL_HEIGHT > SCREEN_HEIGHT:
         ball_speed_y[i] = abs(ball_speed_y[i]) * -1
      
    # 
    # handle collisions
    #

    #handle ball-paddle collisions
    for i in reversed(range(len(ball_x))):
      if (ball_x[i] + BALL_WIDTH > paddle_x 
         and ball_x[i] < paddle_x + PADDLE_WIDTH
         and ball_y[i] + BALL_HEIGHT > paddle_y 
         and ball_y[i] < paddle_y + PADDLE_HEIGHT):
         ball_speed_y[i] = abs(ball_speed_y[i]) * -1.01
         color_one_time = random.randint(0,9)
     
      if (ball_x[i] + BALL_WIDTH > paddle_x 
        and ball_x[i] < paddle_x + PADDLE_WIDTH
        and ball_y[i] + BALL_HEIGHT > paddle_y 
        and ball_y[i] < paddle_y + PADDLE_HEIGHT
        and ball_x[i] + BALL_WIDTH < paddle_x + PADDLE_WIDTH * 0.25):
         ball_speed_y[i] = abs(ball_speed_y[i]) * -1.01
         if ball_speed_x[i] < 0:
          ball_speed_x[i] = abs(ball_speed_x[i]) * -1.2
         elif ball_speed_x[i] > 0:
          ball_speed_x[i] = abs(ball_speed_x[i]) * 1.2
          color_one_time = random.randint(0,9)
    
      if (ball_x[i] + BALL_WIDTH > paddle_x 
        and ball_x[i] < paddle_x + PADDLE_WIDTH
        and ball_y[i] + BALL_HEIGHT > paddle_y 
        and ball_y[i] < paddle_y + PADDLE_HEIGHT
        and ball_x[i] > paddle_x + (PADDLE_WIDTH - PADDLE_WIDTH * 0.25)):
         ball_speed_y[i] = abs(ball_speed_y[i]) * -1.01
         if ball_speed_x[i] < 0:
            ball_speed_x[i] = abs(ball_speed_x[i]) * -1.2
         elif ball_speed_x[i] > 0:
            ball_speed_x[i] = abs(ball_speed_x[i]) * 1.2
            color_one_time = random.randint(0,9)
    
      if (ball_x[i] + BALL_WIDTH > paddle_x 
        and ball_x[i] < paddle_x + PADDLE_WIDTH
        and ball_y[i] + BALL_HEIGHT > paddle_y 
        and ball_y[i] < paddle_y + PADDLE_HEIGHT
        and ball_x[i] + BALL_WIDTH > paddle_x + PADDLE_WIDTH * 0.25
        and ball_x[i] + BALL_WIDTH < paddle_x + (PADDLE_WIDTH - PADDLE_WIDTH * 0.25)):
         ball_speed_y[i] = abs(ball_speed_y[i]) * -1.01
         if ball_speed_x[i] < 0:
            ball_speed_x[i] = abs(ball_speed_x[i]) * -0.8
         elif ball_speed_x[i] > 0:
            ball_speed_x[i] = abs(ball_speed_x[i]) * 0.8
            color_one_time = random.randint(0,9)

      #handle brick-ball collsions
      for brick in reversed(range(0, len(bricks_x))) :
         if (ball_x[i] + BALL_WIDTH > bricks_x[brick]
            and ball_x[i] < bricks_x[brick] + BRICK_WIDTH
            and ball_y[i] + BALL_HEIGHT > bricks_y[brick]
            and ball_y[i] < bricks_y[brick] + BRICK_HEIGHT):

            print('brick touched at ball_x = ' + str(ball_x[i]) + ' and ball_y = ' + str(ball_y[i]))
            print(ball_speed_x[i])

            hit = False
            if (ball_speed_y[i] > 0  and ball_y[i] < bricks_y[brick]):
               ball_speed_y[i] = -abs(ball_speed_y[i]) * 1.01
               bricks_durability[brick] = bricks_durability[brick] - 1
               hit = True

            elif (ball_speed_y[i] < 0 and ball_y[i] + BALL_HEIGHT > bricks_y[brick] + BRICK_HEIGHT):
               ball_speed_y[i] = abs(ball_speed_y[i]) * 1.01
               bricks_durability[brick] = bricks_durability[brick] - 1
               hit = True

            elif (ball_speed_x[i] > 0  and ball_x[i] < bricks_x[brick]):
               ball_speed_x[i] = -abs(ball_speed_x[i]) * 1.01
               bricks_durability[brick] = bricks_durability[brick] - 1
               hit = True

            elif (ball_speed_x[i] < 0 and ball_x[i] + BALL_WIDTH > bricks_x[brick] + BRICK_WIDTH):
               ball_speed_x[i] = abs(ball_speed_x[i]) * 1.01
               bricks_durability[brick] = bricks_durability[brick] - 1
               hit = True
            if hit:
               if bricks_durability[brick] <= 0:
                  if bricks_powerups[brick] == 1:
                        print("This is ze powerup")
                        ball_x.append(bricks_x[brick] + 48)
                        ball_y.append(bricks_y[brick])    
                        ball_speed_x.append(6)
                        ball_speed_y.append(10)  
                  bricks_x.pop(brick)
                  bricks_y.pop(brick)
                  bricks_durability.pop(brick)
                  bricks_powerups.pop(brick)
            print(bricks_durability)
            break
         
         #add speed limit's
         for max in range(0, len(ball_x)):
            if ball_speed_x[max] > MAX_BALL_SPEED_X:
               ball_speed_x[max] = MAX_BALL_SPEED_X
            elif ball_speed_x[max] < -MAX_BALL_SPEED_X:
               ball_speed_x[max] = -MAX_BALL_SPEED_X

            if 0 < ball_speed_x[max] < MIN_BALL_SPEED_X:
                  ball_speed_x[max] = MIN_BALL_SPEED_X
            elif -MIN_BALL_SPEED_X < ball_speed_x[max] < 0:
                  ball_speed_x[max] = -MIN_BALL_SPEED_X

            if ball_speed_y[max] > MAX_BALL_SPEED_Y:
               ball_speed_y[max] = MAX_BALL_SPEED_Y
            elif ball_speed_y[max] < -MAX_BALL_SPEED_Y:
               ball_speed_y[max] = -MAX_BALL_SPEED_Y           
      
      # removes ball if hit ground
      for i in reversed(range(len(ball_x))):
       if ball_y[i] + BALL_HEIGHT > SCREEN_HEIGHT:
         if remove_pop == 0:
            ball_x.pop(i)
            ball_y.pop(i)
            ball_speed_x.pop(i)
            ball_speed_y.pop(i)
            break
      
      # game status
      if len(ball_x) == 0:
          game_status_msg = "You lose!"

      if screen_img_position > SCREEN_HEIGHT:
         game_status_msg = "Out of time!"
         day = 1
         for i in range (0, len(ball_x)):
            ball_speed_x[i] = 0
            ball_speed_y[i] = 0
         
      if len(bricks_x) <= 0:
         game_status_msg = "You win!"
         for i in range(len(ball_x)):
            ball_speed_y[i] = 0
            ball_speed_x[i] = 0

    # 
    # draw everything
    #
   
    # clear screen
    if day == 0:
      screen.fill('dark blue') 
    elif day == 1:
      screen.fill("lightblue")

    screen.blit(screen_img, (0, screen_img_position))
   
    # draw ball
    for ball in range(0, len(ball_x)) :
      screen.blit(ball_img, (ball_x[ball], ball_y[ball]))
    
    #draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw bricks
    for i in range(0, len(bricks_x)) :
      if bricks_durability[i] == 1:
         brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
         brick_img.blit(spritesheet, (0, 0), (brick_color_x[color_one_time], brick_color_y[color_one_time], 384, 128))  # copy part of sheet to image
      else:
         brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
         color = random.randint(0,9)
         brick_img.blit(spritesheet, (0, 0), (brick_color_x[color], brick_color_y[color], 384, 128))  # copy part of sheet to image

      brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # resize image
      screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
    
    # redefine screen_img  
    screen_img_position = screen_img_position + 0.2

    
    # draw game status message
    game_status_img = font.render(game_status_msg, True, 'green')
    screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) / 2 , (SCREEN_HEIGHT - game_status_img.get_height()) / 2)) # (0, 0) is top left corner of screen

    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
