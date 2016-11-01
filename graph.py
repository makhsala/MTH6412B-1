# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 20:06:37 2016

@author: makhloufi, lacroix
"""
import numpy as np
import sys
from edge import Edge
from acm import ACM
from ensemble_node import EnsembleNode
from queue import Queue, PriorityMinQueue


class Graph(object):
    """
    Une classe générique pour représenter un graphe comme un ensemble de
    noeuds et d'aretes.
    """

    def __init__(self, name='Sans nom'):
        self.__graph_name = name
        self.__nodes = []   # Attribut prive.
        self.__edges = []
        self.__adj_matrix = {}  # matrice d'adjacence

    def add_node(self, node):
        """Ajouter un noeud au graphe et initialisé la matrice d'adjacence"""
        self.__nodes.append(node)
        self.__adj_matrix[node] = {}

    def add_edge(self, edge):
        "Ajout un edge au graphe et remplissage de adj_matrix"
        # on rempli la matrice d'adjacence à chaque fois on ajoute un arc
        # < pour éviter de stocker l'arrete deux fois
        if ((edge.edge_startnode != edge.edge_endnode) & (edge.edge_cost != 0)):
            self.__adj_matrix[edge.edge_startnode][edge.edge_endnode] = edge.edge_cost
            self.__edges.append(edge)

    @property
    def graph_name(self):
        "Donne le nom du graphe."
        return self.__graph_name

    @graph_name.setter
    def graph_name(self, name):
        self.__graph_name = name

    @property
    def edges(self):
        "Donne la liste des aretes du graphe."
        return self.__edges

    @property
    def nodes(self):
        "Donne la liste des noeuds du graphe."
        return self.__nodes

    @nodes.setter
    def nodes(self, nodes):
        """"""
        self.__nodes = nodes
        for node in nodes:
            self.__adj_matrix[node] = {}

    @property
    def adj_matrix(self):
        return self.__adj_matrix

    def get_nb_edges(self):
        "Donne le nombre de noeuds du graphe."
        return (len(self.edges))

    def get_nb_nodes(self):
        "Donne le nombre de noeuds du graphe."
        return (len(self.nodes))

    def get_graph_weight(self):
        return sum([edge.edge_cost for edge in self.edges])

    def get_edge(self, startnode, endnode):
        for edge in self.edges:
            if (((edge.edge_startnode == startnode) & (edge.edge_endnode == endnode)) | ((edge.edge_startnode == endnode) & (edge.edge_endnode == startnode))):
                return edge
        return None


    def __repr__(self):
        name = self.graph_name
        nb_nodes = self.get_nb_nodes()
        s = 'Graphe %s comprenant %d noeuds' % (name, nb_nodes)
        for node in self.nodes:
            s += '\n  ' + repr(node)
        for edge in self.edges:
            s += '\n  ' + repr(edge) + '\n  '
        s += "Matrice d'adjacence \n"
        s += str(self.adj_matrix)
        return s

    def plot_graph(self):
        """
        Plot the graph represented by `nodes` and `edges` using Matplotlib.
        Very basic for now.
        """
        import matplotlib.pyplot as plt
        from matplotlib.collections import LineCollection

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = [int(node.node_data[0]) for node in self.__nodes]  # liste des abscisses
        y = [int(node.node_data[1]) for node in self.__nodes]  # liste des ordonnées

        # Plot edges.
        edge_pos = np.asarray([(e.edge_startnode.node_data, e.edge_endnode.node_data
                                ) for e in self.edges])

        edge_collection = LineCollection(edge_pos, linewidth=1.5,
                                         antialiased=True, colors=(.8, .8, .8),
                                         alpha=.75, zorder=0)

        ax.add_collection(edge_collection)
        ax.scatter(x, y, s=35, c='r', antialiased=True, alpha=.75, zorder=1)
        ax.set_xlim(min(x) - 10, max(x) + 10)
        ax.set_ylim(min(y) - 10, max(y) + 10)
        plt.show()
        return

    def kruskal(self):
        """ 
        Kruskal algo: this function returns a graph
        that is the minimal weight spanning tree of the graph.
        Uses EnsembleNode class.
        """

        nb_noeuds = self.get_nb_nodes()
        spanning_tree = Graph(name=self.graph_name + " spanning tree")

        # function used to sort the list of edges
        def getKey(edge):
            return edge.edge_cost

        # construct a list containing EnsembleNode nodes (constructed from the
        # graph nodes) and a list containing edges between these ensemble nodes
        if not all(isinstance(node, EnsembleNode) for node in self.nodes):
            ensemble_nodes = [EnsembleNode(
                name=node.node_name, data=node.node_data,
                father=None) for node in self.nodes]
            ensemble_edges = [Edge(
                name=edge.edge_name, data=edge.edge_data, cost=edge.edge_cost,
                startnode=ensemble_nodes[self.nodes.index(edge.edge_startnode)],
                endnode=ensemble_nodes[self.nodes.index(edge.edge_endnode)]) for edge in self.edges]

        # set spanning_tree nodes list
        spanning_tree.nodes = ensemble_nodes

        # sort list of edges between ensemble nodes
        sorted_edges = sorted(ensemble_edges, key=getKey)

        for edge in sorted_edges:
            # stopping condition of the algorithm
            if len(spanning_tree.edges) == nb_noeuds-1:
                break

            # test whether the 2 nodes connected by the edges
            # belong to the same connected ensembles
            if edge.edge_startnode.get_root_and_compress() != edge.edge_endnode.get_root_and_compress():
                spanning_tree.add_edge(edge)
                edge.edge_startnode.rank_union(edge.edge_endnode)

        return spanning_tree

    def prim(self, source_node):

        n_nodes = self.get_nb_nodes()
        spanning_tree = Graph(name=self.graph_name + " Prim algorithm spanning tree")
        spanning_tree.nodes = self.nodes

        if not all(isinstance(node, EnsembleNode) for node in self.nodes):
            
            # Create queue containing EnsembleNode nodes constructed from graph self
            # the EnsembleNode corresponding to source_node gets 0 as min_weight value,
            # others get +inf
            nodes_queue = PriorityMinQueue()
            for node in self.nodes:
                if node == source_node:
                    ensemble_node = EnsembleNode(name=node.node_name, data=node.node_data, min_weight=0)
                else:
                    ensemble_node = EnsembleNode(name=node.node_name, data=node.node_data, min_weight=float('inf'))
                nodes_queue.enqueue(ensemble_node)
            
            # Create list of edges between EnsembleNode corresponding to 
            # edges in the graph self 
            ensemble_edges = [Edge(
                name=edge.edge_name, data=edge.edge_data, cost=edge.edge_cost,
                startnode=nodes_queue.items[self.nodes.index(edge.edge_startnode)],
                endnode=nodes_queue.items[self.nodes.index(edge.edge_endnode)]) for edge in self.edges]

            # Make dictionnary mapping ensembles_nodes to nodes
            ensnode_to_node_dict = {ens_node: node for (ens_node, node) in zip(nodes_queue.items, self.nodes)}

        while not nodes_queue.is_empty():
            n = nodes_queue.dequeue()
            n.min_weight = 0

            # If n is not the first node to be chosen (the EnsembleNode associated to source_node),
            # add edge between n and its father to the spanning tree Graph
            if not n.is_root():
                spanning_tree.add_edge(self.get_edge(ensnode_to_node_dict[n],ensnode_to_node_dict[n.father]))

            # Search over all ensemble_edges for edges connecting n to other nodes u
            # and update u (min_weight, father) if necessary  
            for edge in ensemble_edges:
                if ((edge.edge_startnode == n) | (edge.edge_endnode == n)):
                    u = edge.edge_startnode if edge.edge_endnode == n else edge.edge_endnode
                    if u.min_weight > edge.edge_cost:
                        u.min_weight = edge.edge_cost
                        u.father = n

        return spanning_tree

if __name__ == '__main__':

    G = Graph(name='Graphe test')
    for k in range(5):
        G.add_node(Node(name='Noeud test %d' % k))
    for k in range(5):
        G.add_edge(Edge(name='Edge test %d' % k, cost=(10-k)))

    print "liste non trié"
    print G.edges[0]
