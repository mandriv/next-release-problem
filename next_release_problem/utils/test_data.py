def parse(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    line_index = 0
    # 1.1 get requirements
    requirements = []
    number_of_levels = int(lines[0])
    for i in range(number_of_levels):
        line = lines[(i + 1) * 2]
        req_costs = line.rstrip().split(' ')
        for req_cost_str in req_costs:
            requirements.append(int(req_cost_str))
    # 1.2 transform requirement cost to

    reqs_deps_index = (number_of_levels * 2) + 1
    reqs_deps_number = int(lines[reqs_deps_index])
    number_of_clients_index = reqs_deps_index + reqs_deps_number + 1
    number_of_clients = int(lines[number_of_clients_index])
    # 2.1 Get clients info
    raw_clients = []
    for i in range(number_of_clients_index + 1, len(lines)):
        line = lines[i]
        bits = line.rstrip().split(' ')
        # get unporcessed client value
        client_value_raw = int(bits.pop(0))
        # remove number of requirements
        bits.pop(0)
        # the leftover is just requirements
        reqs = []
        # convert to ints
        for j in range(len(bits)):
            reqs.append(int(bits[j]))
        # clients is an array [raw_score, [...reqs]]
        raw_clients.append([client_value_raw, reqs])
    # 2.2 get sum of all client value
    raw_client_value_sum = raw_clients[0][0]
    for i in range(len(raw_clients)):
        raw_client_value_sum += raw_clients[i][0]
    # transform raw clients values to floats 0.0-1.0
    # assign values to each client requirement as well
    clients = []
    for raw_client in raw_clients:
        raw_client_value = raw_client[0]
        raw_client_requirements = raw_client[1]

        client_value = raw_client_value / raw_client_value_sum

        number_of_client_requirements = len(raw_client_requirements)
        client_requirements = []
        for i in range(number_of_client_requirements):
            client_requirement_value = ((number_of_client_requirements - i) / number_of_client_requirements) * 100
            client_requirement = raw_client_requirements[i]
            client_requirements.append((client_requirement_value, client_requirement))
        clients.append((client_value, client_requirements))
    return (requirements, clients)
