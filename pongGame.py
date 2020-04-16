import pygame
from pong import Pong
from paddle import Paddle
from agent import DQN
import numpy as np
# import  matplotlib.pyplot as plt

white=(255,255,255)
black=(0,0,0)

class pongGame():
    def __init__(self):
        super().__init__()
        self.hits =0
        self.miss =0
        self.screensize = (640,480)
        self.screen = pygame.display.set_mode(self.screensize)
        self.pong = Pong(self.screensize)
        self.paddle = Paddle(self.screensize)
        self.done = False
        self.reward=0
    
    def reset(self):
        self.pong=Pong(self.screensize)
        self.paddle=Paddle(self.screensize)
        return [self.paddle.centerx*0.01, self.pong.centerx*0.01, self.pong.centery*0.01, self.pong.speedx, self.pong.speedy]
    
    def step(self,action):
        self.reward = 0
        self.done = 0
        
        if action == 0:
            self.paddle.direction=-1
            self.paddle.update()
            self.reward -= .1

        if action == 2:
            self.paddle.direction=1
            self.reward -= .1

        self.update()

        state = [self.paddle.centerx*0.01, self.pong.centerx*0.01, self.pong.centery*0.01, self.pong.speedx, self.pong.speedy]
        return self.reward, state, self.done

    def update(self):
        self.paddle.update()
        newhits=self.pong.update(self.paddle,self.hits)
        if self.hits < newhits:
            self.reward +=3
            self.hits=newhits
        if self.pong.hit_edge_bottom:
            self.miss +=1
            self.reward -= 3
            self.done=True
        self.screen.fill((0,0,0))
        self.paddle.render(self.screen)
        self.pong.render(self.screen)
        #Display scores:
        font = pygame.font.Font(None, 30)
        text = font.render("Hit: "+str(self.hits), 1, white)
        self.screen.blit(text, (250,10))
        text = font.render("Miss: "+str(self.miss), 1, white)
        self.screen.blit(text, (350,10))
        pygame.display.flip()        
        # clock.tick(60)

def run(ep,train=False):
    pygame.init()
    loss=[]
    agent = DQN(3, 5)
    env=pongGame()
    weights_filepath = 'PongGame.h5'
    if train==False:
        agent.model.load_weights(weights_filepath)
        print("weights loaded")
    for e in range(ep):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        state = env.reset()
        state = np.reshape(state, (1, 5))
        score = 0
        max_steps = 1000
        for i in range(max_steps):
            action = agent.act(state)
            reward, next_state, done = env.step(action)
            score += reward
            next_state = np.reshape(next_state, (1, 5))
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if train==True:
                agent.replay()
            if done:
                print("episode: {}/{}, score: {}".format(e, ep, score))
                break
        loss.append(score)
    if train:
        agent.model.save_weights("PongGame.h5")
    return loss

if __name__=='__main__':
    mode=int(input("Please Enter the mode 0 for testing 1 for training "))
    if mode ==0:
        trainflag=False
        ep=100
    elif mode ==1:
        trainflag = True   
        ep = 2000
    loss = run(ep,trainflag)
    # plt.plot([i for i in range(ep)], loss)
    # plt.xlabel('episodes')
    # plt.ylabel('reward')
    # plt.show()