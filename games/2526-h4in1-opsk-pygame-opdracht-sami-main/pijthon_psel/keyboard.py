from . import classes,game,cheats
from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, sys, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle, Text
from pijthon_psel_ffi import panic
from .setup import * # type: ignore



"""
copy(`1234567890`.split("").map((e,i)=>`"${e}": classes.Text((width * 0.22 + ${i * 100}, height * 0.55), biggerfont, "${e.toUpperCase()}", inactive_color),`).join("\n") + '\n\n' + 
`qwertyuiop`.split("").map((e,i)=>`"${e}": classes.Text((width * 0.22 + ${i * 100}, height * 0.65), biggerfont, "${e.toUpperCase()}", inactive_color),`).join("\n") + '\n\n' +
`asdfghjkl`.split("").map((e,i)=>`"${e}": classes.Text((width * 0.24 + ${i * 100}, height * 0.75), biggerfont, "${e.toUpperCase()}", inactive_color),`).join("\n") + '\n\n' +
`zxcvbnm`.split("").map((e,i)=>`"${e}": classes.Text((width * 0.27 + ${i * 100}, height * 0.85), biggerfont, "${e.toUpperCase()}", inactive_color),`).join("\n"))

copy("[\n" + `1234567890`.split("").map((e,i)=>`\t("${e}", classes.Text((width * 0.22 + ${i * 100}, height * 0.55), biggerfont, "${e.toUpperCase()}", inactive_color)),`).join("\n") + '\n],\n\n[\n' + 
`qwertyuiop`.split("").map((e,i)=>`\t("${e}", classes.Text((width * 0.22 + ${i * 100}, height * 0.65), biggerfont, "${e.toUpperCase()}", inactive_color)),`).join("\n") + '\n],\n\n[\n' +
`asdfghjkl`.split("").map((e,i)=>`\t("${e}", classes.Text((width * 0.24 + ${i * 100}, height * 0.75), biggerfont, "${e.toUpperCase()}", inactive_color)),`).join("\n") + '\n],\n\n[\n' +
`zxcvbnm`.split("").map((e,i)=>`\t("${e}", classes.Text((width * 0.27 + ${i * 100}, height * 0.85), biggerfont, "${e.toUpperCase()}", inactive_color)),`).join("\n") + '\n],')
"""

def dialog(screen: pygame.Surface, fps_clock: pygame.time.Clock, prompt: str = "", fps: int = FPS, sample_rate: float = 1/7) -> None | str:

    selected_color: Tuple[int,int,int] = (255,255,255)
    inactive_color: Tuple[int,int,int] = (128,128,128)
    selected: Tuple[int,int] = (2,4)

    promp = classes.Text((width / 2, height / 6), bigfont, prompt, (150,150,150)); promp.center()
    input = classes.Text((width / 2, height / 2), biggerfont, "", (255,255,255))



    running: bool = True
    quit_start: bool = False
    quit_timer: float = 0
    elapsed: float = 0
    elapsed_since_last: float = 0
    exiting: bool = False

    key_buttons: List[List[Tuple[str, classes.Text]]] = [
        [
            ("1", classes.Text((width * 0.22 + 0, height * 0.55), biggerfont, "1", inactive_color)),
            ("2", classes.Text((width * 0.22 + 100, height * 0.55), biggerfont, "2", inactive_color)),
            ("3", classes.Text((width * 0.22 + 200, height * 0.55), biggerfont, "3", inactive_color)),
            ("4", classes.Text((width * 0.22 + 300, height * 0.55), biggerfont, "4", inactive_color)),
            ("5", classes.Text((width * 0.22 + 400, height * 0.55), biggerfont, "5", inactive_color)),
            ("6", classes.Text((width * 0.22 + 500, height * 0.55), biggerfont, "6", inactive_color)),
            ("7", classes.Text((width * 0.22 + 600, height * 0.55), biggerfont, "7", inactive_color)),
            ("8", classes.Text((width * 0.22 + 700, height * 0.55), biggerfont, "8", inactive_color)),
            ("9", classes.Text((width * 0.22 + 800, height * 0.55), biggerfont, "9", inactive_color)),
            ("0", classes.Text((width * 0.22 + 900, height * 0.55), biggerfont, "0", inactive_color)),
        ],

        [
            ("q", classes.Text((width * 0.22 + 0, height * 0.65), biggerfont, "Q", inactive_color)),
            ("w", classes.Text((width * 0.22 + 100, height * 0.65), biggerfont, "W", inactive_color)),
            ("e", classes.Text((width * 0.22 + 200, height * 0.65), biggerfont, "E", inactive_color)),
            ("r", classes.Text((width * 0.22 + 300, height * 0.65), biggerfont, "R", inactive_color)),
            ("t", classes.Text((width * 0.22 + 400, height * 0.65), biggerfont, "T", inactive_color)),
            ("y", classes.Text((width * 0.22 + 500, height * 0.65), biggerfont, "Y", inactive_color)),
            ("u", classes.Text((width * 0.22 + 600, height * 0.65), biggerfont, "U", inactive_color)),
            ("i", classes.Text((width * 0.22 + 700, height * 0.65), biggerfont, "I", inactive_color)),
            ("o", classes.Text((width * 0.22 + 800, height * 0.65), biggerfont, "O", inactive_color)),
            ("p", classes.Text((width * 0.22 + 900, height * 0.65), biggerfont, "P", inactive_color)),
        ],

        [
            ("a", classes.Text((width * 0.24 + 0, height * 0.75), biggerfont, "A", inactive_color)),
            ("s", classes.Text((width * 0.24 + 100, height * 0.75), biggerfont, "S", inactive_color)),
            ("d", classes.Text((width * 0.24 + 200, height * 0.75), biggerfont, "D", inactive_color)),
            ("f", classes.Text((width * 0.24 + 300, height * 0.75), biggerfont, "F", inactive_color)),
            ("g", classes.Text((width * 0.24 + 400, height * 0.75), biggerfont, "G", inactive_color)),
            ("h", classes.Text((width * 0.24 + 500, height * 0.75), biggerfont, "H", inactive_color)),
            ("j", classes.Text((width * 0.24 + 600, height * 0.75), biggerfont, "J", inactive_color)),
            ("k", classes.Text((width * 0.24 + 700, height * 0.75), biggerfont, "K", inactive_color)),
            ("l", classes.Text((width * 0.24 + 800, height * 0.75), biggerfont, "L", inactive_color)),
        ],

        [
            ("z", classes.Text((width * 0.27 + 0, height * 0.85), biggerfont, "Z", inactive_color)),
            ("x", classes.Text((width * 0.27 + 100, height * 0.85), biggerfont, "X", inactive_color)),
            ("c", classes.Text((width * 0.27 + 200, height * 0.85), biggerfont, "C", inactive_color)),
            ("v", classes.Text((width * 0.27 + 300, height * 0.85), biggerfont, "V", inactive_color)),
            ("b", classes.Text((width * 0.27 + 400, height * 0.85), biggerfont, "B", inactive_color)),
            ("n", classes.Text((width * 0.27 + 500, height * 0.85), biggerfont, "N", inactive_color)),
            ("m", classes.Text((width * 0.27 + 600, height * 0.85), biggerfont, "M", inactive_color)),
        ],

        [
            ("enter", classes.Text((width * 0.27 + 10, height * 0.95), biggerfont, "#=#", inactive_color)),
            ("space", classes.Text((width * 0.27 + 200, height * 0.95), biggerfont, "[-----]", inactive_color)),
            ("backspace", classes.Text((width * 0.22 + 670, height * 0.95), biggerfont, "<-", inactive_color)),
        ],
    ]

    while running:
        delta: float = fps_clock.tick(fps) / 1000.0
        elapsed += delta
        elapsed_since_last += delta

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                running = False
                exiting = True
                pass
            pass
      
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 


        if keys[pygame.K_z] and not quit_start: 
            quit_start = True
            quit_timer = elapsed
            pass
        elif keys[pygame.K_z] and quit_timer + 1 < elapsed:
            running = False
            break
        elif not keys[pygame.K_z]:
            quit_timer = False
            quit_timer = elapsed
            pass

        

        
        if elapsed_since_last > sample_rate and keys[pygame.K_w]:
            elapsed_since_last = 0
            row = selected[0] - 1
            k = selected[1]
            if row >= 0:
                key_buttons[selected[0]][k][1].color = inactive_color
                key_buttons[selected[0]][k][1].font = biggerfont

                if k >= len(key_buttons[row]):
                    k = len(key_buttons[row]) - 1
                    pass

                key_buttons[row][k][1].color = selected_color
                key_buttons[row][k][1].font = sbiggerfont

                selected = (row,k)
                pass
            pass
        if elapsed_since_last > sample_rate and keys[pygame.K_s]:
            elapsed_since_last = 0
            row = selected[0] + 1
            k = selected[1]
            if row < len(key_buttons):
                key_buttons[selected[0]][k][1].color = inactive_color
                key_buttons[selected[0]][k][1].font = biggerfont

                if k >= len(key_buttons[row]):
                    k = len(key_buttons[row]) - 1
                    pass

                key_buttons[row][k][1].color = selected_color
                key_buttons[row][k][1].font = sbiggerfont

                selected = (row,k)
                pass
            pass
        if elapsed_since_last > sample_rate and keys[pygame.K_a]:
            elapsed_since_last = 0
            row = selected[0]
            k = selected[1] - 1
            if k >= 0:
                key_buttons[row][selected[1]][1].color = inactive_color
                key_buttons[row][selected[1]][1].font = biggerfont

                key_buttons[row][k][1].color = selected_color
                key_buttons[row][k][1].font = sbiggerfont

                selected = (row,k)
                pass
            pass
        if elapsed_since_last > sample_rate and keys[pygame.K_d]:
            elapsed_since_last = 0
            row = selected[0]
            k = selected[1] + 1
            if k < len(key_buttons[row]):
                key_buttons[row][selected[1]][1].color = inactive_color
                key_buttons[row][selected[1]][1].font = biggerfont

                key_buttons[row][k][1].color = selected_color
                key_buttons[row][k][1].font = sbiggerfont

                selected = (row,k)
                pass
            pass

        if elapsed_since_last > sample_rate and keys[pygame.K_e]:
            id,k = key_buttons[selected[0]][selected[1]]
            elapsed_since_last = 0

            if id == "enter":
                break
            elif id == "space":
                input.text += " "
                pass
            elif id == "backspace":
                input.text = input.text[:-1]
                pass
            else:
                input.text += k.text
                pass

            pass
            
        

        if not cheats.lsd: screen.fill(background) 

        input.x,input.y = width / 2, height / 3
        input.center()

        input.draw(screen)
        promp.draw(screen)

        for row in key_buttons:
            for _,k in row:
                k.draw(screen)
                pass
            pass

        pygame.display.flip()

        pass

    if not exiting: return input.text
    pass