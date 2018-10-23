from enum import Enum


class GraphRepresentation(Enum):
    adjlist = 1
    edgelist = 2
    gml = 3


def dump_graph_to_file(graph, path, representation=GraphRepresentation.adjlist):
    import networkx as nx
    getattr(nx, 'write_' + representation.name)(graph, path)


def load_graph_from_file(path, representation=GraphRepresentation.adjlist):
    import networkx as nx
    return getattr(nx, 'read_' + representation.name)(path)