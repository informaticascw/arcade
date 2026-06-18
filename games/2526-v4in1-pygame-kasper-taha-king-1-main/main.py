#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
# full caps zijn vaste definities, kleine letters kunnen veranderen

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
KOGEL_WIDTH = 8   # breedte van een kogel
KOGEL_HEIGHT = 16 # hoogte van een kogel
KOGEL_SPEED = 12  # hoe snel de kogel omhoog gaat
ball_x = 5
ball_speed_x = 7
ball_y = 100
ball_speed_y = 7
paddle_x = (SCREEN_WIDTH / 2)
paddle_y = (SCREEN_HEIGHT - 100)

game_status_msg = "gebruik [A] en [D] om te bewegen, [S] om te schieten"
game_status_msg2 = 'level 1'
game_status_msg3 = ''
main_message_color = 'blue'


time_played = 0
second_zero = ""
minute_zero = ""
seconds_played = 0
minutes_played = 0
game_status = 'playing'
level = 1
kogels = []  # lijst met alle kogels die momenteel op het scherm zijn
kogel_cooldown = 0  # teller voor vertraging tussen kogels

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
font_small = pygame.font.SysFont('default', 30) 
font_medium = pygame.font.SysFont('default', 50)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) 


paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# kogel plaatje
kogel_img = pygame.Surface((10, 21), pygame.SRCALPHA)
kogel_img.blit(spritesheet, (0, 0), (0, 990, 10, 21))
kogel_img = pygame.transform.scale(kogel_img, (KOGEL_WIDTH, KOGEL_HEIGHT))

# blok plaatjes voor level 1 (heel en gebarsten)
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img1 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img1.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img1 = pygame.transform.scale(brick_img1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img1_1 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img1_1.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img1_1 = pygame.transform.scale(brick_img1_1, (BRICK_WIDTH, BRICK_HEIGHT))

# blok plaatjes voor level 2 (heel en gebarsten)
brick_img2 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img2.blit(spritesheet, (0, 0), (0, 130, 384, 128))
brick_img2 = pygame.transform.scale(brick_img2, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img2_1 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img2_1.blit(spritesheet, (0, 0), (0, 130, 384, 128))
brick_img2_1 = pygame.transform.scale(brick_img2_1, (BRICK_WIDTH, BRICK_HEIGHT))

# gebarsten blok level 1, en gebarsten blok level 2
brick_img3 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img3.blit(spritesheet, (0, 0), (0, 0, 384, 128))
brick_img3 = pygame.transform.scale(brick_img3, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img3_1 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img3_1.blit(spritesheet, (0, 0), (0, 0, 384, 128))
brick_img3_1 = pygame.transform.scale(brick_img3_1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img4 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img4.blit(spritesheet, (0, 0), (0, 260, 384, 128))
brick_img4 = pygame.transform.scale(brick_img4, (BRICK_WIDTH, BRICK_HEIGHT))

# blok plaatjes voor level 3 (heel en gebarsten)
brick_img5 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img5.blit(spritesheet, (0, 0), (772, 260, 384, 128))
brick_img5 = pygame.transform.scale(brick_img5, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img6 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img6.blit(spritesheet, (0, 0), (772, 130, 384, 128))
brick_img6 = pygame.transform.scale(brick_img6, (BRICK_WIDTH, BRICK_HEIGHT))

# originele images opslaan zodat we die bij reset kunnen gebruiken
brick_img_start = brick_img
brick_img2_start = brick_img2
brick_img3_start = brick_img3
brick_img4_start = brick_img4
brick_img5_start = brick_img5
brick_img6_start = brick_img6


# blokken voor level 1, patroon in de vorm van een hart
bricks = [{'pos': (400, 200), 'img': brick_img, 'health': 2},
  {'pos': (496, 200), 'img': brick_img, 'health': 2},
  {'pos': (688, 200), 'img': brick_img, 'health': 2},
  {'pos': (784, 200), 'img': brick_img, 'health': 2},
  {'pos': (400, 232), 'img': brick_img, 'health': 2},
  {'pos': (496, 232), 'img': brick_img, 'health': 2},
  {'pos': (592, 232), 'img': brick_img, 'health': 2},
  {'pos': (688, 232), 'img': brick_img, 'health': 2},
  {'pos': (784, 232), 'img': brick_img, 'health': 2},
  {'pos': (496, 264), 'img': brick_img, 'health': 2},
  {'pos': (592, 264), 'img': brick_img, 'health': 2},
  {'pos': (688, 264), 'img': brick_img, 'health': 2},
  {'pos': (544, 296), 'img': brick_img, 'health': 2},
  {'pos': (640, 296), 'img': brick_img, 'health': 2},
  {'pos': (592, 328), 'img': brick_img, 'health': 2},]


# blokken voor level 2, schaak patroon
bricks_level2 = [{'pos': (100, 132), 'img': brick_img2, 'health': 2},
  {'pos': (292, 132), 'img': brick_img2, 'health': 2},
  {'pos': (484, 132), 'img': brick_img2, 'health': 2},
  {'pos': (676, 132), 'img': brick_img2, 'health': 2},
  {'pos': (868, 132), 'img': brick_img2, 'health': 2},
  {'pos': (1060, 132), 'img': brick_img2, 'health': 2},
  {'pos': (196, 164), 'img': brick_img2, 'health': 2},
  {'pos': (388, 164), 'img': brick_img2, 'health': 2},
  {'pos': (580, 164), 'img': brick_img2, 'health': 2},
  {'pos': (772, 164), 'img': brick_img2, 'health': 2},
  {'pos': (964, 164), 'img': brick_img2, 'health': 2},
  {'pos': (100, 196), 'img': brick_img2, 'health': 2},
  {'pos': (292, 196), 'img': brick_img2, 'health': 2},
  {'pos': (484, 196), 'img': brick_img2, 'health': 2},
  {'pos': (676, 196), 'img': brick_img2, 'health': 2},
  {'pos': (868, 196), 'img': brick_img2, 'health': 2},
  {'pos': (1060, 196), 'img': brick_img2, 'health': 2},
  {'pos': (196, 228), 'img': brick_img2, 'health': 2},
  {'pos': (388, 228), 'img': brick_img2, 'health': 2},
  {'pos': (580, 228), 'img': brick_img2, 'health': 2},
  {'pos': (772, 228), 'img': brick_img2, 'health': 2},
  {'pos': (964, 228), 'img': brick_img2, 'health': 2},
  {'pos': (100, 260), 'img': brick_img2, 'health': 2},
  {'pos': (292, 260), 'img': brick_img2, 'health': 2},
  {'pos': (484, 260), 'img': brick_img2, 'health': 2},
  {'pos': (676, 260), 'img': brick_img2, 'health': 2},
  {'pos': (868, 260), 'img': brick_img2, 'health': 2},
  {'pos': (1060, 260), 'img': brick_img2, 'health': 2},]

# blokken voor level 3, patroon in de vorm van een ster
bricks_level3 = [
  {'pos': (580, 140), 'img': brick_img5, 'health': 2},
  {'pos': (484, 172), 'img': brick_img5, 'health': 2},
  {'pos': (580, 172), 'img': brick_img5, 'health': 2},
  {'pos': (676, 172), 'img': brick_img5, 'health': 2},
  {'pos': (196, 204), 'img': brick_img5, 'health': 2},
  {'pos': (292, 204), 'img': brick_img5, 'health': 2},
  {'pos': (388, 204), 'img': brick_img5, 'health': 2},
  {'pos': (484, 204), 'img': brick_img5, 'health': 2},
  {'pos': (580, 204), 'img': brick_img5, 'health': 2},
  {'pos': (676, 204), 'img': brick_img5, 'health': 2},
  {'pos': (772, 204), 'img': brick_img5, 'health': 2},
  {'pos': (868, 204), 'img': brick_img5, 'health': 2},
  {'pos': (964, 204), 'img': brick_img5, 'health': 2},
  {'pos': (388, 236), 'img': brick_img5, 'health': 2},
  {'pos': (484, 236), 'img': brick_img5, 'health': 2},
  {'pos': (580, 236), 'img': brick_img5, 'health': 2},
  {'pos': (676, 236), 'img': brick_img5, 'health': 2},
  {'pos': (772, 236), 'img': brick_img5, 'health': 2},
  {'pos': (292, 268), 'img': brick_img5, 'health': 2},
  {'pos': (388, 268), 'img': brick_img5, 'health': 2},
  {'pos': (772, 268), 'img': brick_img5, 'health': 2},
  {'pos': (868, 268), 'img': brick_img5, 'health': 2},
  {'pos': (196, 300), 'img': brick_img5, 'health': 2},
  {'pos': (292, 300), 'img': brick_img5, 'health': 2},
  {'pos': (868, 300), 'img': brick_img5, 'health': 2},
  {'pos': (964, 300), 'img': brick_img5, 'health': 2},
  {'pos': (196, 332), 'img': brick_img5, 'health': 2},
  {'pos': (964, 332), 'img': brick_img5, 'health': 2},
]

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
        paddle_x = paddle_x + 21
    if keys[pygame.K_a]:
        paddle_x = paddle_x - 21
    
    # paddle stop aan rechter kant van scherm
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    # paddle stop aan linker kant van scherm
    if paddle_x < 0:
        paddle_x = 0

    # schieten met S, kogel verschijnt midden boven de plank
    # alleen als het spel bezig is
    if kogel_cooldown > 0:
        kogel_cooldown -= 1  # cooldown telt elke frame omlaag

    if keys[pygame.K_s] and game_status == 'playing' and kogel_cooldown == 0:
        kogel = {
            'x': paddle_x + PADDLE_WIDTH // 2 - KOGEL_WIDTH // 2,
            'y': paddle_y - KOGEL_HEIGHT
        }
        kogels.append(kogel)
        kogel_cooldown = 10  # wacht 10 frames voor de volgende kogel

    # beweeg alle kogels omhoog en verwijder ze als ze het scherm verlaten
    for kogel in kogels[:]:
        kogel['y'] -= KOGEL_SPEED
        if kogel['y'] + KOGEL_HEIGHT < 0:
            kogels.remove(kogel)

    # paddle botsing in één blok zodat ball_speed_y maar één keer omgekeerd wordt per frame
    if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT):

        ball_center = ball_x + BALL_WIDTH / 2
        paddle_center = paddle_x + PADDLE_WIDTH / 2
        distance = ball_center - paddle_center
        ball_speed_x = distance / (PADDLE_WIDTH / 2) * 7.2

        # richting aanpassen als je beweegt tijdens botsing
        if keys[pygame.K_d] and ball_speed_x < 0:
            ball_speed_x = abs(ball_speed_x)
        elif keys[pygame.K_a] and ball_speed_x > 0:
            ball_speed_x = -abs(ball_speed_x)

        ball_speed_y = abs(ball_speed_y) * -1

        # bal uit de plank duwen zodat hij niet vast zit
        ball_y = paddle_y - BALL_HEIGHT

    # maximale snelheid van de bal begrenzen zodat hij niet onbestuurbaar wordt
    if ball_speed_y > 16:
        ball_speed_y = 16
    if ball_speed_y < -16:
        ball_speed_y = -16
    if ball_speed_x > 16:
        ball_speed_x = 16
    if ball_speed_x < -16:
        ball_speed_x = -16
       
    for i in reversed(range(len(bricks))):
        brick = bricks[i]
        brick_x, brick_y = brick['pos']

        if (ball_x < brick_x + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > brick_y and
            ball_y < brick_y + BRICK_HEIGHT and
            ball_x + BALL_WIDTH > brick_x):

              overlap_left   = (ball_x + BALL_WIDTH) - brick_x
              overlap_right  = (brick_x + BRICK_WIDTH) - ball_x
              overlap_top    = (ball_y + BALL_HEIGHT) - brick_y
              overlap_bottom = (brick_y + BRICK_HEIGHT) - ball_y

              min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

              print(ball_speed_x)
              print(ball_speed_y)
              print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))

              if min_overlap == overlap_left:
                ball_speed_x = -abs(ball_speed_x)
                ball_x = brick_x - BALL_WIDTH
              elif min_overlap == overlap_right:
                ball_speed_x = abs(ball_speed_x)
                ball_x = brick_x + BRICK_WIDTH
              elif min_overlap == overlap_top:
                ball_speed_y = -abs(ball_speed_y)
                ball_y = brick_y - BALL_HEIGHT
              elif min_overlap == overlap_bottom:
                ball_speed_y = abs(ball_speed_y)
                ball_y = brick_y + BRICK_HEIGHT

              brick['health'] -= 1 # levens van blok verminderen
              if brick['health'] == 1:
                brick['img'] = brick_img3  # verander naar gebarsten plaatje
              elif brick['health'] <= 0:
                bricks.pop(i)  # blok verwijderen uit de lijst
                ball_speed_x = ball_speed_x * 1.05  # bal wordt iets sneller bij elk blok
                ball_speed_y = ball_speed_y * 1.05

              break

        # kogels die een blok raken
        for kogel in kogels[:]:
            if (kogel['x'] < brick_x + BRICK_WIDTH and
                kogel['x'] + KOGEL_WIDTH > brick_x and
                kogel['y'] < brick_y + BRICK_HEIGHT and
                kogel['y'] + KOGEL_HEIGHT > brick_y):
                    kogels.remove(kogel)  # kogel verdwijnt
                    brick['health'] -= 1
                    if brick['health'] == 1:
                        brick['img'] = brick_img3
                    elif brick['health'] <= 0:
                        bricks.pop(i)
                    break
               
    # let op: extra check "ball_y + BALL_HEIGHT <= SCREEN_HEIGHT" voorkomt dat je
    # via E nog naar het volgende level kan als de bal tegelijk onder het scherm valt
    if level == 1 and len(bricks) == 0 and ball_y + BALL_HEIGHT <= SCREEN_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "Je hebt gewonnen!"
        game_status_msg2 = ''
        game_status_msg3 = 'klik op E om naar level 2 te gaan'
        game_status = ''
        
        if keys[pygame.K_e]:
            level = 2
            ball_y = 0
            ball_x = 0
            ball_speed_x = 7
            ball_speed_y = 7
            game_status_msg = 'gebruik [A] en [D] om te bewegen, [S] om te schieten'
            game_status_msg2 = 'level 2'
            game_status_msg3 = ''
            game_status = 'playing'
            brick_img3 = brick_img4  # gebarsten plaatje voor level 2
            bricks = bricks_level2
            kogels = []
            kogel_cooldown = 0

    if level == 2 and len(bricks) == 0 and ball_y + BALL_HEIGHT <= SCREEN_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "Je hebt gewonnen!"
        game_status_msg2 = ''
        game_status_msg3 = 'klik op E om naar level 3 te gaan'
        game_status = ''

        if keys[pygame.K_e]:
            level = 3
            brick_img3 = brick_img6  # gebarsten plaatje voor level 3
            bricks = bricks_level3
            ball_x = 0
            ball_y = 0
            ball_speed_x = 7
            ball_speed_y = 7
            game_status = 'playing'
            game_status_msg = 'gebruik [A] en [D] om te bewegen, [S] om te schieten'
            game_status_msg2 = 'level 3'
            kogels = []
            kogel_cooldown = 0
            game_status_msg3 = ''

    if level == 3 and len(bricks) == 0 and ball_y + BALL_HEIGHT <= SCREEN_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg = "Je hebt spel uitgespeeld!"
        game_status_msg2 = 'Toets `w` om opnieuw te beginnen'
        game_status_msg3 = ''
        game_status = ''

        if keys[pygame.K_w]:
            level = 1
            ball_speed_x = 7
            ball_speed_y = 7
            ball_x = 5
            ball_y = 100
            game_status_msg2 = 'level 1'
            game_status_msg = 'gebruik [A] en [D] om te bewegen, [S] om te schieten'
            game_status_msg3 = ''
            game_status = 'playing'
            minutes_played = 0
            seconds_played = 0
            time_played = 0
            kogels = []
            kogel_cooldown = 0
            # images terugzetten naar origineel
            brick_img3 = brick_img3_start
            brick_img = brick_img_start
            brick_img2 = brick_img2_start
            brick_img5 = brick_img5_start
            bricks = [
              {'pos': (400, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (496, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (688, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (784, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (400, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (496, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (592, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (688, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (784, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (496, 264), 'img': brick_img_start, 'health': 2},
              {'pos': (592, 264), 'img': brick_img_start, 'health': 2},
              {'pos': (688, 264), 'img': brick_img_start, 'health': 2},
              {'pos': (544, 296), 'img': brick_img_start, 'health': 2},
              {'pos': (640, 296), 'img': brick_img_start, 'health': 2},
              {'pos': (592, 328), 'img': brick_img_start, 'health': 2},
            ]
            bricks_level2 = [
              {'pos': (100, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (292, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (484, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (676, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (868, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (1060, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (196, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (388, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (580, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (772, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (964, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (100, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (292, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (484, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (676, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (868, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (1060, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (196, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (388, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (580, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (772, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (964, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (100, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (292, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (484, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (676, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (868, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (1060, 260), 'img': brick_img2_start, 'health': 2},
            ]
            bricks_level3 = [
              {'pos': (580, 140), 'img': brick_img5_start, 'health': 2},
              {'pos': (484, 172), 'img': brick_img5_start, 'health': 2},
              {'pos': (580, 172), 'img': brick_img5_start, 'health': 2},
              {'pos': (676, 172), 'img': brick_img5_start, 'health': 2},
              {'pos': (196, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (292, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (388, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (484, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (580, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (676, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (772, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (868, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (964, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (388, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (484, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (580, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (676, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (772, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (292, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (388, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (772, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (868, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (196, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (292, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (868, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (964, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (196, 332), 'img': brick_img5_start, 'health': 2},
              {'pos': (964, 332), 'img': brick_img5_start, 'health': 2},
            ]

    # bounce ball
    if ball_x < 0: 
        ball_speed_x = abs(ball_speed_x) 
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 
    if ball_y < 0: 
        ball_speed_y = abs(ball_speed_y) 

    # timer bijhouden, minuten en seconden berekenen uit totale tijd
    if game_status == "playing":
        time_played += (1 / FPS)
        total_seconds = int(time_played)
        minutes_played = total_seconds // 60
        seconds_played = total_seconds % 60

    if seconds_played < 10:
        second_zero = "0"
    else:
        second_zero = ""
    if minutes_played < 10:
        minute_zero = "0"
    else:
        minute_zero = ""

    time_text = str(minute_zero) + str(minutes_played) + ":" + str(second_zero) + str(seconds_played)

    # 
    # handle collisions
    # bal raakt onderkant scherm dus stopt want af
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        game_status_msg = "Je bent af!"
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg2 = 'Toets `w` om opnieuw te beginnen '
        game_status = ''

        if keys[pygame.K_w]:
            level = 1
            ball_speed_x = 7
            ball_speed_y = 7
            ball_x = 5
            ball_y = 100
            game_status_msg2 = 'level 1'
            game_status_msg = 'gebruik [A] en [D] om te bewegen, [S] om te schieten'
            game_status_msg3 = ''
            game_status = 'playing'
            minutes_played = 0
            seconds_played = 0
            time_played = 0
            # images terugzetten naar origineel
            brick_img3 = brick_img3_start
            brick_img = brick_img_start
            brick_img2 = brick_img2_start
            brick_img5 = brick_img5_start
            bricks = [
              {'pos': (400, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (496, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (688, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (784, 200), 'img': brick_img_start, 'health': 2},
              {'pos': (400, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (496, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (592, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (688, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (784, 232), 'img': brick_img_start, 'health': 2},
              {'pos': (496, 264), 'img': brick_img_start, 'health': 2},
              {'pos': (592, 264), 'img': brick_img_start, 'health': 2},
              {'pos': (688, 264), 'img': brick_img_start, 'health': 2},
              {'pos': (544, 296), 'img': brick_img_start, 'health': 2},
              {'pos': (640, 296), 'img': brick_img_start, 'health': 2},
              {'pos': (592, 328), 'img': brick_img_start, 'health': 2},
            ]
            bricks_level2 = [
              {'pos': (100, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (292, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (484, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (676, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (868, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (1060, 132), 'img': brick_img2_start, 'health': 2},
              {'pos': (196, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (388, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (580, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (772, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (964, 164), 'img': brick_img2_start, 'health': 2},
              {'pos': (100, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (292, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (484, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (676, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (868, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (1060, 196), 'img': brick_img2_start, 'health': 2},
              {'pos': (196, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (388, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (580, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (772, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (964, 228), 'img': brick_img2_start, 'health': 2},
              {'pos': (100, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (292, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (484, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (676, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (868, 260), 'img': brick_img2_start, 'health': 2},
              {'pos': (1060, 260), 'img': brick_img2_start, 'health': 2},
            ]
            bricks_level3 = [
              {'pos': (580, 140), 'img': brick_img5_start, 'health': 2},
              {'pos': (484, 172), 'img': brick_img5_start, 'health': 2},
              {'pos': (580, 172), 'img': brick_img5_start, 'health': 2},
              {'pos': (676, 172), 'img': brick_img5_start, 'health': 2},
              {'pos': (196, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (292, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (388, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (484, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (580, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (676, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (772, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (868, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (964, 204), 'img': brick_img5_start, 'health': 2},
              {'pos': (388, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (484, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (580, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (676, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (772, 236), 'img': brick_img5_start, 'health': 2},
              {'pos': (292, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (388, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (772, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (868, 268), 'img': brick_img5_start, 'health': 2},
              {'pos': (196, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (292, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (868, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (964, 300), 'img': brick_img5_start, 'health': 2},
              {'pos': (196, 332), 'img': brick_img5_start, 'health': 2},
              {'pos': (964, 332), 'img': brick_img5_start, 'health': 2},
            ]

    # 
    # draw everything
    #

    screen.fill('black') 

    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # teken alle kogels
    for kogel in kogels:
        screen.blit(kogel_img, (kogel['x'], kogel['y']))

    # kleur van het bericht hangt af van de situatie
    if game_status_msg == "Je hebt gewonnen!" or game_status_msg == "Je hebt spel uitgespeeld!":
        message_colour = 'green'
    elif game_status_msg == "Je bent af!":
        message_colour = 'red'
    else:
        message_colour = 'yellow'
 
    game_status_img = font.render(game_status_msg, True, message_colour)
    screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) // 2, 25))

    game_status_img2 = font.render(game_status_msg2, True, main_message_color)
    screen.blit(game_status_img2, ((SCREEN_WIDTH - game_status_img2.get_width()) // 2, 680))

    game_status_img3 = font.render(game_status_msg3, True, 'cyan')
    screen.blit(game_status_img3, ((SCREEN_WIDTH - game_status_img3.get_width()) // 2, (SCREEN_HEIGHT - game_status_img3.get_height()) // 2))

    time_count = font_small.render(time_text, True, "yellow")
    screen.blit(time_count, ((SCREEN_WIDTH - time_count.get_width()) // 2, 50))

    for brick in bricks:
        x, y = brick['pos']
        img = brick['img']
        screen.blit(img, (x, y))

    pygame.display.flip() 

    fps_clock.tick(FPS)

print('mygame stopt running')