import pygame as pg

pg.init()

RESOLUTION = (1280, 720)
PINK = (255, 0, 128)

# Gebruik het game font uit /assets
FONT_PATH = "./assets/font.ttf"
font_big = pg.font.Font(FONT_PATH, 80)
font_med = pg.font.Font(FONT_PATH, 40)
font_small = pg.font.Font(FONT_PATH, 32)

# Maak een transparant oppervlak
surface = pg.Surface(RESOLUTION, pg.SRCALPHA)

# Render de teksten
text1 = font_big.render("LET'S PLAY", True, PINK)
text2 = font_med.render("Games gemaakt door leerlingen", True, PINK)
text3 = font_small.render("4e klas informatica", True, PINK)

# Center de teksten verticaal met wat ruimte ertussen
rect1 = text1.get_rect(center=(RESOLUTION[0]//2, RESOLUTION[1]//2 - 80))
rect2 = text2.get_rect(center=(RESOLUTION[0]//2, RESOLUTION[1]//2 + 10))
rect3 = text3.get_rect(center=(RESOLUTION[0]//2, RESOLUTION[1]//2 + 70))

# Zet de teksten op het oppervlak
surface.blit(text1, rect1)
surface.blit(text2, rect2)
surface.blit(text3, rect3)

# Sla het resultaat op als PNG
pg.image.save(surface, "./assets/screensaver.png")
print("screensaver-forground.png aangemaakt!")

pg.quit()