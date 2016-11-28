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

# optimal distances

opt_dist = { 'bayg29' : 1610, 'bays29' : 2020, 'brazil58' : 25395,
             'brg180': 1950, 'dantzig42' : 699, 'fri26' : 937, 'gr17' : 2085,
             'gr21' : 2707, 'gr24' : 1272, 'gr48' : 5046, 'gr120' : 6942,
             'hk48' : 11461, 'pa561' : 2763, 'swiss42' : 1273 }

def construct_graph(file):
    """
    This function constructs a graph defined in an stsp instance file
    and bypasses the problem of 0-length nodes set returned
    by the read_node function for some stsp instances
    """

    finstance = file
    # sys.argv[1]
    G = Graph("Example Graph")

    with open(finstance, "r") as fd:

        header = read_header(fd)
        dim = header['DIMENSION']
        name = header['NAME']
        G.graph_name = name
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

# result file
rf = open('resultfile', 'w')


# Construct and print example Graph
# construct G minimal weight spanning tree, plot it and print its weight
# G_spanning_tree = G.kruskal()
#G_spanning_tree = G.prim()

st_algo_list = ["kruskal","prim"]
# st_algo ="kruskal"

dic = {}

# instance| kruskal|source|Prim|source|optimal|Gap avec tournée optimal
s = "INSTANCE_NAME|ROOT|PRIM_SOL|GAP_Prim|KRUSKAL_SOL|GAP_KRUSKAL|OPTIMAL_SOL\n"
rf.write(s)
for i in range(1,len(sys.argv)):
    graph = construct_graph(sys.argv[i])
    cle = graph.graph_name.strip()
    for root in graph.nodes:

        s = graph.graph_name + "|" + repr(root)
        for st_algo in st_algo_list:
            dic = graph.rsl(root, st_algo)
            gap = dic["c_c"]-opt_dist[cle]
            s += "|" + str(dic["c_c"])+"|"+str(gap)
        s += "|" + str(opt_dist[cle])+"\n"
        rf.write(s)


#print("MST weight of the graph is " + str(G_spanning_tree.get_graph_weight()))
#G.plot_graph()
#G_spanning_tree.plot_graph()
