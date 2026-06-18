#
# BREAKOUT GAME 
#

import pygame, time, random

#
# definitions 
#

FPS = 50                            # Frames Per Second
SCREEN_WIDTH = 1280                 # Schermbreedte
SCREEN_HEIGHT = 720                 # Schermhoogte
BALL_WIDTH = 16                     # Breedte van de bal
BALL_HEIGHT = 16                    # hoogte van de bal
PADDLE_WIDTH  = 144                 # Breedte van de plank
PADDLE_HEIGHT = 32                  # Hoogte van de plank
BRICK_WIDTH = 96                    # Breedte van de steen
BRICK_HEIGHT = 32                   # Hoogte van de steen
EXPLOSION_WIDTH = 90                # Breedte van de explosie animatie
EXPLOSION_HEIGHT = 90               # Hoogte van de explosie animatie
PARTICLE_WIDTH = 48                 # Breedte van de particle animatie
PARTICLE_HEIGHT = 48                # Hoogte van de particle animatie
STARPOWERUP_WIDTH = 32              # Breedte van de powerup
STARPOWERUP_HEIGHT = 30             # hoogte van de powerup
HIGHSCORE_MULTIPLIER_POWERUP_WIDTH = 25
HIGHSCORE_MULTIPLIER_POWERUP_HEIGHT = 22
HEART_WIDTH = 36                    # Breedte van de hearts
HEART_HEIGHT = 36                   # Hoogte van de hearts
game_status_msg = ""                # Spelmededelingen
TEST_MODE = False                   # Testmodus: paddel volgt de bal
gamePause = False                   # Spel pauzeren door op spatie te drukken
won_counter = 0                     # Counter voor het winnen (zie win loopje)
gameover = False                    # Variabele die bepaald of sommige dingen zoals pauzeren kunnen als het spel geindigd is
ShowMessageForXFunctionRunning = 0  # message fade system (frames)
message_text = ""                   # stored message
message_total_frames = 0            # stored total frames for fade calculations
paddle_fast_counter = 0             # de counter die geupdate wordt voor hoelang de paddle snel moet zijn
c_key_was_pressed = False
t_key_was_pressed = False
r_key_was_pressed = False
highscore_multiplier_counter = 0
highscore_multiplier = 1
playingPong = False
SENSITIVITY = 0.1
MinimumBalsnelheid_x = 6
MinimumBalsnelheid_y = 3.5

def ShowMessageForX(message=None, seconds=None, colour="White"):
  global message_text, message_total_frames, message_colour, ShowMessageForXFunctionRunning
  if message is not None and seconds is not None:
    message_text = message
    message_total_frames = max(0, int(seconds * FPS))
    message_colour = colour
    ShowMessageForXFunctionRunning = message_total_frames
# heartsystem

def CreateLives():
    return [
    {"heart_x":10,"heart_y":10},
    {"heart_x":46,"heart_y":10},
    {"heart_x":82,"heart_y":10},
    {"heart_x":118,"heart_y":10},
    {"heart_x":154,"heart_y":10}
]
def CreateLives2():
  return [
    {"heart_x":SCREEN_WIDTH - 10 - HEART_WIDTH,"heart_y":SCREEN_HEIGHT - 10 - HEART_HEIGHT},
    {"heart_x":SCREEN_WIDTH - 46 - HEART_WIDTH,"heart_y":SCREEN_HEIGHT - 10 - HEART_HEIGHT},
    {"heart_x":SCREEN_WIDTH - 82 - HEART_WIDTH,"heart_y":SCREEN_HEIGHT - 10 - HEART_HEIGHT},
    {"heart_x":SCREEN_WIDTH - 118 - HEART_WIDTH,"heart_y":SCREEN_HEIGHT - 10 - HEART_HEIGHT},
    {"heart_x":SCREEN_WIDTH - 154 - HEART_WIDTH,"heart_y":SCREEN_HEIGHT - 10 - HEART_HEIGHT}
  ]

def RestartGame():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global game_status_msg, gamePause, gameover, paddle_fast, paddle_fast_counter
    global highscore, highscore_multiplier_counter, highscore_multiplier, lives
    global poweruplist, particlelist, ShowMessageForXFunctionRunning, message_text, message_total_frames

    ball_x = random.randint(388,892)
    ball_y = 0
    ball_speed_x = 10
    ball_speed_y = 6
    game_status_msg = ""
    gamePause = False
    gameover = False
    paddle_fast = False
    paddle_fast_counter = 0
    highscore = 0
    highscore_multiplier_counter = 0
    highscore_multiplier = 1
    lives = CreateLives()
    poweruplist = []
    particlelist = []
    ShowMessageForXFunctionRunning = 0  
    message_text = ""                  
    message_total_frames = 0 

    for i in range(len(bricks)):
      bricks[i]["brick_stage"] = 2
      bricks[i]["Explosion"] = 0
      bricks[i]["Explosion_Counter"] = 1

#values
highscore = 0
ball_x = random.randint(388,892)          # horizontale positie van de bal
ball_speed_x = 10                         # horizontale snelheid van de bal
ball_y = 0                                # verticale positie 
ball_speed_y = 6                          # verticale snelheid van de bal
ball_speed_y_pause_cache = 0              # verticale snelheid wordt gecashed zodat hij hetzelfde blijft na unpause
ball_speed_x_pause_cache = 0              # horizontale snelheid wordt gecashed zodat hij hetzelfde blijft na unpause
paddle_x = 568                            # horizontale positie van de plank
paddle_y = 630                            # de verticale positie van de plank 
paddle_speed_x = 10                       # de snelheid van de plank
paddle2_x = 568
paddle2_y = 58 
paddle2_speed_x = 10
particleAnimation = []
poweruplist = []
paddle_fast = False
bricks = [
{
  "brick_name": "brick1",
  "brick_x": 304,
  "brick_y": 82,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick2",
  "brick_x": 880,
  "brick_y": 82,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick3",
  "brick_x": 400,
  "brick_y": 114,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick4",
  "brick_x": 784,
  "brick_y": 114,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick5",
  "brick_x": 304,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick6",
  "brick_x": 400,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick7",
  "brick_x": 496,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick8",
  "brick_x": 592,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick9",
  "brick_x": 688,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick10",
  "brick_x": 784,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick11",
  "brick_x": 880,
  "brick_y": 146,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick12",
  "brick_x": 208,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick13",
  "brick_x": 304,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick14",
  "brick_x": 496,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick15",
  "brick_x": 592,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick16",
  "brick_x": 688,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick17",
  "brick_x": 880,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick18",
  "brick_x": 976,
  "brick_y": 178,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick19",
  "brick_x": 112,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick20",
  "brick_x": 208,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick21",
  "brick_x": 304,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick22",
  "brick_x": 400,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick23",
  "brick_x": 496,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick24",
  "brick_x": 592,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick25",
  "brick_x": 688,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick26",
  "brick_x": 784,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick27",
  "brick_x": 880,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick28",
  "brick_x": 976,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick29",
  "brick_x": 1072,
  "brick_y": 210,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick30",
  "brick_x": 112,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick31",
  "brick_x": 304,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick32",
  "brick_x": 400,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick33",
  "brick_x": 496,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick34",
  "brick_x": 592,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick35",
  "brick_x": 688,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick36",
  "brick_x": 784,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick37",
  "brick_x": 880,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick38",
  "brick_x": 1072,
  "brick_y": 242,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick39",
  "brick_x": 112,
  "brick_y": 274,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick40",
  "brick_x": 304,
  "brick_y": 274,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick41",
  "brick_x": 880,
  "brick_y": 274,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick42",
  "brick_x": 1072,
  "brick_y": 274,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick43",
  "brick_x": 400,
  "brick_y": 306,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick44",
  "brick_x": 496,
  "brick_y": 306,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick45",
  "brick_x": 688,
  "brick_y": 306,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
},
{
  "brick_name": "brick46",
  "brick_x": 784,
  "brick_y": 306,
  "brick_stage": 2,
  "Explosion": 0,
  "Explosion_Counter": 0,
  "has-powerup": random.randint(1, 3)
}
]

particlelist = []

def EdgeBounceAnimation(coordinate, xORy, position):
  if xORy == "y":
    y_particle = coordinate
    
    if position == "left":
      x_particle = -24
   
    elif position == "right":
      x_particle = 1256

  elif xORy == "x":
    x_particle = coordinate
   
    if position == "top":
      y_particle = -24
   
    elif position == "bottom":
      y_particle = 696

  particlelist.append({
    "x": x_particle,
    "y": y_particle,
    "frame" : 1,
    "counter" : 0
  })
 

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)                                              #geeft het font voor de game aan
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)   #de resolutie van het scherm en zet het op fullscreen
fps_clock = pygame.time.Clock()                                                                      # de variabele die bepaald welk frame het nu is

#
# read images
#

menuBackground = pygame.image.load('Game-screen.png').convert_alpha()
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()                                 # Lees de spritesheet afbeelding in en stop hem in de variabele spritesheet
spritesheet_explosions = pygame.image.load('ExplosionSpritesheet.png').convert_alpha()
spritesheet_powerup = pygame.image.load('Star-powerup.png').convert_alpha()
spritesheet_heart = pygame.image.load('Heart.png').convert_alpha()
spritesheet_highscore_multiplier_powerup = pygame.image.load('highscore_multiplier_powerup.png').convert_alpha()

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)                                                      # Maak een nieuwe afbeelding met de naam ball_img
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))                                                   # Kopieer een stukje van de spritesheet naar de bal
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))                                    # De afbeeldingsafmetingen herindelen

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)                                                   # Maak een nieuwe afbeelding met de naam paddle_img
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))                                                # Kopieer een stukje van de spritesheet naar de plank
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))                            # De afbeeldingsafmetingen herindelen

fast_paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)                                                   # Maak een nieuwe afbeelding met de naam paddle_img
fast_paddle_img.blit(spritesheet, (0, 0), (349, 910, 243, 64))                                                # Kopieer een stukje van de spritesheet naar de plank
fast_paddle_img = pygame.transform.scale(fast_paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))           

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)                                                   # Maak een nieuwe afbeelding met de naam brick_img
brick_img.blit(spritesheet, (0,0), (772, 390, 384, 128))                                                  # Kopieer een stukje van de spritesheet naar de steen
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))                                # De afbeeldingsafmetingen herindelen

chipped_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)                                           # Maak een nieuwe afbeelding met de naam chipped_brick_img
chipped_brick_img.blit(spritesheet, (0,0), (0, 0, 384, 128))                                              # Kopieer een stukje van de spritesheet naar de gebroken steen
chipped_brick_img = pygame.transform.scale(chipped_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))                # De afbeeldingsafmetingen herindelen

explosionframe1_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe1_img
explosionframe1_img.blit(spritesheet_explosions, (0, 0), (0, 0, 90, 90))                                          # Kopieer een stukje van de explosie spritesheet naar het eerste frame van de explosie animatie
explosionframe1_img = pygame.transform.scale(explosionframe1_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe2_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe2_img
explosionframe2_img.blit(spritesheet_explosions, (0, 0), (92, 0, 90, 90))                                         # Kopieer een stukje van de explosie spritesheet naar het tweede frame van de explosie animatie
explosionframe2_img = pygame.transform.scale(explosionframe2_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe3_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe3_img
explosionframe3_img.blit(spritesheet_explosions, (0, 0), (184, 0, 90, 90))                                         # Kopieer een stukje van de explosie spritesheet naar het derde frame van de explosie animatie
explosionframe3_img = pygame.transform.scale(explosionframe3_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe4_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe4_img
explosionframe4_img.blit(spritesheet_explosions, (0, 0), (276, 0, 90, 90))                                         # Kopieer een stukje van de explosie spritesheet naar het vierde frame van de explosie animatie
explosionframe4_img = pygame.transform.scale(explosionframe4_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe5_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe5_img
explosionframe5_img.blit(spritesheet_explosions, (0, 0), (368, 0, 90, 90))                                         # Kopieer een stukje van de explosie spritesheet naar het vijfde frame van de explosie animatie
explosionframe5_img = pygame.transform.scale(explosionframe5_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe6_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe6_img
explosionframe6_img.blit(spritesheet_explosions, (0, 0), (0, 92, 90, 90))                                         # Kopieer een stukje van de explosie spritesheet naar het zesde frame van de explosie animatie
explosionframe6_img = pygame.transform.scale(explosionframe6_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe7_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe7_img
explosionframe7_img.blit(spritesheet_explosions, (0, 0), (92, 92, 90, 90))                                        # Kopieer een stukje van de explosie spritesheet naar het zevende frame van de explosie animatie
explosionframe7_img = pygame.transform.scale(explosionframe7_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe8_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe8_img
explosionframe8_img.blit(spritesheet_explosions, (0, 0), (184, 92, 90, 90))                                        # Kopieer een stukje van de explosie spritesheet naar het achtste frame van de explosie animatie
explosionframe8_img = pygame.transform.scale(explosionframe8_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe9_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                     # Maak een nieuwe afbeelding met de naam explosionframe9_img
explosionframe9_img.blit(spritesheet_explosions, (0, 0), (276, 92, 90, 90))                                        # Kopieer een stukje van de explosie spritesheet naar het negende frame van de explosie animatie
explosionframe9_img = pygame.transform.scale(explosionframe9_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))              # De afbeeldingsafmetingen herindelen

explosionframe10_img = pygame.Surface((90, 90), pygame.SRCALPHA)                                                    # Maak een nieuwe afbeelding met de naam explosionframe10_img
explosionframe10_img.blit(spritesheet_explosions, (0, 0), (368, 92, 90, 90))                                       # Kopieer een stukje van de explosie spritesheet naar het tiende frame van de explosie animatie
explosionframe10_img = pygame.transform.scale(explosionframe10_img, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))            # De afbeeldingsafmetingen herindelen

particleframe1_img = pygame.Surface((48, 48), pygame.SRCALPHA)                                                   
particleframe1_img.blit(spritesheet_explosions, (0, 0), (0, 304, 48, 48))                                      
particleframe1_img = pygame.transform.scale(particleframe1_img, (PARTICLE_WIDTH, PARTICLE_HEIGHT))

particleframe2_img = pygame.Surface((48, 48), pygame.SRCALPHA)                                                   
particleframe2_img.blit(spritesheet_explosions, (0, 0), (50, 304, 48, 48))                                      
particleframe2_img = pygame.transform.scale(particleframe2_img, (PARTICLE_WIDTH, PARTICLE_HEIGHT))   

particleframe3_img = pygame.Surface((48, 48), pygame.SRCALPHA)                                                   
particleframe3_img.blit(spritesheet_explosions, (0, 0), (100, 304, 48, 48))                                      
particleframe3_img = pygame.transform.scale(particleframe3_img, (PARTICLE_WIDTH, PARTICLE_HEIGHT))   

particleframe4_img = pygame.Surface((48, 48), pygame.SRCALPHA)                                                   
particleframe4_img.blit(spritesheet_explosions, (0, 0), (150, 304, 48, 48))                                      
particleframe4_img = pygame.transform.scale(particleframe4_img, (PARTICLE_WIDTH, PARTICLE_HEIGHT))   

particleframe5_img = pygame.Surface((48, 48), pygame.SRCALPHA)                                                   
particleframe5_img.blit(spritesheet_explosions, (0, 0), (200, 304, 48, 48))                                      
particleframe5_img = pygame.transform.scale(particleframe5_img, (PARTICLE_WIDTH, PARTICLE_HEIGHT))   

particleframe6_img = pygame.Surface((48, 48), pygame.SRCALPHA)                                                   
particleframe6_img.blit(spritesheet_explosions, (0, 0), (250, 304, 48, 48))                                      
particleframe6_img = pygame.transform.scale(particleframe6_img, (PARTICLE_WIDTH, PARTICLE_HEIGHT))

starpowerup_img = pygame.Surface((32, 30), pygame.SRCALPHA)                                                   
starpowerup_img.blit(spritesheet_powerup, (0, 0), (0, 0, 32, 30))                                      
starpowerup_img = pygame.transform.scale(starpowerup_img, (STARPOWERUP_WIDTH, STARPOWERUP_HEIGHT))

highscore_multiplier_powerup_img = pygame.Surface((25, 22), pygame.SRCALPHA)                                                   
highscore_multiplier_powerup_img.blit(spritesheet_highscore_multiplier_powerup, (0, 0), (0, 0, 25, 22))                                      
highscore_multiplier_powerup_img = pygame.transform.scale(highscore_multiplier_powerup_img, (HIGHSCORE_MULTIPLIER_POWERUP_WIDTH, HIGHSCORE_MULTIPLIER_POWERUP_HEIGHT))

heart_img = pygame.Surface((36, 36), pygame.SRCALPHA)                                                   
heart_img.blit(spritesheet_heart, (0, 0), (0, 0, 36, 36))                                      
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

menuBackground_img = pygame.Surface((1280, 720), pygame.SRCALPHA)                                                   
menuBackground_img.blit(menuBackground, (0, 0), (0, 0, 1280, 720))                                      
menuBackground_img = pygame.transform.scale(menuBackground_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

gameBackground_img = pygame.image.load('Space-background.png').convert()   #background image inbrengen
gameBackground_img = pygame.transform.scale(gameBackground_img, (1280, 720))

#
# Menu Loop
#

gameOnline = True
print('Game Online loop started')
while gameOnline:
  Menu = True
  playingGame = False
  playingPong = False
  r_key_was_pressed = False
  c_key_was_pressed = False
  t_key_was_pressed = False

  print('Menu Initialised')
  while Menu:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    screen.blit(menuBackground_img, (0,0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and not r_key_was_pressed:
      Menu = False
      r_key_was_pressed = True
      playingGame = True                                                                 # de variabele die bepaald of het spel runt
      lives = CreateLives()
    elif keys[pygame.K_c] and not c_key_was_pressed:
      Menu = False
      c_key_was_pressed = True
      playingPong = True
      ball_x = SCREEN_WIDTH / 2 - 120
      ball_y = SCREEN_HEIGHT / 2
      lives = CreateLives()
      lives2 = CreateLives2()
      paddle_x = 568
      paddle2_x = 568
      paddle_fast = False
      paddle_speed_x = 10
    elif not keys[pygame.K_r] or keys[pygame.K_c]:
      r_key_was_pressed = False
      c_key_was_pressed = False

    pygame.display.flip()
    fps_clock.tick(FPS)

  #
  # pong loop
  #
  while playingPong:
    #
    # read events
    #
    return_to_menu = False
    any_keydown = False
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
      if event.type == pygame.KEYDOWN:
        any_keydown = True
        if event.key == pygame.K_q:
          return_to_menu = True

    if return_to_menu:
      RestartGame()
      playingPong = False
      break

    keys = pygame.key.get_pressed()

    game_status_img = font.render(game_status_msg, True, 'Red')               # Maakt van de game status message string een rendered object
    GAME_STATUS_MSG_WIDTH = game_status_img.get_width()                       # Breedte van de spelmededelingen
    GAME_STATUS_MSG_HEIGHT = game_status_img.get_height()                     # Hoogte van de spelmededelingen

    #
    # move everything
    #

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bounce ball
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x)          # Dit zorgt ervoor dat als de x-coördinaat van de bal negatief wordt (wat alleen maar gebeurt als hij aan de linkerkant het einde van het scherm heeft bereikt, omdat ball_x dan 0 is en de ball_speed_x nog steeds negatief is) de snelheid weer positief wordt, wat als resultaat heeft dat de bal terugstuitert
      EdgeBounceAnimation(ball_y, "y", "left")
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1     #dit zorgt ervoor dat als de bal tegen de rechterrand van het scherm komt (op de x-as ) dat de bal van richting omdraait en niet uit het scherm vliegt
      EdgeBounceAnimation(ball_y, "y", "right")
    if ball_y < 0 :
      ball_speed_y = abs(ball_speed_y)
      EdgeBounceAnimation(ball_x, "x", "top")
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
      ball_speed_y = abs(ball_speed_y) * -1
      EdgeBounceAnimation(ball_x, "x", "bottom")
  
    # plank beweging met toetsen
    if gamePause == False:
      if keys[pygame.K_d] :                       # key d
        paddle_x = paddle_x + paddle_speed_x
      if keys[pygame.K_a] :                       # key a
        paddle_x = paddle_x - paddle_speed_x
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  # Dit stopt de plank als hij aan de rechterkant van het scherm komt
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
      if paddle_x < 0:                            # Dit stopt de plank als hij aan de linkerkant van het scherm komt
        paddle_x = 0
      if keys[pygame.K_l] :                       # key l
        paddle2_x = paddle2_x + paddle2_speed_x
      if keys[pygame.K_j] :                       # key j
        paddle2_x = paddle2_x - paddle2_speed_x
      if paddle2_x + PADDLE_WIDTH > SCREEN_WIDTH:  # Dit stopt de tweede plank als hij aan de rechterkant van het scherm komt
        paddle2_x = SCREEN_WIDTH - PADDLE_WIDTH
      if paddle2_x < 0:                            # Dit stopt de tweede plank als hij aan de linkerkant van het scherm komt
        paddle2_x = 0
  
    # debug pause
    if keys[pygame.K_c] and not c_key_was_pressed:
      if gamePause == False:
        gamePause = True
        ball_speed_x_pause_cache = ball_speed_x
        ball_speed_y_pause_cache = ball_speed_y  
        ball_speed_y = 0
        ball_speed_x = 0
        game_status_msg = "Game Paused!"
      elif gamePause == True:
        gamePause = False
        ball_speed_x = ball_speed_x_pause_cache
        ball_speed_y = ball_speed_y_pause_cache
        game_status_msg = ""
    #debug test_mode
    if keys[pygame.K_t] and not t_key_was_pressed:
      if TEST_MODE == False:
        TEST_MODE = True
      elif TEST_MODE == True:
        TEST_MODE = False
    if TEST_MODE == True:
      paddle_x = ball_x - (PADDLE_WIDTH / 2)
      paddle2_x = ball_x - (PADDLE_WIDTH / 2)
    
      #
      # handle collisions
      #

      # Ball-Paddle Collision
    if ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT:     # Dit keert de verticale snelheid van de bal om als hij de paddle raakt, zodat de bal terugstuitert
      ball_speed_y -= paddle_speed_x * SENSITIVITY
      ball_speed_x += paddle_speed_x * SENSITIVITY
      ball_speed_y = abs(ball_speed_y) * -1
    if ball_x + BALL_WIDTH > paddle2_x and ball_x < paddle2_x + PADDLE_WIDTH and ball_y > paddle2_y and ball_y < paddle2_y + PADDLE_HEIGHT:     # Dit keert de verticale snelheid van de bal om als hij de paddle raakt, zodat de bal terugstuitert
      ball_speed_y -= paddle_speed_x * SENSITIVITY
      ball_speed_x += paddle_speed_x * SENSITIVITY
      ball_speed_y = abs(ball_speed_y) 

    # Ball past paddle (lost)
    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
      if len(lives) > 2:
        lives.pop()
        ShowMessageForX("Player One Has " + str(len(lives)) + " Lives Remaining!", 5)
        ball_x = SCREEN_WIDTH / 2 - 120
        ball_y = SCREEN_HEIGHT / 2
        ball_speed_x = 10
        ball_speed_y = 6
      elif len(lives) == 2:
        lives.pop()
        ShowMessageForX("Player One Has " + str(len(lives)) + " Life Remaining!", 5)
        ball_x = SCREEN_WIDTH / 2 - 120
        ball_y = SCREEN_HEIGHT / 2
        ball_speed_x = 10
        ball_speed_y = 6
      elif len(lives) == 1:
        lives.pop()
    
      if len(lives) == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "Player Two Won!"
        gameover = True
        ShowMessageForX("Press Any Key To Return To Menu!", 99999999, "orangered")
    if ball_y < paddle2_y:
      if len(lives2) > 2:
        lives2.pop()
        ShowMessageForX("Player Two Has " + str(len(lives2)) + " Lives Remaining!", 5)
        ball_x = SCREEN_WIDTH / 2 - 120
        ball_y = SCREEN_HEIGHT / 2
        ball_speed_x = 10
        ball_speed_y = 6
      elif len(lives2) == 2:
        lives2.pop()
        ShowMessageForX("Player Two Has " + str(len(lives2)) + " Life Remaining!", 5)
        ball_x = SCREEN_WIDTH / 2 - 120
        ball_y = SCREEN_WIDTH / 2
        ball_speed_x = 10
        ball_speed_y = 6
      elif len(lives2) == 1:
        lives2.pop()
    
      if len(lives2) == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "Player One Won!"
        gameover = True
        ShowMessageForX("Press Any Key To Return To Menu!", 99999999, "orangered")
    
    if any_keydown and game_status_msg in ["Player One Won!", "Player Two Won!"]:
      RestartGame()
      playingPong = False
      break

      # 
      # draw everything
      #

    # clear screen
    screen.blit(gameBackground_img, (0,0))                                                                                                  # Achtergrondkleur                                                                                             # Achtergrondkleur
    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))                                                                                              # Plaatst de bal op het scherm
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))
    screen.blit(pygame.transform.flip(paddle_img, False, True), (paddle2_x, paddle2_y))
    # draw game status message 
    status_x = (SCREEN_WIDTH / 2 - GAME_STATUS_MSG_WIDTH / 2)
    status_y = (SCREEN_HEIGHT / 2 - GAME_STATUS_MSG_HEIGHT / 2)
    screen.blit(game_status_img, (status_x, status_y))     # Plaatst de game status message op het scherm
    if message_text and ShowMessageForXFunctionRunning > 0:
      fade_frames = min(3 * FPS, message_total_frames) if message_total_frames > 0 else 0
      if fade_frames > 0 and ShowMessageForXFunctionRunning <= fade_frames:
        alpha = int(255 * (ShowMessageForXFunctionRunning / fade_frames))
      else:
        alpha = 255

      message_img = font.render(message_text, True, message_colour)
      message_img = message_img.convert_alpha()
      message_img.set_alpha(alpha)
      MSG_W = message_img.get_width()
      MSG_H = message_img.get_height()
      msg_x = (SCREEN_WIDTH / 2 - MSG_W / 2)
      msg_y = status_y + GAME_STATUS_MSG_HEIGHT + 10
      screen.blit(message_img, (msg_x, msg_y))
    #draw hearts
    for i in range(0, len(lives)):
      screen.blit(heart_img, (lives[i]["heart_x"], lives[i]["heart_y"]))
    for i in range(0, len(lives2)):
      screen.blit(heart_img, (lives2[i]["heart_x"], lives2[i]["heart_y"]))
    
    # count down the msg fade
      if ShowMessageForXFunctionRunning > 0:
        ShowMessageForXFunctionRunning = ShowMessageForXFunctionRunning - 1
        if ShowMessageForXFunctionRunning == 0:
          message_text = ""
    
    #animation
    for i in particlelist:

      particle_x = i["x"]
      particle_y = i["y"]

      if i["frame"] == 1 :
        screen.blit(particleframe1_img, (particle_x, particle_y))
      elif i["frame"] == 2 :
        screen.blit(particleframe2_img, (particle_x, particle_y))
      elif i["frame"] == 3 :
        screen.blit(particleframe3_img, (particle_x, particle_y))
      elif i["frame"] == 4 :
        screen.blit(particleframe4_img, (particle_x, particle_y))
      elif i["frame"] == 5 :
        screen.blit(particleframe5_img, (particle_x, particle_y))
      elif i["frame"] == 6 :
        screen.blit(particleframe6_img, (particle_x, particle_y))
      
      i["counter"] += 1
      
      if i["counter"] > 4 :
        i["frame"] += 1
        i["counter"] = 0

      if i["frame"] > 6:
        particlelist.remove(i)
    
    # show screen
    pygame.display.flip() 
    # debug
    t_key_was_pressed = keys[pygame.K_t]
    c_key_was_pressed = keys[pygame.K_c]
    r_key_was_pressed = keys[pygame.K_r]

    fps_clock.tick(FPS) # Sleep the remaining time of this frame                                                                         # regelt de framesnelheid
  #
  # game loop
  #

  print('mygame is running')
  while playingGame:
      #
      # read events
      # 

      return_to_menu = False
      any_keydown = False
      for event in pygame.event.get(): 
          if event.type == pygame.QUIT:  
              pygame.quit()
              raise SystemExit
          if event.type == pygame.KEYDOWN:
              any_keydown = True
              if event.key == pygame.K_q:
                  return_to_menu = True

      if return_to_menu:
          RestartGame()
          playingGame = False
          break

      keys = pygame.key.get_pressed()
      game_status_img = font.render(game_status_msg, True, 'Red')               # Maakt van de game status message string een rendered object
      GAME_STATUS_MSG_WIDTH = game_status_img.get_width()                       # Breedte van de spelmededelingen
      GAME_STATUS_MSG_HEIGHT = game_status_img.get_height()                     # Hoogte van de spelmededelingen

      if paddle_fast == True:
        paddle_speed_x = 20
      else:
        paddle_speed_x = 10
      if paddle_fast_counter == 0:
        paddle_fast = False

      if gamePause == False:
        if abs(ball_speed_x) < MinimumBalsnelheid_x:
          ball_speed_x = MinimumBalsnelheid_x if ball_speed_x >= 0 else -MinimumBalsnelheid_x
        if abs(ball_speed_y) < MinimumBalsnelheid_y:    
          ball_speed_y = MinimumBalsnelheid_y if ball_speed_y >= 0 else -MinimumBalsnelheid_y
            
      # 
      # move everything
      #

      # move ball
      ball_x = ball_x + ball_speed_x # dit zorgt ervoor dat de horizontale positie van de bal veranderd wordt door de balsnelheid door de horizontale balsnelheid erbij op te tellen
      ball_y = ball_y + ball_speed_y # dit zorgt ervoor dat de verticale positie van de bal veranderd wordt door de balsnelheid door de verticale balsnelheid erbij op te tellen

      #move_starpowerup
      if gamePause == False:
        for i in poweruplist:
          i["y"] += 3 #valsnelheid

          if (i["x"] + STARPOWERUP_WIDTH > paddle_x and   #rechterkant van de powerup is groter dan de linkerkant van de paddle
            i["x"] < paddle_x + PADDLE_WIDTH and        #linkerkant van de powerup is kleiner dan de rechterkant van de paddle
            i["y"] + STARPOWERUP_HEIGHT > paddle_y and  #onderkant van de powerup is groter dan de bovenkant van de paddle
            i["y"] < paddle_y + PADDLE_HEIGHT):          #bovenkant van de powerup is groter dan de onderkant van de paddle
            if i["type"] == "speed":
              print("I, am speed")
              if paddle_fast == True:
                ShowMessageForX("Speed Power Up Refreshed!", 3, "mediumturquoise")
              else:
                ShowMessageForX("Speed Power Up Active!", 5, "paleturquoise")
              paddle_fast = True
              paddle_fast_counter = 25 * FPS # counter in seconden * fps
            elif i["type"] == "multiplier":
              print("Test, something something highscore multiplier")
              highscore_multiplier_counter = 25 * FPS
              highscore_multiplier = highscore_multiplier + 0.5
              ShowMessageForX("Highscore Multiplier Active! Multiplier: " + str(highscore_multiplier) + "x", 5, "orange")
            poweruplist.remove(i)
          if i["y"] > SCREEN_HEIGHT:   #verwijderen van powerup als hij van het scherm is 
            poweruplist.remove(i)

      # bounce ball
      if ball_x < 0 : 
        ball_speed_x = abs(ball_speed_x)          # Dit zorgt ervoor dat als de x-coördinaat van de bal negatief wordt (wat alleen maar gebeurt als hij aan de linkerkant het einde van het scherm heeft bereikt, omdat ball_x dan 0 is en de ball_speed_x nog steeds negatief is) de snelheid weer positief wordt, wat als resultaat heeft dat de bal terugstuitert
        EdgeBounceAnimation(ball_y, "y", "left")
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1     #dit zorgt ervoor dat als de bal tegen de rechterrand van het scherm komt (op de x-as ) dat de bal van richting omdraait en niet uit het scherm vliegt
        EdgeBounceAnimation(ball_y, "y", "right")
      if ball_y < 0 :
         ball_speed_y = abs(ball_speed_y)
         EdgeBounceAnimation(ball_x, "x", "top")
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
         ball_speed_y = abs(ball_speed_y) * -1
         EdgeBounceAnimation(ball_x, "x", "bottom")
      # plank beweging met toetsen
      if gamePause == False:
        if keys[pygame.K_d] :                       # key d
          paddle_x = paddle_x + paddle_speed_x
        if keys[pygame.K_a] :                       # key a
          paddle_x = paddle_x - paddle_speed_x
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  # Dit stopt de plank als hij aan de rechterkant van het scherm komt
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
      if paddle_x < 0:                            # Dit stopt de plank als hij aan de linkerkant van het scherm komt
        paddle_x = 0
      # debug restart functie
      if keys[pygame.K_r] and not r_key_was_pressed:
        ball_x = random.randint(388,892)
        ball_y = 0
        ball_speed_x = 10
        ball_speed_y = 6
        game_status_msg = ""
        gamePause = False
        gameover = False
        paddle_fast = False
        paddle_fast_counter = 0
        highscore = 0
        highscore_multiplier_counter = 0
        highscore_multiplier = 1
        lives = CreateLives()
        poweruplist.clear()
      
        for i in range(0,len(bricks)):
          bricks[i]["brick_stage"] = 2
          bricks[i]["Explosion"] = 0
          bricks[i]["Explosion_Counter"] = 1
      
        ShowMessageForX("Game Restarted", 2, "peru")
        print("Game Restarted")                   # zorgt ervoor dat de bloken terugkomen bij gebruiken van de restart functie
      # debug test mode
      if keys[pygame.K_t] and not t_key_was_pressed:
        if TEST_MODE == False:
          TEST_MODE = True
        elif TEST_MODE == True:
          TEST_MODE = False
      if TEST_MODE == True:
          paddle_x = ball_x - (PADDLE_WIDTH / 2)
      # debug pause
      if gameover == False:
       if keys[pygame.K_c] and not c_key_was_pressed:
          if gamePause == False:
            gamePause = True
            ball_speed_x_pause_cache = ball_speed_x
            ball_speed_y_pause_cache = ball_speed_y  
            ball_speed_y = 0
            ball_speed_x = 0
            game_status_msg = "Game Paused!"
          elif gamePause == True:
            gamePause = False
            ball_speed_x = ball_speed_x_pause_cache
            ball_speed_y = ball_speed_y_pause_cache
            game_status_msg = ""

      if gameover and any_keydown:
        RestartGame()
        playingGame = False
        break

      #
      # handle collisions
      #

      # Ball-Paddle Collision
      if ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT:     # Dit keert de verticale snelheid van de bal om als hij de paddle raakt, zodat de bal terugstuitert
        ball_speed_y -= paddle_speed_x * SENSITIVITY
        ball_speed_x += paddle_speed_x * SENSITIVITY
        ball_speed_y = abs(ball_speed_y) * -1
      # Ball-Brick Collision
      for i in range(0,len(bricks)):
        if bricks[i]["brick_stage"] != 0 :
          if ball_x + BALL_WIDTH > bricks[i]["brick_x"] and ball_x < bricks[i]["brick_x"] + BRICK_WIDTH and ball_y + BALL_HEIGHT > bricks[i]["brick_y"] and ball_y < bricks[i]["brick_y"] + BRICK_HEIGHT:
            print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
            if ball_speed_y > 0 and ball_y < bricks[i]["brick_y"]:
              ball_speed_y = abs(ball_speed_y) * -1
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks[i]["brick_y"] + BRICK_HEIGHT:
              ball_speed_y = abs(ball_speed_y)
            elif ball_speed_x > 0 and ball_x < bricks[i]["brick_x"]:
              ball_speed_x = abs(ball_speed_x) * -1
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks[i]["brick_x"] + BRICK_WIDTH:
              ball_speed_x = abs(ball_speed_x)

            bricks[i]["brick_stage"] = bricks[i]["brick_stage"] -1
            if bricks[i]["brick_stage"] == 0 :
              bricks[i]["Explosion"] = 1
              highscore = highscore + 250
              if bricks[i]["has-powerup"] == 1:
                poweruplist.append({
                  "x": bricks[i]["brick_x"],
                  "y": bricks[i]["brick_y"],
                  "type": "speed"
                })

              elif bricks[i]["has-powerup"] == 2:
                poweruplist.append({
                  "x": bricks[i]["brick_x"],
                  "y": bricks[i]["brick_y"],
                  "type": "multiplier"
                })
            break


      # Ball past paddle (lost)
      if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
        if len(lives) > 2:
            lives.pop()
            ShowMessageForX(str(len(lives)) + " Lives Remaining!", 5)
            ball_x = random.randint(388, 892)
            ball_y = 0
            ball_speed_x = 10
            ball_speed_y = 6
        elif len(lives) == 2:
          lives.pop()
          ShowMessageForX(str(len(lives)) + " Life Remaining!", 5)
          ball_x = random.randint(388, 892)
          ball_y = 0
          ball_speed_x = 10
          ball_speed_y = 6
        elif len(lives) == 1:
          lives.pop()
    
        if len(lives) == 0:
            ball_speed_x = 0
            ball_speed_y = 0
            game_status_msg = "You lost!"
            gameover = True
            ShowMessageForX("Press Any Key To Return To Menu!", 99999999, "orangered")

      # Won
      for i in range(0,len(bricks)):
        if bricks[i]["brick_stage"] == 0:
          won_counter = won_counter + 1
      if won_counter == len(bricks):
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "You Won!"
        won_counter = 0
        gameover = True
        ShowMessageForX("Press Any Key To Return To Menu!", 99999999, "orangered")
      else:
        won_counter = 0

      # 
      # draw everything
      #

      # clear screen
      screen.blit(gameBackground_img, ( 0,0))                                                                                                 # Achtergrondkleur                                                                                             # Achtergrondkleur
    
      # draw ball
      screen.blit(ball_img, (ball_x, ball_y))                                                                                              # Plaatst de bal op het scherm
      # draw paddle
      if not paddle_fast:
        screen.blit(paddle_img, (paddle_x, paddle_y))
      elif paddle_fast:
        screen.blit(fast_paddle_img, (paddle_x, paddle_y))
      # draw starpowerup
      for i in poweruplist :
        if i["type"] == "speed":
          screen.blit(starpowerup_img, (i["x"], i["y"]))
        elif i["type"] == "multiplier":
          screen.blit(highscore_multiplier_powerup_img, (i["x"], i["y"]))                                                                             # Plaatst de paddle op het scherm
      # draw bricks
      for i in range(0,len(bricks)):
        brick_x = bricks[i]["brick_x"]
        brick_y = bricks[i]["brick_y"]
        chipped_brick_x = bricks[i]["brick_x"]
        chipped_brick_y = bricks[i]["brick_y"]
        if bricks[i]["brick_stage"] == 2 :
          screen.blit(brick_img, (brick_x, brick_y))   
        elif bricks[i]["brick_stage"] == 1 : 
          screen.blit(chipped_brick_img, (chipped_brick_x, chipped_brick_y))                                                               # Plaats de steen op het scherm
      # draw game status message 
      status_x = (SCREEN_WIDTH / 2 - GAME_STATUS_MSG_WIDTH / 2)
      status_y = (SCREEN_HEIGHT / 2 - GAME_STATUS_MSG_HEIGHT / 2)
      screen.blit(game_status_img, (status_x, status_y))     # Plaatst de game status message op het scherm
      # draw highscore
      if gameover == True:
        highscore_end_img = font.render(("Highscore: " + str(int(highscore))), True, "yellow")
        highscore_x = (SCREEN_WIDTH / 2 - (highscore_end_img.get_width() / 2))
        highscore_y = status_y - 15 - highscore_end_img.get_height()
        screen.blit(highscore_end_img, (highscore_x, highscore_y))
      # draw timed message centered underneath the game status, with a 3s fade
      if message_text and ShowMessageForXFunctionRunning > 0:
        fade_frames = min(3 * FPS, message_total_frames) if message_total_frames > 0 else 0
        if fade_frames > 0 and ShowMessageForXFunctionRunning <= fade_frames:
          alpha = int(255 * (ShowMessageForXFunctionRunning / fade_frames))
        else:
          alpha = 255

        message_img = font.render(message_text, True, message_colour)
        message_img = message_img.convert_alpha()
        message_img.set_alpha(alpha)
        MSG_W = message_img.get_width()
        MSG_H = message_img.get_height()
        msg_x = (SCREEN_WIDTH / 2 - MSG_W / 2)
        msg_y = status_y + GAME_STATUS_MSG_HEIGHT + 10
        screen.blit(message_img, (msg_x, msg_y))
      # Animation
      for i in range(0,len(bricks)):
        explosion_x = bricks[i]["brick_x"] + 3
        explosion_y = bricks[i]["brick_y"] - 27
        if bricks[i]["Explosion"] == 1 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay") 
          screen.blit(explosionframe1_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 1 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 2
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe2_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 2 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay2") 
          screen.blit(explosionframe2_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 2 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 3
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe3_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 3 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay3") 
          screen.blit(explosionframe3_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 3 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 4
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe4_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 4 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay4") 
          screen.blit(explosionframe4_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 4 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 5
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe5_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 5 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay5") 
          screen.blit(explosionframe5_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 5 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 6
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe6_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 6 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay6") 
          screen.blit(explosionframe6_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 6 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 7
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe7_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 7 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay7") 
          screen.blit(explosionframe7_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 7 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 8
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe8_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 8 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay8") 
          screen.blit(explosionframe8_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 8 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 9
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe9_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 9 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay9") 
          screen.blit(explosionframe9_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 9 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 10
          bricks[i]["Explosion_Counter"] = 1
          screen.blit(explosionframe10_img, (explosion_x, explosion_y))
        elif bricks[i]["Explosion"] == 10 and bricks[i]["Explosion_Counter"] != 6:
          print("Yay10") 
          screen.blit(explosionframe10_img, (explosion_x, explosion_y))
          bricks[i]["Explosion_Counter"] = bricks[i]["Explosion_Counter"] + 1
        elif bricks[i]["Explosion"] == 10 and bricks[i]["Explosion_Counter"] == 6:
          bricks[i]["Explosion"] = 0
          bricks[i]["Explosion_Counter"] = 1
  
      #draw particle animation
      for i in particlelist:

        particle_x = i["x"]
        particle_y = i["y"]

        if i["frame"] == 1 :
          screen.blit(particleframe1_img, (particle_x, particle_y))
        elif i["frame"] == 2 :
          screen.blit(particleframe2_img, (particle_x, particle_y))
        elif i["frame"] == 3 :
          screen.blit(particleframe3_img, (particle_x, particle_y))
        elif i["frame"] == 4 :
          screen.blit(particleframe4_img, (particle_x, particle_y))
        elif i["frame"] == 5 :
          screen.blit(particleframe5_img, (particle_x, particle_y))
        elif i["frame"] == 6 :
          screen.blit(particleframe6_img, (particle_x, particle_y))
      
        i["counter"] += 1
      
        if i["counter"] > 4 :
          i["frame"] += 1
          i["counter"] = 0

        if i["frame"] > 6:
          particlelist.remove(i)

      #draw hearts
      for i in range(0, len(lives)):
        screen.blit(heart_img, (lives[i]["heart_x"], lives[i]["heart_y"]))
    
      # count down the msg fade
      if ShowMessageForXFunctionRunning > 0:
        ShowMessageForXFunctionRunning = ShowMessageForXFunctionRunning - 1
        if ShowMessageForXFunctionRunning == 0:
          message_text = ""

      # powerup countdown speed
      if gameover == False:
       if gamePause == False:
         paddle_fast_counter = paddle_fast_counter - 1
         highscore_multiplier_counter = highscore_multiplier_counter - 1
      if highscore_multiplier_counter == 0:
        highscore_multiplier = 1
      # draw paddle fast counter
      if paddle_fast_counter > 0:
        paddle_fast_counter_placeholder = [0] * 4
        paddle_fast_counter_FINAL = ""
        paddle_fast_counter_scorified = str(int(paddle_fast_counter))
        for i in range(len(paddle_fast_counter_scorified)):
          paddle_fast_counter_placeholder.pop()
        for digit in paddle_fast_counter_scorified:
          paddle_fast_counter_placeholder.append(digit)
        for i in paddle_fast_counter_placeholder:
          paddle_fast_counter_FINAL = paddle_fast_counter_FINAL + str(i)
        paddle_fast_counter_img = font.render(paddle_fast_counter_FINAL, True, "mediumturquoise")
        screen.blit(paddle_fast_counter_img, (900, 10))
      # draw highscore multiplier counter
      if highscore_multiplier_counter > 0:
        highscore_multiplier_counter_placeholder = [0] * 4
        highscore_multiplier_counter_FINAL = ""
        highscore_multiplier_counter_scorified = str(int(highscore_multiplier_counter))
        for i in range(len(highscore_multiplier_counter_scorified)):
          highscore_multiplier_counter_placeholder.pop()
        for digit in highscore_multiplier_counter_scorified:
          highscore_multiplier_counter_placeholder.append(digit)
        for i in highscore_multiplier_counter_placeholder:
          highscore_multiplier_counter_FINAL = highscore_multiplier_counter_FINAL + str(i)
        highscore_multiplier_counter_img = font.render(highscore_multiplier_counter_FINAL, True, "darkgoldenrod")
        if paddle_fast_counter > 0:
          screen.blit(highscore_multiplier_counter_img, (780, 10))
        else:
          screen.blit(highscore_multiplier_counter_img, (900, 10))
      #draw highscore
      highscore_scoreFINAL = ""
      highscore_placeholder = [0] * 10
      if gamePause == False and gameover == False:
        highscore = highscore + 0.5 * highscore_multiplier
      highscore_scoreified = str(int(highscore))

      for i in range(len(highscore_scoreified)):
        highscore_placeholder.pop()

      for digit in highscore_scoreified:
        highscore_placeholder.append(digit)

      for i in highscore_placeholder:
        highscore_scoreFINAL = highscore_scoreFINAL + str(i)

      highscore_img = font.render(highscore_scoreFINAL, True, 'Yellow')
      screen.blit(highscore_img, (1030, 10))
      # show screen
      pygame.display.flip() 

      # debug
      t_key_was_pressed = keys[pygame.K_t]
      c_key_was_pressed = keys[pygame.K_c]
      r_key_was_pressed = keys[pygame.K_r]

      # 
      # wait until next frame
      #

      fps_clock.tick(FPS) # Sleep the remaining time of this frame                                                                         # regelt de framesnelheid

  print('mygame stopt running')                                                                                                            # Einde van het spel