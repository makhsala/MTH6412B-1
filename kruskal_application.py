import numpy as np
import random
from node import Node
from edge import Edge
from graph import *
from acm import *
from ensemble_node import EnsembleNode


graph = Graph(name='Application cours')
alphabet = list('ABCDEFGHI')
for k in alphabet:
    node_k = Node(name=k)
    graph.add_node(node_k)

edge = Edge(name='AB', startnode=graph.nodes[0], endnode=graph.nodes[1], cost=4.0)
graph.add_edge(edge)
edge = Edge(name='BC', startnode=graph.nodes[1], endnode=graph.nodes[2], cost=8.0)
graph.add_edge(edge)
edge = Edge(name='CD', startnode=graph.nodes[2], endnode=graph.nodes[3], cost=7.0)
graph.add_edge(edge)
edge = Edge(name='DE', startnode=graph.nodes[3], endnode=graph.nodes[4], cost=9.0)
graph.add_edge(edge)
edge = Edge(name='EF', startnode=graph.nodes[4], endnode=graph.nodes[5], cost=10.0)
graph.add_edge(edge)
edge = Edge(name='FG', startnode=graph.nodes[5], endnode=graph.nodes[6], cost=2.0)
graph.add_edge(edge)
edge = Edge(name='GH', startnode=graph.nodes[6], endnode=graph.nodes[7], cost=1.0)
graph.add_edge(edge)
edge = Edge(name='AH', startnode=graph.nodes[7], endnode=graph.nodes[0], cost=8.0)
graph.add_edge(edge)
edge = Edge(name='DF', startnode=graph.nodes[3], endnode=graph.nodes[5], cost=14.0)
graph.add_edge(edge)
edge = Edge(name='FC', startnode=graph.nodes[5], endnode=graph.nodes[2], cost=4.0)
graph.add_edge(edge)
edge = Edge(name='CI', startnode=graph.nodes[2], endnode=graph.nodes[8], cost=2.0)
graph.add_edge(edge)
edge = Edge(name='IH', startnode=graph.nodes[8], endnode=graph.nodes[7], cost=7.0)
graph.add_edge(edge)
edge = Edge(name='IG', startnode=graph.nodes[8], endnode=graph.nodes[6], cost=6.0)
graph.add_edge(edge)
edge = Edge(name='BH', startnode=graph.nodes[8], endnode=graph.nodes[7], cost=7.0)
graph.add_edge(edge)

#construct MWST of the example graph, plot it and print its weight
kruskal_st = graph.kruskal2()
kruskal_st.plot_graph()
print 'MST WEIGHT : ' + str(kruskal_st.get_graph_weight())
