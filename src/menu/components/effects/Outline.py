import pygame as pg

class Outline():
    def __init__(self, color:pg.Color, width:int, pos:int=0) -> None:
        self.color = color
        self.width = width
        self.pos = pos # 0: inside 1: outside