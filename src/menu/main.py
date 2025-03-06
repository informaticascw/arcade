import pygame as pg
import sys, os

sys.path.append(os.path.join(os.getcwd(), "src"))

import components
from util.constants import Constants

pg.init()
Constants.FONT = components.Font()

from util.data import data
from util.games import fetchGames

from events.handler import EventHandler

class Menu:
	def __init__(self) -> None:
		self.eventsHandler:EventHandler = EventHandler(self)

		self.screen = pg.display.set_mode(Constants.RESOLUTION, Constants.DISPLAY_MODE)
		self.clock:pg.time.Clock = pg.time.Clock()

		self.running = True
  
		self.slideIndex = 0
		self.selection = [0, 0]
  
		self.games = fetchGames()

		print(f"{Constants.CNSL_DATA}[GAMES]: {list(map(lambda game : game.name, self.games))}{Constants.CNSL_RESET}")
		print(f"{Constants.CNSL_DATA}[DATA.JSON]: {data.data}{Constants.CNSL_RESET}")

		self.batches = [self.games[i:i + 6] for i in range(0, len(self.games), 6)]
		self.slides = [components.Slide(self, batch) for batch in self.batches]
  
		self.header = components.gui.Text("STANISLAS ARCADE", Constants.COLOR_PRIMARY, 108, ("center", 100), shadow=components.effects.Shadow((10, -2), Constants.COLOR_SECONDARY))
		self.background = pg.image.load("assets/menu_background.jpg")

	def run(self) -> None:
		while self.running:

			# Handle events
			self.eventsHandler.handleEvent()
   
			self.render()
			
			# Stop the cursor from rendering
			pg.mouse.set_visible(False)

			pg.display.update()
			self.clock.tick(Constants.FPS)

	def render(self):
		# Clear the screen
		self.screen.fill((0, 0, 0))
		self.screen.blit(self.background, (0, 0))
		self.header.draw(self.screen)

		# Render the page onto the screen
		self.slides[self.slideIndex].update()
		self.slides[self.slideIndex].render(self.screen)

if __name__ == "__main__":
	Menu().run()
