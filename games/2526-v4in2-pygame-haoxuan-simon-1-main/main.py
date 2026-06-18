import game
import Menu
import pygame
import os
import Editor

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
first_run = True
back = False

SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.SCALED
)


def fade_out(screen, speed=800):
    clock = pygame.time.Clock()
    fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surf.fill((0, 0, 0))
    alpha = 0
    while alpha < 255:
        dt = clock.tick(60) / 1000
        alpha += speed * dt
        if alpha > 255:
            alpha = 255
        fade_surf.set_alpha(int(alpha))
        screen.blit(fade_surf, (0, 0))
        pygame.display.flip()


# Level loader function


def load_levels():
    levels_folder = "/workspaces/2526-v4in2-pygame-haoxuan-simon-1/levels"
    return [
        os.path.join(levels_folder, file)
        for file in os.listdir(levels_folder)
        if file.endswith(".json")
    ]


if __name__ == "__main__":
    levels = load_levels()
    running = True
    while running:
        result = None
        # Menu

        if first_run == True or back:
            # if we're returning from game/editor, fade out first
            if back:
                fade_out(SCREEN)
            selected_level = Menu.Menu(SCREEN, levels, fade_in=back)
            back = False
        if selected_level is None:
            running = False
            break

        # Editor
        if selected_level == "EDITOR":
            back = Editor.main(SCREEN, False)
            if back:
                # fade out from editor back to menu
                fade_out(SCREEN)

        # Game
        else:
            result = game.game(selected_level, SCREEN, True, False)
            # if game returned True -> go back to menu
            if result is True:
                back = True
                fade_out(SCREEN)
                continue

        # ESC = pause
        if result == "QUIT":
            running = False
