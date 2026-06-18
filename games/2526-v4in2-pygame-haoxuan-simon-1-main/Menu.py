import pygame
import os


def Menu(screen, levels, fade_in=False):

    FPS = 60
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    running = True
    fps_clock = pygame.time.Clock()

    font_big = pygame.font.Font('PressStart2P-Regular.ttf', 48)
    font = pygame.font.Font('PressStart2P-Regular.ttf', 24)

    background_img = pygame.image.load('background.jpg').convert()
    background_img = pygame.transform.scale(background_img, (1280, 720))

    selected_level = 0

    Start_screen = 0
    Level_select = 1
    current_screen = Start_screen

    transitioning = False
    transition_alpha = 0
    transition_state = None   # None / fade_out / fade_in
    fade_speed = 1000
    next_screen = None
    return_level = None

    if fade_in:
        transitioning = True
        transition_state = "fade_in"
        transition_alpha = 255

    def start_transition(target_screen):
        nonlocal transitioning, transition_state, next_screen
        transitioning = True
        transition_state = "fade_out"
        next_screen = target_screen

    def draw_center(text, color, y):
        img = font.render(text, True, color)
        rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(img, rect)

    print("Menu is running")

    while running:

        screen.blit(background_img, (0, 0))
        dt = fps_clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN and not transitioning:
                if current_screen == Start_screen:
                    if event.key == pygame.K_SPACE:
                        start_transition(Level_select)
                    if event.key == pygame.K_e:
                        transitioning = True
                        transition_state = "fade_out"
                        next_screen = None
                        return_level = "EDITOR"

                elif current_screen == Level_select:
                    if event.key == pygame.K_ESCAPE:
                        start_transition(Start_screen)
                    if len(levels) > 0:
                        if event.key == pygame.K_UP:
                            selected_level = (selected_level - 1) % len(levels)

                        if event.key == pygame.K_DOWN:
                            selected_level = (selected_level + 1) % len(levels)

                        if event.key == pygame.K_RETURN:
                            transitioning = True
                            transition_state = "fade_out"
                            next_screen = None
                            return_level = levels[selected_level]

        # Draw screens
        if current_screen == Start_screen:
            title = font_big.render(
                "BREAKOUT", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 220)))
            draw_center("PRESS SPACE TO START", (255, 255, 255), 380)
            draw_center("PRESS E FOR EDITOR", (255, 255, 255), 430)
            draw_center("PRESS ESC TO QUIT", (255, 255, 255), 480)

        elif current_screen == Level_select:
            title = font_big.render("SELECT LEVEL", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 120)))
            if len(levels) == 0:
                draw_center("NO LEVELS FOUND", (255, 0, 0), 300)
            else:
                for i, level in enumerate(levels):
                    level_name = os.path.basename(level).replace(".json", "")
                    if i == selected_level:
                        text = font.render(
                            f"> {level_name}", True, (255, 255, 0))
                    else:
                        text = font.render(level_name, True, (255, 255, 255))
                    screen.blit(text, (420, 220 + i * 60))
                draw_center("ENTER = PLAY   ESC = BACK", (200, 200, 200), 620)

        # Transition
        if transitioning:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))

            if transition_state == "fade_out":
                transition_alpha += fade_speed * dt
                if transition_alpha >= 255:
                    transition_alpha = 255
                alpha = max(0, min(255, int(transition_alpha)))
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                if transition_alpha >= 255:
                    if return_level is not None:
                        return return_level
                    current_screen = next_screen
                    transition_state = "fade_in"

            elif transition_state == "fade_in":
                transition_alpha -= fade_speed * dt
                if transition_alpha <= 0:
                    transition_alpha = 0
                alpha = max(0, min(255, int(transition_alpha)))
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                if transition_alpha <= 0:
                    transitioning = False
                    transition_state = None

        pygame.display.flip()
        fps_clock.tick(FPS)
