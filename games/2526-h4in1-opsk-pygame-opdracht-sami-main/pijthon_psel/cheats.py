from . import classes,game,setup
from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, sys, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle, Text
from pijthon_psel_ffi import panic
from .setup import * # type: ignore

tainted: bool = False
lsd: bool = False

def main(screen: pygame.Surface, fps_clock: pygame.time.Clock, fps: int = FPS) -> None | bool:
    global lsd
    global tainted

    ball = Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 0, BALL_SPEED * 2), ball_img, True)
    # paddle.x = width / 2 - paddle.width / 2

    stats = classes.Text((0,0), smallfont, "", (255,255,255))

    return_brick = new_brick_at((width / 2 - 200 / 2 - 750, height * 0.2), (200, 60), 3)
    return_text = classes.Text((return_brick.x + return_brick.width / 2, return_brick.y + return_brick.height / 2), mediumfont, "return", (255,255,255))
    return_text.center()

    homing_brick = new_brick_at((width / 2 - 200 / 2 + 0, height * 0.2), (200, 60), random.randint(3, 9))
    homing_text = classes.Text((homing_brick.x + homing_brick.width / 2, homing_brick.y + homing_brick.height / 2), smallfont, "homing", (255,255,255))
    homing_text.center()

    hyperspeed_brick = new_brick_at((width / 2 - 200 / 2 - 200, height * 0.2), (200, 60), random.randint(3, 9))
    hyperspeed_text = classes.Text((hyperspeed_brick.x + hyperspeed_brick.width / 2, hyperspeed_brick.y + hyperspeed_brick.height / 2), smallfont, "hyperspeed", (255,255,255))
    hyperspeed_text.center()

    width_brick = new_brick_at((width / 2 - 200 / 2 + 200, height * 0.2), (200, 60), random.randint(3, 9))
    width_text = classes.Text((width_brick.x + width_brick.width / 2, width_brick.y + width_brick.height / 2), smallfont, "width", (255,255,255))
    width_text.center()

    lsd_brick = new_brick_at((width / 2 - 200 / 2 + 400, height * 0.2), (200, 60), random.randint(3, 9))
    lsd_text = classes.Text((lsd_brick.x + lsd_brick.width / 2, lsd_brick.y + lsd_brick.height / 2), smallfont, "lsd", (255,255,255))
    lsd_text.center()

    balls_brick = new_brick_at((width / 2 - 200 / 2 + 600, height * 0.2), (200, 60), random.randint(3, 9))
    balls_text = classes.Text((balls_brick.x + balls_brick.width / 2, balls_brick.y + balls_brick.height / 2), smallfont, "double balls", (255,255,255))
    balls_text.center()

    powerups_brick = new_brick_at((width / 2 - 200 / 2 + 800, height * 0.2), (200, 60), random.randint(3, 9))
    powerups_text = classes.Text((powerups_brick.x + powerups_brick.width / 2, powerups_brick.y + powerups_brick.height / 2), smallfont, "powerups", (255,255,255))
    powerups_text.center()

    running: bool = True
    quit: bool = False
    quit_start: bool = False
    quit_timer: float = 0
    elapsed: float = 0

    while running:
        delta: float = fps_clock.tick(fps) / 1000.0
        elapsed += delta

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                running = False
                pass
            pass
      
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 


        rel: float = ((paddle.y + paddle.height) / height) ** 3.4
        norm = paddle.peed * delta * rel
        if paddle.y > height * 0.80          and keys[pygame.K_w]:
            if paddle.y - paddle.peed * delta * 0.3 < height * 0.80: paddle.y = height * 0.80
            else: paddle.y -= paddle.peed * delta * 0.3
            pass
        if paddle.y + paddle.height < height and keys[pygame.K_s]:
            if paddle.y + paddle.height + paddle.peed * delta * 0.3 > height: paddle.y = height - paddle.height
            else: paddle.y += paddle.peed * delta * 0.3
            pass
        if keys[pygame.K_a]:
            if paddle.x < width * 0.1:
                return_brick.x += norm
                return_text.x += norm

                homing_brick.x += norm
                homing_text.x += norm
                
                hyperspeed_brick.x += norm
                hyperspeed_text.x += norm
                
                width_brick.x += norm
                width_text.x += norm
                
                lsd_brick.x += norm
                lsd_text.x += norm
                
                balls_brick.x += norm
                balls_text.x += norm

                powerups_brick.x += norm
                powerups_text.x += norm
                pass
            else: paddle.x -= norm
            pass
        if keys[pygame.K_d]:
            if paddle.x + paddle.width > width * 0.9:
                return_brick.x -= norm
                return_text.x -= norm

                homing_brick.x -= norm
                homing_text.x -= norm
                
                hyperspeed_brick.x -= norm
                hyperspeed_text.x -= norm
                
                width_brick.x -= norm
                width_text.x -= norm
                
                lsd_brick.x -= norm
                lsd_text.x -= norm
                
                balls_brick.x -= norm
                balls_text.x -= norm

                powerups_brick.x -= norm
                powerups_text.x -= norm
                pass
            else: paddle.x += norm
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


        if keys[pygame.K_z] and not quit_start: 
            quit_start = True
            quit_timer = elapsed
            pass
        elif keys[pygame.K_z] and quit_timer + 2 < elapsed:
            quit = True
            running = False
            break
        elif not keys[pygame.K_z]:
            quit_timer = False
            quit_timer = elapsed
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


        if return_brick.rectCollide(ball):
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            quit = True
            running = False
            break

        if homing_brick.rectCollide(ball):
            tainted = True

            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            paddle.follow_cheat = not paddle.follow_cheat
            pass

        if hyperspeed_brick.rectCollide(ball):
            tainted = True

            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            paddle.peed *= 2
            pass

        if width_brick.rectCollide(ball):
            tainted = True
            
            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            paddle.x -= paddle.width * 0.1
            paddle.width *= 1.2
            paddle.img = pygame.transform.scale(paddle.img, (paddle.width, paddle.height))
            pass

        if lsd_brick.rectCollide(ball):
            tainted = True

            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            lsd = not lsd
            pass

        if balls_brick.rectCollide(ball):
            tainted = True

            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            game.start_balls_override *= 2
            pass

        if powerups_brick.rectCollide(ball):
            tainted = True

            ball.shoot_mode = True
            ball.speed_x = 0
            ball.speed_y = BALL_SPEED * 2

            game.powerup_interval /= 1.2
            pass

        if not lsd: screen.fill(background) 

        stats.text = f"homing = {paddle.follow_cheat}, speed = {paddle.peed}, width = {paddle.width}, lsd = {lsd}, balls = {game.start_balls_override}, powerup interval = {int(game.powerup_interval)}"

        stats.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)
        return_brick.draw(screen); return_text.draw(screen)
        homing_brick.draw(screen); homing_text.draw(screen)
        hyperspeed_brick.draw(screen); hyperspeed_text.draw(screen)
        width_brick.draw(screen); width_text.draw(screen)
        lsd_brick.draw(screen); lsd_text.draw(screen)
        balls_brick.draw(screen); balls_text.draw(screen)
        powerups_brick.draw(screen); powerups_text.draw(screen)

        pygame.display.flip()

        pass

    if quit: return True
    pass