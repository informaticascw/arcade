import pygame as pg
import menu.components as components
from util.constants import Constants

page = components.Page(
    name="tetris_instructions",
    background=Constants.COLOR_DARK,
    components=components.ComponentCollection(
        text={
            components.gui.Text("Tetris Instructions", Constants.COLOR_PRIMARY, 32, (120, 0))
        }
    )
)