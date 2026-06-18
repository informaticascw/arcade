#
# BREAKOUT GAME
#

import pygame
import time # om tijd te gebruiken
import random #om random getallen aan te maken


# De standaard informatie
FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
PADDLE_WIDTH = 144   # paddlesize in x-direction in pixels
PADDLE_HEIGHT = 32   # paddlesize in y-direction in pixels
BRICK_HEIGHT = 32    # bricksize in y-direction in pixels
BRICK_WIDHT = 96     # bricksize in x-direction in pixels
STAR_WIDTH = 18      # starsize in x-direction in pixels
STAR_HEIGHT = 18     # starsize in y direction in pixels

star_spawned = []   # voor de check of een ster al gespawned is 


standaard_gegevens = True #bollien om alles opnieuw te laten starten
if standaard_gegevens == True:
    snelle_bal = 1.05 #snelheid van de bal met power up
    star_blit = False 
    eind_scherm = False
    faster_paddle = False #normale snelheid van paddle
    power_up_msg = ''
    timer = 1 #start van de timer, power up 
    inbeeld_kleur = 'green'
    power_up = False #power up mag niet altijd aan staan
    paddle_timer = 20 # voor hoelang de score blijft staan
    score_paddle = False
    start_scherm = True # je begint op het startscherm
    pauze_scherm = False #scherm om naar pauze te gaan
    game_over = False    # game over boolian
    game_win = False    # game win bollian
    aangeraakt = False   # aangeraakt boolian
    test_mode = False    #test-modus, zodat we zelf niet hoeven te spelen
    win_kleur = False  # kleur van de tekst: You lost! / You won! - ROOD = False
    score = 0 
    ball_x = random.randint(350, 800)            # x-position of ball in pixels
    ball_speed_x = 7      # speed of ball in x-direction in pixels per frame
    star_x = SCREEN_WIDTH / 2
    star_y = SCREEN_HEIGHT / 2
    ball_y = 100           # y-position of ball in pixels
    ball_speed_y = 10     # speed of ball in y-direction in pixels per frame
    game_status_msg = ""
    bricks_left_msg = ''
    score_msg = ""
    # ball x max spawn:890 en min:300


    bricks_x = [100, 196, 292, 100, 196, 292, 100, 196, 292, 100, 196, 292, 1084, 988, 892, 1084, 988, 892, 1084, 988, 892, 1084, 988, 892
            ]  # x-position of bricks in pixels
    bricks_y = [200, 200, 200, 168, 168, 168, 136, 136, 136, 104, 104, 104, 200, 200, 200, 168, 168, 168, 136, 136, 136, 104, 104, 104
            ]  # y-position of bricks in pixels

    totalBricks = len(bricks_x)  # de hoeveelheid bricks we in het spel hebben.

    brick_stage = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
               2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] # Je moet de bricks zovaak aanraken om ze kapot te maken

    # de plank
    PADDLE_HEIGHT = 32 #hoogte paddle
    PADDLE_WIDTH = 144 #breeddte paddle
    paddle_x = SCREEN_WIDTH / 2 - 200 #positie paddle standaard
    paddle_y = SCREEN_HEIGHT - 100 #positie paddle standaard



# init game
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()


# read images
# read spritesheet containing all images

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() #Om de spritesheet in main.py te zetten
achtergrond = pygame.image.load('achtergrond.png').convert_alpha() # om de achtergrond in main.py te zetten


#de bal
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(
    ball_img, (BALL_WIDTH, BALL_HEIGHT))  # resize image

#paddle 
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(
    paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  # resize image


# eerste blok / brick
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
brick_img.blit(spritesheet, (0, 0), (772, 0, 384, 128))
brick_img = pygame.transform.scale(
    brick_img, (BRICK_WIDHT, BRICK_HEIGHT))  # resize image

# cracked brick img
cracked_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
cracked_brick_img.blit(spritesheet, (0, 0), (772, 650, 384, 128))
cracked_brick_img = pygame.transform.scale(
    cracked_brick_img, (BRICK_WIDHT, BRICK_HEIGHT))  # resize image

# ster power up
star_img = pygame.Surface((64, 61), pygame.SRCALPHA)  # create new image
# copy part of sheet to image
star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))
star_img = pygame.transform.scale(
    star_img, (STAR_WIDTH, STAR_HEIGHT))  # resize image

#zodat alle bricks hetzelfde zijn
brick2_img = brick_img
brick3_img = brick2_img
brick4_img = brick3_img
brick5_img = brick4_img

# game loop
# zodat we kunnen zien hoeveel bricks we in het spel hebben. En andere details
print("In totaal zijn er : " + str(totalBricks) + " bricks in het spel")
print('mygame is running')
print("Startwaarde van ball (x,y): " +"(" + str(ball_x) + "," + str(ball_y)+ ")")







#game-loop
running = True
while running:
    keys = pygame.key.get_pressed()
    #hoofdmenu maken
    if start_scherm == True:
        keys = pygame.key.get_pressed()
        


        # read events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        #achtergrond
        screen.blit(achtergrond, (0, 0)) #om de achtergrond aan te maken

        #tekst op hoofdmenu
        hoofdmenu_titel = font.render("Druk op G om te starten", True, "green")
        screen.blit(hoofdmenu_titel, ((SCREEN_WIDTH/2)-250,(SCREEN_HEIGHT/2)-100)) # eerste stuk tekst
        
        hoofdmenu_uitleg = font.render('Je gaat zo met een plankje en een bal alle blokjes-', True, "green") 
        screen.blit(hoofdmenu_uitleg, ((50, SCREEN_HEIGHT/2 -50))) #tweede stuk tekst
        
        hoofdmenu_uitleg2 = font.render('proberen te breken. Druk op T voor pauze', True, 'green')
        screen.blit(hoofdmenu_uitleg2, ((50, SCREEN_HEIGHT/2 ))) #derde stuk tekst

        hoofdmenu_uitleg3 = font.render('Zet cheat-modus aan/uit door SPATIE/BACKSPACE', True, 'green')
        screen.blit(hoofdmenu_uitleg3,((150, SCREEN_HEIGHT/2 + 100 ))) #vierde stuk tekst

        #als je g klikt, begin je.
        if keys[pygame.K_g]:
            start_scherm = False
            standaard_gegevens = True





        pygame.display.flip()
        fps_clock.tick(FPS)
        continue
    
    #Pauzemenu maken maken
    if pauze_scherm == True: #het pauzescherm staat aan
        keys = pygame.key.get_pressed()
        
        star_x = star_x # om star stil te zetten


        # read events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        #achtergrond
        screen.blit(achtergrond, (0, 0))
        
        #tekst op pauze menu
        pauze_titel = font.render("PAUZE!!", True, "green")
        screen.blit(pauze_titel, ((SCREEN_WIDTH/2 -60),(SCREEN_HEIGHT/2 -90)))
        pauze_uitleg = font.render("Als je door wilt gaan, druk op G!", True, 'green')
        screen.blit(pauze_uitleg,(SCREEN_WIDTH/4 , SCREEN_HEIGHT/2 -50))


        #om door te gaan door op G te klikken
        if keys[pygame.K_g]:
            pauze_scherm = False




        pygame.display.flip()
        fps_clock.tick(FPS)
        continue
    
    #Moet er altijd in
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    
    
    #Bal laten stoppen bij game_over
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        game_over = True
        ball_speed_y = 0
        ball_speed_x = 0
    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # bal stuiteren
    if ball_x < 0:
        ball_speed_x = abs(ball_speed_x) #bal terugsturen
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:
        ball_speed_x = abs(ball_speed_x) * -1 #bal terugsturen

    if ball_y < 0:
        ball_speed_y = abs(ball_speed_y) #bal terugsturen
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        ball_speed_y = abs(ball_speed_y) * -1 #bal terugsturen
    
    # handle collisions
    # Plankje laten botsen met rand
    if paddle_x   + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x   = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x   < 0:
        paddle_x   = 0
    # Bal laten botsen met plankje
    if (ball_x + BALL_WIDTH > paddle_x   and
        ball_x < paddle_x   + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y   and
        ball_y < paddle_y   + PADDLE_HEIGHT): #als bal de paddle botst dan:
            ball_speed_y = abs(ball_speed_y) * -1  #bal terugsturen
            if test_mode == False: #als de cheatmodus niet aan staat dan:
                centre_paddle = paddle_x   + PADDLE_WIDTH / 2
                angle_ball = (ball_x - centre_paddle) / 10
                ball_speed_x = angle_ball


    # ALLE BRICK-BALL COLLISION + PRINT TERMINAL, hij print nu details die handig zijn om fouten op te sporen
    for i in range(totalBricks):
        if (ball_x + BALL_WIDTH > bricks_x[i] and
            ball_x < bricks_x[i] + BRICK_WIDHT and
            ball_y + BALL_HEIGHT > bricks_y[i] and
                ball_y < bricks_y[i] + BRICK_HEIGHT): #als bal met brick botst dan:
            print('brrick touched at ball_x = ' +
                  str(ball_x) + ' and ball_y = ' + str(ball_y))
            print(str("Brick stage:") + str(brick_stage)) #hoevaak een brick nog moet worden aangeraakt
            print( str("Total bricks: ") + str(totalBricks)) #hoeveel bricks er nog zijn
            print('Ballspeed (x,y) = ' + '('+ str(ball_speed_x) + ','+str(ball_speed_y)+ ')') #snelheid van bal
            print('')#
            #De printjes geven de host details. Wij gebruiken het om fouten op te sporen
            new_score = (random.randint(100,200)) #score aanmaken zodat als er een brick kapot is, houdt het verschillend.
            if (ball_speed_y > 0 and
                    ball_y < bricks_y[i]):
                ball_speed_y = abs(ball_speed_y) * -1      #laat de ball de andere kant op gaan
                if brick_stage[i] == 2:         #zegt in welke stage de brick is 
                    brick_stage[i] = 1
                elif brick_stage[i] == 1:
                    brick_stage.pop(i)      #zorgt ervoor dat de brick kapot gaan als ze in de laatste stage geraakt worden
                    bricks_x.pop(i)        
                    bricks_y.pop(i)
                    totalBricks = totalBricks - 1       # zorgt dat totalbricks omlaag gaat
                    score = score + new_score
                    score_paddle = True
                break
            elif (ball_speed_y < 0 and
                  ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT):
                ball_speed_y = abs(ball_speed_y)
                if brick_stage[i] == 2:
                    brick_stage[i] = 1
                elif brick_stage[i] == 1:
                    brick_stage.pop(i)
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    totalBricks = totalBricks - 1
                    score = score + new_score
                    score_paddle = True
                break
            elif (ball_speed_x > 0 and
                  ball_x < bricks_x[i]):
                ball_speed_x = abs(ball_speed_x) * -1
                if brick_stage[i] == 2:
                    brick_stage[i] = 1
                elif brick_stage[i] == 1:
                    brick_stage.pop(i)
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    totalBricks = totalBricks - 1
                    score = score + new_score
                    score_paddle = True
                break
            elif (ball_speed_x < 0 and
                  ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDHT):
                ball_speed_x = abs(ball_speed_x)
                if brick_stage[i] == 2:
                    brick_stage[i] = 1
                elif brick_stage[i] == 1:
                    brick_stage.pop(i)
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    totalBricks = totalBricks - 1
                    score = score + new_score
                    score_paddle = True
                break
            elif (ball_x + BALL_WIDTH > bricks_x[i] and     # de bovenkant van de brick vereiste iets meer code
                  ball_x < bricks_x[i] + BRICK_WIDHT and
                  ball_y + BALL_HEIGHT > bricks_y[i] and
                  ball_y < bricks_y[i] + BRICK_HEIGHT):
                ball_speed_y = abs(ball_speed_y) * -1
                aangeraakt = True
                if brick_stage[i] == 2:
                    brick_stage[i] = 1
                elif brick_stage[i] == 1:
                    brick_stage.pop(i)
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    totalBricks = totalBricks - 1
                    score = score + new_score
                    score_paddle = True
                break

   
    # clear screen zodat niet alles blijft staan
    screen.blit(achtergrond, (0, 0))


    # if dead
    if game_over == True:
        game_status_msg = "You lost!" #Berichtje tekenen dat je af bent
        win_kleur = False
        
    #sterretje maken en power up activeren
    if totalBricks == 12 and star_blit == False and 12 not in star_spawned:
       star_blit = True #maakt de star
       star_spawned.append(12)
       star_x = SCREEN_WIDTH / 2
       star_y = SCREEN_HEIGHT / 2
    elif totalBricks == 5 and star_blit == False and 5 not in star_spawned:
       star_blit = True #maakt de star
       star_spawned.append(5)
       star_x = SCREEN_WIDTH / 2
       star_y = SCREEN_HEIGHT / 2
       
    # collision met paddle
    if (star_x + STAR_WIDTH > paddle_x and
        star_x < paddle_x + PADDLE_WIDTH and
        star_y + STAR_HEIGHT > paddle_y and
        star_y < paddle_y + PADDLE_HEIGHT):
            star_blit = False
            power_up = True
            ball_speed_x *= snelle_bal
            ball_speed_y *= snelle_bal   

  #power up
    if power_up == True:
        faster_paddle = True #snellere paddle 
        timer = timer +1 #tijd begint te lopen
        print('tijd:' + str(timer)) #in termanal staat de tijd
        inbeeld_kleur = 'orange' #oranje als kleur voor de tekst

    #timer zodat power-up niet lang duurt
    if timer > 333: #tijd >333 zet je alles weer terug naar hoe het hoorde
        power_up = False
        inbeeld_kleur = 'green'
        timer = 0
        power_up_msg = False
        ball_speed_x = ball_speed_x / snelle_bal
        ball_speed_y = ball_speed_y / snelle_bal
        faster_paddle = False    

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    # draw brick
    for i in range(totalBricks):
        if brick_stage[i] == 2:
            screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
        elif brick_stage[i] == 1:
            screen.blit(cracked_brick_img, (bricks_x[i], bricks_y[i])) #tekent de cracked_bricks als die er nogi zijn

    # plankje tekenen
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # score tonen op paddle
    if score_paddle == True:
        score_paddle_img = font.render('+' + str(new_score), True, inbeeld_kleur)
        screen.blit(score_paddle_img, (paddle_x +19, paddle_y +5)) # voor paddle 1
        #screen.blit(score_paddle_img, (paddle2_x +19, paddle2_y +5)) #voor paddle 2
        paddle_timer = paddle_timer -1
        if paddle_timer < 1:
            score_paddle = False
            paddle_timer = 20


    # plankje bewegen 
    if faster_paddle == True:
        if keys[pygame.K_d]:
            paddle_x = paddle_x + 25 #beweegt de paddle met normale snelheid
        if keys[pygame.K_a]:
            paddle_x = paddle_x - 25 #beweegt de paddle met normale snelheid
    elif faster_paddle == False:
        if keys[pygame.K_d]:
            paddle_x = paddle_x + 15 #beweegt de paddle met hooge snelheid
        if keys[pygame.K_a]:
            paddle_x = paddle_x - 15 #beweegt de paddle met hooge snelheid
    

    #De test mode, a.k.a. de automatische piloot
    if test_mode == True:
        centre_paddle = paddle_x + PADDLE_WIDTH / 2
        paddle_x = ball_x - (PADDLE_WIDTH / 2)  #stuurt bal terug
        if (ball_x == centre_paddle and 
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT):
            ball_speed_y = abs(ball_speed_y) * -1 #stuurt bal terug
            



    #om test = cheat mode aan te zetten, en uit
    if keys[pygame.K_SPACE]:
        test_mode = True

    if keys[pygame.K_BACKSPACE]:
        test_mode = False
    
    
    
    #Om het pauzescherm te openen
    if keys[pygame.K_t]:
        screen.blit(achtergrond,(0,0))
        pauze_scherm = True #pauze scherm aanzetten als je T drukt


    # als gewonnen dan bal stoppen en berichtje geven
    if totalBricks == 0:
        game_status_msg = "You win!" #berichtje dat je hebt gewonnen
        win_kleur = True
        ball_speed_x = 0
        ball_speed_y = 0 #bal stilzetten
        game_over = True

    # Kleur van tekst
    if win_kleur == False:
        win_kleur = 'red' #als je hebt verloren is de tekst rood
    elif win_kleur == True:
        win_kleur = 'lightgreen' #als je hebt gewonnen is de tekst lichtgroen


    #draw score
    if game_over or game_win == True:
        score_msg =  'score: ' + str(round(score,3))# maakt de score mooi in beeld en zorgt dat het niet te groot komma getal is
        score_img = font.render(score_msg, True, inbeeld_kleur) 
        screen.blit(score_img, (700,300))

    #de normale rechs-boven positie, de andere zet hem in het midden
    else:
        score_msg =  'score: ' + str(round(score,3))# maakt de score mooi in beeld en zorgt dat het niet te groot komma getal is
        score_img = font.render(score_msg, True, inbeeld_kleur) 
        screen.blit(score_img, (900,20))       



    #bricks left message in het scherm
    if game_over or game_win == True:
        bricks_left_msg = "Total bricks left: " + str(totalBricks)
        bricks_left_img = font.render(bricks_left_msg, True, inbeeld_kleur)
        screen.blit(bricks_left_img, (140,300)) #laat de tekst in het midden staan
        random_getal = 0
        time = 0
        power_up = False
        inbeeld_kleur = 'green'
        
    else:
        bricks_left_msg = "Total bricks left: " + str(totalBricks)
        bricks_left_img = font.render(bricks_left_msg, True, inbeeld_kleur)
        screen.blit(bricks_left_img, (20,20)) #laat de tekst mooi boven staan


    #Om de ster te gaan tekenen
    if star_blit == True:
        star_y += 2
        screen.blit(star_img, (star_x, star_y))

    elif star_blit == False:
        star_x = 6000 #zodat de ster uit beeld is
        star_y = 3000
    


    # draw game status message
    game_status_img = font.render(game_status_msg, True, win_kleur)
    screen.blit(game_status_img, ((550), (360)))
 

    





    # show screen
    pygame.display.flip()

    #
    # wait until next frame


    fps_clock.tick(FPS)  # Sleep the remaining time of this frame






print('mygame stopt running')
