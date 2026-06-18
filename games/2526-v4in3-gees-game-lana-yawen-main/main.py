#
# BREAKOUT GAME
#

import pygame
import time
import os
import random
#
# definitions
#

# definitions
# define global variables]
player_name = ""
naam_invoeren = False
highscores = []
gesorteerd = []
game_status_msg = ""
score_status_msg = ""
MENU = 5
UITLEG = 6
bg_offset = 0
menu_optie = 0
menu_opties = ["PLAY", "UITLEG", "HIGHSCORE"]
game_status = MENU  # verander START naar MENU
FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
# bal
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
ball_x = 0           # x-position of ball in pixels
ball_speed_x = 8    # speed of ball in x-direction in pixels per frame
ball_y = 0
ball_speed_y = 8
# plankje
PADDLE_WIDTH = 144     # paddle size in x-direction in pixels
PADDLE_HEIGHT = 32     # paddle size in y-direction in pixels
paddle_width_current = PADDLE_WIDTH
paddle_boost_timer = 0  # TIMER VOOR BOOST
PADDLE_BOOST_DURATION = 600  # 20 seconden (30 FPS * 20 = 600 frames)
paddle_x = 600
paddle_y = 650
# blokje
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
BRICKCRACKED_WIDTH = 96
BRICKCRACKED_HEIGHT = 32
score = 0
highscore = 0
HART_WIDTH = 51.2
HART_HEIGHT = 46.4
STAR_WIDTH = 25.6
STAR_HEIGHT = 24.4
STAR_SPEED = 8
star_x = []
star_y = []
stars_spawned_this_level = 0
MAX_STARS_PER_LEVEL = 3
star_effects = []
star_brick_indices = []
aantalharten = 4
aantalballen = 1
levels = 0
harten_x = [20, 90, 160, 230]
harten_y = [20, 20, 20, 20]
brick_effects = []


def load_level(n):
    global bricks_x, bricks_y, bricks_hitsleft, ball_speed_x, ball_speed_y
    global star_brick_indices, paddle_width_current, paddle_boost_timer
    global stars_spawned_this_level
    data = LEVELS[n]
    bricks_x = data["bricks_x"][:]
    bricks_y = data["bricks_y"][:]
    bricks_hitsleft = [2] * len(bricks_x)
    print(bricks_hitsleft)
    ball_speed_x = data["ball_speed_x"]
    ball_speed_y = -data["ball_speed_y"]
    stars_spawned_this_level = 0  # RESET
    star_x.clear()
    star_y.clear()
    star_effects.clear()
    # kiest 3 random blokken die sterren krijgen
    star_brick_indices = random.sample(
        range(len(bricks_x)), min(3, len(bricks_x)))
    paddle_width_current = PADDLE_WIDTH
    paddle_boost_timer


LEVELS = [

    {
        "bricks_x": [
            256, 352, 448, 544, 640, 736, 832, 928,
            256, 352, 448, 544, 640, 736, 832, 928,
            256, 352, 448, 544, 640, 736, 832, 928,
            256, 352, 448, 544, 640, 736, 832, 928],
        "bricks_y": [
            120, 120, 120, 120, 120, 120, 120, 120,
            180, 180, 180, 180, 180, 180, 180, 180,
            240, 240, 240, 240, 240, 240, 240, 240,
            300, 300, 300, 300, 300, 300, 300, 300],
        "ball_speed_x": 8,
        "ball_speed_y": 8
    },


    {
        "bricks_x": [544, 640, 496, 688, 448, 736, 400, 784, 400, 784, 448, 736, 496, 688, 544, 640, 592],
        "bricks_y": [180, 180, 212, 212, 276, 276, 340, 340, 404, 404, 468, 468, 532, 532, 564, 564, 372],
        "ball_speed_x": 8,
        "ball_speed_y": 8



    },


    {
        "bricks_x": [688, 784, 880, 976, 976, 976, 880, 784, 688, 592, 496, 400, 304, 208, 208, 208, 304, 400, 496, 592, 592, 688, 496, 592],
        "bricks_y": [418, 386, 354, 322, 290, 258, 226, 194, 226, 258, 418, 386, 354, 322, 290, 258, 226, 194, 226, 162, 354, 130, 130, 450],
        "ball_speed_x": 8,
        "ball_speed_y": 8

    }
]


gamewin = 0
gamelost = 0

if os.path.exists("highscore.txt"):
    bestand = open("highscore.txt", "r")
    highscore = int(bestand.read())
    bestand.close()
else:
    highscore = 0
if os.path.exists("scoreboard.txt"):
    bestand = open("scoreboard.txt", "r")
    highscores = bestand.readlines()
    bestand.close()
    for regel in highscores:
        if "," in regel:
            naam, scoretekst = regel.strip().split(",")
            gesorteerd.append((naam, int(scoretekst)))
    gesorteerd.sort(key=lambda x: x[1], reverse=True)
else:
    highscores = []

#
# init game
#

# init game
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
klein_font = pygame.font.Font('PressStart2P-Regular.ttf', 14)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()
#
# read images
#

# read images

# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

# Ball; create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
# PLANKJEE
# Paddle; create empty image of 144 x 32 pixels, SRCALPHA supports transparency
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
# copy part (x="1158" y="396" width="243" height="64") from spritesheet to ball_img at (0,0)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
# resize paddle_img from 144 x 32 pixels to PADDLE_WIDTH x PADDLE_HEIGHT
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))


# Brickcracked; create empty image of 96 x 32 pixels, SRCALPHA supports transparency
brickcracked_img = pygame.Surface((384, 128), pygame.SRCALPHA)
# copy part (x="772" y="390" width="384" height="128") from spritesheet to ball_img at (0,0)
brickcracked_img.blit(spritesheet, (0, 0), (0, 0, 384, 128))
# resize ball_img from 64 x 64 pixels to BRICK_WIDTH x BRICK_HEIGHT
brickcracked_img = pygame.transform.scale(
    brickcracked_img, (BRICKCRACKED_WIDTH, BRICKCRACKED_HEIGHT))

# brick purple
# Brick; create empty image of 96 x 32 pixels, SRCALPHA supports transparency
brickp_img = pygame.Surface((384, 128), pygame.SRCALPHA)
# copy part (x="772" y="390" width="384" height="128") from spritesheet to ball_img at (0,0)
brickp_img.blit(spritesheet, (0, 0), (0, 390, 384, 128))
# resize ball_img from 64 x 64 pixels to BRICK_WIDTH x BRICK_HEIGHT
brickp_img = pygame.transform.scale(brickp_img, (BRICK_WIDTH, BRICK_HEIGHT))

# BRICKKK BLUEEEE
# Brick; create empty image of 96 x 32 pixels, SRCALPHA supports transparency
brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
# copy part (x="0" y="390" width="384" height="128") from spritesheet to ball_img at (0,0)
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
# resize ball_img from 64 x 64 pixels to BRICK_WIDTH x BRICK_HEIGHT
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

# hartje
# Hart; create empty image of 64 x 64 pixels, SRCALPHA supports transparency
hart_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1637, y-top=652, width=64, height=64) from spritesheet to hart_img at (0,0)
hart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 64))
# resize hart.img from 64 x 64 pixels to HART_WIDTH x HART_HEIGHT
hart_img = pygame.transform.scale(hart_img, (HART_WIDTH, HART_HEIGHT))

# star
# Star; create empty image of 64 x 64 pixels, SRCALPHA supports transparency
star_img = pygame.Surface((64, 61), pygame.SRCALPHA)
# copy part (x-left=772, y-top=846, width=64, height=61) from spritesheet to star_img at (0,0)
star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))
# resize star.img from 64 x 61 pixels to STAR_WIDTH x STAR_HEIGHT
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))
#
# game loop
#

# game play
PLAY = 1
START = 2
EIND = 3
HIGH = 4
game = []
game_status = MENU
print('mygame is running')
running = True
load_level(0)
current_level = 0
for i in range(len(bricks_x)):
    print(bricks_x[i], bricks_y[i])

while running:

    #
    # read events: lezen gebeurtenissen,
    #
    keys = pygame.key.get_pressed()
    if game_status == MENU:
        screen.fill("pink")
        titel_img = font.render(
            "BREAKOUT GAME Lana & Yawen", True, (180, 0, 80))
        screen.blit(titel_img, (370, 150))
        for i, optie in enumerate(menu_opties):
            kleur = (180, 0, 80) if i == menu_optie else "black"
            pijl = "> " if i == menu_optie else "  "
            tekst = font.render(pijl + optie, True, kleur)
            screen.blit(tekst, (520, 300 + i * 70))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_status == MENU:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    menu_optie = (menu_optie - 1) % len(menu_opties)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    menu_optie = (menu_optie + 1) % len(menu_opties)
                if event.key == pygame.K_RETURN or event.key == pygame.K_d:
                    if menu_optie == 0:
                        player_name = ""
                        naam_invoeren = False
                        gamewin = 0
                        gamelost = 0
                        game_status_msg = ""
                        aantalharten = 4
                        load_level(0)
                        current_level = 0
                        score = 0
                        harten_x = [20, 90, 160, 230]
                        harten_y = [20, 20, 20, 20]
                        ball_x = SCREEN_WIDTH // 2
                        ball_y = 100

                        game_status = PLAY
                    elif menu_optie == 1:
                        game_status = UITLEG
                    elif menu_optie == 2:
                        game_status = HIGH

            if game_status == UITLEG:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_a:
                    game_status = MENU
            if game_status == HIGH:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_a:
                    game_status = MENU

            if game_status == EIND and not naam_invoeren:
                if event.key == pygame.K_RETURN or event.key == pygame.K_a:
                    gamewin = 0
                    gamelost = 0
                    game_status = MENU

            if naam_invoeren:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    bestand = open("scoreboard.txt", "a")
                    bestand.write(player_name + "," + str(score) + "\n")
                    bestand.close()
                    bestand = open("scoreboard.txt", "r")
                    highscores = bestand.readlines()
                    bestand.close()
                    naam_invoeren = False
                    game_status = HIGH
                    gesorteerd.clear()
                    for regel in highscores:
                        naam, scoretekst = regel.strip().split(",")
                        gesorteerd.append((naam, int(scoretekst)))
                    gesorteerd.sort(key=lambda x: x[1], reverse=True)
                else:
                    if len(player_name) < 2:
                        letter = event.unicode.upper()
                        if letter.isalpha():
                            player_name += letter

    #
    # move everything
    #
    if game_status == PLAY:
        # UPDATE PADDLE BOOST TIMER
        if paddle_boost_timer > 0:
            paddle_boost_timer -= 1
        else:
            paddle_width_current = PADDLE_WIDTH  # Reset naar origineel

        ball_x = ball_x + ball_speed_x
        for i in range(len(star_y)):
            star_y[i] += STAR_SPEED
        # bounce ball against edges of screen
        if ball_x < 0:  # left edge
            ball_speed_x = abs(ball_speed_x)  # positive x-speed = move right
        if ball_x + BALL_WIDTH > SCREEN_WIDTH:  # right edge
            # negative x-speed = move left
            ball_speed_x = abs(ball_speed_x) * -1
        # move ball
        ball_y = ball_y + ball_speed_y
        # bounce ball against edges of screen
        if ball_y < 0:  # left edge
            ball_speed_y = abs(ball_speed_y)  # positive y-speed = move up
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:  # right edge
            # negative y-speed = move down
            ball_speed_y = abs(ball_speed_y) * -1
        # gegevens
        rechterkant_bal = ball_x + BALL_WIDTH
        linkerkant_bal = ball_x
        bovenkant_bal = ball_y
        onderkant_bal = ball_y + BALL_HEIGHT

        # paddle
        linkerkant_paddle = paddle_x
        rechterkant_paddle = paddle_x + paddle_width_current
        bovenkant_paddle = paddle_y
        onderkant_paddle = paddle_y + PADDLE_HEIGHT

        # bounce ball on paddle only when the ball is moving downwards
        if (ball_speed_y > 0 and
            rechterkant_bal > linkerkant_paddle and
            linkerkant_bal < rechterkant_paddle and
            onderkant_bal > bovenkant_paddle and
                bovenkant_bal < onderkant_paddle):

            # move ball above the paddle to prevent repeat collision
            ball_y = paddle_y - BALL_HEIGHT
            # reflect vertical direction
            ball_speed_y = -abs(ball_speed_y)

            # change x direction based on hit position on the paddle
            midden_paddle = paddle_x + PADDLE_WIDTH / 2
            midden_bal = ball_x + BALL_WIDTH / 2
            verschil = (midden_bal - midden_paddle) / (PADDLE_WIDTH / 2)
            ball_speed_x = verschil * abs(ball_speed_y)

            # keep a reasonable horizontal/vertical speed
            if abs(ball_speed_x) > 12:
                ball_speed_x = 12 if ball_speed_x > 0 else -12
            if abs(ball_speed_y) > 12:
                ball_speed_y = 12 if ball_speed_y > 0 else -12

        # check of bal tegen brick aan komt

        for i in range(len(star_x)):
            rechterkant_star = star_x[i] + STAR_WIDTH
            linkerkant_star = star_x[i]
            bovenkant_star = star_y[i]
            onderkant_star = star_y[i] + STAR_HEIGHT

            if (rechterkant_star > linkerkant_paddle and
                linkerkant_star < rechterkant_paddle and
                onderkant_star > bovenkant_paddle and
                    bovenkant_star < onderkant_paddle):

                # ster effect
                star_effects.append({
                    "x": star_x[i],
                    "y": star_y[i],
                    "alpha": 255,
                    "size": STAR_WIDTH,
                    "speed": 8
                })

                star_x.pop(i)
                star_y.pop(i)
                paddle_width_current += 50
                paddle_boost_timer = PADDLE_BOOST_DURATION  # Start 10 sec timer

                score += 25  # plus score
                break

        for i in range(len(bricks_x)):
            brick_x = bricks_x[i]
            brick_y = bricks_y[i]
            if (rechterkant_bal > brick_x and
                linkerkant_bal < brick_x + BRICK_WIDTH and
                onderkant_bal > brick_y and
                    bovenkant_bal < brick_y + BRICK_HEIGHT):

                print("eerste hit")

                # if bal raak bovenkant
                if ball_speed_y > 0 and bovenkant_bal < brick_y:
                    ball_speed_y = abs(ball_speed_y) * -1
                # if ball raak onderkant
                elif ball_speed_y < 0 and onderkant_bal > brick_y + BRICK_HEIGHT:
                    ball_speed_y = abs(ball_speed_y)
                # if ball raakt rechterkant
                elif ball_speed_x < 0 and linkerkant_bal < brick_x + BRICK_WIDTH:
                    ball_speed_x = abs(ball_speed_x)
                # if ball raakt linkerkant
                elif ball_speed_x > 0 and rechterkant_bal > brick_x:
                    ball_speed_x = abs(ball_speed_x) * -1

                # create cracked brick
                print("hits left:", bricks_hitsleft[i])
                bricks_hitsleft[i] -= 1

                score += 5

                if bricks_hitsleft[i] == 0:

                    brick_effects.append({
                        "x": bricks_x[i],
                        "y": bricks_y[i],
                        "alpha": 255,
                        "speed_y": -4
                    })

                    # SPAWN STER ALS DIT BLOK IN DE RANDOM LIJST ZIT
                    if i in star_brick_indices and stars_spawned_this_level < MAX_STARS_PER_LEVEL:
                        star_x.append(brick_x + BRICK_WIDTH / 2 - STAR_WIDTH/2)
                        star_y.append(brick_y + BRICK_HEIGHT /
                                      2 - STAR_HEIGHT/2)
                        stars_spawned_this_level += 1

                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    bricks_hitsleft.pop(i)
                    ball_speed_x *= 1.02  # Bal wordt sneller
                    ball_speed_y *= 1.02

                    # move ball away a little
                    ball_y += ball_speed_y

                    # add score
                    score += 5

                    # save high score
                    if score > highscore:
                        highscore = score

                        bestand = open("highscore.txt", "w")
                        bestand.write(str(highscore))
                        bestand.close()

                    # break when one brick has been hit
                    break
        if len(bricks_hitsleft) == 0:
            current_level += 1
            if current_level < len(LEVELS):
                load_level(current_level)
                ball_x = SCREEN_WIDTH // 2
                ball_y = 100
            else:
                score += aantalharten * 50
                game_status = EIND
                gamewin = 10
                naam_invoeren = True

        Hoofdscore = str(score)
        score_status_msg = "Score:" + " " + Hoofdscore
        if score > highscore:
            highscore = score

        # move paddle:
        if keys[pygame.K_a]:
            paddle_x = paddle_x - 10
        if keys[pygame.K_d]:
            paddle_x = paddle_x + 10
        if paddle_x + paddle_width_current > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - paddle_width_current
        if paddle_x < 0:
            paddle_x = 0

        #
        # handle collisions
        # Harten
        if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:

            print("Een leven minder!")
            aantalharten -= 1

            if len(harten_x) > 0:
                harten_x.pop()
                harten_y.pop()

            # reset bal
            ball_x = SCREEN_WIDTH // 2
            ball_y = 100
            ball_speed_y = -6

        # if dead
        # stop het spel
        if len(harten_x) == 0:
            ball_speed_x = 0
            ball_speed_y = 0
            game_status = EIND
            gamelost = 5
            naam_invoeren = True

        #
        # draw everything
        #

        # draw everything, Stukje code uit gameloop die alles tekent:

        # clear screen
        bg_offset += 2

        for y in range(-SCREEN_HEIGHT, SCREEN_HEIGHT * 2, 80):
            pygame.draw.rect(screen, (255, 210, 230),
                             (0, y + bg_offset % 80, SCREEN_WIDTH, 40))

            pygame.draw.rect(screen, (255, 180, 215),
                             (0, y + 40 + bg_offset % 80, SCREEN_WIDTH, 40))
        # draw ball
        screen.blit(ball_img, (ball_x, ball_y))
        # draw paddletje
        # draw paddletje met huidige breedte
        paddle_img_current = pygame.transform.scale(
            paddle_img, (int(paddle_width_current), PADDLE_HEIGHT))
        screen.blit(paddle_img_current, (paddle_x, paddle_y))
        # draw harten
        for i in range(len(harten_x)):
            screen.blit(hart_img, (harten_x[i], harten_y[i]))
        # draw stars
        for i in range(len(star_x)):
            screen.blit(star_img, (star_x[i], star_y[i]))

            # ster effect tekenen
        for effect in star_effects[:]:
            effect["y"] -= effect["speed"]  # Beweeg omhoog
            effect["alpha"] -= 15  # Fade out
            effect["size"] = int(effect["size"] * 1.1)  # Groei

            if effect["alpha"] > 0:
                effect_img = star_img.copy()
                effect_img.set_alpha(effect["alpha"])
                scaled_effect = pygame.transform.scale(
                    effect_img, (effect["size"], effect["size"]))
                screen.blit(scaled_effect, (effect["x"], effect["y"]))
            else:
                star_effects.remove(effect)

        # draw BRICKS
        for i in range(len(bricks_x)):
            if bricks_hitsleft[i] == 2:
                screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
            if bricks_hitsleft[i] == 1:
                screen.blit(brickcracked_img, (bricks_x[i], bricks_y[i]))
        for effect in brick_effects[:]:
            effect["y"] += effect["speed_y"]
            effect["alpha"] -= 5
            if effect["alpha"] > 0:
                effect_img = brickcracked_img.copy()
                effect_img.set_alpha(effect["alpha"])
                screen.blit(effect_img, (effect["x"], effect["y"]))
            else:
                brick_effects.remove(effect)

        game_status_img = font.render(game_status_msg, True, 'green')
        # (0, 0) is top left corner of screen
        screen.blit(game_status_img, (550, 20))
        # score
        score_status_img = font.render(score_status_msg, True, "red")
        screen.blit(score_status_img, (1000, 20))
        # Highscore
        highscore_msg = "Highscore: " + str(highscore)
        highscore_img = font.render(highscore_msg, True, "blue")
        screen.blit(highscore_img, (905, 60))

        # Paddle BOOSt timer
        if paddle_boost_timer > 0:
            seconds_left = paddle_boost_timer / FPS
            timer_msg = f"BOOST: {seconds_left:.1f}s"
            timer_img = font.render(timer_msg, True, "cyan")
            screen.blit(timer_img, (905, 100))

    # eindscherm
    if game_status == EIND:
        screen.fill("pink")

        if gamewin == 10:
            game_status_msg = "YOU WIN!"
        if gamelost == 5:
            game_status_msg = "YOU LOST!"

        eind_img = font.render(game_status_msg, True, "white")
        screen.blit(eind_img, (585, 100))

        if naam_invoeren:
            naam_text = font.render("ENTER 2 INNITIALS:", True, (180, 0, 80))
            naam_img = font.render(player_name, True, (255, 20, 147))

            screen.blit(naam_text, (480, 200))
            screen.blit(naam_img, (650, 280))
            # Na naam terug naar begin scherm
            terug_img = font.render("ENTER = MENU", True, (180, 0, 80))
            screen.blit(terug_img, (560, 600))
    #highscore scherm
    if game_status == HIGH:
        screen.fill("white")

        titel = font.render("HIGHSCORES", True, "black")
        screen.blit(titel, (550, 100))
        back_img = font.render("> BACK = Backspace", True, "black")
        screen.blit(back_img, (480, 630))

        y = 200

        for naam, score in gesorteerd[:10]:
            tekst = f"{naam}  {score}"

            score_img = font.render(tekst, True, (180, 0, 80))
            screen.blit(score_img, (570, y))

            y += 40
    #uitleg scherm
    if game_status == UITLEG:
        screen.fill("white")

        titel_img = font.render("UITLEG", True, (180, 0, 80))
        screen.blit(titel_img, (600, 60))

        klein_font = pygame.font.Font('PressStart2P-Regular.ttf', 14)

        regels = [
            "A / D  =  paddle links en rechts bewegen",
            "Doel: maak alle blokken stuk",
            "Blauw blok moet je 2 keer raken",
            "Ster pakken = grotere paddle (powerup)",
            "4 levens, daarna game over",
            "3 levels in totaal",
        ]

        for i, regel in enumerate(regels):
            r = klein_font.render(regel, True, (180, 0, 80))
            screen.blit(r, (150, 200 + i * 60))

        back_img = font.render("> BACK = Backspace", True, (180, 0, 80))
        screen.blit(back_img, (450, 620))

   # show screen
    pygame.display.flip()
    #
    # wait until next frame
    #

    # wait until next frame
    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
