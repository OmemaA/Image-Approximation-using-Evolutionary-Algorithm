import math, random
from random import randint
from copy import deepcopy
import matplotlib.pyplot as plt


# Base class
class EvolutionaryAlgorithm:
    def __init__(self):
        self.popSize = 30
        self.offsprings = 10
        self.generations = 100
        self.mutationRate = 0.5
        self.iterations = 10
        self.fitness = None
        self.generations_score = [[] for _ in range(self.generations)]

    # Dummy functions defined in child classes acc to each problem
    def initialPopulation(self):
        return [[] for _ in range(self.popSize)]

    def computeFitness(self, path):
        return 0

    def mutation(self, chromosomes):
        return chromosomes

    def crossover(self, parent1, parent2):
        return parent1, parent2

    # EA cycle
    def cycle(self, maximise):
        iters = []
        for _ in range(self.iterations):
            generations = 0
            chromosomes = self.initialPopulation() 
            # compute fitness of each individual in population
            self.fitness = [self.computeFitness(indv) for indv in chromosomes]
            scores = []
            while generations < self.generations:
                # Saving image after every 250 generations
                # if generations % 250 == 0:
                #     print('Generation', generations+1)
                #     for x in chromosomes:
                #         fit = min([self.computeFitness(i) for i in chromosomes])
                #         if self.computeFitness(x) == fit:
                #             x.img.save('MonaLisa'+str(generations)+'.png', 'PNG')
                #             print("Fitness:", fit)
                #             break
                for _ in range(self.offsprings//2):
                    # parent selection
                    parents = self.random(chromosomes, 2)
                    parent1, parent2 = parents[0], parents[1]
                    # cross over
                    offspring1, offspring2  = self.crossover(parent1, parent2)
                    # add new offsprings to population
                    chromosomes.append(offspring1)
                    chromosomes.append(offspring2)
                    # compute fitness of new offsprings
                    self.fitness.append(self.computeFitness(offspring1))
                    self.fitness.append(self.computeFitness(offspring2))
                    # mutation
                    if random.random() < self.mutationRate:
                        chromosomes = self.mutation(chromosomes)
                # survivor selection
                chromosomes = self.truncation(chromosomes,maximise,self.popSize)
                # compute fitness of each individual in population
                self.fitness = [self.computeFitness(indv) for indv in chromosomes]
                if maximise: BFS = max(self.fitness)
                else: BFS = min(self.fitness)
                scores.append((BFS, sum(self.fitness)/len(self.fitness)))
                generations +=1
            iters.append(scores)
        gen = 0
        # calculates average BFS and average AFS
        while gen < self.generations:
            best, avg = 0, 0
            for val in iters:
                best += val[gen][0]
                avg += val[gen][1]
            best = best / len(iters)
            avg = avg / len(iters)
            self.generations_score[gen].append((best,avg))
            gen +=1 
        self.plot_graph()


    def plot_graph(self):
        BFS = [i[0][0] for i in self.generations_score]
        AFS = [i[0][1] for i in self.generations_score]
        generations = [i+1 for i in range(self.generations)]
        plt.plot(generations, BFS, label="Avg best-so-far Fitness")
        plt.plot(generations, AFS, label="Avg average-so-far Fitness")
        plt.title("Random and Truncation")
        plt.xlabel('No. of generations')
        plt.ylabel('Fitness value')
        plt.legend()
        plt.show()
        

    # Selection procedures
    def FPS(self, chromosomes, maximise, size):
        # total fitness
        total = sum([val for val in self.fitness])
        # calculates ranges for chromosomes
        proportion = [val/total for val in self.fitness]
        # calculates cumulative probabilities
        prev_prob = 0
        probabilities = []
        for i in range(len(proportion)):
            prev_prob = prev_prob+proportion[i]
            probabilities.append(prev_prob)
        selected = []
        for _ in range(size):
            # selects two random numbers and chooses parents based on given range
            rand_no = random.random()
            for i in range(len(chromosomes)):
                if rand_no <= probabilities[i]:
                    selected.append(chromosomes[i])
                    break
        return selected

    def RBS(self, chromosomes, maximise, size):
        # assigns a rank to each chromosome acc to its fitness value
        ranks = list(range(len(self.fitness)))
        ranks.sort(key=lambda x: self.fitness[x])
        ranked_list = [0] * len(ranks)
        for i, x in enumerate(ranks):
            ranked_list[x] = i
        # total ranks
        total = sum([val for val in ranks])
        # calculates ranges for chromosomes
        proportion = [val/total for val in ranks]
        # calculates cumulative probabilities
        prev_prob = 0
        probabilities = []
        for i in range(len(proportion)):
            prev_prob = prev_prob+proportion[i]
            probabilities.append(prev_prob)
        selected = []
        for _ in range(size):
            # selects two random numbers and chooses chromosomes based on given range
            rand_no = random.random()
            for i in range(len(chromosomes)):
                if rand_no <= probabilities[i]:
                    selected.append(chromosomes[i])
                    break
        return selected
        

    def BT(self, chromosomes, maximise, size):
        selected = []
        if maximise:
            for _ in range(size):
                # randomly select two individuals
                rand = random.sample(range(0,len(chromosomes)), 2)
                # choose one with higher fitness value
                if self.fitness[rand[0]] > self.fitness[rand[1]]:
                    selected.append(chromosomes[rand[0]])
                selected.append(chromosomes[rand[1]])
        else:
            for _ in range(size):
                # randomly select two individuals
                rand = random.sample(range(0,len(chromosomes)), 2)
                # choose one with lower fitness value
                if self.fitness[rand[0]] < self.fitness[rand[1]]:
                    selected.append(chromosomes[rand[0]])
                selected.append(chromosomes[rand[1]])
        return selected
        

    def truncation(self, chromosomes, maximise, size):
        indexes = [(self.fitness[i], i) for i in range(len(self.fitness))]
        # sorts list accoridng to fitness
        indexes.sort(key = lambda x: x[0], reverse=maximise)
        indexes = indexes[:size]
        # selects top N elements 
        top_N = [chromosomes[i[1]] for i in indexes]
        return top_N

    def random(self, chromosomes, size):
        # randomly selects chromosomes from population
        return random.sample(chromosomes, size)

