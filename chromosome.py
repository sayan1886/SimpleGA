import math
import random
from abc import ABC, abstractproperty, abstractmethod

class Fitness(ABC):
    @abstractmethod
    def __evaluate_fitness__(self):
        '''evaluate the fitness for current chromosome/offspring'''

    @abstractproperty
    def fitness(self):
        '''fitness score for current chromosome/offspring'''

class Chromosome(Fitness):
    # initialize a new chromozome with 
    # chromosome length 
    # chromosome array of binary string only applicable for 
    # crossover and mutation where we have chromosoem alreay 
    # defined otherwise it will be blank __init__ will populate for 
    # initial population
    def __init__(self, gaConfig, chromosomes = []) -> None:
        super.__init__
        self.gaConfig = gaConfig
        if (len(chromosomes) == 0):
            chromosomes = self.__generate_random_chromosome__()
        self.chromosomes = chromosomes.copy()
        encoded_chromosome = self.__encode_chromosome__()
        self.encoded_chromosome = encoded_chromosome
        self.corresponding_value = self.__corresponding_value__()
    
    # genarate a randome chromosome
    def __generate_random_chromosome__(self):
        chromosome = [0] * self.gaConfig.n_chromosomes
        for i in range(self.gaConfig.n_chromosomes):
            chromosome[i] = random.randint(0,1)
        return chromosome
    
        
    # encode chromosome(bianry string array) to integaer value
    def __encode_chromosome__(self):
        # convert binary list to string
        binary_string = ''.join(map(str, self.chromosomes))
        # convert binary string to integer
        encoded_chromosome = int(binary_string, 2) 
        return encoded_chromosome
        
    # decode  integaer value to chromosome(bianry string array)
    def __decode_chromosome__(self, encoded_chromosome):
        # convert to binary string
        binary_string = '{0:0b}'.format(encoded_chromosome)
        # fill with zero(s) to maintain the chromosome length
        binary_string = binary_string.zfill(self.gaConfig.n_chromosomes)
        decoded_chromosome = [0] * len(self.gaConfig.n_chromosomes)
        for i in range (0, len(binary_string)):
            decoded_chromosome[i] = int(self.gaConfig.n_chromosomes[i], 2)
        return decoded_chromosome
    
    # calcualate x using 
    # x = min_boundary + max_boundary/(2^n_chromosome - 1) * encoded_chromosome
    # y = y_min + (y_max - y_min) / x_max - x_min * (x - x_min)
    def __corresponding_value__(self):
        corresponding_value = ( int(self.gaConfig.boundary.min) + 
        ( float(self.gaConfig.boundary.max) / 
         ( 2 ** float(self.gaConfig.n_chromosomes) - 1 ) ) 
        * int(self.encoded_chromosome))
        return corresponding_value
            
    def __str__(self):
        chromosome = ''.join(str(x) for x in self.chromosomes)
        return '''
chromosome:             {0} 
encoded_chromosome:     {1}
corresponding_value:    {2}'''.format(
            chromosome, self.encoded_chromosome, self.corresponding_value)
                
    # mutate the individual
    def mutate(self):
        mutate_chromosome = None
        if (self.gaConfig.mutation.type == "bit-flip"):
            mutate_chromosome = self.__bit_flip_mutation__()
        elif (self.gaConfig.mutation.type == "swap"):
            if (self.gaConfig.mutation.bits % 2 == 0):
                mutate_chromosome = self.__bit_swap_mutation__()
            else:
                print("invalid bit size for mutation")
                exit()
        else:
            print("invalid mutation type")
            exit()
        return mutate_chromosome
    
    def __bit_flip_mutation__(self):
        offspring = self.chromosomes.copy()
        flip_positions = [0] * self.gaConfig.mutation.bits
        for i in range(self.gaConfig.mutation.bits):
            flip_positions[i] = random.randint(0, self.gaConfig.n_chromosomes - 1)
        for i in range(len(flip_positions)):
            bit = offspring[flip_positions[i]]
            if bit == 0:
                offspring[flip_positions[i]] = 1
            else:
                offspring[flip_positions[i]] = 0
        return offspring
        
    # bits must be even for swaping
    def __bit_swap_mutation__(self):
        offspring = self.chromosomes.copy()
        swap_positions = [0] * self.gaConfig.mutation.bits
        for i in range(self.gaConfig.mutation.bits):
            swap_positions[i] = random.randint(0, self.gaConfig.n_chromosomes - 1)
        i = 0
        while i < len(swap_positions):
            bit = offspring[swap_positions[i]]
            offspring[swap_positions[i]] = offspring[swap_positions[i+1]]
            offspring[swap_positions[i+1]] = bit
            i = i + 2
        return offspring
    
    # produce a new offspring from 2 parents
    def crossover(self, other):
        offspring = None
        if (self.gaConfig.crossover_type == "single"):
            offspring = self.__single_point_crossover__(other)
        elif (self.gaConfig.selection == "uniform"):
            offspring = self.__uniform_crossover__(other)
        else:
            print("invalid crossover type")
            exit()
        return offspring
    
    # cross over to creat one offspring from twp parents 
    # using single point crossover return two new offsprings 
    def __single_point_crossover__(self, other):
        offspring_1 = [0] * self.gaConfig.n_chromosomes
        # offspring_2 = [0] * self.gaConfig.n_chromosomes
        crossover_point = random.randint(0, self.gaConfig.n_chromosomes - 1)
        for i in range(self.gaConfig.n_chromosomes):
            if (i <= crossover_point):
                offspring_1[i] = self.chromosomes[i]
                # offspring_2[i] = other[i]
            else:
                offspring_1[i] = other.chromosomes[i]
                # offspring_2[i] = other.chromosomes[i]
        return offspring_1 #, offspring_2
    
    # cross over to creat one offspring from twp parents 
    # using single point crossover
    # create a random mask and based on mask[i] value will be
    #will consider single offspring from parent
    def __uniform_crossover__(self, other):
        offspring_1 = [0] * self.gaConfig.n_chromosomes
        # offspring_2 = [0] * self.gaConfig.n_chromosomes
        mask = self.__generate_random_chromosome__()
        for i in range(self.gaConfig.n_chromosomes):
            if (mask[i] == 0):
                offspring_1[i] = self.chromosomes[i]
                # offspring_2[i] = other.chromosomes[i]
            else:
                offspring_1[i] = other.chromosomes[i]
                # offspring_2[i] = self.chromosomes[i]
        return offspring_1 #, offspring_2
    
    # calculate fitness for the degree of goodness of the encoded solution
    # fitness will be based on the equation f(x) = x(8 – x)
    def __evaluate_fitness__(self):
        # return self.corresponding_value * (8 - self.corresponding_value)
        if (self.corresponding_value == 0):
            return 0
        return math.sin(self.corresponding_value) / self.corresponding_value
    
    # get fitness 
    def fitness(self):
        return self.__evaluate_fitness__()