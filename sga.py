import json

from gaconfig import GAConfig
from gaengine import GAEngine

if __name__ == '__main__':
    with open('config.json','r') as file:
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
    
    while  gaEngine.generations < gaConfig.generation_threshold:
        gaEngine.do_selection()
        mating_pool = gaEngine.do_selection()
        next_gen = gaEngine.do_crossover(mating_pool)
        gaEngine.next_generation(next_gen)
        gaEngine.do_mutation()
        gaEngine.change_genration()
        no_of_crossover = int(gaConfig.n_populations * gaConfig.crossover_chances)
        gaEngine.totalPopulation += no_of_crossover
    
    print(gaEngine)
