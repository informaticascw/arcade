import sys
import pygame as pg
from util.data import data
from util.constants import Constants
from util.router import router

class EventHandler():
    def __init__(self, game):
        self.game = game
        
    def handleEvent(self):
        events = pg.event.get()
        for event in events:
            match event.type:
                case pg.QUIT:
                    data.save()
                    sys.exit()
                case pg.KEYDOWN:
                    self.eventKeydown(event)
                case pg.MOUSEBUTTONDOWN:
                    self.eventMouseButton(event)
 
    def eventKeydown(self, event) -> None:
        if event.key == pg.K_ESCAPE:
            pg.quit()

        if event.key == pg.K_F11:
            pg.display.toggle_fullscreen()
            data.data["displayMode"] = 1 if pg.display.is_fullscreen() else 0

        if event.key == pg.K_UP:
            index = Constants.SUPPORTED_RESOLUTIONS.index(tuple(data.data["resolution"]))
            index += 1
            if index == len(Constants.SUPPORTED_RESOLUTIONS): index = 0
            data.data["resolution"] = Constants.SUPPORTED_RESOLUTIONS[index]
        if event.key == pg.K_DOWN:
            index = Constants.SUPPORTED_RESOLUTIONS.index(tuple(data.data["resolution"]))
            data.data["resolution"] = Constants.SUPPORTED_RESOLUTIONS[index - 1]

        if event.key == pg.K_f:
            if self.game.page == router.pages["settings"]: router.redirect("main")
            if self.game.page == router.pages["main"]: router.redirect("settings")

    def eventMouseButton(self, event) -> None:
        for button in self.game.page.components.buttons:
            if button.rect.collidepoint(event.pos):
                if button.action == "redirect":
                    router.redirect(*button.args)
                else: button.action(*button.args)