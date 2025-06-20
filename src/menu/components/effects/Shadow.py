import pygame as pg
from collections.abc import Iterable

class Shadow():
    def __init__(self, offset:Iterable, color:pg.Color) -> None:
        """Shadow effect for components

        Args:
            offset (Iterable): Shadow position relative to the component position.
            color (pg.Color): Color to render the shadow in.
        """
        self.offset = offset
        self.color = color