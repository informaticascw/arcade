#
# BREAKOUT GAME 
#

import pygame, time
import random

#
# definitions 
#

# current level
current_level = 1

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # breedte van scherm in milimeters
SCREEN_HEIGHT = 720 # hoogte van scherm in milimeters
BALL_WIDTH = 16   # breedte van bal in milimeters
BALL_HEIGHT = 16  # hoogte van bal in milimeters
BRICK_WIDTH = 128
BRICK_HEIGHT = 48
game_status_msg = ""

if current_level == 1:
  ball_x = 600
  ball_speed_x = 7
  ball_y = 200
  ball_speed_y = 14
  paddle_speed = 35
  BRICK_COLUMNS = 10
  BRICK_ROWS = 3
  random_number = random.randint(1003, 1007)
  speed_multiplier = random_number / 1000
elif current_level == 2:
  ball_x = 600
  ball_speed_x = 8
  ball_y = 200
  ball_speed_y = 16
  paddle_speed = 20
  BRICK_COLUMNS = 7
  BRICK_ROWS = 6
  random_number = random.randint(1005, 1010)
  speed_multiplier = random_number / 1000
ball_x = 600
ball_speed_x = 10
ball_y = 250
ball_speed_y = 7

#
# init game
#

pygame.init()
font = pygame.font.SysFont('default', 128)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
# reads spritesheet containing all images

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
if current_level == 1:
  brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
  brick_img.blit(spritesheet, (0, 0), (772, 0, 384, 128))
  brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
elif current_level == 2:
  brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
  brick_img.blit(spritesheet, (0, 0), (386, 650, 384, 128))
  brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))    

star_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
star_img.blit(spritesheet, (0, 0), (1158, 396, 243, 61))   
star_img = pygame.transform.scale(star_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

paddle_x = SCREEN_WIDTH/2-PADDLE_WIDTH/2
paddle_y = SCREEN_HEIGHT-100

# Aantal kolommen en rijen
BRICK_COLUMNS = 10
BRICK_ROWS = 4

# Maak de lijsten voor de brick coördinaten
bricks_x = []
bricks_y = []

# fill in coordinates for bricks
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        # x-coördinaat: kolom * breedte van een brick
        # y-coördinaat: rij * hoogte van een brick
        bricks_x.append(col * BRICK_WIDTH)
        bricks_y.append(row * BRICK_HEIGHT)
# the paddle
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  

#
# game loop
#

print('mygame is running')
running = True #The game is running
while running:
    #
    # read events
    # 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            running = False # if the user exit the game the code stops running (?)
    
    keys = pygame.key.get_pressed()  # reads which key is pressed
    
    if keys [pygame.K_d] : 
       paddle_x += paddle_speed
    if keys [pygame.K_a] : 
       paddle_x -= paddle_speed

    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
        paddle_x = 0

            
    # 
    # move everything
    #

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0:
      ball_speed_x = abs(ball_speed_x)
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:
      ball_speed_x = -abs(ball_speed_x)

    if ball_y < 0:
      ball_speed_y = abs(ball_speed_y)
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
      ball_speed_y = -abs(ball_speed_y)

    # bounce on paddle
    if (ball_y + BALL_HEIGHT >= paddle_y and ball_y + BALL_HEIGHT <= paddle_y + PADDLE_HEIGHT and
      ball_x + BALL_WIDTH >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH):
      ball_speed_y = -abs(ball_speed_y)

    # check collision for all bricks
    for i in range(len(bricks_x)):
        bx = bricks_x[i]
        by = bricks_y[i]
    # check collision for all bricks
    for i in range(len(bricks_x)):
        bx = bricks_x[i]
        by = bricks_y[i]

        if (ball_y + BALL_HEIGHT >= by and ball_y <= by + BRICK_HEIGHT and
            ball_x + BALL_WIDTH >= bx and ball_x <= bx + BRICK_WIDTH):
            print(f'brick {i} touched at ball_x = {ball_x} ball_y = {ball_y}')

            # bepaal kant van botsing
            if ball_speed_y > 0 and ball_y < by:
                ball_speed_y = -abs(ball_speed_y)  # van boven
            elif ball_speed_y < 0 and ball_y > by:
                ball_speed_y = abs(ball_speed_y)   # van onder
            elif ball_speed_x < 0 and ball_x > bx:
                ball_speed_x = -ball_speed_x       # van rechts
            elif ball_speed_x > 0 and ball_x < bx:
                ball_speed_x = -ball_speed_x       # van links
              
            # remove brick
            bricks_x.pop(i)
            bricks_y.pop(i)

            # bal accelerates
            ball_speed_x *= 1.0275
            ball_speed_y *= 1.0275
            break

    # everytime the ball touches the brick the ball and paddle go faster
    if (ball_y + BALL_HEIGHT >= paddle_y and ball_y + BALL_HEIGHT <= paddle_y + PADDLE_HEIGHT and
    ball_x + BALL_WIDTH >= paddle_x and ball_x <= paddle_x + PADDLE_WIDTH):
       ball_speed_y *= speed_multiplier
       ball_speed_x *= speed_multiplier
       paddle_speed *= speed_multiplier
  
        
    # if there are no bricks left the game is won
    if len(bricks_x) == 0 :
       print("You won! GG")
       game_status_msg = "You won! GG\nPress N for the Next Level!\n"
       screen.fill('black')
       game_status_img = font.render(game_status_msg, True, 'green')
       screen.blit(game_status_img, (500, 300))
       pygame.display.flip()
       time.sleep(3)
       running = False
       if keys [pygame.K_n] : 
        current_level += 1
       break

    # check if ball missed the paddle
    if ball_y > paddle_y + PADDLE_HEIGHT:
      print("You lost!")
      game_status_msg = "You lost!"
      screen.fill('black')
      game_status_img = font.render(game_status_msg, True, 'red')
      screen.blit(game_status_img, (500,300))
      pygame.display.flip()
      time.sleep(20)
      running = False
      break

    # clear screen
    screen.fill('black')  # color of the screen

    # draw everything
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    # draw all bricks
    for i in range(len(bricks_x)):
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
    
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame


print('mygame stopt running')
