#
# BREAKOUT GAME
#

import pygame
import time
from pygame import mixer
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup
import random
import math
from math import sin, cos, pi

#
# definitions
#


def game(level_id, screen, cracked_bricks_mode=False, debug=False):
    # Global constants
    FPS = 60  # Frames Per Second
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    BALL_WIDTH = 16
    BALL_HEIGHT = 16
    PADDLE_WIDTH = 144
    PADDLE_HEIGHT = 32
    BRICK_WIDTH = 96
    BRICK_HEIGHT = 32
    score = 0

    # Global variables
    ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
    ball_y = SCREEN_HEIGHT-(SCREEN_HEIGHT // 3) // 2 - BALL_HEIGHT // 2
    ball_speed_x = 0
    ball_speed_y = 6
    paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 15
    game_status_msg = ""
    game_started = False
    game_over = False
    countdown_active = False
    countdown_start_time = 0
    countdown_value = 3
    tree = ET.parse('Bricks.xml')
    root = tree.getroot()
    blocks_data = {}
    first_run = True
    paused = False
    fireworks = []
    level_cleared = False

    with open('Bricks.xml', 'r') as f:
        brick_data = f.read()

    with open(level_id, 'r') as f:
        level_data = json.load(f)
    print(len(level_data))

    #
    # init game
    #

    pygame.init()
    font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
    score_font = pygame.font.Font('PressStart2P-Regular.ttf', 16)
    if debug == True:
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Breakout')

    def draw_center(text, color, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(img, rect)

    def draw_pause_screen():
        # Dark transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        draw_center("PAUSED", 'yellow', SCREEN_HEIGHT // 2 - 50)
        draw_center("Press ESC to resume", 'white', SCREEN_HEIGHT // 2 + 20)
        draw_center("Press Q to go back", 'white', SCREEN_HEIGHT // 2 + 60)

    def reset_game():
        nonlocal level_cleared, fireworks, bricks_list, first_run, game_started, game_over, game_status_msg, countdown_active, countdown_value
        nonlocal ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, score
       # Reset game variables
        ball_x = SCREEN_WIDTH // 2 - BALL_WIDTH // 2
        ball_y = SCREEN_HEIGHT - \
            (SCREEN_HEIGHT // 3) // 2 - BALL_HEIGHT // 2
        ball_speed_x = 0
        ball_speed_y = 6
        score = 0
        paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        game_status_msg = ""
        game_started = False
        game_over = False
        countdown_active = False
        countdown_value = 3
        bricks_list = []
        first_run = True
        fireworks = []
        level_cleared = False

    def spawn_firework():
        firework = []
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 300)
        color = random.choice([
            (255, 50, 50), (255, 255, 100), (255, 255, 255),
            (80, 180, 255), (200, 80, 255), (255, 150, 50), (80, 255, 120)
        ])
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 7)
            firework.append({
                "x": x,
                "y": y,
                "dx": math.cos(angle) * speed,
                "dy": math.sin(angle) * speed,
                "life": random.randint(60, 120),
                "color": color
            })
        fireworks.append(firework)

    def update_fireworks():
        new_fireworks = []
        for firework in fireworks:
            new_firework = []
            for p in firework:
                p["x"] += p["dx"]
                p["y"] += p["dy"]
                p["life"] -= 1
                if p["life"] > 0:
                    new_firework.append(p)
            if new_firework:
                new_fireworks.append(new_firework)
        fireworks[:] = new_fireworks

    def draw_fireworks():
        for firework in fireworks:
            for p in firework:
                alpha = max(0, int((p["life"] / 120) * 255))
                pygame.draw.circle(
                    screen,
                    p["color"],
                    (int(p["x"]), int(p["y"])),
                    2
                )

    # runs a check whether or not the music works and prevent crash
    sound_enabled = True

    try:
        mixer.init()
    except pygame.error:
        print("No audio device found")
        sound_enabled = False

    if sound_enabled:
        mixer.music.load('Bg_music.wav')
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

    #
    # read images
    #

    # spritesheet
    spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

    # Game assets
    ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
    ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
    ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
    paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
    paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
    paddle_img = pygame.transform.scale(
        paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
    background_img = pygame.image.load('background.jpg').convert()
    background_img = pygame.transform.scale(background_img, (1280, 720))

    Bs_data = BeautifulSoup(brick_data, "xml")
    bricks_normal = Bs_data.find_all('SubTexture', {'cracked': 'false'})
    bricks_cracked = Bs_data.find_all('SubTexture', {'cracked': 'true'})

    #
    # game loop
    #

    print('Breakout is running')
    running = True
    bricks_list = []

    while running:

        #
        # read events
        #

        if first_run == True:
            for i in level_data:
                blocks_data = dict(i)
                brick_x = int(blocks_data['x'])
                brick_y = int(blocks_data['y'])
                brick_id = int(blocks_data['id'])
                image_x = int(bricks_normal[brick_id - 1].get('x'))
                image_y = int(bricks_normal[brick_id - 1].get('y'))
                tile_surf = pygame.Surface((384, 128), pygame.SRCALPHA)
                tile_surf.blit(spritesheet, (0, 0),
                               (image_x, image_y, 384, 128))
                tile_surf = pygame.transform.scale(
                    tile_surf, (BRICK_WIDTH, BRICK_HEIGHT))
                tile_rect = tile_surf.get_rect(topleft=(brick_x, brick_y))
                bricks_list.append(
                    {'surf': tile_surf, 'rect': tile_rect, 'cracked': False, 'id': brick_id})

            first_run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # restart game when pressing R
            if event.type == pygame.KEYDOWN:
                # start game with countdown
                if event.key == pygame.K_SPACE and not game_started and not countdown_active and not paused:
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()
                    countdown_value = 3
                # reset game
                if event.key == pygame.K_r and (game_over or level_cleared):
                    reset_game()
                if event.key == pygame.K_ESCAPE and paused == False:
                    paused = True
                elif event.key == pygame.K_ESCAPE and paused == True:
                    paused = False
                if event.key == pygame.K_q and paused:
                    return True

        if not paused:
            keys = pygame.key.get_pressed()

            if countdown_active:
                elapsed = (pygame.time.get_ticks() -
                           countdown_start_time) / 1000

                if elapsed >= 1:
                    countdown_start_time = pygame.time.get_ticks()
                    countdown_value -= 1

                if countdown_value <= 0:
                    countdown_active = False
                    game_started = True

            #
            # move everything
            #

            # move ball only if game started
            if game_started:
                ball_x += ball_speed_x
                ball_y += ball_speed_y

            # move paddle only when game started
            if game_started:
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    paddle_x -= 8
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    paddle_x += 8

            # bounce ball from walls
            if ball_x < 0:
                ball_speed_x = abs(ball_speed_x)
            if ball_x + BALL_WIDTH > SCREEN_WIDTH:
                ball_speed_x = abs(ball_speed_x) * -1
            if ball_y < 0:
                ball_speed_y = abs(ball_speed_y)

            # bounce ball from paddle
            if (ball_y + BALL_HEIGHT >= paddle_y and
                ball_y <= paddle_y + PADDLE_HEIGHT and
                ball_x + BALL_WIDTH >= paddle_x and
                    ball_x <= paddle_x + PADDLE_WIDTH):

                # calculate where the ball hit the paddle
                hit_pos = (ball_x + BALL_WIDTH / 2) - \
                    (paddle_x + PADDLE_WIDTH / 2)

                # more skill based
                ball_speed_x = hit_pos * 0.15
                ball_speed_x = max(-7, min(7, ball_speed_x))

                # always bounce upward
                ball_speed_y = -abs(ball_speed_y)

            #
            # handle collisions
            #
            # check collisions between ball and bricks
            ball_rect = pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_HEIGHT)
            for i in range(len(bricks_list) - 1, -1, -1):
                b = bricks_list[i]
                if ball_rect.colliderect(b['rect']):

                    brick_rect = b['rect']

                    # Calculate overlap on each axis
                    # Horizontal overlap (how much the ball overlaps with brick on X axis)
                    overlap_left = (ball_rect.right - brick_rect.left)
                    overlap_right = (brick_rect.right - ball_rect.left)
                    h_overlap = min(overlap_left, overlap_right)

                    # Vertical overlap (how much the ball overlaps with brick on Y axis)
                    overlap_top = (ball_rect.bottom - brick_rect.top)
                    overlap_bottom = (brick_rect.bottom - ball_rect.top)
                    v_overlap = min(overlap_top, overlap_bottom)

                    # If horizontal overlap is smaller, ball hit from left or right side
                    if h_overlap < v_overlap:
                        ball_speed_x = -ball_speed_x
                    else:
                        # Ball hit from top or bottom
                        ball_speed_y = -ball_speed_y

                    if cracked_bricks_mode == True:
                        if b["cracked"] == False:
                            b["cracked"] = True
                            # Load the cracked version of this brick
                            brick_id = b['id']
                            cracked_brick = bricks_cracked[brick_id - 1]
                            image_x = int(cracked_brick.get('x'))
                            image_y = int(cracked_brick.get('y'))
                            cracked_surf = pygame.Surface(
                                (384, 128), pygame.SRCALPHA)
                            cracked_surf.blit(spritesheet, (0, 0),
                                              (image_x, image_y, 384, 128))
                            cracked_surf = pygame.transform.scale(
                                cracked_surf, (BRICK_WIDTH, BRICK_HEIGHT))
                            b['surf'] = cracked_surf
                            break
                        elif b["cracked"] == True:
                            # remove the brick that was hit
                            bricks_list.pop(i)
                            score += 10
                            break
                    else:
                        bricks_list.pop(i)
                        score += 10

            # win condition
            if game_started and len(bricks_list) == 0 and not level_cleared:
                level_cleared = True
                game_status_msg = "You win!"
                for _ in range(4):
                    spawn_firework()
                ball_speed_x = 0
                ball_speed_y = 0
                game_started = False

            # lose condition
            if ball_y > SCREEN_HEIGHT and not game_over:
                game_over = True
                game_started = False
                game_status_msg = "You lost!"
                ball_speed_x = 0
                ball_speed_y = 0

            # paddle collisions
            paddle_x = max(0, min(paddle_x, SCREEN_WIDTH - PADDLE_WIDTH))

        #
        # draw everything
        #
        # background
        screen.blit(background_img, (0, 0))
        # draw ball
        screen.blit(ball_img, (ball_x, ball_y))
        screen.blit(paddle_img, (paddle_x, paddle_y))
        # draw bricks
        for b in bricks_list:
            screen.blit(b['surf'], b['rect'])

        # draw scoreboard
        score_text = score_font.render(
            f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        # draw win/loss message
        if game_status_msg:
            if game_status_msg == "You win!":
                draw_center(game_status_msg, 'yellow', SCREEN_HEIGHT // 2 - 60)
                draw_center("Press R to restart", 'white', SCREEN_HEIGHT // 2)
                draw_center(f"Final Score: {score}",
                            'white', SCREEN_HEIGHT // 2 + 60)
            else:
                draw_center(game_status_msg, 'green', SCREEN_HEIGHT // 2 - 60)
                draw_center("Press R to restart", 'white', SCREEN_HEIGHT // 2)
                draw_center(f"Final Score: {score}",
                            'white', SCREEN_HEIGHT // 2 + 60)
        # show start message
        if not game_started and not game_over and not countdown_active and not level_cleared:
            draw_center("Press SPACE to begin",
                        'white', SCREEN_HEIGHT // 2)
        # show countdown
        if countdown_active and not game_over:
            if countdown_value > 0:
                text = str(countdown_value)
                color = 'white'
            else:
                text = "GO!"
                color = 'yellow'
            draw_center(text, color, SCREEN_HEIGHT // 2)

        # draw fireworks
        if fireworks:
            update_fireworks()
            draw_fireworks()

        # pause overlay
        if paused:
            draw_pause_screen()

        # show screen
        pygame.display.flip()
        #
        # wait until next frame
        #
        fps_clock.tick(FPS)  # Sleep the remaining time of this frame


print('Breakout stopped running')

# credit logs
# credit for bg img explanation: https://www.youtube.com/watch?v=dGwmmBBMlKs
# credit for bg image: https://wallpapercave.com/w/wp10655314#google_vignette
# credit for bg music explanation: https://www.youtube.com/watch?v=pcdB2s2y4Qc
# credit for bg music: https://freesound.org/people/emceeciscokid/sounds/403372/
