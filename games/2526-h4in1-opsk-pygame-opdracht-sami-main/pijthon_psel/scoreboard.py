from . import classes,cheats,score
from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, sys, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle, Text
from pijthon_psel_ffi import reverse_sort_tuple_str_int
from .setup import * # type: ignore
from random import randint


def main(screen: pygame.Surface, fps_clock: pygame.time.Clock, fps: int = FPS) -> bool:

    game_scores: List[Tuple[str, int]] = reverse_sort_tuple_str_int(list(map(lambda a: (a[0], a[1]),score.get_game())))
    freeplay_scores: List[Tuple[str, int]] = reverse_sort_tuple_str_int(list(map(lambda a: (a[0], a[1]),score.get_freeplay())))
    multiplayer_scores: List[Tuple[str, int]] = reverse_sort_tuple_str_int(list(map(lambda a: (a[0], a[1]),score.get_duos())))

    active_scoreboard: int = 0
    scoreboard: List[List[classes.Text]] = [
        [   classes.Text((width * 0.05 + 0, height * 0.05), bigfont, "Game Scores", (255,255,255)),   ],
        [  classes.Text((width * 0.05 + 0, height * 0.05), bigfont, "Freeplay Scores", (255,255,255)),  ],
        [ classes.Text((width * 0.05 + 0, height * 0.05), bigfont, "Multiplayer Scores", (255,255,255)), ],
    ]
    for i in range(len(game_scores)):
        nam,sc = game_scores[i]
        color = (randint(0,127) + 128, randint(0,127) + 128, randint(0,127) + 128)
        scoreboard[0].append(classes.Text((width * 0.05, height * (i * 15 / 100 + 0.20)), bigfont, f"{nam}", color))
        scoreboard[0].append(classes.Text((width * 0.05, height * (i * 15 / 100 + 0.25)), bigfont, f"{sc}", (255,255,255)))
        pass
    for i in range(len(freeplay_scores)):
        nam,sc = freeplay_scores[i]
        color = (randint(0,127) + 128, randint(0,127) + 128, randint(0,127) + 128)
        scoreboard[1].append(classes.Text((width * 0.05, height * (i * 15 / 100 + 0.20)), bigfont, f"{nam}", color))
        scoreboard[1].append(classes.Text((width * 0.05, height * (i * 15 / 100 + 0.25)), bigfont, f"{sc}", (255,255,255)))
        pass
    for i in range(len(multiplayer_scores)):
        nam,sc = multiplayer_scores[i]
        color = (randint(0,127) + 128, randint(0,127) + 128, randint(0,127) + 128)
        scoreboard[2].append(classes.Text((width * 0.05, height * (i * 15 / 100 + 0.20)), bigfont, f"{nam}", color))
        scoreboard[2].append(classes.Text((width * 0.05, height * (i * 15 / 100 + 0.25)), bigfont, f"{sc}", (255,255,255)))
        pass



    balls: List[Ball] = []
    for _ in range(3):
        ball = Ball((random.uniform(width / 2, width - BALL_WIDTH), random.uniform(0, height - BALL_HEIGHT)), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 0.1, BALL_SPEED * 0.1), ball_img, False)
        angle = random.uniform(
            0,           # math.radians(0),
            2 * math.pi, # math.radians(360)
        )
        # print(f"angle = {angle}")

        ball.speed_x *= math.cos(angle)
        ball.speed_y *= math.sin(angle)

        balls.append(ball)
        pass


    running: bool = True
    elapsed: float = 0
    exiting: bool = False
    release_a: bool = False
    release_d: bool = False

    
    while running:
        delta: float = fps_clock.tick(fps) / 1000.0
        elapsed += delta
        

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                running = False
                exiting = True
                pass
            pass
      
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 


        if keys[pygame.K_z]:
            running = False
            pass

        if release_a and keys[pygame.K_a]:
            release_a = False
            active_scoreboard -= 1
            if active_scoreboard < 0:
                active_scoreboard = 0
                pass
            pass
        elif not keys[pygame.K_a]:
            release_a = True
            pass

        if release_d and keys[pygame.K_d]:
            release_d = False
            active_scoreboard += 1
            if active_scoreboard >= len(scoreboard):
                active_scoreboard = len(scoreboard) - 1
                pass
            pass
        elif not keys[pygame.K_d]:
            release_d = True
            pass


        for ball in balls:
            ball.x += ball.speed_x * delta
            ball.y += ball.speed_y * delta 

            if ball.x < width / 2 : 
                ball.speed_x = abs(ball.speed_x)
                pass
            elif ball.x + BALL_WIDTH > width: 
                ball.speed_x = abs(ball.speed_x) * -1
                pass

            if ball.y < 0 : 
                ball.speed_y = abs(ball.speed_y)
                pass
            elif ball.y + BALL_HEIGHT > height: 
                ball.speed_y = abs(ball.speed_y) * -1
                pass
            pass
        
        

        for t in scoreboard[active_scoreboard]:
            if keys[pygame.K_w]:
                t.y += 300 * delta
                pass
            if keys[pygame.K_s]:
                t.y -= 300 * delta
                pass
            pass
        
            
        if not cheats.lsd: screen.fill(background) 
        
        for b in balls: b.draw(screen)
        for t in scoreboard[active_scoreboard]: t.draw(screen)

        pygame.display.flip()

        pass

    return exiting