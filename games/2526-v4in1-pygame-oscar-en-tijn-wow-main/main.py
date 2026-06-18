# BREAKOUT GAME 

# important imports
import pygame, time
import time
import random

# definitions 
# define global variables
game_started = False
game_status_msg = "Press SPACE to start"
brick_combo_msg = ""
game_score_msg_combo = ""
power_up_msg = ""
game_score_msg = ""
iples = ["SINGLE", "DOUBLE", "TRIPLE", "QUADRUPLE", "QUINTUPLE", "SEXTUPLE", "SEPTUPLE", "OCTUPLE", "NONUPLE", "DECUPLE", "UNDECUPLE", "DUODECUPLE", "TREDECUPLE", "QUATTUORDECUPLE", "QUINDECUPLE", "SEXDECUPLE", "SEPTENDECUPLE", "OCTODECUPLE", "NOVEMDECUPLE", "VIGINTUPLE", "UNVIGINTUPLE", "DUOVIGINTUPLE", "TREVIGINTUPLE", "QUATTUORVIGINTUPLE"]
brick_combo_counter = 0
brick_combo_total = 0
brick_hit_moment = 0
brick_combo_alpha = 255
brick_fade_alpha = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, ]
start_time = 0
first_timer_reset = False
background = pygame.image.load("background.jpg")
# define constants in capital letters
FPS = 40 # Frames Per Second
SCREEN_WIDTH = 1280 # screensize in x-direction in pixels
SCREEN_HEIGHT = 720 # screensize in y-direction in pixels
BALL_WIDTH = 20 # ballsize in x-direction in pixels
BALL_HEIGHT = 20 # ballsize in y-direction in pixels
PADDLE_WIDTH = 144 # the width of the paddle
PADDLE_HEIGHT = 32 # the height of the paddle
BRICK_WIDTH = 96 # the width of the bricks
BRICK_HEIGHT = 32 # the height of the bricks
SPECIAL_BRICK_WIDTH = 96 # the width of the special power-up brick
SPECIAL_BRICK_HEIGHT = 32 # the height of the special power-up brick
POWER_UP_WIDTH = 32 # the width of the falling power-up
POWER_UP_HEIGHT = 30.5 # the height of the falling power-up
PADDLE_ACCELERATION = 1.012 # how strong the paddle accelerates (increase to make acceleration stronger)
SLIDE_COEFFICIENT = 0.75 # how strong the paddle decelerates (decrease to make deceleration stronger)
MIN_Y_SPEED = 6 # minimum y speed of the ball where it can move up and down with
MAX_Y_SPEED = 12 # maximum y speed of the ball can where it move up and downwards with
MAX_X_SPEED = 15 # maximum x speed of the ball


# ball starts in random direction
ball_x = SCREEN_WIDTH / 2 # x-position of ball in pixels
if random.choice([1,2]) == 1:
   ball_speed_x = random.choice([5,6,7,8,9,10,11,11,12]) # speed of ball in x-direction in pixels per frame
else:
   ball_speed_x = random.choice([6,7,8,9,10,11,11,12]) * -1
ball_y = 110 + BRICK_HEIGHT # y-position of ball in pixels
ball_speed_y = 6 # speed of ball in y-direction in pixels per frame
paddle_x = (SCREEN_WIDTH / 2) - (PADDLE_WIDTH / 2) # Makes sure the paddle is placed in the middle upon initiating
paddle_y = SCREEN_HEIGHT - 80

paddle_speed = 0
ball_decrease = False
ball_increase = False

#brick declarations and positioning
brick_x1 = (SCREEN_WIDTH / 2) 
brick_y1 = 100
brick_x2 = (SCREEN_WIDTH / 2) - BRICK_WIDTH
brick_y2 = 100
brick_x3 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 2
brick_y3 = 100
brick_x4 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 3
brick_y4 = 100
brick_x5 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 4
brick_y5 = 100
brick_x6 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 5
brick_y6 = 100
brick_x7 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 6
brick_y7 = 100
brick_x8 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 1
brick_y8 = 100
brick_x9 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 2
brick_y9 = 100
brick_x10 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 3
brick_y10 = 100
brick_x11 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 4
brick_y11 = 100
brick_x12 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 5
brick_y12 = 100
brick_x13 = (SCREEN_WIDTH / 2) 
brick_y13 = 100 - BRICK_HEIGHT
brick_x14 = (SCREEN_WIDTH / 2) - BRICK_WIDTH
brick_y14 = 100 - BRICK_HEIGHT
brick_x15 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 2
brick_y15 = 100 - BRICK_HEIGHT
brick_x16 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 3
brick_y16 = 100 - BRICK_HEIGHT
brick_x17 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 4
brick_y17 = 100 - BRICK_HEIGHT
brick_x18 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 5
brick_y18 = 100 - BRICK_HEIGHT
brick_x19 = (SCREEN_WIDTH / 2) - BRICK_WIDTH * 6
brick_y19 = 100 - BRICK_HEIGHT
brick_x20 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 1
brick_y20 = 100 - BRICK_HEIGHT
brick_x21 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 2
brick_y21 = 100 - BRICK_HEIGHT
brick_x22 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 3
brick_y22 = 100 - BRICK_HEIGHT
brick_x23 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 4
brick_y23 = 100 - BRICK_HEIGHT
brick_x24 = (SCREEN_WIDTH / 2) + BRICK_WIDTH * 5
brick_y24 = 100 - BRICK_HEIGHT
bricks_x = [brick_x1, brick_x2, brick_x3, brick_x4, brick_x5, brick_x6, brick_x7, brick_x8, brick_x9, brick_x10, brick_x11, brick_x12, brick_x13, brick_x14, brick_x15, brick_x16, brick_x17, brick_x18, brick_x19, brick_x20, brick_x21, brick_x22, brick_x23, brick_x24]
bricks_y = [brick_y1, brick_y2, brick_y3, brick_y4, brick_y5, brick_y6, brick_y7, brick_y8, brick_y9, brick_y10, brick_y11, brick_y12, brick_y13, brick_y14, brick_y15, brick_y16, brick_y17, brick_y18, brick_y19, brick_y20, brick_y21, brick_y22, brick_y23, brick_y24]
brick_status = []
for i in range(24):
   brick_status.append("full")
drawn_bricks = 0
brick_colors = [(772, 390, 384, 128), (0, 130, 384, 128), (0, 390, 384, 128), (772, 260, 384, 128), (772, 0, 384, 128), (386, 650, 384, 128), (386, 390, 384, 128), (386, 130, 384, 128), (772, 520, 384, 128), (386, 780, 384, 128)] #list of all the brick-colors which is used to randomize the bricks
brick_colors_cracked = [(0, 0, 384, 128), (0, 260, 384, 128), (0, 520, 384, 128), (772, 130, 384, 128), (772, 650, 384, 128), (386, 520, 384, 128), (386, 260, 384, 128), (386, 0, 384, 128), (0, 650, 384, 128), (0, 780, 384, 128)]
random_brick_colors = []
for i in range(1,len(bricks_x) + 1):
   random_brick_colors.append(random.choice(brick_colors)) # random brick color

#power up variables
power_up = False
power_up_moment = 0
power_up_x = []
power_up_y = []
power_up_costume = (772, 846, 64, 61)
drop_started = []
power_costumes = []

# init game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# set and load fonts and spritesheet
win_lose = pygame.font.Font("PressStart2P-Regular.ttf", 50)
brick_combo = pygame.font.Font("PressStart2P-Regular.ttf", 25)
game_score = pygame.font.Font("PressStart2P-Regular.ttf", 25)
power_up_font = pygame.font.Font("PressStart2P-Regular.ttf", 35)
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()  
# read spritesheet containing all images
# convert_alpha increases speed of blit and keeps transparency of .png   

# create ball and paddle
# create empty image of 64 x 64 pixels, SRCALPHA supports transparency
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT)) 
# resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT

# create empty image of 243 x 64 pixels, SRCALPHA supports transparency
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image
# resize paddle_img from 243 x 64 pixels to PADDLE_WIDTH x PADDLE_HEIGHT

# game loop

print('mygame is running')
running = True
while running:
    screen.fill((0, 0, 0)) #clean screen

    # draw background
    background = pygame.transform.scale(background,(SCREEN_WIDTH, SCREEN_HEIGHT)) # resize image 
    background.set_alpha(165)
    screen.blit(background, (0, 0))
    
    # read events
    for event in pygame.event.get(): # read all events
        if event.type == pygame.QUIT:  # GUI is closed 
            running = False # end programm
    keys = pygame.key.get_pressed() # read which keys are down
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and game_started == True: # key a is down, doesn't work when game not started   
       if paddle_speed <= -11:
         paddle_speed *= PADDLE_ACCELERATION # accelerates paddle when you move it for longer
       else:
          if power_up == True: # checks if power up is active
             paddle_speed = -20 # moves paddle faster to the left when power up is active
          else: paddle_speed = -11 # moves paddle 1 frame to the left
       
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT])and game_started == True: # key d is down, doesn't work when game not starte
       if paddle_speed >= 11:
         paddle_speed *= PADDLE_ACCELERATION # accelerates paddle when you move it for longer
       else:
          if power_up == True: # checks if power up is active
             paddle_speed = 20 # moves paddle faster to the right when power up is active
          else:
             paddle_speed = 11 # moves paddle 1 frame to the right
    elif keys[pygame.K_SPACE] : # space-bar is down
       if game_started == False : 
          game_started = True # starts game
          game_status_msg = ""
          power_up = False
          ball_decrease = False
          ball_increase = False
          power_up_moment = 0
          start_time = time.perf_counter()
    else:
       paddle_speed *= SLIDE_COEFFICIENT # makes the paddle slip a bit when user lets go of keys

    #testmode makes dying impossible in case you have a skill-issue (remove # to enable) 
    #paddle_x = ball_x - (PADDLE_WIDTH / 2)

    # move everything

    # move ball
    if game_started == True : # checks if game has started
      if game_status_msg != "You Lose!" and game_status_msg != "You Win!": #checks if game hasn't ended yet
         ball_x = ball_x + ball_speed_x # moves ball to its next frame on x-axis
         ball_y = ball_y + ball_speed_y # moves ball to its next frame on y-axis

    # move paddle
    if game_started == True :
      if not paddle_x + PADDLE_WIDTH > SCREEN_WIDTH and paddle_speed < 0: # right edge
         if game_status_msg != "You Lose!" and game_status_msg != "You Win!": # checks if game hasn't ended yet
            paddle_x = paddle_x + paddle_speed # moves paddle to its next frame
      elif not (paddle_x * -1) > 0 and paddle_speed > 0: # left edge
         if game_status_msg != "You Lose!" and game_status_msg != "You Win!": # checks if game hasn't ended yet
            paddle_x = paddle_x + paddle_speed # moves  paddle to its next frame

    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH: # right edge
      paddle_speed = 0 # paddle stops at the edge
      paddle_x = SCREEN_WIDTH - PADDLE_WIDTH # paddle goes to the right edge
    elif (paddle_x * -1) > 0: # left edge
       paddle_speed = 0 # paddle stops at the edge
       paddle_x = 0 # paddle goes to the left edge

     # bounce ball

     # bounce ball against edges of screen
    if ball_x < 0 : # left edge
      ball_speed_x = abs(ball_speed_x) # positive x-speed = move right
    if ball_x + BALL_WIDTH > SCREEN_WIDTH: # right edge
      ball_speed_x = abs(ball_speed_x) * -1 # negative x-speed = move left
    if ball_y < 0 : # upper edge
      ball_speed_y = abs(ball_speed_y) # positive y-speed = move down
    if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: # lower edge
      ball_speed_y = abs(ball_speed_y) * -1 # negative y-speed = move up

    # ball touches top of paddle
    if ball_x + BALL_WIDTH >  paddle_x and ball_x + BALL_WIDTH  < paddle_x + PADDLE_WIDTH and ball_y + BALL_HEIGHT > paddle_y and ball_y  < paddle_y + PADDLE_HEIGHT : # checks when ball touches top of paddle
      ball_speed_y -= paddle_speed * 0.2 # adds momentum from paddle to the y-speed of the ball
      ball_speed_x += paddle_speed * 0.2 # adds momentum from paddle to the x-speed of the bal
      normalized_value = (ball_x - (paddle_x + (PADDLE_WIDTH / 2))) / (PADDLE_WIDTH / 2) # gives a number between -1 and 1 depending on how far off the ball hits the paddle from the center 
      if normalized_value * ball_speed_x <= 0: # left of paddle = negative value
         ball_speed_y -= abs(normalized_value * 6) # the closer the ball is to the edge of the paddle the slower it moves up 
         ball_speed_x += normalized_value * 5 # the closer the ball is to the edge of the paddle the more it bounces to that side
      elif normalized_value * ball_speed_x >= 0: # left of paddle left moving or right of paddle right moving
         ball_speed_y -= abs(normalized_value * 2) # the closer the ball is to the edge of the paddle the slower it moves up
         ball_speed_x += normalized_value * 4 # the closer the ball is to the edge of the paddle the more it bounces to that side
      ball_speed_y = abs(ball_speed_y) * -1 # ball bounces back
    
    # ball touches brick
    for i in range(0, len(bricks_x)) :
       if brick_status[i] != "pop": # if brick isn't gone:
         if ball_x + BALL_WIDTH > bricks_x[i] and ball_x + BALL_WIDTH < bricks_x[i] + BRICK_WIDTH and ball_y + BALL_HEIGHT > bricks_y[i] and ball_y < bricks_y[i] + BRICK_HEIGHT : # checks if ball touches brick
            if brick_status[i] == "full": 
               random_brick_colors[i] = brick_colors_cracked[brick_colors.index(random_brick_colors[i])] # changes the coordinates of the brick in the spritesheet to be cracked
               brick_status[i] = "cracked"
            elif brick_status[i] == "cracked":
               if random_brick_colors[i] == (0, 0, 384, 128): # if the brick was a special power-up brick
                  drop_started.append("True") 
                  power_up_x.append(ball_x)
                  power_up_y.append(ball_y)
                  power_costumes.append(power_up_costume)
                  # add some values to lists necessary for the power-up
               brick_status[i] = "pop"
               brick_hit_moment = time.perf_counter() # captures the time the brick was destroyed, so the combo knows how long it has been since the last brick popped

               # brick combo increases
               if not time.perf_counter() - brick_hit_moment > 3: # checks if it has been less than 3 seconds since the last brick popped
                  brick_combo_counter += 1 # increases combo
                  brick_combo_total += 1 # increases combo
                  brick_combo_alpha = 255 # naturally, the fading effect of the brick combo message starts with full opacity
                  brick_combo_img = brick_combo.render(brick_combo_msg, False, (255,255, 0)) # load the brick combo font
                  brick_combo_img.set_alpha(brick_combo_alpha) # give the brick combo message the right opacity
                  brick_combo_msg = "COMBO: " + str(brick_combo_counter) + " " + iples[brick_combo_counter - 1] # makes sure the correct combo gets drawn

            # print in terminal, mainly for testing purposes
            print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))

            # ball bounces correctly from bricks
            if ball_speed_y > 0 and ball_y < bricks_y[i] :
               ball_speed_y = abs(ball_speed_y) *-1 #ball bounces up
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT: 
               ball_speed_y = abs(ball_speed_y) #ball bouncces down
            elif ball_speed_x > 0 and ball_x < bricks_x[i] :
               ball_speed_x = abs(ball_speed_x) *-1#ball bounces to left
               ball_x += ball_speed_x
               ball_y += ball_speed_y
            elif ball_speed_x < 0 and ball_x > bricks_x[i] :
               ball_speed_x = abs(ball_speed_x) #ball bounces to right 
               ball_x += ball_speed_x
               ball_y += ball_speed_y

    # brick combo goes away
    if time.perf_counter() - brick_hit_moment > 3.5: # if it has been too long since the last brick has been popped
      if brick_combo_alpha < 1:
         brick_combo_msg = ""
         brick_combo_alpha = 0 # sets brick visibility to 0
         brick_combo_counter = 0 # sets brick combo to 0
      else:
         brick_combo_alpha -= 2 # takes 128 frames = 3.2 seconds to fade away
    # in total, the brick_combo goes away in 3.5 + 3.2 = 6.7 seconds

    #handle power-ups
      if time.perf_counter() - power_up_moment > 15 and power_up == True and game_status_msg != "You Win!" and game_status_msg != "You Lose!": # if power up has been acrtive for 15 seconds
         power_up = False # turn off power-up after 15 seconds
         ball_increase = False # to make sure the ball doesn't eventually reach an infinte speed
         if ball_decrease == False: # checks if balspeed has not yet been decreased
            ball_speed_x /= 1.35 # decreases ball x speed after power up has ended
            ball_speed_y /= 1.35 # decreases ball y speed after power up has ended
            ball_decrease = True # to make sure the ball doesn't decrease even more and eventually reaches a speed of zero     
      
    for i in range(len(power_costumes) - 1, -1, -1): # negative values to reverse reading order to avoid popping issues
      if i < len(power_costumes) or power_up == True and game_status_msg != "You Lose!" and game_status_msg != "You Win!": # basically says "if power up is allowed to start dropping"
            if drop_started[i] == "True" and game_status_msg != "You Lose!" and game_status_msg != "You Win!": # speaks for itself
               power_up_y[i] += 2 # power up falls down
               if power_up_x[i] + POWER_UP_WIDTH >  paddle_x and power_up_x[i] + POWER_UP_WIDTH  < paddle_x + PADDLE_WIDTH and power_up_y[i] + POWER_UP_HEIGHT > paddle_y and power_up_y[i]  < paddle_y + PADDLE_HEIGHT: # if power up caught:
                  print("POWER_UPPED") # mainly for testing purposes
                  ball_decrease = False # so we can decrease the ball-speed later in the code
                  if ball_increase == False: # ball speed hasn't increased yet since power-upped
                     power_up_moment = time.perf_counter() # code now knows when the power up was caught, this is used to calculate when to stop the power up
                     ball_speed_x *= 1.35 # increases ball x speed when power up has started
                     ball_speed_y *= 1.35 # increases ball y speed when power up has started
                     ball_increase = True # makes sure the ball doesn't become infinitely fast
                     power_up_msg = "Fireball!" # screen should show that the power-up has been activated
                  power_costumes.pop(i) 
                  power_up_x.pop(i)
                  power_up_y.pop(i)
                  drop_started.pop(i)
                  # removes falling power up when caught
                  if power_up == True: # power up already was active
                     power_up_moment = time.perf_counter() # reset 15 second timer for power up
                     power_up_msg = "Fireball Refreshed" # as stated above, the power up is refreshed
                  power_up = True
               elif power_up_y[i] > SCREEN_HEIGHT - 5: # power up drops below screen
                  power_costumes.pop(i)
                  power_up_x.pop(i)
                  power_up_y.pop(i)
                  drop_started.pop(i)
                   # remove falling power up

    
    if time.perf_counter() - power_up_moment > 5 and game_status_msg != "You Win!" and game_status_msg != "You Lose!": # Delete power_up message after 2 seconds
         power_up_msg = ""     
    
    # handle collisions

    if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT : # if ball is under paddle
       ball_speed_y = 0 # y-speed ball = 0
       ball_speed_x = 0 # X-speed ball = 0
       if game_status_msg != "You Win!": # if you have won, you should not be able to lose
          game_status_msg = "You Lose!" # shows the player that they in fact have lost the game
       game_status_img = win_lose.render(game_status_msg, True, (152, 255, 152)) # loads the font of the msg that says you have lost
    elif brick_status.count("pop") == 24: # if all bricks are poppend and thus broken
       ball_speed_y = 0 # stop ball movement
       ball_speed_x = 0 # stop ball movement
       game_status_msg = "You Win!" # shows the player that they in fact have beaten the game
       game_status_img = win_lose.render(game_status_msg, True, (152, 255, 152)) # loads the font of the msg that says you have won

    
   
    # draw everything

    # DRAW MESSAGES

    # draw game status message
    game_status_img = win_lose.render(game_status_msg, False, (152, 255, 152)) # load font, color is mint green
    screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.get_width() / 2), SCREEN_HEIGHT / 2)) # show message at the center of the screen

    # draw brick combo message
    if brick_combo_counter <= 9:
       brick_combo = pygame.font.Font("PressStart2P-Regular.ttf", int(28 + (brick_combo_counter * 2) + ((brick_combo_alpha - 255) * float((28 + (brick_combo_counter * 2)) / 255)))) # brick_combo becomes larger as it increases, and smaller as it fades
    else:
       brick_combo = pygame.font.Font("PressStart2P-Regular.ttf", int(46 + ((brick_combo_alpha - 255) * float((28 + (brick_combo_counter * 2)) / 255)))) # from nonuple combos on, the brick_combo shouldn't increase or it'll get too big
    brick_combo_img = brick_combo.render(brick_combo_msg, False, (255, 255, 0)) # color is yellow
    brick_combo_img.set_alpha(brick_combo_alpha) # makes sure the variable for the opacity of the brick combo message actually does something
    screen.blit(brick_combo_img, ((SCREEN_WIDTH / 2) - (brick_combo_img.get_width() / 2), (SCREEN_HEIGHT / 2) - 100)) # draw message a bit above game_status_msg
    
    # draw score message
    if start_time != 0 and game_status_msg != "You Lose!" and game_status_msg != "You Win!": # if the game has started and the game has not ended
      game_score_msg = "" # clear the score
      game_score_msg_combo = str((brick_combo_counter ** 2) * 3) # score grows exponentioally for large brick-combos
      if (brick_status.count("pop") * 100) - (int((time.perf_counter() - start_time) * 5)) < 0: # if the score ends up being negative:
         game_score_msg = "00000" # then set it to zero
      else:
         game_score_msg += str(int(game_score_msg_combo) + int(brick_status.count("pop") * 100) - (int((time.perf_counter() - start_time) * 5)))
         # set score, score goes up for number of broken bricks, exponentially up for large brick-combos, but down for how long the game has been going for
      if brick_status.count("pop") == 1 and first_timer_reset == False: # if the first brick has just been broken
         start_time = time.perf_counter() # makes sure the clock fo how long the game is going for only starts ticking after the first broken brick
         first_timer_reset = True # this script must happen just once
      elif brick_status.count("pop") == 0: # if no bricks have been broken
         game_score_msg = "00000" # score is set to zero
      for i in range(0, 5 - len(game_score_msg)):
         game_score_msg = "0" + game_score_msg
         # makes sure the score is always 5 digits long
      game_score_msg = "SCORE: " + game_score_msg # implements the score into a message
    game_score_img = game_score.render(game_score_msg, True, (0,0, 255)) # load the font of the score in blue
    screen.blit(game_score_img, (SCREEN_WIDTH - (game_score_img.get_width() + 20) , 20)) # actually shows the score in the top-right corner of the screen

    # draw power up message
    power_up_msg_img = power_up_font.render(power_up_msg, False, (255, 165, 0)) # load power-up message font in orange
    screen.blit(power_up_msg_img, ((SCREEN_WIDTH / 2) - (power_up_msg_img.get_width() / 2), (SCREEN_HEIGHT / 2) + 100)) # actually draw the power-up message, a bit under the game_status_msg

    # draw ball
    screen.blit(ball_img, (ball_x, ball_y)) # draw ball at it's coordinates
    # draw paddle
    screen.blit(paddle_img, (paddle_x, paddle_y)) # draw paddle at it's coordinates
    
   
    # draw bricks
    drawn_bricks = 0 # counter for how many bricks have been drawn
    for i in range(len(bricks_x)): # how many bricks there are left
      if drawn_bricks < len(bricks_x): # if there are still bricks to draw
         if brick_status[i] != "pop": # if the brick is not broken yet
            brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
            brick_img.blit(spritesheet, (0, 0), random_brick_colors[i]) # copy part of sheet to image
            brick_img = pygame.transform.scale(brick_img,(BRICK_WIDTH, BRICK_HEIGHT)) # resize image  
            screen.blit(brick_img, (bricks_x[i], bricks_y[i])) # draw the brick at it's right place
            drawn_bricks += 1 # a bricks has been drawn, so add one to the counter
         elif brick_status[i] == "pop" and brick_fade_alpha[i] <= 255 and not brick_fade_alpha[i] < 1: # if the bricks is fading away:
            brick_img = pygame.Surface((384, 128), pygame.SRCALPHA) # create new image
            brick_img.blit(spritesheet, (0, 0), random_brick_colors[i]) # copy part of sheet to image
            brick_img = pygame.transform.scale(brick_img,(BRICK_WIDTH, BRICK_HEIGHT)) # resize image  
            brick_img.set_alpha(brick_fade_alpha[i]) # give the brick the right opacity
            brick_fade_alpha[i] -= 7 # change the brick's opacity
            drawn_bricks += 1 # a brick has been drawn, so add one to the counter
            screen.blit(brick_img, (bricks_x[i], bricks_y[i])) # draw the brick at it's right place
            if brick_fade_alpha[i] < 0: 
               brick_fade_alpha[i] = 0
               # the alpha should not be negative

    # normal and custom power-up costumes for the ball and the paddle

    # create empty image of 243 x 64 pixels, SRCALPHA supports transparency
    paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) # create new image
    if power_up == True:
      paddle_img.blit(spritesheet, (0, 0), (1262, 726, 243, 64))  # fireball paddle # copy part of sheet to image
    else:
      paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))  # copy part of sheet to image
    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) # resize image  

    # create empty image of 64 x 64 pixels, SRCALPHA supports transparency
    ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
    if power_up == True:
      ball_img.blit(spritesheet, (0, 0), (1467, 652, 64, 64)) # fireball # copy part of sheet to image
    else:
      ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64)) # copy part of sheet to image
    # resize ball_img from 64 x 64 pixels to BALL_WIDTH x BALL_HEIGHT
    ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))    
         
    # draw the star from the power-up
    for i in range(0, len(power_costumes)): 
         if drop_started[i] == "True": # speaks for itself
            # create empty image of 64 x 61 pixels, SRCALPHA supports transparency
            power_up_img = pygame.Surface((64, 61), pygame.SRCALPHA) 
            power_up_img.blit(spritesheet, (0, 0), (power_costumes[i]))  # copy part of sheet to image
            power_up_img = pygame.transform.scale(power_up_img, (POWER_UP_WIDTH, POWER_UP_HEIGHT)) # resize image
            screen.blit(power_up_img, (power_up_x[i], power_up_y[i])) # actually draw the star at it's right place
    
    # minimum and maximum ball speed

    # ball doesn't go below minimum y speed
    if abs(ball_speed_y) < MIN_Y_SPEED: 
       if ball_speed_y < 0: # when moving up
          if game_status_msg != "You Lose!":
             ball_speed_y = MIN_Y_SPEED * -1 # negative because ball is moving up
       else: # when moving down
          if game_status_msg != "You Lose!":  
             ball_speed_y = MIN_Y_SPEED # speed becomes minimal

    # ball doesn't exceed maximum x speed
    if abs(ball_speed_x) > MAX_X_SPEED:
       if ball_speed_x < 0: # when moving left
          if game_status_msg != "You Lose!":
             ball_speed_x = MAX_X_SPEED * -1 # negative because ball is moving left
       else:
          if game_status_msg != "You Lose!": # when moving right
             ball_speed_x = MAX_X_SPEED # speed becomes maximal
    # ball doesn't exceed maximum y speed
    if power_up == True: # the maximum speed is a bit higher when a power up is active
      if abs(ball_speed_y) > MAX_Y_SPEED * 1.35: # maximum y speed increased when power up is active
         if ball_speed_y < 0: # when moving up
            if game_status_msg != "You Lose!":
               ball_speed_y = MAX_Y_SPEED * -1.35 # negative because ball is moving up
         else: # when moving down
            if game_status_msg != "You Lose!":
               ball_speed_y = MAX_Y_SPEED * 1.35 # speed becomes maximal
    else: 
      if abs(ball_speed_y) > MAX_Y_SPEED:
         if ball_speed_y < 0: # when moving up
            if game_status_msg != "You Lose!":
               ball_speed_y = MAX_Y_SPEED * -1 # negative because ball is moving up
         else: # when moving down
            if game_status_msg != "You Lose!":
               ball_speed_y = MAX_Y_SPEED # speed becomes maximal

    
    # show screen
    pygame.display.flip() 

    # wait until next frame

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')