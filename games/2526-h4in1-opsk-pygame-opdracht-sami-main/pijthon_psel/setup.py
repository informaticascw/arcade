from typing import * # type: ignore
# from typing_extensions import * # type: ignore
import pygame, time, os, pijthon_psel_ffi, json, math, random
from .classes import Entity, Brick, Ball, Paddle, Powerup
from pijthon_psel_ffi import panic

#
# definitions 
#

# consts
# INFO: pygame.display._VidInfo = pygame.display.Info()
# WH_RAT: float = INFO.current_w / INFO.current_h

ROOT: str = os.path.abspath(os.path.join(__file__, "../.."))
FPS: int = 120
WRES: int = 1920
# HRES: int = 720

BALL_WIDTH: int = 16
BALL_HEIGHT: int = 16
BALL_SPEED: float = 600
MAX_ANGLE: float = 75
BALLS_POP_INTERVAL: float = 30
MIN_BALLS: int = 2

PADDLE_WIDTH: int = 174
PADDLE_HEIGHT: int = 24

BRICKS_WIDTH: int = 96
BRICKS_HEIGHT: int = 24

POWERUP_INTERVAL: float = 7
POWERUP_WIDTH: int = 120
POWERUP_HEIGHT: int = 32
POWERUP_SPEED: float = 1000


pijthon_psel_ffi.test()


#
# init game
#
print(pygame.init())

modes: List[Tuple[int, int]] = pygame.display.list_modes()
background: Tuple[int, int, int] = (10, 15, 17)
fps: int = FPS
mode: Tuple[int, int] = modes[0]
whRat = mode[1] / mode[0]
width = WRES
height = WRES * whRat

print(f"{width}x{height}@{FPS}")

screen: pygame.Surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED, depth=1, display=0, vsync=1)
fps_clock: pygame.time.Clock = pygame.time.Clock()

sbiggerfont: pygame.font.Font = pygame.font.Font(ROOT + '/assets/PressStart2P-Regular.ttf', 50)
biggerfont: pygame.font.Font = pygame.font.Font(ROOT + '/assets/PressStart2P-Regular.ttf', 48)
bigfont: pygame.font.Font = pygame.font.Font(ROOT + '/assets/PressStart2P-Regular.ttf', 36)
mediumfont: pygame.font.Font = pygame.font.Font(ROOT + '/assets/PressStart2P-Regular.ttf', 24)
smallfont: pygame.font.Font = pygame.font.Font(ROOT + '/assets/PressStart2P-Regular.ttf', 11)
atlas: Dict[str, Dict[str, int]] = json.load(open(ROOT + '/assets/BreakoutAtlas-default.json'))
spritesheet: pygame.Surface = pygame.image.load(ROOT + '/assets/BreakoutAtlas-default.png').convert_alpha()  


#
# read images
#
    
# level: int = 0

ball_data = atlas["ball"]
ball_img: pygame.Surface = pygame.Surface((ball_data["width"], ball_data["height"]), pygame.SRCALPHA)  
ball_img.blit(spritesheet, (0, 0), (ball_data["x"], ball_data["y"], ball_data["width"], ball_data["height"]))
ball_img: pygame.Surface = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))  

paddle_data = atlas["paddle-wide"]
paddle_img: pygame.Surface = pygame.Surface((paddle_data["width"], paddle_data["height"]), pygame.SRCALPHA)  
paddle_img.blit(spritesheet, (0, 0), (paddle_data["x"], paddle_data["y"], paddle_data["width"], paddle_data["height"]))
paddle_img: pygame.Surface = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))


paddle = Paddle((width / 2 - PADDLE_WIDTH / 2, height * 0.87), (PADDLE_WIDTH, PADDLE_HEIGHT), paddle_img, 1000)

brick_tiers: List[pygame.Surface] = []
cracked_brick_tiers: List[pygame.Surface] = []

for tier in [("brick-blue", "brick-blue-cracked"), ("brick-lightgreen", "brick-lightgreen-cracked"), ("brick-purple", "brick-purple-cracked"), ("brick-red", "brick-red-cracked"), ("brick-orange", "brick-orange-cracked"), ("brick-lightblue", "brick-lightblue-cracked"), ("brick-yellow", "brick-yellow-cracked"), ("brick-green", "brick-green-cracked"), ("brick-grey", "brick-grey-cracked"), ("brick-brown", "brick-brown-cracked")]:
    brick_data = atlas[tier[0]]
    bricks_img: pygame.Surface = pygame.Surface((brick_data["width"], brick_data["height"]), pygame.SRCALPHA)  
    bricks_img.blit(spritesheet, (0, 0), (brick_data["x"], brick_data["y"], brick_data["width"], brick_data["height"]))
    # bricks_img: pygame.Surface = pygame.transform.scale(bricks_img, (block_data["width"], block_data["height"]))

    brick_tiers.append(bricks_img)

    brick_data = atlas[tier[1]]
    bricks_img: pygame.Surface = pygame.Surface((brick_data["width"], brick_data["height"]), pygame.SRCALPHA)  
    bricks_img.blit(spritesheet, (0, 0), (brick_data["x"], brick_data["y"], brick_data["width"], brick_data["height"]))

    cracked_brick_tiers.append(bricks_img)
    pass


powerup_types: List[pygame.Surface] = []

for powerup in ["paddle-plus50", "paddle-plus100-step4", "paddle-plus250", "paddle-plus500", "paddle-slow", "paddle-fast", "paddle-balls", "paddle-comet-red", "paddle-comet-green", "paddle-arrows-inside", "paddle-arrows-outside", "paddle-redbar"]:
    powerup_data = atlas[powerup]
    powerup_img: pygame.Surface = pygame.Surface((powerup_data["width"], powerup_data["height"]), pygame.SRCALPHA)  
    powerup_img.blit(spritesheet, (0, 0), (powerup_data["x"], powerup_data["y"], powerup_data["width"], powerup_data["height"]))

    powerup_types.append(powerup_img)
    pass


def new_brick_at(pos: Tuple[float, float], width: Tuple[float, float], tier: int = 0) -> Brick: return Brick(pos, width, tier, brick_tiers, cracked_brick_tiers)
def new_powerup_at(pos: Tuple[float, float], width: Tuple[float, float], type: int = 0, descent: float = 0) -> Powerup: return Powerup(pos, width, powerup_types, type, descent)


profanity: List[str] = json.load(open(ROOT + '/assets/profanity.json'))
