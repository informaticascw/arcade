import pygame as pg
import components
from util.constants import Constants
from util.games import fetchGames

page = components.Page(
    name="main",
    background=Constants.COLOR_DARK,
    components=components.ComponentCollection(
        text={
            components.gui.Text("STANISLAS ARCADE", Constants.COLOR_PRIMARY, 108, (120, 100), shadow=components.effects.Shadow((6, 5), Constants.COLOR_SECONDARY)),
            components.gui.Text(", ".join(map(lambda x : x.name, fetchGames())), Constants.COLOR_PRIMARY, 32, (1000, 1000), outline=components.effects.Outline(pg.Color("yellow"), 3, 0)),
        },
        images={
            components.gui.Image((100, 250), "./assets/img.png", components.effects.Shadow((5, 5), pg.Color("#d1d1d1")))
        },
        buttons={
            components.gui.Button(pg.Rect(1000, 500, 100, 60), 12, "Test", Constants.COLOR_PRIMARY, Constants.COLOR_DARK, print, ["example"], Constants.COLOR_SECONDARY,
            shadow=components.effects.Shadow((6, 4), pg.Color("#dd1111"))
            ),
            components.gui.Button(pg.Rect(1300, 500, 100, 60), 12, "Test", Constants.COLOR_PRIMARY, Constants.COLOR_DARK, print, ["example"], Constants.COLOR_SECONDARY,
            outline=components.effects.Outline(pg.Color("magenta"), 3, 0)
            ),
            components.gui.Button(pg.Rect(1300, 500, 100, 60), 12, components.gui.Text("Ja", Constants.COLOR_SECONDARY, 24, "centered"), Constants.COLOR_PRIMARY, Constants.COLOR_DARK, print, ["example"], Constants.COLOR_SECONDARY,
            outline=components.effects.Outline(pg.Color("magenta"), 3, 0)
            )
        }
    )
)