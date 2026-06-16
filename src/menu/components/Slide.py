import pygame as pg

from util.constants import Constants
from components import ComponentCollection
from components.gui import Button
from components.effects import Outline
from util.games import start_game
from components.default_screenshot import create_starry_placeholder

TILE_WIDTH = 300
TILE_HEIGHT = 168
TILE_X_SPACING = 330
TILE_Y_SPACING = 250
TEXT_TOP_MARGIN = 10
LABEL_FONT_SIZE = 22
LABEL_MAX_LINES = 2
LABEL_LINE_SPACING = 4
LABEL_SIDE_PADDING = 10

game_positions = []
for row in range(Constants.MENU_GRID_ROWS):
    for col in range(Constants.MENU_GRID_COLS):
        game_positions.append([col, row])

class Slide:
    def __init__(self, menu, batch):
        self.menu = menu
        self.batch = batch
        self._placeholder = create_starry_placeholder((TILE_WIDTH, TILE_HEIGHT))
        
        self.components = ComponentCollection(
            buttons=[
                Button(
                rect=pg.Rect(game_positions[index][0] * TILE_X_SPACING + 6, game_positions[index][1] * TILE_Y_SPACING + 6, TILE_WIDTH, TILE_HEIGHT),
                borderRadius=8,
                text=None,
                background=self._get_tile_image(game.screenshotPath),
                color=pg.Color(Constants.COLOR_DARK),
                action=start_game,
                args=[game.entrypoint],
                hover=False,
                outline=Outline(Constants.COLOR_PRIMARY, 6)
            ) for index, game in enumerate(batch)
            ]
        )

        content_w = (Constants.MENU_GRID_COLS - 1) * TILE_X_SPACING + TILE_WIDTH + 12
        label_area_h = LABEL_MAX_LINES * LABEL_FONT_SIZE + (LABEL_MAX_LINES - 1) * LABEL_LINE_SPACING
        content_h = (Constants.MENU_GRID_ROWS - 1) * TILE_Y_SPACING + TILE_HEIGHT + TEXT_TOP_MARGIN + label_area_h + 12
        self.surface = pg.Surface((content_w, content_h), pg.SRCALPHA)

    def _get_tile_image(self, screenshot_path:str|None) -> pg.Surface:
        if screenshot_path:
            try:
                img = pg.image.load(screenshot_path).convert()
                return pg.transform.smoothscale(img, (TILE_WIDTH, TILE_HEIGHT))
            except Exception:
                pass
        return self._placeholder.copy()

    def _trim_to_width(self, value:str, max_width:int) -> str:
        if Constants.FONT.render(value, True, Constants.COLOR_PRIMARY, LABEL_FONT_SIZE).get_width() <= max_width:
            return value

        trimmed = value
        while len(trimmed) > 1:
            candidate = trimmed[:-1].rstrip() + "..."
            if Constants.FONT.render(candidate, True, Constants.COLOR_PRIMARY, LABEL_FONT_SIZE).get_width() <= max_width:
                return candidate
            trimmed = trimmed[:-1]
        return "..."

    def _wrap_title(self, value:str) -> list[str]:
        max_width = TILE_WIDTH - (LABEL_SIDE_PADDING * 2)
        words = value.split()

        if not words:
            return [""]

        lines = []
        current = ""
        i = 0
        while i < len(words) and len(lines) < LABEL_MAX_LINES:
            word = words[i]
            candidate = word if not current else f"{current} {word}"
            candidate_w = Constants.FONT.render(candidate, True, Constants.COLOR_PRIMARY, LABEL_FONT_SIZE).get_width()

            if candidate_w <= max_width:
                current = candidate
                i += 1
                continue

            if current:
                lines.append(current)
                current = ""
            else:
                lines.append(self._trim_to_width(word, max_width))
                i += 1

        if len(lines) < LABEL_MAX_LINES and current:
            lines.append(current)

        if i < len(words):
            overflow = " ".join(words[i:])
            if lines:
                lines[-1] = self._trim_to_width(f"{lines[-1]} {overflow}".strip(), max_width)
            else:
                lines.append(self._trim_to_width(overflow, max_width))

        return lines[:LABEL_MAX_LINES]
    
    def render(self, surface:pg.Surface):
        size = surface.get_size()
        self_size = self.surface.get_size()

        surface.blit(self.surface, (size[0] / 2 - self_size[0] / 2, size[1] / 2 - self_size[1] / 2 + 80))
        
    def update(self):
        self.surface.fill((0, 0, 0, 0))
        
        for btn in self.components.buttons:
            btn.hoverStatus = False
        
        ind = game_positions.index(self.menu.selection)
        self.components.buttons[ind].hoverStatus = True
        
        for btn in self.components.buttons:
            btn.update()
            btn.draw(self.surface)

        for index, game in enumerate(self.batch):
            btn = self.components.buttons[index]
            lines = self._wrap_title(game.name)
            for line_index, line in enumerate(lines):
                label = Constants.FONT.render(line, True, Constants.COLOR_PRIMARY, LABEL_FONT_SIZE)
                y = btn.rect.bottom + TEXT_TOP_MARGIN + line_index * (LABEL_FONT_SIZE + LABEL_LINE_SPACING)
                label_rect = label.get_rect(midtop=(btn.rect.centerx, y))
                self.surface.blit(label, label_rect)