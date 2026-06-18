#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
game_status_msg = "Je kan naar opzij maar ook naar boven en beneden :)"
#



FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16  # ballsize in x-direction in pixels
BALL_HEIGHT = 16 # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH =  96
BRICK_HEIGHT = 32

ball_x = SCREEN_WIDTH / 2  # x-position of ball in pixels
ball_speed_x = 6 # speed of ball in x-direction in pixels per frame
ball_y = SCREEN_HEIGHT - 100
ball_speed_y = 6

bricks_x = []
bricks_y = []

for row in range(5):
    for col in range(10):
        bricks_x.append(160 + col * BRICK_WIDTH)
        bricks_y.append(128 + row * BRICK_HEIGHT)

brick_health = [2] * len(bricks_x)
#hier gaan we een aantal blauwe blokken random paars laten zijn
import random
brick_colors = ["blue"] * len(bricks_x)
purple_indices = random.sample(range(len(bricks_x)), 10)
for i in purple_indices:
    brick_colors[i] = "purple"

paddle_x = SCREEN_WIDTH / 2
paddle_speed_x = 1
paddle_y = SCREEN_HEIGHT - 100

#voor zijkant van scherm raakt
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   
background = pygame.image.load("pikachu.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0,0 ), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0,0 ), (772, 390, 384, 128)) 
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

cracked_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
cracked_brick_img.blit(spritesheet, (0,0), (0, 0, 384, 128))
cracked_brick_img = pygame.transform.scale(cracked_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

purple_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
purple_brick_img.blit(spritesheet, (0,0), (0, 390, 384, 128))
purple_brick_img = pygame.transform.scale(purple_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

purple_cracked_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
purple_cracked_brick_img.blit(spritesheet, (0,0), (0, 520, 384, 128))
purple_cracked_brick_img = pygame.transform.scale(purple_cracked_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

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
    keys = pygame.key.get_pressed() 
            
    # 
    # move everything
    #

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # move paddle
    if keys[pygame.K_d]:
      paddle_x += 10
    if keys[pygame.K_a] :
      paddle_x -= 10
    if keys[pygame.K_s]:
      paddle_y += 10
    if keys[pygame.K_w] :
      paddle_y -= 10
      
    # bounce ball
    if ball_x < 0: 
      ball_speed_x = abs(ball_speed_x) 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1 
    if ball_y < 0: 
      ball_speed_y = abs(ball_speed_y)
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
      ball_speed_y = abs(ball_speed_y) * 0
      ball_speed_x = abs(ball_speed_x) * 0
      game_status_msg = "You lost!"

    # ball to brick collission
    for i in range(len(bricks_x)): 
       if ball_x + BALL_WIDTH > bricks_x[i] and ball_x < bricks_x[i] + BRICK_WIDTH and ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT:
        print('brick touched at:' + str(ball_x) + ' and ball_y = ' + str(ball_y))
        if ball_speed_y > 0 and ball_y + BALL_HEIGHT > bricks_y[i]:
            ball_speed_y = -abs(ball_speed_y)
        elif ball_speed_y < 0 and ball_y < bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y)
        elif ball_speed_x > 0 and ball_x + BALL_WIDTH > bricks_x[i]:
            ball_speed_x = -abs(ball_speed_x)
        elif ball_speed_x < 0 and ball_x < bricks_x[i] + BRICK_WIDTH:
            ball_speed_x = abs(ball_speed_x) 
        ball_speed_x *= 1.01
        ball_speed_y *= 1.01
        brick_health[i] -= 1
       if brick_health[i] == 0:
          #check of het een paarse brick is die wordt gebroken         
          if brick_colors[i] == "purple":
            #zet in een aparte lijst
            to_remove = []

            for j in range(len(bricks_x)):
                #als de brick paars is en in de goeie x-positie zit dan continue
                if j == i:
                    continue
                #check welke blokken ernaast zitten
                if abs(bricks_x[j] - bricks_x[i]) <= BRICK_WIDTH and \
                  abs(bricks_y[j] - bricks_y[i]) <= BRICK_HEIGHT:

                    brick_health[j] -= 1
                    #als de brick health 0 wordt dan remove uit de lijst, code van brick naar cracked brick werkt nu
                    if brick_health[j] <= 0:
                        to_remove.append(j)
            #als hij ernaast zit dan haal je de brick weg en wordt het cracked brick
            for j in sorted(to_remove, reverse=True):
                bricks_x.pop(j)
                bricks_y.pop(j)
                brick_health.pop(j)
                brick_colors.pop(j)

                if j < i:
                    i -= 1

          bricks_x.pop(i)
          bricks_y.pop(i)
          brick_health.pop(i)
          brick_colors.pop(i)
          break
 


  
    #paddle collisions
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
      paddle_x = 0
    #ball collisions
      #ball to paddle collisions
    if ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT:
      ball_speed_y = -abs(ball_speed_y)
      paddle_center = paddle_x + PADDLE_WIDTH / 2
      ball_center = ball_x + BALL_WIDTH / 2
      difference = ball_center - paddle_center
      ball_speed_x = difference * 0.1
      
      
    # winning
    if len(bricks_x) == 0:
      ball_speed_x = 0
      ball_speed_y = 0
      game_status_msg = "You win!"
    
    # draw everything


    # clear screen  
    screen.blit(background, (0, 0))
    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    #draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))
    #draw bricks
    
    for i in range(len(bricks_x)):
      if brick_colors[i] == "purple":

        if brick_health[i] == 2:
            screen.blit(purple_brick_img, (bricks_x[i], bricks_y[i]))

        elif brick_health[i] == 1:
            screen.blit(purple_cracked_brick_img, (bricks_x[i], bricks_y[i]))
      else: 
        if brick_health[i] == 2:
          screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
        elif brick_health[i] == 1:
          screen.blit(cracked_brick_img, (bricks_x[i], bricks_y[i]))


# draw game status message
    game_status_img = font.render(game_status_msg, True, 'white')
    screen.blit(game_status_img, (0, 0))
    pygame.display.flip() 

    # 

    
    # wait until next frame
    #


    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
