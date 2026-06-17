#
# FIGHTING GAME
#
import pygame, time
import math
from math import cos, sin
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
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
hit_effects = []
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
        self.attack = None #I actually dont think this line and the next are neccessary, because we only need them after defining. I now dont even think this proporty is neccessary seeing the way we handle attacks doesn't 
        self.attack_start_tick = None
        self.flipped = flipped #True of False
        self.iframes = iframes #for how many frames/ticks this player is still invincible for
        self.hitstunned = 0
        self.speedboost = 0
        self.speedmult = 1
        self.cooldown = 0 #how long a player still has to cool down from their attack
        if self.flipped == True:
            for i in range(len(self.topleftCoor)):
                #the y needs to stay the same, the x needs to flip
                self.topleftCoor[i], self.bottomrightCoor[i] = ( - self.bottomrightCoor[i][0], self.topleftCoor[i][1]),      ( - self.topleftCoor[i][0], self.bottomrightCoor[i][1]) #This line is x, y = bcuz change

    def play(self, tick): #continues doing attacks and other stuff
        self.flipmult = -2*self.flipped + 1
        keys = pygame.key.get_pressed()
        for box in dmgboxlist:
            if box.owner == self.owner:
                t =  tick - box.tick_created #for how many ticks this attack has been going on for
                if self.hitstunned > 50: #only attacks with hard hitstuns stop attacks
                    t += 10000 #make attacks think they're done because of the hitstun
                
                if box.attackowner == "punch":
                    #continue the punch
                    goodcoor = maketlbr(tadd(self.zerocoor, (40*self.flipmult, -20)), tadd(self.zerocoor, ((30 + 15*t)*self.flipmult, 30))) #having the box stay at the players shoulder
                    box.topleft, box.bottomright = goodcoor #having the box stay at the players shoulder
                    #there we're making the dmgbox follow a parametric function for its end that's becoming longer
                    self.topleftCoor[2], self.bottomrightCoor[2] = tadd((self.zerocoor[0]*-1, self.zerocoor[1]*-1), goodcoor[0]), tadd((self.zerocoor[0]*-1, self.zerocoor[1]*-1), goodcoor[1])
                    if t >= 20:
                        self.topleftCoor[2], self.bottomrightCoor[2] =  maketlbr((60*self.flipmult, 0), (90*self.flipmult, 150))
                        dmgboxlist.remove(box) #.remove() can be buggy when there are two boxes that are the same but it's probably fine
                if box.attackowner == "rocketjump":
                    if t > 10000:
                        t-= 10000 #attacks can't stop a helicopter
                    if self.zerocoor[1] >= zerocoor_floor or t > 300: #stop when you hit floor
                        self.cooldown = 30
                        dmgboxlist.remove(box)
                        self.jumping = False
                        self.topleftCoor = [(-70, -150), (-50, -20), (60, 0), (-100, -10)]
                        self.bottomrightCoor = [(70, -20), (60, 200), (90, 150), (-50, 140)]
                        self.speedboost = 0
                    elif t % 10 == 0:
                        self.turn()
                    elif t > 60 and t < 100:    
                        self.speedboost = 8
                    else:
                        self.speedboost = 0
                    self.zerocoor = tadd(self.zerocoor, (0, (t - 100)*0.08))
                    box.topleft = tadd(self.zerocoor, (-40, 180)) #having the box stay at the players shoulder
                    box.bottomright = tadd(self.zerocoor, (40, 200)) #making the dmgbox follow a parametric function for its bottomright
                    if t == 80:
                        box.rawdmg *= 4
                if box.attackowner == "swordoverhead":
                    t += 10 #this is the easy way to lessen the buildup in the code
                    self.jumping = True
                    self.speedboost = -1
                    if box.owner == "p1":
                        reqKey = pygame.K_r
                    else:
                        reqKey = pygame.K_p
                    if t >= 120 or (keys[reqKey] and t < 100):
                        if t <100:
                            self.cooldown = 0
                            self.abi2(tick)
                        dmgboxlist.remove(box)
                        self.jumping = False
                        self.speedboost = 0
                    
                    if t < 50:
                        box.spin = -4 
                    elif t < 100:
                        box.dis += 2
                        box.spin = t/25  - 6  #this is how far it is in the rotation, it loops
                    elif t == 100:
                        box.rawdmg *= 8
                    else:
                        box.spin = t/5 - 22
                    box.topleft, box.bottomright = maketlbr(tadd(self.zerocoor, ((cos(box.spin)*box.dis)*self.flipmult, sin(box.spin)*box.dis)), tadd(self.zerocoor, ((cos(box.spin)*box.dis+50)*self.flipmult, sin(box.spin)*box.dis+50))) #having the box turn coolly

                if box.attackowner == "swordblock":
                    self.jumping = True
                    self.speedmult = 0
                    box.topleft, box.bottomright = maketlbr(tadd(self.zerocoor, (100*self.flipmult, -180)), tadd(self.zerocoor, (140*self.flipmult, 150)))
                    self.topleftCoor[4], self.bottomrightCoor[4] = maketlbr((100*self.flipmult, -180), (140*self.flipmult, 150))

                    
                    if box.owner == "p1":
                        reqKey = pygame.K_r
                    else:
                        reqKey = pygame.K_p
                    if t > 250 or not keys[reqKey]:
                        self.jumping = False
                        self.speedmult = 1
                        dmgboxlist.remove(box)
                        self.cooldown = 50
                        self.topleftCoor[3], self.bottomrightCoor[3] = maketlbr((-100*self.flipmult, -10), (-50*self.flipmult, 140))
                        self.topleftCoor[2], self.bottomrightCoor[2] = maketlbr((40*self.flipmult, 10), (90*self.flipmult, 150))
                        self.topleftCoor[4], self.bottomrightCoor[4] = (0,0), (1,1)


                if box.attackowner == "fireball":
                    if t > 300:
                        dmgboxlist.remove(box)
                    if t == 65:
                        box.rawdmg = 70
                        self.topleftCoor[2], self.bottomrightCoor[2] = maketlbr((40*self.flipmult, 10), (90*self.flipmult, 150))
                    if t < 50:
                        box.topleft, box.bottomright = maketlbr(tadd(self.zerocoor, (100*self.flipmult, -50)), tadd(self.zerocoor, (160*self.flipmult, 10)))
                    else:
                        if box.bottomright[0] > self.zerocoor[0]:
                            box.topleft, box.bottomright = tadd(box.topleft, (8, 0)), tadd(box.bottomright, (8, 0))
                        else:
                            box.topleft, box.bottomright = tadd(box.topleft, (-8, 0)), tadd(box.bottomright, (-8, 0))
                if box.attackowner == "kick":
                    self.jumping = True
                    if t > 105:
                        box.topleft, box.bottomright = (0,0), (1,1)
                        self.jumping = False
                    if t > 125:
                        self.topleftCoor = [(-50, -160), (-40, -10), (40, 10), (-100, 10), (0, 0)]
                        self.bottomrightCoor = [(50, 0), (40, 200), (90, 150), (-40, 140), (1,1)]
                        dmgboxlist.remove(box)
                    if t < 40:
                        self.topleftCoor[4], self.bottomrightCoor[4] = maketlbr((40*self.flipmult, 150), (90*self.flipmult, 200))
                        for i in range(4):
                            self.topleftCoor[i] = tadd(self.topleftCoor[i], (0, 2))
                        self.bottomrightCoor[0] = tadd(self.bottomrightCoor[0], (0, 2))
                    elif t > 70 and t < 105:
                        box.topleft, box.bottomright = maketlbr(tadd(self.zerocoor, (40*self.flipmult, 150)), tadd(self.zerocoor, ((-330+6*t)*self.flipmult, 200)))
                    if t > 90 and t <105:
                        box.topleft, box.bottomright = maketlbr(tadd(self.zerocoor, (40*self.flipmult, 150)), tadd(self.zerocoor, ((-690+10*t)*self.flipmult, 200)))

                if box.attackowner == "jump":
                    if t > 10000:
                        t-= 10000 #attacks can't stop a jump
                    self.zerocoor = tadd(self.zerocoor, (0, (t-40)*0.2)) #height is 40²/2*0.2 = 160
                    if self.zerocoor[1] >= zerocoor_floor:
                        dmgboxlist.remove(box)
                        self.jumping = False
                        self.speed += 2
                if box.attackowner == "crouch":
                    if box.owner == "p1":
                        reqKey = pygame.K_s
                    else:
                        reqKey = pygame.K_k
                    if not keys[reqKey]:
                        print("ha")
                        self.jumping = False
                        self.speedmult = 1
                        self.attack = None
                        dmgboxlist.remove(box)
                        self.zerocoor = tadd(self.zerocoor, (0, -120))
                        for i in range(len(self.topleftCoor)):
                            self.topleftCoor[i] = (self.topleftCoor[i][0], self.topleftCoor[i][1]*2.5)
                            self.bottomrightCoor[i] = (self.bottomrightCoor[i][0], self.bottomrightCoor[i][1]*2.5)
                    self.cooldown = 5
                    
        #falling if needed:
        if self.zerocoor[1] < zerocoor_floor and self.jumping == False:
            self.zerocoor = tadd(self.zerocoor, (0, 20))
        if self.zerocoor[1] >= zerocoor_floor and not (self.attack == "crouch"):
            self.zerocoor = (self.zerocoor[0], zerocoor_floor)
        
        #adjusting the cooldown
        self.cooldown -= 1
        for box in dmgboxlist:
            if box.owner == self.owner:
                if cooldownDict[box.attackowner] - tick + self.attack_start_tick > self.cooldown:
                    self.cooldown = cooldownDict[box.attackowner] - tick + self.attack_start_tick


    def can_attack(self, tick):
        if self.cooldown > 0:
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
            if self.attack ==  "swordblock" and i == 4:
                critx = 0
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
        play_sound(snd_regular_jump, "regular jump")
    def crouch(self, tick):
        self.jumping = True
        self.speedmult = 0
        self.attack = "crouch"
        self.attack_start_tick = tick
        self.zerocoor = tadd(self.zerocoor, (0, 120))
        dmgboxlist.append(dmgbox((-3333, -3333), (-2222, -2222), 0, self.owner, "crouch", tick, 0)) #create the first frame of the attack
        for i in range(len(self.topleftCoor)):
            self.topleftCoor[i] = (self.topleftCoor[i][0], self.topleftCoor[i][1]/2.5)
            self.bottomrightCoor[i] = (self.bottomrightCoor[i][0], self.bottomrightCoor[i][1]/2.5)

        

        

cooldownDict = { #the cooldown given for a specific attack, measured in ticks
    "punch": 70,
    "kick": 120,
    "flip": 30,
    "rocketjump": 210,
    "jump": 10,
    "crouch": 10, 
    "swordoverhead": 200,
    "swordblock": 300,
    "fireball" : 120
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
        play_sound(snd_hvy_punch, "heavy punch")
    def abi2(self, tick): 
        self.jumping = True
        self.attack_start_tick = tick
        #flapping the arms around
        self.topleftCoor = [(-70, -150), (-50, -20), (60, 0), (-170, -10)]
        self.bottomrightCoor = [(70, -20), (60, 200), (180, 70), (-50, 65)]
        self.zerocoor = tadd(self.zerocoor, (0, -1)) #so it doesnt immediately detect ground
        dmgboxlist.append(dmgbox(tadd(self.zerocoor, (-40, 180)), tadd(self.zerocoor, (40, 200)), 5, self.owner, "rocketjump", tick, 80)) #create the first frame of the attack
        play_sound(snd_rocket_jump, "rocket jump")

class charB(player):
    def __init__(self, zerocoor, health, owner, flipped, iframes):
        #first in list is HEAD, then rest
        self.topleftCoor = [(-50, -120), (-40, -10), (40, 10), (-100, 10), (0,0)]
        self.bottomrightCoor = [(50, 0), (40, 200), (90, 150), (-40, 140), (1,1)]
        super().__init__(zerocoor, health, owner, flipped, iframes)        #adding playerboxes specific to this character
    def abi1(self, tick): #pulling sword over head
        self.attack = "swordoverhead"
        self.attack_start_tick = tick
        self.jumping = True #to slow down

        for i in range(3):
            dmgboxlist.append(dmgbox((0,0), (1,1), 5, self.owner, "swordoverhead", tick, 80)) #create the first frame of the attack
            dmgboxlist[len(dmgboxlist) - 1].dis = 60*i+40
        play_sound(snd_sword_attack, "sword attack")
    def abi2(self, tick):
        self.attack = "swordblock"
        self.attack_start_tick = tick
        self.jumping = True
        self.speedmult = 0
        self.topleftCoor[3], self.bottomrightCoor[3] = maketlbr((40*self.flipmult, 80), (100*self.flipmult, 120))
        self.topleftCoor[2], self.bottomrightCoor[2] = maketlbr((40*self.flipmult, 10), (100*self.flipmult, 50))
        dmgboxlist.append(dmgbox((0,0), (1,1), 5, self.owner, "swordblock", tick, 30))

class charC(player):
    def __init__(self, zerocoor, health, owner, flipped, iframes):
        #first in list is HEAD, then rest
        self.topleftCoor = [(-50, -160), (-40, -10), (40, 10), (-100, 10), (0, 0)]
        self.bottomrightCoor = [(50, 0), (40, 200), (90, 150), (-40, 140), (1,1)]
        super().__init__(zerocoor, health, owner, flipped, iframes)        #adding playerboxes specific to this character
    def abi1(self, tick):
        self.attack = "fireball"
        self.attack_start_tick = tick
        self.topleftCoor[2], self.bottomrightCoor[2] = maketlbr((40*self.flipmult, 10), (160*self.flipmult, 60))
        dmgboxlist.append(dmgbox((0, 0), (1,1), 10, self.owner, "fireball", tick, 20))
    def abi2(self, tick):
        self.attack = "kick"
        self.attack_start_tick = tick
        self.topleftCoor[4], self.bottomrightCoor[4] = maketlbr((40*self.flipmult, 150), (90*self.flipmult, 200))
        dmgboxlist.append(dmgbox((0,0), (1,1), 80, self.owner, "kick", tick, 60))
playerboxList = []
#a fighter is made up of boxes that should resemble it's body
class playerbox: #you don't give names to these objects, you append them to playerboxlist, so we can iterate the list in hitcheck()
    #global playerboxList
    def __init__(self, topleft, bottomright, owner, critx):
        self.topleft = topleft
        self.bottomright = bottomright
        self.owner = owner # "p1"  or "p2", those are strings
        self.critx = critx #the multiplier that is applied to dmg if it hits here. Example for head would be that critx is 2

import random

class SimpleAI:

    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent

    def update(self, tick):

        distance = self.opponent.zerocoor[0] - self.player.zerocoor[0]

        # turn towards opponent
        if distance > 0 and self.player.flipped:
            self.player.turn()

        if distance < 0 and not self.player.flipped:
            self.player.turn()

        # move closer
        if abs(distance) > 200:

            if distance > 0:
                self.player.zerocoor = tadd(self.player.zerocoor, (self.player.speed,0))
            else:
                self.player.zerocoor = tadd(self.player.zerocoor, (-self.player.speed,0))

        # attack
        if abs(distance) < 180 and self.player.can_attack(tick):

            r = random.random()

            if r < 0.4:
                self.player.abi1(tick)

            elif r < 0.8:
                self.player.abi2(tick)

            elif not self.player.jumping:
                self.player.jump(tick)

MAX_HEALTH = 500
# Player creation

def create_players(p1_choice, p2_choice):

    if p1_choice == "A":
        p1 = charA((300,500), MAX_HEALTH, "p1", False, 0)
    elif p1_choice == "B":
        p1 = charB((300,500), MAX_HEALTH, "p1", False, 0)
    else:
        p1 = charC((300,500), MAX_HEALTH, "p1", False, 0)

    if p2_choice == "A":
        p2 = charA((800,500), MAX_HEALTH, "p2", True, 0)
    elif p2_choice == "B":
        p2 = charB((800,500), MAX_HEALTH, "p2", True, 0)
    else:
        p2 = charC((800,500), MAX_HEALTH, "p2", True, 0)

    return p1, p2


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

# -----------------
# START SCREEN
# -----------------

title_font = pygame.font.Font('PressStart2P-Regular.ttf', 60)
menu_font = pygame.font.Font('PressStart2P-Regular.ttf', 25)
def mode_select_screen():

    waiting = True
    mode = 2

    while waiting:

        if background_img:
            screen.blit(background_img, (0,0))
        else:
            screen.fill((20,20,40))

        title = title_font.render("SELECT MODE", False, (255,255,255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 200))

        option1 = menu_font.render("E: 1 PLAYER (VS AI)", False, (255,255,0))
        option2 = menu_font.render("R: 2 PLAYERS", False, (255,255,0))

        screen.blit(option1, (SCREEN_WIDTH//2 - option1.get_width()//2, 350))
        screen.blit(option2, (SCREEN_WIDTH//2 - option2.get_width()//2, 420))
        screen.blit(arcadekeys_img, (400, 550))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:
                    mode = 1
                    waiting = False

                if event.key == pygame.K_r:
                    mode = 2
                    waiting = False

    return mode

def start_screen():

    waiting = True
    blink_timer = 0

    while waiting:

        if background_img:
            screen.blit(background_img, (0,0))
        else:
            screen.fill((20,20,40))

        # titel
        title_y = 100 + math.sin(pygame.time.get_ticks()*0.003)*10
        title_text = title_font.render("FIGHTER GAME", False, (255,255,255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, title_y))

        blink_timer += 1

        # blinking starting text
        if (blink_timer // 30) % 2 == 0:
            start_text = menu_font.render("PRESS Q TO START", False, (255,255,0))
            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 250))

        controls1 = menu_font.render("P1: WASD MOVE | E ABILITY1 | R ABILITY2 | X TURN", False, (200,200,200))
        controls2 = menu_font.render("P2: IJKL MOVE | O ABILITY1 | P ABILITY2 | M TURN", False, (200,200,200))
        screen.blit(controls1, (SCREEN_WIDTH//2 - controls1.get_width()//2, 350))
        screen.blit(controls2, (SCREEN_WIDTH//2 - controls2.get_width()//2, 400))
        quit_text = menu_font.render("ESC = QUIT", False, (180,180,180))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 480))
        screen.blit(arcadekeys_img, (400, 550))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    waiting = False

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


# New character select menu

def character_select_screen(mode):

    selecting = True
    p1_choice = None
    p2_choice = None

    while selecting:

        if background_img:
            screen.blit(background_img,(0,0))
        else:
            screen.fill((20,20,40))

        title = title_font.render("SELECT CHARACTER", False,(255,255,255))
        screen.blit(title,(SCREEN_WIDTH//2-title.get_width()//2,200))

        p1_text = menu_font.render("PLAYER 1: Q=A  E=B  R=C",False,(255,255,0))
        screen.blit(p1_text,(SCREEN_WIDTH//2-p1_text.get_width()//2,350))

        if mode == 2:
            p2_text = menu_font.render("PLAYER 2: U=A  O=B  P=C",False,(255,255,0))
            screen.blit(p2_text,(SCREEN_WIDTH//2-p2_text.get_width()//2,420))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if p1_choice == None:

                    if event.key == pygame.K_q: p1_choice = "A"
                    if event.key == pygame.K_e: p1_choice = "B"
                    if event.key == pygame.K_r: p1_choice = "C"

                elif mode == 2 and p2_choice == None:

                    if event.key == pygame.K_u: p2_choice = "A"
                    if event.key == pygame.K_o: p2_choice = "B"
                    if event.key == pygame.K_p: p2_choice = "C"

                else:
                    selecting = False

    if mode == 1:
        p2_choice = random.choice(["A","B","C"])

    return p1_choice, p2_choice

# audio
try:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)
    snd_sword_attack = pygame.mixer.Sound('Sword_attack.mp3')
    snd_regular_jump = pygame.mixer.Sound('Regular_jump.mp3')
    snd_rocket_jump = pygame.mixer.Sound('Rocket_jump.mp3')
    snd_hvy_punch = pygame.mixer.Sound('Hvy_punch.mp3')
    print(f"Loaded sounds: sword({snd_sword_attack.get_length():.2f}s), jump({snd_regular_jump.get_length():.2f}s)")
except Exception as e:
    print(f"Audio init/load failed: {e}")
    snd_sword_attack = snd_regular_jump = snd_rocket_jump = snd_hvy_punch = None

# helper for playing sounds (avoids repeated None checks)

def play_sound(sound_obj, name):
    if not sound_obj:
        return
    try:
        sound_obj.play()
    except Exception as e:
        print(f"Failed to play {name}: {e}")

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
spritesheet_p1laceholderbox = pygame.image.load('pixil-frame-0 (41).png').convert_alpha()   
spritesheet_p2laceholderbox = pygame.image.load('pixil-frame-0 (5).png').convert_alpha()   
spritesheet_arcadekeys = pygame.image.load('arcade-keys.png').convert_alpha()   

p1laceholderbox_img = pygame.Surface((20,20), pygame.SRCALPHA)  
p1laceholderbox_img.blit(spritesheet_p1laceholderbox, (0, 0)) 
p2laceholderbox_img = pygame.Surface((20,20), pygame.SRCALPHA)  
p2laceholderbox_img.blit(spritesheet_p2laceholderbox, (0, 0))   
arcadekeys_img = pygame.Surface((1320, 282), pygame.SRCALPHA)
arcadekeys_img.blit(spritesheet_arcadekeys, (0, 0))   
arcadekeys_img = pygame.transform.scale(arcadekeys_img, (650, 120))  

#placeholderbox_img = pygame.transform.scale(placeholderbox_img, (BALL_WIDTH, BALL_HEIGHT))  

spritesheet_red_placeholderbox = pygame.image.load('pixil-frame-0 (4).png').convert_alpha()   

red_placeholderbox_img = pygame.Surface((100, 100), pygame.SRCALPHA)  
red_placeholderbox_img.blit(spritesheet_red_placeholderbox, (0, 0))


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

def draw_healthbar(x, y, health, max_health, color):

    bar_width = 400
    bar_height = 35

    # achtergrond (pixel frame)
    pygame.draw.rect(screen, (30,30,30), (x-6, y-6, bar_width+12, bar_height+12))
    pygame.draw.rect(screen, (0,0,0), (x-4, y-4, bar_width+8, bar_height+8))

    # health percentage
    health_ratio = health / max_health
    current_width = int(bar_width * health_ratio)

    # health kleur
    pygame.draw.rect(screen, color, (x, y, current_width, bar_height))

    # pixel segments
    segment_width = 20
    for i in range(bar_width // segment_width):
        pygame.draw.line(
            screen,
            (0,0,0),
            (x + i*segment_width, y),
            (x + i*segment_width, y + bar_height),
            2
        )
def game_over_screen(winner):

    waiting = True
    blink = 0

    while waiting:

        if background_img:
            screen.blit(background_img, (0,0))
        else:
            screen.fill((10,10,20))

        # dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        # GAME OVER title
        title = title_font.render("GAME OVER", False, (255,60,60))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 180))

        # winner text
        win_text = menu_font.render(f"{winner} WINS!", False, (255,255,0))
        screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, 300))

        blink += 1

        # restart text
        if (blink // 30) % 2 == 0:
            restart_text = menu_font.render("PRESS Q TO RESTART", False, (200,200,200))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 420))

        quit_text = menu_font.render("ESC = QUIT", False, (180,180,180))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 480))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:

                    # reset players
                    p1.health = MAX_HEALTH
                    p2.health = MAX_HEALTH

                    p1.zerocoor = (300,500)
                    p2.zerocoor = (800,500)

                    dmgboxlist.clear()
                    playerboxList.clear()

                    waiting = False
                    startagain = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
# game loop
#

startagain = True
print('mygame is running')
running = True
while running:
    if startagain == True:
        tick = 0
        start_screen()

        mode = mode_select_screen()

        p1_choice, p2_choice = character_select_screen(mode)

        p1, p2 = create_players(p1_choice, p2_choice)

        if mode == 1:
            ai = SimpleAI(p2, p1)
        else:
            ai = None
        startagain = False

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                start_screen()
                mode = mode_select_screen()

                p1_choice, p2_choice = character_select_screen(mode)

                p1, p2 = create_players(p1_choice, p2_choice)

                dmgboxlist.clear()
                playerboxList.clear()

                if mode == 1:
                    ai = SimpleAI(p2, p1)
                else:
                    ai = None

                tick = 0


            if p1.can_attack(tick):

                if event.key == pygame.K_e:
                    p1.abi1(tick)
                if event.key == pygame.K_r:
                    p1.abi2(tick)
                if event.key == pygame.K_s and p1.jumping == False:
                    p1.crouch(tick)
                if event.key == pygame.K_w and p1.jumping == False:
                    p1.jump(tick)
                if event.key == pygame.K_x:
                    p1.turn()

            if mode == 2 and p2.can_attack(tick):
                if event.key == pygame.K_o:
                    p2.abi1(tick)
                if event.key == pygame.K_m:
                    p2.turn()
                if event.key == pygame.K_p:
                    p2.abi2(tick)
                if event.key == pygame.K_i and p2.jumping == False:
                    p2.jump(tick)
                if event.key == pygame.K_k and p2.jumping == False:
                    p2.crouch(tick)
                

     #           if event.key
    keys = pygame.key.get_pressed()
    #this next section can be much nicer I know, but it takes a long time and doesnt do much
    p1.speed = (5-2.5*p1.jumping + p1.speedboost)*p1.speedmult
    if p1.hitstunned:
        p1.speed *= 0.3
    p2.speed = (5-2.5*p2.jumping + p2.speedboost)*p2.speedmult
    if p2.hitstunned:
        p2.speed *= 0.3
    if keys[pygame.K_a] and p1.zerocoor[0] > 100:
        p1.zerocoor = tadd(p1.zerocoor, (-p1.speed, 0))
    if keys[pygame.K_d] and p1.zerocoor[0] < SCREEN_WIDTH - 100:
        p1.zerocoor = tadd(p1.zerocoor, (p1.speed, 0))
    if keys[pygame.K_j] and p2.zerocoor[0] > 100:
        p2.zerocoor = tadd(p2.zerocoor, (-p2.speed, 0))
    if keys[pygame.K_l] and p2.zerocoor[0] < SCREEN_WIDTH - 100:
        p2.zerocoor = tadd(p2.zerocoor, (p2.speed, 0))

            


    # 
    # handle damaging with boxes, simplified using for p in [p1, p2]
    # check every box, if it hit: deal dmg, give hitstun, stop boxes belonging to the same attack from damaging even more, stop the opponent attack
    for box in dmgboxlist:
        if box.hitcheck()[0]:
            for p in [p1, p2]:
                if p.owner == "p1":
                    opponent = p2
                else:
                    opponent = p1
                if box.owner == p.owner and opponent.iframes == 0:
                    opponent.health -= box.rawdmg * box.hitcheck()[1]
                    # create pixel hit effect
                    hit_x = (box.topleft[0] + box.bottomright[0]) // 2
                    hit_y = (box.topleft[1] + box.bottomright[1]) // 2

                    for i in range(8):
                        hit_effects.append([
                            hit_x,
                            hit_y,
                            math.cos(i * 0.8) * 6,
                            math.sin(i * 0.8) * 6,
                            10
                        ])
                    if box.hitstun > opponent.hitstunned:
                        opponent.hitstunned = box.hitstun
            
                    if box.rawdmg >= 1:
                        for box2 in dmgboxlist:
                            #if box belongs to dmg dealer: stop further attack, if it belong to dmg taker, act as if it has passed so the attack stops
                            if box2.owner == box.owner and box2.attackowner == box.attackowner: #if the box is owned by dmgdealer
                                box2.hitstun = 0
                                box2.rawdmg = 0 #then make that attack deal no damage because it had already hit
                            
    # 
    # draw everything
    # 
    if ai:
        ai.update(tick)
# clear screen / draw background 
    if background_img: 
        screen.blit(background_img, (0, 0)) 
    else: 
        screen.fill('blue')
    if keys[pygame.K_z]:
        screen.blit(arcadekeys_img, (400, 550))


    # draw players
    if not keys[pygame.K_BACKSPACE]:
        p1.draw()
        p2.draw()
        for p in [p1, p2]:
            if p.hitstunned:
                p.placeholderbox_img = red_placeholderbox_img
            else:
                if p.owner == "p1":
                    p.placeholderbox_img = p1laceholderbox_img
                else:
                    p.placeholderbox_img = p2laceholderbox_img
            for box in playerboxList:
                ''' NEXT 6 lines are for those numbers on the head that tell you if they can (be) attack(ed)
            if box.critx == 2 and box.owner == "p1":
                screen.blit(small_font.render(str(p1.iframes), False, (0, 0, 0)), box.topleft)
                screen.blit(small_font.render(str(p1.hitstunned), False, (0, 0, 0)), tadd(box.topleft, (50, 0)))
            if box.critx == 2 and box.owner == "p2": 
                screen.blit(small_font.render(str(p2.iframes), False, (0, 0, 0)), box.topleft)
                screen.blit(small_font.render(str(p2.hitstunned), False, (0, 0, 0)), tadd(box.topleft, (50, 0)))
            '''
                if box.owner == p.owner:
                    box.placeholderbox_img = pygame.transform.scale(p.placeholderbox_img, (box.bottomright[0] - box.topleft[0], box.bottomright[1] - box.topleft[1]))  
                    screen.blit(box.placeholderbox_img, box.topleft)



        p1.play(tick)
        p2.play(tick)
        for box in dmgboxlist:
            box.placeholderdmgbox_img = pygame.transform.scale(placeholderdmgbox_img, (box.bottomright[0] - box.topleft[0], box.bottomright[1] - box.topleft[1]))  #this gives an error when the player is moving faster back than the box is moving forward when creating, can ez be fixed but all dmgboxes will prob be faster
            screen.blit(box.placeholderdmgbox_img, box.topleft)
            # DRAW HIT EFFECTS
            for effect in hit_effects:

                effect[0] += effect[2]
                effect[1] += effect[3]
                effect[4] -= 1

                pygame.draw.rect(
                screen,
                    (255,220,50),
                    (effect[0], effect[1], 4, 4)
                )

            # remove finished effects
            hit_effects[:] = [e for e in hit_effects if e[4] > 0]
        #health points
        # HEALTH BARS
        draw_healthbar(40, 40, p1.health, MAX_HEALTH, (200,50,50))
        draw_healthbar(SCREEN_WIDTH-440, 40, p2.health, MAX_HEALTH, (50,120,220))
    
    # GAME OVER CHECK
    if p1.health <= 0:
        game_over_screen("PLAYER 2")
        startagain = True

    if p2.health <= 0:
        game_over_screen("PLAYER 1")
        startagain = True
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