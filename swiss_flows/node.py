from haversine import haversine

class Node:
    """
    Represents a node, a city.

    Parameters:
        name name of the Node
        point (latitude, longitude)
        population population of the city
    """

    def __init__(self, name, point, population):
        self.name = name
        self.position = point
        self.population = population
        self.radius = 10

    def dist(self, other):
        """ Return the distance between two nodes in kilometers. """
        return haversine(self.position, other.position)

    @staticmethod
    def generate_nodes():
        pass

    def __str__(self):
        return '[Node] {}, {}, radius = {}.'.format(self.name,
                                                   self.position,
                                                   self.radius)
