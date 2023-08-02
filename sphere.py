import random
from gaengine import GAEngine
from complex_chromosome import ComplexChromosome

# benchmark problem on spehre
# Sphere => f(x) = sumation ( {i=1  to p} x_i^2 )
# x_i in [-5.12, 5.12]				
# x^* = (0,0,...,0); f(x^*) = 0
class Sphere(ComplexChromosome):
    
        def __init__(self, gaConfig, chromosomes=[], n_gene=3) -> None:
             super().__init__(gaConfig, chromosomes, n_gene)
             
        # calculate fitness for the degree of goodness of the encoded solution
        # fitness will be based on the equation f{x} = sum_of {i=1-p} x_i^2
        # where p is no of dimension we set it to number of gene
        def __evaluate_fitness__(self):
            sum = 0
            for i in range(self.n_gene):
                x_i = self.corresponding_value[i]
                sum += x_i ** 2
            return sum

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