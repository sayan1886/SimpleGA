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
        
    # calculate fitness for the degree of goodness of the encoded solution
    # fitness will be based on the equation f{x} = sum_of {i=1-p} x_i^2
    # where p is no of dimension we set it to number of gene
    def __evaluate_fitness__(self):
        sum = 0
        for i in range(self.n_gene):
            x_i = self.corresponding_value[i]
            sum += x_i ** 2
        return sum
    
    # get fitness 
    def fitness(self):
        return self.__evaluate_fitness__()

