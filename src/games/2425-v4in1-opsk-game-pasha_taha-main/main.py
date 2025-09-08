#
# BREAKOUT GAME 
#

import pygame, time
import random

#
# definitions 
#

FPS = 30 # Frames Per Second (Hoevaak de code-loop herhaald wordt per seconde)
SCREEN_WIDTH = 1400 # Hoe wijd het scherm is in pixels
SCREEN_HEIGHT = 720 # Hoe hoog het scherm is in pixels
BALL_WIDTH = 16 # Hoeveel pixels wijd de bal is 
BALL_HEIGHT = 16  # Hoeveel pixels hoog de bal is 
PADDLE_WIDTH = 144 # Hoeveel pixels wijd de paddle is 
PADDLE_HEIGHT = 32 # Hoeveel pixels hoog de paddle is
BRICK_WIDTH = 96 # breedte brick
BRICK_HEIGHT = 32 # hoogte brick
POWERUP_WIDTH = 40 # breedte powerup
POWERUP_HEIGHT = 40 # hoogte powerup
BULLET_WIDTH = 16 # Hoeveel pixels wijd de bullet is 
BULLET_HEIGHT = 16 #Hoeveel pixels hoog de bullet is 
MAX_BULLETS = 15 #max aantal bullets
BULLET_SPEED = 10 #snelheid bullet


ball_x = 0 # Postite van bal in pixels
ball_speed_x = 0 # Hoeveel pixels de bal zich verplaatst per frame (Horizontaal)
ball_y = 0 # Postite van bal in pixels
ball_speed_y = 0 # Hoeveel pixels de bal zich verplaatst per frame (Verticaal)

paddle_x = SCREEN_WIDTH / 2 - 72 #positie paddle en bullet
paddle_y = SCREEN_HEIGHT - 100
bullet_x = -100
bullet_y = -100

bullet_count = 20 #kogels
bullets = []

time_played = 0 #klok
second_zero = "" 
minute_zero = "" 
seconds_played = 0 
minutes_played = 0

can_shoot = True #schiet powerup als je R toetst
can_shoot_enabled = False # dat schieten zoizo mogelijk is
powerup_show = True # dat powerup wordt geblit
bricks1 = []
level = 1 # bepaald level
brick_count = 2
powerup_x = 700
powerup_y = 100
powerup = 0 # betekent geen powerup blitten
score_count = 0

game_status_msg = "Speel met [A] en [D]" #game berichten tekst
game_status_msg_copy = "Speel met [A] en [D]"
game_status_msg2 = ""
game_status_msg3 = ""
game_status_msg4 = ""
game_status_msg5 = "level 1"
game_state = 'start'
game_status_msg_powerup = ''

def gameAgain(): # spel opnieuw instellen functie
  global BALL_WIDTH, POWERUP_WIDTH, POWERUP_HEIGHT, powerup_x, powerup_y, powerup
  BALL_WIDTH = 16
  BALL_WIDTH = 16
  POWERUP_WIDTH = 32
  POWERUP_HEIGHT = 32
  powerup_x = 700
  powerup_y = 100
  powerup = 0
  powerup_options = random.randint(0,1)
  
#
# init game
#

pygame.init() # Begint het "echte programma" (hiervoor werden alleen variabelen gedefineerd)
font = pygame.font.SysFont('default', 64)
font_medium = pygame.font.SysFont('default', 41) # wat de lettertype inhoudt (Grootte, lettertype enz. )
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) # Stelt het scherm in (Hoe groot het is e.d.)
fps_clock = pygame.time.Clock() # Klok die de FPS laat tellen 

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() # Zet de spritesheet in de programma

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA) # Maakt de hitbox aan voor de bal 
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))  # Plakt het deel van de spritesheet waar de bal op staat op de hitbox  
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) # Maakt de bal kleiner (Van 64*64 naar 16*16)



bullet_img = pygame.Surface((64, 64), pygame.SRCALPHA) # Maakt de hitbox aan voor de bullet
bullet_img.blit(spritesheet, (0, 0), (772, 850, 64, 64))  # Plakt het deel van de spritesheet waar de bullet op staat op de hitbox  
bullet_img = pygame.transform.scale(bullet_img, (BALL_WIDTH, BALL_HEIGHT))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # Maakt de hitbox aan voor de paddle
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 1401, 460))  # Plakt het deel van de spritesheet waar de paddle op staat op de hitbox  
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # Maakt de paddle kleiner

paddle_img1 = pygame.Surface((243, 64), pygame.SRCALPHA) # Maakt de hitbox aan voor de paddle
paddle_img1.blit(spritesheet, (0, 0), (1158, 528, 1401, 592))  # Plakt het deel van de spritesheet waar de paddle op staat op de hitbox  
paddle_img1 = pygame.transform.scale(paddle_img1, (PADDLE_WIDTH, PADDLE_HEIGHT)) # Maakt de paddle kleiner
#<SubTexture name="51-Breakout-Tiles.png" x="1158" y="528" width="243" height="64"/>

#hetzelfde procedure voor andere sprites

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128)) 
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img1 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img1.blit(spritesheet, (0, 0), (772, 390, 384, 128)) 
brick_img1 = pygame.transform.scale(brick_img1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img1_1 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img1_1.blit(spritesheet, (0, 0), (772, 390, 384, 128)) 
brick_img1_1 = pygame.transform.scale(brick_img1_1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img2 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img2.blit(spritesheet, (0, 0), (0, 130, 384, 128)) 
brick_img2 = pygame.transform.scale(brick_img2, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img2_1 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img2_1.blit(spritesheet, (0, 0), (0, 130, 384, 128)) 
brick_img2_1 = pygame.transform.scale(brick_img2_1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img3 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img3.blit(spritesheet, (0, 0), (0, 0, 384, 128)) 
brick_img3 = pygame.transform.scale(brick_img3, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img3_1 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img3_1.blit(spritesheet, (0, 0), (0, 0, 384, 128)) 
brick_img3_1 = pygame.transform.scale(brick_img3_1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img4 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img4.blit(spritesheet, (0, 0), (0, 260, 384, 128)) 
brick_img4 = pygame.transform.scale(brick_img4, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img5 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img5.blit(spritesheet, (0, 0), (772, 260, 384, 128)) 
brick_img5 = pygame.transform.scale(brick_img5, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img6 = pygame.Surface((384, 128), pygame.SRCALPHA) 
brick_img6.blit(spritesheet, (0, 0), (772, 130, 384, 128)) 
brick_img6 = pygame.transform.scale(brick_img6, (BRICK_WIDTH, BRICK_HEIGHT))

powerup_img = pygame.Surface((128, 128), pygame.SRCALPHA)
powerup_img.blit(spritesheet, (0, 0), (1403, 392, 128, 128))
powerup_img = pygame.transform.scale(powerup_img, (POWERUP_WIDTH, POWERUP_HEIGHT))

#achtergrond plaatjes 

BG_IMAGE = pygame.image.load('RQ03IX.png').convert()
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

START_IMAGE = pygame.image.load('Breakout_OG-logo.jpg').convert()
START_IMAGE = pygame.transform.scale(START_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

START_IMAGE1 = pygame.image.load('Breakout_OG-logo.jpg').convert()
START_IMAGE1 = pygame.transform.scale(START_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

#lijsten (dicts) voor de postite, plaatje en hp van brick


bricks = [
  {'pos': (140, 228), 'img': brick_img, 'health': 2}, {'pos': (140, 260), 'img': brick_img, 'health': 2}, {'pos': (140, 292), 'img': brick_img, 'health': 2}, 
  {'pos': (236, 228), 'img' : brick_img, 'health': 2}, {'pos': (236, 260), 'img': brick_img, 'health': 2}, {'pos': (236, 292), 'img': brick_img, 'health': 2},
  {'pos': (332, 228), 'img' : brick_img, 'health': 2}, {'pos': (332, 260), 'img': brick_img, 'health': 2}, {'pos': (332, 292), 'img': brick_img, 'health': 2},                                  
  {'pos': (1004, 228), 'img' : brick_img, 'health': 2}, {'pos': (1004, 260), 'img': brick_img, 'health': 2}, {'pos': (1004, 292), 'img': brick_img, 'health': 2},
  {'pos': (1100, 228), 'img' : brick_img, 'health': 2}, {'pos': (1100, 260), 'img': brick_img, 'health': 2}, {'pos': (1100, 292), 'img': brick_img, 'health': 2},
  {'pos': (1196, 228), 'img' : brick_img, 'health': 2},  {'pos': (1196, 260), 'img': brick_img, 'health': 2}, {'pos': (1196, 292), 'img': brick_img, 'health': 2},
  {'pos': (140, 324), 'img': brick_img, 'health': 2},
  {'pos': (236, 324), 'img': brick_img, 'health': 2},
  {'pos': (332, 324), 'img': brick_img, 'health': 2},
  {'pos': (1004, 324), 'img': brick_img, 'health': 2},
  {'pos': (1100, 324), 'img': brick_img, 'health': 2},
  {'pos': (1196, 324), 'img': brick_img, 'health': 2},


  ]


bricks_copy = [ {'pos': (140, 228), 'img': brick_img, 'health': 2}, {'pos': (140, 260), 'img': brick_img, 'health': 2}, {'pos': (140, 292), 'img': brick_img, 'health': 2}, 
  {'pos': (236, 228), 'img' : brick_img, 'health': 2}, {'pos': (236, 260), 'img': brick_img, 'health': 2}, {'pos': (236, 292), 'img': brick_img, 'health': 2},
  {'pos': (332, 228), 'img' : brick_img, 'health': 2}, {'pos': (332, 260), 'img': brick_img, 'health': 2}, {'pos': (332, 292), 'img': brick_img, 'health': 2},                                  
  {'pos': (1004, 228), 'img' : brick_img, 'health': 2}, {'pos': (1004, 260), 'img': brick_img, 'health': 2}, {'pos': (1004, 292), 'img': brick_img, 'health': 2},
  {'pos': (1100, 228), 'img' : brick_img, 'health': 2}, {'pos': (1100, 260), 'img': brick_img, 'health': 2}, {'pos': (1100, 292), 'img': brick_img, 'health': 2},
  {'pos': (1196, 228), 'img' : brick_img, 'health': 2},  {'pos': (1196, 260), 'img': brick_img, 'health': 2}, {'pos': (1196, 292), 'img': brick_img, 'health': 2},
  {'pos': (140, 324), 'img': brick_img, 'health': 2},
  {'pos': (236, 324), 'img': brick_img, 'health': 2},
  {'pos': (332, 324), 'img': brick_img, 'health': 2},
  {'pos': (1004, 324), 'img': brick_img, 'health': 2},
  {'pos': (1100, 324), 'img': brick_img, 'health': 2},
  {'pos': (1196, 324), 'img': brick_img, 'health': 2},
  
  ]

bricks1 = [{'pos': (100, 118), 'img' : brick_img2, 'health': 2},
  {'pos': (100, 150), 'img' : brick_img2, 'health': 2},   {'pos': (888, 182), 'img' : brick_img2, 'health': 2}, 
  {'pos': (100, 182), 'img' : brick_img2, 'health': 2},  {'pos': (888, 150), 'img' : brick_img2, 'health': 2},
  {'pos': (100, 214), 'img' : brick_img2, 'health': 2},  {'pos': (888, 118), 'img' : brick_img2, 'health': 2}, 
  {'pos': (100, 246), 'img' : brick_img2, 'health': 2}, {'pos': (792, 118), 'img' : brick_img2, 'health': 2}, 
  {'pos': (196, 246), 'img' : brick_img2, 'health': 2}, {'pos': (696, 118), 'img' : brick_img2, 'health': 2},
  {'pos': (292, 246), 'img' : brick_img2, 'health': 2},  {'pos': (1000, 118), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 118), 'img' : brick_img2, 'health': 2}, {'pos': (1000, 150), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 150), 'img' : brick_img2, 'health': 2}, {'pos': (1000, 182), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 182), 'img' : brick_img2, 'health': 2},   {'pos': (1000, 214), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 214), 'img' : brick_img2, 'health': 2},  {'pos': (1000, 246), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 246), 'img' : brick_img2, 'health': 2}, {'pos': (1096, 246), 'img' : brick_img2, 'health': 2},
  {'pos': (696, 246), 'img' : brick_img2, 'health': 2}, {'pos': (1192, 246), 'img' : brick_img2, 'health': 2},
  {'pos': (792, 246), 'img' : brick_img2, 'health': 2}, 
  {'pos': (888, 246), 'img' : brick_img2, 'health': 2},  
  {'pos': (888, 214), 'img' : brick_img2, 'health': 2},]


bricks_level3 = [
   {'pos': (100, 200), 'img': brick_img5, 'health': 2}, {'pos': (100, 232), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 232), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 232), 'img': brick_img5, 'health': 2}, 
  {'pos': (100, 264), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 264), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 296), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 296), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 328), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 328), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 360), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 360), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 392), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 392), 'img' : brick_img5, 'health': 2}, 
  {'pos': (100, 426), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 424), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 458), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 458), 'img' : brick_img5, 'health': 2}, 
  {'pos': (100, 490), 'img' : brick_img5, 'health': 2}, {'pos': (196, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (700, 350), 'img' : brick_img5, 'health': 2}, {'pos': (292, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (388, 200), 'img' : brick_img5, 'health': 2}, {'pos': (796, 382), 'img' : brick_img5, 'health': 2},
  {'pos': (484, 200), 'img' : brick_img5, 'health': 2}, {'pos': (700, 382), 'img' : brick_img5, 'health': 2},
  {'pos': (580, 200), 'img' : brick_img5, 'health': 2}, {'pos': (796, 350), 'img' : brick_img5, 'health': 2},
  {'pos': (676, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (772, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (868, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (964, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (1060, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (1156, 200), 'img' : brick_img5, 'health': 2},
  
  
  ]
#maakt nieuwe bricks aan
bricks_opnieuw1 = bricks1.copy()
bricks_opnieuw = bricks.copy()

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
    keys = pygame.key.get_pressed() 
            
    # 
    # move everything


    if keys[pygame.K_d] : # key d is down
       paddle_x = paddle_x + 11
    if keys[pygame.K_a] : # key a is down
       paddle_x = paddle_x - 11
    if keys[pygame.K_RIGHT] : # key right is down
       paddle_x = paddle_x + 11
    if keys[pygame.K_LEFT] : # key left is down
       paddle_x = paddle_x - 11
   
    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0 : # linkerkant
      ball_speed_x = abs(ball_speed_x) # omkeren snelheid, dus naar rechts
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: # rechterkant
      ball_speed_x = abs(ball_speed_x) * -1 # omkeren snelheid, dus naar links
    
    if ball_y < 0 : # bovenkant
      ball_speed_y = abs(ball_speed_y) # omkeren snelheid, dus naar boven
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: # onderkant
      ball_speed_y = abs(ball_speed_y) * -1 # omkeren snelheid, dus naar beneden


    # bounce paddle
    if paddle_x < 0:
      paddle_x = 0
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    
    # 
    # handle collisions
    #
    if (ball_x < paddle_x + PADDLE_WIDTH and 
    ball_x + BALL_WIDTH > paddle_x and
    ball_y + BALL_HEIGHT > paddle_y and
    ball_y < paddle_y + PADDLE_HEIGHT) and keys[pygame.K_d] and ball_speed_x < 0:
      ball_speed_y = abs(ball_speed_y)* -1 
      ball_speed_x = abs(ball_speed_x)* 1 

    if (ball_x < paddle_x + PADDLE_WIDTH and 
    ball_x + BALL_WIDTH > paddle_x and
    ball_y + BALL_HEIGHT > paddle_y and
    ball_y < paddle_y + PADDLE_HEIGHT) and keys[pygame.K_a] and ball_speed_x > 0:
      ball_speed_y = abs(ball_speed_y)* 1
      ball_speed_x = abs(ball_speed_x)* -1
      
    
    if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT):
        ball_center = ball_x + BALL_WIDTH / 2
        paddle_center = paddle_x + PADDLE_WIDTH / 2
        distance = ball_center - paddle_center
        ball_speed_x = distance / (PADDLE_WIDTH / 2) * 6 # zorgt ervoor dat de bal soms slomer gaat anders worden sommige levels te moeilijk
        ball_speed_y = abs(ball_speed_y) * -1


#veranderen brick health + powerup locatie (bullets versie)

    for i in reversed(range(len(bricks))):
        brick = bricks[i]
        brick_x, brick_y = brick['pos']

        for bullet in bullets[:]:
           if (bullet['x'] < brick_x + BRICK_WIDTH and # Brick collision 
            bullet['y'] + BALL_HEIGHT > brick_y and
            bullet['y'] < brick_y + BRICK_HEIGHT and
            bullet['x'] + BALL_WIDTH > brick_x):

          
              brick['health'] -= 1 # maakt hp kleiner
              if brick['health'] == 1:
                bullets.remove(bullet)
                brick['img'] = brick_img3  # verandert plaatje
              elif brick['health'] <= 0: 
                bricks.pop(i)
                score_count += 10
                powerup_show = False
                bullets.remove(bullet)
                break
        #veranderen brick health + powerup locatie        
        if (ball_x < brick_x + BRICK_WIDTH and # Brick collision 
            ball_y + BALL_HEIGHT > brick_y and
            ball_y < brick_y + BRICK_HEIGHT and
            ball_x + BALL_WIDTH > brick_x):
              
              print(ball_speed_x)
              print(ball_speed_y)
              print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
              ball_speed_y = abs(ball_speed_y)* -1
              if ball_speed_y > 0 and ball_y + BALL_HEIGHT - ball_speed_y <= brick_y:
                ball_speed_y = -abs(ball_speed_y)
              elif ball_speed_y < 0 and ball_y - ball_speed_y >= brick_y + BRICK_HEIGHT:
                ball_speed_y = abs(ball_speed_y)
              if ball_speed_x > 0 and ball_x <= brick_x:  
                ball_speed_x = -abs(ball_speed_x)  
              elif ball_speed_x < 0 and ball_x + BALL_WIDTH >= brick_x + BRICK_WIDTH:  
                ball_speed_x = abs(ball_speed_x)
              brick['health'] -= 1 # maakt hp kleiner
              if brick['health'] == 1:
                brick['img'] = brick_img3  # verandert plaatje
              elif brick['health'] <= 0: 
                bricks.pop(i)
                score_count += 10
                ball_speed_x = ball_speed_x * 1.05
                ball_speed_y = ball_speed_y * 1.05
                if powerup_show == True:
                    powerup = random.randint(0,1)
                    powerup_show = False
                    powerup_location = random.randint(1,6)
                    if powerup_location == 1:
                      powerup_x = 100
                      powerup_y = 100
                    if powerup_location == 2:
                      powerup_x = 325
                      powerup_y = 240
                    if powerup_location == 3:
                      powerup_x = 410
                      powerup_y = 190
                    if powerup_location == 4:
                      powerup_x = 665
                      powerup_y = 345
                    if powerup_location == 5:
                      powerup_x = 775
                      powerup_y = 100
                    if powerup_location == 6:
                      powerup_x = 910
                      powerup_y = 300
                
              break
    
        if powerup_y + POWERUP_HEIGHT > SCREEN_HEIGHT:
          powerup_show = True

      
      #winscherm-verlies scherm

    if level ==1 and len(bricks) == 0:
       
       ball_speed_x = 0
       ball_speed_y = 0
       game_status_msg4 = 'You won!'
       game_status_msg = ''
       game_status_msg2 = 'klik E om naar level 2 te gaan'
       game_status_msg_powerup = ''
       game_status_msg_copy = ''
       powerup_y = -100
       
       if keys[pygame.K_e]:
        
        
        
        BALL_HEIGHT = 16
        BALL_WIDTH = 16
        ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
        screen.blit(ball_img, (ball_x, ball_y))
        PADDLE_WIDTH = 144
        PADDLE_HEIGHT = 32
        paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
        screen.blit(paddle_img, (paddle_x, paddle_y))
       
        level = 2
        brick_count = 2       
        brick_img3 = brick_img4
        bricks = bricks1
        brick_img == brick_img2_1
        brick_img1 = brick_img2
        
        ball_x = 0
        ball_y = 0
        ball_speed_x = 7
        ball_speed_y = 7
        game_status_msg = 'Speel met [A] en [D]'
        game_status_msg2 = ''
        game_status_msg3 = ''
        game_status_msg4 = ''
        game_status_msg5 = 'level 2'
        game_status_msg_powerup = ''
        game_status_msg_copy = 'Speel met [A] en [D]'
        
        bullets = []

    if level == 2 and len(bricks) == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg4 = 'You won!'
        game_status_msg = ''
        game_status_msg2 = 'klik E om naar level 3 te gaan'
        game_status_msg_powerup = ''
        game_status_msg_copy = ''
        powerup_y = -100
        
        
        if keys[pygame.K_e]:
          
          BALL_HEIGHT = 16
          BALL_WIDTH = 16
          ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
          screen.blit(ball_img, (ball_x, ball_y))
          PADDLE_WIDTH = 144
          PADDLE_HEIGHT = 32
          paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
          screen.blit(paddle_img, (paddle_x, paddle_y))
          powerup = 0
          level = 3
          brick_count = 2       
          brick_img3 = brick_img6
          bricks = bricks_level3
          brick_img = brick_img5
          brick_img1 = brick_img5
          ball_x = 0
          ball_y = 0
          ball_speed_x = 7
          ball_speed_y = 7
          game_status_msg = 'Speel met [A] en [D]'
          game_status_msg2 = ''
          game_status_msg3 = ''
          game_status_msg4 = ''
          game_status_msg5 = 'level 3'
          game_status_msg_powerup = ''
          game_status_msg_copy = 'Speel met [A] en [D]'
          bullets = []
         
#opnieuw na uitspelen
    if level == 3 and len(bricks) == 0:
          ball_speed_x = 0
          ball_speed_y = 0
          game_status_msg4 = 'Je hebt het spel uitgespeeld'
          game_status_msg = ''
          game_status_msg2 = 'klik W om opnieuw te beginnen'
          game_status_msg_powerup = ''
          powerup_y = -100
          if keys[pygame.K_w]:
            level = 1
            
            gameAgain()
            BALL_HEIGHT = 16
            BALL_WIDTH = 16
            ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
            screen.blit(ball_img, (ball_x, ball_y))
            PADDLE_WIDTH = 144
            PADDLE_HEIGHT = 32
            paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
            screen.blit(paddle_img, (paddle_x, paddle_y))         
            powerup = 0
            score_count = 0
            brick_count = 2
            ball_x = 0
            ball_y = 0
            ball_speed_x = 7
            ball_speed_y = 7
            game_status_msg = 'Speel met [A] en [D]'
            game_status_msg2 = ''
            game_status_msg3 = ''
            game_status_msg5 = 'level 1'
            game_status_msg_powerup = ''
            game_status_msg_copy = 'Speel met [A] en [D]'
            brick_img3 = brick_img3_1        
            brick_img1 = brick_img
            brick_img2_1 = brick_img1
            brick_img = brick_img1_1
            bricks = [
   {'pos': (140, 228), 'img': brick_img, 'health': 2}, {'pos': (140, 260), 'img': brick_img, 'health': 2}, {'pos': (140, 292), 'img': brick_img, 'health': 2}, 
  {'pos': (236, 228), 'img' : brick_img, 'health': 2}, {'pos': (236, 260), 'img': brick_img, 'health': 2}, {'pos': (236, 292), 'img': brick_img, 'health': 2},
  {'pos': (332, 228), 'img' : brick_img, 'health': 2}, {'pos': (332, 260), 'img': brick_img, 'health': 2}, {'pos': (332, 292), 'img': brick_img, 'health': 2},                                  
  {'pos': (1004, 228), 'img' : brick_img, 'health': 2}, {'pos': (1004, 260), 'img': brick_img, 'health': 2}, {'pos': (1004, 292), 'img': brick_img, 'health': 2},
  {'pos': (1100, 228), 'img' : brick_img, 'health': 2}, {'pos': (1100, 260), 'img': brick_img, 'health': 2}, {'pos': (1100, 292), 'img': brick_img, 'health': 2},
  {'pos': (1196, 228), 'img' : brick_img, 'health': 2},  {'pos': (1196, 260), 'img': brick_img, 'health': 2}, {'pos': (1196, 292), 'img': brick_img, 'health': 2},
  {'pos': (140, 324), 'img': brick_img, 'health': 2},
  {'pos': (236, 324), 'img': brick_img, 'health': 2},
  {'pos': (332, 324), 'img': brick_img, 'health': 2},
  {'pos': (1004, 324), 'img': brick_img, 'health': 2},
  {'pos': (1100, 324), 'img': brick_img, 'health': 2},
  {'pos': (1196, 324), 'img': brick_img, 'health': 2},
    ]
            bricks1 = [{'pos': (100, 118), 'img' : brick_img2, 'health': 2},
    {'pos': (100, 150), 'img' : brick_img2, 'health': 2},   {'pos': (888, 182), 'img' : brick_img2, 'health': 2}, 
    {'pos': (100, 182), 'img' : brick_img2, 'health': 2},  {'pos': (888, 150), 'img' : brick_img2, 'health': 2},
    {'pos': (100, 214), 'img' : brick_img2, 'health': 2},  {'pos': (888, 118), 'img' : brick_img2, 'health': 2}, 
    {'pos': (100, 246), 'img' : brick_img2, 'health': 2}, {'pos': (792, 118), 'img' : brick_img2, 'health': 2}, 
    {'pos': (196, 246), 'img' : brick_img2, 'health': 2}, {'pos': (696, 118), 'img' : brick_img2, 'health': 2},
    {'pos': (292, 246), 'img' : brick_img2, 'health': 2},  {'pos': (1000, 118), 'img' : brick_img2, 'health': 2},
    {'pos': (600, 118), 'img' : brick_img2, 'health': 2}, {'pos': (1000, 150), 'img' : brick_img2, 'health': 2},
    {'pos': (600, 150), 'img' : brick_img2, 'health': 2}, {'pos': (1000, 182), 'img' : brick_img2, 'health': 2},
    {'pos': (600, 182), 'img' : brick_img2, 'health': 2},   {'pos': (1000, 214), 'img' : brick_img2, 'health': 2},
    {'pos': (600, 214), 'img' : brick_img2, 'health': 2},  {'pos': (1000, 246), 'img' : brick_img2, 'health': 2},
    {'pos': (600, 246), 'img' : brick_img2, 'health': 2}, {'pos': (1096, 246), 'img' : brick_img2, 'health': 2},
    {'pos': (696, 246), 'img' : brick_img2, 'health': 2}, {'pos': (1192, 246), 'img' : brick_img2, 'health': 2},
    {'pos': (792, 246), 'img' : brick_img2, 'health': 2}, 
    {'pos': (888, 246), 'img' : brick_img2, 'health': 2},  
    {'pos': (888, 214), 'img' : brick_img2, 'health': 2},]
            bricks_level3 = [
     {'pos': (100, 200), 'img': brick_img5, 'health': 2}, {'pos': (100, 232), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 232), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 232), 'img': brick_img5, 'health': 2}, 
  {'pos': (100, 264), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 264), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 296), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 296), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 328), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 328), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 360), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 360), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 392), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 392), 'img' : brick_img5, 'health': 2}, 
  {'pos': (100, 426), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 424), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 458), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 458), 'img' : brick_img5, 'health': 2}, 
  {'pos': (100, 490), 'img' : brick_img5, 'health': 2}, {'pos': (196, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (700, 350), 'img' : brick_img5, 'health': 2}, {'pos': (292, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (388, 200), 'img' : brick_img5, 'health': 2}, {'pos': (796, 382), 'img' : brick_img5, 'health': 2},
  {'pos': (484, 200), 'img' : brick_img5, 'health': 2}, {'pos': (700, 382), 'img' : brick_img5, 'health': 2},
  {'pos': (580, 200), 'img' : brick_img5, 'health': 2}, {'pos': (796, 350), 'img' : brick_img5, 'health': 2},
  {'pos': (676, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (772, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (868, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (964, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (1060, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (1156, 200), 'img' : brick_img5, 'health': 2},]
            paddle_img = paddle_img
            bullets = []
            time_played = 0
            seconds_played = 0 
            minutes_played = 0
        # opnieuw als je verloren hebt
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
       ball_speed_x = 0
       ball_speed_y = 0
       game_status_msg3 = "You lost!"
       game_status_msg2 = 'klik W om opnieuw te beginnen'
       game_status_msg = ""
       game_status_msg_powerup = ""
       game_status_msg_copy = ''
       powerup_y = -100
      
       if keys[pygame.K_w]:
          level = 1
          
          gameAgain()
          BALL_HEIGHT = 16
          BALL_WIDTH = 16
          ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
          screen.blit(ball_img, (ball_x, ball_y))
          PADDLE_WIDTH = 144
          PADDLE_HEIGHT = 32
          paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
          screen.blit(paddle_img, (paddle_x, paddle_y))         
          powerup = 0
          score_count = 0
          brick_count = 2
          ball_x = 0
          ball_y = 0
          ball_speed_x = 7
          ball_speed_y = 7
          game_status_msg = 'Speel met [A] en [D]'
          game_status_msg2 = ''
          game_status_msg3 = ''
          game_status_msg5 = 'level 1'
          game_status_msg_powerup = ''
          game_status_msg_copy = 'Speel met [A] en [D]'
          brick_img3 = brick_img3_1        
          brick_img1 = brick_img
          brick_img2_1 = brick_img1
          brick_img = brick_img1_1
          bricks = [
   {'pos': (140, 228), 'img': brick_img, 'health': 2}, {'pos': (140, 260), 'img': brick_img, 'health': 2}, {'pos': (140, 292), 'img': brick_img, 'health': 2}, 
  {'pos': (236, 228), 'img' : brick_img, 'health': 2}, {'pos': (236, 260), 'img': brick_img, 'health': 2}, {'pos': (236, 292), 'img': brick_img, 'health': 2},
  {'pos': (332, 228), 'img' : brick_img, 'health': 2}, {'pos': (332, 260), 'img': brick_img, 'health': 2}, {'pos': (332, 292), 'img': brick_img, 'health': 2},                                  
  {'pos': (1004, 228), 'img' : brick_img, 'health': 2}, {'pos': (1004, 260), 'img': brick_img, 'health': 2}, {'pos': (1004, 292), 'img': brick_img, 'health': 2},
  {'pos': (1100, 228), 'img' : brick_img, 'health': 2}, {'pos': (1100, 260), 'img': brick_img, 'health': 2}, {'pos': (1100, 292), 'img': brick_img, 'health': 2},
  {'pos': (1196, 228), 'img' : brick_img, 'health': 2},  {'pos': (1196, 260), 'img': brick_img, 'health': 2}, {'pos': (1196, 292), 'img': brick_img, 'health': 2},
  {'pos': (140, 324), 'img': brick_img, 'health': 2},
  {'pos': (236, 324), 'img': brick_img, 'health': 2},
  {'pos': (332, 324), 'img': brick_img, 'health': 2},
  {'pos': (1004, 324), 'img': brick_img, 'health': 2},
  {'pos': (1100, 324), 'img': brick_img, 'health': 2},
  {'pos': (1196, 324), 'img': brick_img, 'health': 2},
  ]
          bricks1 = [{'pos': (100, 118), 'img' : brick_img2, 'health': 2},
  {'pos': (100, 150), 'img' : brick_img2, 'health': 2},   {'pos': (888, 182), 'img' : brick_img2, 'health': 2}, 
  {'pos': (100, 182), 'img' : brick_img2, 'health': 2},  {'pos': (888, 150), 'img' : brick_img2, 'health': 2},
  {'pos': (100, 214), 'img' : brick_img2, 'health': 2},  {'pos': (888, 118), 'img' : brick_img2, 'health': 2}, 
  {'pos': (100, 246), 'img' : brick_img2, 'health': 2}, {'pos': (792, 118), 'img' : brick_img2, 'health': 2}, 
  {'pos': (196, 246), 'img' : brick_img2, 'health': 2}, {'pos': (696, 118), 'img' : brick_img2, 'health': 2},
  {'pos': (292, 246), 'img' : brick_img2, 'health': 2},  {'pos': (1000, 118), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 118), 'img' : brick_img2, 'health': 2}, {'pos': (1000, 150), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 150), 'img' : brick_img2, 'health': 2}, {'pos': (1000, 182), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 182), 'img' : brick_img2, 'health': 2},   {'pos': (1000, 214), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 214), 'img' : brick_img2, 'health': 2},  {'pos': (1000, 246), 'img' : brick_img2, 'health': 2},
  {'pos': (600, 246), 'img' : brick_img2, 'health': 2}, {'pos': (1096, 246), 'img' : brick_img2, 'health': 2},
  {'pos': (696, 246), 'img' : brick_img2, 'health': 2}, {'pos': (1192, 246), 'img' : brick_img2, 'health': 2},
  {'pos': (792, 246), 'img' : brick_img2, 'health': 2}, 
  {'pos': (888, 246), 'img' : brick_img2, 'health': 2},  
  {'pos': (888, 214), 'img' : brick_img2, 'health': 2},]
          bricks_level3 = [
     {'pos': (100, 200), 'img': brick_img5, 'health': 2}, {'pos': (100, 232), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 232), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 232), 'img': brick_img5, 'health': 2}, 
  {'pos': (100, 264), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 264), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 296), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 296), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 328), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 328), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 360), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 360), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 392), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 392), 'img' : brick_img5, 'health': 2}, 
  {'pos': (100, 426), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 424), 'img' : brick_img5, 'health': 2},
  {'pos': (100, 458), 'img' : brick_img5, 'health': 2}, {'pos': (1196, 458), 'img' : brick_img5, 'health': 2}, 
  {'pos': (100, 490), 'img' : brick_img5, 'health': 2}, {'pos': (196, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (700, 350), 'img' : brick_img5, 'health': 2}, {'pos': (292, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (388, 200), 'img' : brick_img5, 'health': 2}, {'pos': (796, 382), 'img' : brick_img5, 'health': 2},
  {'pos': (484, 200), 'img' : brick_img5, 'health': 2}, {'pos': (700, 382), 'img' : brick_img5, 'health': 2},
  {'pos': (580, 200), 'img' : brick_img5, 'health': 2}, {'pos': (796, 350), 'img' : brick_img5, 'health': 2},
  {'pos': (676, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (772, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (868, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (964, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (1060, 200), 'img' : brick_img5, 'health': 2},
  {'pos': (1156, 200), 'img' : brick_img5, 'health': 2},]
          paddle_img = paddle_img
          bullets = []
          time_played = 0
          seconds_played = 0 
          minutes_played = 0   
    # 
    # draw everything
    #

    # clear screen
    
    # begin scherm
    if game_state == "start":
       
      screen.blit(START_IMAGE, (0, 0))
      title_text = font.render("Welkom bij Breakout!", True, "white")
      start_text = font.render("Druk op Q om te starten", True, "green")
      screen.blit(title_text, (500, 150))
      screen.blit(start_text, (450, 300))
    
      if keys[pygame.K_q]:
        game_state = "playing" 
        ball_speed_x = 7
        ball_speed_y = 7
        ball_x = 0
        ball_y = 0

    elif game_state == 'playing':

      if seconds_played < 10:
        second_zero = "0" 
      else: 
        second_zero = "" 
      if minutes_played < 10: 
        minute_zero = "0" 
      else:
        minute_zero = "" 
      if game_state == "playing": 
        time_played += (1 / 30) 
        seconds_played = int(time_played) 
      if seconds_played == 60: 
        minutes_played += 1 
        seconds_played = 0 
        time_played = 0 
            
      time_text = str(minute_zero) + str(minutes_played) + ":" + str(second_zero) + str(seconds_played)

#schiet powerup
      if can_shoot_enabled and can_shoot and keys[pygame.K_s] and len(bullets) < MAX_BULLETS:   
        bullet_y = paddle_y
        bullet_x = paddle_x + PADDLE_WIDTH // 2 - BULLET_WIDTH // 2            
        BULLET_WIDTH = 24
        BULLET_HEIGHT = 24
        bullets.append ({'x': bullet_x, 'y': bullet_y, 'width': BULLET_WIDTH, 'height': BULLET_HEIGHT})
        can_shoot = False
        powerup_show = True
     
      if not keys[pygame.K_s] and not can_shoot:
         can_shoot = True

      if len(bullets) == 15:
          game_status_msg_powerup = game_status_msg_copy
          game_status_img_copy = font.render(game_status_msg_copy, True, 'green') # je kan max 1x deze powerup krijgen per level anders worden de levels te makkelijk dus
                                                                                  #de volgende keer dat je die powerup krijgt kan je meer 1 kogel schieten  tot dat je pas bij de volgende level bent
          screen.blit(game_status_img_copy, (0, 0)) # dus na dat je deze powerup 1x heb opgepakt kan je punten krijgen
          can_shoot_enabled = False
          powerup_show = True

     
      
    # draw elements
      screen.blit(BG_IMAGE, (0,0))

      game_status_img = font.render(game_status_msg, True, 'green')
      screen.blit(game_status_img, (0, 0))

      game_status_img_powerup = font.render(game_status_msg_powerup, True, 'green')
      screen.blit(game_status_img_powerup, (0, 0))


      game_status_img2 = font.render(game_status_msg2, True, 'green')
      screen.blit(game_status_img2, (700, 665))

      game_status_img3 = font.render(game_status_msg3, True, 'red')
      screen.blit(game_status_img3, (610, 400))

      game_status_img4 = font.render(game_status_msg4, True, 'blue')
      screen.blit(game_status_img4, (610, 135))

      game_status_img5 = font.render(game_status_msg5, True, 'purple')
      screen.blit(game_status_img5, (610, 20))

      time_count = font_medium.render("Gespeelde tijd: " + time_text, True, "purple") 
      screen.blit(time_count, (10, 85))

      for bullet in bullets[:]: #copy van de lijst om veilig te verwijderen tijdens loop
        bullet['y'] -= BULLET_SPEED  # laat bullet omhoog bewegen
        screen.blit(bullet_img, (bullet['x'], bullet['y']))
          
      score_text = font.render('je score:' + '  ' + str(score_count), True, "white")
      screen.blit(score_text, (1100, 0))    

      screen.blit(paddle_img1, (paddle_x, paddle_y))
      screen.blit(ball_img, (ball_x, ball_y))
     
      screen.blit(paddle_img, (paddle_x, paddle_y))

      for brick in bricks:
        x, y = brick['pos']
        img = brick['img']
        screen.blit(img, (x, y))
#powerup randomizer
      if powerup == 0:
         powerup_show = True  

      if powerup == 1:
            

            if (not (ball_x < powerup_x + POWERUP_WIDTH and # Brick collision 
              ball_y + POWERUP_HEIGHT > powerup_y and
              ball_y < powerup_y + POWERUP_HEIGHT and
              ball_x + BALL_WIDTH > powerup_x)) and ( not (powerup_x + POWERUP_WIDTH > paddle_x and
              powerup_x < paddle_x + PADDLE_WIDTH and
              powerup_y + POWERUP_HEIGHT > paddle_y and
              powerup_y < paddle_y + PADDLE_HEIGHT)):
            
               powerup_y += 3
               screen.blit(powerup_img, (powerup_x, powerup_y))
            if (ball_x < powerup_x + POWERUP_WIDTH and # Brick collision 
              ball_y + POWERUP_HEIGHT > powerup_y and
              ball_y < powerup_y + POWERUP_HEIGHT and
              ball_x + BALL_WIDTH > powerup_x): 
                score_count += 50 # score + 50
                powerup = 0
                powerup_options = random.randint(0,2)
                powerup_show = True
                if powerup_options == 1:
                  game_status_msg_powerup = 'Powerup! Grote bal'
                  game_status_msg = ''
                  BALL_WIDTH = 64
                  BALL_HEIGHT = 64
                  ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
                  powerup_show = True
                if powerup_options == 0:
                    game_status_msg_powerup = 'Powerup! Grote paddle'
                    game_status_msg = ''
                    PADDLE_WIDTH = 288
                    PADDLE_HEIGHT = 64
                    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
                    powerup_show = True
                if powerup_options == 2:
                    game_status_msg_powerup = 'klik [S] om te Schieten!!'
                   
                    game_status_msg = ''
                    powerup_show = True
                    can_shoot_enabled = True


            if (powerup_x + POWERUP_WIDTH > paddle_x and # powerup met paddle collision
                powerup_x < paddle_x + PADDLE_WIDTH and
                powerup_y + POWERUP_HEIGHT > paddle_y and
                powerup_y < paddle_y + PADDLE_HEIGHT):
                score_count += 50
                powerup = 0
                powerup_options = random.randint(0,2)
                powerup_show = True
                if powerup_options == 1:
                  game_status_msg_powerup = 'Powerup! Grote bal'
                  game_status_msg = ''
                  BALL_WIDTH = 64
                  BALL_HEIGHT = 64
                  ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
                  powerup_show = True
                if powerup_options == 0:
                    game_status_msg_powerup = 'Powerup! Grote paddle'
                    game_status_msg = ''
                    PADDLE_WIDTH = 288
                    PADDLE_HEIGHT = 64
                    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
                    powerup_show = True
                if powerup_options == 2:
                    game_status_msg_powerup = 'klik [S] om te Schieten!!'
                   
                    game_status_msg = ''
                    can_shoot_enabled = True
                    powerup_show = True
          
                   
   
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
#gemaakt door Pasha en Taha