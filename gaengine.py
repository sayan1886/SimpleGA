from random import uniform
import random
from chromosome import Chromosome

class GAEngine:
    def __init__(self, gaConfig) -> None:
        self.populations: list[Chromosome] = []
        self.init_populations: list[Chromosome] = []
        self.next_gen: list[Chromosome] = []
        self.generations = 0
        self.gaConfig = gaConfig
        self.totalPopulation = self.gaConfig.n_populations

    def __str__(self):
        init_population = ' '.join(str(x) for x in self.init_populations)
        populations = ' '.join(str(x) for x in self.populations)
        return '''toatl_population: {0}
generations:{1}
initial populations: {2}\n
current population: {3}'''.format(
            self.totalPopulation, self.generations, 
            init_population, populations)
        
    def get_population(self):
        return self.population
    
    def get_current_generation(self):
        return self.generations
    
    def average_fitness(self):
        fitness_list = [c.fitness() for c in self.populations]
        return (sum(fitness_list) / self.gaConfig.n_populations)
    
    def best_finess(self): 
        fitness = 0 
        for i in range(self.gaConfig.n_populations):
            if fitness < self.populations[i].fitness():
                fitness = self.populations[i].fitness()
        return fitness
    
    def create_elite_group(self):
        # sort the solutions in descending order of fitness
        current_generation = sorted(self.populations, key=lambda x: x.fitness(), 
                                    reverse=True)
        n_elite_generation = int(self.gaConfig.n_populations * 
                                 self.gaConfig.elitism.capacity)
        elite_generation = []
        for i in range(n_elite_generation):
            elite_generation.append(current_generation[i])
        return elite_generation
    
    # breed next generation
    def next_generation(self, population):
        next_gen = []
        n_elite_generation = 0 
        if self.gaConfig.elitism:
            n_elite_generation = int(self.gaConfig.n_populations * 
                                 self.gaConfig.elitism.capacity)
            next_gen = self.create_elite_group().copy()
        if len(population) < self.gaConfig.n_populations - n_elite_generation:
            print("invalid next generation")
            exit()
        for i in range (self.gaConfig.n_populations - n_elite_generation):
            next_gen.append(Chromosome(self.gaConfig, population[i]))
        self.next_gen = next_gen.copy()
        
    def change_genration(self):
        self.generations += 1
        self.populations = self.next_gen.copy()
        self.next_gen.clear()
    
    def make_initial_population(self):       
        for i in range(self.gaConfig.n_populations):
            self.populations.append(
                Chromosome(self.gaConfig))
            self.init_populations = self.populations.copy()
            
    # ga selection implementation
    def do_selection(self):
        mating_pool = None
        if (self.gaConfig.selection.type == "tournament"):
            mating_pool = self.__tournament_selection__()
        elif (self.gaConfig.selection.type == "roulette_wheel"):
            mating_pool = self.__roulte_wheel_selection__().copy()
        else:
            print("invalid selection strategy")
            exit()
        return mating_pool
    
    def __roulte_wheel_selection__(self):
        mating_pool = []
        # sort the solutions in descending order of fitness
        current_generation = sorted(self.populations, key=lambda x: x.fitness(), 
                                    reverse=True)
        # sum of the fitness score
        fitness_sum = self.__calculate_fitness_sum__(current_generation)
        fitness_score = []
        for i in range (len(self.populations)):
            fitness_score.append(current_generation[i].fitness())
        
        # generate weighted probabilty 
        probabilities = [round((float)(value)/fitness_sum,4) for value in fitness_score]
        while (len(mating_pool) < self.gaConfig.n_populations):
            randomNumber = round(uniform(0, 1),3)
            cumulativeprobability = [probabilities[0]]
            for i in probabilities[1:]:
                cumulativeprobability.append(round(probabilities[i] + 
                                                   cumulativeprobability[-1] , 2))
            choose = 0
            for i in probabilities:
                choose = choose + probabilities[i]
                if choose <= randomNumber:
                    mating_pool.append(current_generation[i].chromosomes)
        return mating_pool
    
    def __calculate_fitness_sum__(self, current_generation):
        sum = 0
        for i in range(len(current_generation)):
            sum += current_generation[i].fitness()
        return sum
    
    def __tournament_selection__(self):
        mating_pool = []
        while (len(mating_pool) < self.gaConfig.n_populations):
            fittest_chromosome = None
            fitness_score = 0.0
            for i in range (self.gaConfig.selection.size):
                selected_index = random.randint(0, (self.gaConfig.n_populations - 1))
                selected_chromosome_fitness = self.populations[selected_index].fitness()
                if (fitness_score <= selected_chromosome_fitness):
                    fitness_score = selected_chromosome_fitness
                    fittest_chromosome = self.populations[selected_index]
            mating_pool.append(fittest_chromosome.chromosomes)
        return mating_pool
    
    def do_crossover(self, mating_pool):
        # Get top fittest
        no_of_crossover = int(self.gaConfig.n_populations * 
                              self.gaConfig.crossover_chances)
        no_elite = 0
        if self.gaConfig.elitism:
            no_elite = int(self.gaConfig.n_populations * 
                                 self.gaConfig.elitism.capacity)
            
        # move chromosome to next generation intact for mutation
        keep_next = self.gaConfig.n_populations - no_of_crossover - no_elite
        # sort the solutions in descending order of fitness
        current_generation = sorted(self.populations, key=lambda x: x.fitness(), 
                                    reverse=True)
        next_generation = []
        for i in range (keep_next):
            next_generation.append(current_generation[i].chromosomes)
        for i in range (no_of_crossover):
            parent1, parent2 = random.choices(mating_pool, k=2)
            parent1_chromosome = Chromosome(self.gaConfig, parent1)
            parent2_chromosome = Chromosome(self.gaConfig, parent2)
            next_generation.append(parent1_chromosome.crossover(parent2_chromosome))
        return next_generation
    
    def do_mutation(self):
        no_of_mutation = int(self.gaConfig.n_populations * 
                              self.gaConfig.mutation_chances)
        for i in range (no_of_mutation):
            random_index = random.randint(0, self.gaConfig.n_populations -  1)
            chromosome = self.next_gen[random_index]
            self.next_gen[random_index] = Chromosome(self.gaConfig, chromosome.mutate())