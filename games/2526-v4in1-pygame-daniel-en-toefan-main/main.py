#
# BREAKOUT GAME
#

import pygame


#
# definitions
#

# definitions
FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
ball_x = 0              # x-position of ball in pixels
ball_speed_x = 6     # speed of ball in x-direction in pixels per frame
ball_speed_x_ref = 6
ball_y = 300
ball_speed_y = -10
paddle_x = 640 
paddle_speed_x = 10
paddle_y = 600

num_players = 1
paddle2_x = 640
paddle2_speed_x = 10
paddle2_y = 600
ball2_x = 800
ball2_y = 300
ball2_speed_x = -6
ball2_speed_x_ref = 6
ball2_speed_y = -10

game_status_msg = ""
knop_rect = pygame.Rect(0, 0, 0, 0)
level = 1

BRICK_WIDTH = 96
BRICK_HEIGHT = 32

bricks_x = [
    160, 256, 352, 448, 736, 832, 928, 1024,
    160, 256, 352, 448, 736, 832, 928, 1024,
    160, 256, 352, 448, 736, 832, 928, 1024
]
bricks_y = [
    100, 100, 100, 100, 100, 100, 100, 100,
    130, 130, 130, 130, 130, 130, 130, 130,
    160, 160, 160, 160, 160, 160, 160, 160
]
teller = [
    2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2
]

#
# init game
#
pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()

#
# read images
#
background_img = pygame.image.load("achtergrond4.jpg").convert()


background_img = pygame.transform.scale(
    background_img,
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
# read images

# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img_grey = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_grey.blit(spritesheet, (0, 0), (772, 520, 384, 128))
brick_img_grey = pygame.transform.scale(
    brick_img_grey, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img_blue = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_blue.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img_blue = pygame.transform.scale(
    brick_img_blue, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img_purple = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_purple.blit(spritesheet, (0, 0), (0, 390, 384, 128))
brick_img_purple = pygame.transform.scale(
    brick_img_purple, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img_grey_cracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_grey_cracked.blit(spritesheet, (0, 0), (0, 650, 384, 128))
brick_img_grey_cracked = pygame.transform.scale(
    brick_img_grey_cracked, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img_blue_cracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_blue_cracked.blit(spritesheet, (0, 0), (0, 0, 384, 128))
brick_img_blue_cracked = pygame.transform.scale(
    brick_img_blue_cracked, (BRICK_WIDTH, BRICK_HEIGHT))

brick_img_purple_cracked = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_purple_cracked.blit(spritesheet, (0, 0), (0, 520, 384, 128))
brick_img_purple_cracked = pygame.transform.scale(
    brick_img_purple_cracked, (BRICK_WIDTH, BRICK_HEIGHT))

bricks_img = (
    [brick_img_grey] * 8 +
    [brick_img_blue] * 8 +
    [brick_img_purple] * 8
)
bricks_img_cracked = (
    [brick_img_grey_cracked] * 8 +
    [brick_img_blue_cracked] * 8 +
    [brick_img_purple_cracked] * 8
)

#


game_state = "menu"
menu_option = 1
menu_tick = 0
rect_1p = pygame.Rect(0, 0, 0, 0)
rect_2p = pygame.Rect(0, 0, 0, 0)
rect_tutorial = pygame.Rect(0, 0, 0, 0)
show_tutorial = False
font_menu = pygame.font.Font('PressStart2P-Regular.ttf', 18)
font_klein = pygame.font.Font('PressStart2P-Regular.ttf', 13)

def make_level(lvl):
    rijen = 3 + (lvl - 1)
    bx = []
    by = []
    kolommen_links = [160, 256, 352, 448]
    kolommen_rechts = [736, 832, 928, 1024]
    kolommen = kolommen_links + kolommen_rechts

    for r in range(rijen):
        for k in kolommen:
            bx.append(k)
            by.append(100 + r * 30)

    t = [2] * len(bx)
    return bx, by, t

def reset_to_menu():
    global game_state, game_status_msg, num_players
    global ball_x, ball_y, ball_speed_x, ball_speed_x_ref, ball_speed_y
    global paddle_x, paddle_speed_x
    global ball2_x, ball2_y, ball2_speed_x, ball2_speed_x_ref, ball2_speed_y
    global paddle2_x, paddle2_speed_x
    global bricks_x, bricks_y, teller, bricks_img, bricks_img_cracked

    game_state = "menu"
    game_status_msg = ""

    ball_x = 280
    ball_y = 300
    ball_speed_x = 6
    ball_speed_x_ref = 6
    ball_speed_y = -10
    paddle_x = 240
    paddle_speed_x = 10

    ball2_x = 800
    ball2_y = 300
    ball2_speed_x = -6
    ball2_speed_x_ref = 6
    ball2_speed_y = -10
    paddle2_x = 720
    paddle2_speed_x = 10

    bricks_x, bricks_y, teller = make_level(1)
    level = 1

    teller = [2] * 24

    bricks_img = (
        [brick_img_grey] * 8 +
        [brick_img_blue] * 8 +
        [brick_img_purple] * 8
    )
    bricks_img_cracked = (
        [brick_img_grey_cracked] * 8 +
        [brick_img_blue_cracked] * 8 +
        [brick_img_purple_cracked] * 8
    )

def next_level():
    global level, bricks_x, bricks_y, teller, bricks_img, bricks_img_cracked
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global ball2_x, ball2_y, ball2_speed_x, ball2_speed_y

    level += 1
    bricks_x, bricks_y, teller = make_level(level)

    bricks_img = (
        [brick_img_grey] * 8 +
        [brick_img_blue] * 8 +
        [brick_img_purple] * 8
    ) * ((len(bricks_x) // 24) + 1)
    bricks_img = bricks_img[:len(bricks_x)]

    bricks_img_cracked = (
        [brick_img_grey_cracked] * 8 +
        [brick_img_blue_cracked] * 8 +
        [brick_img_purple_cracked] * 8
    ) * ((len(bricks_x) // 24) + 1)
    bricks_img_cracked = bricks_img_cracked[:len(bricks_x)]

    ball_x = 280
    ball_y = 300
    ball_speed_x = 6
    ball_speed_y = -10

    ball2_x = 800
    ball2_y = 300
    ball2_speed_x = -6
    ball2_speed_y = -10

# game loop
#

print('mygame is running')
running = True
while running:
  # read events
  # move everything
  # handle collisions
  # draw everything
  # wait until next frame
    # read events

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_state = "playing"
                num_players = 1
            if event.key == pygame.K_2:
                game_state = "playing"
                num_players = 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu" and not show_tutorial:
                if rect_1p.collidepoint(event.pos):
                    game_state = "playing"
                    num_players = 1
                if rect_2p.collidepoint(event.pos):
                    game_state = "playing"
                    num_players = 2
                if rect_tutorial.collidepoint(event.pos):
                    show_tutorial = True
            elif show_tutorial:
                show_tutorial = False
            if game_status_msg != "" and knop_rect.collidepoint(event.pos):
                reset_to_menu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_state = "playing"
                num_players = 1
            if event.key == pygame.K_2:
                game_state = "playing"
                num_players = 2
            if event.key == pygame.K_n:
                next_level()
        

    if game_state == "menu":
        screen.blit(background_img, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        if show_tutorial:
            titel = font.render("TUTORIAL", True, (255, 255, 255))
            screen.blit(titel, (SCREEN_WIDTH // 2 - titel.get_width() // 2, 150))

            regel1 = font_menu.render("Speler 1: A en D om te bewegen", True, (255, 255, 255))
            regel2 = font_menu.render("Speler 2: PIJLTJES LINKS/RECHTS", True, (255, 255, 255))
            regel3 = font_menu.render("Kaats de bal terug en sloop blokken", True, (255, 255, 255))
            regel4 = font_klein.render("klik om terug te gaan", True, (200, 200, 200))

            screen.blit(regel1, (SCREEN_WIDTH // 2 - regel1.get_width() // 2, 300))
            screen.blit(regel2, (SCREEN_WIDTH // 2 - regel2.get_width() // 2, 350))
            screen.blit(regel3, (SCREEN_WIDTH // 2 - regel3.get_width() // 2, 400))
            screen.blit(regel4, (SCREEN_WIDTH // 2 - regel4.get_width() // 2, 480))
        else:
            titel = font.render("WELCOME", True, (255, 255, 255))
            screen.blit(titel, (SCREEN_WIDTH // 2 - titel.get_width() // 2, 180))

            rect_1p = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 60)
            rect_2p = pygame.Rect(SCREEN_WIDTH // 2 - 150, 380, 300, 60)
            rect_tutorial = pygame.Rect(SCREEN_WIDTH // 2 - 150, 460, 300, 60)

            mx, my = pygame.mouse.get_pos()
            for rect, label in [(rect_1p, "1 PLAYER"), (rect_2p, "2 PLAYERS"), (rect_tutorial, "TUTORIAL")]:
                hover = rect.collidepoint(mx, my)
                pygame.draw.rect(screen, (60, 60, 60) if not hover else (100, 100, 100), rect, border_radius=8)
                pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=8)
                lbl = font_menu.render(label, True, (255, 255, 255))
                screen.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.y + 18))

        pygame.display.flip()
        fps_clock.tick(FPS)
        continue

    keys = pygame.key.get_pressed()

    #
    # move everything

    if keys[pygame.K_a]:
        paddle_x = paddle_x + abs(paddle_speed_x) * -1
    if keys[pygame.K_d]:
        paddle_x = paddle_x + abs(paddle_speed_x)

    if num_players == 2:
        if keys[pygame.K_LEFT]:
            paddle2_x = paddle2_x + abs(paddle2_speed_x) * -1
        if keys[pygame.K_RIGHT]:
            paddle2_x = paddle2_x + abs(paddle2_speed_x)
        if paddle2_x < 0:
            paddle2_x = 0
        if paddle2_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle2_x = SCREEN_WIDTH - PADDLE_WIDTH

        ball2_x = ball2_x + ball2_speed_x
        ball2_y = ball2_y + ball2_speed_y
        if ball2_x < 0:
            ball2_speed_x = abs(ball2_speed_x)
        if ball2_x + BALL_WIDTH > SCREEN_WIDTH:
            ball2_speed_x = abs(ball2_speed_x) * -1
        if ball2_y < 0:
            ball2_speed_y = abs(ball2_speed_y)

    # padle stopt aan rand:
    if paddle_x < 0:
        paddle_x = 0
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y
    # bounce ball against edges of screen
    if ball_x < 0:  # left edge
        ball_speed_x = abs(ball_speed_x)  # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:  # right edge
        ball_speed_x = abs(ball_speed_x) * -1  # negative x-speed = move left

     # bounce ball against edges of screen
    if ball_y < 0:  # left edge
        ball_speed_y = abs(ball_speed_y)  # positive y-speed = move right
    ball_gemist = ball_y > paddle_y + PADDLE_HEIGHT
    if ball_gemist:
        ball_speed_x = 0
        ball_speed_y = 0

    #
    # handle collisions
    #
    for i in range(len(bricks_x)):
        if (ball_x + BALL_WIDTH > bricks_x[i] and
            ball_x < bricks_x[i] + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > bricks_y[i] and
                ball_y < bricks_y[i] + BRICK_HEIGHT):

            print('brick touched at ball_x = ' +
                  str(ball_x) + ' and ball_y = ' + str(ball_y))

            if ball_speed_y > 0 and ball_y < bricks_y[i]:
                ball_speed_y = -abs(ball_speed_y)
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                ball_speed_y = abs(ball_speed_y)
            elif ball_speed_x > 0 and ball_x < bricks_x[i]:
                ball_speed_x = -abs(ball_speed_x)
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                ball_speed_x = abs(ball_speed_x)

            teller[i] -= 1
            if teller[i] == 0:
                bricks_x.pop(i)
                bricks_img.pop(i)
                bricks_y.pop(i)
                bricks_img_cracked.pop(i)
                teller.pop(i)

            ball_speed_x = ball_speed_x * 1.010
            ball_speed_x_ref = ball_speed_x_ref * 1.01
            ball_speed_y = ball_speed_y * 1.01
            paddle_speed_x = paddle_speed_x * 1.01

            if len(bricks_x) == 0:
                ball_speed_x = 0
                ball_speed_y = 0
                next_level()

            break

    if num_players == 2:
        for i in range(len(bricks_x)):
            if (ball2_x + BALL_WIDTH > bricks_x[i] and
                ball2_x < bricks_x[i] + BRICK_WIDTH and
                ball2_y + BALL_HEIGHT > bricks_y[i] and
                    ball2_y < bricks_y[i] + BRICK_HEIGHT):

                if ball2_speed_y > 0 and ball2_y < bricks_y[i]:
                    ball2_speed_y = -abs(ball2_speed_y)
                elif ball2_speed_y < 0 and ball2_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                    ball2_speed_y = abs(ball2_speed_y)
                elif ball2_speed_x > 0 and ball2_x < bricks_x[i]:
                    ball2_speed_x = -abs(ball2_speed_x)
                elif ball2_speed_x < 0 and ball2_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                    ball2_speed_x = abs(ball2_speed_x)

                teller[i] -= 1
                if teller[i] == 0:
                    bricks_x.pop(i)
                    bricks_img.pop(i)
                    bricks_y.pop(i)
                    bricks_img_cracked.pop(i)
                    teller.pop(i)

                if len(bricks_x) == 0:
                    ball2_speed_x = 0
                    ball2_speed_y = 0
                    next_level()

                break

                ball_hit_paddle = False

    ball_hit_paddle = False

    if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
            ball_y < paddle_y + PADDLE_HEIGHT):
        ball_speed_y = -abs(ball_speed_y)
        paddle_center = paddle_x + (PADDLE_WIDTH / 2)
        ball_center = ball_x + (BALL_WIDTH / 2)
        relatieve_impact = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
        if abs(relatieve_impact) < 0.2:
            if relatieve_impact >= 0:
                relatieve_impact = 0.2
            else:
                relatieve_impact = -0.2
        ball_speed_x = relatieve_impact * ball_speed_x_ref * 1.5
        ball_hit_paddle = True

    if num_players == 2 and not ball_hit_paddle:
        if (ball_x + BALL_WIDTH > paddle2_x and
            ball_x < paddle2_x + PADDLE_WIDTH and
            ball_y + BALL_HEIGHT > paddle2_y and
                ball_y < paddle2_y + PADDLE_HEIGHT):
            ball_speed_y = -abs(ball_speed_y)
            paddle_center = paddle2_x + (PADDLE_WIDTH / 2)
            ball_center = ball_x + (BALL_WIDTH / 2)
            relatieve_impact = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
            if abs(relatieve_impact) < 0.2:
                if relatieve_impact >= 0:
                    relatieve_impact = 0.2
                else:
                    relatieve_impact = -0.2
            ball_speed_x = relatieve_impact * ball_speed_x_ref * 1.5

    if num_players == 2:
        ball2_hit_paddle = False

        if (ball2_x + BALL_WIDTH > paddle2_x and
            ball2_x < paddle2_x + PADDLE_WIDTH and
            ball2_y + BALL_HEIGHT > paddle2_y and
                ball2_y < paddle2_y + PADDLE_HEIGHT):
            ball2_speed_y = -abs(ball2_speed_y)
            paddle_center = paddle2_x + (PADDLE_WIDTH / 2)
            ball_center = ball2_x + (BALL_WIDTH / 2)
            relatieve_impact = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
            ball2_speed_x = relatieve_impact * ball2_speed_x_ref * 1.5
            ball2_hit_paddle = True

        if not ball2_hit_paddle:
            if (ball2_x + BALL_WIDTH > paddle_x and
                ball2_x < paddle_x + PADDLE_WIDTH and
                ball2_y + BALL_HEIGHT > paddle_y and
                    ball2_y < paddle_y + PADDLE_HEIGHT):
                ball2_speed_y = -abs(ball2_speed_y)
                paddle_center = paddle_x + (PADDLE_WIDTH / 2)
                ball_center = ball2_x + (BALL_WIDTH / 2)
                relatieve_impact = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
                if abs(relatieve_impact) < 0.2:
                    if relatieve_impact >= 0:
                        relatieve_impact = 0.2
                    else:
                        relatieve_impact = -0.2
                ball2_speed_x = relatieve_impact * ball2_speed_x_ref * 1.5

        ball2_gemist = ball2_y > paddle2_y + PADDLE_HEIGHT
        if ball2_gemist:
            ball2_speed_x = 0
            ball2_speed_y = 0

    if num_players == 1:
        if ball_gemist:
            game_status_msg = "verloren!"
    else:
        if ball_gemist and ball2_gemist:
            game_status_msg = "verloren!"

    if game_status_msg != "":
        ball_speed_x = 0
        ball_speed_y = 0
        ball2_speed_x = 0
        ball2_speed_y = 0
        paddle_speed_x = 0
        paddle2_speed_x = 0


    #
    # draw everything
    #

   



    # clear screen
    screen.blit(background_img, (0, 0))

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(paddle_img, (paddle_x, paddle_y))
    if num_players == 2:
        screen.blit(ball_img, (ball2_x, ball2_y))
        screen.blit(paddle_img, (paddle2_x, paddle2_y))

    # draw blokken
    for i in range(len(bricks_x)):
        if teller[i] == 2:
            screen.blit(bricks_img[i], (bricks_x[i], bricks_y[i]))
        elif teller[i] == 1:
            screen.blit(bricks_img_cracked[i], (bricks_x[i], bricks_y[i]))

    game_status_img = font.render(game_status_msg, True, 'green')
    screen.blit(game_status_img, (0, 0))

    level_img = font_klein.render("Level " + str(level), True, 'white')
    screen.blit(level_img, (SCREEN_WIDTH - 150, 10))

    # show screen
    if game_status_msg != "":
         knop_rect = pygame.Rect(540, 400, 200, 60)
         pygame.draw.rect(screen, 'red', knop_rect, border_radius=10)
         knop_tekst = font.render("RESTART", True, 'black')
         screen.blit(knop_tekst, (565, 415))
         if keys[pygame.K_r]:
             reset_to_menu()

    pygame.display.flip()

    #
    # wait until next frame
    #

    # wait until next frame
    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
