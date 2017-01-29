from math import radians, cos, sin, asin, sqrt
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

def haversine(point1, point2):
    """
    Calculate the distance between two points.
    Thanks to: https://github.com/mapado/haversine.
    We originally used the package but it's not installed on the cluster.
    """
    AVG_EARTH_RADIUS = 6371

    lat1, lng1 = point1
    lat2, lng2 = point2

    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))

    return h  # in kilometers
