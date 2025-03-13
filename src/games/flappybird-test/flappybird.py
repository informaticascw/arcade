import sys

import pygame as pg

from scripts.bird import Bird
from scripts.pipe import Pipe
from scripts.util import load_image, load_images, Animation, Button

class Game:
	def __init__(self):
		pg.init()
		self.running = False

		self.display = pg.Surface((288, 512))
		self.screen = pg.display.set_mode((1920, 1080))
		pg.display.set_caption("Flappybird")
		self.clock = pg.time.Clock()
		self.dt = 1

		self.started = False
		
		self.header_font = pg.font.Font("assets/fonts/flappy-bird.ttf", 65)
		self.txt_font = pg.font.Font("assets/fonts/flappy-bird.ttf", 35)
		
		self.assets = {
			"background": load_image("background.png"),
			"base": load_image("base.png"),
			"pipe": load_image("pipe.png"),
			"bird_1": Animation(load_images("bird_01"), img_dur=15),
			"bird_2": Animation(load_images("bird_02"), img_dur=15),
			"numbers": load_images("numbers"),
			"gameover": load_image("huds/gameover.png")
		}
		self.sfx = {
			"die": pg.mixer.Sound("assets/audio/die.wav"),
			"hit": pg.mixer.Sound("assets/audio/hit.wav"),
			"point": pg.mixer.Sound("assets/audio/point.wav"),
			"swoosh": pg.mixer.Sound("assets/audio/swoosh.wav"),
			"wing": pg.mixer.Sound("assets/audio/wing.wav"),
		}
		self.sfx["die"].set_volume(0.4)
		self.sfx["hit"].set_volume(0.3)
		self.sfx["point"].set_volume(0.2)
		self.sfx["swoosh"].set_volume(0.4)
		self.sfx["wing"].set_volume(0.3)

		self.constants = {
			"gravity": 280,
			"jump_strength": 140,
			"horizontal_velocity": 65,
			"gap": 82,
			"pipe_dist": 120,
		}
		
		self.birds = []
		self.alive_birds = 0
		self.bases = [0, self.assets["base"].get_width()]
		self.pipes = [Pipe(self, 160)]

		self.inMenu = True
		self.menuButtons = [Button(pg.Rect(self.display.get_width() / 2 - 100, 200, 200, 60), "1 Player", self.txt_font, hovering=True),
                      		Button(pg.Rect(self.display.get_width() / 2 - 100, 300, 200, 60), "2 Players", self.txt_font)
                        ]
		self.hovering = 1

	def run(self):
		self.running = True
		# Game loop -------------------------------------------------------------------------------------#
		while self.running:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						pg.quit()
						sys.exit()

					if self.inMenu:
						if event.key == pg.K_s:
							self.hovering = 2
							self.menuButtons[1].hovering = True
							self.menuButtons[0].hovering = False
						if event.key == pg.K_w:
							self.hovering = 1
							self.menuButtons[0].hovering = True
							self.menuButtons[1].hovering = False
						if event.key == pg.K_q:
							for i in range(self.hovering):
								self.birds.append(Bird(self, i + 1))
								self.alive_birds = len(self.birds)
								self.inMenu = False
  
					if not self.inMenu:
						if event.key == pg.K_SPACE and not self.birds[0].dead:
							if not self.started: self.start()
							self.birds[0].jump = True
							self.sfx["wing"].play()

						if len(self.birds) > 1:
							if event.key == pg.K_q and not self.birds[1].dead:
								if self.started:
									self.birds[1].jump = True
									self.birds[1].gravity = True
									self.sfx["wing"].play()
							
						if event.key == pg.K_r:
							self.reset()

			# Render Game ------------------------------------------------------------------------------#
			self.display.fill((0, 0, 0))
			self.display.blit(self.assets["background"], (0, 0))
   
			self.assets[f"bird_1"].update()
			self.assets[f"bird_2"].update()
			
			if self.inMenu:
				for button in self.menuButtons:
					button.render(self.display)

			if not self.inMenu:
				# Rendering the pipes ------------------------------------------------------------------#
				alive_birds = 0
				for bird in self.birds:
					alive_birds += not bird.dead
				self.alive_birds = alive_birds > 0
					
				if self.started:
					for pipe in self.pipes:
						if self.alive_birds:
							pipe.update()
						pipe.render(self.display)
						
					self.pipes = list(filter(lambda pipe : not (pipe.pos + self.assets["pipe"].get_width() < 0), self.pipes))
					if self.display.get_width() - (self.pipes[-1].pos + self.assets["pipe"].get_width()) >= (self.constants["pipe_dist"] - 20):
						self.pipes.append(Pipe.random(self))
				
				# Rendering the bird -------------------------------------------------------------------#
				for bird in self.birds:
					bird.update()
					bird.render(self.display)
					
			# Rendering the ground ---------------------------------------------------------------------#
			for index in range(len(self.bases)):
				if self.alive_birds or self.inMenu:
					self.bases[index] -= self.constants["horizontal_velocity"] * self.dt
				self.display.blit(self.assets["base"], (self.bases[index], self.display.get_height() - self.assets["base"].get_height()))
			
			self.bases = list(filter(lambda base : not (base + self.assets["base"].get_width() < 0), self.bases))
			if len(self.bases) < 2:
				self.bases.append(self.bases[0] + self.assets["base"].get_width())
					
			# Rendering the title at start -------------------------------------------------------------#
			if not self.started:
				msg = self.header_font.render("Flappybird", False, (255, 255, 255))
				self.display.blit(msg, (self.display.get_width() / 2 - msg.get_width() / 2, 50))
			
			# Scaling to full up large screen ----------------------------------------------------------#
			scaled_surf = pg.transform.scale_by(self.display, 2.109375) # 1080/512 = 2.109375
			self.screen.blit(scaled_surf, (self.screen.get_width() / 2 - scaled_surf.get_width() / 2, 0))
			
			pg.display.flip()
			self.dt = self.clock.tick(60) / 1000
		
	def start(self):
		self.started = True
		
		for bird in self.birds:
			bird.gravity = True
		
	def reset(self):
		self.started = False
		self.pipes = [Pipe(self, 160)]
		self.birds = []
		self.inMenu = True
		
		
		
if __name__ == "__main__":
	Game().run()