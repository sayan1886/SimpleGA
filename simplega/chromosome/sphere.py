from simplega.chromosome.complexchromosome import ComplexChromosome

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