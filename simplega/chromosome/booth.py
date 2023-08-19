from simplega.chromosome.complexchromosome import ComplexChromosome

# benchmark problem on spehre
# study of the Booth function:
# f(x) = (x_1 + 2 * x_2 − 7)^2 + (2 * x_1 + x_2 − 5)^2
class Booth(ComplexChromosome):
    
        def __init__(self, gaConfig, chromosomes=[], n_gene=3) -> None:
             super().__init__(gaConfig, chromosomes, n_gene)
             
        # calculate fitness for the degree of goodness of the encoded solution
        # fitness will be based on the equation 
        # # f(x) = (x_1 + 2 * x_2 − 7)^2 + (2 * x_1 + x_2 − 5)^2
        # where p is no of dimension we set it to number of gene
        def __evaluate_fitness__(self):
            x_1 = self.corresponding_value[0]
            x_2 = self.corresponding_value[1]
            f_x = (((x_1 + 2 * x_2 - 7) ** 2) +  ((2 * x_1 + x_2 - 5) ** 2))
            return f_x