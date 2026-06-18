#
# BREAKOUT GAME 
#

from . import classes,cheats,score,keyboard
from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle
from pijthon_psel_ffi import panic
from .setup import *

start_balls_override: int = 3

# entry
# TODO: split up entry from game logic to allow easier scenes
def main(screen: pygame.Surface, fps_clock: pygame.time.Clock, fps: int = FPS, level: int = 0) -> bool | None:
    paddle2_img: pygame.Surface = pygame.transform.flip(paddle_img, 0, 1)
    paddle2 = Paddle((width / 2 - PADDLE_WIDTH / 2, height * 0.16), (PADDLE_WIDTH, PADDLE_HEIGHT), paddle2_img, 1000)

    levels: List[List[Dict[str, int]]] = json.load(open(ROOT + '/assets/duo_levels.json'))
    
    broken_count: int = 0
    bricks: List[Brick] = []
    for block_data in levels[level]:
        bricks.append(new_brick_at((block_data["x"],block_data["y"]), (block_data["width"], block_data["height"]), block_data["tier"]))
        pass

    init_ball_count: int = 3
    if start_balls_override != init_ball_count:
        init_ball_count = start_balls_override
        pass
    elif random.random() > 0.8:
        init_ball_count = random.randint(5, 20)
        pass

    balls_next_pop: float = BALLS_POP_INTERVAL
    balls: List[Ball] = [
        Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, random.randint(0, 1)) for _ in range(init_ball_count)
    ]

    next_powerup: float = 1
    powerups: List[Powerup] = [
        # new_powerup_at((random.randint(0, width - POWERUP_WIDTH), -POWERUP_HEIGHT), (POWERUP_WIDTH, POWERUP_HEIGHT), random.randint(0,10), POWERUP_SPEED) if random.random() > 0.5 else new_powerup_at((random.randint(0, width - POWERUP_WIDTH), height + POWERUP_HEIGHT), (POWERUP_WIDTH, POWERUP_HEIGHT), random.randint(0,10), -POWERUP_SPEED)
    ]


    gscore: float = 0
    since_last_block: float = 0

    info_text = classes.Text((0,0), smallfont, "", (255,255,255))

    print('mygame is running')
    gameover: bool = False
    won: bool = False
    quit: bool = False
    running: bool = True
    elapsed: float = 0
    quit_start: bool = False
    quit_timer: float = 0

    screen.fill(background)

    while running:
        delta: float = fps_clock.tick(fps) / 1000.0

        elapsed += delta
        since_last_block += delta

        #
        # read events
        # 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                running = False
                pass
            pass
      
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed() 
              
        # 
        # move everything
        #

        # mod: float = abs(ball.speed_x) / BALL_SPEED
        mod: float = elapsed * 0.2
        rel: float = ((paddle.y + PADDLE_HEIGHT) / height) ** 3.4
        if paddle.y > height * 0.80          and keys[pygame.K_w]: paddle.y -= (paddle.peed + mod) * delta * 0.3
        if paddle.x > 0                      and keys[pygame.K_a]: paddle.x -= (paddle.peed + mod) * delta * rel
        if paddle.y + paddle.height < height and keys[pygame.K_s]: paddle.y += (paddle.peed + mod) * delta * 0.3
        if paddle.x + paddle.width < width   and keys[pygame.K_d]: paddle.x += (paddle.peed + mod) * delta * rel

        mod2: float = elapsed * 0.2
        rel2: float = (1 - ((paddle2.y + PADDLE_HEIGHT) / height)) ** 3.4
        if paddle2.y > 0                              and keys[pygame.K_i]: paddle2.y -= (paddle2.peed + mod2) * delta * 0.3
        if paddle2.x > 0                              and keys[pygame.K_j]: paddle2.x -= (paddle2.peed + mod2) * delta * rel2
        if paddle2.y + paddle2.height < height * 0.20 and keys[pygame.K_k]: paddle2.y += (paddle2.peed + mod2) * delta * 0.3
        if paddle2.x + paddle2.width < width          and keys[pygame.K_l]: paddle2.x += (paddle2.peed + mod2) * delta * rel2

        if paddle.follow_cheat:
            ty = -1
            tx = 0
            tw = 0
            for b in balls:
                if b.y > ty:
                    tx,ty,tw = b.x,b.y,b.width
                    pass
                pass
            # paddle.y = height - paddle.height
            target: float = tx - paddle.width / 2 + tw / 2

            if paddle.x > 0                    and target < paddle.x: paddle.x -= (paddle.peed + mod) * delta * rel
            if paddle.x + paddle.width < width and target > paddle.x: paddle.x += (paddle.peed + mod) * delta * rel

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
    
        for p in powerups:
            p.y += p.descent * delta

            tpaddle: Paddle | None = paddle if paddle.rectCollide(p) else paddle2 if paddle2.rectCollide(p) else None

            if tpaddle != None:
                powerups.remove(p)
                
                match p.type:
                    case 0:
                        gscore += 50
                        break
                    case 1:
                        gscore += 100
                        break
                    case 2:
                        gscore += 250
                        break
                    case 3:
                        gscore += 500
                        break
                    case 4:
                        tpaddle.peed *= 0.9
                        break
                    case 5:
                        tpaddle.peed *= 1.1
                        break
                    case 6:
                        chance = random.random()
                        player: int = 0 if tpaddle == paddle else 1

                        if chance < 0.7:
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, player))
                            pass
                        elif chance < 0.9:
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, player))
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, player))
                            pass
                        else:
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, player))
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, player))
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True, player))
                            pass
                        break
                    case 7:
                        # bullet storm
                        pass
                    case 8:
                        # mighty eagle
                        pass
                    case 9:
                        tpaddle.x += tpaddle.width * 0.05
                        tpaddle.width /= 1.1
                        tpaddle.img = pygame.transform.scale(tpaddle.img, (tpaddle.width, tpaddle.height))
                        pass
                    case 10:
                        tpaddle.x -= tpaddle.width * 0.05
                        tpaddle.width *= 1.1
                        tpaddle.img = pygame.transform.scale(tpaddle.img, (tpaddle.width, tpaddle.height))
                        pass
                    case 11:
                        # shoot bullets for a couple sec
                        # or make q shoot a shockwave of bullets
                        pass
                    case _:
                        break

                pass

            if p.descent > 0 and p.y - p.height > height:
                powerups.remove(p)
                pass
            elif p.descent < 0 and p.y + p.height < 0:
                powerups.remove(p)
                pass
            pass

        for ball in balls:
            # move ball

            signx = ball.speed_x / abs(ball.speed_x)
            signy = ball.speed_y / abs(ball.speed_y)

            ball.speed_x += delta * signx
            ball.speed_y += delta * signy

            if not ball.shoot_mode:
                ball.x += ball.speed_x * delta
                ball.y += ball.speed_y * delta 
                pass
            elif ball.player == 0:
                ball.x = paddle.x + paddle.width / 2 - ball.width / 2
                ball.y = paddle.y - ball.height * 2 
                pass
            else:
                ball.x = paddle2.x + paddle2.width / 2 - ball.width / 2
                ball.y = paddle2.y + paddle2.height + ball.height * 2 
                pass
            

            if ball.shoot_mode and ball.player == 0 and keys[pygame.K_q]:
                angle = random.uniform(
                    math.radians(30),
                    math.radians(150)
                )
                # print(f"angle = {angle}")

                ball.speed_x = math.cos(angle) * BALL_SPEED
                ball.speed_y = -abs(math.sin(angle) * BALL_SPEED)
                ball.shoot_mode = False
                pass
            elif ball.shoot_mode and ball.player == 1 and keys[pygame.K_u]:
                angle = random.uniform(
                    math.radians(30),
                    math.radians(150)
                )
                # print(f"angle = {angle}")

                ball.speed_x = math.cos(angle) * BALL_SPEED
                ball.speed_y = abs(math.sin(angle) * BALL_SPEED)
                ball.shoot_mode = False
                pass

          

            # paddle.x = ball.x - paddle.width / 2 + ball.width / 2

            # colisions

            if ball.x < 0 : 
                ball.speed_x = abs(ball.speed_x)
                pass
            elif ball.x + BALL_WIDTH > width: 
                ball.speed_x = abs(ball.speed_x) * -1
                pass

            if ball.y + ball.height < 0 : 
                # ball.speed_y = abs(ball.speed_y)
                balls.remove(ball)
                continue
            elif ball.y - ball.height > height: 
                # ball.speed_y = abs(ball.speed_y) * -1
                balls.remove(ball)
                continue

            if ball.rectCollide(paddle):
                ball.angledCollision(paddle, MAX_ANGLE, True)
                pass
            elif ball.rectCollide(paddle2):
                ball.angledCollision(paddle2, MAX_ANGLE, False)
                pass
        
            for b in bricks:
                if b.broken: 
                    continue
            
                if not b.rectCollide(ball):
                    continue
            
                if b.breakl():
                    broken_count += 1
                    
                    if since_last_block == 0:
                        since_last_block = 1
                        pass

                    gscore += (500 * b.original_tier) * (1 / since_last_block)
                    since_last_block = 0
                    pass

                ball.simpleCollision(b, delta)
                pass
            pass

        
        if len(balls) == 0:
            gameover = True
            running = False
            break
      

        # 
        # handle collisions
        #

        # info_text.text = f"fps = {int(1 / delta)}, score = {int(gscore)}, elapsed = {int(elapsed)}"
        info_text.text = f"fps = {int(1 / delta)}, score = {int(gscore)}, elapsed = {int(elapsed)}, balls = {len(balls)}, next powerup = {int(next_powerup)}, powerup count = {len(powerups)}"
        # 
        # draw everything
        #

        # clear screen
        if not cheats.lsd: screen.fill(background) 

        info_text.draw(screen)

        for p in powerups: p.draw(screen)

        # draw ball
        for ball in balls:
            ball.draw(screen)
            pass
        paddle.draw(screen)
        paddle2.draw(screen)

        for b in bricks:
            if not b.broken: 
                b.draw(screen)
                pass
            pass

      
        # show screen
        pygame.display.flip() 
      
        # print("\033[A\033[K" * 2, end="")
        # print(f"width = {width}, height = {height}")
        # print(f"ball.x = {ball.x}, ball.y = {ball.y}, ")

        if len(balls) > MIN_BALLS and elapsed > balls_next_pop:
            balls.pop()
            balls_next_pop += BALLS_POP_INTERVAL
            pass
        elif len(balls) <= MIN_BALLS:
            balls_next_pop = elapsed + BALLS_POP_INTERVAL
            pass

        if elapsed > next_powerup:
            if random.random() > 0.5:
                powerups.append(new_powerup_at((random.randint(0, width - POWERUP_WIDTH), -POWERUP_HEIGHT), (POWERUP_WIDTH, POWERUP_HEIGHT), Powerup.random(), POWERUP_SPEED))
                pass
            else:
                powerups.append(new_powerup_at((random.randint(0, width - POWERUP_WIDTH), height + POWERUP_HEIGHT), (POWERUP_WIDTH, POWERUP_HEIGHT), Powerup.random(), -POWERUP_SPEED))
                pass
            next_powerup = elapsed + POWERUP_INTERVAL
            pass

        if broken_count == len(bricks):
            for ball in balls:
                ball.shoot_mode = True
                pass

            if level + 1 >= len(levels):
                won = True
                running = False
                pass
            
            else:
              sfps = 24
              level += 1
              screen.fill(background) 
              fps_clock.tick(sfps)
              for i in range(sfps * 2):
                  screen.fill(background) 
                  text: pygame.Surface = bigfont.render(f"level {level}", True, (0, 0, 255 * (1 - i % 2)))
                  screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
                  pygame.display.flip() 
                  fps_clock.tick(sfps)
                  pass
              
              screen.fill(background) 
              fps_clock.tick(sfps)
              
              for block_data in levels[level]:
                  bricks.append(Brick((block_data["x"],block_data["y"]), (block_data["width"], block_data["height"]), block_data["tier"], brick_tiers, cracked_brick_tiers))
                  pass
              pass
            pass

        pass

    result: None | bool = None

    if quit:
        result = False
        pass
    elif won:
        sfps = 120
        gscore += 2000

        screen.fill(background) 
        text: pygame.Surface = bigfont.render(f"you won", True, (0, 255, 0))
        screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.flip() 
        fps_clock.tick(sfps)
        time.sleep(2)

        print("won")
        result = True
        pass
    elif gameover:
        sfps = 12
        for i in range(sfps * 2):
            screen.fill((255 * (i % 2), 0, 0)) 
            text: pygame.Surface = bigfont.render(f"gameover", True, (255 * (1 - i % 2), 0, 0))
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.flip() 
            fps_clock.tick(sfps)
            pass
        print("gameover")
        result = False
        pass
    else:
        print("nothing to do")
        pass

    if not quit and result != None:
        if not cheats.tainted:
            name = keyboard.dialog(screen, fps_clock, f"{int(gscore)} scoreboard name", fps)

            if name == None: result = None
            elif name.lower() in profanity: pass
            elif len(name) > 0: score.add_duos_entry(name, int(gscore))

            pass
        pass

    print('mygame stopt running')
    # panic("craz")
    return result
