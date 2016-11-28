# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 20:06:37 2016

@author: makhloufi, lacroix
"""

import numpy as np
from edge import Edge
from ensemble_node import EnsembleNode
from queue import Queue, PriorityMinQueue
from node import Node
from stack import Stack


class Graph(object):
    """
    Une classe générique pour représenter un graphe comme un ensemble de
    noeuds et d'aretes.
    """

    def __init__(self, name='Sans nom'):
        self.__graph_name = name
        self.__nodes = []  # Attribut prive.
        self.__edges = []
        self.__adj_matrix = {}  # matrice d'adjacence
        self.__graph_weight = 0

    def add_node(self, node):

        self.__nodes.append(node)
        self.__adj_matrix[node] = {}

    def add_edge(self, edge):
        "Ajout un edge au graphe et remplissage de adj_matrix"
        # on rempli la matrice d'adjacence à chaque fois on ajoute un arc
        # < pour éviter de stocker l'arrete deux fois
        if (edge.edge_startnode != edge.edge_endnode):
            self.__adj_matrix[edge.edge_startnode][edge.edge_endnode] = edge
            self.__adj_matrix[edge.edge_endnode][edge.edge_startnode] = edge
            self.set_graph_weight(self.get_graph_weight()+ edge.edge_cost)
            self.__edges.append(edge)

    def add_edge2(self, edge, startnode, endnode):

        self.__adj_matrix[startnode][endnode] = edge
        self.__adj_matrix[endnode][startnode] = edge
        self.set_graph_weight(self.get_graph_weight()+ edge.edge_cost)
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

    def set_graph_weight(self,weight):
        self.__graph_weight = weight

    def get_graph_weight(self):
        return self.__graph_weight

    def get_edge(self, startnode, endnode):
        for edge in self.edges:
            if (((edge.edge_startnode == startnode) & (edge.edge_endnode == endnode)) |
                    ((edge.edge_startnode == endnode) & (edge.edge_endnode == startnode))):
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
        ensemble_nodes = [EnsembleNode(
            name=node.node_name, data=node.node_data,
            father=None, original_node=node ) for node in self.nodes]
        ensemble_edges = [Edge(
            name=edge.edge_name, data=edge.edge_data, cost=edge.edge_cost,
            startnode=ensemble_nodes[self.nodes.index(edge.edge_startnode)],
            endnode=ensemble_nodes[self.nodes.index(edge.edge_endnode)]) for edge in self.edges]

        # set spanning_tree nodes list
        spanning_tree.nodes = ensemble_nodes

        # set spanning_tree nodes list

        # sort list of edges between ensemble nodes
        sorted_edges = sorted(ensemble_edges, key=getKey)
        len_spanning_tree_edges = 0
        for edge in sorted_edges:
            # stopping condition of the algorithm
            if len_spanning_tree_edges == nb_noeuds-1:
                break

            # test whether the 2 nodes connected by the edges
            # belong to the same connected ensembles
            if edge.edge_startnode.get_root_and_compress() != edge.edge_endnode.get_root_and_compress():
                spanning_tree.add_edge2(edge,edge.edge_startnode, edge.edge_endnode)
                len_spanning_tree_edges =+ 1
                edge.edge_startnode.rank_union(edge.edge_endnode)

        return spanning_tree

    def prim(self,root):

        spanning_tree = Graph(name=self.graph_name + " Prim algorithm spanning tree")

        # Initialisation of a queue containing all nodes
        nodes_queue = PriorityMinQueue()

        for node in self.nodes:
            ensemble_node = EnsembleNode(name=node.node_name,
                                         data=node.node_data, min_weight=float('inf'), original_node=node)
            if node == root:
                ensemble_node.min_weight = 0
            spanning_tree.add_node(ensemble_node)
            nodes_queue.enqueue(ensemble_node)

        # exploring graph nodes
        while not nodes_queue.is_empty():
            tuple_father = nodes_queue.dequeue()

            if tuple_father.father:
                edge_add = self.adj_matrix[tuple_father.original_node][tuple_father.father.original_node]
                spanning_tree.add_edge2(edge_add, tuple_father, tuple_father.father)

            for key in self.adj_matrix[tuple_father.original_node].keys():

                for n in nodes_queue.items:

                    if (n.original_node == key) and\
                            (self.adj_matrix[tuple_father.original_node][key].edge_cost < n.min_weight):

                        adj_edge = self.adj_matrix[tuple_father.original_node][key]
                        # instead of searching the key by item for to get the adjacency matrix row,
                        # we used a tuple to avoid the search for the right key in every iteration
                        n.father = tuple_father
                        n.min_weight = adj_edge.edge_cost
                        break

        return spanning_tree

    def node_to_ensnode(self, root_node):
        for n in self.nodes:
            if n.original_node == root_node:
                return n

    def dfs(self, root_node):
        """
        Depth first search algorithm
        returns a sorted list of nodes to construct
        a cycle by linking the i and i+1 node
        """
        root = self.node_to_ensnode(root_node)
        cycle_nodes = []
        pile = Stack()
        pile.push(root)
        neighbor = None
        while not pile.is_empty():
            u = pile.pop()
            cycle_nodes.append(u)
            u.set_visited()
            for neighbor in self.adj_matrix[u].keys():
                if not neighbor.is_visited():
                    pile.push(neighbor)
        return cycle_nodes

    def rsl(self, root, st_algo):

        if st_algo =="prim":
            G = self.prim(root)

        elif st_algo == "kruskal":
            G = self.kruskal()
        else:
            raise ValueError("Unrecognized algorithm")
        # c_n cycle nodes
        c_n = G.dfs(root)
        cycle = Graph("tournee")
        cycle.nodes = self.nodes

        for i in xrange(len(c_n)-1):
            e = self.adj_matrix[c_n[i].original_node][c_n[i+1].original_node]

            cycle.add_edge(e)
        e = self.adj_matrix[c_n[-1].original_node][c_n[0].original_node]
        cycle.add_edge(e)
        return cycle

if __name__ == '__main__':

    G = Graph(name='Graphe test')
    for k in range(5):
        G.add_node(Node(name='Noeud test %d' % k))
    for k in range(5):
        G.add_edge(Edge(name='Edge test %d' % k, cost=(10-k)))

    print "liste non trié"
    print G.edges[0]
