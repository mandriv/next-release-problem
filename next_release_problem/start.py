import math
from platypus import NSGAII, nondominated, unique
import matplotlib.pyplot as plt
from .utils import test_data, cli
from .NRP_MOO import NRP_MOO

def main():
    config = cli.init()
    number_of_runs = config['NUMBER_OF_RUNS']
    config_path = config['TEST_DATA_PATH']

    data = test_data.parse(config_path)

    requirements = data[0]
    clients = data[1]
    NRP_multi = NRP_MOO(requirements, clients)

    problem = NRP_multi.generate_problem()
    algorithm = NSGAII(problem)
    algorithm.run(number_of_runs)


    solutions = unique(nondominated(algorithm.result))
    for solution in solutions:
        reqs_met = []
        for i in range(len(solution.variables[0])):
            if solution.variables[0][i]:
                reqs_met.append(i + 1)
        print(reqs_met, solution.objectives)

    largest_x = 0;
    smallest_y = 0;
    for s in solutions:
        if s.objectives[0] > largest_x:
            largest_x = s.objectives[0]
        if s.objectives[1] < smallest_y:
            smallest_y = s.objectives[1]
    def roundup(x):
        round = math.ceil(x / 10.0)
        if x < 0:
            round = math.floor(x / 10.0)
        return int(round) * 10

    plt.scatter([s.objectives[0] for s in solutions],
                [s.objectives[1] for s in solutions])
    plt.xlim([0, roundup(largest_x)])
    plt.ylim([roundup(smallest_y), 0])
    plt.xlabel("Score")
    plt.ylabel("-Cost")
    plt.show()

if __name__ == '__main__':
    main()
