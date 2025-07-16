import pygame as pg
import os

class Constants:
    RESOLUTION:tuple = (1920, 1080)
    FPS:int = 100
    DISPLAY_MODE:int = pg.FULLSCREEN
    # DISPLAY_MODE:int = pg.NOFRAME
    # DISPLAY_MODE:int = 0
    
    FONT = None
    DEFAULT_FONT_SIZE = 16
    
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

    # Screensaver
    SCREENSAVER_TIMEOUT_MS = 10000  # Time in milliseconds after which the screensaver activates
    SCREENSAVER_IMAGE_PATH = "./assets/screensaver.png"  # Path to the screensaver image
    SCREENSAVER_OVERLAY_OPACITY = 127  # 0-255, 191 = 75% opacity = 25% transparency
    SCREENSAVER_FONT_PATH = "./assets/font.ttf" 
    SCREENSAVER_MESSAGE_OF_THE_DAY = "Uit heel de omtrek komen wij naar de arcadekast"
