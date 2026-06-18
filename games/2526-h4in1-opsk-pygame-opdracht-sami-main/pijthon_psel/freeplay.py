from . import game,classes,cheats,score,keyboard
from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, sys, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle, Text
from pijthon_psel_ffi import panic
from .setup import * # type: ignore


def main(screen: pygame.Surface, fps_clock: pygame.time.Clock, fps: int = FPS, spawn_rate: float = 0) -> bool | None:
    # return print(ROOT)

    #
    # game loop
    #

    next_spawn: float = spawn_rate

    broken_count: int = 0
    bricks: List[Brick] = []
    

    gscore: float = 0
    since_last_block: float = 0


    balls_next_pop: float = BALLS_POP_INTERVAL * 3
    balls: List[Ball] = [
        Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True),
        Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True),
    ]

    next_powerup: float = 1
    powerups: List[Powerup] = [ ]

    print('mygame is running')
    gameover: bool = False
    quit: bool = False
    running: bool = True
    elapsed: float = 0
    quit_start: bool = False
    quit_timer: float = 0

    info_text = classes.Text((0,0), smallfont, f"elapsed = {int(elapsed)}, spawn_rate = {spawn_rate}", (255,255,255))

    while running:
        delta: float = fps_clock.tick(fps) / 1000.0

        elapsed += delta

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
            target = tx - paddle.width / 2 + tw / 2

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

            if paddle.rectCollide(p):
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
                        paddle.peed *= 0.9
                        break
                    case 5:
                        paddle.peed *= 1.1
                        break
                    case 6:
                        chance = random.random()
                        if chance < 0.7:
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True))
                            pass
                        elif chance < 0.9:
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True))
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True))
                            pass
                        else:
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True))
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True))
                            balls.append(Ball((100,100), (BALL_WIDTH, BALL_HEIGHT), (BALL_SPEED * 1, BALL_SPEED * 1), ball_img, True))
                            pass
                        break
                    case 7:
                        # bullet storm
                        pass
                    case 8:
                        # mighty eagle
                        pass
                    case 9:
                        paddle.x += paddle.width * 0.05
                        paddle.width /= 1.1
                        paddle.img = pygame.transform.scale(paddle.img, (paddle.width, paddle.height))
                        pass
                    case 10:
                        paddle.x -= paddle.width * 0.05
                        paddle.width *= 1.1
                        paddle.img = pygame.transform.scale(paddle.img, (paddle.width, paddle.height))
                        pass
                    case 11:
                        # shoot bullets for a couple sec
                        # or make q shoot a shockwave of bullets
                        pass
                    case _:
                        break

                pass

            if p.y - p.height > height:
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
            else:
                ball.x = paddle.x + paddle.width / 2 - ball.width / 2
                ball.y = paddle.y - ball.height * 2 
                pass

            if ball.shoot_mode and keys[pygame.K_q]:
                angle = random.uniform(
                    math.radians(30),
                    math.radians(150)
                )
                print(f"angle = {angle}")

                ball.speed_x = math.cos(angle) * ball.speed_x
                ball.speed_y = -abs(math.sin(angle) * ball.speed_y)
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

            if ball.y < 0 : 
                ball.speed_y = abs(ball.speed_y)
                pass
            elif ball.y + BALL_HEIGHT > height: 
                # ball.speed_y = abs(ball.speed_y) * -1
                balls.remove(ball)
                continue

            if ball.rectCollide(paddle): 
                # ball.speed_y = abs(ball.speed_y) * -1

                ball.angledCollision(paddle, MAX_ANGLE, True)
                pass
        
            for b in bricks:
                if b.broken: 
                    continue
            
                if not b.rectCollide(ball):
                    continue
            
                if b.breakl():
                    broken_count += 1
                    bricks.remove(b)
                    
                    if since_last_block == 0:
                        since_last_block = 1
                        pass

                    gscore += (500 * b.original_tier) * (1 / since_last_block)
                    since_last_block = 0

                    pass

                ball.simpleCollision(b, delta)
            pass

        
        if len(balls) == 0:
            gameover = True
            running = False
            break
      

        
        # info_text.text = f"fps = {int(1 / delta)}, score = {int(gscore)}, elapsed = {int(elapsed)}, brick count = {len(bricks)}, broken count = {broken_count}"
        info_text.text = f"fps = {int(1 / delta)}, score = {int(gscore)}, elapsed = {int(elapsed)}, brick count = {len(bricks)}, broken count = {broken_count}, spawn_rate = {spawn_rate / (elapsed ** 0.5)}"

        if not cheats.lsd: screen.fill(background) 

        info_text.draw(screen)
        for p in powerups: p.draw(screen)
        for b in bricks: b.draw(screen)
        for b in balls: b.draw(screen)
        paddle.draw(screen)

        

        pygame.display.flip()

        if len(balls) > 1 and elapsed > balls_next_pop:
            balls.pop()
            balls_next_pop += BALLS_POP_INTERVAL * 3
            pass
        elif len(balls) == 1:
            balls_next_pop = elapsed + BALLS_POP_INTERVAL * 3
            pass

        if elapsed > next_powerup:
            powerups.append(new_powerup_at((random.randint(0, width - POWERUP_WIDTH), -POWERUP_HEIGHT), (POWERUP_WIDTH, POWERUP_HEIGHT), Powerup.random(), POWERUP_SPEED))
            next_powerup = elapsed + POWERUP_INTERVAL
            pass

        if elapsed > next_spawn:
            next_spawn = elapsed + spawn_rate / (elapsed ** 0.5)
            bricks.append(new_brick_at((random.randint(0, 20) * 96, random.randint(0, 35) * 24), (BRICKS_WIDTH, BRICKS_HEIGHT), random.randint(0, 3)))
            pass

        pass

    result: None | bool = None

    if quit:
        result = False
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
            elif len(name) > 0: score.add_freeplay_entry(name, int(gscore))

            pass
        pass

    print('mygame stopt running')
    # panic("craz")
    return result