from haversine import haversine

class Node:
    """
    Represents a node, a city.

    Parameters:
        name name of the Node
        position (latitude, longitude)
        population population of the city
        canton canton string code
    """

    def __init__(self, name, position, population, canton):
        self.name = name
        self.position = position
        self.population = population
        self.radius = 10
        self.canton = canton

    def dist(self, other):
        """ Return the distance between two nodes in kilometers. """
        return haversine(self.position, other.position)

    @staticmethod
    def generate_nodes():
        pass

    def __str__(self):
        return '[Node] {}, {}, {}, radius = {}.'.format(self.name,
                                                        self.canton,
                                                        self.position,
                                                        self.radius)
