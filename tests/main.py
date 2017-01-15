import sys
sys.path.append('../swiss_flows')

from node import Node
from flow import Flow
from cleaning import filter_users

def run(custom_conf=True):
    if custom_conf:
        conf = ask_conf()
    else:
        conf = {
            'tweets_path': '../data/clean_tweets.csv',
            'delta_t': 2,
            'directed': False,
            'n_swiss_nodes': 10,
            'n_foreign_nodes': 2,
            'pop_threshold': 15000,
            'save_nodes': False
        }

    print('\t Generating nodes...')
    nodes = Node.generate_nodes(n_swiss_nodes=conf['n_swiss_nodes'],
                                n_foreign_nodes=conf['n_foreign_nodes'],
                                pop_threshold=conf['pop_threshold'],
                                save=conf['save_nodes'])

    print('> Starting main algorithm')

    print('\t Filtering users with 1 single tweet...')
    user_tweets = filter_users(conf['tweets_path'])

    print('\t Detecting flows...')

    flows = []
    for user_id, tweets in user_tweets.items():
        tmp = Flow.infer_flows(user_id,
                               tweets,
                               nodes,
                               conf['delta_t'],
                               conf['directed'])
        flows.append(tmp)

    final_flows = Flow.agg_flows(flows)

    print('> Result')
    print('{} flows detected.'.format(len(final_flows)))

    for f in final_flows:
        print(f)

def ask_conf():
    if input('> Run with sample data ? (y/n) ') == 'y':
        tweets_path = '../data/clean_tweets.csv'
    else:
        tweets_path = '../data/clean_tweets_full.csv'

    print('> Flow configutation')
    delta_t = int(input('\t Enter the time interval, in days, to consider 2 tweets as potential flow: '))
    directed = input('\t Do you want to detect directed flows ? (y/n) ') == 'y'

    print('> Node configutation')
    n_swiss_nodes = int(input('\t Enter the number of Swiss node to consider: '))
    n_foreign_nodes = int(input('\t Enter the number of foreign node to consider for each country: '))
    pop_threshold = int(input('\t Enter the population threshold to consider for foreign countries: '))
    save_nodes = input('\t Do you want to save the generated nodes ? (y/n) ') == 'y'

    return {
        'tweets_path': tweets_path,
        'delta_t': delta_t,
        'directed': directed,
        'n_swiss_nodes': n_swiss_nodes,
        'n_foreign_nodes': n_foreign_nodes,
        'pop_threshold': pop_threshold,
        'save_nodes': save_nodes
    }

if __name__ == '__main__':
    run()
