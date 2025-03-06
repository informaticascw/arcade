import pygame as pg
import sys

from util.data import data
from util.constants import Constants
from util.data import data
from util.games import start_game

game_positions = []
for i in range(2):
    for j in range(3):
        game_positions.append(list(reversed([i, j])))

class EventHandler():
    def __init__(self, menu):
        self.menu = menu
        
    def handleEvent(self):
        events = pg.event.get()
        for event in events:
            match event.type:
                case pg.QUIT:
                    data.save()
                    self.menu.running = False
                    sys.exit()
                case pg.KEYDOWN:
                    self.eventKeydown(event)
 
    def eventKeydown(self, event) -> None:
        sel = self.menu.selection
        slide = self.menu.slides[self.menu.slideIndex]
        
        newSelection = list(self.menu.selection)
        
        match event.key:
            case pg.K_ESCAPE:
                self.menu.running = False
                data.save()
                pg.quit()
            case pg.K_w:
                newSelection[1] -= 1
            case pg.K_a:
                newSelection[0] -= 1
            case pg.K_s:
                newSelection[1] += 1
            case pg.K_d:
                newSelection[0] += 1
            case pg.K_q:
                index = game_positions.index(sel)

                try:
                    slide.components.buttons[index].run()
                except:
                    pass # error popup maybe ~
                
        if newSelection in game_positions and -1 < game_positions.index(newSelection) < len(slide.batch):
                self.menu.selection = newSelection
        else:
            # Selection is out of bounds
            print(f"{Constants.CNSL_INFO}[Events] Selection out of bounds{Constants.CNSL_RESET}")
            if len(self.menu.slides) == 1:
                return

            if newSelection[0] > self.menu.selection[0]:
                if self.menu.slideIndex + 1 > len(self.menu.slides) - 1:
                    self.menu.slideIndex = 0
                else:
                    self.menu.slideIndex += 1
            
            if newSelection[0] < 0:
                if self.menu.slideIndex - 1 < 0:
                    self.menu.slideIndex = len(self.menu.slides) - 1
                else:
                    self.menu.slideIndex -= 1
                    
            btns = self.menu.slides[self.menu.slideIndex].components.buttons
            print(btns[:3])
            possibleBtns = btns[3:] or btns[:3] if self.menu.selection[1] > 0 else btns[:3]
            index = btns.index(possibleBtns[:1][0])
            
            self.menu.selection = game_positions[index]