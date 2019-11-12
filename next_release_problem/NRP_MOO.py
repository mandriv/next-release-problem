from platypus import Problem, Binary

class NRP_MOO:

    def __init__(self, requirements, clients):
        self.requirements = requirements.copy()
        self.clients = clients.copy()

    def get_score(self, candidate):
        # score is a sum of all customer weighted scores
        # get all requirement numbers that's been met
        requirements_met = []
        for i in range(len(candidate)):
            if candidate[i]:
                requirements_met.append(i + 1)
        # now find the score for all met requirements
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


    def get_problem_function(self, x):
        return [self.get_score(x[0]), self.get_cost(x[0])]

    def generate_problem(self):
        problem = Problem(1, 2)
        problem.types[:] = Binary(len(self.requirements))
        problem.function = self.get_problem_function
        # problem.directions[0] = Problem.MAXIMIZE
        # problem.directions[1] = Problem.MINIMIZE
        return problem
