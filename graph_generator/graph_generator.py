#!/usr/local/bin/python3
import networkx as nx
from commons.commons import GraphRepresentation, dump_graph_to_file


class GraphGenerator:
    """
    Class used for graph generation.
    Dumps graphs generated using Erdos-Renyi model to specified path.
    """
    delimiter = ' '
    encoding = 'utf-8'

    @staticmethod
    def generate_graph(vertices, path=None, representation=None, verbose=None):
        """
        Main method of the GraphGenerator.
        Creates random graph with predefined edge probability.
        Stores output in a file in desired representation
        """
        graph = GraphGenerator._generate_random_graph(vertices)

        if path:
            dump_graph_to_file(graph, path, representation)
        else:
            if verbose:
                GraphGenerator._print_graph_as_adj_list(graph)
            return graph

    @staticmethod
    def _generate_random_graph(vertices, edge_probability=0.3):
        """
        Method returns Erdos-Renyi graph with specified number of nodes and predefined edge probability.
        """
        return nx.erdos_renyi_graph(vertices, edge_probability)

    @staticmethod
    def _save_graph_as_image(graph):
        """
        Dumps grapht to a PNG file in the working directory.
        """
        import matplotlib.pyplot as plt
        ax = plt.subplot(111)
        ax.set_title('Graph - {} nodes, {} edges'.format(
            len(graph.nodes()),
            len(graph.edges())
        ), fontsize=10)
        plt.tight_layout()
        plt.savefig("Graph.png", format="PNG")

    @staticmethod
    def _print_graph_as_adj_list(graph):
        """
        Prints the generated graph to standard output.
        """
        for line in nx.generate_adjlist(graph, GraphGenerator.delimiter):
            line_elems = line.split(GraphGenerator.delimiter)
            print("Node", line_elems[0], ":", line_elems[1:])


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        "vertices", type=int, help="Desired number of vertices in the generated graph.")
    parser.add_argument(
        "-p", "--path", help="Absolute path to the file in which the graph representation should be saved.")
    parser.add_argument(
        "-r", "--representation", default=GraphRepresentation.adjlist, help="Graph representation",
    )
    parser.add_argument(
        "-v", "--verbose", help="Toggle on verbose mode", action="store_true"
    )

    args = parser.parse_args()
    GraphGenerator.generate_graph(**vars(args))