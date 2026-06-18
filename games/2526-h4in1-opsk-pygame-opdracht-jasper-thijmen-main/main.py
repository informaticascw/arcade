#
# BREAKOUT GAME 
#

import pygame, time, math, random

#
# definitions 
#
# define global variables
game_status_msg = ""
game_score_msg = 0

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32
STAR_WIDTH = 16
STAR_HEIGHT = 16

balls_x = [16]
ball_speed_x = [8]
balls_y = [200]
ball_speed_y = [8]
paddle_x = SCREEN_WIDTH/2 -72
paddle_y = 640
bricks_x = [96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152,96,192,288,384,480,576,672,768,864,960,1056,1152]
bricks_y = [64,64,64,64,64,64,64,64,64,64,64,64,96,96,96,96,96,96,96,96,96,96,96,96,128,128,128,128,128,128,128,128,128,128,128,128,160,160,160,160,160,160,160,160,160,160,160,160,192,192,192,192,192,192,192,192,192,192,192,192,192,224,224,224,224,224,224,224,224,224,224,224,224,256,256,256,256,256,256,256,256,256,256,256,256,288,288,288,288,288,288,288,288,288,288,288,288]
bricks_x2 = []
bricks_y2 = []
star_x = []
star_y = []
star_speed_y = 8
easy_mode = False

def plekkenBlokken():
   for i in range(0,31):
      welkBlok = random.randint(0,len(bricks_x)-1)
      print('Lus ' + str(i) + ',' + 'Waarde welkBlok: '+ str(welkBlok) + ', len lijst ' + str(len(bricks_x)))
      bricks_x2.append(bricks_x[welkBlok])
      bricks_y2.append(bricks_y[welkBlok])
      bricks_x.pop(welkBlok)
      bricks_y.pop(welkBlok)

 
#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  
paddle_img = pygame.Surface((243,64), pygame.SRCALPHA)
paddle_img.blit(spritesheet, (0,0), (1158, 396, 243, 64))
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
brick_img = pygame.Surface((384,128), pygame.SRCALPHA)
brick_img.blit(spritesheet, (0,0), (772,390,384,128))
brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))
star_img = pygame.Surface((64,61), pygame.SRCALPHA)
star_img.blit(spritesheet, (0,0), (772,846,64,61))
star_img = pygame.transform.scale(star_img, (STAR_WIDTH, STAR_HEIGHT))
#
# game loop
#
plekkenBlokken()

print('mygame is running')
running = True
while running:
    #
    # read events
    # 
   for event in pygame.event.get(): 
      if event.type == pygame.QUIT:  
         running = False 
      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_c:
            easy_mode = not easy_mode

   keys = pygame.key.get_pressed() 
     
    # 
    # move everything
    #
   if keys[pygame.K_d] : # key d is down
       paddle_x = paddle_x + 16
   if keys[pygame.K_a] :
       paddle_x = paddle_x - 16
   if paddle_x < 0:
       paddle_x = 0
   if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
   if easy_mode:
       paddle_x = balls_x[0] - 72
       

    # move ball
   for i in range(0, len(balls_x)):
      balls_x[i] = balls_x[i] + ball_speed_x[i]
      balls_y[i] = balls_y[i] + ball_speed_y[i]

   for i in range (0,len(star_y)):
       star_y[i] += star_speed_y

    # bounce ball
   for i in range (0, len(balls_x)):
      if balls_x[i] < 0 : 
         ball_speed_x[i] = abs(ball_speed_x[i]) 
      if balls_x[i] + BALL_WIDTH > SCREEN_WIDTH: 
         ball_speed_x[i] = abs(ball_speed_x[i]) * -1
      if balls_y[i] < 0 : 
         ball_speed_y[i] = abs(ball_speed_y[i]) 

    # 
    # handle collisions
    #
   for i in range(0,len(balls_x)):
      if balls_x[i] + BALL_WIDTH > paddle_x and balls_x[i] < paddle_x + PADDLE_WIDTH and balls_y[i] + BALL_HEIGHT > paddle_y and balls_y[i] < paddle_y + PADDLE_HEIGHT:
       angle = math.atan2(ball_speed_y[i],ball_speed_x[i])
       center = balls_x[i] + BALL_WIDTH/2 
       paddleCenter = paddle_x + PADDLE_WIDTH/2
       difference = center - paddleCenter
       angle -= difference * math.radians(75)
       ball_speed_x[i] = math.cos(angle) * 9
       ball_speed_y[i] = abs(math.sin(angle))*-9

   for i in range(len(balls_x)-1,-1,-1):
      if balls_y[i] > SCREEN_HEIGHT:
         balls_y.pop(i)
         balls_x.pop(i)
      if len(balls_x)==0 : 
       ball_speed_x[i] = 0 
       ball_speed_y[i] = 0
       game_status_msg = "You lost!"
   for i in range(0, len(balls_x)):
      if len(bricks_x2) == 0:
       ball_speed_x[i] = 0
       ball_speed_y[i] = 0
       game_status_msg = "You win!"

   for bi in range(len(bricks_x2)-1,-1,-1):
      for bx in range(len(balls_x)-1,-1,-1):
         if balls_x[bx] + BALL_WIDTH > bricks_x2[bi] and balls_x[bx] < bricks_x2[bi] + BRICK_WIDTH and balls_y[bx] + BALL_HEIGHT > bricks_y2[bi] and balls_y[bx] < bricks_y2[bi] + BRICK_HEIGHT:   
            print('brick touched at ball_x = ' + str(balls_x[bx]) + ' and ball_y = ' + str(balls_y[bx]))
            if (ball_speed_y[bx] > 0 and balls_y[bx] + BALL_HEIGHT > bricks_y2[bi]):
               ball_speed_y[bx] = abs(ball_speed_y[bx]) * -1
            elif (ball_speed_y[bx] < 0 and balls_y[bx] < bricks_y2[bi] + BRICK_HEIGHT):
               ball_speed_y[bx] = abs(ball_speed_y[bx])
            elif (ball_speed_x[bx] > 0 and balls_x[i] + BALL_HEIGHT > bricks_x2[bi]):
               ball_speed_x[bx] = abs(ball_speed_x[bx]) * -1
            elif (ball_speed_x[bx] < 0 and balls_x[bx]  < bricks_x2[bi] + BRICK_WIDTH):
               ball_speed_x[bx] = abs(ball_speed_x[bx])
            game_score_msg=game_score_msg +5
            ball_speed_x[bx] *= 1.05
            ball_speed_y[bx] *= 1.05
            sterJaNee = random.randint(0,2)
            if sterJaNee == 2:
               star_x.append(bricks_x2[bi] + BRICK_WIDTH /2 - 8)
               star_y.append(bricks_y2[bi] + BRICK_HEIGHT /2 - 8)
            bricks_x2.pop(bi)
            bricks_y2.pop(bi)
            break
         
   for i in range (0,len(star_x)):
       if star_x[i] + STAR_WIDTH > paddle_x and star_x[i] < paddle_x + PADDLE_WIDTH and star_y[i] + STAR_HEIGHT > paddle_y and star_y[i] < paddle_y + PADDLE_HEIGHT:
          game_score_msg = game_score_msg+10
          welkePowerup = random.randint(0,1)
          if welkePowerup == 0:
             balls_x.append(paddle_x +80)
             balls_y.append(paddle_y +16)
             ball_speed_x.append(0)
             ball_speed_y.append(-9)
          star_x.pop(i)
          star_y.pop(i)
          break





    # 
    # draw everything
    #
    

    # clear screen
   screen.fill('black') 

    # draw ball
   for i in range(0, len(balls_x)):
      screen.blit(ball_img, (balls_x[i], balls_y[i]))
      screen.blit(paddle_img, (paddle_x, paddle_y))
   for i in range (0, len(bricks_x2)):
      screen.blit(brick_img, (bricks_x2[i], bricks_y2[i]))
   for i in range (0, len(star_x)):
      screen.blit(star_img, (star_x[i], star_y[i]))
   game_score_img = font.render(str(game_score_msg), True, 'white')
   screen.blit(game_score_img, (0,0))
   # draw game status message
   game_status_img = font.render(game_status_msg, True, 'green')
   screen.blit(game_status_img, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) # (0, 0) is top left corner of screen

    # show screen
   pygame.display.flip() 


    # 
    # wait until next frame
    #

   fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
