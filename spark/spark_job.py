from pyspark import SparkContext
from pyspark.sql import SQLContext
import pandas as pd
import pickle
import json
import itertools
import os
import sys
sys.path.append('../swiss_flows')
from node import Node
from flow import Flow

def main():
    # Import the tweets and transform the data
    df = sqlContext.read.json(os.path.join(PATH_BASE, 'filtered_users.json'))
    map_row = lambda row: (row.userId, list(map(_convert_types, row.tweets)))
    user_tweets = df.rdd.map(map_row)

    # Generate nodes as a broadcast variable
    nodes = sc.broadcast(Node.generate_nodes(n_swiss_nodes=10,
                                             n_foreign_nodes=1,
                                             pop_threshold=15000))
    detect_interval = 2
    directed = False

    # Detect tweets on each cluster machine
    flows = user_tweets.flatMap(lambda x: Flow.infer_flows(x[0], x[1], nodes.value, detect_interval, directed))

    # Aggregate results for each Flow
    agg_flows = flows.reduceByKey(Flow.reduce_flows_helper)

    # Build the final Flow objects from attributes
    final_flows = agg_flows.map(lambda x: Flow.build_final_flows(x[0], x[1]))

    # Generate node weights
    weighted_nodes = final_flows.flatMap(lambda x: [(x.src, x.weight), (x.dst, x.weight)])
    weighted_nodes = weighted_nodes.reduceByKey(lambda a, b: a + b)
    weighted_nodes = weighted_nodes.map(lambda x: {'node': x[0], 'weight': x[1]})

    # Save the results
    json_mapper = lambda x: json.dumps(x, default=lambda y: y.json)
    final_flows.map(json_mapper).saveAsTextFile(os.path.join(PATH_BASE, 'results', 'final_flows.json'))
    weighted_nodes.map(json_mapper).saveAsTextFile(os.path.join(PATH_BASE, 'results', 'final_nodes.json'))


def _convert_types(tweet):
    tweet[1] =  pd.Timestamp(tweet[1])
    tweet[2] = float(tweet[2])
    tweet[3] = float(tweet[3])

    return tweet

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
    sqlContext = SQLContext(sc)
    main()

# Run job locally
# /Library/Developer/spark-1.6.2-bin-hadoop2.6/bin/spark-submit --master local spark_job.py
# Run job on the cluster
# Uncomment environment variables
# /Library/Developer/spark-1.6.2-bin-hadoop2.6/bin/spark-submit --master yarn spark_job.py
