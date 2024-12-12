import pygame as pg
from util.constants import Constants

class Font(pg.font.Font):
    def __init__(self, path_to_font:str="./assets/font.ttf"):
        self.path_to_font:str = path_to_font
        
    def render(self, text:str|bytes|None,antialias:bool, color:pg.Color, size:int=None, background:pg.Color=None) -> pg.Surface:
        return pg.font.Font(self.path_to_font, size).render(text, antialias, color, background)