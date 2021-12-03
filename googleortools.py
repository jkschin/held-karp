import heldkarp
import pickle
import numpy as np
import cv2
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model(dists):
    data = {}
    data["distance_matrix"] = dists
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
      index = routing.Start(route_nbr)
      route = [manager.IndexToNode(index)]
      while not routing.IsEnd(index):
        index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
      routes.append(route)
    return routes

def main(dists):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(dists)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)
    return get_routes(solution, routing, manager)


if __name__ == '__main__':
    a = open("tspdump.pickle", "rb")
    b = pickle.load(a)
    print(b[1]["results"])
    subset = b[1]["subset"]
    dists = heldkarp.generate_manhattan_distances(subset)
    routes = main(dists)
    print(routes[0])
# def generate_image_pair(subset, tsp_sol):
#     soln = np.zeros((512, 512, 3))
#     soln = heldkarp.generate_manhattan_solution(soln, subset, tsp_sol[1])
#     soln = heldkarp.draw_dots(soln, subset, heldkarp.RED)
#     cv2.imwrite("test.png", soln)

# generate_image_pair(b[1]["subset"], b[1]["results"])