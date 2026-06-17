import pygame, time, random

# Tea Dzegligashvili en Tamana Sedighi

# basic constanten en variabelen die worden gemaakt 
FPS = 30 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
TOTAL_LIVES = 3
HEART_WIDTH = 32
HEART_HEIGHT = 24
score = 0
frame_count = 0 # aantal frames sinds het spel is gestart (animatie paddle

# foto voor achtergrond
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()
background_img = pygame.image.load('achtergrond2.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# beginwaarden voor bal, paddle en bricks
# ballen worden in het midden van het scherm gezet, paddle onderaan en bricks worden random
# ballen gaan naar rechts en naar beneden, paddle beneden in het midden van het scherm

ball_x = 100 
ball_speed_x = 10
ball_y = 10
ball_speed_y = 8

paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100

bricks_x = []
bricks_y = []
brick_colors = []

game_over = False
game_won = False
lives = TOTAL_LIVES

def reset_game():
    #alle variabelen die buiten deze functie zijn gemaakt, worden aangeroepen met "global", anders worden ze gelezen als nieuwe (meerdere rijen, zo overzichtelijker)
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global paddle_x, paddle_y
    global bricks_x, bricks_y, brick_colors
    global game_over, game_won, lives, TOTAL_LIVES, score, frame_count
    
    # opnieuw starten, brick, ball en paddle worden op hun plekken gezet
    ball_x = 100
    ball_y = 10
    ball_speed_x = 10
    ball_speed_y = 10
    paddle_x = SCREEN_WIDTH /2 - PADDLE_WIDTH/2
    paddle_y = SCREEN_HEIGHT - 100
    game_over = False
    game_won = False
    lives = TOTAL_LIVES
    score = 0
    frame_count = 0

    # lege lijsten voor bricks, worden opnieuw gemaakt
    bricks_x = []
    bricks_y = []
    brick_colors = []

    # bricks opnieuw maken
    for row in range(6):  
        for col in range(11):  
            x = 100 + col * (BRICK_WIDTH)
            y = 100 + row * (BRICK_HEIGHT)
            bricks_x.append(x)
            bricks_y.append(y)
            brick_colors.append(random.randint(0, len(brick_imgs)-1))

#score op scherm tonen
def display_score():
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (10, 650))

# initialisatie van pygame en font, scherm en klok
pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# uit spritesheet images van ball, paddle, brick en heart
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

# verschillende soorten paddles voor animatie
paddle_img1 = pygame.Surface ((243, 64), pygame.SRCALPHA)
paddle_img1.blit(spritesheet, (0, 0), (1158, 462, 243, 64))
paddle_img1 = pygame.transform.scale(paddle_img1, (PADDLE_WIDTH, PADDLE_HEIGHT))

paddle_img2 = pygame.Surface ((243, 64), pygame.SRCALPHA)
paddle_img2.blit(spritesheet, (0, 0), (1158, 528, 243, 64))
paddle_img2 = pygame.transform.scale(paddle_img2, (PADDLE_WIDTH, PADDLE_HEIGHT))

paddle_img3 = pygame.Surface ((243, 64), pygame.SRCALPHA)
paddle_img3.blit(spritesheet, (0, 0), (1158, 594, 243, 64))
paddle_img3 = pygame.transform.scale(paddle_img3, (PADDLE_WIDTH, PADDLE_HEIGHT))

# lijst van paddle afbeeldingen voor animatie
paddle_imgs =[paddle_img1, paddle_img2, paddle_img3]

# verschillende kleuren blokken
brick_red = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_red.blit(spritesheet, (0, 0), (772, 260, 384, 128)) #rood
brick_red = pygame.transform.scale(brick_red, (BRICK_WIDTH, BRICK_HEIGHT))

brick_mintgreen = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_mintgreen.blit(spritesheet, (0, 0), (0, 130, 384, 128)) #mintgroen
brick_mintgreen = pygame.transform.scale(brick_mintgreen, (BRICK_WIDTH, BRICK_HEIGHT))

brick_darkgreen = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_darkgreen.blit(spritesheet, (0, 0), (386, 130, 384, 128)) # donkergroen
brick_darkgreen = pygame.transform.scale(brick_darkgreen, (BRICK_WIDTH, BRICK_HEIGHT))

brick_orange = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_orange.blit(spritesheet, (0, 0), (772, 0, 384, 128)) # oranje
brick_orange = pygame.transform.scale(brick_orange, (BRICK_WIDTH, BRICK_HEIGHT))

brick_darkblue = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_darkblue.blit(spritesheet, (0, 0), (772, 390, 384, 128)) # donkerblauw
brick_darkblue = pygame.transform.scale(brick_darkblue, (BRICK_WIDTH, BRICK_HEIGHT))

brick_yellow = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_yellow.blit(spritesheet, (0, 0), (386, 390, 384, 128)) #geel
brick_yellow = pygame.transform.scale(brick_yellow, (BRICK_WIDTH, BRICK_HEIGHT))

brick_lightblue = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_lightblue.blit(spritesheet, (0, 0), (386, 650, 384, 128)) #lichtblauw
brick_lightblue = pygame.transform.scale(brick_lightblue, (BRICK_WIDTH, BRICK_HEIGHT))

brick_purple = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_purple.blit(spritesheet, (0, 0), (0, 390, 384, 128)) # paars
brick_purple = pygame.transform.scale(brick_purple, (BRICK_WIDTH, BRICK_HEIGHT))

brick_bluegrey = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_bluegrey.blit(spritesheet, (0, 0), (772, 520, 384, 128)) #grijsblauw
brick_bluegrey = pygame.transform.scale(brick_bluegrey, (BRICK_WIDTH, BRICK_HEIGHT))

brick_brown = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_brown.blit(spritesheet, (0, 0), (386, 780, 384, 128)) #grijsblauw
brick_brown = pygame.transform.scale(brick_brown, (BRICK_WIDTH, BRICK_HEIGHT))

# lijst van brick afbeeldingen voor verschillende kleuren
brick_imgs = [brick_red, brick_orange, brick_yellow, brick_mintgreen, brick_darkgreen, brick_darkblue, brick_lightblue, brick_bluegrey, brick_purple, brick_brown]

heart_img = pygame.Surface((64, 64), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 64))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

# start de game met de beginwaarden
reset_game()

# game loop
print('mygame is running')
running = True
while running:
    # bewegingen, gebeurtenissen afhandelen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed() #welke toetsen worden ingedrukt
    
    if not game_over and not game_won: #uitgevoerd als er wordt gespeeld

        # ball speed verhogen na 5 seconden
        frame_count += 1
        if frame_count % (FPS * 5) == 0:
            ball_speed_x = max(-25, min(25, ball_speed_x * 1.1))
            ball_speed_y = max(-25, min(25, ball_speed_y * 1.1))

        # paddle beweging links (a) en rechts (d)
        if keys[pygame.K_d]:
            paddle_x += 18
        if keys[pygame.K_a]:
            paddle_x -= 18

        # paddle botsen tegen randen van het scherm
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH: # paddle raakt rechterkant van het scherm
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH # paddle gaat niet verder dan de rand
        if paddle_x < 0: #paddle raakt linkerkant van het scherm
            paddle_x = 0 #paddle gaat niet verder dan de rand

        # paddle botsen tegen de bal
        if (
            ball_x + BALL_WIDTH > paddle_x and #rechterkant bal
            ball_x < paddle_x + PADDLE_WIDTH and #linkerkant bal
            ball_y + BALL_HEIGHT > paddle_y and # onderkant bal
            ball_y < paddle_y + PADDLE_HEIGHT # bovenkant bal
        ):
            ball_speed_y = -abs(ball_speed_y) #ball_speed_y wordt negatief, ball gaat omhoog
            
        # beweeg bal
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # stuiter tegen randen van het scherm (links, rechts en boven)
        if ball_x < 0: #ball komt tegen linkerrand
            ball_x = 0 #ball zit precies tegen de rand
            ball_speed_x = abs(ball_speed_x) #ball  gaat naar rechts
        if ball_x + BALL_WIDTH > SCREEN_WIDTH: #ball raakt rechterrand
            ball_x = SCREEN_WIDTH - BALL_WIDTH #ball zit precies tegen de rand
            ball_speed_x = -abs(ball_speed_x) #ball_speed_x wordt negatief, ball gaat naar links
        if ball_y < 0: #ball raakt bovenrand
            ball_y = 0 # ball zit precies tegen de rand
            ball_speed_y = abs(ball_speed_y) # bal gaat naar beneden
        # game over bij onderkant
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
                ball_speed_x = 0
                ball_speed_y = 0
            else:
                ball_x = paddle_x + 40
                ball_y = paddle_y - 40
                ball_speed_x = 10
                ball_speed_y = 10
                time.sleep(1)

        # ball botst met brick
        for i in range(len(bricks_x) - 1, -1, -1):  # loop achteruit om veilig te kunnen verwijderen
            if (ball_x + BALL_WIDTH > bricks_x[i] and
                ball_x < bricks_x[i] + BRICK_WIDTH and
                ball_y + BALL_HEIGHT > bricks_y[i] and
                ball_y < bricks_y[i] + BRICK_HEIGHT):

                # botsing met bricks: pas snelheid aan
                if ball_speed_y > 0 and ball_y + BALL_HEIGHT - ball_speed_y <= bricks_y[i]: # ball botst van boven
                    ball_speed_y = -abs(ball_speed_y)
                elif ball_speed_y < 0 and ball_y - ball_speed_y >= bricks_y[i] + BRICK_HEIGHT: #ball botst van onder
                    ball_speed_y = abs(ball_speed_y)
                elif ball_speed_x > 0 and ball_x + BALL_WIDTH - ball_speed_x <= bricks_x[i]: #ball botst van links
                    ball_speed_x = -abs(ball_speed_x)
                elif ball_speed_x < 0 and ball_x - ball_speed_x >= bricks_x[i] + BRICK_WIDTH: #ball botst van rechts
                    ball_speed_x = abs(ball_speed_x)

                # verwijder geraakte brick
                del bricks_x[i]
                del bricks_y[i]
                score += 10 #per geraakte brick 10 punten erbij
                break # stop de loop na het raken van een brick
    # controleer of alle bricks zijn geraakt en of het spel gewonnen is
    if len(bricks_y) == 0:
        game_won = True
        ball_speed_x = 0
        ball_speed_y = 0

    if game_won:
        # game won tekst als alle blokjes geraakt zijn
        text = font.render("GAME WON - Druk R om te herstarten", True, (255,0,0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2)) # waar de tekst komt
        pygame.display.flip()  # laat de tekst zien

        # te resetten met R
        if keys[pygame.K_r]:
            reset_game()
        fps_clock.tick(FPS)
        continue  # sla de rest over in game over

    if game_over:
        # game over tekst als bal onderkant scherm raakt
        text = font.render("GAME OVER - Druk R om te herstarten", True, (255,0,0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2)) # waar de tekst komt
        pygame.display.flip() # laat de tekst zien

        # te resetten met R na game over
        if keys[pygame.K_r]:
            reset_game()
        fps_clock.tick(FPS)
        continue  # sla de rest over in game over
    
    # teken alles op scherm
    screen.blit(background_img, (0, 0))
    screen.blit(ball_img, (ball_x, ball_y))

    # teken paddle met animatie
    frame = (pygame.time.get_ticks() // 80) % len(paddle_imgs)
    screen.blit(paddle_imgs[frame], (paddle_x, paddle_y))

    # teken bricks
    for i in range(len(bricks_x)): 
        screen.blit(brick_imgs[brick_colors[i]], (bricks_x[i], bricks_y[i]))

    # teken levens met hearts
    for i in range(lives):
        heart_x = SCREEN_WIDTH - (i+1) * (HEART_WIDTH + 10) - 20
        heart_y = 20
        screen.blit(heart_img, (heart_x, heart_y))
    # teken score
    display_score()
    pygame.display.flip()
    fps_clock.tick(FPS)
print('mygame stopt running')