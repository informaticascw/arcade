#
# BREAKOUT GAME 
#

import pygame
from random import randint
from math import ceil
from pathlib import Path # we use this to check the existence of highscore.txt

#
# definitions 
#

def drawButtons(buttons: list, selected: int, columns: int = 1, color: str = 'normal', color_from: int = 100): # color_from just needs to be very high
   rows = ceil(len(buttons) / columns)
   for row in range(0, rows):
      row_buttons = buttons[(columns * row):(columns * (row + 1))]

      for button in row_buttons:
         if buttons.index(button) >= color_from:
            temp_img = button_images[color].copy()
         else:
            if buttons.index(button) == selected: # makes it so the selected button is drawn in orange and the others in blue
               temp_img = orange_button_img.copy()
            else:
               temp_img = blue_button_img.copy()


         button_img_text = (font.render(button, True, 'white')) # makes the button text into an img
         temp_img.blit(button_img_text, ((temp_img.get_width() - button_img_text.get_width()) // 2, (temp_img.get_height() - button_img_text.get_height()) // 2)) # draws the text img onto the middle of the 'temp_img'

         screen.blit(temp_img, ((((SCREEN_WIDTH - (columns * BUTTON_WIDTH)) // (columns + 1)) * (row_buttons.index(button)+ 1)) + (BUTTON_WIDTH * row_buttons.index(button)), ((SCREEN_HEIGHT - (rows * BUTTON_HEIGHT)) // (rows + 1) * (row + 1)) + (BUTTON_HEIGHT * row)))

def draw_hearts():           # draws the heart images
    for i in range(0,lives): # for every live you have
        screen.blit(heart_img, (SCREEN_WIDTH - (42 + (i * 35)), 10)) # draw on the right side of the screen, every next 35px left of it

def initialiseBreakoutgameVariables(level: int, newlives: int = 3): # resets all the variables
   global balls, paddle_steer, paddle_x, paddle_y, bricks_animations, lives, button_cooldown_timer, paddle_width, paddle_img, powerups, powerup_timer, paddle_speed, reset_delay_timer, controls_reversed, powerup_message_timer, controls_message_timer, paddle2_x, paddle2_y, paddle2_width, paddle2_img, paddle2_speed, player1_score, player2_score, two_player_mode, singleplayer_score, score_multiplier, game_status
   paddle_width = PADDLE_MEDIUM_WIDTH  # Reset to original width
   paddle_img = paddle_medium_img
   paddle_steer = 12                             # how much you can steer the ball with your paddle
   paddle_x = (SCREEN_WIDTH - paddle_width) // 2 # places ball x in middle of screen
   paddle_y = SCREEN_HEIGHT - 64                 # places ball y 64 pixels above bottom of screen
   paddle_speed = 10 # starting speed of the paddle

     
   controls_reversed = False
   controls_message_timer = 180
   powerup_message_timer = 0
  
   # a list containing al the information about the balls
   balls = [{
      "x": (SCREEN_WIDTH - BALL_WIDTH) // 2,
      "y": paddle_y - BALL_HEIGHT,
      "speed_x": randint(-3, 3),
      "speed_y": int(-(level ** 0.5) * 6),
   }]
   if balls[0]["speed_x"] == 0:
      balls[0]["speed_x"] = 1
   balls[0]["speed_x"], balls[0]["speed_y"] = limit_ball_speed(balls[0]["speed_x"], balls[0]["speed_y"], MAX_BALL_SPEED)
   
   
   if two_player_mode:  # Two player mode
      paddle2_width = PADDLE_MEDIUM_WIDTH
      paddle2_img = paddle_medium_img
      paddle2_x = (SCREEN_WIDTH - paddle2_width) // 2
      paddle2_y = 64  # Positioned at top of screen
      paddle2_speed = 10
      # Spawn ball for player 2 (top)
      balls.append({
         "x": paddle2_x + (paddle2_width - BALL_WIDTH) // 2,
         "y": paddle2_y + PADDLE_HEIGHT,
         "speed_x": randint(-3, 3),
         "speed_y": 5,
         })
      if balls[1]["speed_x"] == 0:
         balls[1]["speed_x"] = 1
      balls[1]["speed_x"], balls[1]["speed_y"] = limit_ball_speed(balls[1]["speed_x"], balls[1]["speed_y"], MAX_BALL_SPEED)

   bricks_animations = []
   powerups = []
   powerup_timer = 0

   reset_delay_timer = 45  # timer to pause between lives and levels

   lives = newlives # resets lives, 3 is standard
   button_cooldown_timer = 0 # timer reset because we now are in breakout

   if level == 1: # only reset the score if we go to level 1
      player1_score = 0
      player2_score = 0
   
   score_multiplier = 1 # we reset the score multiplier every level so it doesn't get to big
   if level == 1 or game_status == 8:  # only reset if we are in level selection screen or on level 1, this is also reset when we go to two player so the game isn't confused that we have singleplayer_score in twoplayer
      singleplayer_score = 0

def makeBricks(level):
   global bricks, levels, two_player_mode # global var so it will update over the whole code
   if two_player_mode:
      level = levels["2p"][level-1]
   else:
      if level > 5:
            level = generate_random_level(level) 
      
      else:
         level = levels["1p"][level-1]
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
   
   
   x_indentation_bricks = (SCREEN_WIDTH - (columns * BRICK_WIDTH)) // 2 # centers the bricks horizontaly
   if x_indentation_bricks < 0: # if there are too many bricks to fit on the screen (debug)
      raise ValueError('Too many columns of bricks') # shows error message

   if two_player_mode:
      y_indentation_bricks = (SCREEN_HEIGHT - (rows * BRICK_HEIGHT)) // 2
   else:
      y_indentation_bricks = 64
   
   # makes the list with bricks, every time: x + 96 and each row: y + 32
   for i in range(0,rows):       # for every row
      for j in range(0,columns): # every column in that row
         if level["shape"][i][j] == 1:  # if there is no brick at that position, skip it
            brick = {}                                  # resets the list of the brick
            brick["x_position"] = ((j * 96) + x_indentation_bricks) # adds the x position of the brick
            brick["y_position"] = ((i * 32) + y_indentation_bricks)                 # adds the y position of the brick
            brick["lives"] = (level["brick_lives"])               # adds the lives of that brick
            brick["color"] = (color_options[randint(0, len(color_options)-1)])
            bricks.append(brick)                        # adds that brick to the list of all bricks

def generate_random_level(level):
    # Increase difficulty with level
    rows = min(5 + (level - 6) // 2, 8)  # Max 8 rows
    columns = min(10 + (level - 6), 13)  # Max 13 columns
    
    # Create a random pattern with increasing density
    shape = []
    for i in range(rows):
        row = []
        for j in range(columns):
            # Higher chance to have a brick as level increases
            if randint(1, 10) > (3 if level < 8 else 2):
                row.append(1)
            else:
                row.append(0)
        shape.append(row)
    
    return {
        "shape": shape,
        "brick_lives": 2  # All bricks have 2 lives
    }

def setBreakout(level: int, two_players: bool = False, newlives: int = 3): # resets the breakoutgame by restoring the bricks and the variables
   global two_player_mode
   two_player_mode = two_players
   initialiseBreakoutgameVariables(level, newlives= newlives) # resets all the variables
   makeBricks(level)

# music
def play_menu_music():
    pygame.mixer.music.load(menu_music)
    pygame.mixer.music.play(-1)  # Loop oneindig
    pygame.mixer.music.set_volume(volume/100)  # Volume aanpassen

def play_gameplay_music():
    pygame.mixer.music.load(gameplay_music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume/100)

def calculate_average_ballspeed() -> float:
   # calculates average speed of all balls
   total_speed = 0
   for ball in balls:
      ball_speed = (ball["speed_x"]**2 + ball["speed_y"]**2)**0.5
      total_speed += ball_speed
    
   average_ball_speed = total_speed / len(balls)
   return average_ball_speed

def update_paddle_speed():
    global paddle_speed, paddle2_speed
    if len(balls) == 0:  # if there are no balls to avoid dividing by 0
        paddle_speed = 10
        paddle2_speed = 10
        return
    
    average_ball_speed = calculate_average_ballspeed()
    
    # increases paddle speed based on average ball speed with maximum limit
    paddle_speed = min(10 + average_ball_speed / 3, MAX_PADDLE_SPEED)
    paddle2_speed = min(10 + average_ball_speed / 3, MAX_PADDLE_SPEED)

def limit_ball_speed(speed_x, speed_y, max_speed):
    current_speed = (speed_x**2 + speed_y**2)**0.5
    if current_speed > max_speed:
        scale_factor = max_speed / current_speed
        return speed_x * scale_factor, speed_y * scale_factor
    return speed_x, speed_y

def handleMenuInputs(buttons: list, columns: int = 1):
   global button_cooldown_timer, button_cooldown_ticks, keys, game_status, GAME_STATUSES, selected_button, level, musicIsPlaying, musicIsInitialised, two_player_mode
   while len(buttons) % columns != 0:
      buttons.append('')

   if button_cooldown_timer == 0: # if there is no cooldown at the moment
      button_cooldown_timer = button_cooldown_ticks # cooldown of when the game wont register any key presses from user in ticks
      
      if keys[pygame.K_q] : # key q is down         
         selected_button_name = str(buttons[selected_button]) # we set this here in case we change it below
         try:
            GAME_STATUSES[selected_button_name] # if the name of the button is not found in the list of gamestatuses it will give crash
            # resets things if needed
            # music
            if (GAME_STATUSES[selected_button_name] == 0 and (game_status == 4 or game_status == 5)) or ((GAME_STATUSES[selected_button_name] == 1 or GAME_STATUSES[selected_button_name] == 7) and (game_status == 0 or game_status == 4 or game_status == 8)): # if (we go to homescreen from pause or game over) or (we go to breakout from homescreen, game over or level select)
               if musicIsInitialised: # only execute is music is working
                  pygame.mixer.stop() # stops the current music so new music can be played
                  musicIsPlaying = False
            # selected button
            if GAME_STATUSES[selected_button_name] == 6 or GAME_STATUSES[selected_button_name] == 8: # if we go to settings or level select
               selected_button = 0
            # reset breakout
            if (GAME_STATUSES[selected_button_name] == 1 or GAME_STATUSES[selected_button_name] == 7) and str(buttons[selected_button]) != "resume": # if we go to breakout while it is not resumed from the pause menu
               level = 1
               if GAME_STATUSES[selected_button_name] and selected_button_name != 'play again'== 1:
                  two_player_mode = False
               if GAME_STATUSES[selected_button_name] == 7:
                  two_player_mode = True
               setBreakout(level, two_player_mode)   # resets the breakout game to level 1
         except KeyError:
            if 'level' in selected_button_name:
               print('A keyerror got exepted, \'' + str(selected_button_name) + '\' was not found in \'GAME_STATUSES\'')
            else:
               raise KeyError('\'' + str(selected_button_name) + '\' was not found in \'GAME_STATUSES\'')
         return selected_button_name # tell the program which button is selected
      
      elif keys[pygame.K_w] : # key w is down
         selected_button -= columns            # moves the selected button number 1 row down; selected button goes up visualy
         if selected_button < 0:               # if the selected button number underflows
            selected_button += len(buttons)    # adds the total number of buttons so it loops around
         while buttons[selected_button] == '': # snaps to a button
            selected_button -= 1
      
      elif keys[pygame.K_s] : # key s is down
         selected_button += columns          # moves the selected button number 1 up; selected button goes down visualy
         if selected_button >= len(buttons): # if the selected button number overflows
            selected_button -= len(buttons)  # subtracts the total number of buttons so it loops around
         while buttons[selected_button] == '': # snaps to a button
            selected_button -= 1
      
      elif keys[pygame.K_a] : # key a is down
         selected_button -= 1                  # moves selected button 1 to the left
         if selected_button < 0:               # if the selected button number underflows
            selected_button = len(buttons) - 1 # change the selected button number to the highest
         while buttons[selected_button] == '': # snaps to a button
            selected_button -= columns

      elif keys[pygame.K_d] : # key d is down
         selected_button += 1                # moves selected button 1 to the right
         if selected_button >= len(buttons): # if the selected button number overflows
            selected_button = 0              # change the selected button number to the lowest
         while buttons[selected_button] == '': # snaps to a button
            selected_button -= columns
            
      else:
         button_cooldown_timer = 0 # no keys were hit so the cooldown is set to 0
   
   else:
      button_cooldown_timer -= 1 # decrease cooldown by 1

   while '' in buttons: # removes all the '' in the list of buttons, buttons should be a local variable but is somehow accessed by drawButtons so we need to revome the ''
      buttons.remove('')


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
BRICK_EXPLOSION_WIDTH = 80   # width of explosion in pixels
BRICK_EXPLOSION_HEIGHT = 77  # height of explosion in pixels
LAST_LEVEL_SINGLEPLAYER = 10 # the number of the last level in singleplayer mode
LAST_LEVEL_TWOPLAYER = 5     # the number of the last level in twoplayer mode
STAR_WIDTH = 32              # width of star in pixels
STAR_HEIGHT = 32             # height of star in pixels
POWERUP_DURATION = 300       # duration of powerup effect in frames (10 seconds at 30 FPS)
MAX_PADDLE_SPEED = 20        # maximum speed of the paddle
MAX_BALL_SPEED = 15          # maximum speed of the ball
RESET_DELAY = 45             # amount of frames between lives
POWERUP_MESSAGE_DURATION = 300 # amount of frames the reverse control warning lasts
WINNING_SCORE = 100          # the amount of points you need to get to win in two player
GAME_STATUSES = {"Back": -1, # back needs to be handled by other code
                 "homescreen": 0,
                 "breakout": 1, # start, resume, play again and breakout all need to start the breakout game
                 "start": 1,
                 "resume": 1,
                 "play again": 1,
                 "info": 2,
                 "quit": 3,
                 "game over": 4,
                 "yes": 4, "no": 4, # yes and no are usen while saving your highscore
                 "pause": 5,
                 "settings": 6,
                 "no sound": 6,
                 "volume": 6,
                 "two player": 7,
                 "level select": 8} # if a button is selected this will tell the code to which number the game_status var needs to be set

# global variables
# breakout game variables are set when you start the game

level = 1 # the current level
max_level_playable = 1 # we use this for the level selection screen

level_1 = {"shape": [
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
    ],  "brick_lives": 1} # how the bricks should be made in level 1

level_2 = {"shape": [
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
    ],  "brick_lives": 2} # how the bricks should be made in level 2

level_3 = {"shape": [
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    ], "brick_lives": 2} # how the bricks should be made in level 3

level_4 = {"shape": [
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]
    ], "brick_lives": 2}

level_5 = {"shape": [
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ], "brick_lives": 2}

level_1_2p = { 
    "shape": [
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    "brick_lives": 1,
}

level_2_2p = {
    "shape": [
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    ],
    "brick_lives": 2,
}

level_3_2p = {
    "shape": [
        [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
    ],
    "brick_lives": 2,
}

level_4_2p = {
    "shape": [
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
    ],
    "brick_lives": 2,
}

level_5_2p = {
    "shape": [
        [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1]
    ],
    "brick_lives": 2,
}

levels = {'1p': [level_1, level_2, level_3, level_4, level_5], '2p': [level_1_2p, level_2_2p, level_3_2p, level_4_2p, level_5_2p]}

controls_reversed = False
controls_message_timer = 0
powerup_message_timer = 0

reset_delay_timer = 0

old_game_status = 0 # so we can keep track of the last game status that we were in
game_status = 0 # 0 = homescreen, 1 = breakoutgame, 2 = infoscreen, 3 = stopping python, 4 = game over, 5 = pause menu, 6 = settings menu, 7 = two player mode, 8 = level select

volume = 50 # the volume of all sound as a number from 0 to 100
volume_change_mode = False

selected_button = 0        # index of which button is selected
button_cooldown_timer = 0  # the timer for the cooldown on hitting a button
button_cooldown_ticks = 10 # the reset value for the timer
extra_ball_cooldown_timer = 0 # the timer for the cooldown on spawning a new ball (debug)

homescreen_buttons = ['start', 'two player', 'level select', 'info', 'settings', 'quit'] # all the buttons on the homescreen
pause_menu_buttons = ['resume', 'settings', 'homescreen']
settings_buttons = ['volume', 'Back']
game_over_screen_buttons = ['play again', 'settings', 'homescreen', 'quit']
save_highscore_buttons = ['yes', 'no']
level_select_buttons = []
for i in range(0, LAST_LEVEL_SINGLEPLAYER): # this will generate the names for all the levels even if you add new levels
   level_select_buttons.append('level' + str(i+1))

singleplayer_score = 0
score_multiplier = 1
highscore = 0
add_highscore_mode = False
highscore_checked = False

player1_score = 0
player2_score = 0

two_player_mode = False

balls = [] # a list of all the active balls
powerups = [] # a list of all the active powerups
powerup_timer = 0
bricks = [] # a list of all the active bricks

informationtext = [
    "WELKOM BIJ BREAKOUT! ",
    " ",
    "DOEL VAN HET SPEL:",
    "- Sla de bal met je paddle om alle stenen te breken",
    "- Laat de bal niet onder je paddle vallen!",
    " ",
    "CONTROLES:",
    "- Paddle bewegen: A (links) en D (rechts)",
    "- Menu navigatie: W (omhoog), S (omlaag), Q (bevestigen)",
    "- Pauzeren: R toets",
    " ",
    "COOLE FEATURES:",
    "- Meerdere levels met unieke patronen",
    " Speciale power-ups uit stenen:",
    "   Groene sterren: Verklein je paddle of reverse controls",
    "   Gele sterren: Vergroot je paddle of score multiplier",
    "   Als je geluk hebt: Krijg een extra bal",
    "   Score multipliers: Verdubbel je punten! Deze werken per level",
    "- Paddle snelheid past zich aan aan de bal",
    "- Levenssysteem met hartjes",
    " ",
    "GAME MECHANICS:",
    "- De bal kaast anders af afhankelijk van waar hij je paddle raakt",
    "- Bal snelheid wordt sneller naarmate je vordert",
    "- Maar geen zorgen, er is een maximumsnelheid!",
    " ",
    "TIPS & TRICKS:",
    "- Probeer de bal met de randen van je paddle te raken",
    "- Het midden van de paddle geeft voorspelbare stuiters",
    "- Vang zo veel mogelijk power-ups op!",
    "- Probeer alle powerdowns te vermijden!",
    " ",
    "SCORE SYSTEM:",
    "- Hogere levels geven meer punten",
    "- Power-ups geven bonuspunten (Powerdowns geven minpunten)",
    "- Probeer je highscore te verbeteren!",
    " ",
    "TWEE SPELERS MODUS:",
    "- Speel tegen een vriend!",
    "- Jij bent de onderste paddle, je vriend de bovenste",
    "- Verzamel punten door stenen te breken en bij de ander te scoren",
    "- Eerste met 100 punten wint!",
    " ",
    "CREDITS:",
    "- Game gemaakt met Python en Pygame",
    "- Kunst van OpenGameArt.org",
    "- Geluidseffecten van freesound.org",
    "                                - Veel plezier! " # ingesprongen omdat die anders voor de paddle zit
]

#
# init game
#
pygame.mixer.pre_init() # music test
pygame.init()
try:
   pygame.mixer.init() # music
except:
   print("music could not be initialised")
   musicIsInitialised = False
   settings_buttons[0] = 'no sound' # the button for changing volume is set to 'no sound' to give information to the player
else:
   # music
   # Sound effects
   musicIsInitialised = True
   bounce_sound = pygame.mixer.Sound("./Bounce.mp3")  # Bal die tegen paddle of bricks botst
   powerup_sound = pygame.mixer.Sound("./Power.mp3")  # Power-up opgepakt
   level_complete_sound = pygame.mixer.Sound("./Win.mp3")  # Level voltooid
   game_over_sound = pygame.mixer.Sound("./Lose.mp3")  # Game over
   ready_sound = pygame.mixer.Sound("./ready.mp3") # ready sound
   break_sound = pygame.mixer.Sound("./blockbreak.mp3") # ready sound
   all_sounds = [bounce_sound, powerup_sound, level_complete_sound, game_over_sound, ready_sound, break_sound]
   for sound in all_sounds:
      sound.set_volume(volume/100)
   break_sound.set_volume(break_sound.get_volume() * 0.5) # break block sound is very loud so it gets scaled down more than the rest
   
   # Background music
   menu_music = "./menu_music.mp3"
   gameplay_music = "./gameplay_music.mp3"
   game_over_music = "./game_over_music.mp3"

musicIsPlaying = False

font = pygame.font.SysFont('default', 64)                                                          # creates the font for the game
font_smaller = pygame.font.SysFont('default', 40)                                                  # Smaller font for some text
font_smallest = pygame.font.SysFont('default', 24)                                                 # Smallest font for info screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED) # makes sure the width and heigth of the screen are set to preference and scales them the max while keeping them in the same ratio
fps_clock = pygame.time.Clock()                                                                    # makes an object to keep track of the time

# loading constant texts, needs to be done after font is loaded
savehighscore_text = font.render('Do you want to save your highscore?', True, 'white')
savehighscore_subtext = font_smaller.render('(this will create a file called \'highscore.txt\')', True, 'white')

ready_text = (font.render("READY?", True, "white"))
ready_text_x = SCREEN_WIDTH // 2 - ready_text.get_width() // 2
ready_text_y = SCREEN_HEIGHT // 2 - ready_text.get_height() // 2

#
# read images
#

background = pygame.image.load("Background.png") # loads background image and names it 'background'
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

green_star = pygame.image.load('powerdown.png').convert_alpha() # converts the image using alpha conversion in to rgba and calls it badstar

wide_paddle = pygame.image.load('wide_paddle.png').convert_alpha() # converts the image using alpha conversion in to rgba and calls it wide_paddle


ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)                   # sets 'ball_img' to aan img with dimentions 64x64 and 'SRCALPHA' to have individual pixel transparency
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))                # picks the ball image fron the spritesheet
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) # scales the image of the ball to the desired height and width

paddle_medium_img = pygame.Surface((243, 64), pygame.SRCALPHA)                        # sets 'paddle_img' to aan img with dimentions 243x64 and 'SRCALPHA' to have individual pixel transparency
paddle_medium_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))                     # picks the paddle image fron the spritesheet
paddle_medium_img = pygame.transform.scale(paddle_medium_img, (PADDLE_MEDIUM_WIDTH, PADDLE_HEIGHT)) # scales the image of the paddle to the desired height and width

paddle_small_img = pygame.Surface((115, 64), pygame.SRCALPHA)                        
paddle_small_img.blit(spritesheet, (0, 0), (1574, 912, 115, 64)) 
paddle_small_img = pygame.transform.scale(paddle_small_img, (PADDLE_SMALL_WIDTH, PADDLE_HEIGHT))

paddle_large_img = pygame.Surface((733, 129), pygame.SRCALPHA)                        
paddle_large_img.blit(wide_paddle, (0, 0), (0, 0, 733, 129))  
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

bad_star_img = pygame.Surface((950, 930), pygame.SRCALPHA)
bad_star_img.blit(green_star, (0, 0), (0, 0, 950, 930))  
bad_star_img = pygame.transform.scale(bad_star_img, (STAR_WIDTH, STAR_HEIGHT))

good_star_img = pygame.Surface((64, 61), pygame.SRCALPHA)
good_star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61)) 
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

red_button_img = pygame.Surface((96, 32), pygame.SRCALPHA) # makes a new button surface
red_button_img.blit(red_brick_img, (0,0))                  # puts the red_brick_img onto the new surface
red_button_img = pygame.transform.scale(red_button_img, (BUTTON_WIDTH, BUTTON_HEIGHT)) # transforms the img to the desired widht and height

button_images = {'blue': blue_button_img,
                 'orange': orange_button_img,
                 'red': red_button_img}

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

      drawButtons(homescreen_buttons, selected_button, columns = 2) # draws the buttons on the homescreen
      if musicIsInitialised and not musicIsPlaying: # only execute if music is working and is not playing already
         play_menu_music()
         musicIsPlaying = True

      
      game_status_msg = "Move with WASD and confirm with Q" # info for the player

      # get the player inputs
      #
      pressed_button = handleMenuInputs(homescreen_buttons, columns = 2)
      if pressed_button != None:
         old_game_status = game_status
         game_status = GAME_STATUSES[pressed_button] # this sets the game status number to the number that is defined by the name on the selected button
   

   #
   # breakout game
   #

   elif game_status == 1 or game_status == 7: # breakout game
      
      if controls_message_timer > 0:
         if level == 1:
            game_status_msg = "Move with A and D" # tell the player what they should do
         controls_message_timer -= 1
      else:
         if powerup_message_timer > 0:
            if controls_reversed:
               game_status_msg = "REVERSE CONTROLS!"
            else:
               game_status_msg = "SCORE MULTIPLIER: " + str(score_multiplier) + "X"
         else:
            game_status_msg = ""
      
      if musicIsInitialised and not musicIsPlaying: # only execute if music is working and is not playing already: # only execute is music is working
         play_gameplay_music()
         musicIsPlaying = True
     
     
      if reset_delay_timer == 0:     
         # 
         # move everything
         #
  
         # player inputs
         if len(balls) > 0:  # Only update paddle speed if there are balls
            update_paddle_speed() # updates the paddlespeed based on the ballspeed
      
         if not controls_reversed:
            if keys[pygame.K_d]:      # key d is down
               paddle_x = paddle_x + paddle_speed # moves the paddle to the right
            if keys[pygame.K_a]:      # key a is down
               paddle_x = paddle_x - paddle_speed # moves the paddle to the left
         
         else:  # controls are reversed
            if keys[pygame.K_d]:      # key d is down (now moves left)
               paddle_x = paddle_x - paddle_speed
            if keys[pygame.K_a]:      # key a is down (now moves right)
               paddle_x = paddle_x + paddle_speed

         if game_status == GAME_STATUSES["two player"]:
            if not controls_reversed:
               if keys[pygame.K_l]:      # l is right for player 2
                  paddle2_x += paddle2_speed
               if keys[pygame.K_j]:       # j is left for player 2
                  paddle2_x -= paddle2_speed
            else:
               if keys[pygame.K_l]:      # reverse controls
                  paddle2_x -= paddle2_speed
               if keys[pygame.K_j]:
                  paddle2_x += paddle2_speed

         # debug controls
         #  
         # press 1 to skip the level
         if keys[pygame.K_1] : # key 1 is down
            print("player skipped level: " + str(level)) # debug
            bricks = [] # makes bricks empty so the level is beaten
         
         # press 0 to spawn an extra ball
         if keys[pygame.K_0] : # key 0 is down
            if extra_ball_cooldown_timer == 0:
               print("player spawned a ball, number of balls is: " + str(len(balls))) # debug
               # spawn a ball
               balls.append({
                  "x": paddle_x + (paddle_width - BALL_WIDTH) // 2,
                  "y": paddle_y - BALL_HEIGHT,
                  "speed_x": randint(-3, 3),
                  "speed_y": -5,
                  })
               if balls[-1]['speed_x'] == 0:
                  balls[-1]['speed_x'] = 1
               extra_ball_cooldown_timer = 10
            else:
               extra_ball_cooldown_timer -= 1

         if button_cooldown_timer == 0:
            if keys[pygame.K_r] : # key r is down
               button_cooldown_timer = button_cooldown_ticks
               old_game_status = game_status
               selected_button = 0
               game_status = GAME_STATUSES["pause"] # pause the game
         else:
            button_cooldown_timer -= 1
  
            # move ball
         for ball in balls[:]:  
            ball["x"] += ball["speed_x"]  # this moves the bal with the ballspeed from the old x of the bal to the new x
            ball["y"] += ball["speed_y"]  # this moves the bal with the ballspeed from the old y of the bal to the new y
  
            # losing
            

            if game_status == 7:  # Two player mode
               # Delete ball if it touches the top of the screen (player 1 scores)
               if ball["y"] < -BALL_HEIGHT:
                  player1_score += 10
                  balls.remove(ball)
                  continue
         
               # Delete ball if it touches the bottom of the screen (player 2 scores)
               if ball["y"] > SCREEN_HEIGHT:
                  player2_score += 10
                  balls.remove(ball)
                  continue
    
               
                     
            else:
               # only needs to be executed if we are in single player mode
               # bounces ball if it reaches the top of the screen
               if ball["y"] < 0:
                  ball["speed_y"] = abs(ball["speed_y"])
                  ball["speed_x"], ball["speed_y"] = limit_ball_speed(ball["speed_x"], ball["speed_y"], MAX_BALL_SPEED)

               if ball["y"] > SCREEN_HEIGHT:
                  balls.remove(ball)
                  if len(balls) == 0:  # there are no more balls
                     lives -= 1
                     if lives == 0: # if you have no lives left
                        game_status_msg = "You lost!"
                        old_game_status = game_status
                        game_status = GAME_STATUSES["game over"]  # game over screen
                        highscore_checked = False
                        if musicIsInitialised: # only execute is music is working
                           pygame.mixer.stop() # stops the current music so new music can be played
                           musicIsPlaying = False
                     else: # if you have lives left
                        reset_delay_timer = RESET_DELAY  # Start delay
                        # Reset ball position/speed, powerups, etc.
                        balls.append({
                        "x": paddle_x + (paddle_width - BALL_WIDTH) // 2,  # Spawn in middle of paddle
                        "y": paddle_y - BALL_HEIGHT,
                        "speed_x": randint(-3, 3),
                        "speed_y": int(-(level ** 0.5) * 6),
                        })
                        if balls[0]["speed_x"] == 0:
                           balls[0]["speed_x"] = 1
                        if reset_delay_timer == RESET_DELAY and musicIsInitialised:
                           ready_sound.play()
                  continue
      
            # bounces ball
  
            # bounces ball if it reaches the side of the screen
            if ball["x"] < 0:
               ball["speed_x"] = abs(ball["speed_x"])
               ball["speed_x"], ball["speed_y"] = limit_ball_speed(ball["speed_x"], ball["speed_y"], MAX_BALL_SPEED)
            if ball["x"] + BALL_WIDTH > SCREEN_WIDTH:
               ball["speed_x"] = -abs(ball["speed_x"])
               ball["speed_x"], ball["speed_y"] = limit_ball_speed(ball["speed_x"], ball["speed_y"], MAX_BALL_SPEED)
  
                  
  
  
        
            # 
            # handle collisions
            #
         
            # ball-paddle collision for multiple balls
   
            # Top of paddle collision
            if (ball["x"] + BALL_WIDTH > paddle_x and  # if the ball is right of paddle's left side
                ball["x"] < paddle_x + paddle_width and # and if the ball is left of paddle's right side
                ball["y"] + BALL_HEIGHT > paddle_y and  # and if the ball's bottom is under paddle's top
                ball["y"] < paddle_y):                  # and if the ball's top is above paddle's top
    
                  ball["speed_y"] = abs(ball["speed_y"]) * -1 # bounce ball by negating y speed
                  print(f'ball hit paddle {round(ball["x"] + (BALL_WIDTH / 2) - (paddle_x + (paddle_width / 2)), 1)}px of the middle of the paddle') # debug info
        
                  # Calculate new x speed based on where ball hits paddle
                  hit_position = ((ball["x"] + (BALL_WIDTH / 2)) - (paddle_x + (paddle_width / 2))) / (paddle_width / 2)
                  ball["speed_x"] = (ball["speed_x"] + (hit_position * paddle_steer)) / 2
        
                  # Limit ball speed
                  ball["speed_x"], ball["speed_y"] = limit_ball_speed(ball["speed_x"], ball["speed_y"], MAX_BALL_SPEED)
                  
                  if musicIsInitialised: # only execute if music is working
                     bounce_sound.play()


            # Side of paddle collision
            elif (ball["y"] + BALL_HEIGHT > paddle_y and # if the ball's bottom is under paddle's top
                ball["y"] < paddle_y + PADDLE_HEIGHT and  # if ball's top is above paddle's bottom
                ((ball["x"] + BALL_WIDTH > paddle_x and ball["x"] < paddle_x) or  # left side collision
                (ball["x"] + BALL_WIDTH > paddle_x + paddle_width and ball["x"] < paddle_x + paddle_width))): # right side collision
    
                  ball["speed_x"] *= -1 # bounce ball by negating x speed
                  if musicIsInitialised: # only execute if music is working
                     bounce_sound.play()

            
            # Top of paddle 2 collision
            # this paddle is on the top of the screen so it needs to bounce on the bottom of the paddle
            if game_status == 7:
               if (ball["x"] + BALL_WIDTH > paddle2_x and # if the ball is right of paddle's left side
                   ball["x"] < paddle2_x + paddle2_width and  # and if the ball is left of paddle's right side
                   ball["y"] < paddle2_y + PADDLE_HEIGHT and  # and if the ball's top is above paddle's bottom
                   ball["y"] + BALL_HEIGHT > paddle2_y + PADDLE_HEIGHT):      # and if the ball's bottom is under paddle's bottom
                     # Handle collision
    
                     ball["speed_y"] = abs(ball["speed_y"]) * 1 # bounce ball by negating y speed
                     print(f'ball hit paddle2 {round(ball["x"] + (BALL_WIDTH / 2) - (paddle2_x + (paddle_width / 2)), 1)}px of the middle of the paddle') # debug info
        
                     # Calculate new x speed based on where ball hits paddle
                     hit_position = ((ball["x"] + (BALL_WIDTH / 2)) - (paddle2_x + (paddle2_width / 2))) / (paddle2_width / 2)
                     ball["speed_x"] = (ball["speed_x"] + (hit_position * paddle_steer)) / 2
        
                     # Limit ball speed
                     ball["speed_x"], ball["speed_y"] = limit_ball_speed(ball["speed_x"], ball["speed_y"], MAX_BALL_SPEED)
                  
                     if musicIsInitialised: # only execute if music is working
                        bounce_sound.play()
            
               # Side of paddle 2 collision
               elif (ball["y"] < paddle2_y  + PADDLE_HEIGHT and # if the ball's top is avove paddle's bottom
                   ball["y"] + BALL_HEIGHT > paddle2_y and  # if ball's bottom is under paddles top
                   ((ball["x"] + BALL_WIDTH > paddle2_x and ball["x"] < paddle2_x) or  # left side collision
                   (ball["x"] + BALL_WIDTH > paddle2_x + paddle2_width and ball["x"] < paddle2_x + paddle2_width))): # right side collision
    
                     ball["speed_x"] *= -1 # bounce ball by negating x speed
                     if musicIsInitialised: # only execute if music is working
                        bounce_sound.play()
            

            # Brick collision
            for i in range(len(bricks)-1, -1, -1):  # Loop backwards through bricks
               if (ball["x"] + BALL_WIDTH > bricks[i]["x_position"] and # if the ball is touching a brick
                  ball["x"] < bricks[i]["x_position"] + BRICK_WIDTH and
                  ball["y"] + BALL_HEIGHT > bricks[i]["y_position"] and
                  ball["y"] < bricks[i]["y_position"] + BRICK_HEIGHT):

                  # Bounce ball based on collision side
                  if ball["speed_y"] > 0 and ball["y"] < bricks[i]["y_position"]:
                     # # ball comes from above
                     ball["speed_y"] *= -1
                  elif ball["speed_y"] < 0 and ball["y"] + BALL_HEIGHT > bricks[i]["y_position"] + BRICK_HEIGHT:
                     # # ball comes from under
                     ball["speed_y"] *= -1
                  elif ball["speed_x"] > 0 and ball["x"] < bricks[i]["x_position"]:
                     # # ball comes from left
                     ball["speed_x"] *= -1
                  elif ball["speed_x"] < 0 and ball["x"] + BALL_WIDTH > bricks[i]["x_position"] + BRICK_WIDTH:
                     # ball comes from right
                     ball["speed_x"] *= -1                                                      # bounches ball by negating x speed
                  if musicIsInitialised: # only execute is music is working
                     break_sound.play()
           
                  bricks_animations.append(bricks[i].copy()) # adds the brick that is hit to the list of bricks that are animated
                  # .copy() is used here so we dont get an error when drawing the animations, if the same block is hit twice too fast, a bad refrence (or something refrence related) whould give it an error
                  bricks_animations[-1]["frame"] = 0  # adds zero because that is the frame of the current animation
                  bricks[i]["lives"] -= 1 # removes 1 life from that block
                  
                  if bricks[i]["lives"] == 0:
                     if game_status == 7: # two player score handling
                        # we check which direction the ball came from to give a player points
                        # the ball has already bounce so we check the direction reversed
                        if ball["speed_y"] > 0: # ball goes down, went up when it hit the brick
                           player1_score += 1
                        elif ball["speed_y"] < 0: # ball goes up, went down when it hit the brick
                           player2_score += 1

                     if game_status == 1: # we only have powerups and singelplayer_score in single player
                        base_points = level * 10  # higher levels give more points
                        singleplayer_score += base_points * score_multiplier
                        powerup_roll = randint(1, 100)  # 1-100 for different probabilities
                        if powerup_roll <= 5: # 5% chance
                           # small paddle
                           powerups.append({
                              "x_position": bricks[i]["x_position"] + BRICK_WIDTH//2 - STAR_WIDTH//2,
                              "y_position": bricks[i]["y_position"],
                              "type": "small",
                              "frame": 0
                              })
                        elif powerup_roll <= 15: # 10% chance
                           # large paddle
                           powerups.append({
                              "x_position": bricks[i]["x_position"] + BRICK_WIDTH//2 - STAR_WIDTH//2, # adds all the propertys of the powerup to the list powerups
                              "y_position": bricks[i]["y_position"],
                              "type": "large",
                              "frame": 0
                              })
                        elif powerup_roll <= 35: # 20% chance
                           #  extra bal
                           average_ballspeed = calculate_average_ballspeed()
                           balls.append({
                              "x": bricks[i]["x_position"] + BRICK_WIDTH//2 - BALL_WIDTH//2,
                              "y": bricks[i]["y_position"] + BRICK_HEIGHT//2 - BALL_HEIGHT//2,
                              "speed_x": ball['speed_x'] + randint(-10,10)/10, # the new ball gets the speed of the ball that hit the brick +/- a random value from -1 to 1
                              "speed_y": ball['speed_y'] + randint(-10,10)/10
                              })
                           if balls[-1]["speed_x"] == 0:
                              balls[-1]["speed_x"] = 1
                        elif powerup_roll <= 40: # 5% chance
                           # reverse controls
                           powerups.append({
                              "x_position": bricks[i]["x_position"] + BRICK_WIDTH//2 - STAR_WIDTH//2,
                              "y_position": bricks[i]["y_position"],
                              "type": "reverse",
                              "frame": 0
                              })
                        elif powerup_roll <= 50: # 10% chance
                           # score multiplier
                           powerups.append({
                              "x_position": bricks[i]["x_position"] + BRICK_WIDTH//2 - STAR_WIDTH//2,
                              "y_position": bricks[i]["y_position"],
                              "type": "score_mult",
                              "frame": 0
                              })
                     bricks.pop(i) # removes the block from list of all bricks
                  
                  ball["speed_x"] *= randint(95, 110)/100
                  ball["speed_y"] *= randint(95, 110)/100
                  ball["speed_x"], ball["speed_y"] = limit_ball_speed(ball["speed_x"], ball["speed_y"], MAX_BALL_SPEED)
                  break # stops the loop so we don't get errors

         if game_status == 7:
            # Respawn balls if none are left
            if len(balls) == 0:
               reset_delay_timer = RESET_DELAY
               # Spawn ball for player 1 (bottom)
               balls.append({
                  "x": paddle_x + (paddle_width - BALL_WIDTH) // 2,
                  "y": paddle_y - BALL_HEIGHT,
                  "speed_x": randint(-3, 3),
                  "speed_y": -5,
                  })
        
               # Spawn ball for player 2 (top)
               balls.append({
                  "x": paddle2_x + (paddle2_width - BALL_WIDTH) // 2,
                  "y": paddle2_y + PADDLE_HEIGHT,
                  "speed_x": randint(-3, 3),
                  "speed_y": 5,
                  })
        
               if balls[0]["speed_x"] == 0:
                  balls[0]["speed_x"] = 1
               if balls[1]["speed_x"] == 0:
                  balls[1]["speed_x"] = 1

            # winning two player
            if player1_score >= WINNING_SCORE:
               game_status_msg = "Player 1 wins!"
               old_game_status = game_status
               game_status = GAME_STATUSES["game over"]
               if musicIsInitialised:
                  pygame.mixer.stop()
                  musicIsPlaying = False
            elif player2_score >= WINNING_SCORE:
               game_status_msg = "Player 2 wins!"
               old_game_status = game_status
               game_status = GAME_STATUSES["game over"]
               if musicIsInitialised:
                  pygame.mixer.stop()
                  musicIsPlaying = False
         
         # paddle-wall colisions
         if paddle_x + paddle_width > SCREEN_WIDTH: # if paddle goes of the screen on the right side
            paddle_x = SCREEN_WIDTH - paddle_width  # paddle is set to the rightmost x position
   
         if paddle_x < 0: # if paddle goes of the screen on the left side
            paddle_x = 0  # paddle is set to the leftmost x position

         # paddle2-wall colisions
         if game_status ==7:
            if paddle2_x + paddle2_width > SCREEN_WIDTH: # if paddle goes of the screen on the right side
               paddle2_x = SCREEN_WIDTH - paddle2_width  # paddle is set to the rightmost x position
   
            if paddle2_x < 0: # if paddle goes of the screen on the left side
               paddle2_x = 0  # paddle is set to the leftmost x position  
         
         # Move and draw powerups
         if game_status == 1: # we only have powerups in single player
            for powerup in powerups[:]:
               powerup["y_position"] += 3  # Move powerup downward
    
               # Draw powerup
               if powerup["type"] == "large" or powerup["type"] == "score_mult":
                  screen.blit(good_star_img, (powerup["x_position"], powerup["y_position"]))
               else:
                  screen.blit(bad_star_img, (powerup["x_position"], powerup["y_position"]))
    
               # Check collision with paddle
               if (powerup["x_position"] + STAR_WIDTH > paddle_x and
                  powerup["x_position"] < paddle_x + paddle_width and
                  powerup["y_position"] + STAR_HEIGHT > paddle_y and
                  powerup["y_position"] < paddle_y + PADDLE_HEIGHT):
            
                  paddle_center = paddle_x + paddle_width // 2
            
                  if musicIsInitialised: # only execute is music is working
                     powerup_sound.play()
            
                  if powerup["type"] == "small":
                     paddle_width = PADDLE_SMALL_WIDTH
                     paddle_img = paddle_small_img
                     singleplayer_score -= 100 * score_multiplier # powerdowns subtract points from score
                  elif powerup["type"] == "reverse":
                     controls_reversed = True
                     powerup_message_timer = POWERUP_MESSAGE_DURATION
                     singleplayer_score -= 100 * score_multiplier # powerdowns subtract points from score
                  elif powerup["type"] == "large":
                     paddle_width = PADDLE_LARGE_WIDTH
                     paddle_img = paddle_large_img
                     singleplayer_score += 100 * score_multiplier
                  elif powerup["type"] == "score_mult":
                     score_multiplier += 1
                     powerup_message_timer = POWERUP_MESSAGE_DURATION
                     singleplayer_score += 100 * score_multiplier
            
                  # Keep paddle centered after powerups
                  paddle_x = paddle_center - paddle_width // 2
    
                  powerup_timer = POWERUP_DURATION
                  powerups.remove(powerup)
                  continue  # Skip the rest of the loop for this powerup
            
        
               # Remove if off screen
               if powerup["y_position"] > SCREEN_HEIGHT:
                  powerups.remove(powerup)

         # Handle powerup timing
         if powerup_message_timer > 0: # makes sure the controls reversed text is only there when the controls are reversed
            powerup_message_timer -= 1
         if powerup_timer >= 0:
            powerup_timer -= 1
         if powerup_timer == 0:
            # Reset paddle to original size
            paddle_center = paddle_x + paddle_width // 2
            paddle_width = PADDLE_MEDIUM_WIDTH
            paddle_img = paddle_medium_img
            paddle_x = paddle_center - paddle_width // 2 # Keep paddle centered after powerups
            if controls_reversed:
               controls_reversed = False

         # checks if game is over
         # winning one player
         
         if len(bricks) == 0: # when there are no bricks
            if level == (LAST_LEVEL_SINGLEPLAYER if not two_player_mode else LAST_LEVEL_TWOPLAYER): # if you completed the last level for your gamemode
               ball_speed_x = 0 # set ballspeed to 0
               ball_speed_y = 0 # set ballspeed to 0
               if two_player_mode:
                  if player1_score > player2_score:
                     game_status_msg = "Player 1 wins!"
                  elif player1_score == player2_score:
                     game_status_msg = "Draw!"
                  else:
                     game_status_msg = "Player 2 wins!"
               else:
                  game_status_msg = "You won the game!" # If you finished the last level set to winningscreen
               old_game_status = game_status
               game_status = GAME_STATUSES["game over"]  # game over screen
               highscore_checked = False
               if musicIsInitialised: # only execute is music is working
                  pygame.mixer.stop() # stops the current music so new music can be played
                  musicIsPlaying = False
            else: # if you completed a level
               level += 1  # Go to next level
               setBreakout(level, two_player_mode, newlives= lives)
               game_status_msg = "Level " + str(level) + "!"
               if musicIsInitialised: # only execute is music is working
                  level_complete_sound.play()
            if not two_player_mode: # the level selection screen update is for single player only
               max_level_playable = max(max_level_playable, level)


      else:
         reset_delay_timer -= 1  # removes 1 from the timer every frame 

      # 
      # draw everything
      #

      # draw ball and paddle
      for ball in balls:
         screen.blit(ball_img, (ball["x"], ball["y"]))
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
      
      if reset_delay_timer > 0:
         screen.blit(ready_text, (ready_text_x, ready_text_y))
         if reset_delay_timer == RESET_DELAY and musicIsInitialised:
            ready_sound.play()
      # draw hearts
      if game_status == 1:
         draw_hearts()
        
      # draw level info
      level_img = font.render("Level: " + str(level), True, 'white')
      screen.blit(level_img, (20, SCREEN_HEIGHT - 50))  # bottom left corner

      if game_status == 7: # only two player
         # Score player 1 (bottom)
         score1_img = font.render("P1: " + str(player1_score), True, 'white')
         screen.blit(score1_img, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))
         # Score player 2 (top)
         score2_img = font.render("P2: " + str(player2_score), True, 'white')
         screen.blit(score2_img, (SCREEN_WIDTH - 150, 10))
         screen.blit(paddle2_img, (paddle2_x, paddle2_y))


      if game_status == 1:  # only singleplayer
         score_img = font.render("Score: " + str(singleplayer_score), True, 'white')
         screen.blit(score_img, (10, 10))  # top left

   #
   # info screen
   #

   elif game_status == 2: # information screen
      # button for going back to the homesceen    
      
      temp_img = orange_button_img.copy()
      button_img_text = (font.render('Back', True, 'white')) # makes the button text into an img
      temp_img.blit(button_img_text, ((temp_img.get_width() - button_img_text.get_width()) // 2, (temp_img.get_height() - button_img_text.get_height()) // 2)) # draws the text img onto the middle of the 'temp_img'
      screen.blit(temp_img, ((SCREEN_WIDTH - temp_img.get_width()) // 2, (SCREEN_HEIGHT - temp_img.get_height()) - 50)) # places the button in the middlebottom of the screen

      game_status_msg = '' 

       # Split the information text into two columns
      split_index = len(informationtext) // 2
      left_column = informationtext[:split_index]
      right_column = informationtext[split_index:]
        
       # Draw left column
      textheight = 30  # starting Y position
      for line in left_column:
         if line == " ":  # handles blank lines
            textheight += 15
            continue
         
         # uses different colors for headers
         text_color = 'orange' if line.endswith(":") and not line.startswith(" ") else 'white'
         line_surface = font_smallest.render(line, True, text_color)
         screen.blit(line_surface, (50, textheight))
         textheight += 25
         
      # Draw right column
      textheight = 30  # recets Y position for right column
      for line in right_column:
        if line == " ":
            textheight += 15
            continue
        
        text_color = 'orange' if line.endswith(":") and not line.startswith(" ") else 'white'
        line_surface = font_smallest.render(line, True, text_color)
        screen.blit(line_surface, (SCREEN_WIDTH // 2 + 50, textheight))
        textheight += 25

      # user input handling for going back to the homescreen
      selected_button = 0
      pressed_button = handleMenuInputs(['Back'])
      if pressed_button == 'Back':
         # we want to go back to the old game status, but we also want to put the current game status in old_game_status
         temp_var = game_status
         game_status = old_game_status
         old_game_status = temp_var
 
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
      if musicIsInitialised and not musicIsPlaying: # only execute if music is working and is not playing already
            pygame.mixer.music.load(game_over_music)
            pygame.mixer.music.play(-1)
            musicIsPlaying = True
            if old_game_status == 1 and lives == 0:
               game_over_sound.play()

      if not highscore_checked:
            try:
               highscorefile = open("highscore.txt")
            except FileNotFoundError:
               highscore = 0 # if there is no highscore.txt file we say the highscore is 0
            else:
               highscore = int(highscorefile.read())
               highscorefile.close()
            highscore_checked = True
            if singleplayer_score > highscore: # we put this in here so we can say 'no' to saving our highscore while not triggering this the whole time
               add_highscore_mode = True

      if add_highscore_mode:
         if old_game_status == 1:  # if we come from single player
            final_score_img = font.render("Final Score: " + str(singleplayer_score), True, 'white')
            screen.blit(final_score_img, (SCREEN_WIDTH // 2 - final_score_img.get_width() // 2, 50))
            highscore_img = font.render('Current highscore: ' + str(highscore), True, 'white')
            screen.blit(highscore_img, (SCREEN_WIDTH // 2 - highscore_img.get_width() // 2, 100))
            screen.blit(savehighscore_text, (SCREEN_WIDTH // 2 - savehighscore_text.get_width() // 2, 150))
            temp_path = Path('highscore.txt')
            if not temp_path.exists(): # if the file does not exist yet, we warn the user that pressing 'yes' will create a file
               screen.blit(savehighscore_subtext, (SCREEN_WIDTH // 2 - savehighscore_subtext.get_width() // 2, 200))
            drawButtons(save_highscore_buttons, selected_button, columns=2)
            pressed_button = handleMenuInputs(save_highscore_buttons, columns=2)
            if pressed_button == 'yes':
               highscorefile = open("highscore.txt", "w")
               highscorefile.write(str(singleplayer_score))
               highscorefile.close()
               highscore = singleplayer_score
               add_highscore_mode = False
            elif pressed_button == 'no':
               add_highscore_mode = False

      else: # if we are not in add_highscore_mode
         if not two_player_mode:
            final_score_img = font.render("Final Score: " + str(singleplayer_score), True, 'white')
            screen.blit(final_score_img, (SCREEN_WIDTH // 2 - final_score_img.get_width() // 2, 50))
            highscore_img = font.render('Highscore: ' + str(highscore), True, 'white')
            screen.blit(highscore_img, (SCREEN_WIDTH // 2 - highscore_img.get_width() // 2, 100))
         
         drawButtons(game_over_screen_buttons, selected_button, columns = 2)
         pressed_button = handleMenuInputs(game_over_screen_buttons, columns = 2)
         if pressed_button != None:
            if pressed_button == 'save score':
               add_highscore_mode = True
            elif pressed_button == 'play again' and two_player_mode == True:
               old_game_status = game_status
               game_status = 7 # back to two player mode
            else:
               old_game_status = game_status
               game_status = GAME_STATUSES[pressed_button] # this sets the game status number to the number that is defined by the name on the selected button

   #
   # game paused screen
   #

   elif game_status == 5:
      game_status_msg = "game paused"

      drawButtons(pause_menu_buttons, selected_button)
      pressed_button = handleMenuInputs(pause_menu_buttons)
      if pressed_button != None:
         old_game_status = game_status
         if pressed_button == 'resume' and two_player_mode == True:
            game_status = 7 # back to two player mode
         else:
            game_status = GAME_STATUSES[pressed_button] # this sets the game status number to the number that is defined by the name on the selected button

      if button_cooldown_timer == 0:
         if keys[pygame.K_r] : # key r is down
            button_cooldown_timer = button_cooldown_ticks
            reset_delay_timer = RESET_DELAY         # pauses game if you play again after you paused
            old_game_status = game_status
            if two_player_mode == True:
               game_status = 7 # back to two player mode
            else:
               game_status = 1 # back to single player mode
      else:
         button_cooldown_timer -=1

      if game_status == GAME_STATUSES["breakout"]: # if the game is reset using the 'r' key of 'resume' is selected from pause menu
         button_cooldown_timer = button_cooldown_ticks
         reset_delay_timer = RESET_DELAY         # pauses game if you play again after you paused

   #
   # settings screen
   #
   elif game_status == 6:
      drawButtons(settings_buttons, selected_button)
      if volume_change_mode:
            game_status_msg = 'volume is set to: ' + str(volume) + ', change it using \'w\' and \'s\'.'
            volume_change = keys[pygame.K_w] - keys[pygame.K_s]
            volume += volume_change
            volume = max(0, min(volume, 100))
            pygame.mixer.music.set_volume(volume/100)  # change volume so you can here the change directly
            pressed_button = handleMenuInputs(['volume'])
            if pressed_button == 'volume':
               for sound in all_sounds:
                  sound.set_volume(volume/100)
               volume_change_mode = False
               game_status_msg = 'volume set to: ' + str(volume)
      else:
         pressed_button = handleMenuInputs(settings_buttons)
         if pressed_button == 'Back':
            # we want to go back to the old game status, but we also want to put the current game status in old_game_status
            temp_var = game_status
            game_status = old_game_status
            old_game_status = temp_var
         elif pressed_button == 'no sound':
            game_status_msg = 'Sound is not working. Try restarting your game.'
         elif pressed_button == 'volume':
            volume_change_mode = True
   
   #
   # level select screen
   #
   elif game_status == 8:
      drawButtons(level_select_buttons, selected_button, columns = 4, color = 'red', color_from = max_level_playable)
      # we draw the buttons first in red and than the buttons of all the completed levels on top of it, so you see all th elevel but cant access all
      pressed_button = handleMenuInputs(level_select_buttons[:max_level_playable], columns = min(4, len(level_select_buttons[:max_level_playable])))
      if pressed_button != None:
         selected_button = 0
         level = int(pressed_button[-1]) # the last character of the string is the level number
         setBreakout(level)
         old_game_status = game_status
         game_status = GAME_STATUSES['breakout']



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
