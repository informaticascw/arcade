'''

import math
from math import cos, sin


class car:
    def __init__(self, brand, tuplething):
        self.brandithas = brand
        self.itstuple = tuplething


myList = []
if 1 > 0:
    myList.append(car("mercedes", (100, 505)))
myList.append(car("audi", (200, 306)))

#for objectX in myList:
    #print(objectX.brandithas)
def tadd(tuple1, tuple2): #adding tuples liek they're coordinates
    return (tuple1[0]+tuple2[0], tuple1[1]+tuple2[1])
#print(str(tadd((5, 8),(-1, 3))))


myList = [8, 7, 6, 5, 4, 3, 2, 1]
class Qwerty:
    def __init__(self, Aprop, Bprop):
        self.A = Aprop
        self.B = Bprop
    def addy(self):
        myList.pop(0)
        return self.A + self.B
        
p55 = Qwerty(3, 9)
dictyyy = {
    "doit": p55.addy()
}
for i in range(5):
    dictyyy["doit"]
#print(dictyyy["doit"]) #12
#print(myList) #[7, 6, 5, 4, 3, 2, 1]

'''
#
# FIGHTING GAME
#
import os
# ensure dummy audio driver in headless/container environments
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame, time
import math
from math import cos, sin

pygame.font.init() # you have to call this at the start, 
                   
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"warning: audio mixer init failed: {e}")

# sound effects container and loader
sound_effects = {}

def load_sounds():
    global sound_effects
    sound_files = {
        'punch': 'Hvy_punch.mp3',
        'jump': 'Regular_jump.mp3',
        'sword': 'Sword_attack.mp3',
        'rocket': 'Rocket_jump.mp3',
        'hit': 'Impact_sound.mp3'
    }
    for sound_name, filename in sound_files.items():
        try:
            sound_effects[sound_name] = pygame.mixer.Sound(filename)
        except Exception as e:
            print(f"warning: couldn't load sound {filename}: {e}")

health_font = pygame.font.SysFont('Times New Roman', 100)
small_font = pygame.font.SysFont('Times New Roman', 25)


def tadd(tuple1, tuple2): #adding tuples liek they're coordinates
    return (tuple1[0]+tuple2[0], tuple1[1]+tuple2[1])

def maketlbr(coor1, coor2):
    #returning the topleft and bottomright of a rectangle with the two parameters as corners
    topleft = (None, None)
    bottomright = (None, None)
    if coor1[0] < coor2[0]:
        topleft = (coor1[0], None)
        bottomright = (coor2[0], None)
    else:
        topleft = (coor2[0], None)
        bottomright = (coor1[0], None)
    if coor1[1] < coor2[1]:
        topleft = (topleft[0], coor1[1])
        bottomright = (bottomright[0], coor2[1])
    else:
        topleft = (topleft[0], coor2[1])
        bottomright = (bottomright[0], coor1[1])
    return topleft, bottomright


#boxes consist of a top-left coordinate pair and a bottom-right coordinate pair.
#creer class dmgbox, zo kan je makkelijk dat maken. Method erin die checkt of het een andere box raakt. 

dmgboxlist = [] #put all dmgboxes in this list! so we can iterate it. 
class dmgbox: #you don't give names to these objects, you append them to playerboxlist, so we can iterate the list
    global playerboxList
    #when you create a dmgbox you have to give its topleft and bottomright coordinates, how much dmg it does, and which player owns that dmg
    def __init__(self, topleft, bottomright, rawdmg, owner, attackowner, tick_created, hitstun):
        self.topleft = topleft
        self.bottomright = bottomright
        self.rawdmg = rawdmg
        self.owner = owner # "p1"  or "p2", those are objects
        self.attackowner = attackowner #which attack this dmgbox belongs to. Example: "punch". This is so we can check all dmgboxes that belong to one attack and only grab the highest dealt dmg. And if an attack has two parts you can take highest hitting of both.
        self.tick_created = tick_created #when you made this dmgboc
        self.hitstun = hitstun
    #checking if this dmgbox hits the opposing player (which is an object). This function does NOT deal the dmg yet
    def hitcheck(self):
        if self.owner == "p1":
            opponent = "p2"
        else:
            opponent = "p1"
        touchOpponent = False
        highestCritx = 0
        for box in playerboxList:
            if box.owner == opponent:
                #code for seeing if boxes touch, [0] is x coor,   [1] is y coor. remember that TOPLEFT of the screen is (0,0)
                #if top of dmgbox is higher than bottom of opponent playerbox and bottom of dmgbox is lower than its top       and left of dmg is left of the right of opoonnent box  and the right of dmg is to the right of the playerbox' left
                if self.topleft[1] < box.bottomright[1]                  and self.bottomright[1] > box.topleft[1]    and self.topleft[0] < box.bottomright[0]          and self.bottomright[0] > box.topleft[0]:
                    touchOpponent = True
                    if box.critx > highestCritx:
                        highestCritx = box.critx
                    #quit the for loop (unless you want a headshot thing)
        return (touchOpponent, highestCritx) #so when you call this function for a dmgbox it gives a tuple telling you if it hit and how hard it hit

        #check for every playerbox with owner = opponent
        


#really broad class of what a fighter looks like, will be parent class of player

class player(): # p1 =    or p2 =
    def __init__(self, zerocoor, health, owner, flipped, iframes): #also things about the character the player plays
        self.zerocoor = zerocoor
        self.health = health
        self.owner = owner
        self.jumping = False #is player jumping?
        self.is_crouching = False #is player crouching?
        self.crouch_original_coords = None #stores original coords before crouch
        self.attack = None
        self.attack_start_tick = None
        self.flipped = flipped #True of False
        self.iframes = iframes #for how many frames/ticks this player is still invincible for
        self.hitstunned = 0
        self.speedboost = 0
        if self.flipped == False:
            for i in range(len(self.topleftCoor)):
                #the y needs to stay the same, the x needs to flip
                self.topleftCoor[i], self.bottomrightCoor[i] = ( - self.bottomrightCoor[i][0], self.topleftCoor[i][1]),      ( - self.topleftCoor[i][0], self.bottomrightCoor[i][1]) #This line is x, y = bcuz change

    def play(self, tick): #continues doing attacks and other stuff
        self.flipmult = 2*self.flipped - 1
        for box in dmgboxlist:
            if box.owner == self.owner:
                t =  tick - box.tick_created #for how many ticks this attack has been going on for
                if box.attackowner == "punch":
                    #continue the punch
                    goodcoor = maketlbr(tadd(self.zerocoor, (40*self.flipmult, -20)), tadd(self.zerocoor, ((30 + 9*t)*self.flipmult, 30))) #having the box stay at the players shoulder
                    box.topleft, box.bottomright = goodcoor #having the box stay at the players shoulder
                    #there we're making the dmgbox follow a parametric function for its end that's becoming longer
                    self.topleftCoor[2], self.bottomrightCoor[2] = tadd((self.zerocoor[0]*-1, self.zerocoor[1]*-1), goodcoor[0]), tadd((self.zerocoor[0]*-1, self.zerocoor[1]*-1), goodcoor[1])
                    if t >= 30:
                        self.topleftCoor[2], self.bottomrightCoor[2] =  maketlbr((60*self.flipmult, 0), (90*self.flipmult, 150))
                        dmgboxlist.remove(box) #.remove() can be buggy when there are two boxes that are the same but it's probably fine
                if box.attackowner == "rocketjump":
                    if self.zerocoor[1] >= zerocoor_floor: #stop when you hit floor
                        dmgboxlist.remove(box)
                        self.jumping = False
                        self.topleftCoor = [(-70, -150), (-50, -20), (60, 0), (-100, -10)]
                        self.bottomrightCoor = [(70, -20), (60, 200), (90, 150), (-50, 140)]

                    if t % 10 == 0:
                        self.turn()
                    if t > 60 and t < 100:
                        self.speedboost = 8
                    else:
                        self.speedboost = 0
                    self.zerocoor = tadd(self.zerocoor, (0, (t - 100)*0.08))
                    box.topleft = tadd(self.zerocoor, (-40, 180)) #having the box stay at the players shoulder
                    box.bottomright = tadd(self.zerocoor, (40, 200)) #making the dmgbox follow a parametric function for its bottomright
                    if t == 80:
                        box.rawdmg *= 4
                if box.attackowner == "swordoverhead":
                    if t >= 120:
                        dmgboxlist.remove(box)
                        self.jumping = False
                    
                    if t < 50:
                        box.spin = -4 
                    elif t < 100:
                        box.dis += 2
                        box.spin = t/25  - 6  #this is how far it is in the rotation, it loops
                    elif t == 100:
                        box.rawdmg *= 8
                    else:
                        box.spin = t/5 - 22
                    box.topleft, box.bottomright = maketlbr(tadd(self.zerocoor, ((cos(box.spin)*box.dis)*self.flipmult, sin(box.spin)*box.dis)), tadd(self.zerocoor, ((cos(box.spin)*box.dis+50)*self.flipmult, sin(box.spin)*box.dis+50))) #having the box stay at the players shoulder



                if box.attackowner == "jump":
                    self.zerocoor = tadd(self.zerocoor, (0, (t-40)*0.2)) #height is 40²/2*0.2 = 160
                    if self.zerocoor[1] >= zerocoor_floor:
                        dmgboxlist.remove(box)
                        self.jumping = False
                        self.speed += 2
        #falling if needed:
        if self.zerocoor[1] < zerocoor_floor and self.jumping == False:
            self.zerocoor = tadd(self.zerocoor, (0, 20))
        if self.zerocoor[1] >= zerocoor_floor:
            self.zerocoor = (self.zerocoor[0], zerocoor_floor)
    

    def can_attack(self, tick):
        for box in dmgboxlist:
            if box.owner == self.owner:
                if tick - box.tick_created <= cooldownDict[box.attackowner]: #if there is an attack that the player is still cooling down from, return False
                    return False
        if self.hitstunned > 0:
            return False
        
        return True

    def draw(self): #renewing the playerboxes
        for box in playerboxList:
            if box.owner == self.owner:
                playerboxList.remove(box) #might cause error bcuz remove is weird
        for i in range(len(self.topleftCoor)):
            critx = 1
            if i == 0:
                critx = 2
            playerboxList.append(playerbox(tadd(self.topleftCoor[i], self.zerocoor), tadd(self.bottomrightCoor[i], self.zerocoor), self.owner, critx))       
    def turn(self):
        if self.flipped == False:
            self.flipped = True
        else:
            self.flipped = False
        for i in range(len(self.topleftCoor)):
            #the y needs to stay the same, the x needs to flip
            self.topleftCoor[i], self.bottomrightCoor[i] = ( - self.bottomrightCoor[i][0], self.topleftCoor[i][1]),      ( - self.topleftCoor[i][0], self.bottomrightCoor[i][1]) #This line is x, y = bcuz change
    def jump(self, tick): #we're treating jump as an attack for simplicity
        self.jumping = True
        self.attack_start_tick = tick
        self.speed -= 2
        dmgboxlist.append(dmgbox((-3333, -3333), (-2222, -2222), 0, self.owner, "jump", tick, 0)) #create the first frame of the attack

    def start_crouch(self):
        if not self.is_crouching:
            self.is_crouching = True
            # Store original coordinates
            self.crouch_original_coords = (self.topleftCoor[:], self.bottomrightCoor[:])
            # Shift body down by 80 pixels (crouch)
            crouch_offset = 80
            self.topleftCoor = [(tl[0], tl[1] + crouch_offset) for tl in self.topleftCoor]
            self.bottomrightCoor = [(br[0], br[1] + crouch_offset) for br in self.bottomrightCoor]
    
    def stop_crouch(self):
        if self.is_crouching and self.crouch_original_coords:
            self.is_crouching = False
            # Restore original coordinates
            self.topleftCoor, self.bottomrightCoor = self.crouch_original_coords
            self.crouch_original_coords = None
        

        

cooldownDict = { #the cooldown given for a specific attack, measured in ticks
    "punch": 70,
    "kick": 80,
    "flip": 30,
    "rocketjump": 80,
    "jump": 10,
    "swordoverhead": 200
}
class charA(player):
    def __init__(self, zerocoor, health, owner, flipped, iframes):
        #first in list is HEAD, then rest
        self.topleftCoor = [(-70, -150), (-50, -20), (60, 0), (-100, -10)]
        self.bottomrightCoor = [(70, -20), (60, 200), (90, 150), (-50, 140)]
        super().__init__(zerocoor, health, owner, flipped, iframes)        #adding playerboxes specific to this character


    def abi1(self, tick): #punch
        self.attack = "punch"
        self.attack_start_tick = tick
        self.zerocoor = tadd(self.zerocoor, (20*self.flipmult, 0))
        tl, br = maketlbr(tadd(self.zerocoor, (40*self.flipmult, -20)), tadd(self.zerocoor, (100*self.flipmult, 30)))
        dmgboxlist.append(dmgbox(tl, br, 30, self.owner, "punch", tick, 20)) #create the first frame of the attack
    def abi2(self, tick): 
        self.jumping = True
        self.attack_start_tick = tick
        #flapping the arms around
        self.topleftCoor = [(-70, -150), (-50, -20), (60, 0), (-170, -10)]
        self.bottomrightCoor = [(70, -20), (60, 200), (180, 70), (-50, 65)]
        self.zerocoor = tadd(self.zerocoor, (0, -1)) #so it doesnt immediately detect ground
        dmgboxlist.append(dmgbox(tadd(self.zerocoor, (-40, 180)), tadd(self.zerocoor, (40, 200)), 5, self.owner, "rocketjump", tick, 80)) #create the first frame of the attack

class charB(player):
    def __init__(self, zerocoor, health, owner, flipped, iframes):
        #first in list is HEAD, then rest
        self.topleftCoor = [(-50, -120), (-40, -10), (40, 10), (-100, 10)]
        self.bottomrightCoor = [(50, 0), (40, 200), (90, 150), (-40, 140)]
        super().__init__(zerocoor, health, owner, flipped, iframes)        #adding playerboxes specific to this character
    def abi1(self, tick): #pulling sword over head
        self.attack = "swordoverhead"
        self.attack_start_tick = tick
        self.jumping = True #to slow down

        for i in range(3):
            dmgboxlist.append(dmgbox((0,0), (1,1), 5, self.owner, "swordoverhead", tick, 80)) #create the first frame of the attack
            dmgboxlist[len(dmgboxlist) - 1].dis = 60*i+40
    def abi2(self, tick):
        self.attack = "swordblock"
playerboxList = []
#a fighter is made up of boxes that should resemble it's body
class playerbox: #you don't give names to these objects, you append them to playerboxlist, so we can iterate the list in hitcheck()
    #global playerboxList
    def __init__(self, topleft, bottomright, owner, critx):
        self.topleft = topleft
        self.bottomright = bottomright
        self.owner = owner # "p1"  or "p2", those are strings
        self.critx = critx #the multiplier that is applied to dmg if it hits here. Example for head would be that critx is 2

p1 = charB((300, 500), 500, "p1", True, 0)
p2 = charC((800, 500), 500, "p2", False, 0)



#print(playerboxList)

#
# definitions 
#

FPS = 60 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
zerocoor_floor = 500 # lowest characters' zerocoor can be


#
# init game
#
pygame.init()
load_sounds()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#
'''
spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  
'''
spritesheet_placeholderbox = pygame.image.load('placeholderbox.png').convert_alpha()   

placeholderbox_img = pygame.Surface((839, 1010), pygame.SRCALPHA)  
placeholderbox_img.blit(spritesheet_placeholderbox, (0, 0))   
#placeholderbox_img = pygame.transform.scale(placeholderbox_img, (BALL_WIDTH, BALL_HEIGHT))  

spritesheet_placeholderdmgbox = pygame.image.load('pixil-frame-0 (38).png').convert_alpha()   
placeholderdmgbox_img = pygame.Surface((20, 20), pygame.SRCALPHA)  
placeholderdmgbox_img.blit(spritesheet_placeholderdmgbox, (0, 0))   

#background



# background image
try:
    background_img = pygame.image.load('placeholderbox.png').convert()
    # scale to fit the screen dimensions
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print(f"failed to load background.jpg: {e}")
    background_img = None


# game loop
#
tick = 0
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
            if p1.can_attack(tick): #attacks
                if event.key == pygame.K_1:
                    p1.abi1(tick)
                if event.key == pygame.K_LSHIFT: #this key will change/it will end up not being a key
                    p1.turn()
                if event.key == pygame.K_2:
                    p1.abi2(tick)
                if event.key == pygame.K_w and p1.jumping == False:
                    p1.jump(tick)
            if p2.can_attack(tick):
                if event.key == pygame.K_k:
                    p2.abi1(tick)
                if event.key == pygame.K_RCTRL:
                    p2.turn()
                if event.key == pygame.K_l:
                    p2.abi2(tick)
                if event.key == pygame.K_UP and p2.jumping == False:
                    p2.jump(tick)
                

     #           if event.key
    keys = pygame.key.get_pressed()
    #this next section can be much nicer I know, but it takes a long time and doesnt do much
    p1.speed = 5-2.5*p1.jumping + p1.speedboost
    if p1.hitstunned:
        p1.speed *= 0.3
    p2.speed = 5-2.5*p2.jumping + p2.speedboost
    if p2.hitstunned:
        p2.speed *= 0.3
    
    # Handle crouching
    if keys[pygame.K_c]:
        p1.start_crouch()
    else:
        p1.stop_crouch()
    
    if keys[pygame.K_SLASH]:
        p2.start_crouch()
    else:
        p2.stop_crouch()
    
    if keys[pygame.K_a] and p1.zerocoor[0] > 100:
        p1.zerocoor = tadd(p1.zerocoor, (-p1.speed, 0))
    if keys[pygame.K_d] and p1.zerocoor[0] < SCREEN_WIDTH - 100:
        p1.zerocoor = tadd(p1.zerocoor, (p1.speed, 0))
    if keys[pygame.K_LEFT] and p2.zerocoor[0] > 100:
        p2.zerocoor = tadd(p2.zerocoor, (-p2.speed, 0))
    if keys[pygame.K_RIGHT] and p2.zerocoor[0] < SCREEN_WIDTH - 100:
        p2.zerocoor = tadd(p2.zerocoor, (p2.speed, 0))

            


    # 
    # handle damaging with boxes
    #
    for box in dmgboxlist:
        if box.hitcheck()[0]:
            if box.owner == "p1" and p2.iframes == 0:
                p2.health -= box.rawdmg * box.hitcheck()[1]
                if box.hitstun > p2.hitstunned:
                    p2.hitstunned = box.hitstun
                #p2.iframes = 50
        
                if box.rawdmg >= 1:
                    for box2 in dmgboxlist:
                        if box2.owner == box.owner and box2.attackowner == box.attackowner: #if the box is owned by dmgdealer
                            box2.hitstun = 0
                            box2.rawdmg = 0 #then make that attack deal no damage because it had already hit
                

            if box.owner == "p2" and p1.iframes == 0:
                p1.health -= box.rawdmg * box.hitcheck()[1]
                if box.hitstun > p1.hitstunned:
                    p1.hitstunned = box.hitstun
                #p1.iframes = 50
                if box.rawdmg >= 1:
                    for box2 in dmgboxlist:
                        if box2.owner == box.owner and box2.attackowner == box.attackowner: #if the box is owned by dmgdealer
                            box2.hitstun = 0
                            box2.rawdmg = 0 #then make that attack deal no damage because it had already hit
                


    # 
    # draw everything
    #

# clear screen / draw background 
    if background_img: 
        screen.blit(background_img, (0, 0)) 
    else: 
        screen.fill('blue')

    # draw players
    if 1 == 1:
        p1.draw()
        p2.draw()
        for box in playerboxList:
            if box.critx == 2 and box.owner == "p1":
                screen.blit(small_font.render(str(p1.iframes), False, (0, 0, 0)), box.topleft)
                screen.blit(small_font.render(str(p1.hitstunned), False, (0, 0, 0)), tadd(box.topleft, (50, 0)))
            if box.critx == 2 and box.owner == "p2": 
                screen.blit(small_font.render(str(p2.iframes), False, (0, 0, 0)), box.topleft)
                screen.blit(small_font.render(str(p2.hitstunned), False, (0, 0, 0)), tadd(box.topleft, (50, 0)))
            box.placeholderbox_img = pygame.transform.scale(placeholderbox_img, (box.bottomright[0] - box.topleft[0], box.bottomright[1] - box.topleft[1]))  
            screen.blit(box.placeholderbox_img, box.topleft)
        p1.play(tick)
        p2.play(tick)
        for box in dmgboxlist:
            box.placeholderdmgbox_img = pygame.transform.scale(placeholderdmgbox_img, (box.bottomright[0] - box.topleft[0], box.bottomright[1] - box.topleft[1]))  #this gives an error when the player is moving faster back than the box is moving forward when creating, can ez be fixed but all dmgboxes will prob be faster
            screen.blit(box.placeholderdmgbox_img, box.topleft)
        #health points
        text_surface1 = health_font.render(str(p1.health), False, (0, 0, 0))
        text_surface2 = health_font.render(str(p2.health), False, (0, 0, 0))
        screen.blit(text_surface1, (0,0))
        screen.blit(text_surface2, (SCREEN_WIDTH - text_surface2.get_width(), 0))

    
    
    # show screen
    pygame.display.flip() 

    # 
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame
    tick += 1
    p1.iframes -= 1
    p1.hitstunned -= 1
    p2.iframes -= 1
    p2.hitstunned -= 1
    for p in [p1, p2]:
        if p.iframes <= 0:
            p.iframes = 0
        if p.hitstunned <= 0:
            p.hitstunned = 0
print('mygame stopt running')