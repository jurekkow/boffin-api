import json

import paths


if __name__ == "__main__":
    alphabet="0123456789aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"
    char_position = {char: i for i, char in enumerate(alphabet)}

    with open(paths.FESTS_IMG_FILE_PATH) as fests_file:
        fests = json.load(fests_file)

    for year, artists in fests.items():
        fests[year] = sorted(
            artists,
            key=lambda artist: [
                char_position.get(char, len(alphabet))
                for char in artist["name"].lower()
            ]
        )
    
    with open(paths.FESTS_IMG_FILE_PATH, "w") as fests_file:
        json.dump(fests, fests_file)
