# The game
# BREAKOUT GAME
#

import pygame
import random


#
# definitions
#

FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # breedte in pixels
SCREEN_HEIGHT = 720  # hoogte in pixels
BALL_WIDTH = 16  # Bal breedte
BALL_HEIGHT = 16  # Bal hoogte

PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32

BRICK_WIDTH = 96
BRICK_HEIGHT = 32

ball_x = SCREEN_WIDTH / 2 -200
ball_speed_x = 8
ball_y = SCREEN_HEIGHT / 2
ball_speed_y = 7

paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle_speed_x = 6
paddle_y = 670

paddle2_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle2_speed_x = 6
paddle2_y = 50

bricks_x = [96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056, 1152,
            96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056, 1152]
bricks_y = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
            132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132]
particles = []
powerups = []

level = 1
MAX_LEVEL = 3



STATUS_PLAY = 1
STATUS_WIN = 2
STATUS_LOSE = 3
STATUS_MENU = 4
STATUS_EASTER = 5
game_status = STATUS_MENU

MODE_SOLO = 1
MODE_1VS1 = 2
game_mode = MODE_SOLO

game_status_msg = ""

def ball_reset():
    global ball_x, ball_speed_x, ball_y, ball_speed_y, paddle_x, paddle2_x
    ball_x = SCREEN_WIDTH / 2 -200
    ball_speed_x = 8
    ball_y = SCREEN_HEIGHT / 2
    ball_speed_y = 7
    paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
    paddle2_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
    return

def load_level(level):
    global bricks_x, bricks_y
    if level == 1:
        bricks_x = [96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056, 1152, 
                    96, 192, 288, 384, 480, 576, 672, 768, 864, 960, 1056, 1152]
        bricks_y = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                    132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132]
    
    elif level == 2:
        bricks_x = [384,480,576,672,768,480,576,672,576]
        bricks_y = [100,100,100,100,100,132,132,132,164]

    elif level == 3:
        bricks_x = [96, 192, 288, 960, 1056, 1152, 96, 192, 288, 960, 1056, 1152]
        bricks_y = [100, 100, 100, 100, 100, 100, 132, 132, 132, 132, 132, 132]
    return


def game_init(game_mode= MODE_SOLO):
    global game_status_msg, particles, powerups, level, bricks_x, bricks_y
    game_status_msg = ""
    level = 1
    if game_mode == MODE_SOLO:
        load_level(level)
    else:
        bricks_x = []
        bricks_y = []
    ball_reset()
    particles = []
    powerups = []
    return

# Effect op blokken
def spawn_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append({
            'x': x + BRICK_WIDTH / 2,
            'y': y + BRICK_HEIGHT / 2,
            'vx': random.uniform(-5, 5),
            'vy': random.uniform(-5, 5),
            'life': 12,
            'color': color
        })


#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)

#
# read images
#
winbackground = pygame.image.load('win.png').convert_alpha()
winbackground = pygame.transform.scale(winbackground, screen.get_size())

losebackground = pygame.image.load('lose.png').convert_alpha()
losebackground = pygame.transform.scale(losebackground, screen.get_size())

background = pygame.image.load('achtergrond.png').convert_alpha()
background = pygame.transform.scale(background, screen.get_size())

menubackground = pygame.image.load('startscherm.png').convert_alpha()
menubackground = pygame.transform.scale(menubackground, screen.get_size())

easter_egg = pygame.image.load('easteregg.png')
easter_egg = pygame.transform.scale(easter_egg, screen.get_size())

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()


ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1262, 726, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

paddle2_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle2_img.blit(spritesheet, (0, 0), (594, 910, 243, 64))
paddle2_img = pygame.transform.scale(paddle2_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

powerup_img = pygame.Surface((64, 61), pygame.SRCALPHA)
powerup_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))
powerup_img = pygame.transform.scale(powerup_img, (32, 32))

# game loop
####################### 

print('mygame is running')
running = True
while running:

########################
    #
    # read events
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        paddle_x += 10
    if keys[pygame.K_a]:
        paddle_x -= 10

    if keys[pygame.K_t] and keys[pygame.K_e] and keys[pygame.K_r]:
        game_status = STATUS_EASTER

    if game_status == STATUS_EASTER:
        if keys[pygame.K_q]:
            game_status = STATUS_MENU


    if game_mode == MODE_1VS1:
        if keys[pygame.K_j]:
            paddle2_x -= 10
        if keys[pygame.K_l]:
            paddle2_x += 10
    

    if game_status == STATUS_MENU:
        if keys[pygame.K_x]:
            game_init(MODE_SOLO)
            game_status = STATUS_PLAY
            game_mode = MODE_SOLO
        if keys[pygame.K_z]:
            game_init(MODE_1VS1)
            game_status = STATUS_PLAY
            game_mode = MODE_1VS1
            

    if game_status == STATUS_WIN or game_status == STATUS_LOSE:
        if keys[pygame.K_r]:
            game_init(game_mode)
            game_status = STATUS_PLAY
        if keys[pygame.K_q]:
            level = 1
            game_init()
            game_status = STATUS_MENU


    # move everything
    if game_status == STATUS_PLAY:
    # move ball
        ball_x = ball_x + ball_speed_x
        ball_y = ball_y + ball_speed_y

      #ball tester(only for testing)
      #  paddle_x = ball_x - 20

        # bounce ball
        if ball_x < 0:
            ball_speed_x = abs(ball_speed_x)
        if ball_x + BALL_WIDTH > SCREEN_WIDTH:
            ball_speed_x = abs(ball_speed_x) * -1
        if ball_y < 0:
            ball_speed_y = abs(ball_speed_y)
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
            ball_speed_y = abs(ball_speed_y) * -1

        # move paddle
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
        if paddle_x < 0:
            paddle_x = 0
        if game_mode == MODE_1VS1:
            if paddle2_x + PADDLE_WIDTH > SCREEN_WIDTH:
                paddle2_x = SCREEN_WIDTH - PADDLE_WIDTH
            if paddle2_x < 0:
                paddle2_x = 0

        # bounce paddle against ball
        if (
            ball_x + BALL_WIDTH > paddle_x and
            ball_x < paddle_x + PADDLE_WIDTH and
            ball_y + BALL_HEIGHT > paddle_y and
            ball_y < paddle_y + PADDLE_HEIGHT
        ):
            ball_speed_y = abs(ball_speed_y) * -1
            if keys[pygame.K_d]:
                ball_speed_x += 2
            if keys[pygame.K_a]:
                ball_speed_x -= 2
            ball_speed_x = max(-16, min(16, ball_speed_x))
            

        # Bounce paddle 2 against ball
        if game_mode == MODE_1VS1:
            if (
            ball_x + BALL_WIDTH > paddle2_x and
            ball_x < paddle2_x + PADDLE_WIDTH and
            ball_y + BALL_HEIGHT > paddle2_y and
            ball_y < paddle2_y + PADDLE_HEIGHT
        ):
                ball_speed_y = abs(ball_speed_y)
                if keys[pygame.K_l]:
                    ball_speed_x += 2
                if keys[pygame.K_j]:
                    ball_speed_x -= 2
                ball_speed_x = max (-16, min(16, ball_speed_x))
            

        # Bounce ball against brick

        for i in range(0, len(bricks_x)):
            if (
            ball_x + BALL_WIDTH > bricks_x[i] and
            ball_x < bricks_x[i] + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > bricks_y[i] and
            ball_y < bricks_y[i] + BRICK_HEIGHT
            ):
                if (
                ball_speed_y > 0 and
                ball_y < bricks_y[i]
                ):
                    ball_speed_y = abs(ball_speed_y) * -1
                    spawn_particles(bricks_x[i], bricks_y[i], 'LightBlue')
                    if random.randint(1,5) == 2:
                        powerups.append({'x': bricks_x[i], 'y': bricks_y[i], 'type': random.choice(['big_paddle','slow_ball','fast_ball'])})
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break
                elif (
                    ball_speed_y < 0 and
                    ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT
                ):
                    ball_speed_y = abs(ball_speed_y)
                    spawn_particles(bricks_x[i], bricks_y[i], 'LightBlue')
                    if random.randint(1,5) == 2:
                        powerups.append({'x': bricks_x[i], 'y': bricks_y[i], 'type': random.choice(['big_paddle','slow_ball','fast_ball'])})
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break
                elif (
                    ball_speed_x > 0 and
                    ball_x < bricks_x[i]
                ):
                    ball_speed_x = abs(ball_speed_x) * -1
                    spawn_particles(bricks_x[i], bricks_y[i], 'LightBlue')
                    if random.randint(1,5) == 2:
                        powerups.append({'x': bricks_x[i], 'y': bricks_y[i], 'type': random.choice(['big_paddle','slow_ball','fast_ball'])})
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break
                elif (
                    ball_speed_x < 0 and
                    ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH
                ):
                    ball_speed_x = abs(ball_speed_x)
                    spawn_particles(bricks_x[i], bricks_y[i], 'LightBlue')
                    if random.randint(1,5) == 2:
                        powerups.append({'x': bricks_x[i], 'y': bricks_y[i], 'type': random.choice(['big_paddle','slow_ball','fast_ball'])})
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break
                print('brick touched at ball_x = ' +
                    str(ball_x) + ' and ball_y = ' + str(ball_y))
#Effecten
        for p in particles[:]:
            p['x'] += p['vx']
            p['y']+= p['vy']
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)
        for powerup in powerups[:]:
            powerup['y'] += 3
            if powerup['y'] > SCREEN_HEIGHT:
                powerups.remove(powerup)
  
            elif (powerup['x'] < paddle_x + PADDLE_WIDTH and
                powerup['x'] + 20 > paddle_x and
                powerup['y'] < paddle_y + PADDLE_HEIGHT and
                powerup['y'] + 20 > paddle_y ) :
                powerups.remove(powerup)
                if powerup['type'] == 'big_paddle':
                    paddle_img = pygame.transform.scale(paddle_img,(PADDLE_WIDTH + 50, PADDLE_HEIGHT))

                elif powerup['type'] == 'slow_ball':
                    ball_speed_x *= 0.8
                    ball_speed_y *= 0.8

                elif powerup['type'] == 'fast_ball':
                    ball_speed_x *= 1.2
                    ball_speed_y *= 1.2        
    # Win
    if game_mode == MODE_SOLO:
        if len(bricks_x) == 0:
            level += 1
            if level > MAX_LEVEL:
                ball_speed_x = 0
                ball_speed_y = 0
                game_status = STATUS_WIN
            else:
                load_level(level)
                ball_reset()


    # Lose
    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status = STATUS_LOSE
    
    #Win and lose, 1vs1
    if game_mode == MODE_1VS1:
        if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
            game_status = STATUS_LOSE
        if ball_y  < paddle2_y:
            game_status = STATUS_WIN
   
    # draw everything

    # clear screen
    screen.fill('purple')
    if game_status == STATUS_PLAY:
        screen.blit(background)
        screen.blit(ball_img, (ball_x, ball_y))
        screen.blit(paddle_img, (paddle_x, paddle_y))
        if game_mode == MODE_1VS1:
            screen.blit(paddle2_img, (paddle2_x, paddle2_y))
        for i in range(0, len(bricks_x)):
            screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
        for p in particles:
            pygame.draw.rect(screen, p['color'], (p['x'], p['y'], 4, 4))
        for powerup in powerups:
            screen.blit(powerup_img, (powerup['x'], powerup['y']))
        if game_mode == MODE_SOLO:
            level_text= small_font.render('LEVEL ' + str(level), True, 'White')
        else:
            level_text = small_font.render('1 VS 1', True, 'White')
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 0))
    elif game_status == STATUS_WIN:
        screen.blit(winbackground)
        if game_mode == MODE_SOLO:
            small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
            sub = small_font.render('You win!', True, 'White')
            screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 350))
        else:
            small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
            sub = small_font.render('Player 1 Wins!!', True, 'White')
            screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 350))
        prompt = small_font.render('Press [r] to restart, or press [q] for menu', True, 'White')
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 450))
    elif game_status == STATUS_LOSE:
        screen.blit(losebackground)
        if game_mode == MODE_SOLO:
            small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
            sub = small_font.render('You lost in LEVEL ' + str(level), True, 'White')
            screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 350))
        else:
            small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
            sub = small_font.render('Player 2 Wins!!', True, 'White')
            screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 350))
        prompt = small_font.render('Press [r] to restart, or press [q] for menu', True, 'White')
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 450))
    elif game_status == STATUS_MENU:
        screen.blit(menubackground)
        small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
        sub = small_font.render('A / D or J / L to move paddle', True, 'yellow')
        screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 350))
       
        prompt = small_font.render('Press [x] to start Solo Adventure', True, 'White')
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 450))
        prompt2 = small_font.render('Press [z] to start 1 VS 1', True, 'White')
        screen.blit(prompt2, (SCREEN_WIDTH//2 - prompt2.get_width()//2, 300))
    elif game_status == STATUS_EASTER:
        screen.blit(easter_egg)
        small_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
        sub = small_font.render('Je Hebt het gevonden, JIPPIE!!!!', True, 'White')
        sub2 = small_font.render('Dit heb je verdient!', True, 'White')
        screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 350))
        prompt = small_font.render('press [q] for menu', True, 'White')
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 450))


    # draw game status message
    game_status_img = font.render(game_status_msg, True, 'White')
    # (0, 0) is top left corner of screen
    screen.blit(game_status_img, (SCREEN_WIDTH//2  - game_status_img.get_width() // 2, SCREEN_HEIGHT//2 - game_status_img.get_height() // 2))

    # show screen
    pygame.display.flip()

    #
    # wait until next frame
    # Uitbreiding, bouncing DVD screensaver, EN MOEILIJKHEDEN. EN MULTIPLAYER, startscherm. confetti als win

    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
