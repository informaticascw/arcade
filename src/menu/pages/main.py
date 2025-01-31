import pygame as pg
import components
from util.constants import Constants
from util.games import fetchGames

page = components.Page(
    name="main",
    background=pg.image.load("assets/menu_background.jpg"),
    components=components.ComponentCollection(
        text=[
            components.gui.Text("STANISLAS ARCADE", Constants.COLOR_PRIMARY, 108, ("center", 100), shadow=components.effects.Shadow((10, -2), Constants.COLOR_SECONDARY)),
            components.gui.Text(", ".join(map(lambda x : x.name, fetchGames())), Constants.COLOR_PRIMARY, 32, (1000, 1000), outline=components.effects.Outline(pg.Color("yellow"), 3, 0)),
        ],
    ),
)