import re
import string


def normalize_artist(artist_name):
    artist_name = artist_name.lower()
    artist_name = artist_name.replace(" & ", " and ")
    non_alpha_num_pattern = re.compile(r"[\W]+")
    artist_name = re.sub(non_alpha_num_pattern, " ", artist_name)
    multple_whitespace_pattern = re.compile(r"\s{2,}")
    artist_name = re.sub(multple_whitespace_pattern, " ", artist_name)
    artist_name = artist_name.strip()
    the_pattern = re.compile(r"(?P<the>the )(?P<rest>.*)")
    the_match = re.match(the_pattern, artist_name)
    if the_match:
        artist_name = the_match.group("rest")
    return artist_name

