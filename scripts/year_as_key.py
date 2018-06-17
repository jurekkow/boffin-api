import json

import paths

with open(paths.FESTS_FILE_PATH) as fest_file:
    fests = json.load(fest_file)

fests_year_as_key = {fest["year"]: fest["artists"] for fest in fests}

with open("fests_year_as_key.json", "w") as fest_file:
    json.dump(fests_year_as_key, fest_file)
