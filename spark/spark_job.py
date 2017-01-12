from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext


def main():
    # /Library/Developer/spark-1.6.2-bin-hadoop2.6/bin/spark-submit --master local --packages com.databricks:spark-csv_2.11:1.5.0 spark_job.py

    # TODO Clean the tweets and save it to HDFS
    # TODO preprocess the tweets by filtering the users with only 1 tweet
    # TODO Generate nodes and save it to HDFS

    #tweets = pd.read_csv('../data/clean_tweets.csv', parse_dates=[2])
    #grouped = tweets.groupby('userId')

    tweets = sqlContext.read.load('../data/clean_tweets.csv',
                                    format='com.databricks.spark.csv',
                                    header='true',
                                    inferSchema='true')

    grouped = tweets.groupby('userId')

    t = sc.parallelize([('A', 1), ('B', 2)])
    #print(t.collectAsMap())
    t.foreach(f)


def f(row):
    print(row[0])
    print(row[1])

if __name__ == '__main__':
    sc = SparkContext()
    sqlContext = SQLContext(sc)
    main()
