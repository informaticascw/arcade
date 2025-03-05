import pygame as pg

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
                rect=pg.Rect(game_positions[index][0] * 350 + 4, game_positions[index][1] * 260 + 4, 275, 180),
                borderRadius=8,
                text=game.name,
                background=pg.Color("gray"),
                color=pg.Color("aqua"),
                action=start_game,
                args=[game.entrypoint],
                hover=False,
                outline=Outline(pg.Color("aqua"), 3)
            ) for index, game in enumerate(batch)
            ]
        )
        
        x, y, w, h = pg.Rect(game_positions[5][0] * 350, game_positions[5][1] * 260, 275, 180)
        self.surface = pg.Surface((x+w + 8, y+h + 8))
        self.surface.set_colorkey((0, 0, 0))
    
    def render(self, surface:pg.Surface):
        size = surface.get_size()
        self_size = self.surface.get_size()

        surface.blit(self.surface, (size[0] / 2 - self_size[0] / 2, size[1] / 2 - self_size[1] / 2))
        
    def update(self):
        for btn in self.components.buttons:
            btn.hoverStatus = False
        
        ind = game_positions.index(self.menu.selection)
        self.components.buttons[ind].hoverStatus = True
        
                
        for btn in self.components.buttons:
            print(btn.hoverStatus)
            btn.update()
            btn.draw(self.surface)