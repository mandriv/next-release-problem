import matplotlib.pyplot as plt

from ..problems import NRP_Problem

def roundup(x):
    round = math.ceil(x / 10.0)
    if x < 0:
        round = math.floor(x / 10.0)
    return int(round) * 10

def find_axis_limits(data):
    smallest_x = float('inf');
    largest_x = 0;
    smallest_y = 0;
    for x in data[0]:
        if x < smallest_x:
            smallest_x = x
        if x > largest_x:
            largest_x = x
    for y in data[1]:
        if y < smallest_y:
            smallest_y = y
    return (smallest_x, largest_x, smallest_y)

def get_graph_data_nsga_ii(solutions):
    return ([s.objectives[0] for s in solutions],
            [s.objectives[1] for s in solutions])

def get_graph_data_ga(solutions, requirements, clients):
    problem = NRP_Problem(requirements, clients)
    data = ([], [])
    for solution in solutions:
        candidate = solution.variables[0]
        data[0].append(problem.get_score(candidate))
        data[1].append(problem.get_cost(candidate))
    return data

def draw_graphs(data):
    print(data[1])
    meta = [('o', 'none', 'r', 'NSGA-II'),
        ('x', 'b', 'none', 'Single-Objective GA'),
        ('.', 'g', 'none', 'Random')]
    for i in range(len(data)):
        current_solutions = data[i]
        plt.scatter(current_solutions[0],
                    current_solutions[1],
                    marker=meta[i][0],
                    facecolors=meta[i][1],
                    edgecolors=meta[i][2],
                    label=meta[i][3]
                    )
    data_flat = ([], [])
    for d in data:
        data_flat[0].extend(d[0])
        data_flat[1].extend(d[1])
    limits = find_axis_limits(data_flat)
    plt.xlim([limits[0], limits[1]])
    plt.ylim([limits[2], 0])
    plt.xlabel("Score")
    plt.ylabel("-Cost")
    plt.legend(loc='upper right')
    plt.show()
