import collections
import datetime
import json
import re

import requests
import requests.exceptions

import paths

TIMETABLE_URL = "https://clashfinder.com/data/event/offfestival2018.json"
WEEK_DAYS = {
    4: "friday",
    5: "saturday",
    6: "sunday"
}
FEST_DAYS = [
    ("friday", "03.08"),
    ("saturday", "04.08"),
    ("sunday", "05.08"),
]
DAY_END_HOUR = 5
HTTP_OK = 200


with open(paths.TIMETABLE_FILE_PATH) as timetable_file:
    boffin_timetable = json.load(timetable_file)


def get_clashfinder_timetable():
    try:
        response = requests.get(TIMETABLE_URL, verify=False)
    except requests.exceptions.ConnectionError:
        return None
    if response.status_code != HTTP_OK:
        return None
    clashfinder_timetable = response.json()
    return clashfinder_timetable


def get_week_day(date_time):
    date, time = date_time.split(" ")
    date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
    hour = int(time.split(":")[0])
    if hour < DAY_END_HOUR:
        date_time -= datetime.timedelta(days=1)
    week_day = WEEK_DAYS[date_time.weekday()]
    return week_day


def get_artist_name(event_name):
    event_name = event_name.strip().lower()
    artist_plays_album_pattern = re.compile(
        r"(?P<artist>.*) (gra|grają) (?P<album>.*)"
    )
    artist_plays_live_pattern = re.compile(
        r"(?P<artist>.*) live"
    )
    artist_plays_album = re.match(artist_plays_album_pattern, event_name)
    artist_plays_live = re.match(artist_plays_live_pattern, event_name)
    if artist_plays_album:
        artist_name = artist_plays_album.group("artist")
    elif artist_plays_live:
        artist_name = artist_plays_live.group("artist")
    else:
        artist_name = event_name
    return artist_name


def create_blank_boffin_timetable():
    boffin_timetable = {
        week_day: {"date": date, "stages": collections.defaultdict(list)}
        for week_day, date in FEST_DAYS
    }
    return boffin_timetable


def add_event_data(boffin_timetable, clashfinder_timetable):
    for location in clashfinder_timetable["locations"]:
        stage = location["name"].strip()
        events = location["events"]
        for event in events:
            week_day = get_week_day(event["start"])
            event_data = {
                "title": event["name"].strip(),
                "name": get_artist_name(event["name"]),
                "start": event[ "start"],
                "end": event["end"]
            }
            boffin_timetable[week_day]["stages"][stage].append(event_data)

    return boffin_timetable


def get_current_timetable():
    global boffin_timetable

    clashfinder_timetable = get_clashfinder_timetable()
    if not clashfinder_timetable:
        return boffin_timetable
            
    boffin_timetable = create_blank_boffin_timetable()
    boffin_timetable = add_event_data(boffin_timetable, clashfinder_timetable)
    with open(paths.TIMETABLE_FILE_PATH, "w") as timetable_file:
        json.dump(boffin_timetable, timetable_file)
    return boffin_timetable
