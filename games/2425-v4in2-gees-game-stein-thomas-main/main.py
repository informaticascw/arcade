#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#
# define messages
game_status_msg = "" 
game_status_msg2= "" 
game_status_msg3= ""
game_status_msg4= ""
game_status_msg5= ""

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # schermgrootte in x-as in pixels
SCREEN_HEIGHT = 720 # schermgrootte in y-as in pixels
BALL_WIDTH = 16 # grootte van de bal in de breedte
BALL_HEIGHT = 16 # grootte van de bal in de lengte

ball_x = 500 # positie van de bal
ball_speed_x = 10 # snelheid van de bal
ball_speed_x = max(-15, min(ball_speed_x, 15))
ball_y = SCREEN_HEIGHT - 300 #postitie verticaal van bal
ball_speed_y =  10# snelheidbal verticaal
ball_speed_y = max(-15, min(ball_speed_y, 15))

PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
paddle_speed = 15
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100

BRICK_WIDTH = 100
BRICK_HEIGHT = 32
levels = [
    {  # Level 1
        'bricks_x' : [600,660,540,490,710,450,750,420,780,780,420,750,450,710,
                      490,540,660,600,500,700,410,790,330,870,270,930,220,980,
                      980,220,930,270,870,330,790,410,700,500,550,650,550,650,
                      450,750,450,750,350,850,350,850,260,940,260,940,180,1020,
                      180,1020,110,1090,110,1090,50,1140,50,1140],
        'bricks_y' : [50] + [82]*2 + [114]*2 + [146]*2 + [178]*2 + [210]*2 + [242]*2 + 
                     [274]*2 + [306]*2 + [338] + [50]*2 + [82]*2 + [114]*2 + [146]*2 +
                     [178]*2 + [210]*2 + [242]*2 + [274]*2 + [306]*2 + [338]*2 + [18]*2 + 
                     [370]*4 + [18]*2 + [338]*2 + [50]*2 + [306]*2 + [82]*2 + [274]*2 + 
                     [114]*2 + [242]*2 + [146]*2 + [210]*2 + [178]*2   ,        
        'bricks_health': [1] * 66,
    },
    {  # Level 2 
        'bricks_x': [200,300,400,500,600,700,800] + 
                    [250,350,450,550,650,750] * 2 + 
                    [275,375,475,575,675,775] *2 + 
                    [700,800]*2 + [750,850,950]*2 + [800,900]*2,
        'bricks_y': [228] * 7 + [196] * 6 + [260] * 6 + [292] * 6 + [164] * 6 + 
                    [324]*2 +[132]*2 +[356]*3 +[100]*3 +[388]*2 +[68]*2,
        'bricks_health': [2] * 45,
    },
    {  # Level 3 
        'bricks_x': [100,200,300,400,500,600,700,800,900,1000,1100] * 4,
        'bricks_y': [100]*11 + [132]*11 + [164]*11 + [196]*11,
        'bricks_health': [3] * 44,
    }
]

current_level = 0

def load_level(level_num):
    global bricks_x, bricks_y, bricks_health
    bricks_x = levels[level_num]['bricks_x'][:]
    bricks_y = levels[level_num]['bricks_y'][:]
    bricks_health = levels[level_num]['bricks_health'][:]

collision_cooldown = 0
collision_cooldown_max = 1

paused = False



#
# init game
#

pygame.init()
font = pygame.font.SysFont('default', 64) # de font in de game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) # de grote van de scherm als je de game speelt
fps_clock = pygame.time.Clock() # de hoeveelheid fps in de game

#
# read images
#

# lees de spritesheet die alle plaatjes bewaard
# vergroot de snelheid van blit en houd de transparantheid van .png convert_alpha
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() 
# maak een leeg plaatje van 64 x 64 pixels, SRCALPHA ondersteunt transparantheid
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
# kopieer het deel (x-left=1403, y-top=652, width=64, height=64) van de spritesheet naar ball_img op (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
# verander de grootte ball_img van 64 x 64 pixels van BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64)) # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize

brick_img_3 = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
brick_img_3.blit(spritesheet, (0, 0), (772, 390, 384, 128)) # copy part of sheet to image
brick_img_3 = pygame.transform.scale(brick_img_3, (BRICK_WIDTH, BRICK_HEIGHT)) # resize

brick_img_2 = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
brick_img_2.blit(spritesheet, (0, 0), (386, 650, 384, 128)) # copy part of sheet to image
brick_img_2 = pygame.transform.scale(brick_img_2, (BRICK_WIDTH, BRICK_HEIGHT)) # resize

brick_img_1 = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
brick_img_1.blit(spritesheet, (0, 0), (772, 520, 384, 128)) # copy part of sheet to image
brick_img_1 = pygame.transform.scale(brick_img_1, (BRICK_WIDTH, BRICK_HEIGHT)) # resize

background = pygame.image.load("informatica.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#
# game loop
#


#
# handle collisions
#

load_level(current_level)


print('mygame is running') 
running = True
while running:
  if len(bricks_x) > 60 :
       game_status_msg3 = 'press A and D to move paddle'
  else:
       game_status_msg3 = ' '
  
  game_status_msg5 = f"Level {current_level + 1}"

    #
    # read events
    # 
  for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
          running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_c: 
            paused = not paused 
            if paused:
              game_status_msg4 = "Game is paused," \
              " press C to continue."
            else:
              game_status_msg4 = ""

  keys = pygame.key.get_pressed() 

  if not paused:        
    # 
    # move everything
    #
    # move paddle
    if keys[pygame.K_d] :
       paddle_x = paddle_x + paddle_speed

    if keys[pygame.K_a] :
       paddle_x = paddle_x - paddle_speed

    if keys[pygame.K_z]:
        if len(bricks_x) == 0 and current_level < len(levels) - 1:
          current_level += 1
          load_level(current_level)
          game_status_msg2 = f"Je bent bij Level {current_level + 1}, druk op z om te starten"
          if keys[pygame.K_z]:
            game_status_msg2 = ''
            ball_speed_x = 10
            ball_speed_y = 10
            paddle_speed = 15
            paddle_x = SCREEN_WIDTH / 2
            ball_y = SCREEN_HEIGHT - 300
            ball_x = 500

        elif len(bricks_x) == 0 and current_level == len(levels) - 1:
          game_status_msg2 = "Gefeliciteerd. Je hebt alle levels voltooid!"
          ball_speed_x = 0
          ball_speed_y = 0

    if keys[pygame.K_r] :

      load_level(current_level)
      game_status_msg2 = ""

      # Reset ball
      ball_x = 500
      ball_y = SCREEN_HEIGHT - 300
      ball_speed_x = 10
      ball_speed_y = 10

      # Reset paddle
      paddle_x = SCREEN_WIDTH / 2
      paddle_speed = 15

      game_status_msg = ""
      game_status_msg3 = ""
      game_status_msg4 = ""

      collision_cooldown = 0

    # make paddles stop at ends of screen
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if  paddle_x < 0 :
       paddle_x = 0


    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    if collision_cooldown > 0: 
      collision_cooldown -= 1 

    


    # 
    # handle collisions
    #

    # bounce ball
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x) 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1 
      
    if ball_y < 0 : 
      ball_speed_y = abs(ball_speed_y) 
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
      ball_speed_x = 0
      ball_speed_y = 0
      game_status_msg = "You lost! Press R to restart the level"
      
    
    # bounce ball on paddle
    if (ball_x + BALL_WIDTH > paddle_x and
      ball_x < paddle_x + PADDLE_WIDTH and
      ball_y + BALL_HEIGHT > paddle_y and
      ball_y < paddle_y + PADDLE_HEIGHT):
      ball_speed_y = -abs(ball_speed_y)

    # midden
      paddle_center = paddle_x + PADDLE_WIDTH / 2
      ball_center = ball_x + BALL_WIDTH / 2

    # Afstand ball-paddle
      afstand_center = ball_center - paddle_center

    # x-speed
      ball_speed_x = ball_speed_x + (afstand_center / 8) 



    
    
    for i in range(len(bricks_x) -1, -1, -1):
      if (ball_x + BALL_WIDTH > bricks_x[i] and 
        ball_x < bricks_x[i] + BRICK_WIDTH and 
        ball_y + BALL_HEIGHT > bricks_y[i] and 
        ball_y < bricks_y[i] + BRICK_HEIGHT):

        print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))

        # Botsing bovenkant
        if ball_speed_y > 0 and ball_y + BALL_HEIGHT >= bricks_y[i] and ball_y < bricks_y[i]:
            ball_speed_y = -abs(ball_speed_y)
            print("boven")

        # Botsing onderkant
        elif ball_speed_y < 0 and ball_y <= bricks_y[i] + BRICK_HEIGHT and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y)
            print("onder")

        # Botsing linkerzijde
        elif ball_speed_x > 0 and ball_x + BALL_WIDTH >= bricks_x[i] and ball_x < bricks_x[i]:
            ball_speed_x = -abs(ball_speed_x)
            print("links")

        # Botsing rechterzijde
        elif ball_speed_x < 0 and ball_x <= bricks_x[i] + BRICK_WIDTH and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
            ball_speed_x = abs(ball_speed_x)
            print("rechts")
        if collision_cooldown == 0:
           bricks_health[i] -= 1
           collision_cooldown = collision_cooldown_max  # cooldown altijd activeren
           if bricks_health[i] <= 0:
            bricks_x.pop(i)
            bricks_y.pop(i)
            bricks_health.pop(i)
            break


    if len(bricks_x) == 0:
      game_status_msg2 = f"Level {current_level + 1} voltooid! Druk Z voor volgend level."
      ball_speed_x = 0
      ball_speed_y = 0
      paddle_speed = 0
   
   
    # 
    # draw everything
    #

    #draw message
    
    # draw background
    screen.blit(background, (0,0))

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw brick
    for i in range(0,len(bricks_x)) :
      if bricks_health[i] == 3:
       screen.blit(brick_img_3, (bricks_x[i], bricks_y[i]))
      elif bricks_health[i] == 2:
       screen.blit(brick_img_2, (bricks_x[i], bricks_y[i]))
      else:
       screen.blit(brick_img_1, (bricks_x[i], bricks_y[i]))
      


    game_status_img = font.render(game_status_msg, True, 'red')
    game_status_img2 = font.render(game_status_msg2, True, 'green')
    game_status_img3 = font.render(game_status_msg3, True, 'white')
    game_status_img5 = font.render(game_status_msg5, True, 'white')
 
    screen.blit(game_status_img, (SCREEN_WIDTH / 2 - (game_status_img.get_width() / 2), SCREEN_HEIGHT / 2))
    screen.blit(game_status_img2, (SCREEN_WIDTH / 2 - (game_status_img2.get_width() / 2), SCREEN_HEIGHT / 2))
    screen.blit(game_status_img3, (SCREEN_WIDTH / 2 - (game_status_img3.get_width() / 2), 30 ))
    screen.blit(game_status_img5, (0, 0 ))

  game_status_img4 = font.render(game_status_msg4, True, 'white')
  screen.blit(game_status_img4, (SCREEN_WIDTH / 2 - (game_status_img4.get_width() / 2), SCREEN_HEIGHT / 2))
  


    # show screen
  pygame.display.flip() 

    # 
    # wait until next frame
    #

  fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
