import sys
sys.path.append('../swiss_flows')

from node import Node
from flow import Flow

def main():
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
   main()
