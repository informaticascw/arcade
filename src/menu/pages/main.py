import pygame as pg
import components
from util.constants import Constants
from util.games import fetchGames
from util.games import start_game

games = []
button = []

for index, game in enumerate(fetchGames()):
    print(type(game.entrypoint))
    txt = components.gui.Text(game.name, Constants.COLOR_PRIMARY, 32, (800, 500 + index * 40))
    games.append(txt)
    btn = components.gui.Button(
        rect=pg.Rect(500, 400  + index * 150, 200, 100),
        borderRadius=3,
        text=game.name,
        background=pg.Color("red"),
        color=pg.Color("white"),
        action=start_game,
        args=[game.entrypoint],
    )
    button.append(btn)


page = components.Page(
    name="main",
    background=pg.image.load("assets/menu_background.jpg"),
    components=components.ComponentCollection(
        text=[
            components.gui.Text("STANISLAS ARCADE", Constants.COLOR_PRIMARY, 108, ("center", 100), shadow=components.effects.Shadow((10, -2), Constants.COLOR_SECONDARY)),
            *games,
        ],
        buttons=[
            *button
        ],
    ),
)