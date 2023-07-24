import json
import matplotlib.pyplot as plt
from gaconfig import GAConfig
from gaengine import GAEngine

# plots the fitness over all generations using matplotlib.
def fitness_plot_stats(fitness_plot):
        plt.plot(fitness_plot)
        plt.title('Average Fitness')
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        plt.legend(['Fitness'], loc='lower right')
        plt.show()

def selct_config(option):
    if option == "1":
        return "config_bts_bit_flip.json"
    elif option == "2":
        return "config_bts_bit_swap.json"
    elif option == "3":
        return "config_roulette_bit_flip.json"
    elif option == "4":
        return "config_roulette_bit_swap.json"
    else:
        return "config_bts_bit_flip.json"

if __name__ == '__main__':
    print("Simple Gentic Algorithm Config Selction:")
    print("1. Binary Tournament Selection with Bit Flip Mutation")
    print("2. Binary Tournament Selection with Bit Swap Mutation")
    print("3. Roulette-Wheel Selection with Bit Flip Mutation")
    print("4. Roulette-Wheel Selection with Bit Swap Mutation")
    option = input("Enter your choice: ")
    config_file_name = selct_config(option)
    print(config_file_name)
    with open(config_file_name,'r') as file:
        configString = file.read()
    configJSON = json.loads(configString)
    gaConfig = GAConfig.from_dict(configJSON)
    # print(gaConfig)
    if gaConfig.selection.type == "tournament":
        if gaConfig.selection.size >= gaConfig.n_populations:
            print("tournament selction size should be less than population size")
            exit()
    gaEngine = GAEngine(gaConfig)
    gaEngine.make_initial_population()
    fitness_plot: list = []
    fitness_plot.append(gaEngine.average_fitness())
    while  gaEngine.generations < gaConfig.generation_threshold:
        gaEngine.do_selection()
        mating_pool = gaEngine.do_selection()
        next_gen = gaEngine.do_crossover(mating_pool)
        gaEngine.next_generation(next_gen)
        gaEngine.do_mutation()
        gaEngine.change_genration()
        no_of_crossover = int(gaConfig.n_populations * gaConfig.crossover_chances)
        gaEngine.totalPopulation += no_of_crossover
        fitness_plot.append(gaEngine.average_fitness())
    
    fitness_plot_stats(fitness_plot)
    print(gaEngine)
