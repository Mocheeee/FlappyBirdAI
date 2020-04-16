import numpy as np
import pygame
import random
import pickle
pygame.init()
pygame.font.init()
from configs import *
from constants import *
from Flappy_bird import Bird, draw_window, Base, Pipe
from NeuralNetwork import NeuralNetModel
from ga import *

bird = Bird(230, 350)
net = pickle.load(open('best_net.sav', 'rb'))
bird.brain = net
score = 0
base = Base(730)
pipes = [Pipe(700)]
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
run = True 


while run:
    # clock.tick(30)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

    bird.move()
    
    rem =[]
    add_pipe = False

    for pipe in pipes:
        if pipe.collide(bird):
            run = False
            print(score)
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            rem.append(pipe)

        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True

        pipe.move()

    if add_pipe:
        score +=1
        pipes.append(Pipe(700))

    for r in rem:
        pipes.remove(r)
    base.move()   

    pipe_ind = 0
    if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
        pipe_ind = 1
    is_jump = bird.brain.predict(np.array([[bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)]]))
    if is_jump > 0.5:
        bird.jump()

    if bird.y < 0 or bird.y > base.y-bird.img.get_height():
        run = False
        print(score)

    draw_window(WIN, [bird], pipes, base, score, 1, 1)

pygame.quit()
