#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 60 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BALL_WIDTH = 16
BALL_HEIGHT = 16

PADDLE_WIDTH = 122
PADDLE_HEIGHT = 32

BRICK_WIDTH = 125
BRICK_HEIGHT = 52

# define brick class
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.removing = False
        self.removal_timer = 0
        self.removal_speed = -10

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT)

    def update(self):
        if self.removing:
            self.y += self.removal_speed
            self.removal_timer -= 1 / FPS

# Levels definitie: lijst van lijsten met posities
levels = [
    # Level 1 dam bord patroon
    [(50 + col * (BRICK_WIDTH + 5), 50 + row * (BRICK_HEIGHT + 5))
     for row in range(4) for col in range(9)
     if (row + col) % 2 == 0],
    # Level 2 pyramide
    [(SCREEN_WIDTH // 2 - (BRICK_WIDTH // 2) + col * (BRICK_WIDTH + 5) - row * (BRICK_WIDTH // 2 + 2), 
      50 + row * (BRICK_HEIGHT + 5))
     for row in range(5) for col in range(row + 1)],
    # Level 3 zigzag
    [(50 + col * (BRICK_WIDTH + 5), 
      50 + row * (BRICK_HEIGHT + 5) + (col % 2) * (BRICK_HEIGHT // 2))
     for row in range(3) for col in range(8)],
    # Level 4 lijn
    [(100 + col * (BRICK_WIDTH + 5), SCREEN_HEIGHT // 3)
     for col in range(7)] +
    [(100 + col * (BRICK_WIDTH + 5), SCREEN_HEIGHT // 3 + BRICK_HEIGHT + 10)
     for col in range(7)],
]
# lijst blokken per level
def create_bricks(level_index):
    positions = levels[level_index]
    return [Brick(x, y) for (x, y) in positions]

# game variables
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT - 150
ball_speed_x = 2
ball_speed_y = 4
paddle_speed = 5

paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100.

game_status_msg = ""
game_status = "start"

current_level = 0

#
# init game
#

pygame.init()
font_big = pygame.font.SysFont('default', 64)
font_small = pygame.font.SysFont('default', 36)
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
paddle_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) 

brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
brick_img.blit(spritesheet, (0, 0), (386, 650, 384, 128))   
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

bricks = []

#
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

    # Clear screen
    screen.fill('black')

    if game_status == "start":
        # laat instructies zien
        title_text = font_big.render("BREAKOUT GAME", True, 'white')
        instruct_text1 = font_small.render("Gebruik A en D om te bewegen", True, 'white')
        instruct_text2 = font_small.render("Druk Q om te starten", True, 'white')
        succes_text = font_big.render("succes", True, 'red')

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
        screen.blit(instruct_text1, (SCREEN_WIDTH // 2 - instruct_text1.get_width() // 2, 350))
        screen.blit(instruct_text2, (SCREEN_WIDTH // 2 - instruct_text2.get_width() // 2, 400))
        screen.blit(succes_text, (SCREEN_WIDTH // 2 - succes_text.get_width() // 2, 450))

        if keys[pygame.K_q]:
            # Reset alle game variabelen en start level 0
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT - 150
            ball_speed_x = 3
            ball_speed_y = 6
            paddle_x = SCREEN_WIDTH / 2
            game_status_msg = ""
            current_level = 0
            bricks = create_bricks(current_level)
            game_status = "playing"

    elif game_status == "playing":
        # move paddle
        if keys[pygame.K_d]:  # move right
            paddle_x += paddle_speed
        elif keys[pygame.K_a]:  # move left
            paddle_x -= paddle_speed
        
        # god mode (paddle volgt bal)
        if keys[pygame.K_c]:
            paddle_x = ball_x - PADDLE_WIDTH / 2

        # game speedup
        if keys[pygame.K_x]:
            FPS = 120 
        else:
            FPS = 60

        # reset/alle blokken verwijderen
        if keys[pygame.K_r]:
            bricks = []

        # move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # bounce ball
        if ball_x < 0: 
            ball_speed_x = abs(ball_speed_x) 
        if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
            ball_speed_x = -abs(ball_speed_x) 
          
        if ball_y < 0: 
            ball_speed_y = abs(ball_speed_y) 
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
            ball_speed_y = -abs(ball_speed_y) 

        # handle collisions
        if paddle_x < 0:
            paddle_x = 0        # paddle stop bij rand van scherm
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        if (ball_x + BALL_WIDTH > paddle_x and
            ball_x < paddle_x + PADDLE_WIDTH and
            ball_y + BALL_HEIGHT > paddle_y and
            ball_y < paddle_y + PADDLE_HEIGHT):
            ball_speed_y = -abs(ball_speed_y)
            
        # ball_rect aangemaakt voor latere code
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_HEIGHT)

        # block removal en raaking
        for brick in bricks:
            if brick.removing:
                continue

            if ball_rect.colliderect(brick.get_rect()):
                overlap_left = (brick.x + BRICK_WIDTH) - ball_x
                overlap_right = (ball_x + BALL_WIDTH) - brick.x
                overlap_top = (brick.y + BRICK_HEIGHT) - ball_y
                overlap_bottom = (ball_y + BALL_HEIGHT) - brick.y

                if min(overlap_left, overlap_right) < min(overlap_top, overlap_bottom):
                    ball_speed_x *= -1
                else:
                    ball_speed_y *= -1

                brick.removing = True
                brick.removal_timer = 0.3

                # Verhoog de snelheid van de bal per blok
                if ball_speed_x > 0:
                  ball_speed_x += 0.2
                else:
                  ball_speed_x -= 0.2

                if ball_speed_y > 0:
                  ball_speed_y += 0.2
                else:
                  ball_speed_y -= 0.2

                #paddle speed gelijk met ball speed houden
                paddle_speed += 0.2


        # update bricks
        for brick in bricks:
            brick.update()

        # verwijder bricks die klaar zijn met verdwijnen
        bricks = [brick for brick in bricks if not (brick.removing and brick.removal_timer <= 0)]

        # Check win - ga naar volgend level of win-game
        if len(bricks) == 0:
            current_level += 1
            if current_level >= len(levels):
                game_status = "won"
            else:
                # reset ball & paddle pos en bricks voor nieuw level
                ball_x = SCREEN_WIDTH // 2
                ball_y = SCREEN_HEIGHT - 150
                ball_speed_x = 3
                ball_speed_y = 6
                paddle_x = SCREEN_WIDTH / 2
                bricks = create_bricks(current_level)

        # Check lose
        if ball_y + BALL_HEIGHT > SCREEN_HEIGHT - 15:
            game_status = "lost"

        # draw everything
        screen.blit(ball_img, (ball_x, ball_y))
        screen.blit(paddle_img, (paddle_x, paddle_y))
        for brick in bricks:
            screen.blit(brick_img, (brick.x, brick.y))
    # win message
    elif game_status == "won":
        win_text = font_big.render("Je hebt gewonnen, goed gedaan! Mij lukte het niet...", True, 'green')
        restart_text = font_small.render("Druk Q om opnieuw te spelen", True, 'white')
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 300))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
        if keys[pygame.K_q]:
            # reset
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT - 150
            ball_speed_x = 3
            ball_speed_y = 6
            paddle_x = SCREEN_WIDTH / 2
            current_level = 0
            bricks = create_bricks(current_level)
            game_status = "playing"
    # Lose message
    elif game_status == "lost":
        lose_text = font_big.render("Da's nie goed, gelukkig is opnieuw proberen gratis.", True, 'red')
        restart_text = font_small.render("Druk Q om opnieuw te spelen", True, 'white')
        screen.blit(lose_text, (SCREEN_WIDTH // 2 - lose_text.get_width() // 2, 300))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
        if keys[pygame.K_q]:
            # reset
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT - 150
            ball_speed_x = 3
            ball_speed_y = 6
            paddle_x = SCREEN_WIDTH / 2
            current_level = 0
            bricks = create_bricks(current_level)
            game_status = "playing"

    pygame.display.flip()
    fps_clock.tick(FPS)

print('mygame stopt running')
