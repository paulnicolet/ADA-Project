import pickle
import warnings

def pickle_try_load(filepath):
    """ Look if the file already exists. """
    try:
        with open(filepath, 'rb') as file:
            warnings.warn('File already exists, importing ...', UserWarning)
            data = pickle.load(file)
        return data
    except FileNotFoundError:
            return None
