#
# BREAKOUT GAME 
#

import pygame, time
import random
import os


#
# definitions 
#

FPS = 30 # Frames Per Second
SCREEN_WIDTH = 1280 # screensize in x-direction in pixels
SCREEN_HEIGHT = 720 # screensize in y-direction in pixels
BALL_WIDTH = 16 # ballsize in x-direction in pixels
BALL_HEIGHT = 16 # ballsize in y-direction in pixels
PADDLE_WIDTH = 144
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

balls = []
balls.append({
    "x": 640,
    "y": 300,
    "vx": 0,
    "vy": -0
})


max_speed_x = 10
max_speed_y = 10
paddle_x = 640
paddle_y = 600



totalbricks = 0
game_status_msg = ""
levels = []
powerups = []
current_level = 0

testmode = False
ballcontrol = False
paddle_left = False
paddle_right = False
paddle_collision = False
ball_launched = False
dev = False
color = 1


#levels


level_1 = [
"000000000000",
"000011110000",
"000111111000",
"000111111000",
"000011110000",
"000001100000",
"000000000000",
"000000000000",
]

level_2 = [
"000000000000",
"000111001110",
"000111001110",
"000000000000",
"000111001110",
"000111001110",
"000000000000",
"000000000000",
]


level_3 = [
"000000000000",
"000000000000",
"001111111100",
"001111111100",
"001111111100",
"000000000000",
"000000000000",
"000000000000",
]


level_4 = [
"000000000000",
"000111001110",
"000111001110",
"000000000000",
"000111001110",
"000111001110",
"000000000000",
"000000000000",
]

level_5 = [
"000111111000",
"000100001000",
"000101101000",
"000100001000",
"000101101000",
"000100001000",
"000111111000",
"000000000000",
]

level_6 = [
"001111111100",
"001000100100",
"001000100100",
"000000000000",
"001000100100",
"001000100100",
"001111111100",
"000000000000",
]

level_7 = [
"000001000000",
"000011100000",
"000111110000",
"001111111000",
"000111110000",
"000011100000",
"000001000000",
"000000000000",
]

level_8 = [
"011011011011",
"110110110110",
"011011011011",
"110110110110",
"011011011011",
"110110110110",
"000000000000",
"000000000000",
]

level_9 = [
"000110001100",
"000110001100",
"000110001100",
"000000000000",
"000110001100",
"000110001100",
"000110001100",
"000000000000",
]

level_10 = [
"001111111100",
"001000000100",
"001011110100",
"001010010100",
"001011110100",
"001000000100",
"001111111100",
"000000000000",
]

levels.append(level_1)
levels.append(level_2)
levels.append(level_3)
levels.append(level_4)
levels.append(level_5)
levels.append(level_6)
levels.append(level_7)
levels.append(level_8)
levels.append(level_9)
levels.append(level_10)
# Add more levels here as needed

# level maker
           
def leveler(list):
    brickss_x = []
    brickss_y = []
    counter = 0
    counterX = 0
    global totalbricks
    while counter < len(list):
       counterX = 0
       for i in list[counter]:
          if i == "0":
             counterX += 1  
          elif i == "1":
             brickss_y.append(100 + counter*32)
             brickss_x.append(64 + counterX* 96)
             counterX += 1
             totalbricks += 1
       counter += 1
    return brickss_x, brickss_y         

bricks_x, bricks_y = leveler(levels[current_level])




   

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images

#read spritesheet all images 
#convert_alpha increases spreed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA) #create image
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64)) #copy from spritesheet
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  #resize ball

paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA) #create image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64)) # copy from spritesheet
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT)) #resize paddle

powerup_img = pygame.Surface((64, 64), pygame.SRCALPHA)
powerup_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))
powerup_img = pygame.transform.scale(powerup_img, (32, 32))



broken_x = 0
broken_y = 0
normal_x = 772
normal_y = 390
broken = []
for i in range(0, len(bricks_x)):
   broken.append(1)



#
# game loop
#

print('mygame is running')
running = True
while running:
    
    # read events
    # 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            running = False 
    keys = pygame.key.get_pressed() 
            
    # 
    # move everything
    #

    # move ball
    if keys[pygame.K_w] and not ball_launched:
      balls[0]["vx"] = random.randint(3, 6)
      balls[0]["vy"] = -10
      ball_launched = True

    for ball in balls:
      ball["x"] += ball["vx"]
      ball["y"] += ball["vy"]

    # move powerups
    for p in powerups:
       p["y"] += p["vy"]

    for p in powerups:
       if p["y"] > SCREEN_HEIGHT:
        powerups.remove(p)

      
          

    # bounce ball
    for ball in balls:
    # wall bounce
      if ball["x"] < 0:
         ball["vx"] = abs(ball["vx"])

      if ball["x"] + BALL_WIDTH > SCREEN_WIDTH:
         ball["vx"] *= -1

      if ball["y"] < 0:
         ball["vy"] = abs(ball["vy"])


    #end game
    balls = [b for b in balls if b["y"] < SCREEN_HEIGHT]

    if len(balls) == 0: 
      ball["vy"] = 0 
      ball["vx"] = 0
      game_status_msg = "You lost!"
      
   
    # dev

   #  if keys[pygame.K_d] and keys[pygame.K_e] and keys[pygame.K_v]: dev = True

   #  if keys[pygame.K_o] and ball["vy"] < 40 and ball["vy"] > -40: ball["vy"] = -50
   #  if keys[pygame.K_o] and ball["vy"] == 50 or ball["vy"]  -50: ball["vy"] = -10

   #  if keys[pygame.K_p] and PADDLE_WIDTH != SCREEN_WIDTH: PADDLE_WIDTH = SCREEN_WIDTH
   #  if keys[pygame.K_p] and PADDLE_WIDTH == SCREEN_WIDTH: PADDLE_WIDTH = 144


    # paddle

    if keys[pygame.K_d] : 
       paddle_x += 20
       paddle_right = True
    else: paddle_right = False


    if keys[pygame.K_a] :
       paddle_x -= 20
       paddle_left = True 
    else: paddle_left = False

   
    if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
       paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
  
    if paddle_x < 0:
       paddle_x = 0

    for p in powerups[:]:
      if (p["x"] < paddle_x + PADDLE_WIDTH and p["x"] + 20 > paddle_x and p["y"] > paddle_y):
         spawn_balls(balls[0], 2)
         game_status_msg = "MULTIBALL!"
         powerups.remove(p)

    for ball in balls: 
      if ball["x"] + BALL_WIDTH > paddle_x and ball["x"] < paddle_x + PADDLE_WIDTH and ball["y"] + BALL_HEIGHT > paddle_y and ball["y"] < paddle_y + PADDLE_HEIGHT:
         paddle_collision = True
         
      if paddle_collision == True:
         if paddle_right == True:
            ball["vx"] = max_speed_x
            ball["vy"] = ball["vy"] * -1
            paddle_collision = False
            paddle_right = False
         elif paddle_left == True:
            ball["vx"] = max_speed_x * -1
            ball["vy"] = ball["vy"] * -1
            paddle_collision = False
            paddle_left = False
         elif paddle_left == False and paddle_right == False:
            direction = random.randint(1,2)
            angle = random.randint(1,10)
            ball["vx"] = angle
            if direction == 1 : 
               ball["vx"] = ball["vx"] * -1
               ball["vy"] = ball["vy"] * -1
               paddle_collision = False
            else:
               ball["vy"] = ball["vy"] * -1
               paddle_collision = False
      
      


    if keys[pygame.K_r] : os.execl(sys.executable, sys.executable, *sys.argv)


   #  if keys[pygame.K_x] and ballcontrol == True:
   #     ballcontrol = False
   #  elif keys[pygame.K_x] and ballcontrol == False:
   #     ballcontrol = True
    
   #  if ballcontrol == True:
   #     ball["vx"] = 0
   #     ball["vy"] = 0
   #     if keys[pygame.K_a] : ball["x"] -= 20
   #     if keys[pygame.K_d] : ball["x"] += 20
   #     if keys[pygame.K_w] : ball["y"] -= 20
   #     if keys[pygame.K_s] : ball["x"] += 20
    




       # break and powerup
    def hit_brick(i):
      global totalbricks
      if random.random() < 0.2:
         powerups.append({
               "x": bricks_x[i],
               "y": bricks_y[i],
               "vy": 3
         })

      if broken[i] == 1:
         broken[i] = 2
      else:
         bricks_x.pop(i)
         bricks_y.pop(i)
         broken.pop(i)
         totalbricks -= 1

    #multiple balls
    def spawn_balls(base_ball, count=2):
      for i in range(count):
         balls.append({
               "x": base_ball["x"],
               "y": base_ball["y"],
               "vx": random.choice([-6, -5, 5, 6]),
               "vy": -abs(base_ball["vy"])
         })

    #bricks

    for ball in balls:
      for i in range(0, len(bricks_x)):
         if ball["y"] + BALL_HEIGHT > bricks_y[i] and ball["y"] < bricks_y[i] + BRICK_HEIGHT and ball["x"] < bricks_x[i] + BRICK_WIDTH and ball["x"] + BALL_WIDTH > bricks_x[i]:
               print('brick touched at ball["x"] = ' + str(ball["x"]) + ' and ball["y"] = ' + str(ball["y"]))
               if ball["vy"] > 0 and ball["y"] < bricks_y[i]:
                  ball["vy"] = ball["vy"] *-1
                  hit_brick(i)
                  break
               elif ball["vy"] < 0 and ball["y"] + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                  ball["vy"] = ball["vy"] *-1
                  hit_brick(i)
                  break
               elif ball["vx"] > 0 and ball["x"] < bricks_x[i]:
                  ball["vx"] = ball["vx"] *-1
                  hit_brick(i)
                  break
               elif ball["vx"] < 0 and ball["x"] + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                  ball["vx"] = ball["vx"] *-1
                  hit_brick(i)
                  break




    #rounds
    if totalbricks == 0 and len(bricks_x) == 0 or keys[pygame.K_n] and dev == True:
       if current_level + 1 < len(levels):
           color = random.randint(1,5)
           current_level += 1
           totalbricks = 0
           bricks_x, bricks_y = leveler(levels[current_level])
           balls = [{
            "x": 640,
            "y": 350,
            "vx": 0,
            "vy": 0
           }]
           game_status_msg = "Level " + str(current_level + 1)
           ball_launched = False
           
           if color == 1:  
              # red
              normal_x = 772
              normal_y = 260
              broken_x = 772
              broken_y = 130 

           elif color == 2:
              # orange
              normal_x = 772
              normal_y = 0
              broken_x = 772
              broken_y = 650 

           elif color == 3:
              # yellow
              normal_x = 386
              normal_y = 390
              broken_x = 386
              broken_y = 260

           elif color == 4:  
              # green
              normal_x = 386
              normal_y = 130
              broken_x = 386
              broken_y = 0 

           elif color == 5:
            # light blue
              normal_x = 386
              normal_y = 650
              broken_x = 386
              broken_y = 520

           broken = []
           for i in range(0, len(bricks_x)):
             broken.append(1)

              
       else:
           game_status_msg = "You won!"
           ball["vy"] = 0
           ball["vx"] = 0
       

      

    if testmode == True:
       paddle_x = ball["x"] - (PADDLE_WIDTH / 2)

    # 
    # handle collisions
    #


    # 
    # draw everything
    #

    # clear screen
    screen.fill('orange') 

    # draw
  
    
    screen.blit(paddle_img, (paddle_x, paddle_y))

    for ball in balls:
      screen.blit(ball_img, (ball["x"], ball["y"]))
   
    for p in powerups:
      screen.blit(powerup_img, (p["x"], p["y"]))

    for i in range(len(bricks_x)):
      if broken[i] == 1:
         brick = (normal_x, normal_y, 384, 128)
      else:
         brick = (broken_x, broken_y, 384, 128)
   
    

      brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)
      brick_img.blit(spritesheet, (0, 0), brick)
      brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT))

      screen.blit(brick_img, (bricks_x[i], bricks_y[i]))
   
    
    # draw death message
    game_status_img = font.render(game_status_msg, True, 'white')
    screen.blit(game_status_img, ((SCREEN_WIDTH / 2) - (game_status_img.get_width() / 2), 50))
    
    
    
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
