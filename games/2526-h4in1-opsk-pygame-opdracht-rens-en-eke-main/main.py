#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second

SCREEN_WIDTH = 1280 # beeld breedte 
SCREEN_HEIGHT = 720 # beeld hoogtge

BALL_WIDTH = 16 # bal breedte 
BALL_HEIGHT = 16 # bal hoogte

PADDLE_HEIGHT = 32
PADDLE_WIDTH = 144

PADDLE_HEIGHT = 32
PADDLE_WIDTH = 144

ball_x = SCREEN_WIDTH / 2 #SCREEN_WIDTH / 2# bal hoogte op x as 
ball_speed_x = 5 # bal snelheid

ball_y = SCREEN_HEIGHT - 100 - PADDLE_HEIGHT
ball_speed_y = -6

paddle_x = SCREEN_WIDTH / 2 - (PADDLE_WIDTH / 2)
paddle_y = SCREEN_HEIGHT-100

BRICK_HEIGHT = 32
BRICK_WIDTH = 96
bricks_x =[0,0,0,0,0,192,192,192,192,192,96,350,446,542,350,542,350,446,542,350,542,350,542,700,700,700,700,700,850,850,850,850,850,1000,1096,1192,1000,1192,1000,1192,1000,1192,1000,1096,1192]
bricks_y =[100,132,164,196,228,100,132,164,196,228,164,100,100,100,132,132,164,164,164,196,196,228,228,100,132,164,196,228,100,132,164,196,228,100,100,100,132,132,164,164,196,196,228,228,228]   

#tekst tijdens spel
game_status_msg = "Speel met [A] en [D]"
game_status_msg1 = "Druk op [R] om te resetten"

# init game
#
 
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)   # plaats lege foto voor de bal
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   # plaats bal op scherm
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  # bal goede grote maken``

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)   # plaats lege foto voor de brick 
brick_img.blit(spritesheet, (0, 0), (386, 390, 384, 128))   # plaats brick op scherm
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))  # brick goede grote maken


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
    # 
    # move everything
    

    
   #
    # draw everything
    # ball raakt brick
    for i in range (0, len(bricks_x)):
      if (ball_y + BALL_HEIGHT > bricks_y[i] and 
          ball_y < bricks_y[i] + BRICK_HEIGHT and 
          ball_x + BALL_WIDTH > bricks_x[i] and 
          ball_x < bricks_x[i] + BRICK_WIDTH): 
        
        print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))

        if ball_speed_y > 0 and ball_y + BALL_HEIGHT > bricks_y[i]:
            ball_speed_y = abs(ball_speed_y) * -1 
        elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i]:
            ball_speed_y = abs(ball_speed_y)
        elif ball_speed_x > 0 and ball_x + BALL_WIDTH > bricks_x[i]:
            ball_speed_x = abs(ball_speed_x) * -1
        elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i]:
            ball_speed_x = abs(ball_speed_x)

    # steen verwijderen
        bricks_x.pop(i)
        bricks_y.pop(i)

        break
      

    # ball raakt plank 
    if (ball_x + BALL_WIDTH > paddle_x and
    ball_x < paddle_x + PADDLE_WIDTH and
    ball_y + BALL_HEIGHT > paddle_y and
    ball_y < paddle_y + PADDLE_HEIGHT):
       ball_speed_y = abs(ball_speed_y) * -1

    # move paddle
    if keys[pygame.K_d] : # keys d is down
       paddle_x += 10
    elif keys[pygame.K_a] : # keys a is down
       paddle_x -= 10
    elif keys[pygame.K_r] : 
     ball_x = SCREEN_WIDTH / 2 
     ball_y = SCREEN_HEIGHT - 100 - PADDLE_HEIGHT
     ball_speed_x = 5
     ball_speed_y = 6
     paddle_x = SCREEN_WIDTH / 2 - (PADDLE_WIDTH / 2)
     game_status_msg = 'Speel met [A] en [D]'
     bricks_x =[0,0,0,0,0,192,192,192,192,192,96,350,446,542,350,542,350,446,542,350,542,350,542,700,700,700,700,700,850,850,850,850,850,1000,1096,1192,1000,1192,1000,1192,1000,1192,1000,1096,1192]
     bricks_y =[100,132,164,196,228,100,132,164,196,228,164,100,100,100,132,132,164,164,164,196,196,228,228,100,132,164,196,228,100,132,164,196,228,100,100,100,132,132,164,164,196,196,228,228,228]   



    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
       paddle_x = 0
    


    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y
    
  

    # bounce ball
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x) 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1 
    if ball_y < 0 : 
      ball_speed_y = abs(ball_speed_y) 
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
      ball_speed_y = abs(ball_speed_y) * -1 

    # 
    # handle collisions
    #
    
    # 
    # draw everything
    background_img = pygame.image.load('achtergrond.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_img, (0,0))

    # clear screen
    
  
    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(paddle_img, (paddle_x, paddle_y))

    for i in range (0, len(bricks_x)):
      screen.blit(brick_img,(bricks_x[i], bricks_y[i]))

  
    # bal onder plank verloren
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = 'You lost!'
   # de game statusen moeten nog bij stap 9 bij het you lost tekst

    # win
    if len(bricks_x) == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = 'Level completed!'

   #draw bricks

   # draw game status message
    game_status_img = font.render(game_status_msg , True, 'yellow')
    screen.blit(game_status_img, (SCREEN_WIDTH / 2 - game_status_img.get_width() / 2, SCREEN_HEIGHT - game_status_img.get_width() / 2)) 
    
    game_status_img1 = font.render(game_status_msg1 , True, 'yellow')
    screen.blit(game_status_img1, (SCREEN_WIDTH / 2 - game_status_img1.get_width() / 2, SCREEN_HEIGHT / 2   - game_status_img1.get_width() / 2))
   # define global variables
   # define global variables

   
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')

                                                                       