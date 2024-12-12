import pygame as pg

class Constants:
    RESOLUTION:tuple = (1920, 1080)
    FPS:int = 100
    DISPLAY_MODE:int = pg.FULLSCREEN
    
    FONT = None
    DEFAULT_FONT_SIZE = 16
    
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
    
    # Components color values
    # These will be the default color values, you can change them on individual components with the .setColor or .setBackground functions
    BUTTON_ACTIVE:pg.Color = pg.Color("cadetblue4")
    BUTTON_INACTIVE:pg.Color = pg.Color("gray5")
    BUTTON_HOVER:pg.Color = pg.Color("purple")
    BUTTON_COLOR:pg.Color = pg.Color("white")
    
    INPUT_ACTIVE:pg.Color = pg.Color("cadetblue4")
    INPUT_INACTIVE:pg.Color = pg.Color("black")
    INPUT_COLOR:pg.Color = pg.Color("white")