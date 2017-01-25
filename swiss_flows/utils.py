import pickle
import warnings
import pandas as pd

def pickle_try_load(filepath):
    """ Look if the file already exists. """
    try:
        with open(filepath, 'rb') as file:
            warnings.warn('File already exists, importing ...', UserWarning)
            data = pickle.load(file)
        return data
    except FileNotFoundError:
            return None

def convert_tweet_types(tweet):
    """Convert types of tweets. Useful when loading data from JSON files."""
    tweet[1] =  pd.Timestamp(tweet[1])
    tweet[2] = float(tweet[2])
    tweet[3] = float(tweet[3])

    return tweet
