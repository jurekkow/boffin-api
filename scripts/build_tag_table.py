import json

import pandas as pd

import paths

from sklearn.externals import joblib

with open(paths.FESTS_FILE_PATH) as fests_file:
    fests = json.load(fests_file)

TAGS_TO_IGNORE = ["seen live", "polish"]

tag_table = pd.DataFrame({})
for fest in fests:
    for artist in fest["artists"]:
        for tag in artist["tags"]:
            if tag in TAGS_TO_IGNORE:
                continue
            tag_table.loc[artist["name"], tag] = 1

joblib.dump(tag_table, paths.TAG_TABLE_FILE_PATH)
