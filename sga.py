import json
import matplotlib.pyplot as plt # type: ignore
from gaconfig import GAConfig
from sphere import SphereGAEngine

# plots the fitness over all generations using matplotlib.
def fitness_plot_stats(avg_fitness_plot, best_fitness_plot, title):
        if len(avg_fitness_plot) > 0 :
            plt.plot(avg_fitness_plot, label="avg")
        if len(best_fitness_plot) > 0 :
            plt.plot(best_fitness_plot, label="best")
        plt.title(title)
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        if gaConfig.plot_type == "avg":
            plt.legend(['Average Fitness'], loc='lower right')
        elif gaConfig.plot_type == "best":
            plt.legend(['Best Fitness'], loc='lower right')
        else:
            plt.legend(['Average Fitness', 'Best Fitness'], loc='lower right')
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
    gaEngine = SphereGAEngine(gaConfig, n_gene=gaConfig.n_gene)
    gaEngine.make_initial_population()
    
    avg_fitness_plot: list = []
    best_fitness_plot: list = []
    
    if gaConfig.plot_type == "avg":
        avg_fitness_plot.append(gaEngine.average_fitness())
    elif gaConfig.plot_type == "best":
        best_fitness_plot.append(gaEngine.best_finess())
    else:
        avg_fitness_plot.append(gaEngine.average_fitness())
        best_fitness_plot.append(gaEngine.best_finess())
        
    while  gaEngine.generations < gaConfig.n_generation:
        mating_pool = gaEngine.do_selection()
        next_gen = gaEngine.do_crossover(mating_pool)
        gaEngine.next_generation(next_gen)
        gaEngine.do_mutation()
        gaEngine.change_genration()
        no_of_crossover = int(gaConfig.n_populations * gaConfig.crossover_chances)
        gaEngine.totalPopulation += no_of_crossover

        if gaConfig.plot_type == "avg":
            avg_fitness_plot.append(gaEngine.average_fitness())
        elif gaConfig.plot_type == "best":
            best_fitness_plot.append(gaEngine.best_finess())
        else:
            avg_fitness_plot.append(gaEngine.average_fitness())
            best_fitness_plot.append(gaEngine.best_finess())
    
    print(gaEngine)
    title = "Fitness for "
    if gaConfig.plot_type == "avg":
        title = "Average Fitness for "
    if gaConfig.plot_type == "best":
        title = "Best Fitness for "   
        
    plot_title = title + selected_option
    fitness_plot_stats(avg_fitness_plot=avg_fitness_plot,
                       best_fitness_plot=best_fitness_plot
                       ,title=plot_title)
    
