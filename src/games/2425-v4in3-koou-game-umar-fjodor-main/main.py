#
# BREAKOUT GAME 
#
# Gemaakt door: Fjodor en Umar

import pygame, time
import random # informatie over random: https://www.w3schools.com/python/module_random.asp

#
# define constants: deze constanten veranderen niet tijdens het spel.
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1350 # Scherm breedte 
SCREEN_HEIGHT = 720 # Scherm hoogte
BALL_WIDTH = 16 # Bal breedte
BALL_HEIGHT = 16 # Bal hoogte
PADDLE_WIDTH = 144 # Plank breedte
PADDLE_HEIGHT = 32 # Plank hoogte
BRICK_WIDTH = 96 # Brick breedte
BRICK_HEIGHT = 32 # Brick hoogte

#
# define global variables: deze variabelen kunnen veranderen tijdens het spel.
#

# variabelen van de bal
balls_x = [0] 
balls_y = [0]
balls_speed_x = [6]
balls_speed_y = [6]
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
paddle2_x = SCREEN_WIDTH / 2
paddle2_y = SCREEN_HEIGHT - 200

# levels, de coordinaten en kleuren
level1_x = [100, 196, 292, 388, 484,
            100, 196, 292, 388, 484, 
            100, 196, 292, 388, 484, 
            100, 196, 292, 388, 484, 
            100, 196, 292, 388, 484,

            1154, 1058, 962, 866, 770, 
            1154, 1058, 962, 866, 770, 
            1154, 1058, 962, 866, 770, 
            1154, 1058, 962, 866, 770, 
            1154, 1058, 962, 866, 770]

level1_y = [100, 100, 100, 100, 100, 
            132, 132, 132, 132, 132, 
            164, 164, 164, 164, 164, 
            196, 196, 196, 196, 196,
            228, 228, 228, 228, 228, 

            100, 100, 100, 100, 100, 
            132, 132, 132, 132, 132, 
            164, 164, 164, 164, 164, 
            196, 196, 196, 196, 196,
            228, 228, 228, 228, 228]

level2_x = [627,
            579, 675,
            483, 579, 675, 771,
            291, 387, 483, 579, 675, 771, 867, 963, 
            291, 387, 483, 579, 675, 771, 867, 963, 
            387, 483, 579, 675, 771, 867,
            483, 579, 675, 771,
            387, 483, 579, 675, 771, 867,
            291, 387, 483, 771, 867, 963, 
            291, 387, 867, 963]

level2_y = [100, 
            132, 132,
            164, 164, 164, 164,
            196, 196, 196, 196, 196, 196, 196, 196, 
            228, 228, 228, 228, 228, 228, 228, 228,   
            260, 260, 260, 260, 260, 260, 
            292, 292, 292, 292,
            324, 324, 324, 324, 324, 324,
            356, 356, 356, 356, 356, 356, 
            388, 388, 388, 388]

level3_x = [435, 819,
            339, 435, 531, 723, 819, 915,
            339, 435, 531, 723, 819, 915,
            243, 339, 435, 531, 627, 723, 819, 915, 1011,
            243, 339, 435, 531, 627, 723, 819, 915, 1011,
            243, 339, 435, 531, 627, 723, 819, 915, 1011,
            243, 339, 435, 531, 627, 723, 819, 915, 1011,
            243, 339, 435, 531, 627, 723, 819, 915, 1011,
            339, 435, 531, 627, 723, 819, 915,
            339, 435, 531, 627, 723, 819, 915,
            435, 531, 627, 723, 819,
            435, 531, 627, 723, 819,
            531, 627, 723,
            531, 627, 723,
            627]

level3_y = [50, 50,
            82, 82, 82, 82, 82, 82,
            114, 114, 114, 114, 114, 114,
            146, 146, 146, 146, 146, 146, 146, 146, 146,
            178, 178, 178, 178, 178, 178, 178, 178, 178,
            210, 210, 210, 210, 210, 210, 210, 210, 210,
            242, 242, 242, 242, 242, 242, 242, 242, 242,
            274, 274, 274, 274, 274, 274, 274, 274, 274,
            306, 306, 306, 306, 306, 306, 306,
            338, 338, 338, 338, 338, 338, 338,
            370, 370, 370, 370, 370,
            402, 402, 402, 402, 402,
            434, 434, 434,
            466, 466, 466,
            498]

level1_colors = [0, 0, 0, 0, 0,
            0, 2, 2, 2, 0, 
            0, 2, 4, 2, 0, 
            0, 2, 2, 2, 0, 
            0, 0, 0, 0, 0,
            
            0, 0, 0, 0, 0,
            0, 2, 2, 2, 0, 
            0, 2, 4, 2, 0, 
            0, 2, 2, 2, 0, 
            0, 0, 0, 0, 0]

level2_colors = [4,
            4, 4,
            4, 4, 4, 4,
            4, 4, 12, 12, 12, 12, 4, 4, 
            4, 12, 2, 2, 2, 2, 12, 4,   
            4, 12, 2, 2, 12, 4, 
            4, 12, 12, 4,
            4, 12, 4, 4, 12, 4,
            4, 12, 4, 4, 12, 4, 
            4, 4, 4, 4]

level3_colors = [2, 2,
            2, 12, 2, 2, 12, 2,
            2, 12, 2, 2, 12, 2,
            2, 12, 4, 12, 2, 12, 4, 12, 2,
            2, 12, 4, 0, 10, 0, 4, 12, 2,
            2, 12, 4, 0, 10, 0, 4, 12, 2,
            2, 12, 4, 0, 10, 0, 4, 12, 2,
            2, 12, 4, 0, 10, 0, 4, 12, 2,
            2, 12, 4, 0, 4, 12, 2,
            2, 12, 4, 0, 4, 12, 2,
            2, 12, 4, 12, 2,
            2, 12, 4, 12, 2,
            2, 12, 2,
            2, 12, 2,
            2]

bricks_x = level1_x[:]
bricks_y = level1_y[:]

brick_color = level1_colors[:]
brick_health = [2]*len(bricks_x)

level = 1

# score, +10 bij brick het en een powerup die + 100 geeft
score = 0

# kogels die je kan schieten
bullets = 0

# levens, in de normale modus 3 en in hardcore 1 
lives = [1,1,1]
hardcore_mode = False

# Zorgt later in het spel voor een pauze 
live_pause = False
pause_timer = 0

# Variabeles van de timer 
time_played = 0
second_zero = ""
minute_zero = ""
seconds_played = 0
minutes_played = 0

# Variabeles die horen bij het schieten
cooldown = 0
switch_guns = True

# Cooldown voor de extra bal en +10 kogels animatie
paddle_animation_cooldown = 0

# messages en game status helpen bij het geven van berichten en het bepalen in welk deel van het spel/menu we zijn. 
# Paddle mode zorgt voor de mogelijkheid om te switchen tussen paddle modus
game_status_msg = ""
won_msg = ""
game_status = "start"
paddle_mode = 'normal'

# brick animation variabelen
brick_animation_x = []
brick_animation_y = []
brick_animation_countdown = []
brick_animation_color = []

# powerup, de timebomb text die erbij komt en de animatie
powerup_x = 0
powerup_y = 0
powerup_timebomb = 0
powerup_showing = False
powerup_falling = False
powerup_timebomb_warning = ""
powerup_timebomb = 0 
ball_powerup_animation_showing = False
ball_powerup_animation = 0
ball_powerup_animation_x = []
ball_powerup_animation_y = []
powerup_text = ''

# kogels coordinaten
bullets_x = []
bullets_y = []

#
# init game: Initialiseert Pygame, defineerd verschillende lettertype's, maakt het scherm en de klok aan
#

pygame.init()
font = pygame.font.SysFont('default', 64)
font_small = pygame.font.SysFont('default', 30) 
font_medium = pygame.font.SysFont('default', 50) 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images: start de spritesheet en de afbeeldingen die eruit worden gebruikt
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

# achtergrond voor spel
background = pygame.image.load('achtergrond.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# achtergrond voor startscherm
background2 = pygame.image.load('background.png')
background2 = pygame.transform.scale(background2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ball plaatje
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

# paddle plaatje
paddle_img = pygame.Surface((244, 65), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1157, 395, 244, 65))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# hartje plaatje
heart_img = pygame.Surface((65, 59), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1636, 651, 65, 59))
heart_img = pygame.transform.scale(heart_img, (32, 32))

# Blauwe brick
brick_img0 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img0.blit(spritesheet, (0, 0), (771, 389, 385, 129))
brick_img0 = pygame.transform.scale(brick_img0, (BRICK_WIDTH, BRICK_HEIGHT))

# Blauwe beschadigde brick
brick_img1 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img1.blit(spritesheet, (0, 0), (0, 0, 385, 129))
brick_img1 = pygame.transform.scale(brick_img1, (BRICK_WIDTH, BRICK_HEIGHT))

# Rode brick
brick_img2 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img2.blit(spritesheet, (0, 0), (771, 259, 385, 129))
brick_img2 = pygame.transform.scale(brick_img2, (BRICK_WIDTH, BRICK_HEIGHT))

# Rode beschadigde brick
brick_img3 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img3.blit(spritesheet, (0, 0), (771, 129, 385, 129))
brick_img3 = pygame.transform.scale(brick_img3, (BRICK_WIDTH, BRICK_HEIGHT))

# Gele brick
brick_img4 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img4.blit(spritesheet, (0, 0), (385, 389, 385, 129))
brick_img4 = pygame.transform.scale(brick_img4, (BRICK_WIDTH, BRICK_HEIGHT))

# Gele beschadigde brick
brick_img5 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img5.blit(spritesheet, (0, 0), (385, 259, 385, 129))
brick_img5 = pygame.transform.scale(brick_img5, (BRICK_WIDTH, BRICK_HEIGHT))

# Licht groene brick
brick_img6 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img6.blit(spritesheet, (0, 0), (0, 129, 385, 129))
brick_img6 = pygame.transform.scale(brick_img6, (BRICK_WIDTH, BRICK_HEIGHT))

# Licht groene beschadigde brick
brick_img7 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img7.blit(spritesheet, (0, 0), (0, 259, 385, 129))
brick_img7 = pygame.transform.scale(brick_img7, (BRICK_WIDTH, BRICK_HEIGHT))

# Paars brick
brick_img8 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img8.blit(spritesheet, (0, 0), (0, 389, 385, 129))
brick_img8 = pygame.transform.scale(brick_img8, (BRICK_WIDTH, BRICK_HEIGHT))

# Paars beschadigde brick
brick_img9 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img9.blit(spritesheet, (0, 0), (0, 519, 385, 129))
brick_img9 = pygame.transform.scale(brick_img9, (BRICK_WIDTH, BRICK_HEIGHT))

# Licht blauwe brick
brick_img10 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img10.blit(spritesheet, (0, 0), (385, 649, 385, 129))
brick_img10 = pygame.transform.scale(brick_img10, (BRICK_WIDTH, BRICK_HEIGHT))

# Licht blauwe beschadigde brick
brick_img11 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img11.blit(spritesheet, (0, 0), (385, 519, 385, 129))
brick_img11 = pygame.transform.scale(brick_img11, (BRICK_WIDTH, BRICK_HEIGHT))

# Oranje brick
brick_img12 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img12.blit(spritesheet, (0, 0), (771, 0, 385, 129))
brick_img12 = pygame.transform.scale(brick_img12, (BRICK_WIDTH, BRICK_HEIGHT))

# Oranje beschadigde brick
brick_img13 = pygame.Surface((385, 129), pygame.SRCALPHA)
brick_img13.blit(spritesheet, (0, 0), (771, 649, 385, 129))
brick_img13 = pygame.transform.scale(brick_img13, (BRICK_WIDTH, BRICK_HEIGHT))

# powerup plaatje
powerup_img = pygame.Surface((129, 129), pygame.SRCALPHA)
powerup_img.blit(spritesheet, (0, 0), (1532, 391, 129, 129))
powerup_img = pygame.transform.scale(powerup_img, (48, 48))

# kogel plaatje
bullet_img = pygame.Surface((9, 22), pygame.SRCALPHA)
bullet_img.blit(spritesheet, (0, 0), (0, 989, 9, 22))
bullet_img = pygame.transform.scale(bullet_img, (9, 22))

#
# game loop: herhaalt verschillende processen zoals bewegingen die worden gemaakt,
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

    # start screen
    if game_status == 'start':
       start = font.render("Druk op [E] om het spel te starten!", True, 'royalblue')
       hardcore = font.render("Druk op [C] om het spel in HARDCORE modus te starten!", True, 'crimson')
       keybinds = font_medium.render("[Z] Keybinds", True, 'darkorange')
       uitleg = font_medium.render("[X] Uitleg", True, 'darkorange')
       screen.blit(background2, (0, 0))
       screen.blit(start, ((SCREEN_WIDTH - start.get_width()) // 2 , 75))
       screen.blit(hardcore, ((SCREEN_WIDTH - hardcore.get_width()) // 2 , 20))
       screen.blit(keybinds, ((SCREEN_WIDTH - keybinds.get_width()) // 2 , 200))
       screen.blit(uitleg, ((SCREEN_WIDTH - uitleg.get_width()) // 2 , 250))
       pygame.display.flip()
       if keys[pygame.K_e]:
          game_status = "gamemode"
       if keys[pygame.K_c]:
          game_status = 'gamemode'
          hardcore_mode = True
       if keys[pygame.K_z]:
          game_status = 'keybinds'
       if keys[pygame.K_x]:
          game_status = 'uitleg'
       continue
    
    # gamemode
    if game_status == "gamemode":
      gamemode1 = font.render("Druk op [E] voor singleplayer!", True, 'royalblue')
      gamemode2 = font.render("Druk op [C] voor multiplayer", True, 'crimson') 
      screen.blit(gamemode1, ((SCREEN_WIDTH - gamemode1.get_width()) // 2 , 75))
      screen.blit(gamemode2, ((SCREEN_WIDTH - gamemode2.get_width()) // 2 , 20))  
      pygame.display.flip()
      if keys[pygame.K_e]:
         game_status = "playing"    
      if keys[pygame.K_c]:
         game_status = "playing"  
         multiplayer = True

    # keybinds submenu
    if game_status == 'keybinds':
       keybinds_title = font.render("Keybinds", True, 'darkorange')
       ad = font_small.render("1. Beweeg de plank met [A] en [D]", True, 'aqua')
       plank_modus = font_small.render("2. Verander de plank modus met de volgende knoppen:", True, 'aqua')
       plank_modus1 = font_small.render("[Z] Normale modus (Voor het kaatsen van de bal.)", True, 'aqua')
       plank_modus2 = font_small.render("[X] Schiet modus (Niet voor het kaatsen van ballen)", True, 'aqua')
       schieten = font_small.render("3. Druk op [W] om te schieten (Als je kogels hebt en in de schietmodus zit.)", True, 'aqua')
       esc1 = font_small.render("Druk op [Q] om terug te gaan", True, 'red')       
       screen.blit(background2, (0, 0))
       screen.blit(keybinds_title, ((SCREEN_WIDTH - keybinds_title.get_width()) // 2 , 50))
       screen.blit(ad, ((SCREEN_WIDTH - ad.get_width()) // 2 , 150))
       screen.blit(plank_modus, ((SCREEN_WIDTH - plank_modus.get_width()) // 2 , 180))
       screen.blit(plank_modus1, ((SCREEN_WIDTH - plank_modus1.get_width()) // 2 , 210))
       screen.blit(plank_modus2, ((SCREEN_WIDTH - plank_modus1.get_width()) // 2 , 240))
       screen.blit(schieten, ((SCREEN_WIDTH - schieten.get_width()) // 2 , 270))
       screen.blit(esc1, ((SCREEN_WIDTH - esc1.get_width()) // 2 , (SCREEN_HEIGHT - 50)))
       pygame.display.flip()
       if keys[pygame.K_q]:
        game_status = 'start'
       continue
  
    # uitleg submenu
    if game_status =='uitleg':
       uitleg_title = font.render("Uitleg", True, 'darkorange')
       uitleg1 = font_small.render("Welkom bij de breakout game gemaakt door Umar Aliev en Fjodor van der Kloet.", True, 'aqua')
       uitleg2 = font_small.render("In deze game is het de bedoeling om een zo hoog mogelijke score te behalen zonder af te gaan.", True, 'aqua')
       uitleg3 = font_small.render("In het eerste level hebben de bricks 2 hits nodig om te verdwijnen. Level 2: 4 hits Level 3: 8 Hits", True, 'aqua')
       uitleg4 = font_small.render("Elke keer als je bal een brick raakt gaat de bal steeds sneller!", True, 'aqua')
       uitleg5 = font_small.render("Bij elk level heb je een kans om Power-Ups te krijgen. Er zijn verschillende Power-Ups.", True, 'aqua')
       uitleg6 = font_small.render("1. +100 Score", True, 'aqua')
       uitleg7 = font_small.render("2. +10 Kogels", True, 'aqua')
       uitleg8 = font_small.render("3. Extra Bal", True, 'aqua')
       uitleg9 = font_small.render("In HARDCORE modus heb je maar 1 leven, in de normale modus 3.", True, 'aqua')
       esc2 = font_small.render("Druk op [Q] om terug te gaan", True, 'red')
       screen.blit(background2, (0, 0))
       screen.blit(uitleg_title, ((SCREEN_WIDTH - uitleg_title.get_width()) // 2 , 50))
       screen.blit(uitleg1, ((SCREEN_WIDTH - uitleg1.get_width()) // 2 , 150))
       screen.blit(uitleg2, ((SCREEN_WIDTH - uitleg2.get_width()) // 2 , 180))
       screen.blit(uitleg3, ((SCREEN_WIDTH - uitleg3.get_width()) // 2 , 210))
       screen.blit(uitleg4, ((SCREEN_WIDTH - uitleg4.get_width()) // 2 , 240))
       screen.blit(uitleg9, ((SCREEN_WIDTH - uitleg9.get_width()) // 2 , 270))       
       screen.blit(uitleg5, ((SCREEN_WIDTH - uitleg5.get_width()) // 2 , 300))
       screen.blit(uitleg6, ((SCREEN_WIDTH - uitleg7.get_width()) // 2 , 330))
       screen.blit(uitleg7, ((SCREEN_WIDTH - uitleg7.get_width()) // 2 , 360))
       screen.blit(uitleg8, ((SCREEN_WIDTH - uitleg7.get_width()) // 2 , 390))
       screen.blit(esc2, ((SCREEN_WIDTH - esc2.get_width()) // 2 , (SCREEN_HEIGHT - 50)))
       pygame.display.flip()
       if keys[pygame.K_q]:
        game_status = 'start'
       continue

    # check if you beat the level
    if game_status == 'playing' and len(bricks_x) == 0 and level != 3:
          game_status = 'next_level'

    # check if won + message      
    if level == 3 and len(bricks_x) == 0:
       game_status = 'won'
       won_msg = "You Won!" 

    # next level system       
    if game_status == 'next_level':    
        if keys[pygame.K_e]:
          if level == 1:
               level = 2
               bricks_x = level2_x[:]
               bricks_y = level2_y[:]
               brick_color = level2_colors[:]
               brick_health = [4]*len(bricks_x)
               balls_x = [0]
               balls_y = [0]
               balls_speed_x = [6]
               balls_speed_y = [6]
               game_status = 'playing'
               if powerup_showing: powerup_showing = False
               if powerup_falling: powerup_falling = False
               powerup_timebomb_warning = ""
          elif level == 2:
               level = 3
               bricks_x = level3_x[:]
               bricks_y = level3_y[:]
               brick_color = level3_colors[:]  
               brick_health = [8]*len(bricks_x)        
               balls_x = [0]
               balls_y = [100]
               balls_speed_x = [6]
               balls_speed_y = [6]
               game_status = 'playing'     
               if powerup_showing: powerup_showing = False
               if powerup_falling: powerup_falling = False 
               powerup_timebomb_warning = ""

    # lost screen
    if game_status != 'next_level':
        balls_lost = True
        for i in range(len(balls_x)):
           if balls_y[i] + BALL_HEIGHT < SCREEN_HEIGHT:
              balls_lost = False
        if balls_lost and not game_status == 'won':
              if len(lives) > 0: lives.pop()
              if len(lives) == 0:
                game_status_msg = "You lost!"
                game_status = 'lost'
                powerup_timebomb_warning = ""
              else:
                live_pause = True
                pause_timer += 90
                balls_x = [0]
                balls_y = [0]
                balls_speed_x = [6]
                balls_speed_y = [6]


    # pauze als je leven kwijt bent geraakt
    if live_pause == True:
       pause_timer -= 1
       pause_text = font.render("Je bent een leven kwijgt geraakt!", True, "yellow")
       screen.blit(pause_text, ((SCREEN_WIDTH - pause_text.get_width()) // 2, ((SCREEN_HEIGHT - pause_text.get_height()) // 2)))
       pygame.display.flip()
       if pause_timer == 0:
        live_pause = False
       continue


    # Clear messages while playing
    if game_status == 'playing':
        game_status_msg = ''
        won_msg = ''

    # restart 
    if keys[pygame.K_r] and game_status == 'lost' or game_status == 'won':
        if balls_x: balls_x.pop()
        if balls_y: balls_y.pop()
        if balls_speed_x: balls_speed_x.pop()
        if balls_speed_y: balls_speed_y.pop()
        powerup_falling = False
        powerup_showing = False
        level = 1
        time_played = 0
        score = 0
        bullets = 0
        bricks_x = level1_x[:]
        bricks_y = level1_y[:]
        brick_color = level1_colors[:]
        brick_health = [2]*len(bricks_x)
        balls_x = [0]
        balls_y = [0]
        balls_speed_x = [6]
        balls_speed_y = [6]
        game_status = 'playing'
        if powerup_showing: powerup_showing = False
        if powerup_falling: powerup_falling = False
        powerup_timebomb_warning = ""

    # time played counter
    if seconds_played < 10:
       second_zero = "0"
    else:
       second_zero = ""
    if minutes_played < 10:
       minute_zero = "0"
    else:
       minute_zero = ""
    if game_status == "playing":
       time_played += (1 / 30)
       seconds_played = int(time_played)
       if seconds_played == 60:
        minutes_played += 1
        seconds_played = 0
        time_played = 0
    time_text = str(minute_zero) + str(minutes_played) + ":" + str(second_zero) + str(seconds_played)

    # hardcore mode
    if hardcore_mode == True:
       lives = [1]
    
    # 
    # move everything
    #

    # move ball
    for i in range(len(balls_x)):
      balls_x[i] = balls_x[i] + balls_speed_x[i]
      balls_y[i] = balls_y[i] + balls_speed_y[i]

    # move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and game_status == 'playing':
        paddle_x = paddle_x - 17
    if keys[pygame.K_d] and game_status == 'playing':
        paddle_x = paddle_x + 17

    # 
    # handle collisions
    #

    # bounce ball
    for i in range(len(balls_x)-1,-1,-1):
      if balls_x[i] < 0 : 
        balls_speed_x[i] = abs(balls_speed_x[i]) 
      if balls_x[i] + BALL_WIDTH > SCREEN_WIDTH: 
        balls_speed_x[i] = abs(balls_speed_x[i]) * -1 
      if balls_y[i] < 0 : 
        balls_speed_y[i] = abs(balls_speed_y[i])
      if balls_y[i] + BALL_HEIGHT > SCREEN_HEIGHT:
        balls_speed_x[i] = 0
        balls_speed_y[i] = 0

    # detect and bounce ball on bricks
    for a in range(len(balls_x)-1, -1, -1):
      for i in range(len(bricks_x)-1, -1, -1):
        if (balls_x[a] + BALL_WIDTH > bricks_x[i] and
          balls_x[a] < bricks_x[i] + BRICK_WIDTH and
          balls_y[a] + BALL_HEIGHT > bricks_y[i] and
          balls_y[a] < bricks_y[i] + BRICK_HEIGHT):
          print('brick touched at ball_x = ' + str(balls_x[a]) + ' and ball_y = ' + str(balls_y[a]))
          brick_health[i] -= 1
          if balls_speed_y[a] > 0 and balls_y[a] < bricks_y[i]:
            balls_speed_y[a] = balls_speed_y[a] * -1
          if balls_speed_y[a] < 0 and balls_y[a] + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
            balls_speed_y[a] = balls_speed_y[a] * -1
          if balls_speed_x[a] > 0 and balls_x[a] < bricks_x[i]:
            balls_speed_x[a] = balls_speed_x[a] * -1
          if balls_speed_x[a] < 0 and balls_x[a] + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
            balls_speed_x[a] = balls_speed_x[a] * -1
          balls_speed_y[a] = balls_speed_y[a] * 1.015
          balls_speed_x[a] = balls_speed_x[a] * 1.015
          if brick_health[i] in [7,5,3,1]:
             brick_color[i] += 1
          elif brick_health[i] in [6,4,2]:
             possible_color = [0,2,4,6,8,10,12]
             if brick_color[i] - 1 in possible_color:
                current_color = brick_color[i] - 1
                possible_color.remove(current_color)
             brick_color[i] = random.choice(possible_color)
          elif brick_health[i] == 0:
              if not powerup_showing and not powerup_falling:
                if level == 1 and random.random() < 0.3:
                  powerup_showing = True
                  powerup_timebomb = 750 
                  while True:
                     powerup_x = random.randint(0, SCREEN_WIDTH - 48)
                     powerup_y = random.randint(0, SCREEN_HEIGHT // 2)
                     in_brick = False
                     for b in range(len(bricks_x)):
                        if (powerup_x + 48 > bricks_x[b] and
                          powerup_x < bricks_x[b] + BRICK_WIDTH and
                          powerup_y + 48 > bricks_y[b] and
                          powerup_y < bricks_y[b] + BRICK_HEIGHT):
                          in_brick = True
                          break
                     if not in_brick:
                         break          
                if level == 2 and random.random() < 0.2:
                  powerup_showing = True
                  powerup_timebomb = 750
                  while True:
                     powerup_x = random.randint(0, SCREEN_WIDTH - 48)
                     powerup_y = random.randint(0, SCREEN_HEIGHT // 2)
                     in_brick = False
                     for b in range(len(bricks_x)):
                        if (powerup_x + 48 > bricks_x[b] and
                          powerup_x < bricks_x[b] + BRICK_WIDTH and
                          powerup_y + 48 > bricks_y[b] and
                          powerup_y < bricks_y[b] + BRICK_HEIGHT):
                          in_brick = True
                          break
                     if not in_brick:
                         break     
                if level == 3 and random.random() < 0.1:
                  powerup_showing = True
                  powerup_timebomb = 750
                  while True:
                     powerup_x = random.randint(0, SCREEN_WIDTH - 48)
                     powerup_y = random.randint(0, SCREEN_HEIGHT // 2)
                     in_brick = False
                     for b in range(len(bricks_x)):
                        if (powerup_x + 48 > bricks_x[b] and
                          powerup_x < bricks_x[b] + BRICK_WIDTH and
                          powerup_y + 48 > bricks_y[b] and
                          powerup_y < bricks_y[b] + BRICK_HEIGHT):
                          in_brick = True
                          break
                     if not in_brick:
                         break     
              brick_animation_x.append(bricks_x[i])
              brick_animation_y.append(bricks_y[i])
              brick_animation_countdown.append(90)
              brick_animation_color.append(brick_color[i])
              bricks_x.pop(i)
              bricks_y.pop(i)
              brick_health.pop(i)
              brick_color.pop(i)
              score += 10
          break

    # stop paddle zodat hij niet buiten scherm gaat
    if paddle_x < 0 :
        paddle_x = 0
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # bounce ball on paddle
    for i in range(len(balls_x)-1, -1, -1):
      if (balls_x[i] + BALL_WIDTH > paddle_x and
        balls_x[i] < paddle_x + PADDLE_WIDTH and
        balls_y[i] + BALL_HEIGHT > paddle_y and
        balls_y[i] < paddle_y + PADDLE_HEIGHT):
        if paddle_mode == 'normal':
          ball_center = balls_x[i] + BALL_WIDTH / 2
          paddle_center = paddle_x + PADDLE_WIDTH / 2
          distance = ball_center - paddle_center
          balls_speed_x[i] = distance / (PADDLE_WIDTH / 2) * 6
          balls_speed_y[i] = abs(balls_speed_y[i]) * -1
        if paddle_mode != 'normal':
          game_status = 'lost'
          game_status_msg = 'You lost!'
          balls_speed_x.pop(i)
          balls_speed_y.pop(i)
          balls_x.pop(i)
          balls_y.pop(i)
             
    #
    # bullets
    #

    # detect bullets on bricks + pop bricks
    for a in range(len(bullets_x)-1, -1, -1):
      for i in range(len(bricks_x)-1, -1, -1):
        if (bullets_x[a] + BALL_WIDTH > bricks_x[i] and
          bullets_x[a] < bricks_x[i] + BRICK_WIDTH and
          bullets_y[a] + BALL_HEIGHT > bricks_y[i] and
          bullets_y[a] < bricks_y[i] + BRICK_HEIGHT):
          print('bullet hit brick at bullet_x = ' + str(bullets_x[a]) + ' and bullets_y = ' + str(bullets_y[a]))
          brick_health[i] -= 1 
          if brick_health[i] in [7,5,3,1]:
             brick_color[i] += 1
          elif brick_health[i] in [6,4,2]:
             possible_color = [0,2,4,6,8,10,12]
             if brick_color[i] - 1 in possible_color:
                current_color = brick_color[i] - 1
                possible_color.remove(current_color)
             brick_color[i] = random.choice(possible_color)
          elif brick_health[i] == 0:
              if not powerup_showing and not powerup_falling:
                if level == 1 and random.random() < 0.3:
                  powerup_showing = True
                  powerup_timebomb = 750
                  while True:
                     powerup_x = random.randint(0, SCREEN_WIDTH - 48)
                     powerup_y = random.randint(0, SCREEN_HEIGHT // 2)
                     in_brick = False
                     for b in range(len(bricks_x)):
                        if (powerup_x + 48 > bricks_x[b] and
                          powerup_x < bricks_x[b] + BRICK_WIDTH and
                          powerup_y + 48 > bricks_y[b] and
                          powerup_y < bricks_y[b] + BRICK_HEIGHT):
                          in_brick = True
                          break
                     if not in_brick:
                         break          
                if level == 2 and random.random() < 0.2:
                  powerup_showing = True
                  powerup_timebomb = 750
                  while True:
                     powerup_x = random.randint(0, SCREEN_WIDTH - 48)
                     powerup_y = random.randint(0, SCREEN_HEIGHT // 2)
                     in_brick = False
                     for b in range(len(bricks_x)):
                        if (powerup_x + 48 > bricks_x[b] and
                          powerup_x < bricks_x[b] + BRICK_WIDTH and
                          powerup_y + 48 > bricks_y[b] and
                          powerup_y < bricks_y[b] + BRICK_HEIGHT):
                          in_brick = True
                          break
                     if not in_brick:
                         break     
                if level == 3 and random.random() < 0.1:
                  powerup_showing = True
                  powerup_timebomb = 750
                  while True:
                     powerup_x = random.randint(0, SCREEN_WIDTH - 48)
                     powerup_y = random.randint(0, SCREEN_HEIGHT // 2)
                     in_brick = False
                     for b in range(len(bricks_x)):
                        if (powerup_x + 48 > bricks_x[b] and
                          powerup_x < bricks_x[b] + BRICK_WIDTH and
                          powerup_y + 48 > bricks_y[b] and
                          powerup_y < bricks_y[b] + BRICK_HEIGHT):
                          in_brick = True
                          break
                     if not in_brick:
                         break     
              brick_animation_x.append(bricks_x[i])
              brick_animation_y.append(bricks_y[i])
              brick_animation_countdown.append(90)
              brick_animation_color.append(brick_color[i])
              bricks_x.pop(i)
              bricks_y.pop(i)
              brick_health.pop(i)
              brick_color.pop(i)
          bullets_x.pop(a)
          bullets_y.pop(a) 
          break    

    # shoot bullets
    if bullets > 0 and paddle_mode == 'guns' and game_status == 'playing':
       if keys[pygame.K_w] and cooldown == 0:
          if switch_guns: 
            bullets_x.append(paddle_x + 1)
          else:
            bullets_x.append(paddle_x + PADDLE_WIDTH - 10)
          bullets_y.append(paddle_y - 20)
          bullets -= 1
          cooldown = 7
          switch_guns = not switch_guns

    # move bullets
    for i in range(len(bullets_x)):
       bullets_y[i] -= 5

    # bullets cooldown (anders als je spatie balk in klikt gaat alles heel snel achter elkaar)
    if cooldown > 0:
       cooldown -= 1

    #
    # paddle mode's
    #

    # paddle mode 1 (normaal)
    if keys[pygame.K_z] and game_status == 'playing':
      paddle_img.fill((0, 0, 0, 0))
      paddle_img = pygame.Surface((244, 65), pygame.SRCALPHA)
      paddle_img.blit(spritesheet, (0, 0), (1157, 395, 244, 65))
      paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
      paddle_mode = 'normal'

    # paddle mode 2 (schieten)
    if keys[pygame.K_x] and game_status == 'playing':
      paddle_img.fill((0, 0, 0, 0))
      paddle_img = pygame.Surface((244, 65), pygame.SRCALPHA)
      paddle_img.blit(spritesheet, (0, 0), (1157, 659, 244, 65))
      paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
      paddle_mode = 'guns'

    #
    # powerups
    #

    # powerup timebomb
    if powerup_showing == True and powerup_falling == False:
       if powerup_timebomb > 0:
          powerup_timebomb -= 1
          powerup_timebomb_timer = powerup_timebomb // 30
          powerup_timebomb_warning = "Powerup gespawned! Hij verdwijnt over: " + str(powerup_timebomb_timer) + " seconden"
       if powerup_timebomb == 0:
          powerup_y -= 5
          powerup_timebomb_warning = ""
          if powerup_y < -40:
             powerup_showing = False

    # bounce ball on powerup
    for i in range(len(balls_x)):
      if powerup_showing == True:
        if (balls_x[i] + BALL_WIDTH > powerup_x and
          balls_x[i] < powerup_x + 48 and
          balls_y[i] + BALL_HEIGHT > powerup_y and
          balls_y[i] < powerup_y + 48):
          print('ball touched powerup at ball_x = ' + str(balls_x[i]) + ' and ball_y = ' + str(balls_y[i]))
          if balls_speed_y[i] > 0 and balls_y[i] < powerup_y:
            balls_speed_y[i] = balls_speed_y[i] * -1
          if balls_speed_y[i] < 0 and balls_y[i] + BALL_HEIGHT > powerup_y + 48:
            balls_speed_y[i] = balls_speed_y[i] * -1
          if balls_speed_x[i] > 0 and balls_x[i] < powerup_x:
            balls_speed_x[i] = balls_speed_x[i] * -1
          if balls_speed_x[i] < 0 and balls_x[i] + BALL_WIDTH > powerup_x + 48:
            balls_speed_x[i] = balls_speed_x[i] * -1
          powerup_falling = True
          powerup_timebomb = 0
          powerup_timebomb_warning = ""

    # powerup falling + detect als paddle vangt
    if powerup_falling:
       powerup_y += 5
       if (powerup_x + 48 > paddle_x and
        powerup_x < paddle_x + PADDLE_WIDTH and
        powerup_y + 48 > paddle_y and
        powerup_y < paddle_y + PADDLE_HEIGHT):
          random_powerup_amount = [1,2,3]
          random_powerup = random.choice(random_powerup_amount)
          if paddle_mode == 'normal':
            if random_powerup == 1:
              score += 100
              paddle_animation_cooldown += 70
            if random_powerup == 2:
              balls_x.append(50)
              balls_y.append(50)
              balls_speed_x.append(6)
              balls_speed_y.append(6)
              ball_powerup_animation += 250
              ball_powerup_animation_showing = True
              powerup_text = font_small.render("Extra Bal!", True, "orange")
              ball_powerup_animation_x.append(paddle_x + ((PADDLE_WIDTH - powerup_text.get_width()) // 2))
              ball_powerup_animation_y.append(paddle_y + ((PADDLE_HEIGHT - powerup_text.get_height()) // 2))
            if random_powerup == 3:
              bullets += 10
              ball_powerup_animation += 90 
              ball_powerup_animation_showing = True
              powerup_text = font_small.render("+10 Kogels!", True, "orange")
              ball_powerup_animation_x.append(paddle_x + ((PADDLE_WIDTH - powerup_text.get_width()) // 2))
              ball_powerup_animation_y.append(paddle_y + ((PADDLE_HEIGHT - powerup_text.get_height()) // 2))
            powerup_falling = False
            powerup_showing = False
          if paddle_mode != 'normal':
            powerup_falling = False
            powerup_showing = False             
       if powerup_y > SCREEN_HEIGHT:
         powerup_falling = False
         powerup_showing = False

    # +100 score animation
    if paddle_animation_cooldown > 0:
      paddle_img.fill((0, 0, 0, 0))
      paddle_img = pygame.Surface((244, 65), pygame.SRCALPHA)
      if paddle_animation_cooldown > 60:
        paddle_img.blit(spritesheet, (0, 0), (1157, 0, 244, 65))
      elif paddle_animation_cooldown > 50:
        paddle_img.blit(spritesheet, (0, 0), (1083, 912, 244, 65))
      elif paddle_animation_cooldown > 40:
        paddle_img.blit(spritesheet, (0, 0), (1083, 846, 244, 65))
      elif paddle_animation_cooldown > 30:
        paddle_img.blit(spritesheet, (0, 0), (1328, 792, 244, 65))
      elif paddle_animation_cooldown > 20:
        paddle_img.blit(spritesheet, (0, 0), (1016, 780, 244, 65))
      elif paddle_animation_cooldown > 10:
        paddle_img.blit(spritesheet, (0, 0), (838, 912, 244, 65))
      elif paddle_animation_cooldown > 0:
        paddle_img.blit(spritesheet, (0, 0), (1328, 858, 244, 65))
      paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
      paddle_animation_cooldown -= 1
    if paddle_animation_cooldown == 0 and paddle_mode != 'guns':
      paddle_img = pygame.Surface((244, 65), pygame.SRCALPHA)
      paddle_img.blit(spritesheet, (0, 0), (1157, 395, 244, 65))
      paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
       
    # extra ball animation tekst
    for i in range(len(ball_powerup_animation_y)):
      if ball_powerup_animation > 0 and ball_powerup_animation_showing == True:
        ball_powerup_animation_y[i] -= 5
        ball_powerup_animation -= 1
    if ball_powerup_animation == 0 and ball_powerup_animation_showing == True:
       ball_powerup_animation_showing = False
       ball_powerup_animation_x.pop(i)
       ball_powerup_animation_y.pop(i)
       
       
    # 
    # draw everything
    #

    # clear screen
    screen.fill('black') 

    # background
    screen.blit(background, (0, 0))

    # draw ball
    for i in range(len(balls_x)):
      screen.blit(ball_img, (balls_x[i], balls_y[i]))

    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw bullet
    for i in range(len(bullets_x)):
       screen.blit(bullet_img, (bullets_x[i], bullets_y[i]))

    # draw bricks
    for i in range(len(bricks_x)):
        if brick_color[i] == 0:
            screen.blit(brick_img0, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 1:
            screen.blit(brick_img1, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 2:
            screen.blit(brick_img2, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 3:
            screen.blit(brick_img3, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 4:
            screen.blit(brick_img4, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 5:
            screen.blit(brick_img5, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 6:
            screen.blit(brick_img6, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 7:
            screen.blit(brick_img7, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 8:
            screen.blit(brick_img8, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 9:
            screen.blit(brick_img9, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 10:
            screen.blit(brick_img10, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 11:
            screen.blit(brick_img11, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 12:
            screen.blit(brick_img12, (bricks_x[i], bricks_y[i]))
        if brick_color[i] == 13:
            screen.blit(brick_img13, (bricks_x[i], bricks_y[i]))                                                

    # draw powerup
    if powerup_showing:
        screen.blit(powerup_img, (powerup_x, powerup_y))

    # draw current level
    level_tekst = font_medium.render("Level " + str(level), True, 'deepskyblue')
    screen.blit(level_tekst, ((SCREEN_WIDTH - level_tekst.get_width()) // 2, 10))

    # draw score
    score_count = font_medium.render("Score: " + str(score), True, 'white')
    screen.blit(score_count, (10, 10))

    # draw powerup timebomb warning
    if powerup_timebomb > 450:
       powerup_timebomb_warning_tekst = font_small.render(powerup_timebomb_warning, True, "green")
    if powerup_timebomb < 300:
       powerup_timebomb_warning_tekst = font_small.render(powerup_timebomb_warning, True, "yellow")
    if powerup_timebomb < 150:
       powerup_timebomb_warning_tekst = font_small.render(powerup_timebomb_warning, True, "orange")
    if powerup_timebomb < 90:
       powerup_timebomb_warning_tekst = font_small.render(powerup_timebomb_warning, True, "red")
    screen.blit(powerup_timebomb_warning_tekst, ((SCREEN_WIDTH - powerup_timebomb_warning_tekst.get_width()) // 2, (SCREEN_HEIGHT - 30)))

    # draw hearts
    for i in range(len(lives)):
       heart_x = SCREEN_WIDTH - (i + 1) * (42)
       heart_y = 10
       screen.blit(heart_img, (heart_x, heart_y))

    # draw bullet count
    bullet_count = font_medium.render("Kogels: " + str(bullets), True, 'yellow')
    screen.blit(bullet_count, (10, 50))

    # draw time 
    time_count = font_small.render(time_text, True, "yellow")
    screen.blit(time_count, ((SCREEN_WIDTH - time_count.get_width()) // 2, 47))

    # extra ball text animation
    if ball_powerup_animation_showing == True:
      for i in range(len(ball_powerup_animation_x)):
        screen.blit(powerup_text, (ball_powerup_animation_x[i], ball_powerup_animation_y[i]))

    # brick animation
    for i in range(len(brick_animation_x)-1,-1,-1):
          color = brick_animation_color[i]
          if color == 1: 
            screen.blit(brick_img1, (brick_animation_x[i], brick_animation_y[i]))
          if color == 3: 
            screen.blit(brick_img3, (brick_animation_x[i], brick_animation_y[i]))
          if color == 5: 
            screen.blit(brick_img5, (brick_animation_x[i], brick_animation_y[i]))
          if color == 7: 
            screen.blit(brick_img7, (brick_animation_x[i], brick_animation_y[i]))
          if color == 9: 
            screen.blit(brick_img9, (brick_animation_x[i], brick_animation_y[i]))
          if color == 11:
             screen.blit(brick_img11, (brick_animation_x[i], brick_animation_y[i]))
          if color == 13:
             screen.blit(brick_img13, (brick_animation_x[i], brick_animation_y[i]))
          if brick_animation_y: brick_animation_y[i] -= 15
          brick_animation_countdown[i] -= 1
          if brick_animation_countdown[i] == 0:
            brick_animation_x.pop(i)
            brick_animation_y.pop(i)
            brick_animation_countdown.pop(i)
            brick_animation_color.pop(i)

    # draw lost screen
    game_status_img = font.render(game_status_msg, True, 'red')
    screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) // 2, 200))

    # draw restart screen
    if game_status == 'lost' or game_status == 'won':
      restart_tekst = font.render("Klik op [R] om opnieuw te beginnen", True, 'coral')
      screen.blit(restart_tekst, ((SCREEN_WIDTH - restart_tekst.get_width()) // 2, 250))    

    # draw win screen
    won_img = font.render(won_msg, True, 'blue')
    screen.blit(won_img, ((SCREEN_WIDTH - won_img.get_width()) // 2, 200))

    # draw next level screen
    if game_status == 'next_level':
        if balls_x: balls_x.pop()
        if balls_y: balls_y.pop()
        if balls_speed_x: balls_speed_x.pop()
        if balls_speed_y: balls_speed_y.pop()
        next_level_msg = font.render('Level ' + str(level) + ' voltooid! Druk op [E] voor het volgende level', True, 'cyan')
        screen.blit(next_level_msg, ((SCREEN_WIDTH - next_level_msg.get_width()) // 2, 100))

    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')