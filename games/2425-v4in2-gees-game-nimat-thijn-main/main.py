# BREAKOUT GAME 

import pygame, time, random

# definitions 
FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280      # screensize in x-direction in pixels
SCREEN_HEIGHT = 720      # screensize in y direction in pixels
BALL_WIDTH = 16          # ballsize in x-direction in pixels
BALL_HEIGHT = 16         # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 110
BRICK_HEIGHT = 50

ball_x = -50+SCREEN_WIDTH / 2               # x-position of ball in pixels 
ball_speed_x = 6         # speed of ball in x-direction in pixels per frame
ball_y = SCREEN_HEIGHT / 2
ball_speed_y = 10

paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT  -  100

bricks_x = [
    0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
    0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
    0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
    0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
    0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100
]
bricks_x = [x + 35 for x in bricks_x]
bricks_y = [
    40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
    90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
    140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140,
    190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190,
    240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240
]

bricks_colors = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
    2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
    3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3,
    4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4
]
random.shuffle(bricks_colors)

# init game
pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# read images

# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

background = pygame.image.load('93121.jpg').convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH,SCREEN_HEIGHT)) 

brick_pixels = [
    (771, 389), (385, 649), (385, 129), (0, 129), (771, 519),
    (385, 779), (0, 389), (771, 259), (771, 0), (385, 389)
]

brick_imgs = []
for px in brick_pixels:
    img = pygame.Surface((386, 130), pygame.SRCALPHA)
    img.blit(spritesheet, (0, 0), (px[0], px[1], 386, 130))
    img = pygame.transform.scale(img, (BRICK_WIDTH, BRICK_HEIGHT))
    brick_imgs.append(img)

button_img = pygame.Surface((386, 130), pygame.SRCALPHA)
button_img.blit(spritesheet, (0, 0), (771, 389, 386, 130))
button_img = pygame.transform.scale(button_img, (300, 60))

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (144, 32)) # resize image
# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to ball_img at (0,0)
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))  
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT 
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

heart_img = pygame.Surface((64, 64), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1636, 651, 64, 64))
heart_img = pygame.transform.scale(heart_img, (32, 32))  # resize smaller for lives display

# define global variables
game_status_msg = ""
lives = 3
game_over = False

def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    global paddle_x, paddle_y
    global bricks_x, bricks_y, bricks_colors
    global game_status_msg, game_over
    global lives

    ball_x = -50 + SCREEN_WIDTH / 2               
    ball_speed_x = 6         
    ball_y = SCREEN_HEIGHT / 2
    ball_speed_y = 10

    paddle_x = SCREEN_WIDTH / 2
    paddle_y = SCREEN_HEIGHT - 100

    bricks_x = [
        0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
        0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
        0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
        0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100,
        0, 110, 220, 330, 440, 550, 660, 770, 880, 990, 1100
    ]
    bricks_x = [x + 35 for x in bricks_x]
    bricks_y = [
        40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
        90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90,
        140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140,
        190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190,
        240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240
    ]

    bricks_colors = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1,
        2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2,
        3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3,
        4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4
    ]
    random.shuffle(bricks_colors)

    game_status_msg = "Speel met [A] en [D]"
    game_over = False
    lives = 3

reset_game()
# game loop

print('mygame is running')
running = True
while running:
    game_status_msg = "Speel met [A] en [D]"

    # read events
    for event in pygame.event.get():    # read all events
        if event.type == pygame.QUIT:   # GUI is closed
            running = False             # end program
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if SCREEN_WIDTH//2 - 150 <= mouse_x <= SCREEN_WIDTH//2 + 150 and SCREEN_HEIGHT//2 + 50 <= mouse_y <= SCREEN_HEIGHT//2 + 110:
             reset_game()

    keys = pygame.key.get_pressed()     # read which keys are down
    if keys[pygame.K_d] : # key d is down
       paddle_x = paddle_x + 20
    if keys[pygame.K_a] : # key a is down
       paddle_x = paddle_x - 20


    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
       paddle_x = 0 
    # move everything

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

   # bounce ball against edges of screen
    if ball_x < 0 :   # left edge
      ball_speed_x = abs(ball_speed_x)          # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:      # right edge
      ball_speed_x = abs(ball_speed_x) * -1     # negative x speed = move left

    if ball_y < 0 :   # top edge
      ball_speed_y = abs(ball_speed_y)          # positive y-speed = move right
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:      # bottom edge
      ball_speed_y = abs(ball_speed_y) * -1     # negative y speed = move left
    
  
    # paddle bounche
    if (ball_x + BALL_WIDTH > paddle_x and 
    ball_x < paddle_x + PADDLE_WIDTH and
    ball_y + BALL_HEIGHT > paddle_y and
    ball_y < paddle_y + PADDLE_HEIGHT):
       
       # Calculate hit position relative to center of paddle
       paddle_center = paddle_x + PADDLE_WIDTH / 2
       ball_center = ball_x + BALL_WIDTH / 2
       distance_from_center = ball_center - paddle_center

       # Normalize: -1 (far left), 0 (center), 1 (far right)
       normalized = distance_from_center / (PADDLE_WIDTH / 2)

       # Adjust ball direction: horizontal speed depends on where it hit
       ball_speed_x = normalized * 10  # 10 is max horizontal speed
       ball_speed_y = -abs(ball_speed_y)

       print("ball botst tegen paddle")

    # brick collision
    for i in range(len(bricks_x)):
       if (ball_x + BALL_WIDTH > bricks_x[i] and
           ball_x < bricks_x[i] + BRICK_WIDTH and
           ball_y + BALL_HEIGHT > bricks_y[i] and
           ball_y < bricks_y[i] + BRICK_HEIGHT):
         print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))

         ball_speed_x *= 1.05
         ball_speed_y *= 1.05

         # vertical touch
         if ball_speed_y > 0 and ball_y + BALL_HEIGHT - ball_speed_y <= bricks_y[i]:
            ball_speed_y = -abs(ball_speed_y)

         elif ball_speed_y < 0 and ball_y - ball_speed_y >= bricks_y[i] + BRICK_HEIGHT:
            ball_speed_y = abs(ball_speed_y)

         # horizontal touch
         elif ball_speed_x > 0 and ball_x + BALL_WIDTH - ball_speed_x <= bricks_x[i]:
            ball_speed_x = -abs(ball_speed_x)

         elif ball_speed_x < 0 and ball_x - ball_speed_x >= bricks_x[i] + BRICK_WIDTH:
            ball_speed_x = abs(ball_speed_x)

         bricks_x.pop(i)
         bricks_y.pop(i)
         bricks_colors.pop(i)
         break

    # handle collisions
    ball_bottom = ball_y + BALL_HEIGHT
    if ball_bottom >= SCREEN_HEIGHT:
       lives -= 1
       if lives <= 0:
         game_status_msg = "YOU LOST!"
         ball_speed_y = 0
         ball_speed_x = 0
         game_over = True
       else:
        #Freeze the game
        ball_speed_x = 0
        ball_speed_y = 0

        # Countdown before resuming
        countdown_font = pygame.font.SysFont('impact', 200)
        for n in [3, 2, 1]:
            screen.blit(background, (0, 0))
            screen.blit(ball_img, (ball_x, ball_y))
            screen.blit(paddle_img, (paddle_x, paddle_y))
            for i in range(len(bricks_x)):
                color_idx = bricks_colors[i]
                screen.blit(brick_imgs[color_idx], (bricks_x[i], bricks_y[i]))
            for i in range(lives):
                screen.blit(heart_img, (SCREEN_WIDTH - 40 * (i + 1), 10))

            # Draw countdown number
            text = countdown_font.render(str(n), True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

            pygame.display.flip()
            pygame.time.wait(1000)

        # Reset ball and paddle
        ball_x = SCREEN_WIDTH / 2 - BALL_WIDTH / 2
        ball_y = SCREEN_HEIGHT / 2
        paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
        ball_speed_x = random.choice([-6, 6])
        ball_speed_y = -10

    # win condition
    if len(bricks_x) == 0:
       game_status_msg = "YOU WON!"
       ball_speed_x = 0
       ball_speed_y = 0
       game_over = True
    # move everything

    # wait until next frame
    # 
    # handle collisions
    #
    # draw everything
    # draw everything
  
    # clear screen
    screen.blit(background, (0, 0))
    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))
    # draw bricks
    for i in range(len(bricks_x)):
        color_idx = bricks_colors[i]
        screen.blit(brick_imgs[color_idx], (bricks_x[i], bricks_y[i]))
    # show screen
    # draw lives hearts on top right
    for i in range(lives):
        screen.blit(heart_img, (SCREEN_WIDTH - 40 * (i + 1), 5))
    # draw button
    if game_over:
     button_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50, 300, 60)
     screen.blit(button_img, button_rect.topleft)

     font = pygame.font.SysFont('default', 48)
     button_text = font.render("Try Again", True, (255, 255, 255))
     button_text_rect = button_text.get_rect(center=button_rect.center)
     screen.blit(button_text, button_text_rect)

    # draw game status message
    font = pygame.font.SysFont('default', 50)
    game_status_img = font.render(game_status_msg, True, 'green')
    screen.blit(game_status_img, (0, 0)) # (0, 0) is top left corner of screen
    pygame.display.flip() 

    # wait until next frame
    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')

