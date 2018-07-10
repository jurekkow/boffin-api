import json

import pandas as pd

import paths

from collections import OrderedDict

from sklearn.externals import joblib

from datautils.names import normalize_artist


artist_similarities = joblib.load(paths.MODEL_FILE_PATH)
with open(paths.FESTS_FILE_PATH) as fests_json_file:
    fests = json.load(fests_json_file)
artists_2018 = [artist["name"] for artist in fests["2018"]]
tag_table = joblib.load(paths.TAG_TABLE_FILE_PATH)
tag_table.fillna(0, inplace=True)


def get_listener_row(chosen_artists):
    all_artists = artist_similarities.index
    listener = pd.Series(
        data=[int(artist in chosen_artists) for artist in all_artists],
        index=all_artists
    )
    return listener


def make_recommendation(listener):
    artist_2018_similarities = artist_similarities.reindex(artists_2018)
    scores = artist_2018_similarities.dot(listener)
    scores = scores.div(artist_2018_similarities.sum(axis=1))
    scores.fillna(0, inplace=True)
    return scores


def score_by_tags(chosen_artists, score_factor=0.01):
    user_tags = tag_table.reindex(chosen_artists).sum()
    tag_table_2018 = tag_table.reindex(artists_2018)
    tag_scores = tag_table_2018.dot(user_tags) * score_factor
    tag_scores.fillna(0, inplace=True)
    return tag_scores


def recommend(chosen_artists):
    listener = get_listener_row(chosen_artists)
    scores = make_recommendation(listener)

    tag_scores = score_by_tags(chosen_artists)
    scores += tag_scores

    scores = pd.Series.sort_values(scores, ascending=False)
    scores /= scores.max()
    scores.index = [normalize_artist(artist) for artist in scores.index]
    scores_dict = scores.to_dict(OrderedDict)
    return scores_dict
