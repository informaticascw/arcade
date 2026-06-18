#
# BREAKOUT GAME
#

import pygame
import time

#
# definitions
#

FPS = 30  # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16  # ballsize in x-direction in pixels
BALL_HEIGHT = 16  # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2
paddle_speed_x = 10
paddle_y = SCREEN_HEIGHT - 100
paddle_center = paddle_x + PADDLE_WIDTH  / 2
ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2   # x-position of ball in pixels
ball_speed_x = 0  # speed of ball in x-direction in pixels per frame
ball_y = paddle_y - BALL_HEIGHT - 10
ball_speed_y = 0
ball_center = ball_x + BALL_WIDTH / 2
offset = ball_center - paddle_center
game_won = False


# bricks
brick_animations = []

# Define global variables
game_status_msg = ""

# init game

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# read images

# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

#background_imgs
backgroundlevel1_img = pygame.image.load('vault.png').convert()

backgroundlevel1_img = pygame.transform.scale(
    backgroundlevel1_img,
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# brick_darkblue_img
brick_darkblue_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_darkblue_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))
brick_darkblue_img = pygame.transform.scale(
    brick_darkblue_img, (BRICK_WIDTH, BRICK_HEIGHT))

# brick_lightblue_img
brick_lightblue_img = pygame.Surface((384, 128), pygame.SRCALPHA)
brick_lightblue_img.blit(spritesheet, (0, 0), (386, 650, 384, 128))
brick_lightblue_img = pygame.transform.scale(
    brick_lightblue_img, (BRICK_WIDTH, BRICK_HEIGHT)
)

# paddle_img
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# ball_img
# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
# copy part (x-left=1403, y-top=652, width=64, height=64) from spritesheet to
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))

#levels
levels = [
    #level 1
    {
        "bricks_x": [
            600, 
            552, 648,
            504, 600, 696,
            456, 552, 648, 744,
            504, 600, 696,
            552, 648,
            600,
        ],

        "bricks_y": [
            165,
            197, 197,
            229, 229, 229,
            261, 261, 261, 261,
            293, 293, 293,
            325, 325,
            357,
        ],

        "bricks_type": [
            "dark",
            "dark", "dark",
            "dark", "light", "dark",
            "dark", "light", "light", "dark",
            "dark", "light", "dark",
            "dark", "dark",
            "dark",
        ]                
    },

    #level 2
    {
         "bricks_x": [
           176,
           128, 224,
           80, 176, 272,
           128, 224,
           176,

           592,
           544, 640,
           496, 592, 688,
           544, 640,
           592,

           1008,
           960, 1056,
           912, 1008, 1104,
           960, 1056,
           1008,
       ],

       "bricks_y": [
           268,
           300, 300,
           332, 332, 332,
           364, 364,
           396,

           268,
           300, 300,
           332, 332, 332,
           364, 364,
           396,

           268,
           300, 300,
           332, 332, 332,
           364, 364,
           396,         
       ],

       "bricks_type": [
           "dark",
           "dark", "dark",
           "dark", "light", "dark",
           "dark", "dark",
           "dark",

           "dark",
           "dark", "dark",
           "dark", "light", "dark",
           "dark", "dark",
           "dark",

           "dark",
           "dark", "dark",
           "dark", "light", "dark",
           "dark", "dark",
           "dark",  
       ]              
    },
    
    #level 3
    {
       "bricks_x": [
            176,
            128, 224,
            176,
            
            600,
            552, 648,
            504, 600, 696,
            456, 552, 648, 744,
            408, 504, 600, 696, 792,
            456, 552, 648, 744,
            504, 600, 696,
            552, 648,
            600,

            1008,
            960, 1056,
            1008,
        ],

        "bricks_y": [
            284,
            316, 316,
            348,

            150,
            182, 182,
            214, 214, 214,
            246, 246, 246, 246,
            278, 278, 278, 278, 278,
            310, 310, 310, 310,
            342, 342, 342, 
            374, 374,
            406,

            284,
            316, 316,
            348,
        ],

        "bricks_type": [
            "light",
            "light", "light",
            "light",
            
            "dark",
            "dark", "dark",
            "dark", "light", "dark",
            "dark", "light", "light", "dark",
            "dark", "light", "light", "light", "dark",
            "dark", "light", "light", "dark",
            "dark", "light", "dark",
            "dark", "dark",
            "dark",

            "light",
            "light", "light",
            "light",

        ]
    }
]

# game loop
current_level = 0

bricks_x = levels[current_level]["bricks_x"].copy()
bricks_y = levels[current_level]["bricks_y"].copy()
bricks_type = levels[current_level]["bricks_type"].copy()

waiting = True
start_time = pygame.time.get_ticks()

retry_rect = pygame.Rect(
    SCREEN_WIDTH // 2 - 100,
    SCREEN_HEIGHT // 2 + 50,
    200,
    60
)

print('mygame is running')
running = True
while running:
  # read events
    # move everything
    # handle collisions
    # draw everything
    # wait until next frame

    for event in pygame.event.get():  # read all events
        if event.type == pygame.QUIT:  # GUI is closed
            running = False  # end programm
    keys = pygame.key.get_pressed()  # read which keys are down
        
    if event.type == pygame.MOUSEBUTTONDOWN:

        if (game_status_msg == "You lose!" and
                retry_rect.collidepoint(event.pos)):

            # reset game
            current_level = 0

            bricks_x = levels[0]["bricks_x"].copy()
            bricks_y = levels[0]["bricks_y"].copy()
            bricks_type = levels[0]["bricks_type"].copy()

            paddle_x = SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2

            ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
            ball_y = paddle_y - BALL_HEIGHT - 10

            ball_speed_x = 0
            ball_speed_y = 0

            brick_animations.clear()

            waiting = True
            start_time = pygame.time.get_ticks()

            game_status_msg = ""
            game_won = False
    
    if waiting: 
         seconds_left = max(
             0,
             3 - (pygame.time.get_ticks() - start_time) // 1000
         )
         ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
         ball_y = paddle_y - BALL_HEIGHT - 10

         current_time = pygame.time.get_ticks()

         if current_time - start_time > 3000:
            ball_speed_x = 7
            ball_speed_y = -7
            waiting = False

    
       
    # move everything

    # move ball
    ball_x = ball_x + ball_speed_x
    ball_y = ball_y + ball_speed_y

    # move paddle
    if keys[pygame.K_d]:
        paddle_x = paddle_x + paddle_speed_x
    if keys[pygame.K_a]:
        paddle_x = paddle_x - paddle_speed_x

    # bounce ball against edges of screen
    if ball_x < 0:  # left edge
        ball_speed_x = abs(ball_speed_x)  # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH:  # right edge
        ball_speed_x = abs(ball_speed_x) * -1  # negative x-speed = move left
    if ball_y < 0:
        ball_speed_y = abs(ball_speed_y)
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
        ball_speed_y = abs(ball_speed_y) * -1

    # stop paddle against edges of screen
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
    if paddle_x < 0:
        paddle_x = 0

#
# handle collisions
#

    # ball under paddle, elimination
    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
        ball_speed_x = 0
        ball_speed_y = 0
        # If dead
        game_status_msg = "You lose!"
      
    #if all bricks are destroyed, win!
    if len(bricks_x) == 0 and not game_won:

      if current_level == len(levels) - 1:
          ball_speed_x = 0
          ball_speed_y = 0
          game_status_msg = "You won!"
          game_won = True

      else:
          current_level += 1

          bricks_x = levels[current_level]["bricks_x"].copy()
          bricks_y = levels[current_level]["bricks_y"].copy()
          bricks_type = levels[current_level]["bricks_type"].copy()

          ball_x = paddle_x + PADDLE_WIDTH / 2 - BALL_WIDTH / 2
          ball_y = paddle_y - BALL_HEIGHT - 10

          ball_speed_x = 0
          ball_speed_y = 0

          waiting = True
          start_time = pygame.time.get_ticks()

          game_status_msg = ""

    # ball collision with bricks
    for i in range(0, len(bricks_x)):
        if (ball_x + BALL_WIDTH > bricks_x[i] and
            ball_x < bricks_x[i] + BRICK_WIDTH and
            ball_y + BALL_HEIGHT > bricks_y[i] and
                ball_y < bricks_y[i] + BRICK_HEIGHT):
            print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
            if (ball_speed_y > 0 and
                    ball_x > bricks_x[i]):
                ball_speed_y = abs(ball_speed_y) * -1
            elif (ball_speed_y < 0 and
                ball_x + BALL_HEIGHT > bricks_x[i] + BRICK_HEIGHT):
                ball_speed_y = abs(ball_speed_y) * 1
            elif (ball_speed_x > 0 and
                ball_x + BALL_WIDTH > bricks_x[i]):
                ball_speed_x = abs(ball_speed_x) * -1
            elif (ball_speed_x < 0 and
                ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH):
                ball_speed_x = abs(ball_speed_x) * 1
            brick_animations.append({
                "x": bricks_x[i],
                "y": bricks_y[i],
                "speed" : 8,
                "alpha": 255,
                "type": bricks_type[i],
            })
            bricks_x.pop(i)
            bricks_y.pop(i)
            bricks_type.pop(i)
            break
    for anim in brick_animations:
            anim["y"] -= anim["speed"]
            anim["alpha"] -= 10
    brick_animations = [
        anim for anim in brick_animations
        if anim["alpha"] > 0
        if anim["y"] > -BRICK_HEIGHT
    ]
    

    # ball collision with paddle
    if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
            ball_y < paddle_y + PADDLE_HEIGHT):
        ball_speed_y = abs(ball_speed_y) * -1
        offset = (ball_x + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)
        ball_speed_x = offset / 8

        if ball_speed_x > 7.2:
            ball_speed_x = 7.2
        if ball_speed_y > 7.2:
            ball_speed_y = 7.2
#
# draw everything
#

    # clear screen
    screen.blit(backgroundlevel1_img, (0, 0))

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y))

    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y))

    # draw brick
    for i in range(len(bricks_x)):
        if bricks_type[i] == "dark":
            screen.blit(
                brick_darkblue_img,
                (bricks_x[i], bricks_y[i])
            )

        else:
            screen.blit(
                brick_lightblue_img,
                (bricks_x[i], bricks_y[i])
            )
 
    for anim in brick_animations:
        if anim["type"] == "dark":
            img = brick_darkblue_img.copy()
        else:
            img = brick_lightblue_img.copy()

        img.set_alpha(anim["alpha"])
        screen.blit(img, (anim["x"], anim["y"]))

    #countdown image
    if waiting:
        countdown_img = font.render(
            str(seconds_left),
            True, 
            "black"
        )

        countdown_rect = countdown_img.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        screen.blit(countdown_img, countdown_rect)
    
    #retry image
    if game_status_msg == "You lose!":
            pygame.draw.rect(screen, "orange", retry_rect)
            retry_text = font.render("RETRY", True, "white")
            retry_text_rect = retry_text.get_rect(center=retry_rect.center)
            screen.blit(retry_text, retry_text_rect)
    #level image
    level_img = font.render(
        "Level " + str(current_level + 1),
        True,
        "white"
    )
    screen.blit(level_img, (0, 40))

    # Draw game status message
    game_status_img = font.render(game_status_msg, True, 'green')
    status_rect = game_status_img.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )
    screen.blit(game_status_img, status_rect)
    # show screen
    pygame.display.flip()

    # wait until next frame
    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')
