import datetime

from platypus import NSGAII, GeneticAlgorithm, nondominated, unique, CompoundOperator, SBX, HUX, PM, BitFlip

from .utils import test_data, cli, results
from .problems import NRP_MOO, NRP_SOO, NRP_Random

def main():
    # get config vars
    config = cli.init()
    population_size_nsgaii = config['POPULATION_SIZE_NSGAII']
    number_of_runs_nsgaii = config['NUMBER_OF_RUNS_NSGAII']
    number_of_runs_ga = config['NUMBER_OF_RUNS_GA']
    population_size_ga = config['POPULATION_SIZE_GA']
    config_path = config['TEST_DATA_PATH']
    ga_weights = config['GA_WEIGHTS']
    budget_constraint = config['BUDGET_CONSTRAINT']
    # parse and get specific data
    data = test_data.parse(config_path)
    requirements = data[0]
    clients = data[1]
    # run NSGA-II multi-objective algorithm
    print(datetime.datetime.now())
    print('Running NSGA-II...')
    NRP_multi = NRP_MOO(requirements, clients, budget_constraint)
    algorithm = NSGAII(NRP_multi.generate_problem(), population_size=population_size_nsgaii)
    algorithm.run(number_of_runs_nsgaii)
    NSGAII_solutions = unique(nondominated(algorithm.result))
    # run GA single-objective algorithm with different weights
    GA_solutions = []
    for ga_weight in ga_weights:
        print(datetime.datetime.now())
        print('Running GA for weights ' + str(ga_weight) + ' and ' + str(1 - ga_weight) + '...')
        NRP_single = NRP_SOO(requirements, clients, budget_constraint, ga_weight, 1 - ga_weight)
        algorithm = GeneticAlgorithm(NRP_single.generate_problem(), population_size=population_size_ga)
        algorithm.run(number_of_runs_ga)
        GA_solutions.extend(unique(nondominated(algorithm.result)))
    # run random algorithm
    print(datetime.datetime.now())
    print('Generating random solution...')
    NRP_random = NRP_Random(requirements, clients, budget_constraint)
    random_solutions = NRP_random.generate_solutions()
    print('done!')
    # draw graphs
    results.draw_graphs([results.get_graph_data_nsga_ii(NSGAII_solutions),
                        results.get_graph_data_ga(GA_solutions, requirements, clients, budget_constraint),
                        results.get_graph_data_ga(random_solutions, requirements, clients, budget_constraint)])

if __name__ == '__main__':
    main()
