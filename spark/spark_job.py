from pyspark import SparkContext
import pandas as pd
import pickle
import itertools
import os
import sys
sys.path.append('../swiss_flows')
from node import Node
from flow import Flow

def main():
    # Get filtered tweets
    with open(os.path.join(PATH_BASE, 'filtered_users.pkl'), 'rb') as file:
        user_tweets = pickle.load(file)

    # Generate nodes as a broadcast variable
    nodes = sc.broadcast(Node.generate_nodes(n_swiss_nodes=10,
                                             n_foreign_nodes=1,
                                             pop_threshold=15000))
    detect_interval = 2
    directed = False

    # RDD (user_id, [tweets])
    user_tweets = sc.parallelize(list(user_tweets.items()))

    # Detect tweets on each cluster machine
    flows = user_tweets.flatMap(lambda x: Flow.infer_flows(x[0], x[1], nodes.value, detect_interval, directed))

    # Aggregate results for each Flow
    agg_flows = flows.reduceByKey(Flow.reduce_flows_helper)

    # Build the final Flow objects from attributes
    final_flows = agg_flows.map(lambda x: Flow.build_final_flows(x[0], x[1]))

    #print(agg_flows.take(5))
    result = sorted(final_flows.collect(), reverse=True, key=lambda x: x.weight)

    for flow in result:
        print(flow)

    # TODO Save agg flows to HDFS.


# Constants set up
LOCAL = True
HOSTNAME = 'hdfs://iccluster046.iccluster.epfl.ch'
if LOCAL:
    PATH_BASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'data')
else:
    PATH_BASE = os.path.join(HOSTNAME, 'user', 'pnicolet')

# Spark set up
if __name__ == '__main__':
    base = [os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'swiss_flows']
    print(base)
    files = [os.path.join(*(base + ['flow.py'])),
             os.path.join(*(base + ['node.py'])),
             os.path.join(*(base + ['utils.py']))]

    sc = SparkContext(pyFiles=files)
    main()

# Run job locally
# /Library/Developer/spark-1.6.2-bin-hadoop2.6/bin/spark-submit --master local spark_job.py
# Run job on the cluster
# Uncomment environment variables
# /Library/Developer/spark-1.6.2-bin-hadoop2.6/bin/spark-submit --master yarn spark_job.py
