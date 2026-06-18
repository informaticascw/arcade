#
# BREAKOUT GAME 
#

import pygame, time
import random
#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16    # ball settings
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
#variabelen
ball_x = random.randint(384, 850)
ball_speed_x = 6
ball_y = 100
ball_speed_y = 8
paddle_x = SCREEN_WIDTH / 2 - 80
paddle_y = SCREEN_HEIGHT - 100
bricks_x = [96, 96, 96, 96, 192, 192, 192, 192, 288, 288, 288, 288, 1088, 1088, 1088, 1088, 992, 992, 992, 992, 896, 896, 896, 896]
bricks_y = [200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296]
bricks_color = ['green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen']
game_status_msg = "You lost!"
game_status_msg2 = 'Victory!'
destroy_effects = []




#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
achtergrond = pygame.image.load('achtergrond2.png').convert_alpha()   
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  # ball visuals

# game loop

# PADDLE
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

#BRICK
# DONKERGROEN BLOK
brick_green_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_green_img.blit(spritesheet, (0, 0), (386, 130, 384, 128))
brick_green_img = pygame.transform.scale(brick_green_img, (BRICK_WIDTH, BRICK_HEIGHT))

# LICHTGROEN BLOK
brick_lightgreen_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_lightgreen_img.blit(spritesheet, (0, 0), (0, 130, 384, 128))
brick_lightgreen_img = pygame.transform.scale(brick_lightgreen_img, (BRICK_WIDTH, BRICK_HEIGHT))

print('mygame is running')
running = True
while running:
    # achtergrond niks
    screen.blit(achtergrond,(0, 0))
    # read events
    # 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            running = False 
    keys = pygame.key.get_pressed() 

    # reset game
    if keys[pygame.K_r] :
       # bal wordt gereset
       ball_x = random.randint(384, 850)
       ball_speed_x = 6
       ball_y = 100
       ball_speed_y = 8

       # blokken reset
       bricks_x = [96, 96, 96, 96, 192, 192, 192, 192, 288, 288, 288, 288, 1088, 1088, 1088, 1088, 992, 992, 992, 992, 896, 896, 896, 896]
       bricks_y = [200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296, 200, 232, 264, 296]
       bricks_color = ['green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen', 'green', 'lightgreen']
       
       #effecten leegmaken
       destroy_effects = []

       # reset paddle
       paddle_x = SCREEN_WIDTH / 2 - 80
       paddle_y = SCREEN_HEIGHT - 100


    
    # move everything
    if keys[pygame.K_d] : #key d is down
       paddle_x = paddle_x + 10
    if keys[pygame.K_a] : #key a is down
       paddle_x = paddle_x - 10
  
    # paddle kan niet uit scherm
    if (paddle_x + PADDLE_WIDTH > SCREEN_WIDTH):
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
   
    if paddle_x < 0:
       paddle_x = 0

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball_x
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x) 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1 


    # bounce ball_y
    if ball_y < 0 : 
      ball_speed_y = abs(ball_speed_y) 
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
      ball_speed_y = abs(ball_speed_y) *  -1
    

    # bal stuitert op paddle
    if (ball_x + BALL_WIDTH > paddle_x and 
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT) :
        # bal omhoog laten gaan
     ball_speed_y = abs(ball_speed_y) * -1

    # midden van paddle berekenen
     paddle_center = paddle_x + PADDLE_WIDTH / 2

    # midden van bal berekenen
     ball_center = ball_x + BALL_WIDTH / 2

    # verschil tussen bal en midden plank
     verschil = ball_center - paddle_center

    # nieuwe horizontale snelheid
     ball_speed_x = verschil / 8
       

   # bal raakt niet vast in paddle
     ball_y = paddle_y - BALL_HEIGHT

   # tekst hoeveel blokken nog
    blokken_over_tekst = font.render(
       'Blokken over:' + ' ' + str(len(bricks_x)), True, 'black'
    )
    screen.blit(blokken_over_tekst, (20,20))

   

# bal stuitert op blok
    for i in range(len(bricks_x)):
     if (ball_x + BALL_WIDTH > bricks_x[i] and
        ball_x < bricks_x[i] + BRICK_WIDTH and
        ball_y + BALL_HEIGHT > bricks_y[i] and
        ball_y < bricks_y[i] + BRICK_HEIGHT):

        ball_speed_x = ball_speed_x * 1.025
        ball_speed_y = ball_speed_y * 1.025

        print('brick touched at ball_x = ' + str(ball_x) +
              ' and ball_y = ' + str(ball_y))

        # bal komt van boven
        if ball_speed_y > 0 and ball_y < bricks_y[i]:
            ball_speed_y = abs(ball_speed_y) * -1

        elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y)

        elif ball_speed_x > 0 and ball_x < bricks_x[i]:
            ball_speed_x = abs(ball_speed_x) * -1

        elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
            ball_speed_x = abs(ball_speed_x)

        # blok verwijderen
        destroy_effects.append([
         bricks_x[i],
         bricks_y[i],
         bricks_color[i]
         ])

        bricks_x.pop(i)
        bricks_y.pop(i)
        bricks_color.pop(i)
        break


   
    
    
    # tekst als je verliest
    
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT :
       ball_speed_y = 0
       ball_speed_x = 0
       game_status_img = font.render(game_status_msg, True, 'red')
       screen.blit(game_status_img, ((SCREEN_WIDTH / 2 - 80), (SCREEN_HEIGHT / 2 - 50))) # (0, 0) is top left corner of screen
       reset_tekst = font.render(
       'Druk op [R] om te resetten', True, 'red'
    ) 
       screen.blit(reset_tekst, ((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 2 + 100)))
       
   #tekst als je wint
    if len(bricks_x) == 0:
        ball_speed_y = 0
        ball_speed_x = 0
        game_status_img = font.render(game_status_msg2, True, 'blue')
        screen.blit(game_status_img, ((SCREEN_WIDTH / 2 - 80), (SCREEN_HEIGHT / 2 - 100))) # (0, 0) is top left corner of screen
        reset_tekst = font.render(
       'Druk op [R] om te resetten', True, 'red'
    )
        screen.blit(reset_tekst, ((SCREEN_WIDTH / 4), (SCREEN_HEIGHT / 2 + 100)))
       
       
  
    
    # draw everything
    for i in range(len(bricks_x)):

      if bricks_color[i] == 'green':
        screen.blit(brick_green_img, (bricks_x[i], bricks_y[i]))

      elif bricks_color[i] == 'lightgreen':
        screen.blit(brick_lightgreen_img, (bricks_x[i], bricks_y[i]))
        
    # effect blok
    for effect in destroy_effects:

    # omhoog bewegen
     effect[1] = effect[1] - 8

    # juiste kleur tekenen
     if effect[2] == 'green':
        screen.blit(brick_green_img, (effect[0], effect[1]))

     elif effect[2] == 'lightgreen':
        screen.blit(brick_lightgreen_img, (effect[0], effect[1]))  

    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')     #einde game
