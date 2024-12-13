import pygame as pg
from components.gui.GUIComponent import GUIComponent
from collections.abc import Iterable
import components.effects

class Image(GUIComponent):
    def __init__(self, pos:Iterable, source:str, shadow:components.effects.Shadow=None, outline:components.effects.Outline=None):
        self.image = pg.image.load(source)
        _, _, w, h, = self.image.get_rect()
        self.pos = pos
        self.rect = pg.Rect(pos[0], pos[1], w, h)
        super().__init__(self.rect, shadow, outline)
        
    def draw(self, surface:pg.Surface) -> None:
        super().draw(surface)
        surface.blit(self.image, self.pos)