import pygame as pg
from collections.abc import Iterable

class GUIComponent:
    """Base class for all gui components, default
    """
    
    def __init__(self, rect:pg.Rect, value:str, background:pg.Rect|pg.Surface, color:pg.Color) -> None: 
        self.rect = rect
        self.value = value
        self.background = background
        self.color = color
        self.transition = False

    def draw(self, screen) -> None:
        pg.draw.rect(screen, self.background, self.rect)
        for textArea in self.textAreas:
            textArea.render(self.value, )
    
    def animate(self) -> None:
        pass
    
    def update(self, event) -> None:
        pass
            
    def setValue(self, value:str) -> None:
        self.value = value
        
    def setBackground(self, background:pg.Rect|pg.Surface):
        self.background = background
        if isinstance(background, pg.Surface):
            if self.rect is None:
                self.rect = self.background.get_rect()
            else: _, _, self.rect[2], self.rect[3] = self.background.get_rect()
    
    def setColor(self, color:pg.Color) -> None:
        self.color = color
        
    def translate(self, pos:Iterable, transitionSpeed:int) -> None:
        """Translate the position of gui component

        Args:
            pos (Iterable): New component position.
            transitionSpeed (int): Speed of the translation.
        """
        self.transition = True
        