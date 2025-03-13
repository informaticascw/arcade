import pygame as pg

class Bird:
    def __init__(self, game, id):
        self.game = game

        self.id = id
        self.animation = game.assets[f"bird_{self.id}"]
        self.animation.done = False
        self.sprite = self.animation.copy().get_img()
        self.size = (self.sprite.get_width(), self.animation.images[0].get_height())
        
        self.pos = [40 if self.id == 1 else 100, (game.display.get_height() - game.assets["base"].get_height()) / 2 - self.size[1] / 2]
        self.vert_velocity = 0
        self.jump = False
        self.gravity = False
        self.dead = False
        
        self.score = 0
        
    def update(self):
        self.sprite = self.animation.get_img()
        
        # Jumping - add velocity upwards
        if self.jump:
            self.vert_velocity = -1 * self.game.constants["jump_strength"]
            self.jump = False
        
        self.pos[1] += self.vert_velocity * self.game.dt
        
        # Gravity - add velocity downwards
        if self.gravity:
            self.vert_velocity += self.game.constants["gravity"] * self.game.dt
        
        if self.dead and self.game.alive_birds:
            self.pos[0] += -1 * self.game.constants["horizontal_velocity"] * self.game.dt
        
        # Dont go above the screen
        if self.pos[1] <= 0:
            self.pos[1] = 0
            
        if self.pos[1] + self.size[1] >= (self.game.display.get_height() - self.game.assets["base"].get_height()):
            self.pos[1] = self.game.display.get_height() - self.game.assets["base"].get_height() - self.size[1]
            self.gravity = False
            self.die()
        
        if self.vert_velocity < 0:
            self.sprite = pg.transform.rotate(self.animation.get_img(), 35)
        if self.vert_velocity > 0:
            self.sprite = pg.transform.rotate(self.animation.get_img(), -35)

    def render(self, surface):
        surface.blit(self.sprite, self.pos)

        if self.game.started:
            scoreImg = pg.Surface((50, 36))
            for index, i in enumerate(f"{self.score:02d}"):
                i = int(i)
                img = self.game.assets["numbers"][i]
                img.set_colorkey((0,0,0))
                scoreImg.blit(img, (25 * index, 0))
            scoreImg.set_colorkey((0,0,0))
            if len(self.game.birds) > 1:
                if self.id == 1:
                    surface.blit(scoreImg, (surface.get_width() * .25 - scoreImg.get_width() / 2, 40))
                if self.id == 2:
                    surface.blit(scoreImg, (surface.get_width() * .75 - scoreImg.get_width() / 2, 40))
            else:
                surface.blit(scoreImg, (surface.get_width() / 2 - scoreImg.get_width() / 2, 40))
            
    def die(self):
        self.dead = True
        self.animation.done = True
        
    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])