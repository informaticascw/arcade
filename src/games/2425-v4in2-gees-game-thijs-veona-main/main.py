
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280     # Schrem breedte
SCREEN_HEIGHT = 720     # Scherm hoogte
BALL_WIDTH = 16         # Bal breedte
BALL_HEIGHT = 16        # Bal hoogte
PADDLE_WIDTH = 144      # Plank breedte
PADDLE_HEIGHT = 32      # Plank hoogte
BRICK_WIDTH = 96        # Blok breedte
BRICK_HEIGHT = 32       # Blok hoogte
HEART_WIDTH = 40        # Hart (levens) breedte
HEART_HEIGHT = 40       # Hart (levens) hoogte
STAR_WIDTH = 30
STAR_HEIGHT = 30
# move ball


# define global variables
game_status_msg = ""

def display_score(): # Score spel
    score_text = small_font.render(f"Score: {score}", True, (255, 0, 0))  # Rood
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 20))       # Midden bovenaan
    screen.blit(score_text, text_rect)

score = 0   # Score variable

levens = 3  # Levens variable

vallende_ster = []

glitters = []
import random

ball_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2  # Bal startpunt (horizontaal)
ball_speed_x = 10                             # Bal snelheid
ball_x = ball_x + ball_speed_x                # Bal beweging

ball_y = SCREEN_HEIGHT - 120                  # Bal startpunt (verticaal)
ball_speed_y = 8                              # Bal snelheid
ball_y = ball_y + ball_speed_y                # Bal beweging


paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2  # Plank startpunt (horizontaal)
paddle_y = SCREEN_HEIGHT - 100                  # Plank startpunt (verticaal)


hearts_x = [10,50,90]     # Levens positie lijst (horizontaal)
hearts_y = [10,10,10]     # Levens positie lijst (verticaal)


bricks_x = [156, 156, 156, 156, 156, 156,       # Blok positie lijst (horizontaal)
            252, 252, 252, 252, 252, 252,
            348, 348, 348, 348, 348, 348,
            444, 444, 444, 444, 444, 444,
            540, 540, 540, 540, 540, 540,
            636, 636, 636, 636, 636, 636,
            732, 732, 732, 732, 732, 732,
            828, 828, 828, 828, 828, 828,
            924, 924, 924, 924, 924, 924, 
            1020, 1020, 1020, 1020, 1020, 1020]

bricks_y = [112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,       # Blok positie lijst (verticaal)
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272]

bricks_x2 = [156, 156, 156, 156, 156, 156,       # Blok positie lijst (horizontaal)
             252, 252, 252, 252, 252, 252,
             348, 348, 348, 348, 348, 348,
             444, 444, 444, 444, 444, 444,
             540, 540, 540, 540, 540, 540,
             636, 636, 636, 636, 636, 636,
             732, 732, 732, 732, 732, 732,
             828, 828, 828, 828, 828, 828,
             924, 924, 924, 924, 924, 924, 
             1020, 1020, 1020, 1020, 1020, 1020]

bricks_y2 = [112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,       # Blok positie lijst (verticaal)
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272,
            112, 144, 176, 208, 240, 272]


# Variablen voor de loop
i = 0
l = 0
k = 0
p = 0
a = 0
q = 0


pygame.init()
font = pygame.font.SysFont('default', 64) # Lettertype
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)  # Scherm
fps_clock = pygame.time.Clock()  # Beheer van framesnelheid

small_font = pygame.font.SysFont('arial', 28) # Lettertype (kleine tekst)
# init game

game_status = "intro"  # Variable voor beginscherm, verliesscherm en winscherm

versnelling = 1  # Variable voor de versnelling van de bal

gekozen_level = 1  # Variable voor de gekozen level van versnelling
#
# read images
#
#afbeeldingen
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()    # Laad en bereid afbeelding voor 

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)                         # Afbeeldig bal
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)                      # Afbeelding plank
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64)) 
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) 

brick_img1 = pygame.Surface((384, 128), pygame.SRCALPHA)                     # Afbeelding blok
brick_img1.blit(spritesheet, (0, 0), (0, 130, 384, 128)) 
brick_img1 = pygame.transform.scale(brick_img1, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img2 = pygame.Surface((384, 128), pygame.SRCALPHA)                     # Afbeelding blok
brick_img2.blit(spritesheet, (0, 0), (0, 260, 384, 128)) 
brick_img2 = pygame.transform.scale(brick_img2, (BRICK_WIDTH, BRICK_HEIGHT))


heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)                        # Afbeelding hart (levens)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

star_img = pygame.Surface((64, 58), pygame.SRCALPHA)                        # Afbeelding ster 
star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))

# game loop
# Game laten werken
print('mygame is running')
running = True
while running:
    #
    # Read events]
    #
    for event in pygame.event.get(): # Afsluiten spel 
        if event.type == pygame.QUIT:  
            running = False 
   
    keys = pygame.key.get_pressed() # Indrukken toetsen

    if game_status == "intro":  # Beginscherm met uitleg
        screen.fill('black')
        intro_font = pygame.font.SysFont('sans serif', 48)
        text1 = intro_font.render('Welkom bij Breakout!', True, (255, 255, 255))
        text2 = intro_font.render('Gebruik A en D om te bewegen.', True, (255, 255, 255))
        text3 = intro_font.render('Druk op Q om te starten.', True, (181, 50, 128))
        text4 = intro_font.render('Kies je level van moeilijkheid uit: ', True, (255, 255, 255))
        text5 = intro_font.render('Druk 1 = Makkelijk ', True, (255, 255, 255))
        text6 = intro_font.render('Druk 2 = Normaal ', True, (255, 255, 255))
        text7 = intro_font.render('Druk 3 = Moeilijk ', True, (255, 255, 255))

        screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(text5, (SCREEN_WIDTH // 2 - text5.get_width() // 2, SCREEN_HEIGHT // 2 + 140))
        screen.blit(text6, (SCREEN_WIDTH // 2 - text6.get_width() // 2, SCREEN_HEIGHT // 2 + 180))
        screen.blit(text7, (SCREEN_WIDTH // 2 - text7.get_width() // 2, SCREEN_HEIGHT // 2 + 220))


        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:  # Starten spel
            game_status = "playing"

        if keys[pygame.K_1]:     # Kiezen van versnelling 1
           versnelling = 1
           gekozen_level = 1
        elif keys[pygame.K_2]:   # Kiezen van versnelling 2
           versnelling = 1.01
           gekozen_level = 2
        elif keys[pygame.K_3]:   # Kiezen van versnelling 3
           versnelling = 1.03
           gekozen_level = 3
        fps_clock.tick(FPS)
        continue 
    
    elif game_status == "lose":  # Verliesscherm
        screen.fill((100,10,10))
        lose_font = pygame.font.SysFont('arial', 40)
        text = lose_font.render('GAME OVER! Druk R om opnieuw te starten.', True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        if keys[pygame.K_r]:
            # Alles opniew herstellen
            levens = 3
            score = 0
            hearts_x = [10, 50, 90]
            hearts_y = [10, 10, 10]
            bricks_x = [156, 156, 156, 156, 156, 156,
                        252, 252, 252, 252, 252, 252,
                        348, 348, 348, 348, 348, 348,
                        444, 444, 444, 444, 444, 444,
                        540, 540, 540, 540, 540, 540,
                        636, 636, 636, 636, 636, 636,
                        732, 732, 732, 732, 732, 732,
                        828, 828, 828, 828, 828, 828,
                        924, 924, 924, 924, 924, 924, 
                        1020, 1020, 1020, 1020, 1020, 1020]
            bricks_x2 = [156, 156, 156, 156, 156, 156,
                        252, 252, 252, 252, 252, 252,
                        348, 348, 348, 348, 348, 348,
                        444, 444, 444, 444, 444, 444,
                        540, 540, 540, 540, 540, 540,
                        636, 636, 636, 636, 636, 636,
                        732, 732, 732, 732, 732, 732,
                        828, 828, 828, 828, 828, 828,
                        924, 924, 924, 924, 924, 924, 
                        1020, 1020, 1020, 1020, 1020, 1020]
            bricks_y = [112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,       # Blok positie lijst (verticaal)
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272,
                       112, 144, 176, 208, 240, 272]
            bricks_y2 = [112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,       # Blok positie lijst (verticaal)
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272,
                         112, 144, 176, 208, 240, 272]
            ball_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
            ball_y = SCREEN_HEIGHT - 120
            ball_speed_x = 10
            ball_speed_y = 8
            paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2  
            paddle_y = SCREEN_HEIGHT - 100
            vallende_ster = []  
            gekozen_level = 1
            game_status = "intro"
        fps_clock.tick(FPS)
        continue

    elif game_status == "win":   # Winscherm
        screen.fill((13,95,43))
        win_font = pygame.font.SysFont('arial', 40)
        text = win_font.render('YOU WIN! Druk R om opnieuw te starten.', True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        if keys[pygame.K_r]:
            # Alles opnieuw herstellen
            levens = 3
            score = 0
            hearts_x = [10, 50, 90]
            hearts_y = [10, 10, 10]
            bricks_x = [156, 156, 156, 156, 156, 156,
                        252, 252, 252, 252, 252, 252,
                        348, 348, 348, 348, 348, 348,
                        444, 444, 444, 444, 444, 444,
                        540, 540, 540, 540, 540, 540,
                        636, 636, 636, 636, 636, 636,
                        732, 732, 732, 732, 732, 732,
                        828, 828, 828, 828, 828, 828,
                        924, 924, 924, 924, 924, 924, 
                        1020, 1020, 1020, 1020, 1020, 1020]
            bricks_x2 = [156, 156, 156, 156, 156, 156,      
                         252, 252, 252, 252, 252, 252,
                         348, 348, 348, 348, 348, 348,
                         444, 444, 444, 444, 444, 444,
                         540, 540, 540, 540, 540, 540,
                         636, 636, 636, 636, 636, 636,
                         732, 732, 732, 732, 732, 732,
                         828, 828, 828, 828, 828, 828,
                         924, 924, 924, 924, 924, 924, 
                         1020, 1020, 1020, 1020, 1020, 1020]
            bricks_y = [112, 144, 176, 208, 240, 272] * 10
            bricks_y2 = [112, 144, 176, 208, 240, 272] * 10
            ball_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
            ball_y = SCREEN_HEIGHT - 120
            ball_speed_x = 10
            ball_speed_y = 8
            paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2 
            paddle_y = SCREEN_HEIGHT - 100
            vallende_ster = [] 
            gekozen_level = 1
            game_status = "intro"
        fps_clock.tick(FPS)
        continue


    if game_status != "playing":
      continue
   
    

    # Move everything
    game_over = False
    
  # Voeg nieuwe glitter toe
    if random.random() < 0.2:  
      glitters.append({
        'x': random.randint(0, SCREEN_WIDTH),
        'y': 0,
        'radius': random.randint(1, 2),
        'speed': random.uniform(0.3, 0.8)
    })

    for g in glitters:
      g['y'] += g['speed']
    glitters = [g for g in glitters if g['y'] < SCREEN_HEIGHT]

    # Bewegen bal
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # Plank
    paddle_y =  paddle_y
    paddle_x = paddle_x

    # Blok
    bricks_y = bricks_y
    bricks_x = bricks_x

    # Botsing plank
    if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT):
       ball_speed_y = abs(ball_speed_y) * -1

    # Stuiteren van bal
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x)  # Beweegt de andere kant op
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1 

    if ball_y < 0 : 
      ball_speed_y = abs(ball_speed_y)   # Beweegt de andere kant op
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
      ball_speed_y = abs(ball_speed_y) * -1 

    # Bewegen plank door toetsen in te drukken
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_d] : # Toets D ingedrukt
      paddle_x += 30      # Plank gaat naar links
    if keys[pygame.K_a] : # Toets A ingedrukt
       paddle_x -= 30     # Plank gaat naar rechts

    # Botsing plank tegen randen
    if paddle_x < 0:
      paddle_x = 0
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH


    # Als je af gaat
    for p in range (0, len(hearts_x)):
      if ball_y > 700:
        ball_x = paddle_x
        ball_y = paddle_y 
     
        levens = levens -1
  
        hearts_x.pop(p)
        break
    
    if levens == 0:
      game_over = True
      ball_speed_x = 0
      ball_speed_y = 0
      game_status = "lose"
      continue 
    

    if len(bricks_x) == 0:
      game_status = "win"

    

   

    # 
    # handle collisions

    # Botsing bal tegen blokken

    if bricks_x == bricks_x:
      for l in range (0, len(bricks_x)):
        if (ball_x + BALL_WIDTH > bricks_x[l] and
        ball_x < bricks_x[l] + BRICK_WIDTH and
        ball_y + BALL_HEIGHT > bricks_y[l] and
        ball_y < bricks_y[l] + BRICK_HEIGHT):
      
          if ball_speed_y > 0 and ball_y + BALL_HEIGHT <= bricks_y[l] + BRICK_HEIGHT: 
            ball_speed_y *= -1
          elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y[l] + BRICK_HEIGHT: 
            ball_speed_y *= -1
          elif ball_speed_x > 0 and ball_x + BALL_WIDTH   <= bricks_x[l] + BRICK_WIDTH: 
            ball_speed_x *= -1
          elif ball_speed_x < 0 and ball_x + BALL_WIDTH  >= bricks_x[l] + BRICK_WIDTH: 
            ball_speed_x *= -1   

          bricks_x.pop(l)
          bricks_y.pop(l)
          score += 5
          if gekozen_level > 1:
            ball_speed_x *= versnelling
            ball_speed_y *= versnelling
          break

    
      

      else :
        for a in range (0, len(bricks_x2)):
          if (ball_x + BALL_WIDTH > bricks_x2[a] and
          ball_x < bricks_x2[a] + BRICK_WIDTH and
          ball_y + BALL_HEIGHT > bricks_y2[a] and
          ball_y < bricks_y2[a] + BRICK_HEIGHT):
      
            if ball_speed_y > 0 and ball_y + BALL_HEIGHT <= bricks_y2[a] + BRICK_HEIGHT: 
              ball_speed_y *= -1
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT >= bricks_y2[a] + BRICK_HEIGHT: 
              ball_speed_y *= -1
            elif ball_speed_x > 0 and ball_x + BALL_WIDTH   <= bricks_x2[a] + BRICK_WIDTH: 
              ball_speed_x *= -1
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH  >= bricks_x2[a] + BRICK_WIDTH: 
              ball_speed_x *= -1   

            vallende_ster.append([bricks_x2[a], bricks_y2[a]])
            bricks_x2.pop(a)
            bricks_y2.pop(a)
            score += 10
            
            if gekozen_level > 1:
              ball_speed_x *= versnelling
              ball_speed_y *= versnelling
            break
    


    # draw everything
    #

    # clear screen
    screen.fill((112, 193, 179)) # Kleur achtergrond

    for g in glitters:
      pygame.draw.circle(screen, (211, 175, 55), (int(g['x']), int(g['y'])), g['radius'])


    # Tekenen van bal
    screen.blit(ball_img, (ball_x, ball_y)) 
    screen.blit(paddle_img,(int(paddle_x), int(paddle_y)))

    # Tekenen blokken

    for q in range (0, len(bricks_x2)):
      screen.blit(brick_img2, (bricks_x2[q], bricks_y2[q]))
      q = q + 1

    for i in range (0, len(bricks_x)):
      screen.blit(brick_img1, (bricks_x[i], bricks_y[i]))
      i = i + 1

    # Tekenen harten (levens)
    game_status_img = font.render(game_status_msg, True, 'green')
    screen.blit(game_status_img, (SCREEN_WIDTH / 2 - 100, 360))
    for k in range (0, len(hearts_x)):
      screen.blit(heart_img, (hearts_x[k],hearts_y[k]))
      k = k + 1

  

  
    # Tekenen van score
    display_score()

    for ster in vallende_ster:
      ster[1] += 5  # Laat ze vallen met snelheid 5 pixels per frame

    for ster in vallende_ster:
      screen.blit(star_img, (ster[0], ster[1]))

    vallende_ster = [ster for ster in vallende_ster if ster[1] < SCREEN_HEIGHT]


    # Tekenen tekst van level
    level_text = small_font.render(f"Level: {gekozen_level}", True, (255, 255, 255))
    level_rect = level_text.get_rect(topright=(SCREEN_WIDTH - 20, 20)) 
    screen.blit(level_text, level_rect)

    # show screen
    pygame.display.flip() # Laat scherm zien

    # 
    
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
