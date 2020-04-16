import pygame

white=(255,255,255)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screensize):
        super().__init__()
        self.screensize = screensize
        self.centerx = screensize[0]*0.5
        self.centery = screensize[1]-10
        #player paddle dimensions
        self.width = 160
        self.height = 10
        self.rect = pygame.Rect(self.centerx-self.width*0.5,self.screensize[1],self.width,self.height)
        self.color = white
        #player paddle speed
        self.speed = 5
        self.direction = 0

    def update(self):
        self.centerx += self.direction*self.speed
        self.rect.center = (self.centerx, self.centery)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screensize[0]-1:
            self.rect.right = self.screensize[0]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
