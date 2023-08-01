from gaengine import GAEngine
from complex_chromosome import ComplexChromosome

class ComplexGAEngine(GAEngine):
    
    def __init__(self, gaConfig) -> None:
        super().__init__(gaConfig)

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
            self.populations.append(ComplexChromosome(gaConfig=self.gaConfig))
            self.init_populations = self.populations.copy()
        # create elite populations if any
        self.__create_elite_group__()