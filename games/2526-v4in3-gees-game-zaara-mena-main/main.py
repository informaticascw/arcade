#
# BREAKOUT GAME
#

import pygame
import time

#
# definitions
FPS = 60  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
ball_x = 0        # x-position of ball in pixels     begin = 0
ball_speed_x = -2  # speed of ball in x-direction in pixels per frame (was6) -2
ball_y = 440       # y-position of ball in pixels
ball_speed_y = -4   # speed of ball in y-direction in pixels per frame -10
paddle_x = SCREEN_WIDTH / 2      # start position paddle
paddle_y = SCREEN_HEIGHT - 100       # start position paddle
paddle_x_2 = SCREEN_WIDTH / 2
paddle_y_2 = SCREEN_HEIGHT - 190
PADDLE_WIDTH = 144   # width from paddle
PADDLE_HEIGHT = 32   # height from paddle
game_status_msg = ""  # define global varible, text
BRICK_WIDTH = 96  # width brick
BRICK_HEIGHT = 32  # height brick
lives = 3
score = 0
highscore = 0
combo = 0
# init game
#
STATUS_START = 0
STATUS_PLAY = 1
STATUS_GAMEOVER = 2
spel_status = STATUS_START
playermode = 1  # 1 for one player 2 for 2 players


pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#
# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
#
# paddle
#
# create empty image of 243 x 64 pixels, SRCALPHA supports transparency
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
# copy part (x-left=1158, y-top=396, width=243, height=64) from spritesheet to paddle_img at (0,0)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
# resize paddle_img from 243 x 64 pixels to PADDLE_WIDTH x PADDLE_HEIGHT
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
#
# heart
#
heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)

heart_img.blit(
    spritesheet,
    (0, 0),
    (1637, 652, 64, 58)
)

heart_img = pygame.transform.scale(
    heart_img,
    (32, 29)
)
# brick
#
# create empty image of 384 x 128 pixels, SRCALPHA supports transparency
# resize paddle_img from 384 x 128 pixels to BRICK_WIDTH x BRICK_HEIGHT
green_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
green_brick_img.blit(spritesheet, (0, 0), (0, 130, 384, 128))
green_brick_img = pygame.transform.scale(
    green_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
blue_brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
blue_brick_img.blit(spritesheet, (0, 0), (0, 0, 384, 128))
blue_brick_img = pygame.transform.scale(
    blue_brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
#
clouds = [
    {"x": 60, "y": 80, "speed": 0.2, "scale": 1.5},
    {"x": 350, "y": 150, "speed": 0.3, "scale": 1.0},
    {"x": 700, "y": 100, "speed": 0.4, "scale": 0.9},
    {"x": 980, "y": 170, "speed": 0.1, "scale": 1.8},
]


def update_clouds():
    for cloud in clouds:
        cloud["x"] += cloud["speed"]
        cloud_width = int(140 * cloud["scale"])
        if cloud["x"] > SCREEN_WIDTH + cloud_width:
            cloud["x"] = -cloud_width


def draw_cloud(x, y, scale):
    color = (255, 255, 255)
    pygame.draw.ellipse(screen, color, (x, y, 60 * scale, 35 * scale))
    pygame.draw.ellipse(screen, color, (x + 25 * scale,
                        y - 15 * scale, 70 * scale, 45 * scale))
    pygame.draw.ellipse(
        screen, color, (x + 65 * scale, y, 60 * scale, 35 * scale))


def draw_sky():
    screen.fill((120, 190, 255))
    for cloud in clouds:
        draw_cloud(cloud["x"], cloud["y"], cloud["scale"])


level = 1


def maak_level():
    global bricks_x, bricks_y, brick_hits

    if level == 1:
        bricks_x = [544, 640, 496, 688, 448, 736, 400, 784,
                    400, 784, 448, 736, 496, 688, 544, 640, 592]
        bricks_y = [180, 180, 212, 212, 276, 276, 340, 340,
                    404, 404, 468, 468, 532, 532, 564, 564, 372]

    elif level == 2:
        bricks_x = [688, 784, 880, 976, 976, 976, 880, 784, 688,
                    592, 496, 400, 304, 208, 208, 208, 304, 400,
                    496, 592, 592, 688, 496, 592]
        bricks_y = [418, 386, 354, 322, 290, 258, 226, 194, 226,
                    258, 418, 386, 354, 322, 290, 258, 226, 194,
                    226, 162, 354, 130, 130, 450]

    elif level == 3:
        bricks_x = [544, 640, 496, 688, 448, 736, 400, 784,
                    400, 784, 448, 736, 496, 688, 544, 640, 592]
        bricks_y = [180, 180, 212, 212, 276, 276, 340, 340,
                    404, 404, 468, 468, 532, 532, 564, 564, 372]

    brick_hits = [2] * len(bricks_x)


maak_level()
#
# game loop
#

print('mygame is running')
running = True
while running:
    #
    # read events
    #
    for event in pygame.event.get():  # read all events
        if event.type == pygame.QUIT:  # GUI is closed
            running = False  # end programm
    keys = pygame.key.get_pressed()  # read which keys are down

    if spel_status == STATUS_START:
        # clear screen

        # move paddle right-left
        if keys[pygame.K_e]:
            playermode = 1
            spel_status = STATUS_PLAY
        if keys[pygame.K_r]:
            playermode = 2
            spel_status = STATUS_PLAY

        # draw game status message
        game_status_img = font.render(
            'e voor 1 player, r voor 2 player', True, 'green')
        # (0, 0) is top left corner of screen
        screen.blit(game_status_img, (0, 0))
        draw_sky()
        update_clouds()
        titel = font.render("BREAKOUT", True, "yellow")

        screen.blit(
            titel,
            (SCREEN_WIDTH // 2 - titel.get_width() // 2, 150)
        )
        keuze = font.render(
            "E = 1 PLAYER   R = 2 PLAYERS",
            True,
            "green"
        )

        screen.blit(
            keuze,
            (SCREEN_WIDTH // 2 - keuze.get_width() // 2, 300)
        )

    if spel_status == STATUS_PLAY:
        #
        # move everything
        #

        if level == 1:
            # move paddle right-left
            if keys[pygame.K_d]:  # key d is down
                paddle_x = paddle_x + 10
            if keys[pygame.K_a]:  # key a is down
                paddle_x = paddle_x - 10
            # stop paddle at border
            if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  # screen boundary right
                paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
            if paddle_x < 0:  # screen boundary left
                paddle_x = 0

            if playermode == 2:
                # move paddle 2 right-left
                if keys[pygame.K_l]:  # key d is down
                    paddle_x_2 = paddle_x_2 + 10
                if keys[pygame.K_j]:  # key a is down
                    paddle_x_2 = paddle_x_2 - 10
                # stop paddle at border
                if paddle_x_2 + PADDLE_WIDTH > SCREEN_WIDTH:  # screen boundary right
                    paddle_x_2 = SCREEN_WIDTH - PADDLE_WIDTH
                if paddle_x_2 < 0:  # screen boundary left
                    paddle_x_2 = 0
        # end level 1

        if level == 2:
           # move paddle right-left
            if keys[pygame.K_d]:  # key d is down
                paddle_x = paddle_x + 10
            if keys[pygame.K_a]:  # key a is down
                paddle_x = paddle_x - 10
            # stop paddle at border
            if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  # screen boundary right
                paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
            if paddle_x < 0:  # screen boundary left
                paddle_x = 0

            if playermode == 2:
                # move paddle 2 right-left
                if keys[pygame.K_l]:  # key d is down
                    paddle_x_2 = paddle_x_2 + 10
                if keys[pygame.K_j]:  # key a is down
                    paddle_x_2 = paddle_x_2 - 10
                # stop paddle at border
                if paddle_x_2 + PADDLE_WIDTH > SCREEN_WIDTH:  # screen boundary right
                    paddle_x_2 = SCREEN_WIDTH - PADDLE_WIDTH
                if paddle_x_2 < 0:  # screen boundary left
                    paddle_x_2 = 0
        # end level 2
        if level == 3:
           # move paddle right-left
            if keys[pygame.K_d]:  # key d is down
                paddle_x = paddle_x + 10
            if keys[pygame.K_a]:  # key a is down
                paddle_x = paddle_x - 10
            # stop paddle at border
            if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:  # screen boundary right
                paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
            if paddle_x < 0:  # screen boundary left
                paddle_x = 0

            if playermode == 2:
                # move paddle 2 right-left
                if keys[pygame.K_l]:  # key d is down
                    paddle_x_2 = paddle_x_2 + 10
                if keys[pygame.K_j]:  # key a is down
                    paddle_x_2 = paddle_x_2 - 10
                # stop paddle at border
                if paddle_x_2 + PADDLE_WIDTH > SCREEN_WIDTH:  # screen boundary right
                    paddle_x_2 = SCREEN_WIDTH - PADDLE_WIDTH
                if paddle_x_2 < 0:  # screen boundary left
                    paddle_x_2 = 0
        # end level 3
        
        # move ball right-left
        ball_x = ball_x + ball_speed_x
        # move ball up-down
        ball_y = ball_y + ball_speed_y

        # bounce ball against edges of screen
        if ball_x < 0:  # left edge
            ball_speed_x = abs(ball_speed_x)  # positive x-speed = move right
        if ball_x + BALL_WIDTH > SCREEN_WIDTH:  # right edge
            # negative x-speed = move left
            ball_speed_x = abs(ball_speed_x) * -1
        if ball_y < 0:  # upper edge
            ball_speed_y = abs(ball_speed_y)  # positive y-speed = move up

        # bounce ball against paddle
        ball_bovenkant = ball_y
        ball_onderkant = ball_y + BALL_HEIGHT
        ball_right = ball_x + BALL_WIDTH
        ball_left = ball_x
        paddle_bovenkant = paddle_y
        paddle_onderkant = paddle_y + PADDLE_HEIGHT
        paddle_right = paddle_x + PADDLE_WIDTH
        paddle_left = paddle_x
        if (ball_right > paddle_left and
            ball_left < paddle_right and
            ball_onderkant > paddle_bovenkant and
                ball_bovenkant < paddle_onderkant):  # y_top_paddle
            # negative y = ball moves upwards
            ball_speed_y = (abs(ball_speed_y) * -1)
            combo = 0

        # bounce ball against paddle_2 (only exists in 2-player mode)
        if playermode == 2:
            ball_bovenkant = ball_y
            ball_onderkant = ball_y + BALL_HEIGHT
            ball_right = ball_x + BALL_WIDTH
            ball_left = ball_x
            paddle_bovenkant_2 = paddle_y_2
            paddle_onderkant_2 = paddle_y_2 + PADDLE_HEIGHT
            paddle_right_2 = paddle_x_2 + PADDLE_WIDTH
            paddle_left_2 = paddle_x_2
            if (ball_right > paddle_left_2 and
                ball_left < paddle_right_2 and
                ball_onderkant > paddle_bovenkant_2 and
                    ball_bovenkant < paddle_onderkant_2):  # y_top_paddle
                # negative y = ball moves upwards
                ball_speed_y = (abs(ball_speed_y) * -1)
                combo = 0

        #
        # handle collisions
        #

        # for-loop collisions
        for i in range(0, len(bricks_x)):
            brick_left = bricks_x[i]
            brick_right = bricks_x[i] + BRICK_WIDTH
            brick_top = bricks_y[i]
            brick_bottom = bricks_y[i] + BRICK_HEIGHT

            # ball bounce
            if (ball_right > brick_left and
                ball_left < brick_right and
                ball_onderkant > brick_top and
                    ball_bovenkant < brick_bottom):

                brick_hits[i] -= 1
                score += 20

                combo += 1

                if combo > 1:
                    score += 30   # totaal 50 punten voor combo-hit

                if ball_speed_y > 0:
                    ball_speed_y = float(-abs(ball_speed_y)) - 1
                else:
                    ball_speed_y = float(abs(ball_speed_y)) + 1
                break

        # remove brick
        i = 0
        while i < len(bricks_x):
            if brick_hits[i] <= 0:
                bricks_x.pop(i)
                bricks_y.pop(i)
                brick_hits.pop(i)
            else:
                i += 1

        # check if dead
        if score > highscore:
            highscore = score
        if ball_onderkant > SCREEN_HEIGHT:

            lives -= 1

            if lives > 0:
                ball_x = SCREEN_WIDTH // 2
                ball_y = 440
                ball_speed_x = -2
                ball_speed_y = -4

            else:
                ball_speed_x = 0
                ball_speed_y = 0
                spel_status = STATUS_GAMEOVER

        # check for win
        if len(bricks_x) == 0:
            level += 1

            if level <= 3:

                draw_sky()
                update_clouds()
                tekst = font.render(f"Level {level}", True, "green")
                x = SCREEN_WIDTH // 2 - tekst.get_width() // 2
                y = SCREEN_HEIGHT // 2 - tekst.get_height() // 2
                screen.blit(tekst, (x, y))
                pygame.display.flip()
                pygame.time.delay(3000)
                maak_level()

                ball_x = SCREEN_WIDTH // 2
                ball_y = 440
                ball_speed_x = -2
                ball_speed_y = -4

            else:
                game_status_msg = "Je hebt alle levels gehaald!"

        #
        # draw everything
        #

        draw_sky()
        update_clouds()

        # clear screen

        # draw game status message
        game_status_img = font.render(game_status_msg, True, 'green')
        # (0, 0) is top left corner of screen
        screen.blit(game_status_img, (0, 0))
        score_img = font.render(f"Score: {score}", True, "green")
        screen.blit(score_img, (20, 70))

        # draw ball_x
        screen.blit(ball_img, (ball_x, ball_y))  # ball op het scherm x, y

        # draw paddle
        screen.blit(paddle_img, (paddle_x, paddle_y))
        if playermode == 2:
            screen.blit(paddle_img, (paddle_x_2, paddle_y_2))

        # draw blocks
        for i in range(0, len(bricks_x)):
            # loop for printing bricks

            # screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
            if brick_hits[i] == 2:
                screen.blit(green_brick_img, (bricks_x[i], bricks_y[i]))

            elif brick_hits[i] == 1:
                screen.blit(blue_brick_img, (bricks_x[i], bricks_y[i]))

        # heart
        for i in range(lives):
            screen.blit(heart_img, (20 + i * 40, 20))

    if spel_status == STATUS_GAMEOVER:
        draw_sky()
        update_clouds()

        gameover = font.render("GAME OVER", True, "red")

        score_txt = font.render(
            f"Score: {score}",
            True,
            "white"
        )

        high_txt = font.render(
            f"Highscore: {highscore}",
            True,
            "yellow"
        )

        restart_txt = font.render(
            "Druk X voor nieuw spel",
            True,
            "green"
        )

        screen.blit(
            gameover,
            (SCREEN_WIDTH//2 - gameover.get_width()//2, 180)
        )

        screen.blit(
            score_txt,
            (SCREEN_WIDTH//2 - score_txt.get_width()//2, 280)
        )

        screen.blit(
            high_txt,
            (SCREEN_WIDTH//2 - high_txt.get_width()//2, 350)
        )

        screen.blit(
            restart_txt,
            (SCREEN_WIDTH//2 - restart_txt.get_width()//2, 450)
        )
        if keys[pygame.K_x]:
            score = 0
            lives = 3
            level = 1

            ball_x = SCREEN_WIDTH // 2
            ball_y = 440

            ball_speed_x = -2
            ball_speed_y = -4

            maak_level()

            spel_status = STATUS_PLAY

    # show screen
    pygame.display.flip()

    #
    # wait until next frame
    #

    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')