import pygame as pg
import os

class Constants:
    RESOLUTION:tuple = (1920, 1080)
    FPS:int = 100
    # DISPLAY_MODE:int = pg.FULLSCREEN
    # DISPLAY_MODE:int = pg.NOFRAME
    DISPLAY_MODE:int = 0
    
    FONT = None
    DEFAULT_FONT_SIZE = 16
    
    # GAMES_PATH = "./src/games"
    GAMES_PATH = os.path.join("src", "games")
    
    # Console ansii escape code color values
    CNSL_ERROR:str = "\x1b[1;31m"
    CNSL_SUCCESS:str = "\x1b[1;32m"
    CNSL_DATA:str = "\x1b[1;33m"
    CNSL_INFO:str = "\x1b[1;34m"
    CNSL_RESET:str = "\x1B[0m"
    
    # Theme colors
    COLOR_PRIMARY:pg.Color = pg.Color("#0094AA")
    COLOR_SECONDARY:pg.Color = pg.Color("#52AE32")
    COLOR_DARK:pg.Color = pg.Color("#424242")