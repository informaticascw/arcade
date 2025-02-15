import sys
import pygame as pg
from util.data import data
from util.constants import Constants
from util.router import router
from util.data import data

class EventHandler():
    def __init__(self, game):
        self.game = game
        
    def handleEvent(self):
        events = pg.event.get()
        for event in events:
            match event.type:
                case pg.QUIT:
                    data.save()
                    self.game.running = False
                    sys.exit()
                case pg.KEYDOWN:
                    self.eventKeydown(event)
                case pg.MOUSEBUTTONDOWN:
                    self.eventMouseButton(event)
 
    def eventKeydown(self, event) -> None:
        if event.key == pg.K_ESCAPE:
            data.save()
            pg.quit()

    def eventMouseButton(self, event) -> None:
        for button in self.game.page.components.buttons:
            if button.rect.collidepoint(event.pos):
                if button.action == "redirect":
                    router.redirect(*button.args)
                else: button.action(*button.args)