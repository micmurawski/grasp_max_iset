from commons.commons import load_graph_from_file
from algorithms import *

if __name__=="__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="Absolute path to the file in which the graph representation should be saved.")
    parser.add_argument(
        "-it", "--iter", help="Number of grasp loops", default=100)
    parser.add_argument(
        "-t", "--type", help="0-adding nodes, 1-removing nodes",default=0)
    parser.add_argument(
        "-s", "--stop", help="loops of local search",default=1000)
    parser.add_argument(
        "-a", "--alfa", help="loops of local search",default=0.6)
    args = parser.parse_args()
    graph=load_graph_from_file(path=args.path)
    print('sciezka grafu', args.path)
    print('ilosc iteracji grasp', args.iter)
    print('ilosc iteracji local_search', args.stop)
    print('parametr alfa', args.alfa)
    print('GRAF')
    print('ilosc wierzcholkow: ',len(graph.nodes()))
    print('ilosc krawedzi: ' ,len(graph.edges))
    if int(args.type)==0:
        print('rodzaj algorytmu: dodawanie wierzcholkow')
        start = time.time()
        result = grasp(graph, int(args.iter), greedy=get_iset_by_adding_nodes, pick_random=False,with_local_search=True,alfa=float(args.alfa),stop=int(args.stop))
        end = time.time()
        print(result)
        print('rozmiar zbioru niezalezego:', len(result))
        print('czas wykonania', end-start)
    else:
        print('rodzaj algorytmu: usuwanie wierzcholkow')
        start = time.time()
        result = grasp(graph, int(args.iter), greedy=get_iset_by_removing_nodes, pick_random=False,with_local_search=True,alfa=float(args.alfa),stop=int(args.stop))
        end = time.time()
        print(result)
        print('rozmiar zbioru niezalezego:', len(result))
        print('czas wykonania', end-start)