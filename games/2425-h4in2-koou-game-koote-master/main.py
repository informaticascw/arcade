#
# BREAKOUT GAME 
#

#  normaal schrijf ik alles in het engels,
#  gebruik ik afkortingen als variabel namen,
#  maak ik erg gebruik van project opsplitsing in modules,
#  stop ik dingen zoals de bal in classes,
#  en maak ik gebruik van ffi.
#  maar koote vind dat niet zo leuk

#  dezelfde code stijl is aangehouden zoals in de startcode
#  daarom zijn variabellen in het engels
#  en comments in nederlands


from typing import Literal
import textures, pygame, time, sys, math, random

#
# definities 
#

FPS: Literal[30, 960] = 30 # Frames Per Seconden
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720

BALL_WIDTH: int = 16
BALL_HEIGHT: int = 16
BASE_BALL_SPEED: float = 6

BAR_WIDTH: float = 243/2
BAR_HEIGHT: float = 32
BAR_SPEED: float = 20

BLOCK_WIDTH: float = 243/2
BLOCK_HEIGHT: float = 32

POWER_UP_WIDTH: float = 384/4
POWER_UP_HEIGHT: float = 128/4
POWER_UP_SPEED: float = 10
POWER_UP_COOLDOWN: float = 10 # 10 seconden

REVIVE: int = 0
EXTRA_BALL_DESPAWN_TIME: float = 10

LEVELS: int =2

DEBUG: int = 0 # debug gereedschap

ball_x: float = 0
ball_y: float = 0
ball_speed_x: float = BASE_BALL_SPEED
ball_speed_y: float = BASE_BALL_SPEED

bar_x: float = 0
bar_y: float = SCREEN_HEIGHT * 0.8
bar_speed: float = BAR_SPEED

blocks_x: list[float]=[]
blocks_y: list[float]=[]
blocks: list[list[tuple[float, float]]] = [[
    (64, 100), (228, 100), (392, 100), (556, 100), (720, 100), (884, 100),
    (64, 134), (228, 134), (392, 134), (556, 134), (720, 134), (884, 134),
    (64, 168), (228, 168), (392, 168), (556, 168), (720, 168), (884, 168),
    (64, 202), (228, 202), (392, 202), (556, 202), (720, 202), (884, 202),
],[
    (64, 100), (228, 100), (392, 100), (556, 100), (720, 100), (884, 100),
    (64, 134), (228, 134), (392, 134), (556, 134), (720, 134), (884, 134),
    (64, 168), (228, 168), (392, 168), (556, 168), (720, 168), (884, 168),
    (64, 202), (228, 202), (392, 202), (556, 202), (720, 202), (884, 202),
],[
    (64, 100), (228, 100), (392, 100), (556, 100), (720, 100), (884, 100),
    (64, 134), (228, 134), (392, 134), (556, 134), (720, 134), (884, 134),
    (64, 168), (228, 168), (392, 168), (556, 168), (720, 168), (884, 168),
    (64, 202), (228, 202), (392, 202), (556, 202), (720, 202), (884, 202),
]]

extra_balls: list[list[float]]=[
  # [0,0,0] (x,y,speed)
]

atlevel: int=0


for block_x,block_y in blocks[atlevel]:
  blocks_x.append(block_x)
  blocks_y.append(block_y)
  pass



game_status_msg: str = ""


#
# initialiseer game
#

pygame.init()
font: pygame.font.Font = pygame.font.SysFont('default', 64)
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock: pygame.time.Clock = pygame.time.Clock()

#
# lees afbeeldingen
#

spritesheet: pygame.Surface = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img: pygame.Surface = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img: pygame.Surface = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

bar_img: pygame.Surface = pygame.Surface((243, 64), pygame.SRCALPHA)  
bar_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))   
bar_img: pygame.Surface = pygame.transform.scale(bar_img, (BAR_WIDTH,BAR_HEIGHT))  

ablock_imgs: list[pygame.Surface]=[]
block_imgs: list[pygame.Surface]=[]

# 41-paddle-slow.png, 42-paddle-fast.png, 43-paddle-balls.png, 44-paddle-comet-red.png, 45-paddle-comet-green.png, 46-paddle-arrows-inside.png, 47-paddle-arrows-outside.png
powerUpsInUse: list[list[pygame.Surface,float,float,str]]=[] # naam, x, y
power_ups_ik_heb_geen_zin_meer = {
    "41-paddle-slow": textures.items["41-paddle-slow.png"],
    "42-paddle-fast": textures.items["42-paddle-fast.png"],
    "43-paddle-balls": textures.items["43-paddle-balls.png"],
    # "44-paddle-comet-red": textures.items["44-paddle-comet-red.png"],
    # "45-paddle-comet-green": textures.items["45-paddle-comet-green.png"],
    # "46-paddle-arrows-inside": textures.items["46-paddle-arrows-inside.png"],
    # "47-paddle-arrows-outside": textures.items["47-paddle-arrows-outside.png"],
    # "48-paddle-redbar": textures.items["48-paddle-redbar.png"],
    # "50-paddle-electric-step1": textures.items["50-paddle-electric-step1.png"],
    # "51-paddle-electric-step2": textures.items["51-paddle-electric-step2.png"],
    # "52-paddle-electric-step3": textures.items["52-paddle-electric-step3.png"],
    "39-paddle-plus250": textures.items["39-paddle-plus250.png"],
    "31-paddle-plus50": textures.items["31-paddle-plus50.png"],
    # "59-star": textures.items["59-star.png"],
    "60-heart": textures.items["60-heart.png"],
    # "40-paddle-plus500": textures.items["40-paddle-plus500.png"],
    # "32-paddle-plus100-step7": textures.items["32-paddle-plus100-step7.png"],
}; power_up_names=list(power_ups_ik_heb_geen_zin_meer)



for x,y in [
   [386, 650],
   [386, 130],
   [386, 390],
   [772, 0],
   [772, 260],
]:
  block_img: pygame.Surface = pygame.Surface((384, 128), pygame.SRCALPHA)  
  block_img.blit(spritesheet, (0, 0), (x, y, 384, 128))   
  block_img: pygame.Surface = pygame.transform.scale(block_img, (BLOCK_WIDTH,BLOCK_HEIGHT))
  ablock_imgs.append(block_img)
  pass

for i in range(blocks_x.__len__()-1):
   block_imgs.append(ablock_imgs[random.randint(0,len(ablock_imgs)-1)])
   pass




spacing=" "
for _ in range(4):spacing+=spacing
#
# game loep
#

print('mygame is running\n\n\n\n\n')
running: bool = True
lastTime:float = 0
lastPowerup: float=time.time()
game_status: int=2
start_time: float=time.time()
despawn_timer: float=time.time()
start_timeout_counter: float=time.time()
# if(DEBUG):game_status=0

while running:
    keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 

    #
    # verwijder info van de terminal
    #
    if DEBUG:
      for _ in range(10):sys.stdout.write("\033[1A\033[2k\r")
      pass
    
    if game_status==0:

      


      #
      # lees gebeurtenissen
      # 
      
      if time.time()-lastPowerup>POWER_UP_COOLDOWN:
        lastPowerup=time.time()
        picked=power_up_names[random.randint(0,power_up_names.__len__()-1)]
        x,y,w,h=power_ups_ik_heb_geen_zin_meer[picked]

        img: pygame.Surface = pygame.Surface((w, h), pygame.SRCALPHA)  
        img. blit(spritesheet, (0, 0), (x, y, w, h))   
        img: pygame.Surface = pygame.transform.scale(img, (POWER_UP_WIDTH,POWER_UP_HEIGHT))
        
        powerUpsInUse.append([
          img,
          random.randint(0,int(SCREEN_WIDTH-POWER_UP_WIDTH)),
          0-POWER_UP_HEIGHT,
          picked,
        ])
        pass

      if len(extra_balls)==0:despawn_timer=time.time()
      if time.time()-despawn_timer>EXTRA_BALL_DESPAWN_TIME:
        despawn_timer=time.time()
        if len(extra_balls)==0:break
        extra_balls.pop(0)
        pass

      for event in pygame.event.get(): 
          if event.type == pygame.QUIT:  
              running = False 
              pass
          pass
      keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 
    
      if keys[pygame.K_d]:
        if bar_x+bar_speed+BAR_WIDTH<SCREEN_WIDTH: bar_x+=bar_speed
        else: bar_x=SCREEN_WIDTH-BAR_WIDTH
      if keys[pygame.K_a]:
        if bar_x-bar_speed>0: bar_x-=bar_speed
        else: bar_x=0
      
      

      if keys[pygame.K_c]:
        bar_x=ball_x-BAR_WIDTH/2
        pass
      
      if keys[pygame.K_x]:
        FPS=960
        pass
      
      if not keys[pygame.K_x]:
        FPS=30
        pass

      if DEBUG and keys[pygame.K_r]: exit()
      

      # 
      # beweeg alles
      #
      ball_rect=pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_HEIGHT)
      bar_rect=pygame.Rect(bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT)


      # beweeg bal
      ball_x = ball_x + ball_speed_x
      ball_y = ball_y + ball_speed_y

      for i in extra_balls:
        i[0]+=i[2]
        i[1]+=i[3]
        pass


      # beweeg POWER_UPs
      for i in range(0,powerUpsInUse.__len__()-1):
        # print(f"powerUpsInUse[{i}] = {powerUpsInUse[i]}")
        _,x,y,n=powerUpsInUse[i]

        if y-POWER_UP_HEIGHT>SCREEN_HEIGHT:powerUpsInUse.pop(i)
        else:powerUpsInUse[i][2]+=POWER_UP_SPEED
        pass


      # stuiter bal
      if ball_x < 0 : 
        ball_speed_x = abs(ball_speed_x) 
        pass
      if ball_x + BALL_WIDTH > SCREEN_WIDTH: 
        ball_speed_x = abs(ball_speed_x) * -1 
        pass
    
      if ball_y < 0:
        ball_speed_y = abs(ball_speed_y) 
        pass
      if ball_y + BALL_HEIGHT > SCREEN_HEIGHT: 
        if not(DEBUG): game_status = 1
        game_status_msg="game over"
        ball_speed_y = abs(ball_speed_y) * -1 
        pass

      if abs(ball_speed_y)<0.5:
        ball_speed_y*=10
        pass

      # extra ballen
      for i in extra_balls:
        x,y,sx,sy=i
        if x < 0 : 
          i[2] = abs(sx) 
          pass
        if x + BALL_WIDTH > SCREEN_WIDTH: 
          i[2] = abs(sx) * -1 
          pass
      
        if y < 0:
          i[3] = abs(sy) 
          pass
        if y + BALL_HEIGHT > SCREEN_HEIGHT: 
          # if not(DEBUG): game_status = 1    # express uitgezet
          # game_status_msg="game over"       # deze mogen wel de bodem aanraken
          i[3] = abs(sy) * -1 
          pass
        pass

      if ball_rect.colliderect(bar_rect):
        #  dx = ball_rect.centerx - bar_rect.centerx
        #  dy = ball_rect.centery - bar_rect.centery
        #  angle_rad = math.atan2(dy, dx)
        #  flip_rad = (angle_rad+math.pi) % (2 * math.pi)

        #  ball_speed_y = abs(ball_speed_y) * (abs(math.cos(flip_rad)) * -1)
        offset = (ball_rect.centerx - bar_rect.centerx) / (BAR_WIDTH / 2) * 2

        ball_speed_y = abs(ball_speed_y) * -1 + offset
        pass
      
      # extra ballen
      for i in extra_balls:
        x,y,sx,sy=i
        rect=pygame.Rect(x, y, BALL_WIDTH, BALL_HEIGHT)
        if rect.colliderect(bar_rect):
          offset = (rect.centerx - rect.centerx) / (BAR_WIDTH / 2) * 2
          i[3] = abs(sy) * -1 + offset
          pass
        pass

      # removeBlocks:list[int]=[]

      # 
      # behandel botsingen
      #

      i=0
      for i in range(0,blocks_x.__len__()-1): # while loop zodat hij constant de index checkt al is deze veranderd
      # for block_x,block_y in blocks:
        block_x=blocks_x[i]
        block_y=blocks_y[i]


        block_rect=pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT)

        # touchBlockx=(block_x<(ball_x+BALL_WIDTH/2)<block_x+BLOCK_WIDTH)
        # touchBlocky=(block_y<(ball_y+BALL_HEIGHT/2)<block_y+BLOCK_HEIGHT)

        
        # if not(ball_rect.colliderect(block_rect)):
        #    dx = (ball_rect.centerx - block_rect.centerx) / BLOCK_WIDTH
        #    dy = (ball_rect.centery - block_rect.centery) / BLOCK_HEIGHT

        #    if abs(dx)>abs(dy):ball_speed_x *= -1
        #    else:ball_speed_y *= -1
              

        #    pass

        hasCollided=False
        # # if block_y<(ball_y+BALL_HEIGHT/2):
        # #   ball_speed_y = abs(ball_speed_y) * 1 
        # #   pass
        
        # # elif (ball_y+BALL_HEIGHT/2)<(block_y+BLOCK_HEIGHT):
        # #   ball_speed_y = abs(ball_speed_y) * -1
        # #   pass
        
        # # elif block_x<(ball_x+BALL_WIDTH/2):
        # #   ball_speed_x=abs(ball_speed_x) * -1
        # #   pass

        # # elif (ball_x+BALL_WIDTH/2)<(block_x+BLOCK_WIDTH):
        # #   ball_speed_x=abs(ball_speed_x) * 1
        # #   pass
        

        if ball_rect.colliderect(block_rect) and ball_x<=block_x:
          ball_speed_x=abs(ball_speed_x) * -1
          #  hasCollided=True
          pass
        elif ball_rect.colliderect(block_rect) and ball_x>=block_x:
          ball_speed_x=abs(ball_speed_x) * 1
          #  hasCollided=True
          pass
        
        if ball_rect.colliderect(block_rect) and ball_y<=block_y:
          ball_speed_y=abs(ball_speed_y) * -1
          #  hasCollided=True
          pass
        elif ball_rect.colliderect(block_rect) and ball_y>=block_y:
          ball_speed_y=abs(ball_speed_y) * 1
          #  hasCollided=True
          pass
        
        if ball_rect.colliderect(block_rect):
          # blocks_x[i]=-1000 # haalt blokken weg
          # blocks_y[i]=-1000 # zonder de indexing te verpesten
          blocks_x.pop(i); blocks_y.pop(i); block_imgs.pop(i)
          
          break # laat alleen 1 block reageren
          pass

        for e in extra_balls:
          x,y,sx,sy=e
          rect=pygame.Rect(x, y, BALL_WIDTH, BALL_HEIGHT)
          if rect.colliderect(block_rect) and x<=block_x:
            e[2]=abs(sx) * -1
            pass
          elif rect.colliderect(block_rect) and x>=block_x:
            e[2]=abs(sx) * 1
            pass
          
          if rect.colliderect(block_rect) and y<=block_y:
            e[3]=abs(sy) * -1
            pass
          elif rect.colliderect(block_rect) and y>=block_y:
            e[3]=abs(sy) * 1
            pass
          
          if rect.colliderect(block_rect):
            blocks_x.pop(i); blocks_y.pop(i); block_imgs.pop(i)
            break
            pass
          pass
        
        i+=1
        pass

      
      for i in range(0,powerUpsInUse.__len__()-1):
        _,x,y,n=powerUpsInUse[i]
        rect=pygame.Rect(x, y, POWER_UP_WIDTH, POWER_UP_HEIGHT)

        if not(rect.colliderect(bar_rect)):continue

        powerUpsInUse.pop(i)
        print("powerup is "+n)

        if n=="42-paddle-fast":
          BAR_SPEED*=1.2
          pass
        elif n=="41-paddle-slow":
          BAR_SPEED/=1.2
          pass
        elif n=="43-paddle-balls":
          extra_balls.append([0,0,ball_speed_x,ball_speed_y])
          pass
        elif n=="44-paddle-comet-red":pass
        elif n=="45-paddle-comet-green":pass
        elif n=="46-paddle-arrows-inside":pass
        elif n=="47-paddle-arrows-outside":pass
        elif n=="48-paddle-redbar":pass
        elif n=="39-paddle-plus250":
          BAR_WIDTH+=25
          bar_img: pygame.Surface = pygame.Surface((243, 64), pygame.SRCALPHA)  
          bar_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))   
          bar_img: pygame.Surface = pygame.transform.scale(bar_img, (BAR_WIDTH,BAR_HEIGHT))  
          pass
        elif n=="31-paddle-plus50":
          BAR_WIDTH+=5
          bar_img: pygame.Surface = pygame.Surface((243, 64), pygame.SRCALPHA)  
          bar_img.blit(spritesheet, (0, 0), (1158, 462, 243, 64))   
          bar_img: pygame.Surface = pygame.transform.scale(bar_img, (BAR_WIDTH,BAR_HEIGHT))  
          pass
        elif n=="59-star":pass
        elif n=="60-heart":
          REVIVE=1
          pass
        elif n=="40-paddle-plus500":pass
        elif n=="32-paddle-plus100-step7":pass

        pass

      
      
      # 
      # teken alles
      #

      # wis scherm
      screen.fill('black') 

      # teken bal
      screen.blit(ball_img, (ball_x, ball_y))

      for x,y,sx,sy in extra_balls:
        screen.blit(ball_img, (x, y))
        pass
      
      # teken bar
      screen.blit(bar_img, (bar_x, bar_y))

      # teken blokken
      for i in range(0,blocks_x.__len__()-1):
        # for block_x,block_y in blocks:
        block_x=blocks_x[i]
        block_y=blocks_y[i]
        block_img=block_imgs[i]

        # for block_x,block_y in blocks: 
        screen.blit(block_img, (block_x, block_y))
        pass

      if len(blocks_x)<=1:
        game_status_msg="gewonnen"
        if(not DEBUG):game_status=1
        pass

      # teken status berichten
      game_status_img = font.render(game_status_msg, True, 'red')
      screen.blit(game_status_img, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2))

      # teken power ups
      for i,x,y,n in powerUpsInUse:
        screen.blit(i, (x, y))
        pass

      
      # laat scherm zien
      pygame.display.flip() 

      #
      # extra
      #

      


      # snelere bal
      # ball_speed_x+=math.log10(abs(ball_speed_x))/10
      # ball_speed_y+=math.log10(abs(ball_speed_y))/10
      ball_speed_x*=1.0001
      ball_speed_y*=1.0001
      bar_speed=math.log(abs(ball_speed_x))*BAR_SPEED

      # 
      # wacht tot de volgende frame
      #

      lastTime=time.time()
      fps_clock.tick(FPS) # slaap de rest van de frame
      pass
    elif game_status==1:
      screen.fill('black') 
      print(f"atlevel = {atlevel}\n{atlevel+1} == {LEVELS} = {atlevel+1==LEVELS}\ngame status = \"{game_status_msg}\"")
      if(game_status_msg=="gewonnen" and not(atlevel+1==LEVELS)):
        atlevel+=1; game_status=0
        game_status_msg==""
        print(blocks[atlevel]); print(f"{len(blocks_x)} {len(blocks_y)}")
        for block_x,block_y in blocks[atlevel]:
          blocks_x.append(block_x)
          blocks_y.append(block_y)
          print(f"appended block ({block_x},{block_y})")
          pass
        for i in range(blocks_x.__len__()-1):
          block_imgs.append(ablock_imgs[random.randint(0,len(ablock_imgs)-1)])
          pass
        pass
      else:
        print("gebruiker zit al hoogste level")
        pass
      game_status_img: pygame.Surface = font.render(game_status_msg, True, 'red')
      screen.blit(game_status_img, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2))
      pygame.display.flip()
      time.sleep(1) # zorgt ervoor dat de loop niet beeindigd, maar zorgt ervoor dat de cpu niet bezet word gehouden
      if(game_status_msg=="game over" and REVIVE):
        REVIVE-=1; game_status=0
        pass
      
      # time.sleep(10) # zorgt ervoor dat de loop niet beeindigd, maar zorgt ervoor dat de cpu niet bezet word gehouden
      pass
    elif game_status==2:

      screen.fill('black') 
      game_status_img = font.render("breakout game", True, 'green')
      screen.blit(game_status_img, (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2))
      # overschijving is express. de variable word verder niet gebruikt. meer memory efficient
      game_status_img = font.render("laat de bal niet de bodem raken met het plankje.", True, 'white')
      screen.blit(game_status_img, (SCREEN_WIDTH/2-500, SCREEN_HEIGHT/2+200))

      game_status_img = font.render("beweeg hem met [A] links of [D] rechts", True, 'white')
      screen.blit(game_status_img, (SCREEN_WIDTH/2-500, SCREEN_HEIGHT/2+250))
      
      # start_timeout_counter=time.time()

      pygame.display.flip()
      # print(f"timing {}")
      if(time.time()-start_timeout_counter>4.6):
        game_status=0
        pass
      if DEBUG:game_status=0
      
      pass
    
    # info in terminal
    if DEBUG:
      delay=time.time()-lastTime
      sys.stdout.write(f"DEBUG={DEBUG}{spacing}\nelapsed time = {time.time()-start_time}{spacing}\ntarget fps = {FPS}{spacing}\nactual fps = {1/delay}{spacing}\nball_speed(x,y) = ({ball_speed_x}, {ball_speed_y}){spacing}\nball_pos(x,y) = ({ball_x}, {ball_y}){spacing}\nBAR_SPEED = {BAR_SPEED}{spacing}\nbar_speed = {bar_speed}{spacing}\natlevel = {atlevel}{spacing}\nblock len = {len(blocks_x)}{spacing}\n")
      sys.stdout.flush()
      pass
    pass


print('mygame stopt running')

# keep alive
while True:
   pass