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
  
		self.img = None
		self.rect = None

	def draw(self, surface:pg.Surface) -> None:
		self.createImg()
		self.rect[0], self.rect[1] = self.pos
		super().draw(surface)
		surface.blit(self.img, self.rect)

	def createImg(self, center=None) -> pg.Surface:
		self.img = Constants.FONT.render(self.value, True, self.color, self.size)
		if center: self.rect = self.img.get_rect(center=center)
		else: self.rect = self.img.get_rect()
		return self.img

    # Setters -------------------------------------------------------------- #
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