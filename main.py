# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 20:04:50 2016

@author: makhloufi, lacroix
"""

from graph import Graph
from edge import Edge
from node import Node
from read_stsp import *
import sys


def construct_graph(file):
    """
    This function constructs a graph defined in an stsp instance file
    and bypasses the problem of 0-length nodes set returned
    by the read_node function for some stsp instances
    """

    finstance = file
    sys.argv[1]
    G = Graph("Example Graph")

    with open(finstance, "r") as fd:

        header = read_header(fd)
        dim = header['DIMENSION']

        nodes = read_nodes(header, fd)
        if nodes:
            for n in range(len(nodes)):
                G.add_node(Node(data=nodes[n]))
        else:
            for n in range(dim):
                G.add_node(Node())

        edges = read_edges(header, fd)
        for e in edges:
            G.add_edge(Edge(startnode=G.nodes[int(e[0])],
                            endnode=G.nodes[int(e[1])], cost=e[2]))

    return G

# Construct and print example Graph
G = construct_graph(sys.argv[1])
# construct G minimal weight spanning tree, plot it and print its weight
# G_spanning_tree = G.kruskal()
G_spanning_tree = G.prim()

print("MST weight of the graph is " + str(G_spanning_tree.get_graph_weight()))
G.plot_graph()
G_spanning_tree.plot_graph()
