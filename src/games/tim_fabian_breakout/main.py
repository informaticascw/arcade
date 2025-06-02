#
# BREAKOUT GAME 
#

import pygame, time
from random import randint
from math import ceil


# Background music
menu_music = "./menu_music.mp3"
gameplay_music = "./gameplay_music.mp3"
game_over_music = "./game_over_music.mp3"

def play_menu_music():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)  # Loop oneindig
    pygame.mixer.music.set_volume(0.5)  # Volume aanpassen

def play_gameplay_music():
    pygame.mixer.music.load(gameplay_music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

#
# definitions 
#

def drawButtons(buttons: list, selected: int, columns: int = 1):
   buttonsPercolumn = ceil(len(buttons) / columns) # the amount of buttons needed per column

   for column in range(0,columns):

      column_buttons = buttons[(buttonsPercolumn * column):(buttonsPercolumn * (column + 1))]

      for button in column_buttons:
         if buttons.index(button) == selected: # makes it so the selected button is drawn in orange and the others in blue
            temp_img = orange_button_img.copy()
         else:
            temp_img = blue_button_img.copy()

         button_img_text = (font.render(button, True, 'white')) # makes the button text into an img
         temp_img.blit(button_img_text, ((temp_img.get_width() - button_img_text.get_width()) // 2, (temp_img.get_height() - button_img_text.get_height()) // 2)) # draws the text img onto the middle of the 'temp_img'

         screen.blit(temp_img, ((((SCREEN_WIDTH - (columns * BUTTON_WIDTH)) // (columns + 1)) * (column + 1)) + (BUTTON_WIDTH * column), ((SCREEN_HEIGHT - (buttonsPercolumn * BUTTON_HEIGHT)) // (buttonsPercolumn + 1) * (column_buttons.index(button) + 1)) + (BUTTON_HEIGHT * column_buttons.index(button))))

def draw_hearts():           # draws the heart images
    for i in range(0,lives): # for every live you have
        screen.blit(heart_img, (SCREEN_WIDTH - (42 + (i * 35)), 10)) # draw on the right side of the screen, every next 35px left of it

def initialiseBreakoutgameVariables(level): # resets all the variables
   global ball_x, ball_speed_x, ball_y, ball_speed_y, paddle_steer, paddle_x, paddle_y, bricks_animations, lives, button_cooldown_timer, paddle_width, paddle_img, powerups, powerup_timer, paddle_speed
   
   ball_x = (SCREEN_WIDTH - BALL_WIDTH) // 2 # starting x position of ball 
   ball_y = 300     # starting y position of ball
   ball_speed_x = 0 # speed of ball in x direction
   ball_speed_y = int((level ** 0.5) * 6) # speed of ball in y direction
   
   paddle_steer = 12                             # how much you can steer the ball with your paddle
   paddle_x = (SCREEN_WIDTH - paddle_width) // 2 # places ball x in middle of screen
   paddle_y = SCREEN_HEIGHT - 64                 # places ball y 64 pixels above bottom of screen
   
   paddle_speed = 10 # starting speed of the paddle

   bricks_animations = []

   powerups = []
   powerup_timer = 0
   paddle_width = PADDLE_MEDIUM_WIDTH  # Reset to original width
   paddle_img = paddle_medium_img


   if level == 1:
      lives = 3 # resets lives if you start level 1
      button_cooldown_timer = 0 # timer reset because we now are in breakout

def makeBricks(level):
   global bricks # global var so it will update over the whole code
   bricks = []   # list of all bricks, every bricks item is ordered: [x position, y position, bricks_lives, brick_color]
   color_options = ['blue', 'orange', 'green', 'red', 'yellow', 'purple']


   if type(level["shape"]) == dict: # if the level is given as an dict, this will convert it to a usable list
      new_shape = []
      
      for i in range(0, level["shape"]["rows"]):
         new_shape.append([])
         for j in range(0, level["shape"]["columns"]):
            new_shape[i].append(1)
      
      level["shape"] = new_shape
   
   elif type(level["shape"]) != list: # debug
      raise TypeError('expected list or dict, but got: ' + type(level["shape"]))
   
   rows = len(level["shape"])
   columns = len(level["shape"][0])
   
   
   indentation_bricks = (SCREEN_WIDTH - (columns * BRICK_WIDTH)) // 2 # centers the bricks horizontaly
   if indentation_bricks < 0: # if there are too many bricks to fit on the screen (debug)
      raise ValueError('Too many columns of bricks') # shows error message
   
   # makes the list with bricks, every time: x + 96 and each row: y + 32
   for i in range(0,rows):       # for every row
      for j in range(0,columns): # every column in that row
         if level["shape"][i][j] == 1:  # if there is no brick at that position, skip it
            brick = {}                                  # resets the list of the brick
            brick["x_position"] = ((j * 96) + indentation_bricks) # adds the x position of the brick
            brick["y_position"] = ((i * 32) + 64)                 # adds the y position of the brick
            brick["lives"] = (level["brick_lives"])               # adds the lives of that brick
            brick["color"] = (color_options[randint(0, len(color_options)-1)])
            bricks.append(brick)                        # adds that brick to the list of all bricks

def setBreakout(level: int): # resets the breakoutgame by restoring the bricks and the variables
   level_dict = eval('level_' + str(level))
   initialiseBreakoutgameVariables(level) # resets all the variables
   makeBricks(level_dict)

def update_paddle_speed():
    global paddle_speed
    # calculates the speed of the bal at that moment
    ball_speed = (ball_speed_x**2 + ball_speed_y**2)**0.5
    # increases the paddlespeed based on the ballspeed but with a maximum of 20
    paddle_speed = min(10 + ball_speed / 3, MAX_PADDLE_SPEED)

def limit_ball_speed(speed_x, speed_y, max_speed):
    current_speed = (speed_x**2 + speed_y**2)**0.5
    if current_speed > max_speed:
        scale_factor = max_speed / current_speed
        return speed_x * scale_factor, speed_y * scale_factor
    return speed_x, speed_y



# constant values
FPS = 30                     # frames Per Second
SCREEN_WIDTH = 1280          # screen width in pixels
SCREEN_HEIGHT = 720          # screen height in pixels
BALL_WIDTH = 16              # width of ball in pixels
BALL_HEIGHT = 16             # height of ball in pixels
PADDLE_MEDIUM_WIDTH = 144    # width of paddle in pixels
PADDLE_SMALL_WIDTH = 72      # width of small paddle
PADDLE_LARGE_WIDTH = 216     # width of large paddle
PADDLE_HEIGHT = 32           # height of paddle in pixels
BRICK_WIDTH = 96             # width of brick in pixels
BRICK_HEIGHT = 32            # height of brick in pixels
BUTTON_WIDTH = 300           # width of button in pixels
BUTTON_HEIGHT = 100          # height of button in pixels
BRICK_EXPLOSION_WIDTH = 80  # width of explosion in pixels
BRICK_EXPLOSION_HEIGHT = 77 # height of explosion in pixels
LAST_LEVEL = 5           # the number of the last level
STAR_WIDTH = 32              # width of star in pixels
STAR_HEIGHT = 32             # height of star in pixels
POWERUP_DURATION = 300       # duration of powerup effect in frames (10 seconds at 30 FPS)
MUSIC_VOLUME = 0.5           # the volume of all music
MAX_PADDLE_SPEED = 20        # maximum speed of the paddle
MAX_BALL_SPEED = 15



# global variables
# breakout game variables are set when you start the game

level = 1 # the current level

level_1 = { "shape": [
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    ],  "brick_lives": 1} # how the bricks should be made in level 1

level_2 = {"shape": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],  "brick_lives": 2} # how the bricks should be made in level 2

level_3 = {"shape": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    ], "brick_lives": 2} # how the bricks should be made in level 3

level_4 = { "shape": [
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],

], "brick_lives": 2}

level_5 = { "shape": [
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
], "brick_lives": 2}


game_status = 0 # 0 = homescreen, 1 = breakoutgame, 2 = infoscreen, 3 = stopping python, 4 = game over

selected_button = 0        # index of which button is selected
button_cooldown_timer = 0  # the timer for the cooldown on hitting a button
button_cooldown_ticks = 10 # the reset value for the timer

homescreen_buttons = ['start', 'info', 'quit'] # all the buttons on the homescreen

informationtext = [
    "This Breakout game is made with Python and Pygame.",
    "The player moves the paddle left and right using the A and D keys",
    "to keep the ball in play and break all the bricks.",
    "The ball bounces off walls, the paddle, and bricks,",
    "with its direction changing based on where it hits.",
    "When the ball hits a brick, the brick disappears and the ball's speed changes slightly.",
    "Collision with the paddle lets the player influence the ball's angle.",
    "The game focuses on core mechanics like movement, collision, and brick removal."
]

game_over_screen_buttons = ['play again', 'homescreen', 'quit']

paddle_width = PADDLE_MEDIUM_WIDTH  # store original paddle width

#
# init game
#
print("test for music: " + str(pygame.mixer.get_sdl_mixer_version())) # music
pygame.mixer.pre_init() # music test
pygame.init()
try:
   pygame.mixer.init() # music
except:
   print("music could not be initialised")
   musicIsInitialised = False
else:
   # music
   # Sound effects
   musicIsInitialised = True
   bounce_sound = pygame.mixer.Sound("./Bounce.mp3")  # Bal die tegen paddle of bricks botst
   powerup_sound = pygame.mixer.Sound("./Power.mp3")  # Power-up opgepakt
   level_complete_sound = pygame.mixer.Sound("./Win.mp3")  # Level voltooid
   game_over_sound = pygame.mixer.Sound("./Lose.mp3")  # Game over

font = pygame.font.SysFont('default', 64)                                                          # creates the font for the game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) # makes sure the width and heigth of the screen are set to preference and scales them the max while keeping them in the same ratio
fps_clock = pygame.time.Clock()                                                                    # makes an object to keep track of the time



#
# read images
#

background = pygame.image.load("Background2.png") # loads background image and names it 'background'
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) # scales the image of the background to the desired height and width

# brick_explode.png is from https://opengameart.org/content/arkanoid-assets
brick_explosions = pygame.image.load("brick_explode.png").convert_alpha()
brick_explosions = pygame.transform.scale(brick_explosions, (320, 231))

brick_explosion_1 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_1.blit(brick_explosions, (0, 0), (0, 0, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_2 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_2.blit(brick_explosions, (0, 0), (80, 0, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_3 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_3.blit(brick_explosions, (0, 0), (160, 0, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_4 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_4.blit(brick_explosions, (0, 0), (240, 0, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_5 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_5.blit(brick_explosions, (0, 0), (0, 77, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_6 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_6.blit(brick_explosions, (0, 0), (80, 77, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_7 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_7.blit(brick_explosions, (0, 0), (160, 77, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_8 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_8.blit(brick_explosions, (0, 0), (240, 77, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_9 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_9.blit(brick_explosions, (0, 0), (0, 154, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_10 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_10.blit(brick_explosions, (0, 0), (80, 154, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_11 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_11.blit(brick_explosions, (0, 0), (160, 154, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))

brick_explosion_12 = pygame.Surface((80, 77), pygame.SRCALPHA)
brick_explosion_12.blit(brick_explosions, (0, 0), (240, 154, BRICK_EXPLOSION_WIDTH, BRICK_EXPLOSION_HEIGHT))



explosion_images = { # a dictionary with all the images
    0: brick_explosion_1,
    1: brick_explosion_2,
    2: brick_explosion_3,
    3: brick_explosion_4,
    4: brick_explosion_5,
    5: brick_explosion_6,
    6: brick_explosion_7,
    7: brick_explosion_8,
    8: brick_explosion_9,
    9: brick_explosion_10,
    10: brick_explosion_11,
    11: brick_explosion_12,
}

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha() # converts the image using alpha conversion in to rgba and calls it spritesheet

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)                   # sets 'ball_img' to aan img with dimentions 64x64 and 'SRCALPHA' to have individual pixel transparency
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))                # picks the ball image fron the spritesheet
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) # scales the image of the ball to the desired height and width

paddle_medium_img = pygame.Surface((243, 64), pygame.SRCALPHA)                        # sets 'paddle_img' to aan img with dimentions 243x64 and 'SRCALPHA' to have individual pixel transparency
paddle_medium_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))                     # picks the paddle image fron the spritesheet
paddle_medium_img = pygame.transform.scale(paddle_medium_img, (PADDLE_MEDIUM_WIDTH, PADDLE_HEIGHT)) # scales the image of the paddle to the desired height and width

paddle_small_img = pygame.Surface((115, 64), pygame.SRCALPHA)                        
paddle_small_img.blit(spritesheet, (0, 0), (1574, 912, 115, 64)) 
paddle_small_img = pygame.transform.scale(paddle_small_img, (PADDLE_SMALL_WIDTH, PADDLE_HEIGHT))

paddle_large_img = pygame.Surface((347, 64), pygame.SRCALPHA)                        
paddle_large_img.blit(spritesheet, (0, 0), (0, 910, 347, 64))  
paddle_large_img = pygame.transform.scale(paddle_large_img, (PADDLE_LARGE_WIDTH, PADDLE_HEIGHT))

blue_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'blue_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
blue_brick_img.blit(spritesheet, (0, 0), (772, 390, 386, 130))                       # picks the brick image fron the spritesheet
blue_brick_img = pygame.transform.scale(blue_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

damaged_blue_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'damaged_blue_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
damaged_blue_brick_img.blit(spritesheet, (0, 0), (0, 0, 386, 130))                       # picks the brick image fron the spritesheet
damaged_blue_brick_img = pygame.transform.scale(damaged_blue_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

orange_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'orange_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
orange_brick_img.blit(spritesheet, (0, 0), (772, 0, 386, 130))                       # picks the brick image fron the spritesheet
orange_brick_img = pygame.transform.scale(orange_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

damaged_orange_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'damaged_orange_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
damaged_orange_brick_img.blit(spritesheet, (0, 0), (772, 650, 386, 130))                       # picks the brick image fron the spritesheet
damaged_orange_brick_img = pygame.transform.scale(damaged_orange_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

green_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'green_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
green_brick_img.blit(spritesheet, (0, 0), (386, 130, 386, 130))                       # picks the brick image fron the spritesheet
green_brick_img = pygame.transform.scale(green_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

damaged_green_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'damaged_green_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
damaged_green_brick_img.blit(spritesheet, (0, 0), (386, 0, 386, 130))                       # picks the brick image fron the spritesheet
damaged_green_brick_img = pygame.transform.scale(damaged_green_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

yellow_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'yellow_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
yellow_brick_img.blit(spritesheet, (0, 0), (386, 390, 386, 130))                       # picks the brick image fron the spritesheet
yellow_brick_img = pygame.transform.scale(yellow_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

damaged_yellow_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'damaged_yellow_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
damaged_yellow_brick_img.blit(spritesheet, (0, 0), (386, 260, 386, 130))                       # picks the brick image fron the spritesheet
damaged_yellow_brick_img = pygame.transform.scale(damaged_yellow_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

red_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'red_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
red_brick_img.blit(spritesheet, (0, 0), (772, 260, 386, 130))                       # picks the brick image fron the spritesheet
red_brick_img = pygame.transform.scale(red_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

damaged_red_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'damaged_red_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
damaged_red_brick_img.blit(spritesheet, (0, 0), (772, 130, 386, 130))                       # picks the brick image fron the spritesheet
damaged_red_brick_img = pygame.transform.scale(damaged_red_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

purple_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'purple_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
purple_brick_img.blit(spritesheet, (0, 0), (0, 390, 386, 130))                       # picks the brick image fron the spritesheet
purple_brick_img = pygame.transform.scale(purple_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

damaged_purple_brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)                         # sets 'damaged_purple_brick_img' to aan img with dimentions 386x130 and 'SRCALPHA' to have individual pixel transparency
damaged_purple_brick_img.blit(spritesheet, (0, 0), (0, 520, 386, 130))                       # picks the brick image fron the spritesheet
damaged_purple_brick_img = pygame.transform.scale(damaged_purple_brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) # scales the image of the brick to the desired height and width

bad_star_img = pygame.Surface((64, 61), pygame.SRCALPHA)
bad_star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))  # adjust coordinates to your star image
bad_star_img = pygame.transform.scale(bad_star_img, (STAR_WIDTH, STAR_HEIGHT))

good_star_img = pygame.Surface((64, 61), pygame.SRCALPHA)
good_star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))  # adjust coordinates to your star image
good_star_img = pygame.transform.scale(good_star_img, (STAR_WIDTH, STAR_HEIGHT))

brick_images = {"normal": {
   "blue": blue_brick_img,
   "orange": orange_brick_img,
   "green": green_brick_img,
   "yellow": yellow_brick_img,
   "red": red_brick_img,
   "purple": purple_brick_img},
   
   "damaged": {
   "blue": damaged_blue_brick_img,
   "orange": damaged_orange_brick_img,
   "green": damaged_green_brick_img,
   "yellow": damaged_yellow_brick_img,
   "red": damaged_red_brick_img,
   "purple": damaged_purple_brick_img
   }}

blue_button_img = pygame.Surface((96, 32), pygame.SRCALPHA) # makes a new button surface
blue_button_img.blit(blue_brick_img, (0,0))                 # puts the blue_brick_img onto the new surface
blue_button_img = pygame.transform.scale(blue_button_img, (BUTTON_WIDTH, BUTTON_HEIGHT)) # transforms the img to the desired widht and height

orange_button_img = pygame.Surface((96, 32), pygame.SRCALPHA) # makes a new button surface
orange_button_img.blit(orange_brick_img, (0,0))               # puts the orange_brick_img onto the new surface
orange_button_img = pygame.transform.scale(orange_button_img, (BUTTON_WIDTH, BUTTON_HEIGHT)) # transforms the img to the desired widht and height

heart_img = pygame.Surface((64, 58), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0, 0), (1637, 652, 64, 58))  # picks the hearth from the spitesheet
heart_img = pygame.transform.scale(heart_img, (32, 28))  # Maak het hartje kleiner

#
# game loop
#

print('mygame is running') # This prints the sentence: "mygame is running" to the terminal (debug info)
running = True

while running: # This creates a loop which keeps getting repeated until the game is over
   #
   # begin of tick things
   #

   # clear screen by drawing the background
   screen.blit(background, (0, 0))  # draws screen with the background
   # the background is drawn here because it needs to be drawn before everything else is drawn, but needs to be drawn regardless of the game status
   
   #
   # read events
   # 
   for event in pygame.event.get(): # Looks at what the player is doing
      if event.type == pygame.QUIT: # sets 'running' so game will end if event 'quit' is in 'events'
         running = False            # Stop the game (if the button was pressed)
   keys = pygame.key.get_pressed()  # keys is set to a sequence of boolean values of all the keys pressed
  
   #
   # homescreen
   #

   if game_status == 0: # homescreen
      
      # draw all the homescreen buttons
      #

      drawButtons(homescreen_buttons, selected_button) # draws the buttons on the homescreen
      if musicIsInitialised: # only execute is music is working
         play_menu_music()
      
      game_status_msg = "Move with WASD and confirm with Q" # info for the player

      # get the player inputs
      #
      if button_cooldown_timer == 0: # if there is no cooldown at the moment
         button_cooldown_timer = button_cooldown_ticks # cooldown of when the game wont register any key presses from user in ticks
         
         if keys[pygame.K_q] : # key q is down
            game_status = selected_button + 1 # this sets the game status number to the good number because of how the gamestatus numbers are defined
            if game_status == 1: # if breakout is selected
               level = 1
               setBreakout(level)   # resets the breakout game to level 1

         elif keys[pygame.K_w] : # key w is down
            selected_button -= 1                             # moves the selected button number 1 down; selected button goes up visualy
            if selected_button < 0:                          # if the selected button number underflows
               selected_button = len(homescreen_buttons) - 1 # change the selected button number to the highest

         elif keys[pygame.K_s] : # key s is down
            selected_button += 1                           # moves the selected button number 1 up; selected button goes down visualy
            if selected_button == len(homescreen_buttons): # if the selected button number overflows
               selected_button = 0                         # change the selected button number to the lowest
         else:
            button_cooldown_timer = 0 # no keys were hit so the cooldown is set to 0
      
      else:
         button_cooldown_timer -= 1 # decrease cooldown by 1
   

   #
   # breakout game
   #

   elif game_status == 1: # breakout game
      
      game_status_msg = "Speel met [A] en [D]" # tell the player what they should do
      if musicIsInitialised: # only execute is music is working
         play_gameplay_music()
      # 
      # move everything
      #
  
      # player inputs
      update_paddle_speed() # updates the paddlespeed based on the ballspeed
      
      if keys[pygame.K_d] :      # key d is down
        paddle_x = paddle_x + paddle_speed # moves the paddle to the right
      
      if keys[pygame.K_a] :      # key a is down
        paddle_x = paddle_x - paddle_speed # moves the paddle to the left

      # the cooldown is only needed for the 1 button
      if button_cooldown_timer == 0: # if there is no cooldown at the moment
         # press 1 to skip the level
         if keys[pygame.K_1] : # keys 1 is down
            print("player skipped level") # debug
            bricks = [] # makes bricks empty so the level is beaten
            button_cooldown_timer = button_cooldown_ticks # cooldown of when the game wont register any key presses from user in ticks
      else:
         button_cooldown_timer -= 1 # decrease cooldown by 1
  
      # move ball
      ball_x = ball_x + ball_speed_x # this moves the bal with the ballspeed from the old x of the bal to the new x
      ball_y = ball_y + ball_speed_y # this moves the bal with the ballspeed from the old y of the bal to the new y
  
      
      # bounces ball
  
        # bounces ball if it reaches the side of the screen
      if ball_x < 0 :
        ball_speed_x = abs(ball_speed_x) 
        ball_speed_x, ball_speed_y = limit_ball_speed(ball_speed_x, ball_speed_y, MAX_BALL_SPEED) # makes sure that the ballspeed wont exeed the speedlimit
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 
        ball_speed_x, ball_speed_y = limit_ball_speed(ball_speed_x, ball_speed_y, MAX_BALL_SPEED) # makes sure that the ballspeed wont exeed the speedlimit
  
        # bounces ball if it reaches the top of the screen
      if ball_y < 0: 
         ball_speed_y = abs(ball_speed_y)
         ball_speed_x, ball_speed_y = limit_ball_speed(ball_speed_x, ball_speed_y, MAX_BALL_SPEED) # makes sure that the ballspeed wont exeed the speedlimit
  
      
  
  
        
      # 
      # handle collisions
      #
  
      # paddle-wall colisions
      if paddle_x + paddle_width > SCREEN_WIDTH: # if paddle goes of the screen on the right side
         paddle_x = SCREEN_WIDTH - paddle_width  # paddle is set to the rightmost x position
         if musicIsInitialised: # only execute is music is working
            bounce_sound.play()
     
      if paddle_x < 0: # if paddle goes of the screen on the left side
         paddle_x = 0  # paddle is set to the leftmost x position
         if musicIsInitialised: # only execute is music is working
            bounce_sound.play()
  
  
      # ball-paddle colision
      # top of paddle
      if (ball_x + BALL_WIDTH > paddle_x and  # if the ball is right of paddle's left side
         ball_x < paddle_x + paddle_width and # and if the ball is left of paddle's right side
         ball_y + BALL_HEIGHT > paddle_y and  # and if the ball's bottom is under paddle's top
         ball_y < paddle_y) :                 # and if the ball's top is above paddle's top
        
         ball_speed_y = abs(ball_speed_y) * -1 # bounches ball by negating y speed
         print('ball hit paddle ' + str((ball_x + (BALL_WIDTH / 2)) - (paddle_x + (paddle_width / 2))) + 'px of the middle of the paddle') # debug info
         ball_speed_x = (ball_speed_x + ((((ball_x + (BALL_WIDTH / 2)) - (paddle_x + (paddle_width / 2))) / (paddle_width / 2)) * paddle_steer)) /2              # where the ball hits the paddle becomes a number between 0 and 1 which is multiplied by the 'paddle steer' variable
         ball_speed_x, ball_speed_y = limit_ball_speed(ball_speed_x, ball_speed_y, MAX_BALL_SPEED) # makes sure that the ballspeed wont exeed the speedlimit
         if musicIsInitialised: # only execute is music is working
            bounce_sound.play()
  
      # side of paddle
      elif (ball_y + BALL_HEIGHT > paddle_y and ball_y < paddle_y + PADDLE_HEIGHT                           # if ball is between paddle's top and bottom
            and ((ball_x + BALL_WIDTH > paddle_x and ball_x < paddle_x)                                     # checks if ball is on left side of paddle
                 or (ball_x + BALL_WIDTH > paddle_x + paddle_width and ball_x < paddle_x + paddle_width))): # checks if ball is on right side of paddle
  
         ball_speed_x = ball_speed_x * -1 # bounches ball by negating x speed
         if musicIsInitialised: # only execute is music is working
            bounce_sound.play()
  
  
      # ball-brick collision
      for i in range(0, len(bricks)) :
         if (ball_x + BALL_WIDTH > bricks[i]["x_position"] and # if the ball is right of brick's left side
          ball_x < bricks[i]["x_position"] + BRICK_WIDTH and    # and if the ball is left of brick's right side
          ball_y + BALL_HEIGHT > bricks[i]["y_position"] and    # and if the ball is under brick's top
          ball_y < bricks[i]["y_position"] + BRICK_HEIGHT):     # and if the ball is above brick's bottom
  
            print("brick touched at ball_x = " + str(ball_x) + " and ball_y = " + str(ball_y)) # prints where the ball hit the brick to the terminal
    
            # bounce ball
            if ball_speed_y > 0 and ball_y < bricks[i]["y_position"]:                                # if "ball goes down" and "ball's top is above brick's top"
               ball_speed_y *= -1                                                        # bounces ball by negating y speed
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks[i]["y_position"] + BRICK_HEIGHT: # if "ball goes up" and "bottom of ball is below bottom of brick"
               ball_speed_y *= -1                                                        # bounches ball by negating y speed
            elif ball_speed_x > 0 and ball_x < bricks[i]["x_position"]:                              # if "ball goes right" and "ball's left is left of brick's left side"
               ball_speed_x *= -1                                                        # bounches ball by negating x speed
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks[i]["x_position"] + BRICK_WIDTH:   # if "ball goes left" and "ball's right is right of brick's right side"
               ball_speed_x *= -1                                                        # bounches ball by negating x speed
            if musicIsInitialised: # only execute is music is working
               bounce_sound.play()
           
            bricks_animations.append(bricks[i].copy()) # adds the brick that is hit to the list of bricks that are animated
            # .copy() is used here so we dont get an error when drawing the animations, if the same block is hit twice too fast, a bad refrence (or something refrence related) whould give it an error
            bricks_animations[-1]["frame"] = 0  # adds zero because that is the frame of the current animation
            bricks[i]["lives"] -= 1 # removes 1 life from that block
            if bricks[i]["lives"] == 0: # if the block is destroyed
               if bricks[i]["color"] == "red":
                  powerups.append({
                     "x_position": bricks[i]["x_position"] + BRICK_WIDTH//2 - STAR_WIDTH//2,
                     "y_position": bricks[i]["y_position"],
                     "type": "small",
                     "frame": 0
                  })
               elif bricks[i]["color"] == "blue":
                  powerups.append({
                     "x_position": bricks[i]["x_position"] + BRICK_WIDTH//2 - STAR_WIDTH//2,
                     "y_position": bricks[i]["y_position"],
                     "type": "large",
                     "frame": 0
                   })
               bricks.pop(i) # removes the block from list of all bricks
            ball_speed_x *= randint(95,110)/100 # increases or decreases ballspeed a random amount in x direction
            ball_speed_y *= randint(95,110)/100 # increases or decreases ballspeed a random amount in y direction
            ball_speed_x, ball_speed_y = limit_ball_speed(ball_speed_x, ball_speed_y, MAX_BALL_SPEED) # makes sure that the ballspeed wont exeed the speedlimit
            break # stops the loop so we don't get errors
            
      # Move and draw powerups
      for powerup in powerups[:]:
         powerup["y_position"] += 3  # Move powerup downward
    
         # Draw powerup
         if powerup["type"] == "small":
            screen.blit(bad_star_img, (powerup["x_position"], powerup["y_position"]))
         else:
            screen.blit(good_star_img, (powerup["x_position"], powerup["y_position"]))
    
         # Check collision with paddle
         if (powerup["x_position"] + STAR_WIDTH > paddle_x and
            powerup["x_position"] < paddle_x + paddle_width and
            powerup["y_position"] + STAR_HEIGHT > paddle_y and
            powerup["y_position"] < paddle_y + PADDLE_HEIGHT):
            
            paddle_center = paddle_x + paddle_width //2
            
            if musicIsInitialised: # only execute is music is working
               powerup_sound.play()
            
            if powerup["type"] == "small":
               paddle_width = PADDLE_SMALL_WIDTH
               paddle_img = paddle_small_img
            else:
               paddle_width = PADDLE_LARGE_WIDTH
               paddle_img = paddle_large_img
            
            # Keep paddle centered
            paddle_x = paddle_center - paddle_width // 2
    
            powerup_timer = POWERUP_DURATION
            powerups.remove(powerup)
            continue  # Skip the rest of the loop for this powerup
        
         # Remove if off screen
         if powerup["y_position"] > SCREEN_HEIGHT:
            powerups.remove(powerup)

      # Handle powerup timer
      if powerup_timer > 0:
            powerup_timer -= 1
      if powerup_timer == 0:
         # Reset paddle to original size
         powerup_timer = -1 # powerup_timer is set to -1 so we dont execute the folowing code more than 1 time
         paddle_width = PADDLE_MEDIUM_WIDTH
         paddle_img = paddle_medium_img

      # checks if game is over
      # winning
      if len(bricks) == 0: # when there are no bricks
         if level == LAST_LEVEL: # if you completed the last level
            ball_speed_x = 0 # set ballspeed to 0
            ball_speed_y = 0 # set ballspeed to 0
            game_status_msg = "You won the game!" # If you finished the last level set to winningscreen
            game_status = 4  # game over screen
            if musicIsInitialised: # only execute is music is working
               pygame.mixer.music.load(game_over_music)
               pygame.mixer.music.play(-1)  # -1 betekent loop oneindig
         else: # if you completed a level
            level += 1  # Go to next level
            setBreakout(level)
            game_status_msg = "Level " + str(level) + "!"
            if musicIsInitialised: # only execute is music is working
               level_complete_sound.play()

      # losing
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:  # checks if the ball hit the bottom of the screen
         lives -= 1
         if lives == 0: # if you have no lives left
            ball_speed_x = 0
            ball_speed_y = 0
            game_status_msg = "You lost!"
            game_status = 4  # game over screen
            if musicIsInitialised: # only execute is music is working
               pygame.mixer.music.load(game_over_music)
               pygame.mixer.music.play(-1)
         else: # if you have lives left
            ball_x = paddle_x + paddle_width // 2 - BALL_WIDTH // 2 # Resets bal and paddle position
            ball_y = paddle_y - BALL_HEIGHT
            ball_speed_x = 0
            ball_speed_y = -abs(ball_speed_y)
            ball_speed_x, ball_speed_y = limit_ball_speed(ball_speed_x, ball_speed_y, MAX_BALL_SPEED) # makes sure that the ballspeed wont exeed the speedlimit
      

      # 
      # draw everything
      #
  
      # draw level info
      level_img = font.render(f"Level: {level}", True, 'white')
      screen.blit(level_img, (10, 10))  # Teken in de linkerbovenhoek

      # draw ball and paddle
      screen.blit(ball_img, (ball_x, ball_y))       # draws the ball img at (x of ball, y of ball)
      screen.blit(paddle_img, (paddle_x, paddle_y)) # draws the paddle img at (x of paddle, y of paddle)
      
      # draw bricks
      for i in range(0, len(bricks)) : # draws the bricks for every bricks in the bricks_x list
         if bricks[i]["lives"] == 1:         # if the bricks has only 1 life left
            screen.blit(brick_images["damaged"][bricks[i]["color"]], (bricks[i]["x_position"], bricks[i]["y_position"]))
         else:
            screen.blit(brick_images["normal"][bricks[i]["color"]], (bricks[i]["x_position"], bricks[i]["y_position"]))
      
      # draw animated bricks
      for i in range(len(bricks_animations)-1, -1, -1): # loops backwards (so we dont get index out of range errors) through every brick that need to be animated
         frame = bricks_animations[i]["frame"]
         screen.blit(explosion_images[frame], (bricks_animations[i]["x_position"] + (BRICK_WIDTH - BRICK_EXPLOSION_WIDTH) // 2, bricks_animations[i]["y_position"] + (BRICK_HEIGHT - BRICK_EXPLOSION_HEIGHT) // 2 + 5))

         bricks_animations[i]["frame"] += 1 # adds 1 frame
         if bricks_animations[i]["frame"] >= 12: # after 12 frames
            bricks_animations.pop(i)        # remove that animation
      
      # draw hearts
      draw_hearts()
   #
   # info screen
   #

   elif game_status == 2: # information screen
      # button for going back to the homesceen    
      
      temp_img = orange_button_img.copy()
      button_img_text = (font.render('Back', True, 'white')) # makes the button text into an img
      temp_img.blit(button_img_text, ((temp_img.get_width() - button_img_text.get_width()) // 2, (temp_img.get_height() - button_img_text.get_height()) // 2)) # draws the text img onto the middle of the 'temp_img'
      screen.blit(temp_img, ((SCREEN_WIDTH - temp_img.get_width()) // 2, (SCREEN_HEIGHT - temp_img.get_height()) - 50)) # places the button in the middlebottom of the screen

      font = pygame.font.SysFont('default', 32)

      game_status_msg = '' # no info message needed because this is already the info page
      # Draw each line at a different height
      textheight = 50  # starting Y position
      for line in informationtext:
         game_status_img = font.render(line, True, 'green')
         screen.blit(game_status_img, (50, textheight))
         textheight += 30  # move down for the next line

      if button_cooldown_timer == 0: # if there is no cooldown at the moment
         if keys[pygame.K_q] : # key q is down
            game_status = 0          # goes back to the homesceen
            button_cooldown_timer = button_cooldown_ticks # cooldown gets set to 10 so the player doesn't hit a button twice
      else:
         button_cooldown_timer -= 1
      font = pygame.font.SysFont('default', 64)    
   #
   # quit python
   #   
   elif game_status == 3:             # end python
      print('mygame was ended by player') # debug info; player hit a quit button
      quit()                          # ends the python script
   
   #
   # game over
   #

   elif game_status == 4: # game over screen
      
      drawButtons(game_over_screen_buttons, selected_button)
      if musicIsInitialised: # only execute is music is working
         pygame.mixer.music.load(game_over_music)
         pygame.mixer.music.play(-1)

      if button_cooldown_timer == 0: # if there is no cooldown at the moment
         button_cooldown_timer = button_cooldown_ticks # cooldown gets set to 10 so the player doesn't hit a button twice
         if keys[pygame.K_q] : # key q is down
            if selected_button == 0:
               game_status = 1 # play again / breakout game
               level = 1
               setBreakout(level) # resets the breakout game to level 1

            elif selected_button == 1:
               game_status = 0 # homescreen
               selected_button = 0 # resets the selected button
            elif selected_button == 2:
               game_status = 3 # end python
            
         elif keys[pygame.K_w] : # key w is down
            selected_button -= 1                                          # moves the selected button number 1 down; selected button goes up visualy
            if selected_button < 0:                                       # if the selected button number underflows
               selected_button = len(game_over_screen_buttons) - 1 # change the selected button number to the highest

         elif keys[pygame.K_s] : # key s is down
            selected_button += 1                                        # moves the selected button number 1 up; selected button goes down visualy
            if selected_button == len(game_over_screen_buttons): # if the selected button number overflows
               selected_button = 0                                      # change the selected button number to the lowest
         
         else:
            button_cooldown_timer = 0 # no keys were hit so the cooldown is set to 0
      
      else:
         button_cooldown_timer -= 1

   #
   # end of tick things
   #

   # these need to be executed no matter what the game status is   
   # show game msg
   game_status_img = font.render(game_status_msg, True, 'green')                        # makes the text the right font and color
   screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) // 2, 0)) # makes sure the text is placed in the middle by deviding the left over space by two so that the space is the same on both sides
   
   # show screen
   pygame.display.flip() # updates screen


   # 
   # wait until next frame
   #

   fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running') # if 'running' is 'False'
