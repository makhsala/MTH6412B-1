# -*- coding: utf-8 -*-
"""
Arbre a cout minimum

@author: makhloufi, lacroix
"""
from node import Node


class ACM(Node):
    """
    En ajoutant a la classe Node un attribut set pour obtenir les parents
    (les ancetres les plus proches). on peut obtenir tout l arbre ascendant
    en parcourant les ancetres de chaque parents
     """
    def __init__(self, name='Sans nom', data=(0, 0), acm_parent=None):

        Node.__init__(self, name, data)

        if acm_parent is None:
            self.acm_parent = set([self])
        else:
            self.acm_parent = acm_parent

    @property
    def acm_parent(self):
        return self.__acm_parent

    @acm_parent.setter
    def acm_parent(self, set_nodes):
        self.__acm_parent = set_nodes

    def update_parents(self, cc):
        """on met a jour tout les parents du noeud """
        for n in self.acm_parent:
            n.acm_parent = n.acm_parent | cc
