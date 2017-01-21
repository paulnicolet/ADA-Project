from pyspark import SparkContext
import pickle
import itertools
import os
import sys
sys.path.append('../swiss_flows')
from node import Node
from flow import Flow

def main():
    # /Library/Developer/spark-1.6.2-bin-hadoop2.6/bin/spark-submit --master local spark_job.py

    # TODO clean_tweets()   --> save it to HDFS
    # TODO filter_users()   --> save it to HDFS
    # TODO generate_nodes() --> save it to HDFS


    # Path to write to HDFS : 'hdfs://iccluster046.iccluster.epfl.ch/user/pnicolet/test.txt'

    with open('../data/filtered_users.pkl', 'rb') as file:
        user_tweets = pickle.load(file)

    nodes = Node.generate_nodes(n_swiss_nodes=10, n_foreign_nodes=1, pop_threshold=15000)

    # RDD as [(userId, [[t1], [t2]])] with ti = [id, Timestamp, long, lat]
    #user_tweets = sc.broadcast([(key, value) for key, value in user_tweets.items()])

    user_flows = sc.parallelize([(key, value) for key, value in user_tweets.items()])

    #print(user_flows.take(5))

    lol = user_flows.map(lambda x: detect(x, nodes, 2, False)).filter(lambda x: len(x[1]) > 0)

    print(lol.collect())


def detect(entry, nodes, l, directed):
    print('-------------- DETECT ----------------')
    user = entry[0]
    tweet_info = entry[1]

    # Generate all possible pairs of tweet sorted by interval length
    pairs = sorted(list(itertools.combinations(tweet_info, 2)), key=by_interval_len)

    # {f1 : {weight:1, intervals:[interval1, interval2...]}}
    flows = {}
    for id_pair in pairs:

        # [id, Timestamp, lon, lat]
        t1 = id_pair[0]
        t2 = id_pair[1]

        # Nodes corresponding to the tweets
        n1 = Node.locate_point((t1[3], t1[2]), nodes)
        n2 = Node.locate_point((t2[3], t2[2]), nodes)

        # Time interval condition
        time1 = t1[1].to_pydatetime()
        time2 = t2[1].to_pydatetime()
        ts1 = time1 if time1 < time2 else time2
        ts2 = time2 if time1 < time2 else time1
        tweet_interval = (ts1, ts2)
        time_cond = (ts2 - ts1).days <= l

        # Node conditions
        geo_cond = n1 and n2 and (n1 != n2)

        if time_cond and geo_cond:
            # Build the flow
            src = n1
            dst = n2

            if directed:
                if time1 < time2 and time1.time() < time2.time():
                    src = n1
                    dst = n2
                elif time2 < time1 and time2.time() < time1.time():
                    src = n2
                    dst = n1
                else:
                    # Cannot conclude
                    continue

            flow = Flow(src=src, dst=dst, directed=directed)

            overlap = False
            if flow in flows:
                # Look for overlapping flows
                for interval in flows[flow]['intervals']:
                    if Flow.is_overlapping(tweet_interval, interval):
                        overlap = True
                        break

            else:
                # Add the initial values if it's a new flow
                flows[flow] = {'weight': 1, 'intervals': [], 'start':ts1, 'end':ts2}

            # If no overlap, then it's not the exact same flow
            if not overlap:
                # Update start date
                flows[flow]['start'] = min(ts1, flows[flow]['start'])

                # Update end date
                flows[flow]['end'] = max(ts2, flows[flow]['end'])

                # Update weight
                flows[flow]['weight'] += 1

            # In any case, add the interval we just found for later use
            flows[flow]['intervals'].append(tweet_interval)

    return (user, flows)

def by_interval_len(tweet_tuple):
    tmp1 = tweet_tuple[0]
    tmp2 = tweet_tuple[1]

    # Order the tweet by timestamp
    t1 = tmp1 if tmp1[1].to_pydatetime() < tmp2[1].to_pydatetime() else tmp2
    t2 = tmp2 if tmp1[1].to_pydatetime() < tmp2[1].to_pydatetime() else tmp1

    # Return the length of the interval
    return t2[1].to_pydatetime() - t1[1].to_pydatetime()

if __name__ == '__main__':
    base = [os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'swiss_flows']
    files = [os.path.join(*base.append('flow.py')),
               os.path.join(*base.append('node.py'))]

    sc = SparkContext(pyFiles=files)
    main()
