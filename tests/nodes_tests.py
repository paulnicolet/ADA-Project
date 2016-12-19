import sys
sys.path.append('../swiss_flows')

from node import Node
from flow import Flow
import unittest

class TestNodes(unittest.TestCase):

    def test_locate_point(self):
        print('-- test_locate_point --')
        # Generate 10 nodes, Lausanne is in the list
        print('Creating 10 nodes...')
        nodes = Node.generate_nodes(n_nodes=10)

        # Create a node close to Lausanne
        print('Creating a node close to Lausanne...')
        name = 'Somewhere close to Lausanne'
        city = Node(name=name, position=(46.5375, 6.4917), population=10, canton='VD')

        # Perform the search
        print('Performing the search...')
        best = Node.locate_point(point=city.position, nodes=nodes)
        print('Best node found : {}.'.format(best))

        self.assertEqual(best.name, 'Lausanne')

    def test_generate_nodes(self):
        print('-- test_generate_nodes --')
        n_nodes = [10, 100, 3000]

        for n in n_nodes:
            print('Testing with {} nodes...'.format(n))
            print('\t Creating the list...')
            nodes = Node.generate_nodes(n_nodes=n)
            print('\t First node : {}, length : {}'.format(nodes[0], len(nodes)))
            print('\t Trying to create it again...')
            nodes = Node.generate_nodes(n_nodes=n)
            print('\t First node : {}, length : {}'.format(nodes[0], len(nodes)))

if __name__ == '__main__':
    unittest.main()
