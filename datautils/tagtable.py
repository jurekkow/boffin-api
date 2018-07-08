import json

import pandas as pd

import paths

from sklearn.externals import joblib


def build():
    with open(paths.FESTS_FILE_PATH) as fests_file:
        fests = json.load(fests_file)

    tag_table = pd.DataFrame({})
    for fest in fests.values():
        for artist in fest:
            for tag in artist["tags"]:
                tag_table.loc[artist["name"], tag] = 1

    joblib.dump(tag_table, paths.TAG_TABLE_FILE_PATH)


if __name__ == "__main__":
    build()

