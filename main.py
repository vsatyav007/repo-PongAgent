import pygame
from pong import Pong
from paddle import Paddle

white=(255,255,255)

def main():    
    pygame.init()
    pointcounter =0
    screensize = (640,480)
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()
    pong = Pong(screensize)
    paddle = Paddle(screensize)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    paddle.direction = -1
                elif event.key == K_RIGHT:
                    paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_LEFT and paddle.direction == -1:
                    paddle.direction = 0
                elif event.key == K_RIGHT and paddle.direction == 1:
                    paddle.direction = 0
        paddle.update()
        pointcounter= pong.update(paddle,pointcounter)
        if pong.hit_edge_bottom:
            print ('Your Score ' + str(pointcounter))
            running = False
        screen.fill((0,0,0))
        paddle.render(screen)
        pong.render(screen)
        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(pointcounter), 1, white)
        screen.blit(text, (310,10))
        pygame.display.flip()        
        clock.tick(60)
    pygame.quit()

main()