import sys
sys.path.append('../swiss_flows')

from node import Node
from flow import Flow

def main():
    node1 = Node('Source', (45, 15), 1000)
    node2 = Node('Destination', (46, 16), 1000)
    undir_flow = Flow(node1, node2)
    dir_flow = Flow(node1, node2, directed=True)

    print(node1)
    print(node2)
    print(undir_flow)
    print(dir_flow)

    print('Distance between the two nodes : {} km.'.format(node1.dist(node2)))


if __name__ == '__main__':
   main()
