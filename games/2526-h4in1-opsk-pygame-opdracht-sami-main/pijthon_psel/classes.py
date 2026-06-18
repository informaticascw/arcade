import pygame, math, random
from pygame import Surface, Rect
from typing import * # type: ignore



class Entity:
    x: float
    y: float


    def draw(self, surface: Surface) -> None: ...

    # def rectCollide(self, target: Entity, swidth: Tuple[float, float], twidth: Tuple[float, float]) -> bool: 
    #     self_rect = Rect(self.x, self.y, swidth[0], swidth[1])
    #     target_rect = Rect(target.x, target.y, twidth[0], twidth[1])
    #     return self_rect.colliderect(target_rect)

    pass

class HasWidth(Entity):
    width: float
    height: float

    def rectCollide(self, target: HasWidth) -> bool: 
        self_rect = Rect(self.x, self.y, self.width, self.height)
        target_rect = Rect(target.x, target.y, target.width, target.height)
        return self_rect.colliderect(target_rect)

    pass

class Text(Entity):
    text: str
    font: pygame.font.Font
    color: Tuple[int,int,int]

    def __init__(self, pos: Tuple[float, float], font: pygame.font.Font, text: str, color: Tuple[int,int,int], center: bool = False) -> None:
        self.font = font
        self.text = text
        self.color = color
        self.x, self.y = pos

        if center: self.center()
        pass

    def gettext(self) -> Surface:
        text: pygame.Surface = self.font.render(self.text, True, self.color)
        return text
    
    def center(self) -> None:
        text = self.gettext()
        self.x -= text.get_width() / 2
        self.y -= text.get_height() / 2
        pass

    @override
    def draw(self, surface: Surface) -> None:
        text: Surface = self.gettext()
        surface.blit(text, (self.x,self.y))
        pass

    pass

class Ball(HasWidth):
    speed_x: float = 0
    speed_y: float = 0
    img: Surface
    bounceMultiplier: float = -1
    shoot_mode: bool = False
    player: int = 0

    def __init__(self, pos: Tuple[float, float], width: Tuple[float, float], speed: Tuple[float, float], img: Surface, shoot_mode: bool = False, player: int = 0) -> None:
        self.img = img
        self.x, self.y = pos
        self.player = player
        self.shoot_mode = shoot_mode
        self.width, self.height = width
        self.speed_x, self.speed_y = speed
        pass

    @override
    def draw(self, surface: Surface) -> None:
        surface.blit(self.img, (self.x, self.y))
        pass

    # TODO: allow collisions from all sides
    def angledCollision(self, other: HasWidth, max_angle: float, upward: bool = True) -> None:
        angle: float = math.atan2(self.speed_y, self.speed_x)

        cent: float = self.x + self.width / 2
        othercent: float = other.x + other.width / 2
        diff: float = (cent - othercent) / (other.width / 2)
        diff = max(-1, min(1, diff))

        angle -= diff * math.radians(max_angle)
        speed: float = math.hypot(self.speed_x, self.speed_y)

        self.speed_x = math.cos(angle) * speed
        if upward: self.speed_y = -abs(math.sin(angle) * speed)
        else     : self.speed_y = abs(math.sin(angle) * speed)

        pass

    def simpleCollision(self, other: HasWidth, modifier: float = 1) -> None:
        pre_x = self.x - self.speed_x * modifier * 2
        pre_y = self.y - self.speed_y * modifier * 2

        prev_x = self.x - self.speed_x * modifier
        prev_y = self.y - self.speed_y * modifier

        from_left   = prev_x + self.width  <= other.x
        from_right  = prev_x >= other.x + other.width
        from_top    = prev_y + self.height <= other.y
        from_bottom = prev_y >= other.y + other.height

        if from_left:
            self.x = pre_x
            self.speed_x = -abs(self.speed_x)
            pass

        elif from_right:
            self.x = pre_x
            self.speed_x = abs(self.speed_x)
            pass

        if from_top:
            self.y = pre_y
            self.speed_y = -abs(self.speed_y)
            pass

        elif from_bottom:
            self.y = pre_y
            self.speed_y = abs(self.speed_y)
            pass
        pass

    pass

class Paddle(HasWidth):
    peed: float = 1000
    img: Surface

    follow_cheat: bool = False

    opos: Tuple[float, float]
    owidth: Tuple[float, float]
    oimg: Surface
    opeed: float

    def __init__(self, pos: Tuple[float, float], width: Tuple[float, float], img: Surface, peed: float) -> None:
        self.oimg = self.img = img
        self.opeed = self.peed = peed
        self.opos = self.x, self.y = pos
        self.owidth = self.width, self.height = width
        pass

    @override
    def draw(self, surface: Surface) -> None:
        surface.blit(self.img, (self.x, self.y))
        pass

    def reset(self) -> None:
        self.img = self.oimg
        self.peed = self.opeed
        self.x, self.y = self.opos
        self.width, self.height = self.owidth
        pass
    pass

class Brick(HasWidth):
    # img: Surface
    broken: bool = False
    tier: int = 0
    cracked: bool = False
    tiers: List[Surface]
    cracked_tiers: List[Surface]
    original_tier: int = 0

    def __init__(self, pos: Tuple[float, float], width: Tuple[float, float], tier: int, tiers: List[Surface], cracked_tiers: List[Surface]) -> None:
        self.x, self.y = pos
        self.width, self.height = width
        self.original_tier = self.tier = tier
        self.tiers, self.cracked_tiers = tiers, cracked_tiers
        pass

    @override
    def draw(self, surface: Surface) -> None:
        if self.cracked:
            img: Surface = pygame.transform.scale(self.cracked_tiers[self.tier], (self.width, self.height))
            surface.blit(img, (self.x, self.y))
            pass
        else:
            img: Surface = pygame.transform.scale(self.tiers[self.tier], (self.width, self.height))
            surface.blit(img, (self.x, self.y))
            pass
        # if not self.broken:
        #     pass
        pass

    def breakl(self) -> bool:
        if not self.cracked:
            self.cracked = True
            pass
        elif self.tier != 0:
            self.tier -= 1
            self.cracked = False
            pass
        else:
            self.broken = True
            pass

        # print(f"tier = {self.tier}, cracked = {self.cracked}, broken = {self.broken}")
        return self.broken

    pass

class Powerup(HasWidth):
    types: List[Surface]
    type: int
    descent: float

    def __init__(self, pos: Tuple[float, float], width: Tuple[float, float], types: List[Surface], type: int, descent: float) -> None:
        self.type = type
        self.types = types
        self.x, self.y = pos
        self.descent = descent
        self.width, self.height = width
        pass

    @override
    def draw(self, surface: Surface) -> None:
        img: Surface = pygame.transform.scale(self.types[self.type], (self.width, self.height))
        surface.blit(img, (self.x, self.y))
        pass

    @staticmethod
    def random() -> int:
        return random.choices(
            population=range(12),
            weights=[5, 3, 2, 1, 4, 4, 2, 0.5, 0.5, 2, 2, 2],
            k=1
        )[0]
    
    pass

class Bullet(HasWidth):
    img: Surface
    oimg: Surface
    angle: float
    velocity: float

    def __init__(self, pos: Tuple[float, float], width: Tuple[float, float], img: Surface, angle: float, velocity: float) -> None:
        self.img = img
        self.oimg = img
        self.angle = angle
        self.x, self.y = pos
        self.velocity = velocity
        self.width, self.height = width

        self.update_angle()
        pass

    def update_angle(self) -> None:
        self.img = pygame.transform.rotate(self.oimg, self.angle)
        pass

    def update(self, multiplier: float) -> None:
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.velocity * multiplier
        self.y += math.sin(rad) * self.velocity * multiplier
        pass

    @override
    def draw(self, surface: Surface) -> None:
        surface.blit(self.img, (self.x, self.y))
        pass