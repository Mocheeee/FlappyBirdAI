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

# bird = Bird(230, 350)
score = 0
base = Base(730)
pipes = [Pipe(700)]
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
run = True 
gen = 0

birds = [Bird(230, 350) for _ in range(POPULATION_SIZE)]
for i, bird in enumerate(birds):
    birds[i].brain = NeuralNetModel(input_shape= (3,))

genomes = []
best_fitness = None

while run:
    # clock.tick(30)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    for bird in birds:
        bird.move()
        bird.distance += 1
    
    rem =[]
    add_pipe = False
    rm_bird = []

    for pipe in pipes:
        for bird in birds:
            if pipe.collide(bird):
                genomes.append(bird)
                rm_bird.append(bird)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
        
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            rem.append(pipe)

        pipe.move()

    if add_pipe:
        for i, _ in enumerate(birds):
            birds[i].score += 1
        score +=1
        pipes.append(Pipe(700))

    for r in rem:
        pipes.remove(r)
    base.move()   

    pipe_ind = 0
    if len(birds) > 0:
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
            pipe_ind = 1  

    for i, bird in enumerate(birds):
        if bird.y < 0 or bird.y > base.y-bird.img.get_height():
            rm_bird.append(bird)
            genomes.append(bird)
        is_jump = bird.brain.predict(np.array([[bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)]]))
        if is_jump > 0.5:
            birds[i].jump()

    for bird in rm_bird:
        birds.remove(bird)

    
    if len(birds) == 0:
        # run = False
        gen +=1
        print(f'gen: {gen}----score: {score} ----Distance: {max([bird.distance for _ in genomes])}')
        genomes = calculate_fitness(genomes)
        next_gen = next_genergation(genomes,MUTATE_RATE, POOL_SIZE)
        birds = []
        for bird in next_gen:
            new_bird = Bird(230, 350)
            new_bird.brain = bird.brain
            birds.append(new_bird)
        # Setting defaul
        score = 0
        base = Base(730)
        pipes = [Pipe(700)]
        WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        genomes=[]

    if score >= MAX_SCORE:
        run = False
        #  Save best net
        best_distance = 0
        best_net = None
        for bird in birds:
            if bird.distance > best_distance:
                best_distance = bird.distance
                best_net = bird.brain
        print(f'alive: {len(birds)}')    
        pickle.dump(best_net, open('best_net.sav', 'wb'))

    if gen >= MAX_GENERATIONS:
        run = False
        #  Save best net
        best_distance = 0
        best_net = None
        for bird in birds:
            if bird.distance > best_distance:
                best_distance = bird.distance
                best_net = bird.brain
        
        pickle.dump(best_net, open('best_net.sav', 'wb'))
        print(f'best score: {score}')

    draw_window(WIN, birds, pipes, base, score, gen, len(birds))

pygame.quit()
