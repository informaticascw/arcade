#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#


FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280  #size screen in x direction
SCREEN_HEIGHT = 720  #size screen in y direction
BALL_WIDTH = 16  #size ball in x direction
BALL_HEIGHT = 16  #size ball in y direction
PADDLE_WIDTH = 144 #size paddle in x direction
PADDLE_HEIGHT = 32 #size paddle in y direction
BRICK_WIDTH = 96 #size brick in x direction
BRICK_HEIGHT = 32 #size brick in y direction
BRICK_BREAK_WIDTH =  96
BRICK_BREAK_HEIGHT = 32
STAR_WIDTH = 32
STAR_HEIGHT = 30

ball_x = 0 # place ball on screen in x direction
ball_speed_x = 6 # constant speed of the ball in x direction
ball_y = 85 # place ball on screen in y direction
ball_speed_y = 8 #constant speed of the ball in y direction
paddle_x = SCREEN_WIDTH / 2 # place paddle in x directon
paddle_y = SCREEN_HEIGHT - 70 # place paddle in y direction
paddle_x2 = SCREEN_WIDTH / 2
paddle_y2 =  SCREEN_HEIGHT - 112 # place paddle in y direction
star_speed_y = 4
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

bricks_x = [30, 126, 222, 318, 414, 510, 606, 702, 798, 894, 990, 1086,
            30, 126, 222, 318, 414, 510, 606, 702, 798, 894, 990, 1086]
bricks_y = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]
bricks_break_x = [20, 116, 212, 308, 404, 500, 596, 692, 788, 884, 980, 1076,
            20, 116, 212, 308, 404, 500, 596, 692, 788, 884, 980, 1076]
bricks_break_y = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]
brick_state = [0] * len(bricks_x)
brick_broken = []
stars_x = []
stars_y = []

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
brick_img = pygame.Surface((386, 130), pygame.SRCALPHA)  
brick_img.blit(spritesheet, (0, 0), (386, 650, 384, 128))   
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
brick_break_img = pygame.Surface((386, 130), pygame.SRCALPHA)  
brick_break_img.blit(spritesheet, (0, 0), (386, 520, 384, 128))   
brick_break_img = pygame.transform.scale(brick_break_img, (BRICK_BREAK_WIDTH, BRICK_BREAK_HEIGHT))
star_img = pygame.Surface((64,61), pygame.SRCALPHA)
star_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))


#
# game loop
#
player2 = False
games_status = "INTRO"
print('mygame is running')
screen.fill('#00001C')
running = True  # makes it run always until running is made false
while running == True: 
    #
    # read events

    if games_status == "INTRO":
      game_begin = False
    if games_status == "INTRO" and game_begin == False:
      game_status_msg = "[q] for 1 player [e] for two"
      game_status_img = font.render(game_status_msg, True, 'green')
      screen.blit(game_status_img, (450,350))
      game_begin = True

    


    for event in pygame.event.get(): # return a dictionary of queued events
      if event.type == pygame.QUIT:  #when event is pygame.quit it does what is below
        running = False # stop the game
      keys = pygame.key.get_pressed() # reads which key is pressed

    if games_status == "INTRO":
      if keys[pygame.K_q]:
        games_status = "SPELEN"
      if keys[pygame.K_e]:
        player2 = True
      
        

    if games_status == "SPELEN" or player2 == True:
    # 
    # move everything
    #

    # move ball
      ball_x = ball_x + ball_speed_x # changing of the position of the ball in x direction
      ball_y = ball_y + ball_speed_y # changing of the postition of the ball in y direction
  	  
    #move star
      for i in range (0, len(stars_y)):
        stars_y[i] = stars_y[i] + star_speed_y
    

    # bounce ball
      if ball_x < 0 : 
        ball_speed_x = abs(ball_speed_x) # when ball hits the left side of the screen it bounces to the right
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 # when ball hits right side of the screen it bounces to the left
      if ball_y < 0 : 
        ball_speed_y = abs(ball_speed_y)  # when ball hits the top of the screen it bounces down
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
        ball_speed_y = abs(ball_speed_y) * -1 # when ball hits the bottom of the screen it bounces up

    # paddle movement
      if keys[pygame.K_d] : # key d is pressed
         paddle_x = paddle_x +20 # adds 10 to the x position of the paddle
      if keys[pygame.K_a] : # key a is pressed
        paddle_x = paddle_x - 20 # removes 10 to the x position of the paddle
      if player2 == True:
        if keys[pygame.K_j]:
         paddle_x2 = paddle_x2 - 20
        if keys[pygame.K_l]:
          paddle_x2 = paddle_x2 + 20
    # paddle stop at edge of the screen
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH # stops paddle on the right of the screen
      if paddle_x < 0 :
         paddle_x = -144 + PADDLE_WIDTH # stops the paddle on the left of the screen
      if player2 == True:
        if paddle_x2 + PADDLE_WIDTH > SCREEN_WIDTH:
          paddle_x2 = SCREEN_WIDTH - PADDLE_WIDTH # stops paddle on the right of the screen
        if paddle_x2 < 0 :
           paddle_x2 = -144 + PADDLE_WIDTH # stops the paddle on the left of the screen




    # 
    # handle collisions
      if (ball_x + BALL_WIDTH > paddle_x and
         ball_x < paddle_x + PADDLE_WIDTH and
         ball_y + BALL_HEIGHT > paddle_y and
          ball_y < paddle_y + PADDLE_HEIGHT): #  makes the ball bounce on the paddle
            if ball_speed_y < 32: 
             ball_speed_y = ball_speed_y *-1.1
            else:
              ball_speed_y = ball_speed_y * -1
      if player2 == True:
        if (ball_x + BALL_WIDTH > paddle_x2 and
         ball_x < paddle_x2 + PADDLE_WIDTH and
         ball_y + BALL_HEIGHT > paddle_y2 and
          ball_y < paddle_y2 + PADDLE_HEIGHT): #  makes the ball bounce on the paddle
            if ball_speed_y < 32: 
             ball_speed_y = ball_speed_y *-1.1
            else:
              ball_speed_y = ball_speed_y * -1

    
   
    
      for i in range(0, len(bricks_x)):
        if (ball_x + BALL_WIDTH > bricks_x[i] and
        ball_x < bricks_x[i] + BRICK_WIDTH and
        ball_y + BALL_HEIGHT > bricks_y[i] and
        ball_y < bricks_y[i] + BRICK_HEIGHT):
        
          if brick_state[i] == 0: 
            if ball_speed_y > 0 and ball_y + BALL_HEIGHT < bricks_y[i] + BRICK_HEIGHT:
                ball_speed_y *= -1  
            elif ball_speed_y < 0 and ball_y + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                ball_speed_y *= -1          
            elif ball_speed_x > 0 and ball_x + BALL_WIDTH < bricks_x[i] + BRICK_WIDTH:
                ball_speed_x *= -1  
            elif ball_speed_x < 0 and ball_x + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                ball_speed_x *= -1  
            brick_state[i] = 1 
          elif brick_state[i] == 1: 
            stars_x.append(bricks_x[i])
            stars_y.append(bricks_y[i])
            del bricks_x[i]
            del bricks_y[i]
            del brick_state[i]
          break

      for i in range (0, len(stars_x)):
          if (stars_x[i] + STAR_WIDTH > paddle_x and
        stars_x[i] < paddle_x + PADDLE_WIDTH and
        stars_y[i] + STAR_HEIGHT > paddle_y and
        stars_y[i] < paddle_y + PADDLE_HEIGHT):
           del stars_x[i]
           del stars_y[i]
           break
      if player2 == True:
        for i in range (0, len(stars_x)):
          if (stars_x[i] + STAR_WIDTH > paddle_x2 and
        stars_x[i] < paddle_x2 + PADDLE_WIDTH and
        stars_y[i] + STAR_HEIGHT > paddle_y2 and
        stars_y[i] < paddle_y2 + PADDLE_HEIGHT):
           del stars_x[i]
           del stars_y[i]
           break
         




    


      game_over = False

    # stop game
      if ball_y + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT and game_over == False: # when ball passes the paddle stops the game
       ball_speed_y = 0
       ball_speed_x = 0
       game_over = True


      if len(bricks_x) > 0 and game_over == False and ball_y > paddle_y + PADDLE_HEIGHT:  
       ball_speed_y = 0
       ball_speed_x = 0
       game_over = True
    
    
      if len(bricks_x) == 0 and game_over == False:
       game_status_msg = "You WON!"
       game_status_img = font.render(game_status_msg, True, 'green')
       screen.blit(game_status_img, (0,0))
       ball_speed_x = 0
       ball_speed_y = 0
       

      if game_over == True :
        game_status_msg = "You lost! press [r] to restart"
        game_status_img = font.render(game_status_msg, True, 'green')
        screen.blit(game_status_img, (0,0))

      if game_over == False and len(bricks_x) > 0:
        game_status_msg = "speel met [A] en [D] en [j] en [l] "
      

     



    
    

    # clear screen
      screen.fill('#00001C') # color of screen
    # 
    # draw everything
    #
      game_status_img = font.render(game_status_msg, True, 'green')
      screen.blit(game_status_img, (450,350))



    # draw ball
      screen.blit(ball_img, (ball_x, ball_y)) # puts the ball image on the position of the ball

    # draw plank
      screen.blit(paddle_img, (paddle_x, paddle_y)) # puts the paddle image on the position of the paddle
     
      if player2 == True:
        screen.blit(paddle_img, (paddle_x2, paddle_y2)) # puts the paddle image on the position of the paddle

    # draw brick


    for i in range(len(bricks_x)):
      if brick_state[i] == 0:
        screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
      elif brick_state[i] == 1:
        screen.blit(brick_break_img, (bricks_x[i], bricks_y[i]))


    # draw star
    

         
    for i in range(0, len(stars_x)):
        screen.blit(star_img, (stars_x[i], stars_y[i]))
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
