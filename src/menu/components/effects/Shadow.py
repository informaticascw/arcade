import pygame as pg
from collections.abc import Iterable

class Shadow():
    def __init__(self, pos:Iterable, color:pg.Color, blur:int) -> None:
        """Shadow effect for components

        Args:
            pos (Iterable): Shadow position relative to the component position.
            color (pg.Color): Color to render the shadow in.
            blur (int): Shadow blur
        """
        self.pos = pos
        self.color = color
        self.blur = blur