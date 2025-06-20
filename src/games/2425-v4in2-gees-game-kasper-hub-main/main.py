#
# BREAKOUT GAME 
#

import pygame, time
import random
#
# definitions 
# define global variables
game_status_msg_loss = ""
game_status_msg_win = ""

FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_HEIGHT = 32
BRICK_WIDTH = 96
HEART_WIDTH = 32
HEART_HEIGHT = 29
ball_x = 600
ball_speed_x = 0
ball_y = 400
ball_speed_y = -9

paddle_x = 575
paddle_y = 600
levens = 3 # begin met 3 levens

wacht_op_verdergaan = False
pauze = True
# levelsysteem
level_index = 0

def get_levels():
    return [
        [  # Level 1
            (100, 100), (196, 100), (292, 100), (388, 100), (484, 100), (580, 100), (676, 100), (772, 100), 
            (868, 100), (964, 100), (1060, 100),(100, 132), (196, 132), (292, 132), (388, 132), (484, 132),
            (580, 132), (676, 132), (772, 132), (868, 132), (964, 132), (1060, 132), (484, 164), (676, 164)
        ],
        [  # Level 2
            (100, 100), (196, 100), (292, 100), (388, 100), (772, 100), (868, 100), (964, 100), (1060, 100), 
            (100, 132), (196, 132), (292, 132), (388, 132), (772, 132), (868, 132), (964, 132), (1060, 132),
            (100, 164), (196, 164), (292, 164), (388, 164), (772, 164), (868, 164), (964, 164), (1060, 164),
        ],
        [  # Level 3
            (388, 68), (772, 68), (292, 100), (388, 100), (484, 100), (676, 100), (772, 100), (868, 100),
            (292, 132), (388, 132), (484, 132), (676, 132), (772, 132), (868, 132), (292, 164), (388, 164), 
            (484, 164), (676, 164), (772, 164), (868, 164), (196, 196), (292, 196), (388, 196), (772, 196), 
            (868, 196), (964, 196), (196, 228), (292, 228), (388, 228), (772, 228), (868, 228), (964, 228),
        ],
        [  # Level 4
            (100, 228), (196, 228), (292, 228), (388, 228), (484, 228), (580, 228), (676, 228), (772, 228), (868, 228), (964, 228), (1060, 228), (1156, 228),
            (4, 164), (100, 164), (196, 164), (292, 164), (388, 164), (484, 164), (580, 164), (676, 164), (772, 164), (868, 164), (964, 164), (1060, 164),
            (100, 100), (196, 100), (292, 100), (388, 100), (484, 100), (580, 100), (676, 100), (772, 100), (868, 100), (964, 100), (1060, 100), (1156, 100),

        ],
        [  # Level 5: Geest
             # G 
            (0, 100), (96, 100), (192, 100), (0, 132), (0, 164), (192, 164), (0, 196), (192, 196), (0, 228), (96, 228), (192, 228),
            # E 
            (298, 100), (394, 100), (298, 132), (298, 164), (394, 164), (298, 196), (298, 228), (394, 228),
            # E 
            (500, 100), (596, 100), (500, 132), (500, 164), (596, 164), (500, 196), (500, 228), (596, 228),
            # S 
            (702, 100), (798, 100), (894, 100), (702, 132), (702, 164), (798, 164), (894, 164), (894, 196), (702, 228), (798, 228), (894, 228),
            # T 
            (1000, 100), (1096, 100), (1192, 100), (1096, 132), (1096, 164),(1096, 196), (1096, 228)
        ],
    ]


levels = get_levels()
bricks_x = []
bricks_y = []
bricks_health = []
brick_textures = []

# laad level
def load_current_level():
    global bricks_x, bricks_y, bricks_health, brick_textures
    bricks_x = []
    bricks_y = []
    bricks_health = []
    for x, y in levels[level_index]:
        bricks_x.append(x)
        bricks_y.append(y)

        if level_index == 0:
            health = 1
        elif level_index == 1:
            health = 1
        elif level_index == 2:
            health = 2
        else:
            health = 3
        bricks_health.append(health)

        if health == 1:
            brick_texture = random.choice(cracked_bricks)
        else:
            brick_texture = random.choice(normal_bricks)
        brick_textures.append(brick_texture)

# game opnieuw spelen
def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global paddle_x
    global game_status_msg_loss, game_status_msg_win
    global levens
    global pauze
    
    pauze = True

    paddle_x = 575
    ball_x = 800
    ball_y = 400
    ball_speed_x = 0
    ball_speed_y = -9
    levens = 3

    game_status_msg_loss = ""
    game_status_msg_win = ""

    load_current_level()

# verlies leven
def verlies_leven():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, wacht_op_verdergaan, game_status_msg_loss

    game_status_msg_loss = "Je verloor een leven! Druk op Z om door te gaan."
    ball_speed_x = 0
    ball_speed_y = 0
    ball_x = paddle_x + (PADDLE_WIDTH // 2) - (BALL_WIDTH // 2)
    ball_y = paddle_y - BALL_HEIGHT - 10
    wacht_op_verdergaan = True

# pauze knop en uitlegscherm
def toon_uitleg_scherm():
    uitleg_regels = [
        "Breakout Controls:",
        "A: Beweeg naar links",
        "D: Beweeg naar rechts",
        "Z: Ga verder na verlies van een leven",
        "Q: Ga naar het volgende level",
        "R: Herstart het spel",
        "C: Pauze aan/uit",
        "",
        "Druk op C om te beginnen!"
    ]
    i = 0
    for regel in uitleg_regels:
        regel_img = font.render(regel, True, "black")
        screen.blit(regel_img,((SCREEN_WIDTH / 2) - regel_img.get_width() / 2, 200 + i * 50))
        i += 1
#
# init game
#
pygame.init()
font = pygame.font.SysFont('default', 64)
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
# lichtblauw brick cracked
brick_img_1 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_1.blit(spritesheet, (0, 0), (386, 520, 384, 128))
brick_img_1 = pygame.transform.scale(brick_img_1, (BRICK_WIDTH, BRICK_HEIGHT))
# lichtblauw brick
brick_img_2 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_2.blit(spritesheet, (0, 0), (386, 650, 384, 128))
brick_img_2 = pygame.transform.scale(brick_img_2, (BRICK_WIDTH, BRICK_HEIGHT))
# donkerblauw brick
brick_img_3 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_3.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_img_3 = pygame.transform.scale(brick_img_3, (BRICK_WIDTH, BRICK_HEIGHT))
# donkerblauw brick cracked
brick_img_4 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_4.blit(spritesheet, (0, 0), (0, 0, 384, 128))
brick_img_4 = pygame.transform.scale(brick_img_4, (BRICK_WIDTH, BRICK_HEIGHT))
# grijs brick
brick_img_5 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_5.blit(spritesheet, (0, 0), (772, 520, 384, 128))
brick_img_5 = pygame.transform.scale(brick_img_5, (BRICK_WIDTH, BRICK_HEIGHT))
# grijs brick cracked
brick_img_6 = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_img_6.blit(spritesheet, (0, 0), (0, 650, 384, 128))
brick_img_6 = pygame.transform.scale(brick_img_6, (BRICK_WIDTH, BRICK_HEIGHT))
# hartje/leven
heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (HEART_WIDTH, HEART_HEIGHT))

cracked_bricks = [brick_img_1, brick_img_4, brick_img_6]
normal_bricks = [brick_img_2, brick_img_3, brick_img_5]
#
# start game
#
reset_game()
print('mygame is running')
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                pauze = not pauze
    keys = pygame.key.get_pressed()

    # Paddle movement
    if keys[pygame.K_d]:
        paddle_x += 16
    if keys[pygame.K_a]:
        paddle_x -= 16

    # Keep paddle in bounds
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
        paddle_x = 0

    # Reset game
    if (game_status_msg_loss or game_status_msg_win == "Je hebt het spel uitgespeeld!") and keys[pygame.K_r]:
        level_index = 0
        reset_game()
    
    # hartjes reset
    if game_status_msg_loss == "Game Over!" and keys[pygame.K_r]:
        level_index = 0 
        levens = 3
        reset_game()
    
    # wachten op verdergaan na verliezen leven
    if wacht_op_verdergaan and keys[pygame.K_z] and game_status_msg_loss != "Game Over!":
        ball_speed_y = 9
        ball_speed_x = 0
        game_status_msg_loss = ""
        wacht_op_verdergaan = False

    # Naar volgende level
    if keys[pygame.K_q] and game_status_msg_win.startswith("Level voltooid"):
        level_index += 1
        if level_index >= len(levels):
            game_status_msg_win = "Je hebt het spel uitgespeeld!"
        else:
            reset_game()
    
    # kijken of het pauze is
    if pauze:
        screen.fill("lightblue")  # Of een andere achtergrondkleur
        toon_uitleg_scherm()
        level_tekst = font.render("Level " + str(level_index + 1), True, "black")
        screen.blit(level_tekst, (10, 10))
        pygame.display.flip()
        fps_clock.tick(FPS)
        continue


    # Ball movement
    if not (game_status_msg_loss or game_status_msg_win):
        ball_x += ball_speed_x
        ball_y += ball_speed_y

    if ball_x < 0:
        ball_speed_x = abs(ball_speed_x)
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:
        ball_speed_x = -abs(ball_speed_x)
    if ball_y < 0:
        ball_speed_y = abs(ball_speed_y)
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        ball_speed_y = -abs(ball_speed_y)

    # Ball-paddle collision
    if (ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT):
        
        ball_speed_y = -abs(ball_speed_y)

        paddle_midden = paddle_x + PADDLE_WIDTH / 2
        ball_midden = ball_x + BALL_WIDTH / 2
        raak_ratio = (ball_midden - paddle_midden) / (PADDLE_WIDTH / 2)   # tussen -1 en 1
        max_bounce_angle = 9        # maximale afwijking

        ball_speed_x = (raak_ratio) * max_bounce_angle

    # Ball-brick collision
    for i in range(len(bricks_x) - 1, -1, -1):
        if (ball_x + BALL_WIDTH > bricks_x[i] and ball_x < bricks_x[i] + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT):
            if ball_speed_y > 0 and ball_y + BALL_HEIGHT <= bricks_y[i] + (ball_speed_y * 2):
                ball_speed_y = -abs(ball_speed_y)
            elif ball_speed_y < 0 and ball_y <= bricks_y[i] + BRICK_HEIGHT - (ball_speed_y * 2):
                ball_speed_y = abs(ball_speed_y)
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                ball_speed_x = abs(ball_speed_x)
            elif ball_speed_x > 0 and ball_x < bricks_x[i]:
                ball_speed_x = -abs(ball_speed_x)
            bricks_health[i] -= 1    
            if bricks_health[i] == 1:
                brick_textures[i] = random.choice(cracked_bricks)
            if bricks_health[i] <= 0:
                bricks_x.pop(i)
                bricks_y.pop(i)
                bricks_health.pop(i)
                brick_textures.pop(i)
                ball_speed_x *= 1.01
                ball_speed_y *= 1.01
            break

    # Check verlies
    if ball_y - BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
        levens -= 1
        if levens <= 0:
            levens = 0  # extra veiligheid
            wacht_op_verdergaan = False  # belangrijk
            game_status_msg_loss = "Game Over!"
            ball_speed_x = 0
            ball_speed_y = 0
        else:
            verlies_leven()
        

    # Check winst
    if len(bricks_x) == 0 and not game_status_msg_win:
        ball_speed_x = 0
        ball_speed_y = 0
        game_status_msg_win = "Level voltooid! Druk op Q"

    #
    # DRAWING
    #
    screen.fill("lightpink")
    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(paddle_img, (paddle_x, paddle_y))
    for i in range(len(bricks_x)):
        screen.blit(brick_textures[i], (bricks_x[i], bricks_y[i]))
    # level tekst
    level_tekst = font.render("Level " + str(level_index + 1), True, "black")
    screen.blit(level_tekst, (10, 10))
    #levens tekst
    for i in range(levens):
        screen.blit(heart_img, (SCREEN_WIDTH - (i + 1) * 36 - 10, 10))
    # Draw messages
    if game_status_msg_loss:
        game_status_img = font.render(game_status_msg_loss, True, 'red')
        screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.get_width() / 2), SCREEN_HEIGHT / 2 - 40))
        if levens == 0:
            restart_msg_img = font.render("Druk op 'r' om het spel te herstarten", True, "white")
            screen.blit(restart_msg_img, ((SCREEN_WIDTH / 2) - (restart_msg_img.get_width() / 2), SCREEN_HEIGHT / 2 + 40))

    if game_status_msg_win:
        game_status_img = font.render(game_status_msg_win, True, 'green')
        screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.get_width() / 2), SCREEN_HEIGHT / 2 - 40))
        if "voltooid" in game_status_msg_win:
            next_level_img = font.render("Druk op Q voor volgende level", True, "white")
            screen.blit(next_level_img, ((SCREEN_WIDTH / 2) - (next_level_img.get_width() / 2), SCREEN_HEIGHT / 2 + 40))
        else:
            restart_msg_img = font.render("Druk op 'r' om het spel te herstarten", True, "white")
            screen.blit(restart_msg_img, ((SCREEN_WIDTH / 2) - (restart_msg_img.get_width() / 2), SCREEN_HEIGHT / 2 + 40))

    pygame.display.flip()
    fps_clock.tick(FPS)

print('mygame stopt running')