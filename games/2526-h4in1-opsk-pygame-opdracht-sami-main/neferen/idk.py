# @chatgpt maak mooie python script maakt niet uit wat, liefst met pygame
# https://chatgpt.com/share/6a101dff-947c-83eb-901f-722a91bd39b9

import math
import random
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Particle Flow")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 24)
small_font = pygame.font.SysFont("consolas", 16)


class Particle:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 4)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.size = random.randint(2, 6)
        self.life = random.randint(100, 300)
        self.max_life = self.life

        palette = [
            (0, 255, 255),
            (255, 0, 255),
            (0, 180, 255),
            (140, 0, 255),
            (255, 80, 180),
        ]

        self.color = random.choice(palette)

    def update(self, mouse_pos):
        mx, my = mouse_pos

        dx = mx - self.x
        dy = my - self.y

        distance = max(math.hypot(dx, dy), 0.001)

        force = min(2500 / (distance * distance), 0.3)

        self.vx += dx / distance * force
        self.vy += dy / distance * force

        self.vx *= 0.985
        self.vy *= 0.985

        self.x += self.vx
        self.y += self.vy

        self.life -= 1

        if (
            self.life <= 0
            or self.x < -50
            or self.x > WIDTH + 50
            or self.y < -50
            or self.y > HEIGHT + 50
        ):
            self.reset()

    def draw(self, surface):
        alpha = int((self.life / self.max_life) * 255)

        glow_surface = pygame.Surface((self.size * 8, self.size * 8), pygame.SRCALPHA)

        glow_color = (*self.color, alpha // 4)
        core_color = (*self.color, alpha)

        center = glow_surface.get_width() // 2

        for radius in range(self.size * 3, 0, -1):
            pygame.draw.circle(
                glow_surface,
                glow_color,
                (center, center),
                radius,
            )

        pygame.draw.circle(
            glow_surface,
            core_color,
            (center, center),
            self.size,
        )

        surface.blit(
            glow_surface,
            (
                self.x - glow_surface.get_width() // 2,
                self.y - glow_surface.get_height() // 2,
            ),
        )


particles = [Particle() for _ in range(250)]


def draw_background(surface, t):
    for y in range(HEIGHT):
        ratio = y / HEIGHT

        r = int(10 + 20 * ratio)
        g = int(5 + 10 * ratio)
        b = int(20 + 60 * ratio)

        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

    grid_spacing = 40

    offset = int((t * 40) % grid_spacing)

    grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for x in range(-grid_spacing, WIDTH + grid_spacing, grid_spacing):
        pygame.draw.line(
            grid_surface,
            (0, 255, 255, 25),
            (x + offset, 0),
            (x + offset, HEIGHT),
        )

    for y in range(-grid_spacing, HEIGHT + grid_spacing, grid_spacing):
        pygame.draw.line(
            grid_surface,
            (255, 0, 255, 25),
            (0, y + offset),
            (WIDTH, y + offset),
        )

    surface.blit(grid_surface, (0, 0))


running = True
start_time = pygame.time.get_ticks()

while running:
    dt = clock.tick(FPS) / 1000
    t = (pygame.time.get_ticks() - start_time) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    mouse_pos = pygame.mouse.get_pos()

    draw_background(screen, t)

    connection_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for particle in particles:
        particle.update(mouse_pos)

    for i, p1 in enumerate(particles):
        for p2 in particles[i + 1 :]:
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            dist = math.hypot(dx, dy)

            if dist < 100:
                alpha = int(120 * (1 - dist / 100))

                pygame.draw.line(
                    connection_surface,
                    (100, 200, 255, alpha),
                    (p1.x, p1.y),
                    (p2.x, p2.y),
                    1,
                )

    screen.blit(connection_surface, (0, 0))

    for particle in particles:
        particle.draw(screen)

    pulse = (math.sin(t * 2) + 1) / 2

    title = font.render("NEON FLOW", True, (255, 255, 255))
    subtitle = small_font.render(
        "Move your mouse to manipulate the particles",
        True,
        (150, 200, 255),
    )

    glow = pygame.Surface((title.get_width() + 30, title.get_height() + 30), pygame.SRCALPHA)

    pygame.draw.rect(
        glow,
        (0, 255, 255, int(40 + pulse * 50)),
        glow.get_rect(),
        border_radius=20,
    )

    screen.blit(glow, (30, 25))
    screen.blit(title, (45, 35))
    screen.blit(subtitle, (45, 70))

    fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (WIDTH - 120, 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
