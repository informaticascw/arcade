import pygame as pg

class Outline():
    def __init__(self, color:pg.Color, width:int) -> None:
        self.color = color
        self.width = width