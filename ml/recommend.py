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


def get_artist_tags(artist):
    tags = next(
        a["tags"]
        for fest in fests
        for a in fest["artists"] if a["name"] == artist
    )
    tags = [tag for tag in tags if tag not in ["seen live", "polish"]]
    return tags


def score_by_tags(chosen_artists, score_factor=0.01):
    tag_table = joblib.load(paths.TAG_TABLE_FILE_PATH)
    tag_table.fillna(0, inplace=True)
    user_tags = pd.Series(0, index=tag_table.columns)
    for chosen_artist in chosen_artists:
        tags = get_artist_tags(chosen_artist)
        user_tags[tags] += 1

    tag_table_2018 = tag_table.loc[artists_2018, :]
    tag_scores = tag_table_2018.dot(user_tags) * score_factor
    tag_scores.fillna(0, inplace=True)
    return tag_scores


def recommend(chosen_artists):
    listener = get_listener_row(chosen_artists)
    scores = make_recommendation(listener)

    tag_scores = score_by_tags(chosen_artists)
    scores += tag_scores

    scores = pd.Series.sort_values(scores, ascending=False)
    scores_dict = scores.to_dict(OrderedDict)
    return scores_dict
