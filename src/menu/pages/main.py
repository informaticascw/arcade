import pygame as pg
import components
from util.constants import Constants

page = components.Page(
    name="main",
    background=Constants.COLOR_DARK,
    components=components.ComponentCollection(
        text={
            components.gui.Text("STANISLAS ARCADE", Constants.COLOR_PRIMARY, 108, (120, 0))
        }
    )
)