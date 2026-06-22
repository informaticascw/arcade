#
# BREAKOUT GAME 
#

import pygame, time
import random
#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 #Screen width
SCREEN_HEIGHT = 720 #Screen height
BALL_WIDTH = 16 #ball width
BALL_HEIGHT = 16 #ball heigth
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
HEART_WIDTH = 32
HEART_HEIGHT = 29

game_status = 0

hit = 1
game_status_msg = "Druk op [X] om singelplayer te starten"
game_status_msg_2 = "Druk op [R] om te restarten"
game_status_msg_3 = "Druk op [C] om twoplayer te kunnen spelen"
tijd_msg = "Tijd = "
levens = 3
levens_2 = 3
score = 0


paddle_x = 640
paddle_y = 620
paddle_x_2 = 640
paddle_y_2 = 60
paddle_speed = 25
paddle_speed_2 = 25

ball_x = paddle_y + (PADDLE_WIDTH/2)#ball location
ball_speed_x = random.choice([-10, 10]) #ball speed

ball_y = paddle_x - BALL_HEIGHT
ball_speed_y = 10

lengte_rij = [7,15,23,31]   #hier kun je makkelijk de lengte van je blok rijen aanpassen 
hoeveel_bricks = 24         #hier kun je makkelijk de hoeveelheid bricks aanpassen
afstand_links = 250         #hier kun je de afstand links van het blokken blok aanpassen
afstand_boven = 100         #hier kun je de afstand boven van het blokken blok aanpassen

brick_hits = [2] * hoeveel_bricks
explosion_time = [-999999999999999999999999999999999999999999999999999999999999999999] * hoeveel_bricks

bricks_x = []
for i in range(0,hoeveel_bricks):
  if i <= lengte_rij[0] :
    loca_brick_x = afstand_links + i * 96
  elif i <= lengte_rij[1] :
    loca_brick_x = afstand_links + (i - (lengte_rij[0] + 1)) * 96
  elif i <= lengte_rij[2] :
    loca_brick_x = afstand_links + (i - (lengte_rij[1] + 1)) * 96
  elif i <= lengte_rij[3] :
    loca_brick_x = afstand_links + (i - (lengte_rij[3] + 1)) * 96
  bricks_x.append(loca_brick_x)
print("x",bricks_x)

bricks_y = []
for i in range(0,hoeveel_bricks):
  if i <= lengte_rij[0] :
    loca_brick_y = afstand_boven
  elif i <= lengte_rij[1] :
    loca_brick_y = afstand_boven + BRICK_HEIGHT
  elif i <= lengte_rij[2] :
    loca_brick_y = afstand_boven + (BRICK_HEIGHT * 2)
  elif i <= lengte_rij[3] :
    loca_brick_y = afstand_boven + (BRICK_HEIGHT * 3)
  bricks_y.append(loca_brick_y)
print("y",bricks_y)

heart_x = [20, 62, 104]
heart_y = [20,20,20]
heart_x_2 = [20, 62, 104]
heart_y_2 = [20,20,20]

explosions_x = []
for i in range(0,hoeveel_bricks):
  if i <= lengte_rij[0] :
    loca_brick_x = afstand_links + i * 96
  elif i <= lengte_rij[1] :
    loca_brick_x = afstand_links + (i - (lengte_rij[0] + 1)) * 96
  elif i <= lengte_rij[2] :
    loca_brick_x = afstand_links + (i - (lengte_rij[1] + 1)) * 96
  elif i <= lengte_rij[3] :
    loca_brick_x = afstand_links + (i - (lengte_rij[3] + 1)) * 96
  explosions_x.append(loca_brick_x)

explosions_y = []
for i in range(0,hoeveel_bricks):
  if i <= lengte_rij[0] :
    loca_brick_y = afstand_boven
  elif i <= lengte_rij[1] :
    loca_brick_y = afstand_boven + BRICK_HEIGHT
  elif i <= lengte_rij[2] :
    loca_brick_y = afstand_boven + (BRICK_HEIGHT * 2)
  elif i <= lengte_rij[3] :
    loca_brick_y = afstand_boven + (BRICK_HEIGHT * 3)
  explosions_y.append(loca_brick_y)

explosions_frame = []

explosion_imgs = []
 
# init game
#

def reset_game():
  global game_status
  global levens
  global paddle_x, paddle_y
  global paddle_speed
  global ball_x, ball_y
  global ball_speed_x, ball_speed_y
  global bricks_x, bricks_y, brick_hits
  global explosion_time
  global score
  global hit
  global hoeveel_bricks
  global lengte_rij
  global afstand_boven, afstand_links
  global explosions_frame, explosion_imgs
  global explosions_x, explosions_y
  global levens_2
  global paddle_x_2, paddle_y_2
  global heart_x, heart_y
  global heart_x_2, heart_y_2
  game_status = 0
  levens = 3

  paddle_x = 640
  paddle_y = 620

  ball_x = paddle_x + (PADDLE_WIDTH / 2) - (BALL_WIDTH / 2)
  ball_y = paddle_y - BALL_HEIGHT

  ball_speed_x = 10
  ball_speed_y = -10
  paddle_speed = 25

  brick_hits = [2] * hoeveel_bricks
  explosion_time = [-9999999999999999999999999999999999999999999999999999999999999999999999999999] * hoeveel_bricks
  score = 0

  hit = 1

  lengte_rij = [7,15,23,31]
  hoeveel_bricks = 24   
  afstand_links = 250   
  afstand_boven = 100 

  levens_2 = 3

  paddle_x_2 = 640
  paddle_y_2 = 60

  heart_x = [20, 62, 104]
  heart_y = [20, 20, 20]

  heart_x_2 = [20, 62, 104]
  heart_y_2 = [20, 20, 20]

  explosions_frame = []

  explosion_imgs = []

  bricks_x = []
  for i in range(0,hoeveel_bricks):
    if i <= lengte_rij[0] :
      loca_brick_x = afstand_links + i * 96
    elif i <= lengte_rij[1] :
      loca_brick_x = afstand_links + (i - (lengte_rij[0] + 1)) * 96
    elif i <= lengte_rij[2] :
      loca_brick_x = afstand_links + (i - (lengte_rij[1] + 1)) * 96
    elif i <= lengte_rij[3] :
      loca_brick_x = afstand_links + (i - (lengte_rij[3] + 1)) * 96
    bricks_x.append(loca_brick_x)
  print("x",bricks_x)

  bricks_y = []
  for i in range(0,hoeveel_bricks):
    if i <= lengte_rij[0] :
      loca_brick_y = afstand_boven
    elif i <= lengte_rij[1] :
      loca_brick_y = afstand_boven + BRICK_HEIGHT
    elif i <= lengte_rij[2] :
      loca_brick_y = afstand_boven + (BRICK_HEIGHT * 2)
    elif i <= lengte_rij[3] :
      loca_brick_y = afstand_boven + (BRICK_HEIGHT * 3)
    bricks_y.append(loca_brick_y)
  print("y",bricks_y)

  explosions_x = []
  for i in range(0,hoeveel_bricks):
    if i <= lengte_rij[0] :
      loca_brick_x = afstand_links + i * 96
    elif i <= lengte_rij[1] :
      loca_brick_x = afstand_links + (i - (lengte_rij[0] + 1)) * 96
    elif i <= lengte_rij[2] :
      loca_brick_x = afstand_links + (i - (lengte_rij[1] + 1)) * 96
    elif i <= lengte_rij[3] :
      loca_brick_x = afstand_links + (i - (lengte_rij[3] + 1)) * 96
    explosions_x.append(loca_brick_x)

  explosions_y = []
  for i in range(0,hoeveel_bricks):
    if i <= lengte_rij[0] :
      loca_brick_y = afstand_boven
    elif i <= lengte_rij[1] :
      loca_brick_y = afstand_boven + BRICK_HEIGHT
    elif i <= lengte_rij[2] :
      loca_brick_y = afstand_boven + (BRICK_HEIGHT * 2)
    elif i <= lengte_rij[3] :
      loca_brick_y = afstand_boven + (BRICK_HEIGHT * 3)
    explosions_y.append(loca_brick_y)





pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 30)
small_font = pygame.font.Font('PressStart2P-Regular.ttf', 15)
mid_font = pygame.font.Font('PressStart2P-Regular.ttf', 22)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# read images
#
#contain images
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   
explosionsheet = pygame.image.load('explosie.png').convert_alpha()

stage_1 = pygame.image.load('pixel_art_1.png').convert_alpha()
stage_1 = pygame.transform.scale(stage_1, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage_2 = pygame.image.load('pixel_art_2.png').convert_alpha()
stage_2 = pygame.transform.scale(stage_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage_3 = pygame.image.load('pixel_art_3.png').convert_alpha()
stage_3 = pygame.transform.scale(stage_3, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage_4 = pygame.image.load('pixel_art_4.png').convert_alpha()
stage_4 = pygame.transform.scale(stage_4, (SCREEN_WIDTH, SCREEN_HEIGHT))

dead_message = pygame.image.load('you lost.png').convert_alpha()
dead_message = pygame.transform.scale(dead_message, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_knop = pygame.image.load('start_knop.png').convert_alpha()
start_knop = pygame.transform.scale(start_knop, (SCREEN_WIDTH, SCREEN_HEIGHT))

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  #create bounce space
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  #resize ball

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))   
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

brokenbrick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
brokenbrick_img.blit(spritesheet, (0, 0), (0, 0, 384, 128))   
brokenbrick_img = pygame.transform.scale(brokenbrick_img, (BRICK_WIDTH, BRICK_HEIGHT))


heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH,HEART_HEIGHT))

explosion_img = pygame.Surface((64,64), pygame.SRCALPHA)
explosion_img.blit(explosionsheet, (0, 0), (0, 0, 64, 64))
explosion_img = pygame.transform.scale(explosion_img, (BRICK_WIDTH,BRICK_WIDTH))

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
    keys = pygame.key.get_pressed() #if button is pressed
            
    # 
    # move everything
    #

    if game_status == 0:
      screen.blit(stage_1)
      game_status_msg = "Druk op [X] om singelplayer te starten"
      game_status_img = mid_font.render(game_status_msg, True, 'red')
      screen.blit(game_status_img, (SCREEN_WIDTH/2 - 400, 100))
      game_status_msg_3 = "Druk op [C] om twoplayer te kunnen spelen"
      game_status_msg_3 = mid_font.render(game_status_msg_3, True, 'red')
      screen.blit(game_status_msg_3, (SCREEN_WIDTH/2 - 440, 200))

      if keys[pygame.K_x] : 
        game_status = 1
        start_tijd = pygame.time.get_ticks()
      if keys[pygame.K_c]:
        game_status = 4
        start_tijd = pygame.time.get_ticks()

    elif game_status == 2:
      screen.blit(stage_4)

      game_status_msg = "Je bent dood"
      game_status_img = font.render(game_status_msg, True, 'yellow')
      screen.blit(game_status_img, (SCREEN_WIDTH/2 - 200, 125))
      
      game_status_msg_2 = "Druk op [R] om te restarten"
      game_status_msg_2 = font.render(game_status_msg_2, True, 'yellow')
      screen.blit(game_status_msg_2, (SCREEN_WIDTH/2 - 400, 250))

      tijd_msg = "Tijd = " + str((eind_tijd - start_tijd)/1000) + "s"
      tijd_msg = font.render(tijd_msg, True, 'yellow')
      screen.blit(tijd_msg, (SCREEN_WIDTH/2 - 170, 300))
      
      if keys[pygame.K_r] : 
        reset_game()
    
    elif game_status == 3:
      
      screen.blit(stage_1)
      game_status_msg = "Je hebt gewonnen"
      game_status_img = font.render(game_status_msg, True, 'red')
      screen.blit(game_status_img, (SCREEN_WIDTH/2 - 260, 100))      
      
      score_msg = "Score = " + str(score)      
      score_msg = mid_font.render(score_msg, True, 'red')
      screen.blit(score_msg, (SCREEN_WIDTH/2 - 145, 150))  

      tijd_msg = "Tijd = " + str((eind_tijd - start_tijd)/1000) + "s"
      tijd_msg = mid_font.render(tijd_msg, True, 'red')
      screen.blit(tijd_msg, (SCREEN_WIDTH/2 - 175, 200))
      
      game_status_msg_2 = "Druk op [R] om te restarten"
      game_status_msg_2 = small_font.render(game_status_msg_2, True, 'yellow')
      screen.blit(game_status_msg_2, (SCREEN_WIDTH/2 - 245, 250))
      if keys[pygame.K_r] : 
        reset_game()

    elif game_status == 1:
    # move ball
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y
      
      if len(bricks_x) == 0:
        game_status = 3
        eind_tijd = pygame.time.get_ticks()
    # bounce ball
      if ball_x < 0 : 
        ball_speed_x = abs(ball_speed_x) 
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 

      if ball_y < 0 :
        ball_speed_y = abs(ball_speed_y)
    
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT and levens > 0:
        ball_x = paddle_x + (PADDLE_WIDTH/2) - (BALL_WIDTH/2)
        ball_y = paddle_y - BALL_HEIGHT
        ball_speed_y = 10
        ball_speed_x = random.choice([-10, 10])
        levens = levens - 1
        print(levens)
    
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT and levens == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status = 2
        eind_tijd = pygame.time.get_ticks()

    
  
    # 
    # handle collisions
    #
      if keys[pygame.K_d] : paddle_x = paddle_x + paddle_speed
      if keys[pygame.K_a] : paddle_x = paddle_x - paddle_speed
    #
    # draw everything
    #
    
      if paddle_x + PADDLE_WIDTH >= SCREEN_WIDTH :
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

      if paddle_x <= 0 :
        paddle_x = 0

      if ( ball_x + BALL_WIDTH > paddle_x and
           ball_x < paddle_x + PADDLE_WIDTH and
           ball_y + BALL_HEIGHT > paddle_y and
           ball_y < paddle_y + PADDLE_HEIGHT) :
        ball_speed_y = -abs(ball_speed_y)
        if ball_speed_x > 0 :
          if abs(ball_speed_x) > 8 :
            if ball_x > paddle_x and ball_x < (paddle_x+(PADDLE_WIDTH/3)) :
              ball_speed_x = ball_speed_x * 0.8
          if abs(ball_speed_x) < 20 :
            if ball_x < (paddle_x + PADDLE_WIDTH) and ball_x > (paddle_x+(PADDLE_WIDTH/3*2)) :
              ball_speed_x = ball_speed_x *1.15
        if ball_speed_x < 0 :
          if abs(ball_speed_x) < 20 :
            if ball_x > paddle_x and ball_x < (paddle_x+(PADDLE_WIDTH/3)) :
              ball_speed_x = ball_speed_x * 1.15
          if abs(ball_speed_x) > 8 :
            if ball_x < (paddle_x + PADDLE_WIDTH) and ball_x > (paddle_x+(PADDLE_WIDTH/3*2)) :
              ball_speed_x = ball_speed_x *0.8

    
      for i in range(len(bricks_x)) :
        explosion_time[i] = explosion_time[i] + 1
        if explosion_time[i] >= 8 :
            bricks_x.pop(i)
            bricks_y.pop(i)
            brick_hits.pop(i)
            explosion_time.pop(i)
            break
          

        if (ball_x + BALL_WIDTH >= bricks_x[i] and
        ball_x <= bricks_x[i] + BRICK_WIDTH and
        ball_y + BALL_HEIGHT >= bricks_y[i] and
        ball_y <= bricks_y[i] + BRICK_HEIGHT) :

          print("bam" + str(hit) + " " + str(i))
          hit = hit + 1

          if ball_speed_y > 0 and ball_y < bricks_y[i] :
            ball_speed_y = -abs(ball_speed_y)

          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y)
    
          elif ball_speed_x > 0 and ball_x < bricks_x[i] :
            ball_speed_x = -abs(ball_speed_x)

          elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH :
            ball_speed_x = abs(ball_speed_x)
        
          brick_hits[i] = brick_hits[i] - 1
          
          if brick_hits[i] == 1:
            score = score + 50
          if brick_hits[i] == 0 :
            score = score + 100
            explosion_time[i] = 0
            if abs(ball_speed_y) < 17.5 :
              ball_speed_y = ball_speed_y * 1.03
          break 
        

    # clear screen
      if levens == 3:
        screen.blit(stage_1, (0, 0))
      elif levens == 2:
        screen.blit(stage_2, (0, 0))
      elif levens == 1:
        screen.blit(stage_3, (0, 0))
      elif levens == 0:
        screen.blit(stage_4, (0, 0)) 

    # draw ball
      screen.blit(ball_img, (ball_x, ball_y))
   
      screen.blit(paddle_img, (paddle_x, paddle_y))

      for i in range(0, len(bricks_x)) :
        if brick_hits[i] == 2 :
          screen.blit(brick_img, (bricks_x[int(i)], bricks_y[int(i)]))
        if brick_hits[i] == 1 :
          screen.blit(brokenbrick_img, (bricks_x[int(i)], bricks_y[int(i)]))
        if brick_hits[i] == 0 :
          screen.blit(explosion_img, (bricks_x[int(i)], (bricks_y[int(i)]- BRICK_HEIGHT/4*3)))

      for i in range(0, (levens)) :
        screen.blit(heart_img, (heart_x[int(i)], heart_y[int(i)]))

      lengte_tijd = (pygame.time.get_ticks() - start_tijd) / 1000    
      tijd_msg = "Tijd = " + str(lengte_tijd) + "s"
      tijd_msg = small_font.render(tijd_msg, True, 'red')
      screen.blit(tijd_msg, (1050, 30))          

      score_msg = "Score = " + str(score)
      score_msg = small_font.render(score_msg, True, 'red')
      screen.blit(score_msg, (800, 30))       

    if game_status == 4:
      screen.blit(stage_1)
      lengte_tijd = (pygame.time.get_ticks() - start_tijd) / 1000    

      paddle_speed = 20
      paddle_speed_2 = 20

      heart_x = [20, 62, 104]
      heart_y = [670,670,670]

      if keys[pygame.K_d] : paddle_x = paddle_x + paddle_speed
      if keys[pygame.K_a] : paddle_x = paddle_x - paddle_speed

      if keys[pygame.K_l] : paddle_x_2 = paddle_x_2 + paddle_speed_2
      if keys[pygame.K_j] : paddle_x_2 = paddle_x_2 - paddle_speed_2

      if paddle_x + PADDLE_WIDTH >= SCREEN_WIDTH :
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

      if paddle_x <= 0 :
        paddle_x = 0

      if paddle_x_2 + PADDLE_WIDTH >= SCREEN_WIDTH :
        paddle_x_2 = SCREEN_WIDTH - PADDLE_WIDTH

      if paddle_x_2 <= 0 :
        paddle_x_2 = 0

      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y

      if ball_x < 0 : 
        ball_speed_x = abs(ball_speed_x)
        ball_speed_x = ball_speed_x * 1.1
        ball_speed_y = ball_speed_y * 1.1

      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 
        ball_speed_x = ball_speed_x * 1.02
        ball_speed_y = ball_speed_y * 1.02

      if ( ball_x + BALL_WIDTH > paddle_x and
           ball_x < paddle_x + PADDLE_WIDTH and
           ball_y + BALL_HEIGHT > paddle_y and
           ball_y < paddle_y + PADDLE_HEIGHT) :
        ball_speed_y = -abs(ball_speed_y)

      if ( ball_x + BALL_WIDTH > paddle_x_2 and
           ball_x < paddle_x_2 + PADDLE_WIDTH and
           ball_y + BALL_HEIGHT > paddle_y_2 and
           ball_y < paddle_y_2 + PADDLE_HEIGHT) :
        ball_speed_y = abs(ball_speed_y)        

        if ball_speed_x > 0 and ball_speed_x > 10:
          if abs(ball_speed_x) > 8 :
            if ball_x > paddle_x and ball_x < (paddle_x+(PADDLE_WIDTH/3)) :
              ball_speed_x = ball_speed_x * 0.8
          if abs(ball_speed_x) < 20 :
            if ball_x < (paddle_x + PADDLE_WIDTH) and ball_x > (paddle_x+(PADDLE_WIDTH/3*2)) :
              ball_speed_x = ball_speed_x *1.15
        if ball_speed_x < 0 and ball_speed_x > 10 :
          if abs(ball_speed_x) < 20 :
            if ball_x > paddle_x and ball_x < (paddle_x+(PADDLE_WIDTH/3)) :
              ball_speed_x = ball_speed_x * 1.15
          if abs(ball_speed_x) > 8 :
            if ball_x < (paddle_x + PADDLE_WIDTH) and ball_x > (paddle_x+(PADDLE_WIDTH/3*2)) :
              ball_speed_x = ball_speed_x *0.8

        if ball_speed_x > 0 and ball_speed_x > 10:
          if abs(ball_speed_x) > 8 :
            if ball_x > paddle_x_2 and ball_x < (paddle_x_2+(PADDLE_WIDTH/3)) :
              ball_speed_x = ball_speed_x * 0.8
          if abs(ball_speed_x) < 20 :
            if ball_x < (paddle_x_2 + PADDLE_WIDTH) and ball_x > (paddle_x_2+(PADDLE_WIDTH/3*2)) :
              ball_speed_x = ball_speed_x *1.15
        if ball_speed_x < 0 and ball_speed_x > 10:
          if abs(ball_speed_x) < 20 :
            if ball_x > paddle_x_2 and ball_x < (paddle_x_2+(PADDLE_WIDTH/3)) :
              ball_speed_x = ball_speed_x * 1.15
          if abs(ball_speed_x) > 8 :
            if ball_x < (paddle_x_2 + PADDLE_WIDTH) and ball_x > (paddle_x_2+(PADDLE_WIDTH/3*2)) :
              ball_speed_x = ball_speed_x *0.8

      if ball_y + BALL_HEIGHT < 0 and levens_2 > 0:
        ball_x = paddle_x_2 + (PADDLE_WIDTH/2) - (BALL_WIDTH/2)
        ball_y = paddle_y_2 + BALL_HEIGHT + PADDLE_HEIGHT
        ball_speed_y = 10
        ball_speed_x = random.choice([-10, 10])
        levens_2 = levens_2 - 1
        print(str(levens_2) + "  player 2")

      if ball_y + BALL_HEIGHT < 0 and levens_2 == 0 :
        ball_speed_x = 0
        ball_speed_y = 0
        game_status = 6
        eind_tijd = pygame.time.get_ticks()

      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT  and levens > 0:
        ball_x = paddle_x + (PADDLE_WIDTH/2) - (BALL_WIDTH/2)
        ball_y = paddle_y - BALL_HEIGHT
        ball_speed_y = -10
        ball_speed_x = random.choice([-10, 10])
        levens = levens - 1
        print(str(levens) + "  player 1")
      
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT and levens == 0 :
        ball_speed_x = 0
        ball_speed_y = 0
        game_status = 5
        eind_tijd = pygame.time.get_ticks()

      tijd_msg = "Tijd = " + str(lengte_tijd) + "s"
      tijd_msg = small_font.render(tijd_msg, True, 'red')
      screen.blit(tijd_msg, (1050, 30))  

      for i in range(0, (levens)) :
        screen.blit(heart_img, (heart_x[int(i)], heart_y[int(i)]))
      for i in range(0, (levens_2)) :
        screen.blit(heart_img, (heart_x_2[int(i)], heart_y_2[int(i)]))
      screen.blit(paddle_img, (paddle_x, paddle_y))
      screen.blit(paddle_img, (paddle_x_2, paddle_y_2))
      screen.blit(ball_img, (ball_x, ball_y))

    if game_status == 5: # player 2 wint
      screen.blit(stage_1)

      game_status_msg = "Player 2 heeft gewonnen"
      game_status_img = font.render(game_status_msg, True, 'yellow')
      screen.blit(game_status_img, (SCREEN_WIDTH/2 - 320, 250))  

      game_status_msg_2 = "Druk op [R] om te restarten"
      game_status_msg_2 = small_font.render(game_status_msg_2, True, 'yellow')
      screen.blit(game_status_msg_2, (SCREEN_WIDTH/2 - 220, 320))

      tijd_msg = "Tijd = " + str((eind_tijd - start_tijd)/1000) + "s"
      tijd_msg = mid_font.render(tijd_msg, True, 'red')
      screen.blit(tijd_msg, (SCREEN_WIDTH/2 - 170, 130))

      if keys[pygame.K_r]:
        reset_game()

    if game_status == 6: # player 1 wint
      screen.blit(stage_1)

      game_status_msg = "Player 1 heeft gewonnen"
      game_status_img = font.render(game_status_msg, True, 'yellow')
      screen.blit(game_status_img, (SCREEN_WIDTH/2 - 320, 250))  

      game_status_msg_2 = "Druk op [R] om te restarten"
      game_status_msg_2 = small_font.render(game_status_msg_2, True, 'yellow')
      screen.blit(game_status_msg_2, (SCREEN_WIDTH/2 - 220, 320))

      tijd_msg = "Tijd = " + str((eind_tijd - start_tijd)/1000) + "s"
      tijd_msg = mid_font.render(tijd_msg, True, 'red')
      screen.blit(tijd_msg, (SCREEN_WIDTH/2 - 170, 130))

      if keys[pygame.K_r]:
        reset_game()

    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
