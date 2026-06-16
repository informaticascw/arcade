import random
import pygame as pg


def create_starry_placeholder(size: tuple[int, int]) -> pg.Surface:
    width, height = size
    surface = pg.Surface(size)

    # Vertical sky gradient.
    for y in range(height):
        ratio = y / max(1, height - 1)
        r = int(6 + 16 * ratio)
        g = int(14 + 24 * ratio)
        b = int(34 + 40 * ratio)
        pg.draw.line(surface, (r, g, b), (0, y), (width, y))

    # Deterministic stars so all placeholders look consistent.
    rnd = random.Random(42)
    star_count = max(80, (width * height) // 1600)
    for _ in range(star_count):
        x = rnd.randrange(0, width)
        y = rnd.randrange(0, height)
        radius = 1 if rnd.random() < 0.9 else 2
        tone = rnd.randrange(210, 256)
        pg.draw.circle(surface, (tone, tone, min(255, tone + 10)), (x, y), radius)

    return surface
