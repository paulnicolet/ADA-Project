import pandas as pd
import numpy as np
import pickle
import json
import csv

def clean_tweets(file_path, tosave_path):
	"""
	Clean the tweet data set to keep only the desired features and save the result.

	Parameters:
		file_path 	The path of the original file.
		tosave_path Path of the new csv file to save.

	Returns:
		The dataframe of clean tweets.
	"""
	# Load the schema
	SCHEMA_PATH = '../data/twitter-swisscom/schema.txt'
	schema = pd.read_csv(SCHEMA_PATH, delim_whitespace=True, header=None)

	# Load the dirty tweets
	df = pd.read_csv(file_path, sep='\t',
								encoding='utf-8',
								escapechar='\\',
								quoting=csv.QUOTE_NONE,
								names=schema[1],
								na_values='N')

	# Keep only the useful columns
	useful_col = ['id', 'userId', 'createdAt',
				  'placeLongitude', 'placeLatitude']
	df = df[useful_col]

	# Drop rows which have missing values in important columns
	imp_col = ['userId', 'createdAt', 'placeLatitude', 'placeLatitude']
	df = df.dropna(subset=imp_col, how='any')

	# Write in a file
	df.to_csv(tosave_path + '.csv', index=False)

	return df

def filter_users(clean_tweets_path, save=False, tosave_path=None, tosave_format='pickle'):
	"""
	Keep only users with more than one tweet and save them
	as a dictionnary of the form {'user_id': [list of tweets]}

	Parameters:
		clean_tweets_path 	Path of the clean tweets to treat.
		tosave_path 		Path of the .pkl to save.

	Returns:
		The dictionnary of tweets mapped to their user.
	"""
	# Load the clean tweets
	df = pd.read_csv(clean_tweets_path, parse_dates=[2])

	# Group by user id
	grouped = df.groupby('userId')

	user_tweets = {}

	# Filter users and update dictionnary
	for user, tweets in grouped:
		if tweets.shape[0] > 1:
			user_tweets[user] = tweets.drop('userId', axis=1).values.tolist()

	if save:
		if tosave_format == 'pickle':
			with open(tosave_path + '.pkl', 'wb') as file:
				pickle.dump(user_tweets, file)

		elif tosave_format == 'json':
			data = list(map(lambda x: {'userId': x[0], 'tweets': x[1]}, user_tweets.items()))
			with open(tosave_path + '.json', 'w') as file:
				json.dump(data, file, default=str)

	return user_tweets
