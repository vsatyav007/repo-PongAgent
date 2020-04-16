import pygame

class Pong(pygame.sprite.Sprite):
    def __init__(self, screensize):
       super().__init__()
       self.screensize = screensize
       self.centerx = int(screensize[0]*0.5)
       self.centery = int(screensize[1]*0.5)
       self.radius = 8
       self.rect = pygame.Rect(self.centerx-self.radius,
                               self.centery-self.radius,
                               self.radius*2, self.radius*2)
       self.color = (255, 255, 255)
       self.direction = [1, -1]
       #speed of ball
       self.speedx = 5
       self.speedy = 5
       self.hit_edge_bottom = False

    def update(self, player_paddle,hits):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy
        self.rect.center = (self.centerx, self.centery)
        if self.rect.left <= 0:
            self.direction[0] = 1
        elif self.rect.top < 0:
            self.direction[1] = 1
        elif self.rect.right >= self.screensize[0]-1:
            self.direction[0]=-1
        elif self.rect.bottom >=self.screensize[1]-1:
            self.hit_edge_bottom = True

        if self.rect.colliderect(player_paddle.rect):
            self.direction[1] = -1
            hits += 1
        return hits

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
