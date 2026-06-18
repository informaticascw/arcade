import pygame, time

#
# definitions 
#

FPS = 30

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# bal
BALL_WIDTH = 16
BALL_HEIGHT = 16
ball_x = 0
ball_y = 0
ball_speed_x = 6
ball_speed_y = 6

# plank
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
paddle_speed = 10
MAX_PADDLE_SPEED = 20

# brick 
BRICK_WIDTH = 96 
BRICK_HEIGHT = 32 

# heart
HEART_WIDTH = 57
HEART_HEIGHT = 52

# maximale snelheid
MAX_SPEED = 20

# lijst bricks
level = 0
levels_x = [[
  256+96*7
], [
  256, 256+96, 256+96*2, 256+96*3, 256+96*4, 256+96*5, 256+96*6, 256+96*7,
  256, 256+96, 256+96*2, 256+96*3, 256+96*4, 256+96*5, 256+96*6, 256+96*7,
  256, 256+96, 256+96*2, 256+96*3, 256+96*4, 256+96*5, 256+96*6, 256+96*7,
]]
levels_y = [[
  164
], [
  100, 100, 100, 100, 100, 100, 100, 100,
  132, 132, 132, 132, 132, 132, 132, 132,
  164, 164, 164, 164, 164, 164, 164, 164,
]]
bricks_x = levels_x[level].copy()
bricks_y = levels_y[level].copy()
start_bricks = len(bricks_x)

# define global variables
game_state = "start"
game_paused = False
game_status_msg = "DRUK OP Q OM TE STARTEN"

# score
score = 0

# hp
hp = 3

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
font_big = pygame.font.Font('PressStart2P-Regular.ttf', 50)
font_small = pygame.font.Font('PressStart2P-Regular.ttf', 10)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

# ball image
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

# paddle image
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) 

# brick image 
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128)) 
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

# heart image
heart_img = pygame.Surface((64, 58), pygame.SRCALPHA) 
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58)) 
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

# background image
# background image
background_img = pygame.image.load("black.webp").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#
# game loop
#

print('mygame is running')
running = True
while running:
    #
    # read events
    # 
    for event in pygame.event.get(): # krijg alle events 
        if event.type == pygame.QUIT:  # afsluiten van spel
            running = False 
    keys = pygame.key.get_pressed() # ontvang alle keys
       
    # 
    # move everything
    #
    if game_state == "play":

      # beweeg alleen als het spel niet gepauzeerd is

      if not game_paused:
        # move paddle
        if keys[pygame.K_d]:
          paddle_x = paddle_x + paddle_speed
        if keys[pygame.K_a]:
          paddle_x = paddle_x - paddle_speed

        # paddle tegen muur
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
          paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
        if paddle_x < 0:
          paddle_x = 0

        # move ball
        ball_x = ball_x + ball_speed_x
        ball_y = ball_y + ball_speed_y

        # bounce ball
        if ball_x < 0 : # Bal raakt linker muur
          ball_speed_x = abs(ball_speed_x) 
        if ball_x + BALL_WIDTH > SCREEN_WIDTH: # Bal raakt rechter muur
          ball_speed_x = abs(ball_speed_x) * -1

        if ball_y < 0 : # Bal raakt bovenkant
          ball_speed_y = abs(ball_speed_y) 
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: # Bal raakt onderkant 
          ball_speed_y = abs(ball_speed_y) * -1  

      # verder spelen
      else:
        if keys[pygame.K_q]:
          game_paused = False
          game_status_msg = "Level " + str(level + 1)
          ball_speed_x = abs(ball_speed_y)

      # 
      # handle collisions
      #

      # bal tegen vloer
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        # zet spel op pauze
        game_paused = True

        # bal terug zetten boven 
        ball_x = 0
        ball_y = 0

        # hp omlaag
        hp = hp - 1

        # als alle levens op zijn
        if hp == 0:
          ball_speed_x = 0
          ball_speed_y = 0
          game_status_msg = "SPEL VERLOREN..."
          game_state = "lost"
        else:
          game_status_msg = "-1 LEVEN, DRUK OP Q OM VERDER TE SPELEN"
      
      # spel gewonnen
      if len(bricks_x) == 0 :
        game_paused = True

        # als het spel is gewonnen
        if level == len(levels_x) - 1:
          game_state = "game won"
        else:
          # level gewonnen
          game_state = "won level"


      # bal tegen paddel
      if (
          ball_x + BALL_WIDTH > paddle_x and 
          ball_x < paddle_x + PADDLE_WIDTH and
          ball_y + BALL_HEIGHT > paddle_y and
          ball_y < paddle_y + PADDLE_HEIGHT
        ):
        ball_speed_y = -abs(ball_speed_y)

        # bereken waar de bal de paddle raakt
        ball_center = ball_x + BALL_WIDTH / 2
        paddle_center = paddle_x + PADDLE_WIDTH / 2

        hit_pos = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)

        # geef de bal een richting
        ball_speed_x = hit_pos * 12
      
      # bal tegen brick
      for i in range(0, len(bricks_x)) : 
        if (
          ball_x + BALL_WIDTH > bricks_x[i] and 
          ball_x < bricks_x[i] + BRICK_WIDTH and
          ball_y + BALL_HEIGHT > bricks_y[i] and
          ball_y < bricks_y[i] + BRICK_HEIGHT
        ):
          print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))

          # bal bovenkant brick
          if ball_speed_y > 0 and ball_y < bricks_y[i]:
            ball_speed_y = abs(ball_speed_y) * -1

          # bal onderkant brick
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y)

          # bal rechterkant brick
          elif ball_speed_x > 0 and ball_x < bricks_x[i]:
            ball_speed_x = abs(ball_speed_x) * -1

          # bal onderkant brick
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
            ball_speed_x = abs(ball_speed_x)

          bricks_x.pop(i)  
          bricks_y.pop(i)

          remaining = len(bricks_x)
          factor = 1 + (start_bricks - remaining) * 0.008

          ball_speed_x = ball_speed_x * factor
          ball_speed_y = ball_speed_y * factor
          paddle_speed = paddle_speed * factor

          # maximale snelheid
          if ball_speed_x > MAX_SPEED:
            ball_speed_x = MAX_SPEED
          if ball_speed_x < -MAX_SPEED:
            ball_speed_x = -MAX_SPEED
          
          if ball_speed_y > MAX_SPEED:
            ball_speed_y = MAX_SPEED
          if ball_speed_y < -MAX_SPEED:
            ball_speed_y = -MAX_SPEED
          
          if paddle_speed > MAX_PADDLE_SPEED:
            paddle_speed = MAX_PADDLE_SPEED
            
          score += 100
          break

      if keys[pygame.K_e]:
        if level == len(levels_x) - 1:
          game_state = "game won"
        else:
          game_state = "won level"
          game_status_msg = "Level " + str(level + 1)

      # 
      # draw everything
      #

      # clear screen
      screen.blit(background_img, (0, 0))

      # draw game status message
      game_status_img = font.render(game_status_msg, True, 'green')
      screen.blit(game_status_img, (10, 10)) # (0, 0) is top left corner of screen

      level_skip_img = font_small.render("Klik E om dit level over te slaan", True, "gray")
      screen.blit(level_skip_img, (10, SCREEN_HEIGHT - 30))

      score_img = font.render(f"Score: {score}", True, "white")
      screen.blit(score_img, (10, 50))

      # draw hartjes
      for i in range(0, hp):
        screen.blit(heart_img, ((1280 - 20 - HEART_WIDTH) - i*(HEART_WIDTH+5), 20))

      # draw ball
      if hp > 0:
        screen.blit(ball_img, (ball_x, ball_y))
 
      # draw plank
      screen.blit(paddle_img, (paddle_x, paddle_y))

      # draw brick 
      for i in range(0, len(bricks_x)): 
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))

    elif game_state == "game won":

      screen.blit(background_img, (0, 0)) 

      # speler start spel nieuwe level geladen
      if keys[pygame.K_q]:
        level = 0
        bricks_x = levels_x[level].copy()
        bricks_y = levels_y[level].copy()
        ball_x = 0
        ball_y = 0
        start_bricks = len(bricks_x)
        hp = 3
        game_status_msg = "Level " + str(level + 1)
        game_state = "play"
      
      # teken tekst
      game_status_img = font_big.render("ALLE LEVELS OVERWONNEN", True, 'green')
      restart_img = font.render(f"KLIK Q OM OPNIEUW TE SPELEN OF E OM TE STOPPEN", True, 'gray')
      screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.width / 2), (SCREEN_HEIGHT / 2) - (game_status_img.height / 2) - 20))
      screen.blit(restart_img, ((SCREEN_WIDTH / 2) - (restart_img.width / 2), (SCREEN_HEIGHT / 2) - (restart_img.height / 2) + 40))

    elif game_state == "won level":

      screen.blit(background_img, (0, 0)) 

      # speler start spel nieuwe level geladen
      if keys[pygame.K_q]:
        level += 1
        bricks_x = levels_x[level].copy()
        bricks_y = levels_y[level].copy()
        ball_x = 0
        ball_y = 0
        start_bricks = len(bricks_x)
        hp = 3
        game_status_msg = "Level " + str(level + 1)
        game_state = "play"
      
      # teken tekst
      game_status_img = font_big.render("LEVEL GEHAALD", True, 'green')
      restart_img = font.render(f"Level {level+1} GEHAALD KLIK Q OM VERDER TE SPELEN", True, 'gray')
      screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.width / 2), (SCREEN_HEIGHT / 2) - (game_status_img.height / 2) - 20))
      screen.blit(restart_img, ((SCREEN_WIDTH / 2) - (restart_img.width / 2), (SCREEN_HEIGHT / 2) - (restart_img.height / 2) + 40))

    elif game_state == "lost":
      
      screen.blit(background_img, (0, 0)) 

      # speler start spel
      if keys[pygame.K_q]:
        game_status_msg = "Level " + str(level + 1)
        game_state = "play"
      
      # teken tekst
      game_status_img = font_big.render(game_status_msg, True, 'green')
      restart_img = font.render("DRUK OP Q OM TE HERSTARTEN", True, 'gray')
      screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.width / 2), (SCREEN_HEIGHT / 2) - (game_status_img.height / 2) - 20))
      screen.blit(restart_img, ((SCREEN_WIDTH / 2) - (restart_img.width / 2), (SCREEN_HEIGHT / 2) - (restart_img.height / 2) + 40))

    elif game_state == "start":

      screen.blit(background_img, (0, 0)) 

      # speler start spel
      if keys[pygame.K_q]:
        game_status_msg = "Level " + str(level + 1)
        game_state = "play"
      
      # teken tekst
      game_status_img = font_big.render(game_status_msg, True, 'green')
      screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.width / 2), (SCREEN_HEIGHT / 2) - (game_status_img.height / 2) - 20))
     
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
