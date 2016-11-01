# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 20:04:50 2016

@author: makhloufi, lacroix
"""
import random


class Node(object):
    """
    Une classe generique pour representer les noeuds d'un graphe.
    """

    def __init__(self, name='Sans nom', data=None):
        self.__node_name = name
        if data is not None:
            self.__node_data = data
        else:
            self.__node_data = (random.random() * 1000, random.random() * 1000)

    @property
    def node_count(self):
        return self.__node_count

    @property
    def node_name(self):
        "Donne le nom du noeud."
        return self.__node_name

    @property
    def node_id(self):
        """Donne le numéro d'identification du noeud."""
        return self.__node_id

    @property
    def node_data(self):
        """Donne les données contenues dans le noeud."""
        return (self.__node_data)

    @node_name.setter
    def node_name(self, name):
        """spécifie le nom du noeud"""
        self.__node_name = name

    @node_data.setter
    def node_data(self, data):
        """"Pour specifier les donnees du noeuds"""
        self.__node_data = data

    def __repr__(self):
        name = self.node_name
        data = self.node_data
        s = 'Noeud %s ' + name
        s += ' (donnees: ' + repr(data) + ')'
        return s

if __name__ == '__main__':

    nodes = []
    for k in range(9):
        nodes.append(Node())

    for node in nodes:
        print node