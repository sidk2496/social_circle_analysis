from graph_utils import *
from input_utils import *
import pickle
import argparse

def main(args):
    threshold = args.t
    alpha = args.a
    input_filename = args.inp
    iterations = args.iter

    data_dir = '../../data/facebook/processed/'
    with open(data_dir + input_filename, 'rb') as input_file:
        ego_network = pickle.load(input_file)

    nodes = ego_network['nodes']
    edges = ego_network['edges']
    adjlist = ego_network['adjlist']
    circles = [Circle(node_id, {node_id}) for node_id in nodes.keys()]
    circles = dict(zip(nodes.keys(), circles))
    ego_network = Graph(nodes, edges, adjlist, circles)

    while iterations:
        ego_network.edges.sort(key=lambda edge: edge.w)
        ego_network.circle_formation()
        ego_network.dissolve_circles(threshold)
        ego_network.label_propagation(alpha)
        ego_network.update_edge_weights()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=float, help='IoU threshold')
    parser.add_argument('--a', type=float, help='alpha for updating label values')
    parser.add_argument('--inp', type=str, help='input file')
    parser.add_argument('--iter', type=float, help='max number of iterations')
    args = parser.parse_args()
    main(args)