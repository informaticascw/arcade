import pygame as pg

from components.gui.GUIComponent import GUIComponent
from collections.abc import Iterable, Callable
from util.constants import Constants
import components.effects
import components.gui

class Button(GUIComponent): # Text can be either components.gui.Text class and pos will be relative to button rect, or string.
    def __init__(self, rect:pg.Rect=None, borderRadius:int=-1, text:object=None, background:pg.Color|pg.Surface=Constants.COLOR_PRIMARY, color:pg.Color=Constants.COLOR_DARK, action:Callable=None, args:list=[], hover:pg.Color|Callable=Constants.COLOR_SECONDARY, shadow:components.effects.Shadow=None, outline:components.effects.Outline=None) -> None:
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
        super().__init__(rect, None, None)
        self.text = text
        self.background = background
        self.color = color
        self.borderRadius = borderRadius
        self.action = action
        self.args = args
        self.hoverStatus = False
        
        self.shadow = shadow
        self.outline = outline
        
        if isinstance(self.text, components.gui.Text):
            if self.text.pos == "centered":
                self.text.createImg(center=self.rect.center)
                self.text.pos = (self.text.rect[0], self.text.rect[1])
            else:
                self.text.pos[0] += self.rect[0]
                self.text.pos[1] += self.rect[1]

    def draw(self, surface:pg.Surface) -> None:
        if (self.background is None or isinstance(self.background, pg.Color)) and self.rect is None:
            raise Exception(f"Buttton must have either background image or rect to render")
        
        if isinstance(self.background, pg.Surface):
            surface.blit(self.background, self.rect)
        else:
            super().draw(surface)
            pg.draw.rect(surface, self.background, self.rect, border_radius=self.borderRadius)

            if self.text:
                if isinstance(self.text, components.gui.Text):
                    self.text.draw(surface)
                else:
                    fontImg = Constants.FONT.render(self.text, False, self.color, 24)
                    fontRect = fontImg.get_rect(center=self.rect.center)
                    surface.blit(fontImg, fontRect)
    
    def run(self):
        self.action(*self.args)

    # Setters -------------------------------------------------------------- #
    def setRect(self, rect:pg.Rect):
        if isinstance(self.background, pg.Surface):
            self.rect[0], self.rect[1], _, _, = rect
        else: self.rect = rect
        
    def setBorderRadius(self, borderRadius:int):
        self.borderRadius = borderRadius

    def setText(self, text:str):
        self.text = text

    def setAction(self, action:Callable, args:list=Iterable[any]):
        self.action = action
        self.args = args

    def setHoverAction(self, HoverAction:pg.Color|Callable):
        self.HoverAction = HoverAction