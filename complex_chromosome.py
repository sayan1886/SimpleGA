from chromosome import Chromosome
import random

# complex chromosome structure where gene represnts a single unit of bianry 
# string encoded to integer value and chromosome will contain n numebr of genes. 
# n_gene will decide the number gene can be store inside chromosome
class ComplexChromosome(Chromosome):
    
    def __init__(self, gaConfig, chromosomes=[], n_gene=3) -> None:
        self.n_gene = n_gene
        self.gaConfig = gaConfig
        if (len(chromosomes) == 0):
            chromosomes = self.__generate_random_chromosome__()
        self.chromosomes = chromosomes.copy()
        encoded_chromosome = self.__encode_chromosome__()
        self.encoded_chromosome = encoded_chromosome.copy()
        self.corresponding_value = self.__corresponding_value__()
        
    def __str__(self):
        chromosome = []
        for i in range(self.n_gene):
            gene = ''.join(str(x) for x in self.chromosomes[i])
            chromosome.append(gene)
            
        return '''
chromosome:             {0} 
encoded_chromosome:     {1}
corresponding_value:    {2}'''.format(
            chromosome, self.encoded_chromosome, self.corresponding_value)
        
    # genarate a randome chromosome with number of gene
    def __generate_random_chromosome__(self):
        chromosome = [0] * self.n_gene
        for i in range(self.n_gene):
            chromosome[i] = self.__generate_random_gene__().copy()
        return chromosome
        
    # genarate a randome gene main unit of chromosome
    def __generate_random_gene__(self):
        gene = [0] * self.gaConfig.n_chromosomes
        for i in range(self.gaConfig.n_chromosomes):
            gene[i] = random.randint(0,1)
        return gene
    
    # encode chromosome will return array of integer 
    # where each integer denote a enocded gene
    def __encode_chromosome__(self):
        # array of integer represent encoded genes 
        # converted from binary string array or gene
        encoded_chromosome = [0] * self.n_gene
        for i in range(self.n_gene):
            encoded_chromosome[i] = self.__encode_gene__(self.chromosomes[i])
        return encoded_chromosome
    
    # encode gene(binary string array) to integer value
    def __encode_gene__(self, gene):
        # convert binary list to string
        binary_string = ''.join(map(str, gene))
        # convert binary string to integer
        encoded_gene = int(binary_string, 2) 
        return encoded_gene
    
    # decode integer value to gene(binary string array)
    def __decode_chromosome__(self, encoded_chromosome):
        # array of integer represent encoded genes 
        # and decode will covert then into binary string array represents single gene
        decoded_chromosome = [0] * self.n_gene
        for i in range(self.n_gene):
            decoded_chromosome[i] = self.__decode_gene__(encoded_chromosome[i]).copy()
        return decoded_chromosome
    
    # decode integer value to gene(binary string array)
    def __decode_gene__(self, encoded_gene):
        # convert to binary string
        binary_string = '{0:0b}'.format(encoded_gene)
        # fill with zero(s) to maintain the chromosome length
        binary_string = binary_string.zfill(self.gaConfig.n_chromosomes)
        decoded_chromosome = [0] * len(self.gaConfig.n_chromosomes)
        for i in range (0, len(binary_string)):
            decoded_chromosome[i] = int(self.gaConfig.n_chromosomes[i], 2)
        return decoded_chromosome
    
    # evaluate corresponding chormosome value 
    def __corresponding_value__(self):
        # array of integer represent encoded genes
        encoded_chromosome = self.__encode_chromosome__()
        corresponding_value = [0] * self.n_gene
        for i in range(self.n_gene):
            corresponding_value[i] = self.__corresponding_gene_value__(
                                        encoded_chromosome[i])
        return corresponding_value
    
    # calcualate corresponfing gene value using interpolation
    # where y_min = config.bounday.min y_max = config.bounday.min
    # x_max = 2^chormosomeLength - 1 and x_min = 0
    # x will encoded gene value
    # y = y_min + (y_max - y_min) / (x_max - x_min) * (x - x_min)
    def __corresponding_gene_value__(self, encoded_gene):
        # corresponding_value = ( int(self.gaConfig.boundary.min) + 
        corresponding_value = (self.gaConfig.boundary.min + 
                        ((self.gaConfig.boundary.max - self.gaConfig.boundary.min) / 
                        (2 ** self.gaConfig.n_chromosomes - 1) - 0) * 
                        (encoded_gene - self.gaConfig.boundary.min))
        return corresponding_value
    
    # cross over to creat one offspring from two parents 
    # using single point crossover return new offspring(s) 
    # will consider to breed single offspring gene from parent gene
    def __single_point_crossover__(self, other):
        offspring_1 = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring_1[i] = self.__single_point_gene_crossover__(
                self_gene=self.chromosomes[i], other_gene=other.chromosomes[i])
        return offspring_1
    
    # crossover to creat one offspring gene from two parent gene
    # using single point crossover return new offspring(s) gene
    def __single_point_gene_crossover__(self,self_gene, other_gene):
        offspring_1 = [0] * self.gaConfig.n_chromosomes
        # offspring_2 = [0] * self.gaConfig.n_chromosomes
        crossover_point = random.randint(0, self.gaConfig.n_chromosomes - 1)
        for i in range(self.gaConfig.n_chromosomes):
            if (i <= crossover_point):
                offspring_1[i] = self_gene[i]
                # offspring_2[i] = other[i]
            else:
                offspring_1[i] = other_gene[i]
                # offspring_2[i] = other.chromosomes[i]
        return offspring_1 #, offspring_2
    
    # crossover to creat one offspring from two parents using uniform crossover
    # create a random mask and based on mask[i] value will be
    # will consider to breed single offspring from parent
    def __uniform_crossover__(self, other):
        offspring_1 = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring_1[i] = self.__uniform_gene_crossover__(
                self_gene=self.chromosomes[i], other_gene=other.chromosomes[i])
        return offspring_1
    
    # crossover to creat one offspring from two parents using uniform crossover
    # create a random mask and based on mask[i] value will be
    # will consider to breed single offspring gene from parent gene
    def __uniform_gene_crossover__(self,self_gene, other_gene):
        offspring_1 = [0] * self.gaConfig.n_chromosomes
        # offspring_2 = [0] * self.gaConfig.n_chromosomes
        mask = self.__generate_random_gene__()
        for i in range(self.gaConfig.n_chromosomes):
            if (mask[i] == 0):
                offspring_1[i] = self_gene[i]
                # offspring_2[i] = other.chromosomes[i]
            else:
                offspring_1[i] = other_gene[i]
                # offspring_2[i] = self.chromosomes[i]
        return offspring_1 #, offspring_2
    
    # bit flip mutation 
    def __bit_flip_mutation__(self):
        offspring = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring[i] = self.__bit_flip_gene_mutation__(self.chromosomes[i])
        return offspring
    
    # bit flip mutation done by choosing random position of gene
    # and fliping the bit
    def __bit_flip_gene_mutation__(self, gene):
        offspring = gene.copy()
        flip_positions = [0] * self.gaConfig.mutation.bits
        for i in range(self.gaConfig.mutation.bits):
            flip_positions[i] = random.randint(0, self.gaConfig.n_chromosomes - 1)
        for i in range(len(flip_positions)):
            pos = flip_positions[i]
            bit = offspring[pos]
            if bit == 0:
                offspring[pos] = 1
            else:
                offspring[pos] = 0
        return offspring
    
    # bit flip mutation 
    def __bit_swap_mutation__(self):
        offspring = [0] * self.n_gene
        for i in range(self.n_gene):
            offspring[i] = self.__bit_swap_gene_mutation__(self.chromosomes[i])
        return offspring
        
    # bit swap mutation done by swaping the value at given bit position of
    # gene; bits must be even for swaping
    def __bit_swap_gene_mutation__(self, gene):
        offspring = gene.copy()
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
        
    # calculate fitness for the degree of goodness of the encoded solution
    # fitness will be based on the equation f{x} = sum_of {i=1-p} x_i^2
    # where p is no of dimension we set it to number of gene
    def __evaluate_fitness__(self):
        sum = 0
        for i in range(self.n_gene):
            x_i = self.corresponding_value[i]
            sum += x_i ** 2
        return sum
    
    # get fitness score for each chromosome 
    # need to convert minimize objective problem to 
    # maximize objective problem by 1 / objective 
    def fitness(self):
        return 1 / self.__evaluate_fitness__()

