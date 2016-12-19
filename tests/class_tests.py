import sys
sys.path.append('../swiss_flows')

from node import Node
from flow import Flow
import unittest

class TestClasses(unittest.TestCase):

    def test_node(self):
        node = Node('NoName', (45, 15), 1000, ':)')
        print(node)
        self.assertEqual(node.name, 'NoName')
        self.assertEqual(node.position, (45, 15))

    def test_flow(self):
        node1 = Node('Source', (45, 15), 1000, ':)')
        node2 = Node('Destination', (46, 16), 1000, ':)')
        undir_flow = Flow(node1, node2)
        dir_flow = Flow(node1, node2, directed=True)

        print(undir_flow)
        print(dir_flow)

        self.assertEqual(dir_flow.src, node1)
        self.assertEqual(dir_flow.dst, node2)

if __name__ == '__main__':
    unittest.main()
