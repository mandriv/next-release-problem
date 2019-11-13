from abc import ABCMeta, abstractmethod

from platypus import Problem, Binary, Real, RandomGenerator

class NRP_Problem():

    __metaclass__ = ABCMeta

    def __init__(self, requirements, clients):
        self.requirements = requirements.copy()
        self.clients = clients.copy()

    def get_requirements_met(self, candidate):
        requirements_met = []
        for i in range(len(candidate)):
            if candidate[i]:
                requirements_met.append(i + 1)
        return requirements_met

    def get_score(self, candidate):
        # score is a sum of all customer weighted scores
        requirements_met = self.get_requirements_met(candidate)
        score = 0
        for requirement_number in requirements_met:
            for client in self.clients:
                client_value = client[0]
                client_requirements = client[1]
                client_requirement_weight = 0.0
                for req in client_requirements:
                    if req[1] == requirement_number:
                        client_requirement_weight = req[0]
                        break
                score += client_value * client_requirement_weight
        return score

    def get_cost(self, candidate):
        cost = 0;
        for i in range(len(candidate)):
            if candidate[i]:
                cost -= self.requirements[i]
        return cost

    @abstractmethod
    def get_problem_function(self):
        raise NotImplementedError('Method not implemented')

    @abstractmethod
    def generate_problem(self):
        raise NotImplementedError('Method not implemented')

class NRP_MOO(NRP_Problem):

    def get_problem_function(self, x):
        score = self.get_score(x[0])
        cost = self.get_cost(x[0])
        number_of_requirements_met = len(self.get_requirements_met(x[0]))
        return [score, cost], [number_of_requirements_met]

    def generate_problem(self):
        # 1 decision variables, 2 objectives, 1 constraint
        problem = Problem(1, 2, 1)
        problem.types[:] = Binary(len(self.requirements))
        problem.directions[:] = Problem.MAXIMIZE
        problem.constraints[:] = "!=0"
        problem.function = self.get_problem_function
        return problem

class NRP_SOO(NRP_Problem):

    def __init__(self, requirements, clients, score_weight, cost_weight):
        super(NRP_SOO, self).__init__(requirements, clients)
        self.score_weight = score_weight
        self.cost_weight = cost_weight

    def get_problem_function(self, x):
        weighted_score = self.score_weight * self.get_score(x[0])
        weighted_cost = self.cost_weight * self.get_cost(x[0])
        fitness = weighted_score + weighted_cost
        number_of_requirements_met = len(self.get_requirements_met(x[0]))
        return [fitness], [number_of_requirements_met]

    def generate_problem(self):
        # 1 decision variables, 1 objectives, 1 constraint
        problem = Problem(1, 1, 1)
        problem.types[:] = Binary(len(self.requirements))
        problem.directions[:] = Problem.MAXIMIZE
        problem.constraints[:] = "!=0"
        problem.function = self.get_problem_function
        return problem

class NRP_Random(NRP_MOO):

    def generate_solutions(self):
        problem = super(NRP_Random, self).generate_problem()
        random_generator = RandomGenerator()
        solutions = []
        for _ in range(1000):
            solutions.append(random_generator.generate(problem))
        return solutions
