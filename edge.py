# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:04:50 2016

@author: makhloufi, lacroix
"""
from node import Node


class Edge(object):
    """
    Une classe generique pour representer les arretes d'un graphe.
    """

    # On passe L ID du noeud de depart, et du noeud d arrivee
    def __init__(self, name='Sans nom',  data=None, startnode=None,
                 endnode=None, cost=0):
        self.__edge_name = name
        self.__edge_data = data
        self.__edge_cost = cost
        self.__edge_startnode = startnode
        self.__edge_endnode = endnode

    @property
    def edge_name(self):
        "Donne le nom de l arete."
        return self.__edge_name

    @property
    def edge_id(self):
        " Donne le numero d'identification de l arc."
        return self.__edge_id

    @property
    def edge_data(self):
        """Donne les donnees contenues dans le l'arc."""
        return self.__edge_data

    @property
    def edge_count(self):
        return self.__edge_count

    @property
    def edge_startnode(self):
        "Donne l ID du premier noeud de l arc"
        return self.__edge_startnode

    @property
    def edge_endnode(self):
        "Donne l ID du dernier noeud de l arc."
        return self.__edge_endnode

    @property
    def edge_cost(self):
        " Donne le cout de l arc"
        return self.__edge_cost

    @edge_name.setter
    def edge_name(self, name):
        "specifier le non du l arc"
        self.__edge_name = name

    @edge_data.setter
    def edge_data(self, data):
        "Spécifie les donnees de l arc."
        return self.__edge_data

    @edge_startnode.setter
    def edge_startnode(self, startnode):
        "specifie le premier noeud de l arc"
        self.__edge_startnode = startnode

    @edge_endnode.setter
    def edge_endnode(self, endnode):
        "Specifie le dernier noeud de l arc"
        self.__edge_endnode = endnode

    @edge_cost.setter
    def edge_cost(self, cost):
        "Spécifi le cout de l arc"
        self.__edge_cost = max(0, cost)

    def __repr__(self):
        id = self.edge_id
        name = self.edge_name
        data = self.__edge_data
        startnode = self.edge_startnode
        endnode = self.edge_endnode
        cost = self.edge_cost
        s = 'Edge %s (id : %d) (cost : %.2f) ' % (name, id, cost)
        s += 'start node : ' + repr(startnode) + ' end node : ' + \
            repr(endnode)
        s += ' (donnees: ' + repr(data) + ')\n'
        return s

if __name__ == '__main__':

    edges = []
    for k in range(5):
        edges.append(Edge())
    for edge in edges:
        print edge
