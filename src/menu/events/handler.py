import pygame as pg
import sys

from util.data import data
from util.constants import Constants
from util.data import data

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
        match event.key:
            case pg.K_ESCAPE:
                data.save()
                pg.quit()
            case pg.K_w:
                print("W")
                self.menu.selection[1] -= 1
            case pg.K_a:
                print("A")
                self.menu.selection[0] -= 1
            case pg.K_s:
                print("S")
                self.menu.selection[1] += 1
            case pg.K_d:
                print("D")
                self.menu.selection[0] += 1
        
        