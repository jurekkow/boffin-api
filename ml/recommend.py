import json

import pandas as pd

import paths

from collections import OrderedDict

from sklearn.externals import joblib


artist_similarities = joblib.load(paths.MODEL_FILE_PATH)
with open(paths.FESTS_FILE_PATH) as fests_json_file:
    fests = json.load(fests_json_file)
fest_2018 = next(fest for fest in fests if fest["year"] == "2018")
artists_2018 = [artist["name"] for artist in fest_2018["artists"]]


def get_listener_row(chosen_artists):
    all_artists = artist_similarities.index
    listener = pd.Series(
        data=[int(artist in chosen_artists) for artist in all_artists],
        index=all_artists
    )
    return listener


def make_recommendation(listener):
    artist_2018_similarities = artist_similarities.loc[artists_2018, :]
    scores = artist_2018_similarities.dot(listener)
    scores = scores.div(artist_2018_similarities.sum(axis=1))
    scores.fillna(0, inplace=True)
    return scores


def recommend(chosen_artists):
    listener = get_listener_row(chosen_artists)
    scores = make_recommendation(listener)
    scores = pd.Series.sort_values(scores, ascending=False)
    scores_dict = scores.to_dict(OrderedDict)
    return scores_dict
