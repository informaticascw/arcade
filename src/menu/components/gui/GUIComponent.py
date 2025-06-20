import pygame as pg
from collections.abc import Iterable
import components
from util.constants import Constants
import components.effects
class GUIComponent:
    """Base class for all gui components.
    """
    
    def __init__(self, rect:pg.Rect, shadow:components.effects.Shadow=None, outline:components.effects.Outline=None) -> None: 
        self.rect = rect
        self.transition = False
        self.shadow = shadow
        self.outline = outline

    def draw(self, surface:pg.Surface) -> None:
        borderRadius = self.__dict__.get("borderRadius") if not self.__dict__.get("borderRadius") is None else -1
        if self.shadow:
            # For text render the font image rather than the rect
            if isinstance(self, components.gui.Text):
                img = Constants.FONT.render(self.value, True, self.shadow.color, self.size)
                rect = pg.Rect(*self.rect)
                rect[0] += self.shadow.offset[0]
                rect[1] += self.shadow.offset[1]
                surface.blit(img, rect)
            else:
                rect = pg.Rect(*self.rect)
                rect[0] += self.shadow.offset[0]
                rect[1] += self.shadow.offset[1]
                pg.draw.rect(surface, self.shadow.color, rect, border_radius=borderRadius)

        if self.outline:
            if isinstance(self, components.gui.Button):
                if not self.hoverStatus: return
                
            if isinstance(self, components.gui.Text):
                for i in range(4):
                    rect = pg.Rect(*self.rect)
                    if i < 2: rect[i % 2] -= self.outline.width
                    if i > 1: rect[i % 2] += self.outline.width
                    img = Constants.FONT.render(self.value, True, self.outline.color, self.size)
                    surface.blit(img, rect)
            else:
                rect = pg.Rect(*self.rect)
                rect[0] -= self.outline.width
                rect[1] -= self.outline.width
                rect[2] += self.outline.width * 2
                rect[3] += self.outline.width * 2
                pg.draw.rect(surface, self.outline.color, rect, border_radius=borderRadius)
        
    def update(self) -> None:
        pass
        
    def setBackground(self, background:pg.Rect|pg.Surface):
        self.background = background
        if isinstance(background, pg.Surface):
            if self.rect is None:
                self.rect = self.background.get_rect()
            else: _, _, self.rect[2], self.rect[3] = self.background.get_rect()
        
    def translate(self, pos:Iterable, transitionSpeed:int) -> None:
        """Translate the position of gui component.

        Args:
            pos (Iterable): New component position.
            transitionSpeed (int): Speed of the translation.
        """
        self.transition = True
        