import pygame as pg

from components.gui.GUIComponent import GUIComponent
from collections.abc import Iterable, Callable
from util.constants import Constants

class Button(GUIComponent):
    def __init__(self, rect:pg.Rect=None, borderRadius:int=-1, value:str=None, background:pg.Color|pg.Surface=Constants.BUTTON_INACTIVE, color:pg.Color=Constants.BUTTON_COLOR, action:Callable=None, args:list=[], hover:pg.Color|Callable=Constants.BUTTON_HOVER) -> None:
        """Generate a button class

        Args:
            rect (pg.Rect): Pygame rectangle to represent the shape of the button\
            borderRadius (int): Border radius of the rect to be rendered
            background (Color): Background color of the button
            color (Color): Font color for the button
            action (Callable): Function to run when button is pressed
            args (list): Arguments to be passed down the action function
            hover (Color|Callable): The button to change to when hovered
        """
        super().__init__(rect, value, background, color)
        self.borderRadius = borderRadius
        self.action = action
        self.args = args
        self.hover = hover
        self.hoverStatus = False

    def draw(self, surface:pg.Surface) -> None:
        if self.background is None or isinstance(self.background, pg.Color) and self.rect is None:
            raise Exception(f"Buttton must have either background image or rect to render")
        
        if isinstance(self.background, pg.Surface):
            surface.blit(self.background, self.rect)
        else:
            rectBg = self.background if isinstance(self.hover, Callable) else self.hover if self.hoverStatus else self.background
            pg.draw.rect(surface, rectBg, self.rect, border_radius=self.borderRadius)
            if not self.value is None:
                fontImg = Constants.FONT.render(self.value, False, self.color)
                fontRect = fontImg.get_rect(center=self.rect.center)
                surface.blit(fontImg, fontRect)
            
    def update(self):
        mx, my = pg.mouse.get_pos()
        self.hoverStatus = self.rect.collidepoint((mx, my))
    
    def run(self):
        self.action(*self.args)

    # Setters -------------------------------------------------------------- #
    def setRect(self, rect:pg.Rect):
        if isinstance(self.background, pg.Surface):
            self.rect[0], self.rect[1], _, _, = rect
        else: self.rect = rect
        
    def setBorderRadius(self, borderRadius:int):
        self.borderRadius = borderRadius

    def setValue(self, value:str):
        self.value = value

    def setAction(self, action:Callable, args:list=Iterable[any]):
        self.action = action
        self.args = args

    def setHoverAction(self, HoverAction:pg.Color|Callable):
        self.HoverAction = HoverAction