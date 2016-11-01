class Queue(object):
    "Une implementation de la structure de donnees << file >>."

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        "Ajoute `item` a la fin de la file."
        self.items.append(item)

    def dequeue(self):
        "Retire l'objet du debut de la file."
        return self.items.pop(0)

    def is_empty(self):
        "Verifie si la file est vide."
        return (len(self.items) == 0)

    def __contains__(self, item):
        return (item in self.items)

    def __repr__(self):
        return repr(self.items)


class PriorityQueue(Queue):

    def dequeue(self):
        "Retire l'objet ayant la plus haute priorite."
        highest = self.items[0]
        for item in self.items[1:]:
            if item > highest:
                highest = item
        idx = self.items.index(highest)
        return self.items.pop(idx)


# Les items de priorite nous permettent d'utiliser min() et max().

class PriorityMinQueue(Queue):

    def dequeue(self):
        "Retire l'objet ayant la plus petite priorite."
        return self.items.pop(self.items.index(min(self.items)))


class PriorityMaxQueue(Queue):

    def dequeue(self):
        "Retire l'objet ayant la plus haute priorite."
        return self.items.pop(self.items.index(max(self.items)))
