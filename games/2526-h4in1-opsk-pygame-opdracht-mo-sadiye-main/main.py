import os

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BALL_WIDTH = 16
BALL_HEIGHT = 16
PADDLE_WIDTH = 170
PADDLE_HEIGHT = 32
BRICK_WIDTH = 96
BRICK_HEIGHT = 32

PADDLE_Y = SCREEN_HEIGHT - 60
PADDLE_SPEED = 12
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = -7
MAX_BALL_SPEED = 14


def load_sprite(source, source_rect, size):
    surface = pygame.Surface(source_rect[2:], pygame.SRCALPHA)
    surface.blit(source, (0, 0), source_rect)
    return pygame.transform.scale(surface, size)


def create_bricks():
    bricks = []
    spacing = 10
    columns = max(1, (SCREEN_WIDTH + spacing) // (BRICK_WIDTH + spacing))

    for row in range(3):
        for col in range(columns):
            x = col * (BRICK_WIDTH + spacing)
            y = 40 + row * (BRICK_HEIGHT + 10)
            bricks.append(
                {
                    "rect": pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT),
                    "hits": 2 if row == 0 else 1,
                }
            )
    return bricks


def reset_ball_position(screen_width, screen_height, paddle_x, paddle_y):
    ball_x = paddle_x + PADDLE_WIDTH // 2 - BALL_WIDTH // 2
    ball_y = paddle_y - BALL_HEIGHT - 4
    return ball_x, ball_y


def main():
    global SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_Y

    pygame.init()

    try:
        font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
    except FileNotFoundError:
        font = pygame.font.SysFont(None, 24)

    try:
        screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN,
        )
    except pygame.error:
        screen = pygame.display.set_mode((1280, 720))

    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    PADDLE_Y = SCREEN_HEIGHT - 60
    paddle_y = PADDLE_Y
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()

    spritesheet = pygame.image.load("Breakout_Tile_Free.png").convert_alpha()

    ball_img = load_sprite(
        spritesheet,
        (1403, 652, 64, 64),
        (BALL_WIDTH, BALL_HEIGHT),
    )
    paddle_img = load_sprite(
        spritesheet,
        (1158, 462, 243, 64),
        (PADDLE_WIDTH, PADDLE_HEIGHT),
    )
    brick_img = load_sprite(
        spritesheet,
        (772, 390, 384, 128),
        (BRICK_WIDTH, BRICK_HEIGHT),
    )
    damaged_brick_img = load_sprite(
        spritesheet,
        (772, 520, 384, 128),
        (BRICK_WIDTH, BRICK_HEIGHT),
    )

    bricks = create_bricks()
    paddle_x = screen_width // 2 - PADDLE_WIDTH // 2
    ball_x, ball_y = reset_ball_position(
        screen_width,
        screen_height,
        paddle_x,
        paddle_y,
    )
    ball_speed_x = 0
    ball_speed_y = 0
    score = 0
    lives = 3
    game_status = "intro"
    animations = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_status == "intro":
                    game_status = "ready"
                elif game_status == "ready":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_status = "play"
                        ball_speed_x = 0
                        ball_speed_y = INITIAL_BALL_SPEED_Y
                        ball_x, ball_y = reset_ball_position(
                            screen_width,
                            screen_height,
                            paddle_x,
                            paddle_y,
                        )
                elif game_status in ("won", "lost"):
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        bricks = create_bricks()
                        paddle_x = screen_width // 2 - PADDLE_WIDTH // 2
                        ball_x, ball_y = reset_ball_position(
                            screen_width,
                            screen_height,
                            paddle_x,
                            paddle_y,
                        )
                        ball_speed_x = 0
                        ball_speed_y = 0
                        score = 0
                        lives = 3
                        animations.clear()
                        game_status = "ready"

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            paddle_x -= PADDLE_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            paddle_x += PADDLE_SPEED

        paddle_x = max(0, min(paddle_x, screen_width - PADDLE_WIDTH))

        if game_status == "play":
            ball_x += ball_speed_x
            ball_y += ball_speed_y
        else:
            ball_x, ball_y = reset_ball_position(
                screen_width,
                screen_height,
                paddle_x,
                paddle_y,
            )

        for animation in animations:
            animation[1] -= 10
        animations = [a for a in animations if a[1] + a[3] > 0]

        ball_rect = pygame.Rect(ball_x, ball_y, BALL_WIDTH, BALL_HEIGHT)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

        if ball_rect.left <= 0:
            ball_rect.left = 0
            ball_speed_x = abs(ball_speed_x)
        elif ball_rect.right >= screen_width:
            ball_rect.right = screen_width
            ball_speed_x = -abs(ball_speed_x)

        if ball_rect.top <= 0:
            ball_rect.top = 0
            ball_speed_y = abs(ball_speed_y)

        if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
            ball_rect.bottom = paddle_rect.top
            offset = (ball_rect.centerx - paddle_rect.centerx) / (PADDLE_WIDTH / 2)
            ball_speed_x = max(
                -MAX_BALL_SPEED,
                min(MAX_BALL_SPEED, offset * 10),
            )
            ball_speed_y = -abs(ball_speed_y)

        for i, brick in enumerate(bricks):
            brick_rect = brick["rect"]
            if ball_rect.colliderect(brick_rect):
                overlap_x = min(ball_rect.right, brick_rect.right) - max(ball_rect.left, brick_rect.left)
                overlap_y = min(ball_rect.bottom, brick_rect.bottom) - max(ball_rect.top, brick_rect.top)

                if overlap_x < overlap_y:
                    ball_speed_x = -ball_speed_x
                else:
                    ball_speed_y = -ball_speed_y

                brick["hits"] -= 1
                if brick["hits"] <= 0:
                    score += 10
                    animations.append(
                        [brick_rect.x, brick_rect.y, BRICK_WIDTH, BRICK_HEIGHT]
                    )
                    bricks.pop(i)
                else:
                    score += 2

                ball_speed_x = max(
                    -MAX_BALL_SPEED,
                    min(MAX_BALL_SPEED, ball_speed_x * 1.03),
                )
                ball_speed_y = max(
                    -MAX_BALL_SPEED,
                    min(MAX_BALL_SPEED, ball_speed_y * 1.03),
                )
                break

        if ball_rect.bottom > screen_height and game_status == "play":
            lives -= 1
            if lives <= 0:
                game_status = "lost"
                ball_speed_x = 0
                ball_speed_y = 0
            else:
                paddle_x = screen_width // 2 - PADDLE_WIDTH // 2
                ball_x, ball_y = reset_ball_position(
                    screen_width,
                    screen_height,
                    paddle_x,
                    paddle_y,
                )
                ball_speed_x = 0
                ball_speed_y = 0
                game_status = "ready"

        if len(bricks) == 0 and game_status == "play":
            game_status = "won"
            ball_speed_x = 0
            ball_speed_y = 0

        screen.fill((8, 10, 24))

        for y in range(0, screen_height, 40):
            pygame.draw.line(screen, (18, 24, 48), (0, y), (screen_width, y), 1)

        score_surface = font.render(f"Score: {score}", True, "white")
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        screen.blit(score_surface, (18, 18))
        screen.blit(
            lives_surface,
            (screen_width - lives_surface.get_width() - 18, 18),
        )

        screen.blit(ball_img, (ball_rect.x, ball_rect.y))
        screen.blit(paddle_img, (paddle_rect.x, paddle_rect.y))

        for brick in bricks:
            brick_rect = brick["rect"]
            if brick["hits"] == 2:
                screen.blit(brick_img, brick_rect)
            else:
                screen.blit(damaged_brick_img, brick_rect)

        for x, y, w, h in animations:
            pygame.draw.rect(screen, (255, 215, 0), (x, y, w, h), 2)

        if game_status == "intro":
            text = font.render("PRESS ANY KEY TO START", True, "white")
            screen.blit(
                text,
                (screen_width // 2 - text.get_width() // 2, screen_height // 2),
            )
        elif game_status == "ready":
            text = font.render("PRESS SPACE TO LAUNCH", True, "white")
            screen.blit(
                text,
                (screen_width // 2 - text.get_width() // 2, screen_height // 2),
            )
        elif game_status == "won":
            text = font.render("YOU WON!", True, "white")
            restart = font.render("PRESS ENTER TO PLAY AGAIN", True, "white")
            screen.blit(
                text,
                (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 40),
            )
            screen.blit(
                restart,
                (screen_width // 2 - restart.get_width() // 2, screen_height // 2 + 10),
            )
        elif game_status == "lost":
            text = font.render("YOU LOST!", True, "white")
            restart = font.render("PRESS ENTER TO PLAY AGAIN", True, "white")
            screen.blit(
                text,
                (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 40),
            )
            screen.blit(
                restart,
                (screen_width // 2 - restart.get_width() // 2, screen_height // 2 + 10),
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
