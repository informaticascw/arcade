import pygame as pg
import time
from util.constants import Constants

class Screensaver:
    def __init__(self):
        # Load and scale the screensaver image with alpha support
        self.image = pg.image.load(Constants.SCREENSAVER_IMAGE_PATH).convert_alpha()
        self.image = pg.transform.scale(self.image, Constants.RESOLUTION)
        # Track the time (in ms) since the screensaver started
        self.start_time_ms = int(time.time() * 1000)
        self._active = False

    @property
    def active(self):
        return self._active

    def activate(self):
        print("Screensaver activated!")
        self._active = True
        self.start_time_ms = int(time.time() * 1000)

    def deactivate(self):
        self._active = False

    def render(self, surface: pg.Surface):
        if self._active:
            surface.blit(self.image, (0, 0))