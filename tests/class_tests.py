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

    def test_compare(self):
        node1 = Node('Source', (45, 15), 1000, ':)')
        node2 = Node('Source', (45, 15), 1000, ':)')
        node3 = Node('Destination', (46, 16), 1000, ':)')

        self.assertTrue(node1 == node2)
        self.assertFalse(node1 == node3)

        flow1 = Flow(node1, node3)
        flow2 = Flow(node1, node3)
        flow3 = Flow(node1, node2)

        self.assertTrue(flow1 == flow2)
        self.assertFalse(flow1 == flow3)

    def test_hash(self):
        names = ['1', '2', '3']
        pops = [10, 100, 1000]
        pos = (10, 10)

        for name in names:
            for pop in pops:
                node1 = Node(name, pos, pop)
                node2 = Node(name, pos, pop)
                self.assertTrue(hash(node1) == hash(node2))

        n1 = Node('test1', pos, 100)
        n2 = Node('test2', pos, 1000)
        print(hash(n1))
        flow1 = Flow(src=n1, dst=n2)
        flow2 = Flow(src=n1, dst=n2)
        print(hash(flow1))
        self.assertTrue(hash(flow1) == hash(flow2))

if __name__ == '__main__':
    unittest.main()
