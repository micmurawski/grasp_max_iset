import networkx as nx
import random
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import time


def get_iset_by_removing_nodes(G, pick_random=False, alfa=0.6):
    """
    Implementation of the algorithm used for finding the 
    largest independent set by removing nodes
    """
    X = G.copy()
    while X.number_of_edges() != 0:
        nodes = sorted(X.degree(), key=lambda x: x[1])

        if not pick_random:
            node = nodes.pop()[0]
        else:
            restricted_candidates_list = make_restricted_candidate_list(X, alfa=alfa)
            node = random.choice(restricted_candidates_list)
        X.remove_node(node)
    return set.union(*[{x[0]} for x in X.degree()])


def get_iset_by_adding_nodes(G, pick_random=False, alfa=0.6):
    """
    Implementation of the algorithm used for finding the 
    largest independent set by adding nodes
    """
    X = G.copy()
    nodes = sorted(X.degree(), key=lambda x: x[1], reverse=True)
    U = set()
    while len(nodes) != 0:
        if not pick_random:
            node = nodes.pop()[0]
        else:
            restricted_candidates_list = make_restricted_candidate_list(X, alfa=alfa, reverse=True)
            node = random.choice(restricted_candidates_list)

        U.add(node)
        for neighbor in set(X.neighbors(node)):
            X.remove_node(neighbor)
        X.remove_node(node)
        nodes = sorted(X.degree(), key=lambda x: x[1], reverse=True)
    return U


def is_independent_set(graph, nodes):
    """
    Method used for veryfing the independce of the graph set
    """ 
    neighbors = set.union(*[set(graph.neighbors(v)) for v in nodes])
    if set.intersection(neighbors, nodes):
        return False
    return True


def local_search23(graph, solution, stop=None):
    it = 0
    for ki,kj in combinations(solution,2):
        if ki != kj:
            solution_temp = solution.difference({ki, kj})
            Q = set(graph.nodes()).difference(solution_temp)
            for qi,qj,qk in combinations(Q,3):
                if qi != qj and qj != qk and qi != qk:
                    new_solution = solution_temp
                    new_solution.add(qi)
                    new_solution.add(qj)
                    new_solution.add(qk)
                    it += 1
                    if is_independent_set(graph, new_solution) and len(new_solution) > 0:
                        print('2-3, exchange')
                        print(ki,kj,'-',qi,qj,qk)
                        return new_solution, True
                    else:
                        if stop is None:
                            pass
                        elif stop < it:
                            return solution, False
    return solution, False


def local_search12(graph, solution, stop=None):
    it = 0
    iterlist = [e for e in solution]
    for i in range(len(iterlist)):
            ki = iterlist.pop(random.randrange(len(iterlist)))
            solution_temp = solution.difference({ki})
            Q = set(graph.nodes()).difference(solution_temp)
            list2 = [(qi,qj) for qi,qj in combinations(Q,2)]
            for j in range(len(list2)):
                qi, qj = list2.pop(random.randrange(len(list2)))
                if qi != qj:
                    new_solution = solution_temp
                    new_solution.add(qi)
                    new_solution.add(qj)
                    it += 1
                    if is_independent_set(graph, new_solution) and len(new_solution) > 0:
                        print('1-2, exchange')
                        print(ki,'-',qi,qj)
                        return new_solution, True
                    else:
                        if stop is None:
                            pass
                        elif stop < it:
                            return solution, False
    return solution, False


def update_solution(solution, best_solution):
    if len(best_solution) < len(solution):
        return solution
    else:
        return best_solution


def make_restricted_candidate_list(graph, alfa, reverse=False):
    degrees = graph.degree()
    dlist = sorted([degrees(i) for i in graph.nodes])
    d_max = dlist[-1]
    d_min = dlist[0]
    if not reverse:
        condition = d_min + alfa * (d_max - d_min)
    else:
        condition = d_max - alfa * (d_max - d_min)
    restricted_candidate_list = [v for v in graph.nodes if degrees[v] >= condition]
    return restricted_candidate_list



def grasp(G, loops, greedy, pick_random=False, with_local_search=True, alfa=0.6, stop=100):
    """
    Implementation of the GRASP algorithm according to the paper specified in the documentation.
    """
    graph = G.copy()
    best_solution = set()
    continue_searching = with_local_search
    for i in range(loops):
        solution = greedy(graph, pick_random=pick_random, alfa=alfa)
        while continue_searching:
            solution, continue_searching = local_search12(graph, solution, stop=stop)
            best_solution = update_solution(solution, best_solution)

    return best_solution
