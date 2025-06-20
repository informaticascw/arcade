import pygame as pg

from util.constants import Constants
from components import ComponentCollection
from components.gui import Button
from components.effects import Outline
from util.games import start_game

game_positions = []
for i in range(2):
    for j in range(3):
        game_positions.append(list(reversed([i, j])))

class Slide:
    def __init__(self, menu, batch):
        self.menu = menu
        self.batch = batch
        
        self.components = ComponentCollection(
            buttons=[
                Button(
                rect=pg.Rect(game_positions[index][0] * 350 + 6, game_positions[index][1] * 260 + 6, 290, 180),
                borderRadius=8,
                text=game.name,
                background=pg.Color("gray"),
                color=pg.Color(Constants.COLOR_DARK),
                action=start_game,
                args=[game.entrypoint],
                hover=False,
                outline=Outline(Constants.COLOR_PRIMARY, 6)
            ) for index, game in enumerate(batch)
            ]
        )
        
        x, y, w, h = pg.Rect(game_positions[5][0] * 350, game_positions[5][1] * 260, 290, 180)
        self.surface = pg.Surface((x+w + 12, y+h + 12))
        self.surface.set_colorkey((0, 0, 0))
    
    def render(self, surface:pg.Surface):
        size = surface.get_size()
        self_size = self.surface.get_size()

        surface.blit(self.surface, (size[0] / 2 - self_size[0] / 2, size[1] / 2 - self_size[1] / 2 + 80))
        
    def update(self):
        self.surface.fill((0, 0, 0))
        
        for btn in self.components.buttons:
            btn.hoverStatus = False
        
        ind = game_positions.index(self.menu.selection)
        self.components.buttons[ind].hoverStatus = True
        
        for btn in self.components.buttons:
            btn.update()
            btn.draw(self.surface)