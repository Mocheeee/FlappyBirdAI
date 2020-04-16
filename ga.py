import numpy as np

def calculate_fitness(population):
    sum_distance = 0
    for chormosome in population:
        sum_distance += chormosome.distance
    
    for i, chormosome in enumerate(population):
        population[i].fitness = chormosome.distance / sum_distance
    
    return population

def mating_pool(population, size_pool = 100):
    pool = []
    for chormosome in population:
        fitness = round(chormosome.fitness * size_pool)
        for _ in range(fitness):
            pool.append(chormosome)
    
    return pool

def next_genergation(population, mutate_rate=0.01, size_pool = 100):
    pool = mating_pool(population, size_pool)
    next_gen = []
    
    for _ in range(len(population)):
        chormosome = pool[np.random.randint(0, len(pool))]
        chormosome.brain.mutate(mutate_rate)
        next_gen.append(chormosome)
    
    return next_gen
        

