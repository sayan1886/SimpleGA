from random import uniform
import random
from chromosome import Chromosome

class GAEngine:
    def __init__(self, gaConfig) -> None:
        self.populations: list[Chromosome] = []
        self.init_populations: list[Chromosome] = []
        self.next_gen: list[Chromosome] = []
        self.elite_group : list[Chromosome] = []
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
    
    def get_elite_population(self):
        return len(self.elite_group)
    
    def average_fitness(self):
        fitness_list = [c.fitness() for c in self.populations]
        return (sum(fitness_list) / self.gaConfig.n_populations)
    
    def __fittest_chromosome__(self):
        fittest = max(self.populations, key=lambda x: x.fitness())
        return fittest
    
    def __fittest_chromosome_in__(self, population):
        fittest = max(population, key=lambda x: x.fitness())
        return fittest
    
    def __weakest_chromosome__(self):
        weakest = min(self.populations, key=lambda x: x.fitness())
        return weakest
    
    def __weakest_chromosome_in__(self, population):
        weakest = min(population, key=lambda x: x.fitness())
        return weakest
            
    def best_finess(self): 
        fittest = self.__fittest_chromosome__()
        return fittest.fitness()
    
    def __create_elite_group__(self):
        # check if elite grouping required
        if self.gaConfig.elitism:
            # sort the solutions in descending order of fitness
            current_generation = sorted(self.populations, key=lambda x: x.fitness(), 
                                        reverse=True)
            n_elite_generation = int(self.gaConfig.n_populations * 
                                    self.gaConfig.elitism.capacity)
            elite_generation = []
            for i in range(n_elite_generation):
                elite_generation.append(current_generation[i])
            self.elite_group = elite_generation.copy()
        else:
            self.elite_group = []
        
    # create initial population
    def make_initial_population(self):       
        for i in range(self.gaConfig.n_populations):
            self.populations.append(
                Chromosome(self.gaConfig))
            self.init_populations = self.populations.copy()
        # create elite populations if any
        self.__create_elite_group__()
    
    # breed next generation
    def next_generation(self, population):
        next_gen = []
        # check for valid next gen
        if len(population) < self.gaConfig.n_populations:
            print("invalid next generation")
            exit()
        for i in range (self.gaConfig.n_populations):
            next_gen.append(Chromosome(self.gaConfig, population[i]))
        self.next_gen = next_gen.copy()
        
    def __elite_selection__(self):
        elites = self.elite_group
        # compare elite and next gen
        for i in range(len(elites)):
            chromosome_worst = sorted(self.next_gen, key=lambda x: x.fitness(), 
                                    reverse=False)
            # check elite generation is superior than next gen
            for j in range(len(chromosome_worst)):
                # found a spot for inserting elite gen and remove next gen member
                if chromosome_worst[j].fitness() < elites[i].fitness():
                    # elite gen is superior than any chromosome in next gen
                    # remove weakest and add chromosome for elite gen
                    weakest_chromosome = self.__weakest_chromosome_in__(self.next_gen)
                    index = self.next_gen.index(weakest_chromosome)
                    self.next_gen[index] = elites[i]
                    break
                # next gen is superior than elite chromosome
                else:
                    print("next gen supeior than elite")

            
        
    # set next generation as current generation
    def change_genration(self):
        self.generations += 1
        self.populations.clear()
        self.__elite_selection__()
        self.populations = self.next_gen.copy()
        self.next_gen.clear()
        self.elite_group.clear()
            
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
    
    # roulette wheel selction
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
        while (len(mating_pool) < (self.gaConfig.n_populations)):
            randomNumber = round(uniform(0, 1),3)
            cumulativeprobability = [probabilities[0]]
            i = 1
            for i in range(len(probabilities[1:])):
                cumulativeprobability.append(round(probabilities[i] + 
                                                   cumulativeprobability[-1] , 2))
            choose = 0
            for i in range(len(probabilities)):
                choose = choose + probabilities[i]
                if choose <= randomNumber:
                    mating_pool.append(current_generation[i].chromosomes)
        return mating_pool
    
    def __calculate_fitness_sum__(self, current_generation):
        sum = 0
        for i in range(len(current_generation)):
            sum += current_generation[i].fitness()
        return sum
    
    # tournament selection
    def __tournament_selection__(self):
        mating_pool = []
        while (len(mating_pool) < (self.gaConfig.n_populations)):
            fittest_chromosome = None
            fitness_score = -999999999999999 
            for i in range (self.gaConfig.selection.size):
                selected_index = random.randint(0, (self.gaConfig.n_populations - 1))
                selected_chromosome_fitness = self.populations[selected_index].fitness()
                if (fitness_score <= selected_chromosome_fitness):
                    fitness_score = selected_chromosome_fitness
                    fittest_chromosome = self.populations[selected_index]
                    
            mating_pool.append(fittest_chromosome.chromosomes)
        return mating_pool
    
    # crossover using mating pool and fill next generation
    def do_crossover(self, mating_pool):     
        # get total population except elits
        population = self.gaConfig.n_populations
        # Get no of crossover required 
        no_of_crossover = int(population * self.gaConfig.crossover_chances)
            
        # get top fittest chromosome to next generation intact for mutation
        keep_next = population - no_of_crossover
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
    
    # implemnet mutation on next generation breeds 
    def do_mutation(self):
        # get elite group count if any
        no_elite = self.get_elite_population()
        # get total population except elits
        population = int(self.gaConfig.n_populations - no_elite)
        
        no_of_mutation = int(population * self.gaConfig.mutation_chances)
        # mutate only chromosome we got from mating pool
        for i in range (no_of_mutation):
            random_index = random.randint(0, population -  1)
            chromosome = self.next_gen[random_index]
            self.next_gen[random_index] = Chromosome(self.gaConfig, chromosome.mutate())