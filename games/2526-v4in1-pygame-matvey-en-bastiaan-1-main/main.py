# BREAKOUT GAME
# Matvey en Bastiaan

import pygame, time, random, json, os
try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("You need to install CV2. Copy this in terminal: pip install opencv-python ")

# definitions
FPS = 30             # Frames Per Second
SCREEN_WIDTH = 1280  # screensize in x-direction in pixels
SCREEN_HEIGHT = 720  # screensize in y-direction in pixels
BALL_WIDTH = 16      # ballsize in x-direction in pixels
BALL_HEIGHT = 16     # ballsize in y-direction in pixels
PADDLE_BASE_WIDTH = 144   # paddlesize in x-direction in pixels
PADDLE_WIDTH = PADDLE_BASE_WIDTH
PADDLE_HEIGHT = 32   # paddlesize in y-direction in pixels
PADDLE_BASE_SPEED = 10 # initial paddle speed
PADDLE_MAX_SPEED = 20
PADDLE_SPEED_MIN = 4
BALL_SPEED_MIN = 4
BALL_SPEED_MAX = 12
BRICK_WIDTH = 80     # bricksize in x-direction in pixels
BRICK_HEIGHT = 32    # bricksize in y-direction in pixels

# Multi-ball support
balls_x = []         # list of x-positions of balls in pixels
balls_y = []         # list of y-positions of balls in pixels
balls_speed_x = []   # list of x-speeds of balls in pixels per frame
balls_speed_y = []   # list of y-speeds of balls in pixels per frame
balls_launched = []  # list of whether each ball has been launched from the paddle

# Ball variables
ball_x = 0           # x-position of ball in pixels
ball_speed_x = 10      # speed of ball in x-direction in pixels per frame
ball_y = 300         # y-position of ball in pixels
ball_speed_y = -15    # speed of ball in y-direction in pixels per frame
ball_launched = False # whether the ball has been launched from the paddle

#paddle variables
max_lives = 3
paddle_x = 640 
paddle_y = 600       # y-position of paddle in pixels
paddle_speed_x = PADDLE_BASE_SPEED  # speed of paddle in x-direction in pixels per frame

#brick variables
bricks_x = []
bricks_y = []
bricks_color = []  # color for each brick

# voor de animatie
flying_bricks_x = []
flying_bricks_y = []
flying_bricks_color = []

# powerups
powerups_x = []
powerups_y = []
powerups_color = []
paddle_timer = 0  # for the +50 paddle
lives = 1  # number of lives

# shooting bullets
BULLET_WIDTH = 4
BULLET_HEIGHT = 12
BULLET_SPEED = 15
bullets_x = []
bullets_y = []
bullets_speed_y = []
shoot_cooldown_p1 = 0
shoot_cooldown_p2 = 0

# Boss variables
boss_active = False
boss_x = 500
boss_y = 120
boss_width = 240
boss_height = 80
BOSS_BASE_SPEED = 6
boss_speed = BOSS_BASE_SPEED
boss_direction = 1
boss_vertical_direction = 1
boss_vertical_speed = 1
boss_next_action_time = 0
boss_last_hit_cooldown = 0
boss_shake_timer = 0
boss_shake_magnitude = 4
boss_hp = 20
boss_max_hp = 20
boss_rocket_drop_time = 0

row_colors = ["blue", "lightgreen", "purple", "red", "orange", "lightblue", "yellow", "green", "grey", "brown"]


game_state = "INTRO"  # can be: INTRO, START, PLAYING, GAME_OVER, LEVEL_START, OUTRO
game_status_msg = ""
blocks_broken = 0
score_msg = ""

# timer variables for speedrun
timer_started = False
timer_start_ticks = 0
timer_end_ticks = 0
record_ticks = 180000
RECORD_FILE = 'record.json'
INTRO_FILE = 'intro.mp4'  # mp4 video file for the intro
OUTRO_FILE = 'outro.mp4'  # mp4 video file for the outro

# level message variables
level_message_timer = 0
level_message_alpha = 255
transition_timer = 0

player_mode = 1  # 1 or 2 players
start_options = ["1 Player", "2 Players"]
start_selected_index = 0
start_nav_key_pressed = False
start_confirm_key_pressed = False

player2_paddle_x = 640
player2_paddle_y = paddle_y

# Video variables
intro_video = None
intro_frame_count = 0
intro_total_frames = 0
intro_fps = 30

outro_video = None
outro_frame_count = 0
outro_total_frames = 0
outro_fps = 30

#
# levels
#
level_1 = [
    "0000101010100000", 
    "0000010101010000"
]

level_2 = [
    "1111111111111111",
    "1111111111111111",
    "1111111111111111"
]

level_3 = [
    "0000011000110000",
    "0000111101111000",
    "0001111111111100",
    "0011111111111110",
    "0011111111111110",
    "0001111111111100",
    "0000111111111000",
    "0000011111110000",
    "0000001111100000",
    "0000000111000000"
]

level_4 = [
    "1111111111111111",
    "1000100010001000",
    "1000100010001000",
    "1010101010101010",
    "1000100010001000",
    "1000100010001000",
    "1111111111111111"
]

level_5 = [
    "1111111111111111",
    "1010101010101010",
    "0101010101010101",
    "1010101010101010",
    "0101010101010101",
    "1111111111111111"
]

level_6 = [
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111",
    "1111111111111111"
]

level_7 = [
    "0"
]






current_level = 0

# test mode

# level_1 = ["1"]
# level_2 = ["1"]
# level_3 = ["1"]
# level_4 = ["1"]
# level_5 = ["1"]
# level_6 = ["1"]

# current_level = 6

all_levels = [level_1, level_2, level_3, level_4, level_5, level_6, level_7]

# Define custom color schemes for each level
level_colors = {
    0: ["lightgreen"] * 2,                                                      # level 1
    1: ["blue"] * 3,                                                            # level 2
    2: ["red"] * 10,                                                            # level 3
    3: ["red", "orange", "green", "lightgreen", "green", "orange", "red"],      # level 4
    4: ["purple", "blue", "purple", "blue", "purple", "blue"],                  # level 5
    5: ["orange"] * 10                                                          # level 6
}

def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    tenths = (milliseconds % 1000) // 10
    return str(minutes) + ":" + str(seconds).zfill(2) + "." + str(tenths).zfill(2)


def load_record():
    global record_ticks
    try:
        with open(RECORD_FILE, 'r') as record:
            data = json.load(record)
        record_ticks = int(data.get('record_ticks', record_ticks))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        record_ticks = 180000


def save_record():
    try:
        with open(RECORD_FILE, 'w') as record:
            json.dump({'record_ticks': record_ticks}, record)
    except OSError:
        pass


def play_video(filename, screen, video_type):
    """Play an MP4 video file (intro or outro). Returns True when finished.
    video_type: 'intro' or 'outro'
    """
    global intro_video, intro_frame_count, intro_total_frames, intro_fps
    global outro_video, outro_frame_count, outro_total_frames, outro_fps
    
    if not HAS_CV2:
        return True
    
    if video_type == 'intro':
        if intro_video is None:
            try:
                intro_video = cv2.VideoCapture(filename)
                if not intro_video.isOpened():
                    print("Could not open video file: " + str(filename))
                    return True
                intro_total_frames = int(intro_video.get(cv2.CAP_PROP_FRAME_COUNT))
                intro_fps = int(intro_video.get(cv2.CAP_PROP_FPS)) or 30
                intro_frame_count = 0
            except Exception as e:
                print("Error opening video: " + str(e))
                return True
        
        ret, frame = intro_video.read()
        if not ret or intro_frame_count >= intro_total_frames:
            if intro_video:
                intro_video.release()
                intro_video = None
            intro_frame_count = 0
            intro_total_frames = 0
            return True
        
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.fromstring(frame.tobytes(), (SCREEN_WIDTH, SCREEN_HEIGHT), "RGB")
        screen.blit(frame_surface, (0, 0))
        intro_frame_count += 1
    
    else:  # outro
        if outro_video is None:
            try:
                outro_video = cv2.VideoCapture(filename)
                if not outro_video.isOpened():
                    print("Could not open video file: " + str(filename))
                    return True
                outro_total_frames = int(outro_video.get(cv2.CAP_PROP_FRAME_COUNT))
                outro_fps = int(outro_video.get(cv2.CAP_PROP_FPS)) or 30
                outro_frame_count = 0
            except Exception as e:
                print("Error opening video: " + str(e))
                return True
        
        ret, frame = outro_video.read()
        if not ret or outro_frame_count >= outro_total_frames:
            if outro_video:
                outro_video.release()
                outro_video = None
            outro_frame_count = 0
            outro_total_frames = 0
            return True
        
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.fromstring(frame.tobytes(), (SCREEN_WIDTH, SCREEN_HEIGHT), "RGB")
        screen.blit(frame_surface, (0, 0))
        outro_frame_count += 1
    
    return False



def load_level(level_map, level_index): # level_map can be level_1, 2 etc
    new_bricks_x = []
    new_bricks_y = []
    new_bricks_color = []

    start_x = 0     # coords left upper corner
    start_y = 100

    # Get custom colors for this level, or fall back to row_colors
    colors_for_level = level_colors.get(level_index, row_colors)

    for row_index in range(len(level_map)):  # for each row
        row_string = level_map[row_index]    # get the data for that row: "111111"
        for col_index in range(len(row_string)):  # for each collumn
            character = row_string[col_index]     # get the caracter for that collumn: "1"
            if character == "1":
                brick_x = start_x + (col_index * 80)
                brick_y = start_y + (row_index * 32)

                new_bricks_x.append(brick_x)
                new_bricks_y.append(brick_y)
                # Use custom color scheme for the level
                new_bricks_color.append(colors_for_level[row_index])

    return new_bricks_x, new_bricks_y, new_bricks_color

# selecting powerups for the level 
def get_powerup_colors_for_level(level_index):
    colors_for_level = level_colors.get(level_index, row_colors)
    available = colors_for_level[:len(all_levels[level_index])]
    return [color for color in available if color in powerup_types]


def get_paddle_speed_for_level(level_index):
    return min(paddle_speed_setting + level_index, PADDLE_MAX_SPEED)


def reset_game():
    global current_level, blocks_broken, lives, player_mode, start_selected_index, menu_selected_index, menu_page
    global bricks_x, bricks_y, bricks_color
    global balls_x, balls_y, balls_speed_x, balls_speed_y, balls_launched
    global paddle_x, player2_paddle_x, paddle_speed_x
    global flying_bricks_x, flying_bricks_y, flying_bricks_color
    global powerups_x, powerups_y, powerups_color
    global bullets_x, bullets_y, bullets_speed_y, shoot_cooldown_p1, shoot_cooldown_p2
    global level_message_timer, level_message_alpha, game_state, transition_timer
    global cheat_states, paddle_cheat, cheats_used
    global boss_active, boss_hp, boss_speed, boss_direction, boss_vertical_direction, boss_vertical_speed, boss_next_action_time, boss_last_hit_cooldown, boss_rocket_drop_time
    global timer_started, timer_start_ticks, timer_end_ticks

    current_level = 0
    blocks_broken = 0
    lives = 1
    player_mode = 1
    start_selected_index = 0
    menu_page = "MAIN"
    menu_selected_index = 0
    menu_key_pressed = False
    menu_nav_key_pressed = False
    menu_confirm_key_pressed = False
    menu_return_state = "START"
    cheat_states = [False, False, False, False, False]
    cheats_used = False
    paddle_cheat = 0

    bricks_x, bricks_y, bricks_color = load_level(all_levels[current_level], current_level)

    paddle_x = 640
    player2_paddle_x = 640
    paddle_speed_x = get_paddle_speed_for_level(current_level)

    balls_x = [paddle_x + (PADDLE_WIDTH - BALL_WIDTH) // 2]
    balls_y = [paddle_y - BALL_HEIGHT]
    balls_speed_x = [0]
    balls_speed_y = [0]
    balls_launched = [False]

    flying_bricks_x.clear()
    flying_bricks_y.clear()
    flying_bricks_color.clear()
    powerups_x.clear()
    powerups_y.clear()
    powerups_color.clear()
    bullets_x.clear()
    bullets_y.clear()
    bullets_speed_y.clear()
    shoot_cooldown_p1 = 0
    shoot_cooldown_p2 = 0

    level_message_timer = pygame.time.get_ticks() + 2000
    level_message_alpha = 255
    timer_started = False
    timer_start_ticks = 0
    timer_end_ticks = 0
    game_state = "START"


def reset_settings():
    global paddle_speed_setting, ball_speed_setting, cheat_states, paddle_speed_x

    paddle_speed_setting = PADDLE_BASE_SPEED
    ball_speed_setting = 6
    cheat_states = [False, False, False, False, False]
    paddle_speed_x = get_paddle_speed_for_level(current_level)


def check_level_clear():
    global current_level, bricks_x, bricks_y, bricks_color
    global paddle_x, player2_paddle_x, paddle_speed_x
    global flying_bricks_x, flying_bricks_y, flying_bricks_color
    global powerups_x, powerups_y, powerups_color
    global bullets_x, bullets_y, bullets_speed_y
    global shoot_cooldown_p1, shoot_cooldown_p2
    global balls_x, balls_y, balls_speed_x, balls_speed_y, balls_launched
    global level_message_timer, level_message_alpha, game_state, transition_timer
    global score_msg, game_status_msg, blocks_broken
    global boss_active, boss_hp

    if len(bricks_x) != 0:
        return False

    if current_level + 1 < len(all_levels):
        # start a short transition with flying colored bricks (3-5 seconds)
        current_time = pygame.time.get_ticks()
        transition_ms = random.randint(3000, 5000)
        transition_timer = current_time + transition_ms

        flying_bricks_x.clear()
        flying_bricks_y.clear()
        flying_bricks_color.clear()

        # spawn a bunch of flying bricks below the screen that will move up
        colors_pool = level_colors.get(current_level, row_colors)
        for _ in range(40):
            fx = random.randint(-BRICK_WIDTH, SCREEN_WIDTH)
            fy = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 400)
            fcolor = random.choice(colors_pool)
            flying_bricks_x.append(fx)
            flying_bricks_y.append(fy)
            flying_bricks_color.append(fcolor)

        game_state = "LEVEL_TRANSITION"
        return True
    else:
        for b_idx in range(len(balls_speed_x)):
            balls_speed_x[b_idx] = 0
            balls_speed_y[b_idx] = 0
        score_msg = "Score: " + str(blocks_broken)
        game_status_msg = "You beat the whole game!"
        game_state = "GAME_OVER"
        return True


# Function to spawn a new ball
def spawn_new_ball(x, y, speed_x_ref, speed_y_ref):
    """Spawn a new ball with a slight variation in trajectory"""
    new_speed_x = speed_x_ref * random.uniform(0.8, 1.2)
    new_speed_y = speed_y_ref
    balls_x.append(x)
    balls_y.append(y)
    balls_speed_x.append(new_speed_x)
    balls_speed_y.append(new_speed_y)
    balls_launched.append(True)


# loading first level(before game loop)
load_record()
bricks_x, bricks_y, bricks_color = load_level(all_levels[current_level], current_level) 

# position ball on paddle
ball_x = paddle_x + (PADDLE_WIDTH - BALL_WIDTH) // 2
ball_y = paddle_y - BALL_HEIGHT
ball_launched = False 

# Initialize first ball in the list
balls_x = [ball_x]
balls_y = [ball_y]
balls_speed_x = [0]
balls_speed_y = [0]
balls_launched = [False]

#
# init game
#

pygame.init()
font = pygame.font.Font('PressStart2P-Regular.ttf', 24)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
fps_clock = pygame.time.Clock()

#
# read images
#

spritesheet = pygame.image.load('Breakout_Tile_Free.png').convert_alpha()
background_img = pygame.image.load('background.jpg').convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

ball_powerup_img = pygame.image.load('Breakout_ball_powerup.png').convert_alpha()
ball_powerup_img = pygame.transform.scale(ball_powerup_img, (32, 32))

rocket_img = pygame.image.load('raket.png').convert_alpha()
rocket_img = pygame.transform.scale(rocket_img, (32, 32))
rocket_img = pygame.transform.flip(rocket_img, False, True)

boss_img = pygame.image.load('Brick_boss.png').convert_alpha()
boss_img = pygame.transform.scale(boss_img, (boss_width, boss_height)).convert_alpha()
boss_img.set_colorkey((255, 255, 255))


def get_sprite(x, y, w, h, scale_w=None, scale_h=None):
    img = pygame.Surface((w, h), pygame.SRCALPHA)
    img.blit(spritesheet, (0, 0), (x, y, w, h))

    if scale_w is not None and scale_h is not None:
        return pygame.transform.scale(img, (scale_w, scale_h))
    return img


ball_img = get_sprite(1403, 652, 64, 64, BALL_WIDTH, BALL_HEIGHT)

paddle_img = get_sprite(1158, 396, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)

paddle_powerup_img = get_sprite(1403, 66, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)

brick_types = {
    "blue": get_sprite(772, 390, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "blue_cracked": get_sprite(0, 0, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "lightgreen": get_sprite(0, 130, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "lightgreen_cracked": get_sprite(0, 260, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "purple": get_sprite(0, 390, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "purple_cracked": get_sprite(0, 520, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "red": get_sprite(772, 260, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "red_cracked": get_sprite(772, 130, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "orange": get_sprite(772, 0, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "orange_cracked": get_sprite(772, 650, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "lightblue": get_sprite(386, 650, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "lightblue_cracked": get_sprite(386, 520, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "yellow": get_sprite(386, 390, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "yellow_cracked": get_sprite(386, 260, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "green": get_sprite(386, 130, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "green_cracked": get_sprite(386, 0, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "grey": get_sprite(772, 520, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "grey_cracked": get_sprite(0, 650, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),

    "brown": get_sprite(386, 780, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
    "brown_cracked": get_sprite(0, 780, 384, 128, BRICK_WIDTH, BRICK_HEIGHT),
}

powerup_types = {
    "red": get_sprite(1403, 392, 128, 128, 32, 32),
    "orange": get_sprite(1403, 522, 128, 128, 32, 32),
    "green": get_sprite(1533, 262, 128, 128, 32, 32),
    "blue": get_sprite(1533, 392, 128, 128, 32, 32),
    "purple": get_sprite(1403, 262, 128, 128, 32, 32),
    "yellow": get_sprite(1507, 652, 128, 128, 32, 32),
    "lightgreen": get_sprite(1403, 132, 128, 128, 32, 32),
    "lightblue": get_sprite(1533, 132, 128, 128, 32, 32),
    "brown": get_sprite(1533, 392, 128, 128, 32, 32),
    "grey": get_sprite(1574, 782, 128, 128, 32, 32),
    "life": get_sprite(1637, 652, 64, 58, 32, 32),
    "ball": ball_powerup_img,
    "rocket": rocket_img
}

# small life/heart image to show lives as icons
life_img = powerup_types.get("life")

#
# debug mode 
#

dev_mode = False
dev_mode_key_pressed = False
skip_key_pressed = False
level_skip = 0
paddle_cheat = 0
cheat_options = ["Wide paddle", "Ultra wide paddle", "Unlimited lives", "Extra balls", "Shoot powerup"]
main_menu_options = ["Settings", "Cheats", "Reset game"]
cheats_menu_options = cheat_options + ["Terug"]
menu_page = "MAIN"
paddle_speed_setting = PADDLE_BASE_SPEED
ball_speed_setting = 6
cheat_states = [False, False, False, False, False]
cheats_used = False
menu_return_state = "START"
menu_key_pressed = False
menu_nav_key_pressed = False
menu_confirm_key_pressed = False
menu_selected_index = 0

def draw_dev_info(surface, x, y):
    # Draw debug information on the screen
    small_font = pygame.font.Font('PressStart2P-Regular.ttf', 16)
    if timer_started:
        if timer_end_ticks > 0:
            timer_text = format_time(timer_end_ticks - timer_start_ticks)
        else:
            timer_text = format_time(pygame.time.get_ticks() - timer_start_ticks)
    else:
        timer_text = "OFF"
    debug_lines = [
        "BALL_X: " + str(round(balls_x[0], 1)) if balls_x else "BALL_X: N/A",
        "BALL_Y: " + str(round(balls_y[0], 1)) if balls_y else "BALL_Y: N/A",
        "BALL_SPD_X: " + str(round(balls_speed_x[0], 2)) if balls_speed_x else "BALL_SPD_X: N/A",
        "BALL_SPD_Y: " + str(round(balls_speed_y[0], 2)) if balls_speed_y else "BALL_SPD_Y: N/A",
        "PADDLE_X: " + str(round(paddle_x, 1)),
        "PADDLE_Y: " + str(round(paddle_y, 1)),
        "BRICKS: " + str(len(bricks_x)),
        "POWERUPS: " + str(len(powerups_x)),
        "BALLS: " + str(len(balls_x)),
        "LEVEL: " + str(current_level + 1),
        "SCORE: " + str(blocks_broken),
        "TIMER: " + timer_text,
    ]
    
    for line_index in range(len(debug_lines)):
        line = debug_lines[line_index]
        debug_text = small_font.render(line, True, (0, 255, 0))
        surface.blit(debug_text, (x, y + line_index * 22))


#
# game loop
#

print('mygame is running')
running = True
while running:
    #
    # read events
    #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # Toggle the menu screen on/off with M
    if keys[pygame.K_m]:
        if not menu_key_pressed:
            if game_state != "MENU_SCREEN":
                menu_return_state = game_state
                game_state = "MENU_SCREEN"
            else:
                game_state = menu_return_state
            menu_key_pressed = True
    else:
        menu_key_pressed = False

    # Apply paddle width cheats
    if cheat_states[1]:
        if PADDLE_WIDTH != SCREEN_WIDTH:
            PADDLE_WIDTH = SCREEN_WIDTH
            paddle_img = get_sprite(1158, 396, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
            paddle_powerup_img = get_sprite(1403, 66, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
    elif cheat_states[0]:
        if PADDLE_WIDTH != PADDLE_BASE_WIDTH * 3:
            PADDLE_WIDTH = PADDLE_BASE_WIDTH * 3
            paddle_img = get_sprite(1158, 396, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
            paddle_powerup_img = get_sprite(1403, 66, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
    else:
        if PADDLE_WIDTH != PADDLE_BASE_WIDTH:
            PADDLE_WIDTH = PADDLE_BASE_WIDTH
            paddle_img = get_sprite(1158, 396, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
            paddle_powerup_img = get_sprite(1403, 66, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)

    if game_state == "INTRO":
        # Show intro video
        intro_finished = play_video(INTRO_FILE, screen, 'intro')
        
        # Allow skipping intro with SPACE or ESC
        if intro_finished or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            game_state = "START"
            if intro_video:
                intro_video.release()
            intro_video = None
        
        pygame.display.flip()
    
    elif game_state == "START":
        screen.fill('black')

        title_text = font.render("BREAKOUT", True, 'yellow')
        select_text = font.render("Kies speler mode", True, 'white')
        controls_text = font.render(
            "P1: A/D, P2: J/L", True, 'gray')
        select_help_text = font.render(
            "Gebruik W/S om te selecteren", True, 'gray')
        confirm_text = font.render(
            "Druk op A/D om te starten", True, 'gray')

        screen.blit(title_text, (100, 180))
        screen.blit(select_text, (100, 280))
        screen.blit(controls_text, (100, 520))
        screen.blit(select_help_text, (100, 560))
        screen.blit(confirm_text, (100, 600))

        option_y = 360
        option_index = 0
        while option_index < len(start_options):
            option = start_options[option_index]
            selected = option_index == start_selected_index
            option_color = 'yellow' if selected else 'white'
            option_surface = font.render(option, True, option_color)
            if selected:
                text_width = option_surface.get_width()
                pygame.draw.rect(screen, (60, 60, 100), (80, option_y - 12, text_width + 80, 60))
            screen.blit(option_surface, (100, option_y))
            option_y += 60
            option_index += 1

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if not start_nav_key_pressed:
                start_selected_index = max(0, start_selected_index - 1)
                start_nav_key_pressed = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if not start_nav_key_pressed:
                start_selected_index = min(len(start_options) - 1, start_selected_index + 1)
                start_nav_key_pressed = True
        else:
            start_nav_key_pressed = False

        if keys[pygame.K_a] or keys[pygame.K_d]:
            if not start_confirm_key_pressed:
                player_mode = 1 if start_selected_index == 0 else 2
                level_message_timer = pygame.time.get_ticks() + 2000  # 2 seconds
                level_message_alpha = 255
                game_state = "LEVEL_START"
                start_confirm_key_pressed = True
        else:
            start_confirm_key_pressed = False
    elif game_state == "MENU_SCREEN":
        screen.fill((10, 10, 30))

        if menu_page == "MAIN":
            page_title = "MENU"
        elif menu_page == "RESET_CONFIRM":
            page_title = "Confirm"
        else:
            page_title = menu_page
        menu_title = font.render(page_title, True, 'yellow')
        screen.blit(menu_title, (100, 140))

        if menu_page == "MAIN":
            cheat_status = font.render(
                "Cheats enabled: " + ("YES" if any(cheat_states) else "NO"), True, 'white')
            return_text = font.render("Druk op M om terug te keren", True, 'gray')
            help_text = font.render("Gebruik W/S om te selecteren, A/D om te bevestigen", True, 'gray')

            screen.blit(cheat_status, (100, 220))
            screen.blit(return_text, (100, 620))
            screen.blit(help_text, (100, 660))
            options = main_menu_options
        elif menu_page == "CHEATS":
            options = cheats_menu_options
        elif menu_page == "SETTINGS":
            options = [
                "Paddle speed: " + str(paddle_speed_setting),
                "Ball speed: " + str(ball_speed_setting),
                "Reset settings",
                "Terug"
            ]
        elif menu_page == "RESET_CONFIRM":
            options = []
            popup_lines = [
                "Are you sure you want to reset the game?",
                "Press A to continue, D to cancel."
            ]
        else:
            options = []
            popup_lines = []

        option_index = 0
        while option_index < len(options):
            option = options[option_index]
            if menu_page == "CHEATS" and option_index < len(cheat_options):
                option_text = option + ": " + ("ON" if cheat_states[option_index] else "OFF")
            else:
                option_text = option
            text_color = 'yellow' if option_index == menu_selected_index else 'white'
            background_color = (60, 60, 100) if option_index == menu_selected_index else None
            y = 280 + option_index * 60
            option_surface = font.render(option_text, True, text_color)
            if background_color is not None:
                text_width = option_surface.get_width()
                rect_width = text_width + 40
                pygame.draw.rect(screen, background_color, (80, y - 15, rect_width, 50))
            screen.blit(option_surface, (100, y))
            option_index += 1

        if menu_page.startswith("RESET_"):
            popup_y = 280
            for line in popup_lines:
                popup_surface = font.render(line, True, 'white')
                screen.blit(popup_surface, (100, popup_y))
                popup_y += 60

        # menu navigation via W and S
        if menu_page != "RESET_CONFIRM":
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if not menu_nav_key_pressed:
                    menu_selected_index = max(0, menu_selected_index - 1)
                    menu_nav_key_pressed = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if not menu_nav_key_pressed:
                    menu_selected_index = min(len(options) - 1, menu_selected_index + 1)
                    menu_nav_key_pressed = True
            else:
                menu_nav_key_pressed = False
        else:
            menu_nav_key_pressed = False

        if keys[pygame.K_a] or keys[pygame.K_d]:
            if not menu_confirm_key_pressed:
                if menu_page == "MAIN":
                    if menu_selected_index == 0:
                        menu_page = "SETTINGS"
                        menu_selected_index = 0
                    elif menu_selected_index == 1:
                        menu_page = "CHEATS"
                        menu_selected_index = 0
                    else:
                        menu_page = "RESET_CONFIRM"
                elif menu_page == "CHEATS":
                    if menu_selected_index < len(cheat_options):
                        was_enabled = cheat_states[menu_selected_index]
                        cheat_states[menu_selected_index] = not cheat_states[menu_selected_index]
                        if cheat_states[menu_selected_index] and not was_enabled:
                            cheats_used = True
                        if menu_selected_index == 1 and cheat_states[1]:
                            cheat_states[0] = False
                        elif menu_selected_index == 0 and cheat_states[0]:
                            cheat_states[1] = False
                    else:
                        menu_page = "MAIN"
                        menu_selected_index = 0
                elif menu_page == "SETTINGS":
                    if menu_selected_index == 0:
                        if keys[pygame.K_a]:
                            paddle_speed_setting = max(PADDLE_SPEED_MIN, paddle_speed_setting - 1)
                        elif keys[pygame.K_d]:
                            paddle_speed_setting = min(PADDLE_MAX_SPEED, paddle_speed_setting + 1)
                        paddle_speed_x = get_paddle_speed_for_level(current_level)
                    elif menu_selected_index == 1:
                        if keys[pygame.K_a]:
                            ball_speed_setting = max(BALL_SPEED_MIN, ball_speed_setting - 1)
                        elif keys[pygame.K_d]:
                            ball_speed_setting = min(BALL_SPEED_MAX, ball_speed_setting + 1)
                    elif menu_selected_index == 2:
                        reset_settings()
                    else:
                        menu_page = "MAIN"
                        menu_selected_index = 0
                elif menu_page == "RESET_CONFIRM":
                    if keys[pygame.K_a]:
                        reset_game()
                    else:
                        menu_page = "MAIN"
                        menu_selected_index = 0
                else:
                    menu_page = "MAIN"
                    menu_selected_index = 0
                menu_confirm_key_pressed = True   
        else:
            menu_confirm_key_pressed = False
    elif game_state == "LEVEL_TRANSITION":
        current_time = pygame.time.get_ticks()
        time_left = max(0, transition_timer - current_time)
        total_duration = 4000  # approximate max

        # Dark overlay that fades in over the last 500ms
        screen.blit(background_img, (0, 0))

        # Move flying bricks upward with wobble
        for i in range(len(flying_bricks_y) - 1, -1, -1):
            flying_bricks_y[i] -= 10
            flying_bricks_x[i] += random.randint(-2, 2)
            if flying_bricks_y[i] < -BRICK_HEIGHT - 50:
                flying_bricks_x.pop(i)
                flying_bricks_y.pop(i)
                flying_bricks_color.pop(i)

        # Draw flying bricks
        for i in range(len(flying_bricks_x)):
            color_name = flying_bricks_color[i]
            screen.blit(brick_types[color_name], (flying_bricks_x[i], flying_bricks_y[i]))

        # Draw paddle so player can see it
        screen.blit(paddle_img, (paddle_x, paddle_y))
        if player_mode == 2:
            screen.blit(paddle_img, (player2_paddle_x, player2_paddle_y))

        # Pulsing "LEVEL CLEAR!" text
        pulse = abs((current_time % 600) - 300) / 300  # 0.0 to 1.0
        r = int(200 + 55 * pulse)
        g = int(200 + 55 * pulse)
        b = 0
        clear_text = font.render("LEVEL CLEAR!", True, (r, g, b))
        clear_rect = clear_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(clear_text, clear_rect)

        # Countdown bar at the bottom
        bar_width = int((time_left / total_duration) * (SCREEN_WIDTH - 100))
        bar_width = max(0, min(bar_width, SCREEN_WIDTH - 100))
        pygame.draw.rect(screen, (60, 60, 60), (50, SCREEN_HEIGHT - 40, SCREEN_WIDTH - 100, 16))
        pygame.draw.rect(screen, (100, 220, 100), (50, SCREEN_HEIGHT - 40, bar_width, 16))

        next_level_num = current_level + 2  # +1 for 0-index, +1 for next
        next_text = font.render("Next: Level " + str(next_level_num), True, (180, 180, 180))
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(next_text, next_rect)

        # Score so far
        score_text = font.render("Score: " + str(blocks_broken), True, 'white')
        screen.blit(score_text, (20, 20))

        # Transition ends
        if current_time >= transition_timer:
            current_level += 1
            boss_active = current_level == 6
            if boss_active:
                boss_hp = boss_max_hp
                boss_speed = BOSS_BASE_SPEED
                boss_direction = 1
                boss_vertical_direction = 1
                boss_vertical_speed = 1
                boss_next_action_time = pygame.time.get_ticks() + random.randint(700, 2200)
                boss_last_hit_cooldown = 0
                boss_rocket_drop_time = pygame.time.get_ticks() + random.randint(3500, 4500)
                boss_x = (SCREEN_WIDTH - boss_width) // 2
                boss_y = 120

            bricks_x, bricks_y, bricks_color = load_level(all_levels[current_level], current_level)

            balls_x[0] = paddle_x + (PADDLE_WIDTH - BALL_WIDTH) // 2
            balls_y[0] = paddle_y - BALL_HEIGHT
            balls_launched[0] = False
            balls_speed_x[0] = 0
            balls_speed_y[0] = 0
            paddle_x = 640
            player2_paddle_x = 640
            paddle_speed_x = get_paddle_speed_for_level(current_level)

            flying_bricks_x.clear()
            flying_bricks_y.clear()
            flying_bricks_color.clear()
            powerups_x.clear()
            powerups_y.clear()
            powerups_color.clear()
            bullets_x.clear()
            bullets_y.clear()
            bullets_speed_y.clear()
            shoot_cooldown_p1 = 0
            shoot_cooldown_p2 = 0

            while len(balls_x) > 1:
                balls_x.pop()
                balls_y.pop()
                balls_speed_x.pop()
                balls_speed_y.pop()
                balls_launched.pop()

            level_message_timer = pygame.time.get_ticks() + 2000
            level_message_alpha = 255
            game_state = "LEVEL_START"
    elif game_state == "LEVEL_START":
        # Update fade effect
        current_time = pygame.time.get_ticks()
        if current_time >= level_message_timer:
            game_state = "PLAYING"
        else:
            # calculate alpha based on remaining time
            time_left = level_message_timer - current_time
            if time_left < 500:  # Last 0.5 seconds
                level_message_alpha = int((time_left / 500) * 255)

        # Draw the current level scene behind the message
        screen.blit(background_img, (0, 0))
        
        # Draw all balls
        for i in range(len(balls_x)):
            screen.blit(ball_img, (balls_x[i], balls_y[i]))
        
        if pygame.time.get_ticks() < paddle_timer:
            screen.blit(paddle_powerup_img, (paddle_x, paddle_y))
        else:
            screen.blit(paddle_img, (paddle_x, paddle_y))

        if player_mode == 2:
            screen.blit(paddle_img, (player2_paddle_x, player2_paddle_y))

        for i in range(len(bricks_x)):
            color_name = bricks_color[i]
            current_brick_img = brick_types[color_name]
            screen.blit(current_brick_img, (bricks_x[i], bricks_y[i]))
        for i in range(len(flying_bricks_x)):
            color_name = flying_bricks_color[i]
            current_brick_img = brick_types[color_name]
            screen.blit(current_brick_img,
                        (flying_bricks_x[i], flying_bricks_y[i]))
        for i in range(len(powerups_x)):
            color_name = powerups_color[i]
            current_powerup_img = powerup_types[color_name]
            screen.blit(current_powerup_img, (powerups_x[i], powerups_y[i]))

        # Render level message (show "Final Level" for last level)
        if current_level == len(all_levels) - 1:
            level_label = "Final Level"
        else:
            level_label = "LEVEL " + str(current_level + 1)
        level_text = font.render(level_label, True, (255, 255, 255))
        level_text.set_alpha(level_message_alpha)

        # Center the text
        text_rect = level_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(level_text, text_rect)

        # skip level with skip
        if keys[pygame.K_s]:
            level_skip = 1
        if keys[pygame.K_k] and level_skip == 1:
            level_skip = 2
        if keys[pygame.K_i] and level_skip == 2:
            level_skip = 3
        if keys[pygame.K_p] and level_skip == 3:
            level_skip = 4
        if level_skip == 4:
            cheats_used = True
            if not skip_key_pressed:
                if current_level + 1 < len(all_levels):
                    # Move to the next level
                    current_level += 1

                    # Load the new level
                    bricks_x, bricks_y, bricks_color = load_level(
                        all_levels[current_level], current_level)

                    # Handle boss initialization on final level
                    boss_active = current_level == 6
                    if boss_active:
                        boss_hp = boss_max_hp
                        boss_speed = BOSS_BASE_SPEED
                        boss_direction = 1
                        boss_vertical_direction = 1
                        boss_vertical_speed = 1
                        boss_next_action_time = pygame.time.get_ticks() + random.randint(700, 2200)
                        boss_last_hit_cooldown = 0
                        boss_rocket_drop_time = pygame.time.get_ticks() + random.randint(3500, 4500)
                        boss_x = (SCREEN_WIDTH - boss_width) // 2
                        boss_y = 120

                    # Reset ball and paddle
                    balls_x[0] = paddle_x + (PADDLE_WIDTH - BALL_WIDTH) // 2
                    balls_y[0] = paddle_y - BALL_HEIGHT
                    balls_launched[0] = False
                    balls_speed_x[0] = 0
                    balls_speed_y[0] = 0
                    paddle_x = 640
                    player2_paddle_x = 640
                    paddle_speed_x = get_paddle_speed_for_level(current_level)
                    

                    # Clear flying bricks, powerups, and bullets for the new level
                    flying_bricks_x.clear()
                    flying_bricks_y.clear()
                    flying_bricks_color.clear()
                    powerups_x.clear()
                    powerups_y.clear()
                    powerups_color.clear()
                    bullets_x.clear()
                    bullets_y.clear()
                    bullets_speed_y.clear()
                    shoot_cooldown_p1 = 0
                    shoot_cooldown_p2 = 0
                    
                    # Clear extra balls, keep only the main ball
                    while len(balls_x) > 1:
                        balls_x.pop()
                        balls_y.pop()
                        balls_speed_x.pop()
                        balls_speed_y.pop()
                        balls_launched.pop()

                    # Show level message
                    level_message_timer = pygame.time.get_ticks() + 2000  # 2 seconds
                    level_message_alpha = 255
                    game_state = "LEVEL_START"
                skip_key_pressed = True
                level_skip = 0
        else:
            skip_key_pressed = False
        
        if keys[pygame.K_p]:
            paddle_cheat = 1
        if keys[pygame.K_a] and paddle_cheat == 1:
            paddle_cheat = 2
        if keys[pygame.K_d] and paddle_cheat == 2:
            paddle_cheat = 3
        if keys[pygame.K_d] and paddle_cheat == 3:
            paddle_cheat = 4
        if keys[pygame.K_l] and paddle_cheat == 4:
            paddle_cheat = 5
        if keys[pygame.K_e] and paddle_cheat == 5:
            paddle_cheat = 6
        if paddle_cheat == 6:
            cheats_used = True
            PADDLE_WIDTH = SCREEN_WIDTH
            paddle_img = get_sprite(1158, 396, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
            paddle_powerup_img = get_sprite(1403, 66, 243, 64, PADDLE_WIDTH, PADDLE_HEIGHT)
    elif game_state == "PLAYING":

        #
        # move everything
        #

        # toggle dev mode with T
        if keys[pygame.K_t]:
            if not dev_mode_key_pressed:
                dev_mode = not dev_mode
                dev_mode_key_pressed = True
        else:
            dev_mode_key_pressed = False

        
        if keys[pygame.K_d]:                              # key d is down
            # makes the paddle move right
            paddle_x = paddle_x + abs(paddle_speed_x)
        if keys[pygame.K_a]:                              # key a is down
            # makes the paddle move left
            paddle_x = paddle_x - abs(paddle_speed_x)

        if player_mode == 2:
            if keys[pygame.K_l]:
                player2_paddle_x += paddle_speed_x
            if keys[pygame.K_j]:
                player2_paddle_x -= paddle_speed_x

        if boss_active:
            # increase speed when boss reaches half HP (apply once)
            if boss_hp <= boss_max_hp // 2 and boss_speed == BOSS_BASE_SPEED:
                boss_speed = BOSS_BASE_SPEED * 2

            boss_x += boss_speed * boss_direction
            boss_y += boss_vertical_speed * boss_vertical_direction

            # Bounce boss vertically within a limited range
            if boss_y <= 80:
                boss_y = 80
                boss_vertical_direction = 1
            elif boss_y >= 220:
                boss_y = 220
                boss_vertical_direction = -1

            current_time = pygame.time.get_ticks()
            if current_time >= boss_next_action_time:
                boss_next_action_time = current_time + random.randint(700, 2200)

                # Randomly change horizontal direction for a less predictable path
                if random.random() < 0.35:
                    boss_direction *= -1

                # Randomly change vertical movement speed and direction
                boss_vertical_speed = random.randint(1, 3)
                if random.random() < 0.5:
                    boss_vertical_direction *= -1

            if boss_last_hit_cooldown > 0:
                boss_last_hit_cooldown -= 1

            if boss_shake_timer > 0:
                boss_shake_timer -= 1

            # boss drops rockets periodically, faster after half HP
            if current_time >= boss_rocket_drop_time:
                boss_rocket_drop_time = current_time + random.randint(2500, 3500) if boss_hp <= boss_max_hp // 2 else current_time + random.randint(3500, 4500)
                powerups_x.append(boss_x + (boss_width // 2) - 16)
                powerups_y.append(boss_y + boss_height)
                powerups_color.append("rocket")
        if boss_x <= 0:
            boss_direction = 1

        if boss_x + boss_width >= SCREEN_WIDTH:
            boss_direction = -1

        # shoot bullets when shoot powerup cheat is enabled
        current_time = pygame.time.get_ticks()
        if cheat_states[4]:
            if keys[pygame.K_q] and current_time >= shoot_cooldown_p1:
                bullets_x.append(paddle_x + (PADDLE_WIDTH - BULLET_WIDTH) // 2)
                bullets_y.append(paddle_y - BULLET_HEIGHT)
                bullets_speed_y.append(-BULLET_SPEED)
                shoot_cooldown_p1 = current_time + 250
            if player_mode == 2 and keys[pygame.K_u] and current_time >= shoot_cooldown_p2:
                bullets_x.append(player2_paddle_x + (PADDLE_WIDTH - BULLET_WIDTH) // 2)
                bullets_y.append(player2_paddle_y - BULLET_HEIGHT)
                bullets_speed_y.append(-BULLET_SPEED)
                shoot_cooldown_p2 = current_time + 250

        # stop paddle at edge
        if paddle_x < 0:                             # left edge
            paddle_x = 0                             # stops the paddle at left edge of screen
        if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:   # right edge
            # stops the paddle at right edge of screen
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        if player_mode == 2:
            if player2_paddle_x < 0:
                player2_paddle_x = 0
            if player2_paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
                player2_paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        # launch ball if not launched
        if len(balls_x) > 0 and not balls_launched[0]:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                balls_launched[0] = True
                direction = random.choice([-1, 1])
                # Increase starting speed based on settings and level
                start_speed = ball_speed_setting + (current_level * 1)
                balls_speed_x[0] = start_speed * direction
                balls_speed_y[0] = -start_speed
                if current_level == 0 and not timer_started:
                    timer_started = True
                    timer_start_ticks = pygame.time.get_ticks()
                    timer_end_ticks = 0
            else:
                # keep ball on paddle
                balls_x[0] = paddle_x + (PADDLE_WIDTH - BALL_WIDTH) // 2
                balls_y[0] = paddle_y - BALL_HEIGHT

        # move all balls
        for ball_idx in range(len(balls_x) - 1, -1, -1):
            if balls_launched[ball_idx]:
                balls_x[ball_idx] = balls_x[ball_idx] + balls_speed_x[ball_idx]
                balls_y[ball_idx] = balls_y[ball_idx] + balls_speed_y[ball_idx]
            
            # Remove ball if it goes off the bottom without hitting paddle
            if balls_y[ball_idx] + BALL_HEIGHT > paddle_y + PADDLE_HEIGHT:
                balls_x.pop(ball_idx)
                balls_y.pop(ball_idx)
                balls_speed_x.pop(ball_idx)
                balls_speed_y.pop(ball_idx)
                balls_launched.pop(ball_idx)

        # move flying bricks
        for i in range(len(flying_bricks_y) - 1, -1, -1):
            flying_bricks_y[i] -= 15

            if flying_bricks_y[i] < -BRICK_HEIGHT:
                flying_bricks_x.pop(i)
                flying_bricks_y.pop(i)
                flying_bricks_color.pop(i)

        # move powerups
        for i in range(len(powerups_y) - 1, -1, -1):
            powerups_y[i] += 8
            caught_by_p1 = (powerups_x[i] + 32 > paddle_x and
                            powerups_x[i] < paddle_x + PADDLE_WIDTH and
                            powerups_y[i] + 32 > paddle_y and
                            powerups_y[i] < paddle_y + PADDLE_HEIGHT)
            caught_by_p2 = False
            if player_mode == 2:
                caught_by_p2 = (powerups_x[i] + 32 > player2_paddle_x and
                                powerups_x[i] < player2_paddle_x + PADDLE_WIDTH and
                                powerups_y[i] + 32 > player2_paddle_y and
                                powerups_y[i] < player2_paddle_y + PADDLE_HEIGHT)

            if caught_by_p1 or caught_by_p2:
                gevangen_kleur = powerups_color[i]

                if gevangen_kleur == "grey":
                    blocks_broken += 50
                    paddle_timer = pygame.time.get_ticks() + 2000 # 2000 miliseconds so 2 seconds
                elif gevangen_kleur == "life":
                    if lives < max_lives:
                        lives += 1
                elif gevangen_kleur == "ball":
                    # Spawn a new ball with the same velocity as the first ball
                    if len(balls_x) > 0:
                        spawn_new_ball(
                            balls_x[0], 
                            balls_y[0], 
                            balls_speed_x[0],
                            balls_speed_y[0]
                        )
                    print("Extra ball spawned! Total balls: " + str(len(balls_x)))
                elif gevangen_kleur == "rocket":
                    if not cheat_states[2]:
                        lives -= 1
                    if lives <= 0:
                        score_msg = "Score: " + str(blocks_broken)
                        game_status_msg = "You lost"
                        game_state = "GAME_OVER"
                else:
                    for j in range(len(bricks_color) - 1, -1, -1): # used j because i was already taken
                        if gevangen_kleur in bricks_color[j]:
                            if "_cracked" not in bricks_color[j]:
                                bricks_color[j] = bricks_color[j] + "_cracked"
                            else:
                                flying_bricks_x.append(bricks_x[j])
                                flying_bricks_y.append(bricks_y[j])
                                flying_bricks_color.append(bricks_color[j])

                                bricks_x.pop(j)
                                bricks_y.pop(j)
                                bricks_color.pop(j)
                                blocks_broken += 10

                                if len(bricks_x) == 0:
                                    check_level_clear()
                if len(powerups_x) == 0:
                    break
                powerups_x.pop(i)
                powerups_y.pop(i)
                powerups_color.pop(i)
            elif powerups_y[i] > SCREEN_HEIGHT:
                powerups_x.pop(i)
                powerups_y.pop(i)
                powerups_color.pop(i)

        # move bullets
        for b_idx in range(len(bullets_y) - 1, -1, -1):
            bullets_y[b_idx] += bullets_speed_y[b_idx]
            if bullets_y[b_idx] < -BULLET_HEIGHT:
                bullets_x.pop(b_idx)
                bullets_y.pop(b_idx)
                bullets_speed_y.pop(b_idx)
                continue

            bullet_level_cleared = False
            if boss_active:
                if (bullets_x[b_idx] + BULLET_WIDTH > boss_x and
                    bullets_x[b_idx] < boss_x + boss_width and
                    bullets_y[b_idx] + BULLET_HEIGHT > boss_y and
                    bullets_y[b_idx] < boss_y + boss_height):

                    boss_hp -= 1

                    bullets_x.pop(b_idx)
                    bullets_y.pop(b_idx)
                    bullets_speed_y.pop(b_idx)

                    if boss_hp <= 0:
                        boss_active = False
                        if timer_started and timer_end_ticks == 0:
                            timer_end_ticks = pygame.time.get_ticks()

                        score_msg = "Score: " + str(blocks_broken + 1000)
                        game_status_msg = "Boss Defeated!"
                        if os.path.exists(OUTRO_FILE):
                            game_state = "OUTRO"
                        else:
                            game_state = "GAME_OVER"

                    continue
            for i in range(len(bricks_x) - 1, -1, -1):
                if (bullets_x[b_idx] + BULLET_WIDTH > bricks_x[i] and
                        bullets_x[b_idx] < bricks_x[i] + BRICK_WIDTH and
                        bullets_y[b_idx] + BULLET_HEIGHT > bricks_y[i] and
                        bullets_y[b_idx] < bricks_y[i] + BRICK_HEIGHT):
                    if "_cracked" not in bricks_color[i]:
                        bricks_color[i] = bricks_color[i] + "_cracked"
                    else:
                        bricks_x.pop(i)
                        bricks_y.pop(i)
                        bricks_color.pop(i)
                        blocks_broken += 10
                        bullet_level_cleared = check_level_clear()

                    if not bullet_level_cleared:
                        bullets_x.pop(b_idx)
                        bullets_y.pop(b_idx)
                        bullets_speed_y.pop(b_idx)
                    break

            if bullet_level_cleared:
                break

        # bounce ball for all balls
        for ball_idx in range(len(balls_x)):
            if balls_x[ball_idx] < 0:                           # left edge
                # positive x-speed = move right
                balls_speed_x[ball_idx] = abs(balls_speed_x[ball_idx])
            if balls_x[ball_idx] + BALL_WIDTH > SCREEN_WIDTH:   # right edge
                # negative x-speed = move left
                balls_speed_x[ball_idx] = abs(balls_speed_x[ball_idx]) * -1
            if balls_y[ball_idx] < 0:                           # top edge
                # positive y-speed = move down
                balls_speed_y[ball_idx] = abs(balls_speed_y[ball_idx])

        #
        # handle collisions
        #
        level_cleared = False
        for ball_idx in range(len(balls_x)):
            # boss collision for this ball
            if boss_active and boss_last_hit_cooldown <= 0:
                if (balls_x[ball_idx] + BALL_WIDTH > boss_x and
                    balls_x[ball_idx] < boss_x + boss_width and
                    balls_y[ball_idx] + BALL_HEIGHT > boss_y and
                    balls_y[ball_idx] < boss_y + boss_height):

                    boss_hp -= 1
                    boss_last_hit_cooldown = 5
                    boss_shake_timer = 8

                    overlap_left = balls_x[ball_idx] + BALL_WIDTH - boss_x
                    overlap_right = boss_x + boss_width - balls_x[ball_idx]
                    overlap_top = balls_y[ball_idx] + BALL_HEIGHT - boss_y
                    overlap_bottom = boss_y + boss_height - balls_y[ball_idx]
                    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                    if min_overlap == overlap_top:
                        balls_speed_y[ball_idx] = -abs(balls_speed_y[ball_idx])
                        balls_y[ball_idx] = boss_y - BALL_HEIGHT - 2
                    elif min_overlap == overlap_bottom:
                        balls_speed_y[ball_idx] = abs(balls_speed_y[ball_idx])
                        balls_y[ball_idx] = boss_y + boss_height + 2
                    elif min_overlap == overlap_left:
                        balls_speed_x[ball_idx] = -abs(balls_speed_x[ball_idx])
                        balls_x[ball_idx] = boss_x - BALL_WIDTH - 2
                    else:
                        balls_speed_x[ball_idx] = abs(balls_speed_x[ball_idx])
                        balls_x[ball_idx] = boss_x + boss_width + 2

                    if boss_hp <= 0:
                        boss_active = False
                        if timer_started and timer_end_ticks == 0:
                            timer_end_ticks = pygame.time.get_ticks()

                        score_msg = "Score: " + str(blocks_broken + 1000)
                        game_status_msg = "Boss Defeated!"
                        # Play outro if file exists
                        if os.path.exists(OUTRO_FILE):
                            game_state = "OUTRO"
                        else:
                            game_state = "GAME_OVER"

                    # skip further collision checks for this ball this frame
                    continue

            for i in range(len(bricks_x) - 1, -1, -1):
                if balls_x[ball_idx] + BALL_WIDTH > bricks_x[i] and balls_x[ball_idx] < bricks_x[i] + BRICK_WIDTH and balls_y[ball_idx] + BALL_HEIGHT > bricks_y[i] and balls_y[ball_idx] < bricks_y[i] + BRICK_HEIGHT:
                    print('brick ' + str(i) + ' geraakt')

                    # from up
                    if balls_speed_y[ball_idx] > 0 and balls_y[ball_idx] < bricks_y[i]:
                        balls_speed_y[ball_idx] = -abs(balls_speed_y[ball_idx])
                    # from down
                    elif balls_speed_y[ball_idx] < 0 and balls_y[ball_idx] + BALL_HEIGHT > bricks_y[i] + BRICK_HEIGHT:
                        balls_speed_y[ball_idx] = abs(balls_speed_y[ball_idx])
                    # from left
                    elif balls_speed_x[ball_idx] > 0 and balls_x[ball_idx] < bricks_x[i]:
                        balls_speed_x[ball_idx] = -abs(balls_speed_x[ball_idx])
                    # from right
                    elif balls_speed_x[ball_idx] < 0 and balls_x[ball_idx] + BALL_WIDTH > bricks_x[i] + BRICK_WIDTH:
                        balls_speed_x[ball_idx] = abs(balls_speed_x[ball_idx])

                    current_color = bricks_color[i]
                   
                    # checking is brick is cracked 
                    if "_cracked" not in current_color:     # not cracked yet
                        bricks_color[i] = current_color + "_cracked"
                    else:                                   # cracked
                        if cheat_states[3]:
                            if random.randint(1, 10) <= 10:
                                available_powerups = get_powerup_colors_for_level(current_level) + ["grey", "ball"]
                                # 20% chance to spawn a life powerup instead
                                if random.randint(1, 10) <= 0:
                                    gekozen_powerup = "life"
                                # 10% chance to spawn a ball powerup instead
                                elif random.randint(1, 10) <= 10:
                                    gekozen_powerup = "ball"
                                else:
                                    gekozen_powerup = random.choice(available_powerups)
                                powerups_x.append(
                                    bricks_x[i] + (BRICK_WIDTH // 2) - 16)
                                powerups_y.append(bricks_y[i])
                                powerups_color.append(gekozen_powerup)
                            
                            else:
                                flying_bricks_x.append(bricks_x[i])
                                flying_bricks_y.append(bricks_y[i])
                                flying_bricks_color.append(bricks_color[i])
                        else:
                            if random.randint(1, 10) <= 3:
                                available_powerups = get_powerup_colors_for_level(current_level) + ["grey", "ball"]
                                # 20% chance to spawn a life powerup instead
                                if random.randint(1, 10) <= 3:
                                    gekozen_powerup = "life"
                                # 10% chance to spawn a ball powerup instead
                                elif random.randint(1, 10) >= 8:
                                    gekozen_powerup = "ball"
                                else:
                                    gekozen_powerup = random.choice(available_powerups)
                                powerups_x.append(
                                    bricks_x[i] + (BRICK_WIDTH // 2) - 16)
                                powerups_y.append(bricks_y[i])
                                powerups_color.append(gekozen_powerup)
                            
                            else:
                                flying_bricks_x.append(bricks_x[i])
                                flying_bricks_y.append(bricks_y[i])
                                flying_bricks_color.append(bricks_color[i])

                        bricks_x.pop(i)
                        bricks_y.pop(i)
                        bricks_color.pop(i)

                        blocks_broken += 10

                        # speed increase: increase ball Y speed and paddle speed together
                        max_speed = 10

                        if abs(balls_speed_y[ball_idx]) < max_speed:
                            balls_speed_y[ball_idx] *= 1.04
                            paddle_speed_x = min(paddle_speed_x * 1.04, PADDLE_MAX_SPEED)

                        if len(bricks_x) == 0:
                            if check_level_clear():
                                level_cleared = True

                        break
            if level_cleared:
                break

        # making the ball collide with the paddle
        for ball_idx in range(len(balls_x)):
            if balls_x[ball_idx] + BALL_WIDTH > paddle_x and balls_x[ball_idx] < paddle_x + PADDLE_WIDTH and balls_y[ball_idx] + BALL_HEIGHT > paddle_y and balls_y[ball_idx] < paddle_y + PADDLE_HEIGHT:
                if balls_speed_y[ball_idx] > 0:
                    balls_speed_y[ball_idx] = -abs(balls_speed_y[ball_idx])

                # calculate center
                paddle_center = paddle_x + (PADDLE_WIDTH / 2)
                ball_center = balls_x[ball_idx] + (BALL_WIDTH / 2)

                # calculate distance from center
                offset = ball_center - paddle_center

                # calculate ratio
                ratio = offset / (PADDLE_WIDTH / 2)
                MAX_BOUNCE_SPEED = 10
                balls_speed_x[ball_idx] = ratio * MAX_BOUNCE_SPEED

            if player_mode == 2 and balls_x[ball_idx] + BALL_WIDTH > player2_paddle_x and balls_x[ball_idx] < player2_paddle_x + PADDLE_WIDTH and balls_y[ball_idx] < player2_paddle_y + PADDLE_HEIGHT and balls_y[ball_idx] + BALL_HEIGHT > player2_paddle_y:
                if balls_speed_y[ball_idx] > 0:
                    balls_speed_y[ball_idx] = -abs(balls_speed_y[ball_idx])

                paddle_center = player2_paddle_x + (PADDLE_WIDTH / 2)
                ball_center = balls_x[ball_idx] + (BALL_WIDTH / 2)
                offset = ball_center - paddle_center
                ratio = offset / (PADDLE_WIDTH / 2)
                MAX_BOUNCE_SPEED = 10
                balls_speed_x[ball_idx] = ratio * MAX_BOUNCE_SPEED

        # Check if all balls are lost
        if len(balls_x) == 0:
            if not cheat_states[2]:
                lives -= 1
            else:
                lives = max(lives, 1)

            if lives <= 0:
                score_msg = "Score: " + str(blocks_broken)
                game_status_msg = "You lost"
                game_state = "GAME_OVER"
            else:
                # Reset with one new ball
                balls_x = [paddle_x + (PADDLE_WIDTH - BALL_WIDTH) // 2]
                balls_y = [paddle_y - BALL_HEIGHT]
                balls_speed_x = [0]
                balls_speed_y = [0]
                balls_launched = [False]

        #
        # draw everything
        #

        # draw background
        screen.blit(background_img, (0, 0))

        # draw all balls
        for i in range(len(balls_x)):
            screen.blit(ball_img, (balls_x[i], balls_y[i]))

        # draw bullets
        for i in range(len(bullets_x)):
            pygame.draw.rect(screen, (255, 255, 255), (bullets_x[i], bullets_y[i], BULLET_WIDTH, BULLET_HEIGHT))

        # draw boss
        if boss_active:
            shake_x = 0
            shake_y = 0
            if boss_shake_timer > 0:
                shake_x = random.randint(-boss_shake_magnitude, boss_shake_magnitude)
                shake_y = random.randint(-boss_shake_magnitude // 2, boss_shake_magnitude // 2)
            screen.blit(boss_img, (boss_x + shake_x, boss_y + shake_y))

        if boss_active:

            pygame.draw.rect(
                screen,
                (80, 80, 80),
                (SCREEN_WIDTH//2 - 200, 90, 400, 25)
            )

            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (
                    SCREEN_WIDTH//2 - 200,
                    90,
                    int(400 * boss_hp / boss_max_hp),
                    25
                )
            )

            boss_text = font.render(
                "BOSS HP: " + str(boss_hp),
                True,
                (255,255,255)
            )

            screen.blit(
                boss_text,
                (SCREEN_WIDTH//2 - 80, 55)
            )
        # draw paddle
        if pygame.time.get_ticks() < paddle_timer:
            screen.blit(paddle_powerup_img, (paddle_x, paddle_y))
        else:
            screen.blit(paddle_img, (paddle_x, paddle_y))
        if player_mode == 2:
            screen.blit(paddle_img, (player2_paddle_x, player2_paddle_y))
        # draw bricks
        for i in range(len(bricks_x)):
            color_name = bricks_color[i]
            current_brick_img = brick_types[color_name]
            screen.blit(current_brick_img, (bricks_x[i], bricks_y[i]))
        # draw flying bricks
        for i in range(len(flying_bricks_x)):
            color_name = flying_bricks_color[i]
            current_brick_img = brick_types[color_name]
            screen.blit(current_brick_img,
                        (flying_bricks_x[i], flying_bricks_y[i]))
        # draw powerups
        for i in range(len(powerups_x)):
            color_name = powerups_color[i]
            current_powerup_img = powerup_types[color_name]
            screen.blit(current_powerup_img, (powerups_x[i], powerups_y[i]))
        
        # draw score at top of screen
        score_text = font.render("Score: " + str(blocks_broken), True, 'white')
        screen.blit(score_text, (20, 20))
        
        # draw level at top right 
        if current_level == len(all_levels) - 1:
            level_label = "Final Level"
        else:
            level_label = "Level " + str(current_level + 1)
        level_text = font.render(level_label, True, 'white')
        level_text_rect = level_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        screen.blit(level_text, level_text_rect)
        
        # draw lives as small heart icons at top center
        label_text = font.render("Lives:", True, (255, 100, 100))
        label_rect = label_text.get_rect()
        # position label just left of center
        label_rect.top = 20
        label_rect.centerx = (SCREEN_WIDTH // 2) - 40
        screen.blit(label_text, label_rect)

        # draw hearts 
        if cheat_states[2]:
            # infinite lives
            if life_img:
                screen.blit(life_img, (label_rect.right + 8, 18))
            inf_text = font.render("∞", True, (255, 100, 100))
            inf_rect = inf_text.get_rect()
            inf_rect.left = label_rect.right + (44 if life_img else 8)
            inf_rect.top = 20
            screen.blit(inf_text, inf_rect)
        else:
            # draw one heart per life 
            max_draw = min(lives, max_lives)
            for i in range(max_draw):
                x = label_rect.right + 8 + i * 36
                y = 18
                if life_img:
                    screen.blit(life_img, (x, y))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, 24, 24))
        
        if cheat_states[4]:
            if player_mode == 2:
                shoot_text = font.render("Shoot: Q (P1) / U (P2)", True, (255, 255, 100))
            else:
                shoot_text = font.render("Shoot: Q", True, (255, 255, 100))
            screen.blit(shoot_text, (20, 100))

        # draw ball count 
        if current_level != len(all_levels) - 1:
            balls_text = font.render("Balls: " + str(len(balls_x)), True, (100, 255, 100))
            balls_text_rect = balls_text.get_rect(centerx=SCREEN_WIDTH // 2, top=60)
            screen.blit(balls_text, balls_text_rect)
        
        # draw dev info if enabled
        if dev_mode:
            draw_dev_info(screen, 20, 100)
    elif game_state == "OUTRO":
        # Show outro video
        outro_finished = play_video(OUTRO_FILE, screen, 'outro')
        if keys[pygame.K_x]:
            cheats_used = False
        if outro_finished or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            game_state = "GAME_OVER"
            if outro_video:
                outro_video.release()
            outro_video = None
        
        pygame.display.flip()
    
    elif game_state == "GAME_OVER":
        screen.fill('black')
 
        end_text = font.render(game_status_msg, True, 'white')
        screen.blit(end_text, (100, 300))
 
        score_end_text = font.render(score_msg, True, 'white')
        screen.blit(score_end_text, (100, 400))
        extra_line_y = 520
        if timer_started and timer_end_ticks > 0:   #als de timer gestart is 
            if timer_end_ticks - timer_start_ticks <= record_ticks: #als het record verbroken is
                if not cheats_used:
                    timer_text = font.render(
                        "Time: " + format_time(timer_end_ticks - timer_start_ticks) + "   Well done! You beat the record!", True, 'white')
                    record_ticks = timer_end_ticks - timer_start_ticks
                    save_record()
                else:                 # wel cheats
                    timer_text = font.render(
                        "Time: " + format_time(timer_end_ticks - timer_start_ticks) + "   Well done! You beat the record!", True, 'white')
            else:     # niet record verbroken
                timer_text = font.render(
                    "Time: " + format_time(timer_end_ticks - timer_start_ticks), True, 'white')
            screen.blit(timer_text, (100, 460))
            if cheats_used:
                cheat_timer_text = font.render("Try to do it without cheats next time!", True, (200, 200, 100))
                screen.blit(cheat_timer_text, (100, 500))
            extra_line_y = 560  # push the rest down to make room
            print(timer_end_ticks, timer_start_ticks, timer_end_ticks - timer_start_ticks)

        if not cheats_used and game_status_msg != "You lost": #als je verloren hebt zonder cheats
            no_cheat_text = font.render("Well done! Without cheats!", True, (180, 255, 180))
            screen.blit(no_cheat_text, (100, extra_line_y))
            restart_y = extra_line_y + 80
        else:
            restart_y = extra_line_y

        restart_text = font.render(
            "Druk op R om opnieuw te spelen", True, 'gray')
        screen.blit(restart_text, (100, restart_y))
        # restart game option  
        if keys[pygame.K_r]:  # r to restart
            reset_game()

    # show screen
    pygame.display.flip()

    #
    # wait until next frame
    #

    fps_clock.tick(FPS)  # Sleep the remaining time of this frame

print('mygame stopt running')