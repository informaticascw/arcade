import pygame as pg
import time
from util.constants import Constants

class Screensaver:
    def __init__(self):
        # lines to render on the screensaver image
        # Each dict: text, font_size, color, y_offset (relative to center)
        PINK = (255, 0, 128)
        WHITE = (255, 255, 255)
        lines = [
            {"text": "HIT ANY KEY", "font_size": 80, "color": PINK, "y_offset": -220},
            {"text": "LET'S PLAY!", "font_size": 120, "color": PINK, "y_offset": -60},
            {"text": "games gemaakt door leerlingen", "font_size": 80, "color": PINK, "y_offset": 220},
            {"text": "4e klas informatica", "font_size": 80, "color": PINK, "y_offset": 380},
            {"text": Constants.SCREENSAVER_MESSAGE_OF_THE_DAY, "font_size": 40, "color": WHITE, "y_offset": 460},
        ]

        # Prepare fonts by size
        font_cache = {}
        for line in lines:
            size = line["font_size"]
            if size not in font_cache:
                font_cache[size] = pg.font.Font(Constants.SCREENSAVER_FONT_PATH, size)

        # Create a transparent surface for the screensaver image
        self.image = pg.Surface(Constants.RESOLUTION, pg.SRCALPHA)

        # Render and blit each line
        for line in lines:
            font = font_cache[line["font_size"]]
            text_surf = font.render(line["text"], True, line["color"])
            rect = text_surf.get_rect(center=(Constants.RESOLUTION[0] // 2, Constants.RESOLUTION[1] // 2 + line["y_offset"]))
            self.image.blit(text_surf, rect)

        self._active = False

        # Create an semi transparant dark overlay surface between the screensaver and the background
        self.overlay = pg.Surface(Constants.RESOLUTION, pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, Constants.SCREENSAVER_OVERLAY_OPACITY))  # Opacity from Constants

        # Define the flexible animation sequence
        # Each dict in config represents a state with a mode and duration (in ms)
        # modes: "scroll", "invisible", "visible"
        self.config = [
            {"mode": "scroll", "duration": 500},
            {"mode": "visible", "duration": 2000},
            {"mode": "invisible", "duration": 250},
            {"mode": "visible", "duration": 500},
            {"mode": "invisible", "duration": 250},
            {"mode": "visible", "duration": 500},
            {"mode": "invisible", "duration": 250},
            {"mode": "visible", "duration": 10000},
        ]
        self.reset()

    @property
    def active(self):
        return self._active

    def reset(self):
        self.state_index = 0
        self.scroll_y = Constants.RESOLUTION[1]
        self.visible = True
        self.last_update = time.time()
        self._set_state(self.config[0])

    def activate(self):
        print("Screensaver activated!")
        self._active = True
        self.reset()

    def deactivate(self):
        self._active = False

    def _set_state(self, state):
        self.current_mode = state["mode"]
        self.current_duration = state["duration"] / 1000.0  # ms to seconds
        self.state_start_time = time.time()
        # For scroll, reset position
        if self.current_mode == "scroll":
            self.scroll_y = Constants.RESOLUTION[1]
            self.scroll_speed = Constants.RESOLUTION[1] / self.current_duration

    def update(self):
        if not self._active:
            return

        now = time.time()

        # Handle the current animation mode
        match self.current_mode:
            case "scroll":
                elapsed = now - self.last_update
                self.scroll_y -= self.scroll_speed * elapsed
                if self.scroll_y <= 0:
                    self.scroll_y = 0
                self.visible = True
            case "invisible":
                self.visible = False
            case "visible":
                self.visible = True

        # Check if it's time to move to the next state
        if now - self.state_start_time >= self.current_duration:
            self.state_index += 1
            if self.state_index >= len(self.config):
                self.state_index = 0  # Loop the sequence
            self._set_state(self.config[self.state_index])
        self.last_update = now

    def render(self, surface: pg.Surface):
        if not self._active:
            return
        
        surface.blit(self.overlay, (0, 0))
        if self.visible:
            surface.blit(self.image, (0, int(self.scroll_y)))