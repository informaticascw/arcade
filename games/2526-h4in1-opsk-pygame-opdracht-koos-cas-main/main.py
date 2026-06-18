#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280  # maakt de breedte van het scherm 1280 pixels wijd
SCREEN_HEIGHT = 720  # maakt de hoogte van het scherm 720 pixels hoog
BALL_WIDTH = 16  # maakt de breedte van de bal 16 pixels wijd
BALL_HEIGHT = 16  # maakt de hoogte van de bal 16 pixels hoog
PADDLE_WIDTH = 144 # zorgt voor de breedte de paddle 
PADDLE_HEIGHT = 32 # zorgt voor de hoogte van de paddle 
BRICK_WIDHT = 96 # zorgt voor de breedte van het blok
BRICK_HEIGHT = 32 # zorgt voor de hoogte van het blok

ball_x = SCREEN_WIDTH / 2 #de x-positie van de bal in pixels
ball_speed_x = 6 #snelheid van de bal in de x directie per frame

ball_y = SCREEN_HEIGHT - 100
ball_speed_y = 11

paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100


level = 1
score = 0
def load_level(level):
    global bricks_x, bricks_y, brick_health

    if level == 1:
        bricks_x = [
            50,150,250,50,150,250,50,150,250,50,150,250,
            934,1034,1134,934,1034,1134,934,1034,1134,934,1034,1134
        ]

        bricks_y = [
            70,70,70,105,105,105,140,140,140,175,175,175,
            70,70,70,105,105,105,140,140,140,175,175,175
        ]

    elif level == 2:
        bricks_x = [
            350,450,550,650,750,
            400,500,600,700,
            450,550,650,
            500,600,
            550
        ]

        bricks_y = [
            70,70,70,70,70,
            105,105,105,105,
            140,140,140,
            175,175,
            210
]
        

    brick_health = [2] * len(bricks_x)

# define global variables
game_status_msg = "Level 1"

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# keys


#
# read images
achtergrond = pygame.image.load("one piece.jpg").convert()
achtergrond = pygame.transform.scale(
    achtergrond,
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

achtergrond2 = pygame.image.load("one piece 2.jpg").convert()
achtergrond2 = pygame.transform.scale(
    achtergrond2,
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

#Lees spritesheet met alle plaatjes erin
# convert_alpha vergroot de snelheid van blit en houdt transparansie van .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

#maak een leeg plaatje van 64 bij 64 pixels, SRCALPHA supports transparancy
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA) 
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0) 
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imggreen = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imggreen.blit(spritesheet, (0, 0), (0, 130, 384, 128))
brick_imggreen = pygame.transform.scale(brick_imggreen, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgred = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgred.blit(spritesheet, (0, 0), (772, 260, 384, 128))
brick_imgred = pygame.transform.scale(brick_imgred, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgyellow = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgyellow.blit(spritesheet, (0, 0), (386, 390, 384, 128))
brick_imgyellow = pygame.transform.scale(brick_imgyellow, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgorange = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgorange.blit(spritesheet, (0, 0), (772, 0, 384, 128))
brick_imgorange = pygame.transform.scale(brick_imgorange, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgBlueCracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgBlueCracked.blit(spritesheet, (0, 0), (0, 0, 384, 128))
brick_imgBlueCracked = pygame.transform.scale(brick_imgBlueCracked, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgredCracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgredCracked.blit(spritesheet, (0, 0), (772, 130, 384, 128))
brick_imgredCracked = pygame.transform.scale(brick_imgredCracked, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgGreenCracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgGreenCracked.blit(spritesheet, (0, 0), (0, 260, 384, 128))
brick_imgGreenCracked = pygame.transform.scale(brick_imgGreenCracked, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgYellowCracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgYellowCracked.blit(spritesheet, (0, 0), (386, 260, 384, 128))
brick_imgYellowCracked = pygame.transform.scale(brick_imgYellowCracked, (BRICK_WIDHT, BRICK_HEIGHT))

brick_imgOrangeCracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_imgOrangeCracked.blit(spritesheet, (0, 0), (772, 650, 384, 128))
brick_imgOrangeCracked = pygame.transform.scale(brick_imgOrangeCracked, (BRICK_WIDHT, BRICK_HEIGHT))
#


# game loop
#
game_status_msg = "Speel met [A] en [D]"

load_level(level)

print('mygame is running')
running = True
while running:
  # read events
  # move everything
  # handle collisions
  # draw everything
  # wait until next frame
  for event in pygame.event.get():  # read all events
    if event.type == pygame.QUIT:  # GUI is closed
      running = False # end programm
  keys = pygame.key.get_pressed() # read which keys are down
            
  # 
  # move everything
  #

  # move paddle
  if keys[pygame.K_d]: # key d is down
    paddle_x += 10
  if keys[pygame.K_a]: # key a is down
    paddle_x -= 10
  # paddle stop against the edges of screen
  if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH: 
    paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
  if paddle_x < 0:
    paddle_x = 0

  # bal stopt tegen de paddle
  if (ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT):
    ball_y = paddle_y - BALL_HEIGHT
    ball_speed_y = -abs(ball_speed_y)

  #ball stuiterd tegen het blok en het blok breekt

  for i in range(len(bricks_x)):
    if (ball_x + BALL_WIDTH > bricks_x[i] and
        ball_x < bricks_x[i] + BRICK_WIDHT and
        ball_y + BALL_HEIGHT > bricks_y[i] and
        ball_y < bricks_y[i] + BRICK_HEIGHT):

        print("brick touched")

        if ball_speed_y > 0:
            ball_speed_y = -abs(ball_speed_y)
        else:
            ball_speed_y = abs(ball_speed_y)

        brick_health[i] -= 1

        ball_speed_x *= 1.01
        ball_speed_y *= 1.01

        if brick_health[i] == 0:
            score += 100
            bricks_x.pop(i)
            bricks_y.pop(i)
            brick_health.pop(i)

        break

  if len(bricks_x) == 0:

    level += 1

    if level <= 2:

        load_level(level)

        ball_x = SCREEN_WIDTH / 2
        ball_y = SCREEN_HEIGHT - 100

        ball_speed_x = 6
        ball_speed_y = -11

        paddle_x = SCREEN_WIDTH / 2

        game_status_msg = f"Level {level}"

    else:

        ball_speed_x = 0
        ball_speed_y = 0

        game_status_msg = "You have reached the end mate, well done!"
  
  # move ball
  ball_x = ball_x + ball_speed_x
  ball_y = ball_y + ball_speed_y

  # bounce ball against edges of screen
  if ball_x < 0 : # left edge
    ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
  if ball_x + BALL_WIDTH > SCREEN_WIDTH: # right edge
    ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left
    
  if ball_y < 0 : # up edge
    ball_speed_y = abs(ball_speed_y) # positive y-speed = move down


  # 
  # handle collisions
  #
  if ball_y + BALL_HEIGHT >= SCREEN_HEIGHT:
    ball_speed_x = 0
    ball_speed_y = 0
    game_status_msg = "You have drowned, you may try again!" # this comes in screen when the ball is dead
  # draw everything

  # clear screen
  screen.blit(achtergrond, (0, 0))
  if level == 1:
    screen.blit(achtergrond2, (0, 0))
  elif level == 2:
    screen.blit(achtergrond, (0, 0))

  game_status_img = font.render(game_status_msg, True, 'green')
  screen.blit(game_status_img, (0, 0)) # (0, 0) is top left corner of screen
  score_text = font.render(f"Score: {score}", True, (255, 255, 255))
  screen.blit(score_text, (1000, 10))
  # draw ball
  screen.blit(ball_img, (ball_x, ball_y))
  # draw paddle
  screen.blit(paddle_img, (paddle_x, paddle_y))
  #draw brick
 
  for i in range(len(bricks_x)):
    if bricks_y[i] == 70:
      if brick_health[i] == 2:
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))        # blauw
      else:
        screen.blit(brick_imgBlueCracked, (bricks_x[i], bricks_y[i])) # blauw cracked
    elif bricks_y[i] == 105:
      if brick_health[i] == 2:
        screen.blit(brick_imggreen, (bricks_x[i], bricks_y[i]))   # groen
      else:
        screen.blit(brick_imgGreenCracked, (bricks_x[i], bricks_y[i]))  #groen cracked 
    elif bricks_y[i] == 140:
      if brick_health[i] == 2:
        screen.blit(brick_imgyellow, (bricks_x[i], bricks_y[i]))  # geel
      else:
        screen.blit(brick_imgYellowCracked, (bricks_x[i], bricks_y[i]))  # geel cracked
    elif bricks_y[i] == 175:
      if brick_health[i] == 2:
        screen.blit(brick_imgorange, (bricks_x[i], bricks_y[i]))  # oranje
      else:
        screen.blit(brick_imgOrangeCracked, (bricks_x[i], bricks_y[i]))  # oranje
    elif bricks_y[i] == 210:
      if brick_health[i] == 2:
        screen.blit(brick_imgred, (bricks_x[i], bricks_y[i]))  # oranje
      else:
        screen.blit(brick_imgredCracked, (bricks_x[i], bricks_y[i]))  # oranje
 # screen.blit(brick_img, (bricks_x[1], bricks_y[1]))  
 # show screen
  pygame.display.flip() 
# draw game status message
 
     


  # wait until next frame
  #

  fps_clock.tick(FPS) # Sleep the remaining time of this frame

pygame.quit()
print('mygame stopt running')
