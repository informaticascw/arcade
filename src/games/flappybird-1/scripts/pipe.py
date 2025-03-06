import random

import pygame as pg

class Pipe:
    def __init__(self, game, gap_y):
        self.pos = game.display.get_width() + 20
        self.game = game
        self.velocity = -1 * game.constants["horizontal_velocity"]
        self.gap_y = gap_y
        self.gap_height = game.constants["gap"]
        
        self.img_top = pg.transform.flip(game.assets["pipe"], False, True)
        self.img_bottom = game.assets["pipe"]
        
        self.pointScored = False
        
    def update(self):
        self.pos += self.velocity * self.game.dt
        
        # Collisions with bird ---------------------------------------------------#
        rect_top = pg.Rect(self.pos, self.gap_y - self.img_top.get_height() - 6, *self.img_top.get_size())
        rect_bottom = pg.Rect(self.pos, self.gap_y + self.gap_height + 6, *self.img_bottom.get_size())

        for bird in self.game.birds:
            if bird.dead: continue
            if bird.rect().colliderect(rect_top) or bird.rect().colliderect(rect_bottom) and not bird.dead:
                bird.die()
                self.game.sfx["hit"].play()
                
            # Give point when past left of pipe --------------------------------------#
            if bird.rect().left > self.pos and not self.pointScored:
                bird.score += 1
                self.game.sfx["point"].play()
                self.pointScored = True
    
    def render(self, surface):
        surface.blit(self.img_top, (self.pos, self.gap_y - self.img_top.get_height()))
        surface.blit(self.img_bottom, (self.pos, self.gap_y + self.gap_height))
        
    def random(game):
        return Pipe(game, random.randint(50, 300))