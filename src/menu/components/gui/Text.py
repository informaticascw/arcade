import pygame as pg

import components
import components.effects
from components.gui.GUIComponent import GUIComponent
from collections.abc import Iterable, Callable
from util.constants import Constants

class Text(GUIComponent):
	def __init__(self, value:str, color:pg.Color, size:int, pos:Iterable, outline:components.effects.Outline=None, shadow:components.effects.Shadow=None):
		self.value = value
		self.color = color
		self.size = size
		self.pos = pos
		self.outline = outline
		self.shadow = shadow

	def draw(self, surface:pg.Surface) -> None:
		img = Constants.FONT.render(self.value, True, self.color, 96)
		img.get_rect()[0], img.get_rect()[1] = self.pos
		surface.blit(img, img.get_rect())

	def setFont(self, font:components.Font) -> None:
		self.font = font
  
	def setSize(self, size:int) -> None:
		self.size = size
  
	def setPos(self, pos:Iterable) -> None:
		self.pos = pos
  
	def setOutline(self, outline:components.effects.Outline) -> None:
		self.outline = outline
  
	def setShadow(self, shadow:components.effects.Shadow) -> None:
		self.shadown = shadow