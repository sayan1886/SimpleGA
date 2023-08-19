import random
from gaengine.gaengine import GAEngine
from chromosome.sphere import Sphere

class SphereGAEngine(GAEngine):
    
    def __init__(self, gaConfig, n_gene) -> None:
        super().__init__(gaConfig)
        self.n_gene = n_gene

    def __str__(self):
        init_population = ''.join(str(x) for x in self.init_populations)
        populations = ''.join(str(x) for x in self.populations)
        return '''toatl_population: {0}
generations:{1}
initial populations: {2}\n
current population: {3}'''.format(
            self.totalPopulation, self.generations, 
            init_population, populations)

    # create initial population
    def make_initial_population(self):       
        for i in range(self.gaConfig.n_populations):
            self.populations.append(Sphere(gaConfig=self.gaConfig, 
                                    n_gene=self.n_gene))
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
            next_gen.append(Sphere(self.gaConfig, 
                            population[i], self.n_gene))
        self.next_gen = next_gen.copy()
        
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
            parent1_chromosome = Sphere(self.gaConfig, parent1, self.n_gene)
            parent2_chromosome = Sphere(self.gaConfig, parent2, self.n_gene)
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
            self.next_gen[random_index] = Sphere(self.gaConfig,
                                        chromosome.mutate(), self.n_gene)