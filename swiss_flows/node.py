import pandas as pd
import pickle
import warnings
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

    def __str__(self):
        return '[Node] {}, {}, {}, radius = {}.'.format(self.name,
                                                        self.canton,
                                                        self.position,
                                                        self.radius)

    @staticmethod
    def generate_nodes(n_nodes=10):
        """
        Generate the nodes
        and save it to a file nodes_<n_nodes>.pkl in the data/ directory.
        If the file already exists, simply return the list of nodes.
        See nodes.ypnb notebook for the detailed process.

        Parameters:
            n_nodes Number of nodes to generate.
        """
        filepath = '../data/nodes_{}.pkl'.format(n_nodes)

        # Look if the file already exists
        try:
            with open(filepath, 'rb') as file:
                warnings.warn('File already exists, importing ...', UserWarning)
                nodes = pickle.load(file)
            return nodes
        except FileNotFoundError:
                pass

        # Import data
        df = pd.read_csv('../data/CH/CH.txt', header=None, encoding='utf8',
                                              delimiter='\t', dtype={9: str})

        # Build the index
        index = ['geonameid', 'name', 'asciiname', 'alternatenames',
                 'latitude', 'longitude', 'feature class', 'feature code',
                 'country code', 'cc2', 'admin1 code', 'admin2 code',
                 'admin3 code', 'admin4 code','population', 'elevation', 'dem',
                 'timezone', 'modification date']

        df.columns = index

        # Drop null population, keep cities, drop useless columns
        df = df[df['population'] != 0]
        df = df[df['feature code'].str.contains(r'PPL(A\d?|C)?$')]
        df = df[['asciiname', 'latitude', 'longitude', 'admin1 code',
                'feature code','population']]

        # Sort rows by population and take the n_nodes first
        df = df.sort_values(by='population', ascending=False)
        if df.shape[0] < n_nodes:
            warnings.warn(
                '{} nodes requested, {} nodes max, returns {} nodes'.format(n_nodes, df.shape[0], df.shape[0]),
                UserWarning)

        df = df[:n_nodes]

        # Generate the list of node
        nodes = []
        for row in df.iterrows():
            args = {'name': row[1].asciiname,
                    'position': (row[1].latitude, row[1].longitude),
                    'population': row[1].population,
                    'canton': row[1]['admin1 code']}

            nodes.append(Node(**args))

        # Save the result
        with open(filepath, 'wb') as file:
            pickle.dump(nodes, file)

        return nodes
