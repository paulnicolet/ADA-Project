import pandas as pd
import numpy as np
import pickle
import os
import csv
import sys

def clean_tweets(filename):

	# Load the dirty tweets
	# Taken from Slack: https://adaepfl.slack.com/archives/twitter/p1480527805000002
	data_path = os.path.dirname('__file__') + '../data/twitter-swisscom/sample.tsv'
	df = pd.read_csv(data_path, sep="\t",encoding='utf-8', escapechar='\\', quoting=csv.QUOTE_NONE, header=None, na_values='N')

	# Load the schema
	schema_path = os.path.dirname('__file__') + '../data/twitter-swisscom/schema.txt'
	schema = pd.read_csv(schema_path, delim_whitespace=True, header=None)

	# Assign column names
	df.columns = schema[1]

	# Keep only the useful columns
	useful_col = ['id', 'userId', 'createdAt', 'placeLongitude', 'placeLatitude']
	df = df[useful_col]

	# Drop rows which have missing values in important columns
	imp_col = ['userId', 'createdAt', 'placeLatitude', 'placeLatitude']
	df = df.dropna(subset=imp_col, how='any')

	# Write in a file
	df.to_csv(filename + '.csv', index=False)

	return df

def filter_users(df):
	grouped = df.groupby('userId')

	user_tweets = {}

	for user, tweets in grouped:
		if tweets.shape[0] > 1:
			user_tweets[user] = tweets.drop('userId', axis=1).values.tolist()

	# Save the result
	with open('../data/filtered_users.pkl', 'wb') as file:
		pickle.dump(user_tweets, file)
