import itertools
import json
import traceback

import pandas as pd
import requests

from bs4 import BeautifulSoup

import paths


HTTP_OK = 200
API_KEY = "PUT YOUR API KEY HERE"
ARTIST_INFO_URL_PATTERN = "http://ws.audioscrobbler.com/2.0/" \
                          "?method=artist.getinfo&" \
                          "artist={}" \
                          "&api_key={}" \
                          "&format=json"
TOP_ARTISTS_URL_PATTERN = "http://ws.audioscrobbler.com/2.0/" \
                          "?method=user.gettopartists" \
                          "&user={}" \
                          "&api_key={}" \
                          "&format=json" \
                          "&limit=100"


def is_url_valid(url):
    response = requests.head(url)
    url_valid = response.status_code == HTTP_OK
    print("URL: {} is {}".format(url, "valid" if url_valid else "broken"))
    return url_valid


def load_fest_urls(urls_file_path=paths.URLS_FILE_PATH):
    with open(urls_file_path) as urls_file:
        fest_urls = [url.strip() for url in urls_file]
        fest_urls = [url for url in fest_urls if is_url_valid(url)]
    return fest_urls


def paged(endpoint):
    def paged_decorator(find_items):
        def wrapper(url):
            items = []
            previous_items = None
            for i in itertools.count(start=1):
                paged_url = "{}/{}/?page={}".format(url, endpoint, i)
                new_items = find_items(paged_url)
                if new_items == previous_items:
                    return items
                items += new_items
                previous_items = new_items
        return wrapper
    return paged_decorator


@paged("lineup")
def get_fest_artists(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser")
    artist_h3s = bs.find_all("h3", class_="big-artist-list-title")
    artists = [artist_h3.text for artist_h3 in artist_h3s]
    return artists


@paged("attendance/going")
def get_fest_attendees(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser")
    attendee_as = bs.find_all("a", class_="user-list-link")
    attendees = [attendee_a.text for attendee_a in attendee_as]
    return attendees


def get_fest_year(fest_url):
    # TODO replace with more generic way in the future
    year = fest_url[-4:]
    return year


def get_fest_data(fest_url):
    fest_data = {
        "url": fest_url,
        "year": get_fest_year(fest_url),
        "artists": get_fest_artists(fest_url),
    }
    print("Downloaded fest data from {}".format(fest_url))
    return fest_data


def get_scrobbled_fest_artists(attendee, fest_artists):
    url = TOP_ARTISTS_URL_PATTERN.format(attendee, API_KEY)
    response = requests.get(url)
    artist_data = response.json()["topartists"]
    artists = {artist["name"]: artist["playcount"]
               for artist in artist_data["artist"]}
    scrobbled_fest_artist = {artist: playcount
                             for artist, playcount in artists.items()
                             if artist in fest_artists}
    return scrobbled_fest_artist


def build_scrobble_table(fests):
    artists = list(
        {artist for fest in fests for artist in fest["artists"]}
    )
    attendees = list(
        {attendee for fest in fests
         for attendee in get_fest_attendees(fest["url"])}
    )
    print("Downloaded fest atendees")
    scrobble_table = pd.DataFrame(index=artists, columns=attendees)
    for i, attendee in enumerate(attendees, start=1):
        print("Downloading data for user {}... ({}%)".format(
            attendee, 100 * i / len(attendees)))
        try:
            scrobbled_artists = get_scrobbled_fest_artists(attendee, artists)
            if scrobbled_artists:
                scrobble_table[attendee] = pd.Series(scrobbled_artists)
            else:
                del scrobble_table[attendee]
        except:
            print("FAILED")
            traceback.print_exc()
        else:
            print("OK")

    return scrobble_table


def add_artists_details(fest):
    artists = []
    for artist in fest["artists"]:
        url = ARTIST_INFO_URL_PATTERN.format(artist, API_KEY)
        response = requests.get(url)
        default_artist_data = {
            "name": artist,
            "image": [{"#text": ""}],
            "tags": {"tag": []}
        }

        try:
            artist_data = response.json()["artist"]
        except:
            artist_data = default_artist_data
            print("Failed when downloading data for {}".format(artist))
            traceback.print_exc()
            pass

        artists.append({
            "name": artist_data["name"],
            "imageUrl": artist_data["image"][-1]["#text"],
            "tags": [tag["name"] for tag in artist_data["tags"]["tag"]]
        })

    fest["artists"] = artists
    print("Downloaded artist details for fest: {}".format(fest["url"]))
    return fest


def main():
    print("Loading fest URL's...")
    fest_urls = load_fest_urls()
    print("Done!")

    print("Downloading fest data...")
    fests = [get_fest_data(url) for url in fest_urls]
    print("Done!")

    print("Building scrobble table...")
    scrobble_table = build_scrobble_table(fests)
    print("Done!")

    print("Saving scrobble table...")
    scrobble_table.to_csv(paths.SCROBBLES_FILE_PATH, index_label="artist")
    print("Done!")

    print("Downloading artists details...")
    fests = [add_artists_details(fest) for fest in fests]
    print("Done!")

    print("Saving artists data...")
    with open(paths.FESTS_FILE_PATH, "w") as fests_file:
        json.dump(fests, fests_file)
    print("Done!")


if __name__ == "__main__":
    main()
