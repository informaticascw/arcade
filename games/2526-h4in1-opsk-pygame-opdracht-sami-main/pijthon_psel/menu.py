from . import game,classes,freeplay,cheats,keyboard,scoreboard,multiplayer
from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, sys, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle, Text
from pijthon_psel_ffi import panic
from .game import * # type: ignore


def entry() -> None:
    fps: int = FPS

    help_text = classes.Text((width * 0.05, height * 0.93), smallfont, "use WSAD to move, press Q to shoot, press E to bring ball back, hold Z for 2 sec to return", (255,255,255))

    ball = Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 0, BALL_SPEED * 2), ball_img, True)
    
    cheat_brick = new_brick_at((width / 2 - 200 / 2 + 50, height * 0.2 - 60), (200, 60), random.randint(4, 9))
    cheat_text = classes.Text((cheat_brick.x + cheat_brick.width / 2, cheat_brick.y + cheat_brick.height / 2), smallfont, "???", (255,255,255))
    cheat_text.center()

    play_brick = new_brick_at((width / 2 - 200 / 2, height * 0.2), (200, 60), 8)
    play_text = classes.Text((play_brick.x + play_brick.width / 2, play_brick.y + play_brick.height / 2), mediumfont, "play", (255,255,255))
    play_text.center()

    exit_brick = new_brick_at((width / 2 - 200 / 2 - 200, height * 0.2), (200, 60), 3)
    exit_text = classes.Text((exit_brick.x + exit_brick.width / 2, exit_brick.y + exit_brick.height / 2), mediumfont, "exit", (255,255,255))
    exit_text.center()

    free_brick = new_brick_at((width / 2 - 200 / 2 + 200, height * 0.2), (200, 60), 2)
    free_text = classes.Text((free_brick.x + free_brick.width / 2, free_brick.y + free_brick.height / 2), mediumfont, "free play", (255,255,255))
    free_text.center()

    scores_brick = new_brick_at((width / 2 - 200 / 2 - 400, height * 0.2), (200, 60), 1)
    scores_text = classes.Text((scores_brick.x + scores_brick.width / 2, scores_brick.y + scores_brick.height / 2), mediumfont, "scores", (255,255,255))
    scores_text.center()

    multiplayer_brick = new_brick_at((width / 2 - 200 / 2 + 400, height * 0.2), (200, 60), 7)
    multiplayer_text = classes.Text((multiplayer_brick.x + multiplayer_brick.width / 2, multiplayer_brick.y + multiplayer_brick.height / 2), mediumfont, "duos", (255,255,255))
    multiplayer_text.center()


    bricks: List[Brick] = [
        
        # new_brick_at((width / 2 - 200 / 2 + 400, height * 0.2), (200, 60), random.randint(0, 3)),
        # new_brick_at((width / 2 - 200 / 2 - 400, height * 0.2), (200, 60), random.randint(0, 3)),
        
        new_brick_at((width / 2 - 200 / 2 + 600, height * 0.2), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 600, height * 0.2), (200, 60), random.randint(0, 3)),


        # new_brick_at((width / 2 - 200 / 2 + 50, height * 0.2 - 60), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 150, height * 0.2 - 60), (200, 60), random.randint(0, 3)),

        new_brick_at((width / 2 - 200 / 2 + 250, height * 0.2 - 60), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 350, height * 0.2 - 60), (200, 60), random.randint(0, 3)),
        
        new_brick_at((width / 2 - 200 / 2 + 450, height * 0.2 - 60), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 550, height * 0.2 - 60), (200, 60), random.randint(0, 3)),

        new_brick_at((width / 2 - 200 / 2 + 650, height * 0.2 - 60), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 750, height * 0.2 - 60), (200, 60), random.randint(0, 3)),
        

        new_brick_at((width / 2 - 200 / 2 + 150, height * 0.2 - 120), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 50, height * 0.2 - 120), (200, 60), random.randint(0, 3)),
        
        new_brick_at((width / 2 - 200 / 2 + 350, height * 0.2 - 120), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 250, height * 0.2 - 120), (200, 60), random.randint(0, 3)),

        new_brick_at((width / 2 - 200 / 2 + 550, height * 0.2 - 120), (200, 60), random.randint(0, 3)),
        new_brick_at((width / 2 - 200 / 2 - 450, height * 0.2 - 120), (200, 60), random.randint(0, 3)),
    ]

    screen.fill(background)

    brought_cheats: bool = False
    bring_cheats_timer: float = 0
    running: bool = True

    # print(score.get_game())
    # print(keyboard.dialog(screen, fps_clock, "debug test"))
    # scoreboard.main(screen, fps_clock)

    while running:
        delta: float = fps_clock.tick(fps) / 1000.0

        #
        # read events
        # 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                running = False
                pass
            pass
      
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 


        rel: float = ((paddle.y + paddle.height) / height) ** 3.4
        # vy: float = paddle.peed * delta * 0.3
        # vx: float = paddle.peed * delta * rel
        if paddle.y > height * 0.80          and keys[pygame.K_w]:
            if paddle.y - paddle.peed * delta * 0.3 < height * 0.80: paddle.y = height * 0.80
            else: paddle.y -= paddle.peed * delta * 0.3
            pass
        if paddle.x > 0                      and keys[pygame.K_a]:
            if paddle.x - paddle.peed * delta * rel < 0: paddle.x = 0
            else: paddle.x -= paddle.peed * delta * rel
            pass
        if paddle.y + paddle.height < height and keys[pygame.K_s]:
            if paddle.y + paddle.height + paddle.peed * delta * 0.3 > height: paddle.y = height - paddle.height
            else: paddle.y += paddle.peed * delta * 0.3
            pass
        if paddle.x + paddle.width < width   and keys[pygame.K_d]:
            #paddle.x += paddle.peed * delta * rel
            if paddle.x + paddle.width + paddle.peed * delta * rel > width: paddle.x = width - paddle.width
            else: paddle.x += paddle.peed * delta * rel
            pass

        if keys[pygame.K_e]:
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2
            pass

        if not ball.shoot_mode:
            ball.x += ball.speed_x * delta
            ball.y += ball.speed_y * delta 
            pass
        else:
            ball.x = paddle.x + paddle.width / 2 - ball.width / 2
            ball.y = paddle.y - ball.height * 2 
            pass

        if ball.shoot_mode and keys[pygame.K_q]:
            ball.shoot_mode = False
            pass

        if keys[pygame.K_m]:
            bring_cheats_timer += delta
            pass
        else:
            bring_cheats_timer = 0
            pass

        if ball.rectCollide(paddle):
            ball.angledCollision(paddle, MAX_ANGLE, True)
            pass


        if ball.x < 0 : 
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

        if bring_cheats_timer >= 2 and not brought_cheats:
            cheat_brick.y += 120
            cheat_text.y += 120

            brought_cheats = True
            pass
        elif bring_cheats_timer < 2 and brought_cheats:
            cheat_brick.y -= 120
            cheat_text.y -= 120

            brought_cheats = False
            pass
        
        if cheat_brick.rectCollide(ball):
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            # cheats.tainted = True

            result: bool | None = cheats.main(screen, fps_clock, fps)
            if result == None:
                running = False
                break
            pass

        if play_brick.rectCollide(ball):
            # ball.simpleCollision(play_brick, delta)
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2
            pos: Tuple[float, float] = (paddle.x, paddle.y)

            result: bool | None = game.main(screen, fps_clock, fps, 0)
            if result == None:
                running = False
                break

            paddle.reset()
            paddle.x, paddle.y = pos
            pass

        if exit_brick.rectCollide(ball):
            # ball.simpleCollision(play_brick, delta)
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            running = False
            break

        if free_brick.rectCollide(ball):
            # ball.simpleCollision(play_brick, delta)
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2
            pos: Tuple[float, float] = (paddle.x, paddle.y)

            result: bool | None = freeplay.main(screen, fps_clock, fps, 2)
            if result == None:
                running = False
                break

            paddle.reset()
            paddle.x, paddle.y = pos
            pass

        if scores_brick.rectCollide(ball):
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            if scoreboard.main(screen, fps_clock, fps):
                running = False
                break
            pass

        if multiplayer_brick.rectCollide(ball):
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2
            pos: Tuple[float, float] = (paddle.x, paddle.y)

            result: bool | None = multiplayer.main(screen, fps_clock, fps, 0)
            if result == None:
                running = False
                break

            paddle.reset()
            paddle.x, paddle.y = pos
            pass
        

        for b in bricks:
            if b.broken: 
                continue
        
            if not b.rectCollide(ball):
                continue
        
            if b.breakl():
                bricks.remove(b)
                pass

            ball.simpleCollision(b, delta)
            pass

        if not cheats.lsd: screen.fill(background) 

        help_text.draw(screen)
        for b in bricks: b.draw(screen)

        paddle.draw(screen)
        ball.draw(screen)
        cheat_brick.draw(screen); cheat_text.draw(screen)
        play_brick.draw(screen); play_text.draw(screen)
        exit_brick.draw(screen); exit_text.draw(screen)
        free_brick.draw(screen); free_text.draw(screen)
        scores_brick.draw(screen); scores_text.draw(screen)
        multiplayer_brick.draw(screen); multiplayer_text.draw(screen)

        pygame.display.flip()

        # result: bool | None = game.main(screen, fps_clock, fps, 0)
        # if result == None:
        #     running = False
        #     pass

        pass

    pygame.quit()
    # sys.exit()
    # panic("crazy")
    pass