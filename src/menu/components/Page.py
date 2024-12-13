import pygame as pg
import components.gui.Image as Image

from collections.abc import Iterable

class ComponentCollection:
	def __init__(self, buttons:Iterable=[], inputs:Iterable=[], switches:Iterable=[], images:Iterable=[], text:Iterable=[]):
		"""Page components container
		Creates a container to store all the components to be part of of a page
	
		Args:
			buttons (Iterable): Iterable of Button() objects
			inputs (Iterable): Iterable of Input() objects
			images (Iterable): Iterable of Image() objects
			text (Iterable): Iterable of Text() objects
		"""
		self.buttons = buttons
		self.switches = switches
		self.images = images
		self.textAreas = text

class Page:
	def __init__(self, name:str, background:pg.Color|object, components:ComponentCollection) -> None:
		"""Class to hold all properties of a page in order to render it
		Creates a container of page properties to be rendered
	
		Args:
			name (str): Name of the page *MUST BE UNIQUE TO THE PAGE*
			background (pg.Color|components.Image): Background of the page, can be either color or image
			components (ComponentCollection): A collection of page components
		"""
		self.name = name
		self.imageBg = not isinstance(background, pg.Color)
		self.background = background
		
		self.components = components
  
	def render(self, surface:pg.Surface) -> None:
		"""Render the page onto a pygame surface

		Args:
			surface (pg.Surface): Surface to render the page onto
		"""

		if isinstance(self.background, pg.Surface): surface.blit(self.background, (0, 0))
		elif isinstance(self.background, Image): self.background.draw(surface)
		else: surface.fill(self.background)
  
		componentTypes = set(self.components.__dict__)
		for type in componentTypes:
			if len(self.components.__dict__.get(type)) > 0:
				for component in self.components.__dict__.get(type):
					component.update()
					component.draw(surface)