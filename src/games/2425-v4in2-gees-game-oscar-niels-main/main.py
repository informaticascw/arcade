#
# BREAKOUT GAME
#


import pygame, time
import random
import math
#
# definitions


# define global variables
game_status_msg = ""


FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280   # Screen width (x-direction, in pixels)
SCREEN_HEIGHT = 720  # Screen height (y-direction, in pixels)
BALL_WIDTH = 16  # Ball width (x-direction, in pixels)
BALL_HEIGHT = 16  # Ball height (y-direction, in pixels)
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
HEARTS_WIDTH = 32
HEARTS_HEIGHT =29
hearts = 3
STAR_WIDTH = 32
STAR_HEIGHT = 32
game_started = False
running = False
ball_y = 500 # Determines ball position on the y-direction
ball_speed_y = 8 # Determines ball speed on the y-direction
min_ball_speed_y = 2
ball_x = 500 # Determines ball position on the x-direction
ball_speed_x = 0 # Determines ball speed on the x-direction
BALL_MIDDLE = BALL_WIDTH / 2 + ball_x
ball_damage = 1


paddle_x = 500
paddle_y = 620
paddle_speed = 10
PADDLE_MIDDLE = PADDLE_WIDTH / 2 + paddle_x
paddle_animation = []

use_background_image = False
use_cat_ball = False

hearts_x = [
  0, 40, 80
]
hearts_y = SCREEN_HEIGHT - HEARTS_HEIGHT

score_y = SCREEN_HEIGHT - PADDLE_HEIGHT
score_x = SCREEN_WIDTH - PADDLE_WIDTH

star_x = []
star_y = []
star_delete = []
starChance = 0

powerup_chance = 0
powerup = False
powerup_duration = 0
# fast, slow, long, short, ball up


bricksLocations_x = [771, 772, 385, 386, 772, 0]
bricksLocations_y = [259, 0, 390, 130, 390, 390]
brick_colors = []
# red, orange, yellow, green, blue, purple

brick_health_lookup = [1, 2, 3, 4, 5, 6]
bricks_health= []
current_level_index = 0


#levels + blokken
levels = [
   [ # level 1
         [2,2,1,1,1,1,1,1,1,1,2,2],
         [2,2,1,1,1,0,0,1,1,1,2,2],
         [1,1,1,1,0,0,0,0,1,1,1,1],
         [1,1,1,0,0,0,0,0,0,1,1,1],
         [1,1,0,0,0,0,0,0,0,0,1,1],
         [1,0,0,0,0,0,0,0,0,0,0,1]
   ],
   [  # level 2
         [1,1,1,1,1,1,1,1,1,1,1,1],
         [2,2,2,2,2,4,4,2,2,2,2,2],
         [0,0,2,2,2,3,3,2,2,2,0,0],
         [0,2,1,1,1,1,1,1,1,1,2,0],
         [0,0,3,3,3,1,1,3,3,3,0,0],
         [0,0,0,0,0,1,1,0,0,0,0,0]
   ],
   [  # level 3
         [1,1,1,3,3,3,3,3,3,1,1,1],
         [1,4,4,3,4,4,4,4,3,4,4,1],
         [1,4,5,3,4,6,6,4,3,5,4,1],
         [2,4,4,3,4,4,4,4,3,4,4,2],
         [2,2,3,3,4,4,4,4,3,3,2,2],
         [0,2,2,3,3,3,3,3,3,2,2,0]
   ]
]

def loadLevel(index):
    global bricks_x, bricks_y, bricks_color_indices, bricks_health
    bricks_x = []
    bricks_y = []
    bricks_color_indices = []
    bricks_health = []

    level = levels[index]
    for row_index, row in enumerate(level):
        for col_index, cell in enumerate(row):
            if cell != 0:
                x = col_index * (BRICK_WIDTH + 8) + 10
                y = row_index * (BRICK_HEIGHT + 8) + 32
                bricks_x.append(x)
                bricks_y.append(y)
                bricks_color_indices.append(cell - 1)
                bricks_health.append(cell) 


loadLevel(current_level_index)

#
# Running the game
#


pygame.init()
font = pygame.font.SysFont('default', 64)  # Chooses which font should be used
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)  # Screen display (width, height)
fps_clock = pygame.time.Clock()  # Keeps track of time


# Read images


spritesheet = pygame.image.load('Breakout_Tile_Free_Cat.png').convert_alpha()  

catless_spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()

achtergrond = pygame.image.load('super coole kat 2.0.jpg').convert_alpha()
                                                                         
# poesBal                                                  
cat_ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
cat_ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
cat_ball_img = pygame.transform.scale(cat_ball_img, (BALL_WIDTH, BALL_HEIGHT))


# nietPoesBal
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
ball_img.blit(catless_spritesheet, (0, 0), (1403, 652, 64, 64))
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))


heart_img = pygame.Surface((64,58), pygame.SRCALPHA)
heart_img.blit(spritesheet, (0,0), (1637, 652, 64, 58))
heart_img = pygame.transform.scale(heart_img, (HEARTS_WIDTH, HEARTS_HEIGHT))

star_img = pygame.Surface((64, 61), pygame.SRCALPHA) 
star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61)) 
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))

paddle_img_1 = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img_1.blit(spritesheet, (0, 0), (1158, 462, 243, 64))
paddle_img_1 = pygame.transform.scale(paddle_img_1, (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle_animation.append(paddle_img_1)

paddle_img_2 = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img_2.blit(spritesheet, (0, 0), (1158, 528, 243, 64))
paddle_img_2 = pygame.transform.scale(paddle_img_2, (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle_animation.append(paddle_img_2)

paddle_img_3 = pygame.Surface((243, 64), pygame.SRCALPHA)
paddle_img_3.blit(spritesheet, (0, 0), (1158, 594, 243, 64))
paddle_img_3 = pygame.transform.scale(paddle_img_3, (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle_animation.append(paddle_img_3)

paddle_wide = pygame.Surface((347, 64), pygame.SRCALPHA)
paddle_wide.blit(spritesheet, (0, 0), (0, 910, 347, 64))
paddle_wide = pygame.transform.scale(paddle_wide, (200, PADDLE_HEIGHT))

paddle_narrow = pygame.Surface((115, 64), pygame.SRCALPHA)
paddle_narrow.blit(spritesheet, (0, 0), (1574, 912, 115, 64))
paddle_narrow = pygame.transform.scale(paddle_narrow, (50, PADDLE_HEIGHT))

score_img = pygame.Surface((243, 64), pygame.SRCALPHA)
score_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))
score_img = pygame.transform.scale(score_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

slow_img = pygame.Surface((243, 64), pygame.SRCALPHA)
slow_img.blit(spritesheet, (0, 0), (1158, 66, 243, 64))
slow_img = pygame.transform.scale(slow_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

fast_img = pygame.Surface((243, 64), pygame.SRCALPHA)
fast_img.blit(spritesheet, (0, 0), (349, 910, 243, 64))
fast_img = pygame.transform.scale(fast_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

wide_img = pygame.Surface((243, 64), pygame.SRCALPHA)
wide_img.blit(spritesheet, (0, 0), (1158, 264, 243, 64))
wide_img = pygame.transform.scale(wide_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

narrow_img = pygame.Surface((243, 64), pygame.SRCALPHA)
narrow_img.blit(spritesheet, (0, 0), (1158, 198, 243, 64))
narrow_img = pygame.transform.scale(narrow_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

fire_img = pygame.Surface((243, 64), pygame.SRCALPHA)
fire_img.blit(spritesheet, (0, 0), (1262, 726, 243, 64))
fire_img = pygame.transform.scale(fire_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

for i in range(0,len(bricksLocations_x)):
  brick_img = pygame.Surface((385, 129), pygame.SRCALPHA)
  brick_img.blit(spritesheet, (0, 0), (bricksLocations_x[i], bricksLocations_y[i], 385, 129))
  brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
  brick_colors.append(brick_img)


# Animations
animation_index = 0
animation_timer = 0
animation_speed = 70

# Startmenu definitions
menu_options = ["Start game", "Options"]
menu_font = pygame.font.SysFont('Arial', 36)
# Option menu definitions
menu2_options = ["Poes", "Balpoes", "Go back"]
# Play button
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 50
menu1_x = (SCREEN_WIDTH - MENU_BUTTON_WIDTH)/2
menu_play_y = 200
menu_options_y = 400
button_color = (140,186,216)
selected_button_color = (200, 200, 10)
# Menu loop
menu_active = True
current_option = 0
while menu_active:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         menu_active = False


   keys = pygame.key.get_pressed()
   screen.fill((0,0,0))


# start button
   if current_option == 0:
      play_button_color = selected_button_color
   else:
      play_button_color = button_color
   play_rect = pygame.Rect(menu1_x, menu_play_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
   pygame.draw.rect(screen,play_button_color,play_rect)
   text_play = menu_font.render("Start game", True, (0,0,0))
   text_play_button = text_play.get_rect(center=play_rect.center)
   screen.blit(text_play, text_play_button)


# options button
   if current_option == 1:
      options_button_color = selected_button_color
   else:
      options_button_color = button_color
   options_rect = pygame.Rect(menu1_x, menu_options_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
   pygame.draw.rect(screen,options_button_color,options_rect)
   text_options = menu_font.render("Options", True, (0,0,0))
   text_options_button = text_play.get_rect(center=options_rect.center)
   screen.blit(text_options, text_options_button)


   pygame.display.flip()
# keys
   if keys[pygame.K_w]:
     current_option = max(0, current_option - 1)
   if keys[pygame.K_s]:
     current_option = min(len(menu_options) - 1, current_option + 1)
   if keys[pygame.K_z]:
     if current_option == 0:
        menu_active = False
     if current_option == 1:
        menu2_active = True
        submenu_option = 0
        # Options menu
        while menu2_active:
              for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                     menu_active = False
                     menu2_active = False
                  elif event.type == pygame.KEYDOWN:
                       if event.key == pygame.K_w:
                          submenu_option = max(0, submenu_option - 1)
                       elif event.key == pygame.K_s:
                            submenu_option = min(len(menu2_options) - 1, submenu_option + 1)
                       elif  event.key == pygame.K_z:
                             if submenu_option == 0:
                                use_background_image = not use_background_image
                             elif submenu_option == 1:
                                  use_cat_ball = not use_cat_ball
                             elif submenu_option == 2:
                                  menu2_active = False
                                  pygame.time.wait(200)


              keys = pygame.key.get_pressed()
              screen.fill((0,0,0))


              for i, option in enumerate(menu2_options):
                     if i == 0 and use_background_image:
                        color = (0, 200, 0)  
                     elif i == 1 and use_cat_ball:
                        color = (0, 200, 0)  
                     elif i == submenu_option:
                        color = selected_button_color
                     else:
                        color = button_color  
                     y_pos = menu_play_y + i * 100  
                     rect = pygame.Rect(menu1_x, y_pos, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
                     pygame.draw.rect(screen, color, rect)


                     text = menu_font.render(option, True, (0, 0, 0))
                     screen.blit(text, text.get_rect(center=rect.center))


              pygame.display.flip()



# Game loop

running = True
while running:


# read events
# move everything
# handle collisions
# draw everything
# wait until next frame


   # read events
   for event in pygame.event.get(): # read all events
       if event.type == pygame.QUIT:  # GUI is closed
           running = False # end programm
   keys = pygame.key.get_pressed() # read which keys are down
   


   current_time = pygame.time.get_ticks()
   if current_time - animation_timer > animation_speed:
     animation_index += 1
     animation_timer = current_time
   if animation_index >= len(paddle_animation):
       animation_index = 0

   #print(paddle_speed)

   #
   # move everything
 
   # move ball
   ball_x = ball_x + ball_speed_x
   ball_y = ball_y + ball_speed_y


   # bounce ball against wall of screen
   if ball_x < 0 : # left edge
     ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
   if ball_x + BALL_WIDTH > SCREEN_WIDTH: # right edge
     ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left


   if ball_y < 0 : # top of screen
     ball_speed_y = abs(ball_speed_y) # positive y-speed = move up
   if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
      ball_speed_y = -ball_speed_y
   if keys[pygame.K_d] :
      paddle_x = paddle_x + paddle_speed
   if keys[pygame.K_a] :
      paddle_x = paddle_x - paddle_speed


   #
   # handle collisions
  
   for i in range (0, len(bricks_x)):
      if (ball_x + BALL_WIDTH > bricks_x[i] and
       ball_x < bricks_x[i] + BRICK_WIDTH and
       ball_y + BALL_HEIGHT > bricks_y[i] and
       ball_y < bricks_y[i] + BRICK_HEIGHT):
       if (ball_speed_y > 0 and ball_y < bricks_y[i]):
         ball_speed_y *= -1
       elif (ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT):
         ball_speed_y *= -1
       elif (ball_speed_x < 0 and ball_x > bricks_x[i]):
         ball_speed_x *= -1
       elif (ball_speed_x > 0 and ball_x + BALL_WIDTH < bricks_x[i] + BRICK_WIDTH):
         ball_speed_x *= -1

       bricks_health[i] -= ball_damage
       if bricks_color_indices[i] > 0:
         bricks_color_indices[i] -= 1
       else:
         bricks_x.pop(i)
         bricks_y.pop(i)
         bricks_color_indices.pop(i)
         bricks_health.pop(i)
         if random.random() < 0.2:
            star_x.append(ball_x)
            star_y.append(ball_y)
            powerup_chance = random.randint(0,4)
       break
  
   if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
   if paddle_x <= 0:
      paddle_x = 0
 
   if ball_y + BALL_HEIGHT > SCREEN_HEIGHT:
     hearts = hearts - 1
     ball_y = 360
     ball_x = 640
     ball_speed_y = 8
     ball_speed_x = 0
     paddle_x = 600
     if hearts == 0: # if dead
        ball_speed_y = 0
        ball_speed_x = 0 
        game_status_msg = "You lost!"


   if (ball_x + BALL_WIDTH > paddle_x and
        ball_x < paddle_x + PADDLE_WIDTH and
        ball_y + BALL_HEIGHT > paddle_y and
        ball_y < paddle_y + PADDLE_HEIGHT):
         
          ball_y = paddle_y - BALL_HEIGHT


          incoming_angle = math.atan2(ball_speed_y, ball_speed_x)
          reflected_angle = -incoming_angle


          paddle_center = paddle_x + PADDLE_WIDTH / 2
          ball_center = ball_x + BALL_WIDTH / 2
          offset = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)


          reflected_angle += offset * math.radians(30)


          speed = math.hypot(ball_speed_x, ball_speed_y)
          ball_speed_x = speed * math.cos(reflected_angle)
          ball_speed_y = speed * math.sin(reflected_angle)
         
          if abs(ball_speed_y) < min_ball_speed_y:
             ball_speed_y = -min_ball_speed_y if ball_speed_y < 0 else min_ball_speed_y

   for i in range(0,len(star_x)):     
     if not (star_x[i] + STAR_WIDTH > paddle_x and
              star_x[i] < paddle_x + PADDLE_WIDTH and
              star_y[i] + STAR_HEIGHT > paddle_y and
              star_y[i] < paddle_y + PADDLE_HEIGHT or
              star_y[i] + STAR_HEIGHT > SCREEN_HEIGHT):
        star_y[i] += 10
     elif (star_x[i] + STAR_WIDTH > paddle_x and
              star_x[i] < paddle_x + PADDLE_WIDTH and
              star_y[i] + STAR_HEIGHT > paddle_y and
              star_y[i] < paddle_y + PADDLE_HEIGHT):
        star_delete.append(i)
        powerup = True
        if ball_speed_y > 0:
         speed_y_sign = 1  
        else:
          speed_y_sign = -1
        speed_y_mag = abs(ball_speed_y)
        powerup_duration = current_time + 10000 
        if powerup == True:
           if powerup_chance == 0 and paddle_speed < 15:
              paddle_speed = 15
           elif powerup_chance == 1 and paddle_speed > 5:
              paddle_speed = 5
           elif powerup_chance == 2:
              PADDLE_WIDTH = 200
           elif powerup_chance == 3:
              PADDLE_WIDTH = 50
           elif powerup_chance == 4:
              ball_damage = 2
              ball_speed_y = speed_y_sign * speed_y_mag * 1.5
            
     elif star_y[i] + STAR_HEIGHT > SCREEN_HEIGHT:
        star_delete.append(i)  
        
   if current_time >= powerup_duration:
         if powerup_chance == 0:
              paddle_speed = 10
         elif powerup_chance == 1:
              paddle_speed = 10
         elif powerup_chance == 2:
            PADDLE_WIDTH = 144
         elif powerup_chance == 3:
            PADDLE_WIDTH = 144
         elif powerup_chance == 4:
            ball_damage = 1
            ball_speed_y = speed_y_sign * speed_y_mag
         powerup = False

     
  
   for star in star_delete:
      star_x.pop(star)
      star_y.pop(star)
   star_delete = []


   #
   # draw everything
   #


   # clear screen
  
   if use_background_image == True:
      screen.blit(achtergrond,(0,0))
   else:
      screen.fill((0,0,0))


   # draw game status message
   game_status_img = font.render(game_status_msg, True, 'green')
   screen.blit(game_status_img, (SCREEN_WIDTH/2 - (game_status_img.get_width()/2), SCREEN_HEIGHT/2 - game_status_img.get_height()/2)) # (0, 0) is top left corner of screen
 
   # draw ball
   if use_cat_ball == True:
      screen.blit(cat_ball_img, (ball_x, ball_y))
   else:
      screen.blit(ball_img, (ball_x, ball_y))
   # draw paddle
   if PADDLE_WIDTH == 200:
      screen.blit(paddle_wide, (paddle_x, paddle_y))
   elif PADDLE_WIDTH == 50:
      screen.blit(paddle_narrow, (paddle_x, paddle_y))
   else:
      screen.blit(paddle_animation[animation_index], (paddle_x, paddle_y))
  
   # draw brick
   for i in range(len(bricks_x)):
     color_index = bricks_color_indices[i]
     screen.blit(brick_colors[color_index], (bricks_x[i], bricks_y[i]))
   # draw star
   for i in range(len(star_x)):
    screen.blit(star_img, (star_x[i], star_y[i]))


   # draw hearts
   for i in range (hearts):
      screen.blit(heart_img, (hearts_x[i], hearts_y))
   
   # draw score paddle
   if paddle_speed == 5: 
      screen.blit(slow_img, (score_x, score_y))
   elif paddle_speed == 15:
      screen.blit(fast_img, (score_x, score_y))
   elif PADDLE_WIDTH == 200:
      screen.blit(wide_img, (score_x, score_y))
   elif PADDLE_WIDTH == 50:
      screen.blit(narrow_img, (score_x, score_y))
   elif ball_damage == 2:
      screen.blit(fire_img, (score_x, score_y))
   else:
      screen.blit(score_img, (score_x, score_y))

   # if win
   if len(bricks_x) == 0:
    current_level_index += 1
    if current_level_index >= len(levels):
        game_status_msg = "You win!"
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        loadLevel(current_level_index)
        ball_x = 640
        ball_y = 360
        ball_speed_x = 0
        ball_speed_y = 8
        paddle_x = 500


   # show screen
   pygame.display.flip()


   #
   # wait until next frame
   #


   fps_clock.tick(FPS) # Sleep the remaining time of this frame


print('mygame stopt running')
