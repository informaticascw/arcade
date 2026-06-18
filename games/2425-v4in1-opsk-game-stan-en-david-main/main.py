#
# BREAKOUT GAME 
#

import pygame, random, math

# screen constants
FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Initialize message for winning / losing
game_status_msg = ""

# Game starts in main menu
players = None  # Players variable for multiplayer mode
gameMode = "choosePlayers"
platform = None  # Platform variable for the game mode
level = None
unlocked = 1  # Levels that are unlocked by default
highscore = 0


# Initiate game
pygame.init() # pygame functie voor het starten van het spel
title_font = pygame.font.SysFont('default', 134) # lettertype en grootte door middel van pygame functie
font = pygame.font.SysFont('default', 66) # lettertype en grootte door middel van pygame functie
small_font = pygame.font.SysFont('default', 38) # aangepaste lettergrootte voor minder belangrijke berichten
mini_font = pygame.font.SysFont('default', 26) # aangepaste lettergrootte voor kleine berichten
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

# Default keybinds with a dictionary (player can rebind)
keybinds = { 
    "right": pygame.K_d,
    "left": pygame.K_a,
    "pause": pygame.K_SPACE,
    "return": pygame.K_r
}

def swept_aabb(ball_rect, vx, vy, target_rect):
    # Calculate entry and exit times for x and y
    if vx > 0:
        x_entry = target_rect.left - (ball_rect.right)
        x_exit = target_rect.right - ball_rect.left
    else:
        x_entry = target_rect.right - ball_rect.left
        x_exit = target_rect.left - (ball_rect.right)
    if vy > 0:
        y_entry = target_rect.top - (ball_rect.bottom)
        y_exit = target_rect.bottom - ball_rect.top
    else:
        y_entry = target_rect.bottom - ball_rect.top
        y_exit = target_rect.top - (ball_rect.bottom)

    # Avoid division by zero
    tx_entry = x_entry / vx if vx != 0 else float('-inf')
    tx_exit = x_exit / vx if vx != 0 else float('inf')
    ty_entry = y_entry / vy if vy != 0 else float('-inf')
    ty_exit = y_exit / vy if vy != 0 else float('inf')

    entry_time = max(tx_entry, ty_entry)
    exit_time = min(tx_exit, ty_exit)

    # No collision if entry is after exit, or entry is outside [0,1]
    if entry_time > exit_time or (tx_entry < 0 and ty_entry < 0) or entry_time > 1 or entry_time < 0:
        return 1.0, None  # No collision in this frame

    # Determine collision normal
    if tx_entry > ty_entry:
        normal = (-1 if vx > 0 else 1, 0)
    else:
        normal = (0, -1 if vy > 0 else 1)
    return entry_time, normal

# class for buttons
class Button:
    def __init__(self, rect, text, color, error_msg=""):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.error_msg = error_msg

    def draw(self, surface):

        # Make button
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, "black", self.rect, 3)

        # Draw text
        txt_surf = font.render(self.text, True, "black")
        surface.blit(txt_surf, (
            self.rect.centerx - txt_surf.get_width() // 2,
            self.rect.centery - txt_surf.get_height() // 2))

        # error message for conflicting keybinds
        if self.error_msg:
            error_surf = small_font.render(self.error_msg, True, "red")
            error_x = self.rect.right + 20
            error_y = self.rect.centery - error_surf.get_height() // 2
            surface.blit(error_surf, (error_x, error_y))

    # Returns True when clicked
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
def choosePlatform():
    global platform, keybinds
    print("game mode: platform select")

    options = ["Computer", "Arcade"]
    selected_index = 0
    done = False

    while True:
        screen.fill("darkblue")

        for i, opt in enumerate(options):
            if i == selected_index:
                color = "lime" 
            else:
                color = "white"
            txt = font.render(opt, True, color)
            screen.blit(txt, (
                SCREEN_WIDTH // 2 - txt.get_width() // 2,
                SCREEN_HEIGHT // 2 - 80 + i * 100
            ))
        
        title = title_font.render("BREAKOUT!", True, "orange")
        bottom_txt = small_font.render(
            f"Press W/S to navigate, E to select.", True, "white")
        screen.blit(bottom_txt, (
            SCREEN_WIDTH // 2 - bottom_txt.get_width() // 2, SCREEN_HEIGHT - 50))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 75))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if selected_index == 1:
                        selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_s:
                    if selected_index == 0:
                        selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_e:
                    platform = options[selected_index].lower()
                    
                    if platform == "arcade":
                        # Keybinds aangepast aan de arcadekast (gebaseerd op je afbeelding)
                        keybinds = {
                            "right": pygame.K_d,
                            "left": pygame.K_a,
                            "pause": pygame.K_r,
                            "return": pygame.K_q,
                            "p2_right": pygame.K_l,
                            "p2_left": pygame.K_j,
                        }
                    else:
                        # Computer keybinds (standaard)
                        keybinds = {
                            "right": pygame.K_d,
                            "left": pygame.K_a,
                            "pause": pygame.K_r,
                            "return": pygame.K_q,
                            "p2_right": pygame.K_l,
                            "p2_left": pygame.K_j,
                        }
                    done = True
                    break
        if done:
            break


def choosePlayers():
    print("game mode: choose single or multiplayer")
    global players


    selected = 0 # Index of the selected button

    def build_choose_players_buttons(selected):
        labels = ["Singleplayer", "Multiplayer", "Quit"]
        colors = []
        for i in range(len(labels) - 1):
            if platform == "arcade" and i == selected:
                colors.append("lime")
            else:
                colors.append("white")
        if len(labels) - 1 == selected:
            colors.append("darkred")
        else:
            colors.append("red")
        buttons = []
        for i, label in enumerate(labels):
            btn = Button(
                (SCREEN_WIDTH//2 - 150, 200 + i*150, 300, 100),
                label,
                colors[i]
            )
            buttons.append(btn)
        return buttons

    while True:

        # Reset screen
        screen.fill("blue")

        # Draw buttons


        for event in pygame.event.get():

            # Just some code to copy paste in every screen loop
            if event.type == pygame.QUIT:
                return "quit"
            if platform == "arcade":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if selected!= 0:
                            selected = (selected - 1) % len(buttons)
                    elif event.key == pygame.K_s:
                        if selected != len(buttons) - 1:
                            selected = (selected + 1) % len(buttons)
                    elif event.key == pygame.K_e:
                        if selected == 0:
                            players = 1  # singleplayer
                            return "mainMenu"
                        elif selected == 1:
                            players = 2  # multiplayer
                            keybinds.update({
                                "p2_right": pygame.K_l,
                                "p2_left": pygame.K_j,
                            })
                            return "mainMenu"
                        elif selected == 2:
                            return "quit"
            else:
                # Checks if buttons are clicked and reacts by going to other menu / stopping the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].is_clicked(event.pos):
                        players = 1  # singleplayer
                        return "mainMenu"
                    elif buttons[1].is_clicked(event.pos):
                        players = 2  # multiplayer
                        keybinds.update({
                            "p2_right": pygame.K_l,
                            "p2_left": pygame.K_j,
                        })
                        return "mainMenu"
                    elif buttons[2].is_clicked(event.pos):
                        return "quit"

        buttons = build_choose_players_buttons(selected)
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        fps_clock.tick(FPS)


# Main menu code
def mainMenu():

    # Developer info
    print("game mode: main menu")

    highscore_msg = small_font.render(f"Highscore: {highscore}", True, "cornsilk2")
    selected = 0 # Index of the selected button

    def build_main_menu_buttons(selected):
        labels = ["Levels", "Endless", "Controlls", "How to Play", "Quit"]
        colors = []
        for i in range(len(labels) - 1):
            if platform == "arcade" and i == selected:
                colors.append("lime")
            else:
                colors.append("white")
        if len(labels) - 1 == selected:
            colors.append("darkred")
        else:
            colors.append("red")
        buttons = []
        for i, label in enumerate(labels):
            btn = Button(
                (SCREEN_WIDTH//2 - 200, 50 + i*120, 400, 90),
                label,
                colors[i]
            )
            buttons.append(btn)
        return buttons

    while True:

        # Reset screen
        screen.fill("blue")

        # Draw buttons



        # Draw buttons


        for event in pygame.event.get():

            # Just some code to copy paste in every screen loop
            if event.type == pygame.QUIT:
                return "quit"
            if platform == "arcade":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if selected!= 0:
                            selected = (selected - 1) % len(buttons)
                    elif event.key == pygame.K_s:
                        if selected != len(buttons) - 1:
                            selected = (selected + 1) % len(buttons)
                    elif event.key == pygame.K_e:
                        if selected == 0:
                            return "levels"
                        elif selected == 1:
                            return "endless"
                        elif selected == 2:
                            return "controlls"
                        elif selected == 3:
                            return "howToPlay"
                        elif selected == 4:
                            return "quit"
            else:
                # Checks if buttons are clicked and reacts by going to other menu / stopping the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].is_clicked(event.pos):
                        return "levels"
                    elif buttons[1].is_clicked(event.pos):
                        return "endless"
                    elif buttons[2].is_clicked(event.pos):
                        return "controlls"
                    elif buttons[3].is_clicked(event.pos):
                        return "howToPlay"
                    elif buttons[4].is_clicked(event.pos):
                        return "quit"

        buttons = build_main_menu_buttons(selected)
        for button in buttons:
            button.draw(screen)

        # Update screen
        if highscore > 0:
                screen.blit(highscore_msg, (10, 10))
        pygame.display.flip()
        fps_clock.tick(FPS)

# Controlls code
def controlls():

    # Developer info
    print("game mode: controlls")

    # Create variables
    waiting_for = None
    buttons = []
    selected = 0
    rebinding = False
    
    # Just easier to write key_name() instead of pygame.key.name()
    def key_name(k):
        return pygame.key.name(k)
    
    # Error handling (for conflicting keybinds)
    def has_conflicts():

        # Create variables
        seen = {}
        conflicts = {}

        # Check for double keys
        for action, key in keybinds.items():
            if key in seen:
                conflicts[action] = seen[key]
                conflicts[seen[key]] = action
            else:
                seen[key] = action

        # Return conflicting keys
        return conflicts

    # Update screen
    def redraw(rebinding):
        screen.fill("blue")
        for i, button in enumerate(buttons):
            if not rebinding:
                if platform == "arcade" and i == selected:
                    button.color = "lime"
                else:
                    button.color = "white"
            button.draw(screen)


        back_text = small_font.render(f"Press {key_name(keybinds['return'])} to return to main menu", True, "black")
        screen.blit(back_text, (20, SCREEN_HEIGHT - 50))

        if has_conflicts():
            warning = small_font.render("Resolve duplicate keybinds before returning!", True, "red")
            screen.blit(warning, (20, SCREEN_HEIGHT - 100))

        pygame.display.flip()

    def rebuild_buttons():
        buttons.clear()
        spacing = 100
        y = 50
        conflicts = has_conflicts()
        for action, key in keybinds.items():
            if action in conflicts:
                msg = f"Conflicts with {conflicts[action].title()}"
                btn = Button((SCREEN_WIDTH//2 - 250, y, 500, 80), f"{action.title()}: {key_name(key)}", "red", msg)
            else:
                btn = Button((SCREEN_WIDTH//2 - 250, y, 500, 80), f"{action.title()}: {key_name(key)}", "white")
            buttons.append(btn)
            y += spacing

    def highlight_button(pressed):
        buttons.clear()
        spacing = 100
        y = 50
        conflicts = has_conflicts()
        for action, key in keybinds.items():
            if action == pressed:
                color = "yellow"
            elif action in conflicts:
                color = "red"
            else:
                color = "white"

            msg = f"Conflicts with {conflicts[action].title()}" if action in conflicts else ""
            btn = Button((SCREEN_WIDTH//2 - 250, y, 500, 80), f"{action.title()}: {key_name(key)}", color, msg)
            buttons.append(btn)
            y += spacing

    rebuild_buttons()

    while True:
        redraw(rebinding)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if waiting_for:
                if event.type == pygame.KEYDOWN:
                    keybinds[waiting_for] = event.key
                    waiting_for = None
                    rebuild_buttons()
                    rebinding = False
            if platform == "arcade":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        selected = (selected - 1) % len(buttons)
                    elif event.key == pygame.K_s:
                        selected = (selected + 1) % len(buttons)
                    elif event.key == pygame.K_e:
                        waiting_for = buttons[selected].text.split(":")[0].lower()
                        rebinding = True
                        highlight_button(waiting_for)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.is_clicked(event.pos):
                        waiting_for = btn.text.split(":")[0].lower()
                        highlight_button(waiting_for)
            if event.type == pygame.KEYDOWN and event.key == keybinds["return"]:
                if not has_conflicts():
                    return
        fps_clock.tick(FPS)

# How to play code
def howToPlay():
    print("game mode: how to play")
    running = True
    if players == 1:
        explanation_msg = (
            f"Use the bouncing ball to erase all the blocks!\n"
            f"Move your paddle to the right with {pygame.key.name(keybinds['right'])}, and to the left with {pygame.key.name(keybinds['left'])}.\n"
            f"You can always pause the game with {pygame.key.name(keybinds['pause'])}, or even return to the main menu with {pygame.key.name(keybinds['return'])}.\n"
            "If you see a powerup falling down, \n"
            "catch it and the balls will double, or your paddle speed will increase."
        )
    else:
        explanation_msg = (
            f"Use the bouncing ball to erase all the blocks!\n"
            f"Move your paddle to the right with {pygame.key.name(keybinds['right'])} ({pygame.key.name(keybinds['p2_right'])} for player 2), and to the left with {pygame.key.name(keybinds['left'])} ({pygame.key.name(keybinds['p2_left'])} for player 2).\n"
            f"You can always pause the game with {pygame.key.name(keybinds['pause'])}, or even return to the main menu with {pygame.key.name(keybinds['return'])}.\n"
            "If you see a powerup falling down, \n"
            "catch it and the balls will double, or your paddle speed will increase."
        )
    lines = explanation_msg.split('\n')

    while running:
        screen.fill("blue")

        title_text = font.render("How to Play", True, "white")
        screen.blit(title_text, (
            SCREEN_WIDTH // 2 - title_text.get_width() // 2,
            80
        ))

        for i, line in enumerate(lines):
            line_surf = small_font.render(line, True, "black")
            screen.blit(line_surf, (
                SCREEN_WIDTH // 2 - line_surf.get_width() // 2,
                200 + i * 60
            ))

        footer_text = small_font.render(f"Press {pygame.key.name(keybinds['return'])} to return to main menu", True, "black")
        screen.blit(footer_text, (
            SCREEN_WIDTH // 2 - footer_text.get_width() // 2,
            SCREEN_HEIGHT - 100
        ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == keybinds["return"]:
                return

        pygame.display.flip()
        fps_clock.tick(FPS)

# Levels code
def levels():
    print("game mode: levels")
    spacing = 0.14  # afstand tussen knoppen (als factor van schermbreedte)
    size = SCREEN_WIDTH * 0.07
    y = SCREEN_HEIGHT * 0.5 - size * 0.5
    selected = 0 # Index of the selected button

    level_buttons = []
    
    def build_levels_buttons(selected):
        labels = ["1", "2", "3", "4", "5"]
        colors = []
        for i in range(len(labels)):
            if platform == "arcade" and i == selected:
                colors.append("lime")
            elif unlocked > i:
                colors.append("white")
            else:
                colors.append("gray")
        buttons = []
        for i, label in enumerate(labels):
            btn = Button(
                (SCREEN_WIDTH * (0.24 + i * spacing), y, size, size),
                label,
                colors[i]
            )
            buttons.append(btn)
        return buttons

    while True:
        screen.fill("blue")

        # Teken de knoppen
        for btn in level_buttons:
            btn.draw(screen)

        for event in pygame.event.get():

            # Just some code to copy paste in every screen loop
            if event.type == pygame.QUIT:
                return "quit"
            if platform == "arcade":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if selected!= 0:
                            selected = (selected - 1) % len(buttons)
                    elif event.key == pygame.K_s:
                        if selected != unlocked - 1:
                            selected = (selected + 1) % len(buttons)
                    elif event.key == pygame.K_e:
                        if unlocked >= selected + 1:
                            print(f"Level {selected + 1} gekozen")
                            return selected + 1
            elif platform == "computer":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, btn in enumerate(buttons, start=1):
                        if btn.is_clicked(event.pos):
                            print("clicked")
                            if unlocked >= i:  # alleen klikbaar als level is unlocked
                                print(f"Level {i} gekozen")
                                return i
                elif event.type == pygame.KEYDOWN and event.key == keybinds["return"]:
                    return "mainMenu"
            
        buttons = build_levels_buttons(selected)
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        fps_clock.tick(FPS)


# Main game loop
def normalPlay(level, players):
    screen.fill("orange")

    FPS = 30 # Frames Per Second
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # ball constants
    BALL_WIDTH = 16
    BALL_HEIGHT = 16

    # paddle constants
    PADDLE_WIDTH = 144
    PADDLE_HEIGHT = 32

    # brick constants
    BRICK_WIDTH = 96
    BRICK_HEIGHT = 32

    # powerup constants
    POWERUP_WIDTH = 32
    POWERUP_HEIGHT = 32

    # --- MULTI-BALL SUPPORT ---
    balls = [{
        "x": random.randint(0, SCREEN_WIDTH),
        "y": SCREEN_HEIGHT * 0.4,
        "speed_x": 6,
        "speed_y": 6,
        "original_speed_x": 6,
        "original_speed_y": 6,
        "prev_x": 0,
        "prev_y": 0
    }]
    balls[0]["prev_x"] = balls[0]["x"]
    balls[0]["prev_y"] = balls[0]["y"]

    if players == 1:
        multiplayer = False
    else:
        multiplayer = True

    # paddle defenitions
    paddle_x = SCREEN_WIDTH / 2
    paddle_y = SCREEN_HEIGHT * 0.9

    if multiplayer:
        paddle2_x = SCREEN_WIDTH / 2
        paddle2_y = SCREEN_HEIGHT * 0.75


    powerups = []
    paddle_speed = 10  # standard paddle speed
    paddle2_speed = 10  # standard paddle speed

    # class for powerups
    class PowerUp:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 32, 32)
            self.speed = 4  # valsnelheid

        def update(self):
            self.rect.y += self.speed

        def draw(self, surface):
            surface.blit(powerup_img, (self.rect.x, self.rect.y))

    def bricksXGen(level):
        bricks_x = []
        for x in range(level):
            xValue = 16
            for y in range(13):
                bricks_x.append(xValue)
                xValue += 96
        return bricks_x

    def bricksYGen(level):
        bricks_y = []
        yValue = 50
        for x in range(level):
            for y in range(13):
                bricks_y.append(yValue)
            yValue += 42 
        return bricks_y

    # Generate bricks based on level
    bricks_x = bricksXGen(level)
    bricks_y = bricksYGen(level)

    prev_paddle_x = paddle_x
    prev_paddle_y = paddle_y

    paddleSpriteCountdown = 0
    paddle2SpriteCountdown = 0



    spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

    ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
    ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
    ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

    paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
    paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  

    paddle_speed_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
    paddle_speed_img.blit(spritesheet, (0, 0), (349, 910, 243, 64))   
    paddle_speed_img = pygame.transform.scale(paddle_speed_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  

    brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
    brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))   
    brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

    powerup_img = pygame.Surface((64, 61), pygame.SRCALPHA)  
    powerup_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))   
    powerup_img = pygame.transform.scale(powerup_img, (POWERUP_WIDTH, POWERUP_HEIGHT))

    endGame = False

    # Initial draw
    screen.fill('orange')
    for ball in balls:
        screen.blit(ball_img, (ball["x"], ball["y"]))
    if paddleSpriteCountdown == 0:
        screen.blit(paddle_img, (paddle_x, paddle_y))
    else:
        screen.blit(paddle_speed_img, (paddle_x, paddle_y))
    if multiplayer:
        if paddle2SpriteCountdown == 0:
            screen.blit(paddle_img, (paddle2_x, paddle2_y))
        else:
            screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
        p1_label = mini_font.render("Player 1", True, "black")
        p2_label = mini_font.render("Player 2", True, "black")
        screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
        screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
    for brick in range(len(bricks_x)):
        screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
    pygame.display.flip()

    for count in range(3, 0, -1):
        screen.fill('orange')
        for ball in balls:
            screen.blit(ball_img, (ball["x"], ball["y"]))
        if paddleSpriteCountdown == 0:
            screen.blit(paddle_img, (paddle_x, paddle_y))
        else:
            screen.blit(paddle_speed_img, (paddle_x, paddle_y))
        if multiplayer:
            if paddle2SpriteCountdown == 0:
                screen.blit(paddle_img, (paddle2_x, paddle2_y))
            else:
                screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
            p1_label = mini_font.render("Player 1", True, "black")
            p2_label = mini_font.render("Player 2", True, "black")
            screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
            screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
        for brick in range(len(bricks_x)):
            screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
        countdown_text = font.render(str(count), True, "gray")
        screen.blit(countdown_text, (
            SCREEN_WIDTH // 2 - countdown_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2
        ))
        pygame.display.flip()
        pygame.time.delay(1000)

    screen.fill('orange')
    for ball in balls:
        screen.blit(ball_img, (ball["x"], ball["y"]))
    if paddleSpriteCountdown == 0:
        screen.blit(paddle_img, (paddle_x, paddle_y))
    else:
        screen.blit(paddle_speed_img, (paddle_x, paddle_y))
    if multiplayer:
        if paddle2SpriteCountdown == 0:
            screen.blit(paddle_img, (paddle2_x, paddle2_y))
        else:
            screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
        p1_label = mini_font.render("Player 1", True, "black")
        p2_label = mini_font.render("Player 2", True, "black")
        screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
        screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
    for brick in range(len(bricks_x)):
        screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
    go_text = font.render("GO!", True, "gray")
    screen.blit(go_text, (
        SCREEN_WIDTH // 2 - go_text.get_width() // 2,
        SCREEN_HEIGHT // 2 - go_text.get_height() // 2
    ))
    pygame.display.flip()
    pygame.time.delay(500)

    while not endGame:
        toMainMenu = False

        # Store previous positions for all balls
        for ball in balls:
            ball["prev_x"] = ball["x"]
            ball["prev_y"] = ball["y"]
        prev_paddle_x = paddle_x
        prev_paddle_y = paddle_y

        if multiplayer:
            prev_paddle2_x = paddle2_x
            prev_paddle2_y = paddle2_y
        
        if paddleSpriteCountdown > 0:
            paddleSpriteCountdown -=1
        if paddle2SpriteCountdown > 0:
            paddle2SpriteCountdown -= 1

        # game end input config and pause function
        keys = pygame.key.get_pressed() 
            
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN and event.key == keybinds["pause"]:
                paused = True
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == keybinds["return"]:
                            toMainMenu = True
                            break
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == keybinds["pause"]:
                            paused = False
                    if toMainMenu:
                        break
                    screen.fill("orange")
                    paused_msg = "Paused"
                    paused_img = font.render(paused_msg, True, "gray")
                    screen.blit(paused_img, (
                        SCREEN_WIDTH / 2 - paused_img.get_width() / 2,
                        SCREEN_HEIGHT / 2 - paused_img.get_height() / 2
                    ))

                    pygame.display.flip()
                    fps_clock.tick(FPS)
            if toMainMenu:
                break
        
        if toMainMenu:
            break

        if keys[keybinds["return"]]:
            break

        # paddle inputs
        if keys[keybinds["right"]]:
            paddle_x += paddle_speed
        if keys[keybinds["left"]]:
            paddle_x -= paddle_speed

        if multiplayer:
            if keys[keybinds["p2_right"]]:
                paddle2_x += paddle2_speed
            if keys[keybinds["p2_left"]]:
                paddle2_x -= paddle2_speed

        # paddle bounds
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
        
        if multiplayer:
            if paddle2_x < 0:
                paddle2_x = 0
            if paddle2_x + PADDLE_WIDTH > SCREEN_WIDTH:
                paddle2_x = SCREEN_WIDTH - PADDLE_WIDTH

        paddle_rect = pygame.Rect(int(paddle_x), int(paddle_y), PADDLE_WIDTH, PADDLE_HEIGHT)
        if multiplayer:
            paddle2_rect = pygame.Rect(int(paddle2_x), int(paddle2_y), PADDLE_WIDTH, PADDLE_HEIGHT)

        # collision detection for powerups
        for powerup in powerups[:]:
            powerup.update()
            if powerup.rect.colliderect(paddle_rect):
                effect = random.choice(["speed", "ball"])
                if effect == "speed":
                    print("Paddle speed boosted")
                    paddle_speed *= 1.3
                    paddleSpriteCountdown = 40
                elif effect == "ball":
                    print("Balls doubled")
                    new_balls = []
                    for ball in balls:
                        new_balls.append({
                            "x": ball["x"],
                            "y": ball["y"],
                            "speed_x": -ball["speed_x"],
                            "speed_y": ball["speed_y"],
                            "original_speed_x": -ball["original_speed_x"],
                            "original_speed_y": ball["original_speed_y"],
                            "prev_x": ball["x"],
                            "prev_y": ball["y"]
                        })
                    balls.extend(new_balls)
                powerups.remove(powerup)
            if multiplayer:
                if powerup.rect.colliderect(paddle2_rect):
                    effect = random.choice(["speed", "ball"])
                    if effect == "speed":
                        print("Paddle speed boosted")
                        paddle2_speed *= 1.4
                        paddle2SpriteCountdown = 40
                    elif effect == "ball":
                        print("Balls doubled")
                        new_balls = []
                        for ball in balls:
                            new_balls.append({
                                "x": ball["x"],
                                "y": ball["y"],
                                "speed_x": -ball["speed_x"],
                                "speed_y": ball["speed_y"],
                                "original_speed_x": -ball["original_speed_x"],
                                "original_speed_y": ball["original_speed_y"],
                                "prev_x": ball["x"],
                                "prev_y": ball["y"]
                            })
                        balls.extend(new_balls)
                    powerups.remove(powerup)
            if powerup.rect.y > SCREEN_HEIGHT:
                powerups.remove(powerup)

        # --- BALL LOGIC FOR ALL BALLS ---
        for ball in balls[:]:  # copy to allow removal
            # move ball
            ball["x"] += ball["speed_x"]
            ball["y"] += ball["speed_y"]

            # bounce ball off screen borders
            if ball["x"] < 0:
                ball["speed_x"] = abs(ball["speed_x"])
                ball["original_speed_x"] = abs(ball["speed_x"])
            if ball["x"] + BALL_WIDTH > SCREEN_WIDTH:
                ball["speed_x"] = -abs(ball["speed_x"])
                ball["original_speed_x"] = -abs(ball["speed_x"])
            if ball["y"] < 0:
                ball["speed_y"] = abs(ball["speed_y"])
                ball["original_speed_y"] = abs(ball["speed_y"])

            # paddle collision
            ball_dx = ball["x"] - ball["prev_x"]
            ball_dy = ball["y"] - ball["prev_y"]
            paddle_dx = paddle_x - prev_paddle_x
            paddle_dy = paddle_y - prev_paddle_y

            rel_vx = ball_dx - paddle_dx
            rel_vy = ball_dy - paddle_dy

            entry_time, normal = swept_aabb(
                pygame.Rect(ball["prev_x"], ball["prev_y"], BALL_WIDTH, BALL_HEIGHT),
                rel_vx, rel_vy,
                pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
            )

            if entry_time < 1.0:
                ball["x"] = ball["prev_x"] + rel_vx * entry_time
                ball["y"] = ball["prev_y"] + rel_vy * entry_time

                if normal == (0, -1):  # van boven op paddle geraakt
                    incoming_angle = math.degrees(math.atan2(-ball["speed_y"], ball["speed_x"]))
                    reflected_angle = -incoming_angle
                    impact_offset = ((ball["x"] + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
                    bounce_strength = 1.0 - abs(impact_offset) * -0.5
                    angle_deviation = (1 - bounce_strength) * 30 * (-1 if impact_offset < 0 else 1)
                    new_angle = reflected_angle + angle_deviation
                    speed = math.hypot(ball["speed_x"], ball["speed_y"])
                    rad = math.radians(new_angle)
                    ball["speed_x"] = speed * math.cos(rad)
                    ball["speed_y"] = -speed * math.sin(rad)
                elif normal == (-1, 0):
                    ball["speed_x"] = -abs(ball["speed_x"])
                elif normal == (1, 0):
                    ball["speed_x"] = abs(ball["speed_x"])

            if multiplayer:
                paddle_dx = paddle2_x - prev_paddle2_x
                paddle_dy = paddle2_y - prev_paddle2_y

                rel_vx = ball_dx - paddle_dx
                rel_vy = ball_dy - paddle_dy

                entry_time, normal = swept_aabb(
                    pygame.Rect(ball["prev_x"], ball["prev_y"], BALL_WIDTH, BALL_HEIGHT),
                    rel_vx, rel_vy,
                    pygame.Rect(paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
                )

                if entry_time < 1.0:
                    ball["x"] = ball["prev_x"] + rel_vx * entry_time
                    ball["y"] = ball["prev_y"] + rel_vy * entry_time

                    if normal == (0, -1):
                        incoming_angle = math.degrees(math.atan2(-ball["speed_y"], ball["speed_x"]))
                        reflected_angle = -incoming_angle
                        impact_offset = ((ball["x"] + BALL_WIDTH / 2) - (paddle2_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
                        bounce_strength = 1.0 - abs(impact_offset) * -0.5
                        angle_deviation = (1 - bounce_strength) * 30 * (-1 if impact_offset < 0 else 1)
                        new_angle = reflected_angle + angle_deviation
                        speed = math.hypot(ball["speed_x"], ball["speed_y"])
                        rad = math.radians(new_angle)
                        ball["speed_x"] = speed * math.cos(rad)
                        ball["speed_y"] = -speed * math.sin(rad)
                    elif normal == (0, 1):
                        incoming_angle = math.degrees(math.atan2(ball["speed_y"], ball["speed_x"]))
                        reflected_angle = -incoming_angle
                        impact_offset = ((ball["x"] + BALL_WIDTH / 2) - (paddle2_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
                        bounce_strength = -1.0 + abs(impact_offset) * 0.5
                        angle_deviation = (1 - bounce_strength) * 30 * (-1 if impact_offset < 0 else 1)
                        new_angle = reflected_angle + angle_deviation
                        speed = math.hypot(ball["speed_x"], ball["speed_y"])
                        rad = math.radians(new_angle)
                        ball["speed_x"] = speed * math.cos(rad)
                        ball["speed_y"] = -speed * math.sin(rad)
                    elif normal == (-1, 0):
                        ball["speed_x"] = -abs(ball["speed_x"])
                    elif normal == (1, 0):
                        ball["speed_x"] = abs(ball["speed_x"])


            # brick collisions
            for i in range(len(bricks_x)):
                brick_rect = pygame.Rect(bricks_x[i], bricks_y[i], BRICK_WIDTH, BRICK_HEIGHT)
                ball_dx = ball["x"] - ball["prev_x"]
                ball_dy = ball["y"] - ball["prev_y"]
                entry_time, normal = swept_aabb(
                    pygame.Rect(ball["prev_x"], ball["prev_y"], BALL_WIDTH, BALL_HEIGHT),
                    ball_dx, ball_dy,
                    brick_rect
                )
                if entry_time < 1.0:
                    ball["x"] = ball["prev_x"] + ball_dx * entry_time
                    ball["y"] = ball["prev_y"] + ball_dy * entry_time
                    if normal[0] != 0:
                        ball["speed_x"] *= -1
                        ball["original_speed_x"] *= -1
                    if normal[1] != 0:
                        ball["speed_y"] *= -1
                        ball["original_speed_y"] *= -1
                    ball["speed_x"] *= 1.04
                    ball["speed_y"] *= 1.04

                    # 20% chance to spawn a powerup
                    powerupSpawnRng = random.randint(0, 4)
                    if powerupSpawnRng == 0:
                        print("powerup spawned")
                        powerups.append(PowerUp(bricks_x[i] + BRICK_WIDTH / 2 - POWERUP_HEIGHT / 2, bricks_y[i] + BRICK_HEIGHT / 2 - POWERUP_HEIGHT / 2))
                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break

        # Remove balls that fall below the screen
        balls = [ball for ball in balls if ball["y"] < SCREEN_HEIGHT]

        if not balls:
            game_status_msg = "You Lost!"
            game_status_img = font.render(game_status_msg, True, "red")
            msg_width = game_status_img.get_width()
            msg_height = game_status_img.get_height()
            endGame = True

        if len(bricks_x) == 0:
            for ball in balls:
                ball["speed_x"] = 0
                ball["speed_y"] = 0
            game_status_msg = "You Won!"
            game_status_img = font.render(game_status_msg, True, "green")
            msg_width = game_status_img.get_width()
            msg_height = game_status_img.get_height()
            endGame = True
            global unlocked
            if level == unlocked:
                unlocked += 1
                print("Level unlocked:", unlocked)

        # draw
        screen.fill('orange')
        for ball in balls:
            screen.blit(ball_img, (ball["x"], ball["y"]))
        if paddleSpriteCountdown == 0:
            screen.blit(paddle_img, (paddle_x, paddle_y))
        else:
            screen.blit(paddle_speed_img, (paddle_x, paddle_y))
        if multiplayer:
            if paddle2SpriteCountdown == 0:
                screen.blit(paddle_img, (paddle2_x, paddle2_y))
            else:
                screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
            p1_label = mini_font.render("Player 1", True, "black")
            p2_label = mini_font.render("Player 2", True, "black")
            screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
            screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
        for brick in range(len(bricks_x)):
            screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
        for powerup in powerups:
            powerup.draw(screen)
        if endGame:
            waiting = True
            while waiting:
                screen.fill('orange')
                screen.blit(game_status_img, (
                    SCREEN_WIDTH / 2 - msg_width / 2,
                    SCREEN_HEIGHT / 2 - msg_height/ 2
                ))

                info_text = font.render(f"Press {pygame.key.name(keybinds['return'])} to return to menu", True, "black")
                screen.blit(info_text, (
                    SCREEN_WIDTH / 2 - info_text.get_width() / 2,
                    SCREEN_HEIGHT / 2 + game_status_img.get_height()
                ))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == keybinds["return"]:
                        waiting = False

        pygame.display.flip() 
        fps_clock.tick(FPS)

# Endless mode code
def endless(players):
    screen.fill("orange")

    FPS = 30 # Frames Per Second
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # ball constants
    BALL_WIDTH = 16
    BALL_HEIGHT = 16

    # paddle constants
    PADDLE_WIDTH = 144
    PADDLE_HEIGHT = 32

    # brick constants
    BRICK_WIDTH = 96
    BRICK_HEIGHT = 32

    # powerup constants
    POWERUP_WIDTH = 32
    POWERUP_HEIGHT = 32

    # --- MULTI-BALL SUPPORT ---
    balls = [{
        "x": random.randint(0, SCREEN_WIDTH),
        "y": SCREEN_HEIGHT * 0.4,
        "speed_x": 6,
        "speed_y": 6,
        "original_speed_x": 6,
        "original_speed_y": 6,
        "prev_x": 0,
        "prev_y": 0
    }]
    balls[0]["prev_x"] = balls[0]["x"]
    balls[0]["prev_y"] = balls[0]["y"]

    if players == 1:
        multiplayer = False
    else:
        multiplayer = True

    # paddle defenitions
    paddle_x = SCREEN_WIDTH / 2
    paddle_y = SCREEN_HEIGHT * 0.9

    if multiplayer:
        paddle2_x = SCREEN_WIDTH / 2
        paddle2_y = SCREEN_HEIGHT * 0.75

    # brick definitions
    brick_speed = 0.1
    brick_loop = 30
    def bricksXGen():
        bricks_x = []
        xValue = 16
        for y in range(13):
            bricks_x.append(xValue)
            xValue += 96
        return bricks_x

    def bricksYGen():
        bricks_y = []
        yValue = 0
        for y in range(13):
            bricks_y.append(yValue)
        yValue += 42 
        return bricks_y

    bricks_x = bricksXGen()
    bricks_y = bricksYGen()

    powerups = []
    paddle_speed = 10  # standard paddle speed
    paddle2_speed = 10  # standard paddle speed

    # class for powerups
    class PowerUp:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 32, 32)
            self.speed = 4  # valsnelheid

        def update(self):
            self.rect.y += self.speed

        def draw(self, surface):
            surface.blit(powerup_img, (self.rect.x, self.rect.y))

    prev_paddle_x = paddle_x
    prev_paddle_y = paddle_y

    if multiplayer:
        prev_paddle2_x = paddle2_x
        prev_paddle2_y = paddle2_y

    paddleSpriteCountdown = 0
    paddle2SpriteCountdown = 0

    global highscore
    score = 0
    score_msg = font.render(f"Score: {score}", True, "cornsilk2")

    layers = 1  # aantal lagen bricks

    spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()   

    ball_img = pygame.Surface((64, 64), pygame.SRCALPHA)  
    ball_img.blit(spritesheet, (0, 0), (1403, 652, 64, 64))   
    ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

    paddle_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
    paddle_img.blit(spritesheet, (0, 0), (1158, 396, 243, 64))   
    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  

    paddle_speed_img = pygame.Surface((243, 64), pygame.SRCALPHA)  
    paddle_speed_img.blit(spritesheet, (0, 0), (349, 910, 243, 64))   
    paddle_speed_img = pygame.transform.scale(paddle_speed_img, (PADDLE_WIDTH, PADDLE_HEIGHT))  

    brick_img = pygame.Surface((384, 128), pygame.SRCALPHA)  
    brick_img.blit(spritesheet, (0, 0), (772, 390, 384, 128))   
    brick_img = pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) 

    powerup_img = pygame.Surface((64, 61), pygame.SRCALPHA)  
    powerup_img.blit(spritesheet, (0, 0), (772, 846, 64, 61))   
    powerup_img = pygame.transform.scale(powerup_img, (POWERUP_WIDTH, POWERUP_HEIGHT))

    endGame = False

    screen.fill('orange')
    for ball in balls:
        screen.blit(ball_img, (ball["x"], ball["y"]))
    if paddleSpriteCountdown == 0:
        screen.blit(paddle_img, (paddle_x, paddle_y))
    else:
        screen.blit(paddle_speed_img, (paddle_x, paddle_y))
    if multiplayer:
        if paddle2SpriteCountdown == 0:
            screen.blit(paddle_img, (paddle2_x, paddle2_y))
        else:
            screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
        p1_label = mini_font.render("Player 1", True, "black")
        p2_label = mini_font.render("Player 2", True, "black")
        screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
        screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
    for brick in range(len(bricks_x)):
        screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
    pygame.display.flip()

    for count in range(3, 0, -1):
        screen.fill('orange')
        for ball in balls:
            screen.blit(ball_img, (ball["x"], ball["y"]))
        if paddleSpriteCountdown == 0:
            screen.blit(paddle_img, (paddle_x, paddle_y))
        else:
            screen.blit(paddle_speed_img, (paddle_x, paddle_y))
        if multiplayer:
            if paddle2SpriteCountdown == 0:
                screen.blit(paddle_img, (paddle2_x, paddle2_y))
            else:
                screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
            p1_label = mini_font.render("Player 1", True, "black")
            p2_label = mini_font.render("Player 2", True, "black")
            screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
            screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
        for brick in range(len(bricks_x)):
            screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
        countdown_text = font.render(str(count), True, "gray")
        screen.blit(countdown_text, (
            SCREEN_WIDTH // 2 - countdown_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2
        ))
        pygame.display.flip()
        pygame.time.delay(1000)

    screen.fill('orange')
    for ball in balls:
        screen.blit(ball_img, (ball["x"], ball["y"]))
    if paddleSpriteCountdown == 0:
        screen.blit(paddle_img, (paddle_x, paddle_y))
    else:
        screen.blit(paddle_speed_img, (paddle_x, paddle_y))
    if multiplayer:
        if paddle2SpriteCountdown == 0:
            screen.blit(paddle_img, (paddle2_x, paddle2_y))
        else:
            screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
        p1_label = mini_font.render("Player 1", True, "black")
        p2_label = mini_font.render("Player 2", True, "black")
        screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
        screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
    for brick in range(len(bricks_x)):
        screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
    go_text = font.render("GO!", True, "gray")
    screen.blit(go_text, (
        SCREEN_WIDTH // 2 - go_text.get_width() // 2,
        SCREEN_HEIGHT // 2 - go_text.get_height() // 2
    ))
    pygame.display.flip()
    pygame.time.delay(500)

    while not endGame:
        toMainMenu = False

        # Store previous positions for all balls and paddle
        for ball in balls:
            ball["prev_x"] = ball["x"]
            ball["prev_y"] = ball["y"]
        prev_paddle_x = paddle_x
        prev_paddle_y = paddle_y

        if multiplayer:
            prev_paddle2_x = paddle2_x
            prev_paddle2_y = paddle2_y
        
        if paddleSpriteCountdown > 0:
            paddleSpriteCountdown -= 1

        if paddle2SpriteCountdown > 0:
            paddle2SpriteCountdown -= 1

        # game end input config and pause function
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN and event.key == keybinds["pause"]:
                paused = True
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == keybinds["return"]:
                            toMainMenu = True
                            break
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == keybinds["pause"]:
                            paused = False
                    if toMainMenu:
                        break
                    screen.fill("orange")
                    paused_msg = "Paused"
                    paused_img = font.render(paused_msg, True, "gray")
                    screen.blit(paused_img, (
                        SCREEN_WIDTH / 2 - paused_img.get_width() / 2,
                        SCREEN_HEIGHT / 2 - paused_img.get_height() / 2
                    ))
                    pygame.display.flip()
                    fps_clock.tick(FPS)
            if toMainMenu:
                break

        if toMainMenu:
            break

        if keys[keybinds["return"]]:
            if score > highscore:
                highscore = score
            break

        # paddle inputs
        if keys[keybinds["right"]]:
            paddle_x += paddle_speed
        if keys[keybinds["left"]]:
            paddle_x -= paddle_speed

        if multiplayer:
            if keys[keybinds["p2_right"]]:
                paddle2_x += paddle2_speed
            if keys[keybinds["p2_left"]]:
                paddle2_x -= paddle2_speed

        # move bricks
        brick_loop += brick_speed
        if brick_loop > 40:
            print ("new row of bricks")
            layers += 1
            brick_loop = 0
            xValue = 16
            for x in range(13):
                bricks_x.append(xValue)
                xValue += 96
            for x in range(13):
                bricks_y.append(-32)
        for brick in range(len(bricks_x)):
            bricks_y[brick] += brick_speed

        # paddle bounds
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
        
        if multiplayer:
            if paddle2_x < 0:
                paddle2_x = 0
            if paddle2_x + PADDLE_WIDTH > SCREEN_WIDTH:
                paddle2_x = SCREEN_WIDTH - PADDLE_WIDTH

        # collision detection for powerups
        paddle_rect = pygame.Rect(int(paddle_x), int(paddle_y), PADDLE_WIDTH, PADDLE_HEIGHT)
        if multiplayer:
            paddle2_rect = pygame.Rect(int(paddle2_x), int(paddle2_y), PADDLE_WIDTH, PADDLE_HEIGHT)
        for powerup in powerups[:]:
            powerup.update()
            if powerup.rect.colliderect(paddle_rect):
                effect = random.choice(["speed", "ball"])
                if effect == "speed":
                    print("Paddle speed boosted!")
                    paddle_speed *= 1.4
                    paddleSpriteCountdown = 40
                elif effect == "ball":
                    print("balls * 2")
                    # Voeg voor elke bal een extra bal toe met tegengestelde x-richting
                    new_balls = []
                    for ball in balls:
                        new_balls.append({
                            "x": ball["x"],
                            "y": ball["y"],
                            "speed_x": -ball["speed_x"],
                            "speed_y": ball["speed_y"],
                            "original_speed_x": -ball["original_speed_x"],
                            "original_speed_y": ball["original_speed_y"],
                            "prev_x": ball["x"],
                            "prev_y": ball["y"]
                        })
                    balls.extend(new_balls)
                powerups.remove(powerup)
            if multiplayer:
                if powerup.rect.colliderect(paddle2_rect):
                    effect = random.choice(["speed", "ball"])
                    if effect == "speed":
                        print("Paddle speed boosted!")
                        paddle2_speed *= 1.4
                        paddle2SpriteCountdown = 40
                    elif effect == "ball":
                        print("balls * 2")
                        # Voeg voor elke bal een extra bal toe met tegengestelde x-richting
                        new_balls = []
                        for ball in balls:
                            new_balls.append({
                                "x": ball["x"],
                                "y": ball["y"],
                                "speed_x": -ball["speed_x"],
                                "speed_y": ball["speed_y"],
                                "original_speed_x": -ball["original_speed_x"],
                                "original_speed_y": ball["original_speed_y"],
                                "prev_x": ball["x"],
                                "prev_y": ball["y"]
                            })
                        balls.extend(new_balls)
                    powerups.remove(powerup)
            if powerup.rect.y > SCREEN_HEIGHT:
                powerups.remove(powerup)

        # --- BALL LOGIC VOOR ALLE BALLEN ---
        for ball in balls[:]:  # copy to allow removal
            # move ball
            ball["x"] += ball["speed_x"]
            ball["y"] += ball["speed_y"]

            # bounce ball off screen borders
            if ball["x"] < 0:
                ball["speed_x"] = abs(ball["speed_x"])
                ball["original_speed_x"] = abs(ball["speed_x"])
            if ball["x"] + BALL_WIDTH > SCREEN_WIDTH:
                ball["speed_x"] = -abs(ball["speed_x"])
                ball["original_speed_x"] = -abs(ball["speed_x"])
            if ball["y"] < 0:
                ball["speed_y"] = abs(ball["speed_y"])
                ball["original_speed_y"] = abs(ball["speed_y"])

            # paddle collision
            ball_dx = ball["x"] - ball["prev_x"]
            ball_dy = ball["y"] - ball["prev_y"]
            paddle_dx = paddle_x - prev_paddle_x
            paddle_dy = paddle_y - prev_paddle_y

            rel_vx = ball_dx - paddle_dx
            rel_vy = ball_dy - paddle_dy

            entry_time, normal = swept_aabb(
                pygame.Rect(ball["prev_x"], ball["prev_y"], BALL_WIDTH, BALL_HEIGHT),
                rel_vx, rel_vy,
                pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
            )

            if entry_time < 1.0:
                ball["x"] = ball["prev_x"] + rel_vx * entry_time
                ball["y"] = ball["prev_y"] + rel_vy * entry_time

                if normal == (0, -1):  # van boven op paddle geraakt
                    incoming_angle = math.degrees(math.atan2(-ball["speed_y"], ball["speed_x"]))
                    reflected_angle = -incoming_angle
                    impact_offset = ((ball["x"] + BALL_WIDTH / 2) - (paddle_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
                    bounce_strength = 1.0 - abs(impact_offset) * -0.5
                    angle_deviation = (1 - bounce_strength) * 30 * (-1 if impact_offset < 0 else 1)
                    new_angle = reflected_angle + angle_deviation
                    speed = math.hypot(ball["speed_x"], ball["speed_y"])
                    rad = math.radians(new_angle)
                    ball["speed_x"] = speed * math.cos(rad)
                    ball["speed_y"] = -speed * math.sin(rad)
                elif normal == (-1, 0):
                    ball["speed_x"] = -abs(ball["speed_x"])
                elif normal == (1, 0):
                    ball["speed_x"] = abs(ball["speed_x"])
            
            if multiplayer:
                paddle_dx = paddle2_x - prev_paddle2_x
                paddle_dy = paddle2_y - prev_paddle2_y

                rel_vx = ball_dx - paddle_dx
                rel_vy = ball_dy - paddle_dy

                entry_time, normal = swept_aabb(
                    pygame.Rect(ball["prev_x"], ball["prev_y"], BALL_WIDTH, BALL_HEIGHT),
                    rel_vx, rel_vy,
                    pygame.Rect(paddle2_x, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
                )

                if entry_time < 1.0:
                    ball["x"] = ball["prev_x"] + rel_vx * entry_time
                    ball["y"] = ball["prev_y"] + rel_vy * entry_time

                    # Handle paddle2 collision
                    if normal == (0, -1):
                        incoming_angle = math.degrees(math.atan2(-ball["speed_y"], ball["speed_x"]))
                        reflected_angle = -incoming_angle
                        impact_offset = ((ball["x"] + BALL_WIDTH / 2) - (paddle2_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
                        bounce_strength = 1.0 - abs(impact_offset) * -0.5
                        angle_deviation = (1 - bounce_strength) * 30 * (-1 if impact_offset < 0 else 1)
                        new_angle = reflected_angle + angle_deviation
                        speed = math.hypot(ball["speed_x"], ball["speed_y"])
                        rad = math.radians(new_angle)
                        ball["speed_x"] = speed * math.cos(rad)
                        ball["speed_y"] = -speed * math.sin(rad)
                    elif normal == (0, 1):
                        incoming_angle = math.degrees(math.atan2(ball["speed_y"], ball["speed_x"]))
                        reflected_angle = -incoming_angle
                        impact_offset = ((ball["x"] + BALL_WIDTH / 2) - (paddle2_x + PADDLE_WIDTH / 2)) / (PADDLE_WIDTH / 2)
                        bounce_strength = -1.0 + abs(impact_offset) * 0.5
                        angle_deviation = (1 - bounce_strength) * 30 * (-1 if impact_offset < 0 else 1)
                        new_angle = reflected_angle + angle_deviation
                        speed = math.hypot(ball["speed_x"], ball["speed_y"])
                        rad = math.radians(new_angle)
                        ball["speed_x"] = speed * math.cos(rad)
                        ball["speed_y"] = -speed * math.sin(rad)
                    elif normal == (-1, 0):
                        ball["speed_x"] = -abs(ball["speed_x"])
                    elif normal == (1, 0):
                        ball["speed_x"] = abs(ball["speed_x"])

            # brick collisions
            for i in range(len(bricks_x)):
                brick_rect = pygame.Rect(bricks_x[i], bricks_y[i], BRICK_WIDTH, BRICK_HEIGHT)
                ball_dx = ball["x"] - ball["prev_x"]
                ball_dy = ball["y"] - ball["prev_y"]
                entry_time, normal = swept_aabb(
                    pygame.Rect(ball["prev_x"], ball["prev_y"], BALL_WIDTH, BALL_HEIGHT),
                    ball_dx, ball_dy,
                    brick_rect
                )
                if entry_time < 1.0:
                    ball["x"] = ball["prev_x"] + ball_dx * entry_time
                    ball["y"] = ball["prev_y"] + ball_dy * entry_time
                    if normal[0] != 0:
                        ball["speed_x"] *= -1
                        ball["original_speed_x"] *= -1
                    if normal[1] != 0:
                        ball["speed_y"] *= -1
                        ball["original_speed_y"] *= -1
                    ball["speed_x"] *= 1.04
                    ball["speed_y"] *= 1.04

                    # Spawn powerup with a 20% chance
                    powerupSpawnRng = random.randint(0, 4)
                    if powerupSpawnRng == 0:
                        print("powerup spawned")
                        powerups.append(PowerUp(bricks_x[i] + BRICK_WIDTH / 2 - POWERUP_HEIGHT / 2, bricks_y[i] + BRICK_HEIGHT / 2 - POWERUP_HEIGHT / 2))
                    score += math.ceil(layers ** 2 / 2)
                    score_msg = font.render(f"Score: {score}", True, "cornsilk2")

                    bricks_x.pop(i)
                    bricks_y.pop(i)
                    break

        # Remove balls that fall below the screen
        balls = [ball for ball in balls if ball["y"] < SCREEN_HEIGHT]

        if not balls:
            game_status_msg = "You Lost!"
            game_status_img = font.render(game_status_msg, True, "red")
            msg_width = game_status_img.get_width()
            msg_height = game_status_img.get_height()
            endGame = True

        if len(bricks_x) == 0:
            for ball in balls:
                ball["speed_x"] = 0
                ball["speed_y"] = 0
            game_status_msg = "You Won!"
            game_status_img = font.render(game_status_msg, True, "green")
            msg_width = game_status_img.get_width()
            msg_height = game_status_img.get_height()
            endGame = True

        # draw
        screen.fill('orange')
        for ball in balls:
            screen.blit(ball_img, (ball["x"], ball["y"]))
        if paddleSpriteCountdown == 0:
            screen.blit(paddle_img, (paddle_x, paddle_y))
        else:
            screen.blit(paddle_speed_img, (paddle_x, paddle_y))
        if multiplayer:
            if paddle2SpriteCountdown == 0:
                screen.blit(paddle_img, (paddle2_x, paddle2_y))
            else:
                screen.blit(paddle_speed_img, (paddle2_x, paddle2_y))
            p1_label = mini_font.render("Player 1", True, "black")
            p2_label = mini_font.render("Player 2", True, "black")
            screen.blit(p1_label, (paddle_x + 5, paddle_y - 20))
            screen.blit(p2_label, (paddle2_x + 5, paddle2_y - 20))
        for brick in range(len(bricks_x)):
            screen.blit(brick_img, (bricks_x[brick], bricks_y[brick])) 
        for powerup in powerups:
            powerup.draw(screen)
        screen.blit(score_msg, (10, 10))  # Score display
        if endGame:
            if score > highscore:
                highscore = score
            waiting = True
            while waiting:
                screen.fill('orange')
                screen.blit(game_status_img, (
                    SCREEN_WIDTH / 2 - msg_width / 2,
                    SCREEN_HEIGHT / 2 - msg_height/ 2
                ))

                info_text = font.render(f"Press {pygame.key.name(keybinds['return'])} to return to menu", True, "black")
                screen.blit(info_text, (
                    SCREEN_WIDTH / 2 - info_text.get_width() / 2,
                    SCREEN_HEIGHT / 2 + game_status_img.get_height()
                ))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == keybinds["return"]:
                        waiting = False

        pygame.display.flip() 
        fps_clock.tick(FPS)

# Game loop
choosePlatform()
gameMode = "choosePlayers"
running = True
print('mygame is running')
while running:
    if gameMode == "choosePlayers":
        gameMode = choosePlayers()
        if gameMode == "quit":
            running = False
    elif gameMode == "mainMenu":
        gameMode = mainMenu()
        if gameMode == "quit":
            running = False
    elif gameMode == "controlls":
        controlls()
        gameMode = "mainMenu"
    elif gameMode == "howToPlay":
        howToPlay()
        gameMode = "mainMenu"
    elif gameMode == "levels":
        level = levels()
        if level == "mainMenu":
            level = None
            gameMode = "mainMenu"
        else:
            gameMode = "normalPlay"
    elif gameMode == "normalPlay":
        normalPlay(level, players)
        gameMode = "mainMenu"
    elif gameMode == "endless":
        endless(players)
        gameMode = "mainMenu"

print('mygame stopt running')