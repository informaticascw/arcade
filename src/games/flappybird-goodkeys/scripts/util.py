import os

import pygame as pg

BASE_IMG_PATH = "assets/images/"

def load_image(path):
    return pg.image.load(BASE_IMG_PATH + path).convert()

def load_images(path):
    files = sorted(os.listdir(BASE_IMG_PATH + path))
    res = []
    for file in files:
        img = pg.image.load(BASE_IMG_PATH + path + "/" + file).convert()
        img.set_colorkey((0, 0, 0))
        res.append(img)
        
    return res

class Animation:
    def __init__(self, images, img_dur, loop=True):
        self.images = images
        self.img_dur = img_dur # in frames
        self.loop = loop
        
        self.frame = 0
        self.done = False
        
    def update(self):
        if self.done: return
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True
        
    def get_img(self):
        return self.images[int(self.frame / self.img_dur)]
    
    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
class Button:
    def __init__(self, rect, txt, font, hovering=False, action=None, args=[]):
        self.rect = rect
        self.txt = txt
        self.font = font
        
        self.hovering = hovering
        
        self.action = action
        self.args = args
        
    def render(self, surface):
        if self.hovering:
            rect = pg.Rect(*self.rect)
            rect.x -= 3
            rect.y -= 3
            rect.width += 6
            rect.height += 6
            pg.draw.rect(surface, (255, 255, 255), rect)
        
        pg.draw.rect(surface, (255, 96, 24), self.rect)
        
        txt_img = self.font.render(self.txt, False, (255, 255, 255))
        txt_img_rect = txt_img.get_rect()
        surface.blit(txt_img, (self.rect.x + self.rect.width / 2 - txt_img_rect[2] / 2, self.rect.y + self.rect[3] / 2 - txt_img_rect[3] / 2))
        