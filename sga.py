import json
import matplotlib.pyplot as plt
from gaconfig import GAConfig
from gaengine import GAEngine

# plots the fitness over all generations using matplotlib.
def fitness_plot_stats(fitness_plot, title):
        plot_title = "Average Fitness for " + title
        plt.plot(fitness_plot)
        plt.title(plot_title)
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        plt.legend(['Fitness'], loc='lower right')
        plt.show()

def selct_config(option):
    file_name = "config_bts_bit_flip.json"
    selected_option = "Binary Tournament Selection with Bit Flip Mutation"
    if option == "1":
        file_name = "config_bts_bit_flip.json"
        selected_option = "Binary Tournament Selection with Bit Flip Mutation"
    elif option == "2":
        file_name = "config_bts_bit_swap.json"
        selected_option = "Binary Tournament Selection with Bit Swap Mutation"
    elif option == "3":
        file_name = "config_roulette_bit_flip.json"
        selected_option = "Roulette-Wheel Selection with Bit Flip Mutation"
    elif option == "4":
        file_name = "config_roulette_bit_swap.json"
        selected_option = "Roulette-Wheel Selection with Bit Swap Mutation"
    else:
        file_name = "config_bts_bit_flip.json"
        selected_option = "Binary Tournament Selection with Bit Flip Mutation"
    return file_name, selected_option

if __name__ == '__main__':
    print("Simple Gentic Algorithm Config Selction:")
    print("1. Binary Tournament Selection with Bit Flip Mutation")
    print("2. Binary Tournament Selection with Bit Swap Mutation")
    print("3. Roulette-Wheel Selection with Bit Flip Mutation")
    print("4. Roulette-Wheel Selection with Bit Swap Mutation")
    option = input("Enter your choice: ")
    config_file_name, selected_option = selct_config(option)
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
    
    fitness_plot_stats(fitness_plot, selected_option)
    print(gaEngine)
