import numpy as np
import pandas as pd

import paths

from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.externals import joblib


def load_listeners(csv_path, binary=True):
    listeners = pd.read_csv(csv_path, index_col="artist")
    listeners.fillna(0, inplace=True)
    if binary:
        listeners[listeners > 0] = 1
    return listeners


def normalize_listeners(listeners):
    magnitudes = np.sqrt(listeners.pow(2).sum())
    listeners = listeners.divide(magnitudes)
    listeners.fillna(0, inplace=True)
    return listeners


def get_artist_similarities(listeners):
    listeners_sparse = sparse.csr_matrix(listeners)
    artist_similarities = pd.DataFrame(
        data=cosine_similarity(listeners_sparse),
        index=listeners.index,
        columns=listeners.index
    )
    return artist_similarities


def train():
    listeners = load_listeners(paths.SCROBBLES_FILE_PATH)
    listeners = normalize_listeners(listeners)
    artist_similarities = get_artist_similarities(listeners)
    joblib.dump(artist_similarities, paths.MODEL_FILE_PATH)


if __name__ == '__main__':
    train()
