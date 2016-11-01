from node import Node
import warnings


class EnsembleNode(Node):
    """
    This class extends Node class allowing nodes to
    have reference (father attribute) to their parent node.
    EnsembleNode objects with father reference between
    each other define a set of linked ensemble
    or tree if the structure doesn't show cycles
    """

    def __init__(self, name='Sans nom', data=None, father=None, min_weight=None):
        Node.__init__(self, name, data)
        # if father is None:
        #     self.__father = self
        # else:
        self.__father = father
        self.__min_weight = min_weight
        self.__rank = 0

    @property
    def father(self):
        return self.__father

    @property
    def rank(self):
        return self.__rank

    @property
    def min_weight(self):
        return self.__min_weight

    @father.setter
    def father(self, father):
        self.__father = father

    @rank.setter
    def rank(self, rank):
        self.__rank = rank

    @min_weight.setter
    def min_weight(self, min_weight):
        self.__min_weight = min_weight

    def get_root(self):
        """
        Iterative function that returns the root of
        the linked ensemble/tree the node belongs to
        """
        while not parent.is_root():
            parent = parent.father
        return parent
    
    def get_root_and_compress(self):
        """
        Iterative function that returns the root of
        the linked ensemble/tree the node belongs to and 
        compress at the same time the research path
        """
        parent = self
        parents = []
        while not parent.is_root():
             parents.append(parent)
             parent = parent.father
        root = parent

        # Set father of met nodes to the root af the linked component
        for parent in parents:
            parent.father = root
        
        return root

    def is_root(self):
        """
        Returns true if the node is the root of
        the linked ensemble/tree it belongs to, else false
        """
        return (self.__father == None)

    def __lt__(self, other):
        """methode pour comparer les noeuds < """
        return self.min_weight < other.min_weight

    def __le__(self, other):
        """methode pour comparer les noeuds < """
        return self.min_weight <= other.min_weight

    def __gt__(self, other):
        """methode pour comparer les noeuds < """
        return self.min_weight > other.min_weight

    def __ge__(self, other):
        return self.min_weight >= other.min_weight

    def union(self, otherEnsembleNode):
        """
        This function modifies the linked nodes ensemble so that
        the 2 linked nodes ensembles/trees (the one self belongs to and
        the one otherEnsembleNode belong to) become connected
        """
        own_root = self.get_root()
        other_root = otherEnsembleNode.get_root()
        
        # The node and otherEnsembleNode must belong
        # to different nodes linked ensembles
        if own_root == other_root:
            raise ValueError("Nodes belong to the same linked ensembles")
        else:
            other_root = own_root

    def rank_union(self, otherEnsembleNode):
        """
        This function modifies the linked nodes ensemble so that
        the 2 linked nodes ensembles/trees (the one self belongs to and
        the one otherEnsembleNode belong to) become connected
        """
        own_root = self.get_root_and_compress()
        other_root = otherEnsembleNode.get_root_and_compress()

        if own_root.rank == other_root.rank:
            other_root.father = own_root
            other_root.rank = other_root.rank + 1
        elif own_root.rank > other_root.rank:
            other_root.father = own_root
        else:
            own_root.father = other_root

    def __repr__(self):
        fatherNode = self.father
        s = Node.__repr__(self)
        s += " and with father node " + Node.__repr__(fatherNode)
        return s
