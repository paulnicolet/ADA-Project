import pandas as pd
import pickle
import warnings
from haversine import haversine
import operator
import collections

class Node:
    """
    Represents a node, a city.

    Parameters:
        name name of the Node
        position (latitude, longitude)
        population population of the city
        canton canton string code
    """

    def __init__(self, name, position, population, canton=None, country=None):
        self.name = name
        self.position = position
        self.population = population
        self.radius = Node.__radius(population)
        self.canton = canton
        self.country = country

    @staticmethod
    def weight_nodes(weighted_flows):
        """
        Attribute a weight to each node (mainly for the visualization).

        Parameters:
            weighted_flows a list of flows, with weight.

        Returns:
            A list of tuple (Node, weight), sorted by weight in descending order.
        """

        weighted_nodes = collections.defaultdict(int)

        for flow in final_flows:
            weighted_nodes[flow.src] += flow.weight
            weighted_nodes[flow.dst] += flow.weight

        return sorted(weighted_nodes.items(),
                      key=operator.itemgetter(1),
                      reverse=True)

    @staticmethod
    def locate_point(point, nodes):
        """
        Find the best corresponding node to the point in the given list.

        Parameters:
            point Point to evaluate.
            nodes List of nodes.

        Returns:
            The best node in the list or None if not considered in a node.
        """

        best_dist = 10000
        best_node = None

        for node in nodes:
            dist = haversine(point, node.position)

            # Take the closest node, make sure the point is in the city circle
            if dist < best_dist and dist < node.radius:
                best_dist = dist
                best_node = node

        return best_node

    @staticmethod
    def generate_nodes(n_swiss_nodes=10,
                       n_foreign_nodes=10,
                       pop_threshold=15000,
                       save=False):
        """
        Generate all the nodes, swiss and foreign
        and save it to a file nodes_<n_swiss_nodes>_<n_foreign_nodes>.pkl
        in the data/ directory.
        If the file already exists, simply return the list of nodes.
        See 'foreign nodes.ypnb' notebook for the detailed process.

        Parameters:
            n_swiss_nodes Number of swiss nodes to generate.
            n_foreign_nodes Number of node to generate for each foreign country.
            pop_threshold Population threshold for foreign cities.

        Returns:
            list of nodes
        """
        base = '../data/nodes/nodes_{}_{}.pkl'
        filepath = base.format(n_swiss_nodes, n_foreign_nodes)

        # Check if the file already exists
        nodes = Node.__pickle_try_load(filepath)
        if nodes:
            return nodes

        # Generate swiss nodes
        swiss_nodes = Node.generate_swiss_nodes(n_nodes=n_swiss_nodes,
                                                save=save)

        # Define the neighboring countries
        countries = ['FR', 'IT', 'DE', 'AT']

        nodes = swiss_nodes
        for country in countries:
            df = Node.import_country(country)

            # Keep cities with pop > pop_threshold
            df = df[df['population'] > pop_threshold]

            # Create the new distance feature
            find_node = lambda x: Node.__find_closest_node(x['latitude'],
                                                           x['longitude'],
                                                           swiss_nodes)
            df['distance'] = df.apply(find_node, axis=1)

            # Sort rows by distance
            df = df.sort_values(by='distance', ascending=True)

            # Take the desired number
            if df.shape[0] < n_foreign_nodes:
                template = '{} nodes requested, {} nodes max, returns {} nodes'
                msg = template.format(n_foreign_nodes, df.shape[0], df.shape[0])
                warnings.warn(msg, UserWarning)

            df = df[:n_foreign_nodes]

            # Generate the nodes
            for row in df.iterrows():
                args = {'name': row[1].asciiname,
                        'position': (row[1].latitude, row[1].longitude),
                        'population': row[1].population,
                        'canton': row[1]['admin1 code'],
                        'country': country}

                nodes.append(Node(**args))

        # Save and return the result
        if save:
            with open(filepath, 'wb') as file:
                pickle.dump(nodes, file)

        return nodes

    @staticmethod
    def generate_swiss_nodes(n_nodes=10, save=False):
        """
        Generate the swiss nodes
        and save it to a file swiss_nodes_<n_nodes>.pkl in the data/ directory.
        If the file already exists, simply return the list of nodes.
        See 'nodes.ypnb' notebook for the detailed process.

        Parameters:
            n_nodes Number of nodes to generate.

        Returns:
            list of nodes
        """
        filepath = '../data/nodes/swiss_nodes_{}.pkl'.format(n_nodes)

        # Check if the file already exists
        nodes = Node.__pickle_try_load(filepath)
        if nodes:
            return nodes

        # Get the swiss cities
        df = Node.import_country('CH')

        # Sort rows by population and take the n_nodes first
        df = df.sort_values(by='population', ascending=False)
        if df.shape[0] < n_nodes:
            template = '{} nodes requested, {} nodes max, returns {} nodes'
            msg = template.format(n_nodes, df.shape[0], df.shape[0])
            warnings.warn(msg, UserWarning)

        df = df[:n_nodes]

        # Generate the list of node
        nodes = []
        for row in df.iterrows():
            args = {'name': row[1].asciiname,
                    'position': (row[1].latitude, row[1].longitude),
                    'population': row[1].population,
                    'canton': row[1]['admin1 code'],
                    'country': 'CH'}

            nodes.append(Node(**args))

        # Save the result
        if save:
            with open(filepath, 'wb') as file:
                pickle.dump(nodes, file)

        return nodes

    @staticmethod
    def import_country(country_code):
        """
        Import the country data, clean it and keep the cities.

        Parameters:
            country_code For example CH, or FR...

        Returns:
            Pandas Dataframe with cities.
        """
        # Import data
        FILE_BASE = '../data/geonames/{}/{}.txt'
        df = pd.read_csv(FILE_BASE.format(country_code, country_code),
                         header=None,
                         encoding='utf8',
                         delimiter='\t',
                         dtype={9: str})

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

        return df

    def dist(self, other):
        """ Returns the distance between two nodes in kilometers. """
        return haversine(self.position, other.position)

    @staticmethod
    def __radius(pop):
        """ Returns the radius of a city from the population. """
        if pop >= 300000:
            return 12
        elif pop >= 100000:
            return 10
        elif pop >= 40000:
            return 8
        else:
            return 5

    @staticmethod
    def __find_closest_node(lat, lon, nodes):
        """ Find the closest node and return the distance. """
        tmp = Node('tmp', (lat, lon), 0, None)

        best_dst = 99999999
        for node in nodes:
            dst = tmp.dist(node)
            best_dst = dst if dst < best_dst else best_dst

            return best_dst

    @staticmethod
    def __pickle_try_load(filepath):
        """ Look if the file already exists. """
        try:
            with open(filepath, 'rb') as file:
                warnings.warn('File already exists, importing ...', UserWarning)
                nodes = pickle.load(file)
            return nodes
        except FileNotFoundError:
                return None

    def __str__(self):
        return '[Node] {}, {}, {}, {}, {} km, {} people'.format(self.name,
                                                    self.country,
                                                    self.canton,
                                                    self.position,
                                                    self.radius,
                                                    self.population)

    def __eq__(self, other):
        cond = (self.__dict__ == other.__dict__)
        return isinstance(other, type(self)) and cond

    def __hash__(self):
        return ((hash(self.name) ^
                 hash(self.position) ^
                 hash(self.canton) ^
                 hash(self.country))
                + self.population
                + self.radius)
