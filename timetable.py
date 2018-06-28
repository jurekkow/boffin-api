import collections
import datetime
import json

import requests

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


def get_clashfinder_timetable():
    response = requests.get(TIMETABLE_URL, verify=False)
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


def create_blank_boffin_timetable():
    boffin_timetable = {
        week_day: {"date": date, "stages": collections.defaultdict(list)}
        for week_day, date in FEST_DAYS
    }
    return boffin_timetable


def add_event_data(boffin_timetable, clashfinder_timetable):
    for location in clashfinder_timetable["locations"]:
        stage = location["name"].strip()
        for event in location["events"]:
            week_day = get_week_day(event["start"])
            event_data = {
                "name": event["name"].strip().lower(),
                "from": event["start"].split(" ")[1],
                "to": event["end"].split(" ")[1]
            }
            boffin_timetable[week_day]["stages"][stage].append(event_data)
    return boffin_timetable


def get_current_timetable():
    clashfinder_timetable = get_clashfinder_timetable()
    boffin_timetable = create_blank_boffin_timetable()
    boffin_timetable = add_event_data(boffin_timetable, clashfinder_timetable)
    return boffin_timetable
