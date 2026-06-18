
# BREAKOUT GAME 

import pygame, time
import random
import xml.etree.ElementTree as ET

# Definitions 

FPS = 30            #frames Per Second
SCREEN_WIDTH = 1280 #width of screen in pixels
SCREEN_HEIGHT = 720 #height of screen in pixels
BALL_WIDTH = 16     #width of ball in pixels
BALL_HEIGHT = 16    #height of ball in pixels
PADDLE_WIDTH = 144  #width of paddle in pixels
PADDLE_HEIGHT = 32  #height of paddle in pixels
BRICK_WIDTH = 96    #width of brick in pixels
BRICK_HEIGHT = 32   #height of brick in pixels
LIVES_WIDTH = 32
LIVES_HEIGHT = 32
POWERUP_ALLTYPES = ["wide"]
WIDEPADDLE_WIDTH = 244

game_status="intro"
brick_x =[]
brick_y = []
brick_damage = []
brick_color = []

powerup_x = []
powerup_y = []
powerup_type = []

# level lay-outs
house_shape = [[0, 0, 0, 1, 0, 0, 0],  
               [0, 0, 1, 0, 1, 0, 0],
               [0, 1, 0, 0, 0, 1, 0],
               [1, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 0, 0, 1],
               [1, 0, 1, 1, 0, 1, 1],
               [1, 0, 0, 0, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1],]


skull_shape = [[0, 0, 1, 1, 1, 0, 0],  
               [0, 1, 1, 1, 1, 1, 0],
               [1, 1, 0, 1, 0, 1, 1],
               [1, 1, 0, 1, 0, 1, 1],
               [1, 1, 1, 1, 1, 1, 1],
               [0, 1, 1, 1, 1, 1, 0],
               [0, 0, 1, 0, 1, 0, 0],
               [0, 0, 1, 0, 1, 0, 0],
               [0, 0, 0, 1, 0, 0, 0],]


castle_shape =[[1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],  
               [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
               [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
               [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
               [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]
                
def makehouseshape(startX, startY, marginY, marginX):
    for row_index, row in enumerate(house_shape):
        for column_index, cell in enumerate(row):
          if cell == 1:
           x = startX + column_index * (BRICK_WIDTH + marginX)
           y = startY + row_index * (BRICK_HEIGHT + marginY)
           brick_x.append(x)
           brick_y.append(y)
           brick_damage.append(2)
           brick_color.append(random.randint(0, 9))
def makeskullshape(startX, startY, marginY, marginX):
    for row_index, row in enumerate(skull_shape):
        for column_index, cell in enumerate(row):
          if cell == 1:
           x = startX + column_index * (BRICK_WIDTH + marginX)
           y = startY + row_index * (BRICK_HEIGHT + marginY)
           brick_x.append(x)
           brick_y.append(y)
           brick_damage.append(2)
           brick_color.append(random.randint(0, 9))
def makecastleshape(startX, startY, marginY, marginX):
    for row_index, row in enumerate(castle_shape):
        for column_index, cell in enumerate(row):
          if cell == 1:
           x = startX + column_index * (BRICK_WIDTH + marginX)
           y = startY + row_index * (BRICK_HEIGHT + marginY)
           brick_x.append(x)
           brick_y.append(y)
           brick_damage.append(2)
           brick_color.append(random.randint(0, 9))
 
ball_speed_x = 6    #speed in the x-direction of the game

ball_speed_y = 6    #speed in the y-direction of the game
paddle_x = SCREEN_WIDTH / 2
paddle_y = SCREEN_HEIGHT - 100
paddle_speed = 10
game_status_msg = ""
lives = 3
currentLevel = 0
score = 0



# Init game
pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# Read images

#read spritesheet containing all images
#convert_alpha increases speed of blit and keeps transparency of .png
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()  
widePaddle_img = pygame.image.load('widePaddle.png').convert_alpha()

#cleate empty image
ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)
paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)
powerup_img = pygame.Surface((64, 61), pygame.SRCALPHA)

brick_img = []
brick_cracked_img = []

textures_X = []
textures_Y = []

#read xml
tree = ET.parse('Breakout_Tile_Free.xml')
root = tree.getroot()
for subtexture in root.findall('SubTexture'):
    x = subtexture.get('x')
    y = subtexture.get('y')
    
    # Append values to lists
    textures_X.append(int(x))
    textures_Y.append(int(y))


'''
Colors:
0: Dark blue
1: Light green
2: Purple
3: Red
4: Orange
5: Light blue
6: Yellow
7: Dark green
8: Grey
9: Brown
'''



#add the brick_img's to a list
for i in range(0, 10):
  brick_img.append(pygame.Surface((384, 128), pygame.SRCALPHA))
  brick_img[i].blit(spritesheet, (0, 0), (textures_X[2 * i], textures_Y[2 * i], 384, 128))
  brick_img[i] = pygame.transform.scale(brick_img[i], (BRICK_WIDTH, BRICK_HEIGHT))

for i in range(0, 10):
  brick_cracked_img.append(pygame.Surface((384, 128), pygame.SRCALPHA))
  brick_cracked_img[i].blit(spritesheet, (0, 0), (textures_X[2 * i + 1], textures_Y[2 * i + 1], 384, 128))
  brick_cracked_img[i] = pygame.transform.scale(brick_cracked_img[i], (BRICK_WIDTH, BRICK_HEIGHT))

lives_img = pygame.Surface((64, 58), pygame.SRCALPHA)

#copy image from spritesheet to image
paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))

#widePaddle_img.blit(widePaddle, (0, 0), (0, 0, 732, 128))
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))
lives_img.blit(spritesheet, (0, 0), (1637, 652 , 64, 58))
powerup_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))


ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  
paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
lives_img = pygame.transform.scale(lives_img, (LIVES_WIDTH, LIVES_HEIGHT))
powerup_img = pygame.transform.scale(powerup_img, (LIVES_WIDTH, LIVES_HEIGHT))
widePaddle_img = pygame.transform.scale(widePaddle_img, (WIDEPADDLE_WIDTH, PADDLE_HEIGHT))
# Game loop

print('mygame is running')
game_status_msg = "Speel met [A] en [D]"


# level lay-outs


def makeCustomShape(shape, startX, startY, marginY, marginX):
    for row_index in range(len(shape)):
        for column_index in range(len(shape[row_index])):
          if shape[row_index][column_index] == 1:
           x = startX + column_index * (BRICK_WIDTH + marginX)
           y = startY + row_index * (BRICK_HEIGHT + marginY)
           brick_x.append(x)
           brick_y.append(y)
           brick_damage.append(2)
           brick_color.append(random.randint(0, 9))


def makeBlocksGrid(yBlocks, xBlocks, xPos, yPos, marginY, marginX, brickDamage, color):
   currentY = yPos
   for row in range(yBlocks):
      currentX = xPos
      for block in range(xBlocks):
        brick_y.append(currentY)
        brick_x.append(currentX)
        brick_damage.append(brickDamage)
        if color == None:
          brick_color.append(random.randint(0, 9))
        else:
           brick_color.append(color)
        currentX += BRICK_WIDTH + marginX
      currentY += BRICK_HEIGHT + marginY
        


running = True
while running:
    # read events
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False 
    keys = pygame.key.get_pressed() 

    #explaination-screen
    if game_status == "intro":
      screen.fill('black')
      title = font.render("Welkom bij breakout!", True, "white")
      instructie1 = font.render("Gebruik [A] en [D] om te bewegen", True, "white")
      instructie2 = font.render("Druk op [Q] om te beginnen", True, "yellow")
      screen.blit(title, ((SCREEN_WIDTH - title.get_width()) / 2, 200))
      screen.blit(instructie1, ((SCREEN_WIDTH - instructie1.get_width()) / 2, 300))
      screen.blit(instructie2, ((SCREEN_WIDTH - instructie2.get_width()) / 2, 400))
      pygame.display.flip()
      
      if keys[pygame.K_q]:
        game_status = "playing"
      fps_clock.tick(FPS)
      continue

    if keys[pygame.K_d] :
       paddle_x = paddle_x + paddle_speed
    if keys[pygame.K_a] :
       paddle_x = paddle_x - paddle_speed
      
    #make next level
    totalLevels = 3
    currentLevel += 1
    if currentLevel % totalLevels == 1:
      makehouseshape(100, 100, 10, 10)
    elif currentLevel % totalLevels == 2:
      makeskullshape(250, 100, 10, 10)
      random_game_status = random.randint(1, 3)
      if random_game_status == 1:
        game_status_msg = "Goed gedaan!"
      elif random_game_status == 2:
        game_status_msg = "Ga zo door!"
      elif random_game_status == 3:
        game_status_msg = "lekker bezig!"
    elif currentLevel % totalLevels == 0:
      makecastleshape(0, 100, 10, 10)
      random_game_status2 = random.randint(1, 3)
      if random_game_status2 == 1:
        game_status_msg = "Bijna klaar!"
      elif random_game_status2 == 2:
        game_status_msg = "Nog een level te gaan!"
      elif random_game_status2 == 3:
        game_status_msg = "Laatste level!"

    ball_x = paddle_x        #x-position of the ball in pixels 
    ball_y = paddle_y - BALL_HEIGHT - 50
    time.sleep(0.5)
    ball_speed_x = 6    #speed in the x-direction of the game
    ball_speed_y = 6
    paddle_speed = 10

    currentPaddle_img = paddle_img


    frame = 0
    playingLevel = True

    todo = []
    while playingLevel:
      # read events
      for event in pygame.event.get(): 
          if event.type == pygame.QUIT:
              running = False
              playingLevel = False
      keys = pygame.key.get_pressed() 
      if keys[pygame.K_d] :
        paddle_x = paddle_x + paddle_speed
      if keys[pygame.K_a] :
        paddle_x = paddle_x - paddle_speed

      # stop paddle at screen edges
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
      if paddle_x < 0:
        paddle_x = 0
      # move everything

      # move ball
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y

      # move powerups
      for i in range(len(powerup_x)):
         powerup_y[i] += 10


      # bounce ball
      if ball_x < 0 : 
        ball_speed_x = abs(ball_speed_x) 
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 

      if ball_y < 0 :
        ball_speed_y = abs(ball_speed_y) 
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
        ball_speed_y = abs(ball_speed_y) * -1 
      
      # sides ball and paddle and brick

      ball_left = ball_x
      ball_right = ball_x + BALL_WIDTH
      ball_upper = ball_y
      ball_under = ball_y + BALL_HEIGHT
      paddle_left = paddle_x
      paddle_right = paddle_x + PADDLE_WIDTH
      paddle_upper = paddle_y
      paddle_under = paddle_y + PADDLE_HEIGHT

      brick_left = []
      brick_right = []
      brick_upper = []
      brick_under = []

      for brick in range(len(brick_x)):
        brick_left.append(brick_x[brick])
        brick_right.append(brick_x[brick] + BRICK_WIDTH)
        brick_upper.append(brick_y[brick])
        brick_under.append(brick_y[brick] + BRICK_HEIGHT)

      

      # handle collisions
      # bounce ball from paddle
      if (ball_right > paddle_left and
      ball_left < paddle_right and
      ball_under > paddle_upper and
      ball_upper < paddle_under):

        ball_speed_y = -abs(ball_speed_y)

        paddle_centre = paddle_x + PADDLE_WIDTH / 2
        ball_centre = ball_x + BALL_WIDTH / 2

    
        offset = (ball_centre - paddle_centre) / (PADDLE_WIDTH / 2)

        ball_speed_x = offset * 10  

      if abs(ball_speed_x) < 2:
          ball_speed_x = 2 if ball_speed_x > 0 else -2


      # ball touches bricks
      for brick in range(len(brick_x)):
        if (ball_right > brick_left[brick] and
        ball_left < brick_right[brick] and
        ball_under > brick_upper[brick] and
        ball_upper < brick_under[brick]):
          print('brick touched at ball_x = ' + str(ball_x) + ' and ball_y = ' + str(ball_y))
          if (ball_speed_y > 0 and
              ball_y < brick_y[brick]):
              ball_speed_y = -abs(ball_speed_y)
          elif (ball_speed_y < 0 and 
              ball_y + BALL_HEIGHT > brick_y[brick] + BRICK_HEIGHT):
              ball_speed_y = abs(ball_speed_y)
          elif (ball_speed_x > 0 and
              ball_x < brick_x[brick]):
              ball_speed_x = -abs(ball_speed_x)
          elif (ball_speed_x < 0 and 
              ball_x + BALL_HEIGHT > brick_x[brick] + BRICK_HEIGHT):
              ball_speed_x = abs(ball_speed_x)
          
          brick_damage[brick] -= 1
          if brick_damage[brick] == 0:
            
            paddle_speed += 0.8
            score += 100

            if ball_speed_y < 0 and ball_speed_y > -12:
              ball_speed_y -= 0.8
            elif ball_speed_y > 0 and ball_speed_y < 12:
              ball_speed_y += 0.8

            if random.randint(1, 5) == 1:
              powerup_x.append(brick_x[brick])
              powerup_y.append(brick_y[brick])
              powerup_type.append(POWERUP_ALLTYPES[random.randint(0, len(POWERUP_ALLTYPES) - 1)])

            brick_x.pop(brick)
            brick_y.pop(brick)
            brick_damage.pop(brick)
            brick_color.pop(brick)

          if ball_speed_x < 0:
            ball_speed_x -= 0.6
          elif ball_speed_x > 0:
            ball_speed_x += 0.6
          
          break
      

      new_powerup_x = powerup_x
      new_powerup_y = powerup_y

      #handle powerups
      for powerup in range(0, len(powerup_x)):
        if (powerup_x[powerup] >= paddle_left and
        powerup_x[powerup] <= paddle_right and
        powerup_y[powerup] >= paddle_upper and
        powerup_y[powerup] <= paddle_under):
          if powerup_type[powerup] == "wide":
             currentPaddle_img = widePaddle_img
             PADDLE_WIDTH = 288
             new_powerup_x.pop(powerup)
             new_powerup_y.pop(powerup)
             todo.append([frame + 400, "ChangeToNormalPaddle"])
             break
      
        
        if powerup_y[powerup] > SCREEN_HEIGHT:
           new_powerup_x.pop(powerup)
           new_powerup_y.pop(powerup)
      
      powerup_x = new_powerup_x
      powerup_y = new_powerup_y



      if len(brick_x) == 0:
        ball_speed_x = 0
        ball_speed_y = 0
        playingLevel = False
        if currentLevel == totalLevels:
           running = False
          
      
      # game over 
      if ball_y > paddle_under:
        lives -= 1
        score -= 500
        
        if lives <= 0:

          running = False
          playingLevel = False
        else:
          ball_x = paddle_x        #x-position of the ball in pixels 
          ball_y = 300 
          time.sleep(0.5)
          ball_speed_x = 6    #speed in the x-direction of the game
          ball_speed_y = 6
          paddle_speed = 10



      # clear screen
      screen.fill('black') 

      # draw everything
      game_status_img = font.render(game_status_msg, True, "green")
      screen.blit(game_status_img, ((SCREEN_WIDTH - game_status_img.get_width()) / 2, 40))
      
      game_level_img = font.render("level: " + str(currentLevel), True, "green")
      screen.blit(game_level_img, ((5, 40)))

      score_img = font.render("Score: " + str(score), True, "green")
      screen.blit(score_img, (170, 40))

      #draw powerups
      for i in range(len(powerup_x)):
         screen.blit(powerup_img, (powerup_x[i], powerup_y[i]))

      # draw ball
      screen.blit(ball_img, (ball_x, ball_y))
      screen.blit(currentPaddle_img, (paddle_x, paddle_y))

      #draw bricks
      for brick in range(len(brick_x)):
        if brick_damage[brick] == 1:
          screen.blit(brick_cracked_img[brick_color[brick]], (brick_x[brick], brick_y[brick]))
        else:
          screen.blit(brick_img[brick_color[brick]], (brick_x[brick], brick_y[brick]))

      #draw lives
      for live in range(lives):
        screen.blit(lives_img, (SCREEN_WIDTH - 40  - (LIVES_WIDTH + 10) * live, 50))


      for i in range(len(todo)):
         if frame == todo[i][0]:
            if todo[i][1] == "ChangeToNormalPaddle":
               currentPaddle_img = paddle_img
               PADDLE_WIDTH = 144

      # show screen
      pygame.display.flip() 

      # wait until next frame
      fps_clock.tick(FPS) # Sleep the remaining time of this frame
      frame += 1


#read xml
leaderboard = ET.parse('Leaderboard.xml')
leaderboardlist = []
leaderboard_img = []
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
leaderboardtxt = ""
rootleaderboard = leaderboard.getroot()
currentName = [0, 0, 0]
selected = 0
skip = 0

FPS = 2

for entry in rootleaderboard.findall('entry'):
    entryname = entry.find('username').text
    entryscore = entry.find('score').text
    leaderboardlist.append([int(entryscore), entryname])

running = True
while running:
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
   keys = pygame.key.get_pressed() 

   screen.fill('black')
   leaderboardlist.sort()
   leaderboardlist.reverse()
   for i in range(0, 3):
      screen.blit(font.render(str(leaderboardlist[i][0]) + " " + str(leaderboardlist[i][1]), 0, "green"), (0, i * 80 + 80))

   screen.blit(font.render("LEADERBOARD", 0, "green"), (10, 0))
   screen.blit(font.render("Use [A], [D], [W] and [S] to select name, then press [Q]", 0, "green"), (0 , SCREEN_HEIGHT - 100))

   for i in range(0,3):
      if i != selected:
        screen.blit(font.render(alphabet[currentName[i]], 0, "green"), (SCREEN_WIDTH / 2 + 80 * i, 280))
      else:
         screen.blit(font.render(alphabet[currentName[i]], 0, "blue"), (SCREEN_WIDTH / 2 + 80 * i, 280))

   if keys[pygame.K_d] and selected != 2:
       selected += 1
   if keys[pygame.K_a] and selected != 0 :
       selected -= 1

   if keys[pygame.K_w] and currentName[selected] != 25:
       currentName[selected] += 1
   if keys[pygame.K_s] and currentName[selected] != 0:
       currentName[selected] -= 1

   if keys[pygame.K_q]:
      name = ""
      for i in currentName:
          name += alphabet[i]

      new_entry = ET.Element('entry')

      username_elem = ET.SubElement(new_entry, 'username')
      username_elem.text = name

      score_elem = ET.SubElement(new_entry, 'score')
      score_elem.text = str(score)

      rootleaderboard.append(new_entry)
      leaderboard.write("Leaderboard.xml")
      running = False


  # show screen
   pygame.display.flip() 

   # wait until next frame
   fps_clock.tick(FPS) # Sleep the remaining time of this frame


   

screen.fill('black')
pygame.display.flip()
time.sleep(10)
print('mygame stopt running')