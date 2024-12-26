import os
import random
import zoneinfo
from datetime import datetime

from icalendar import Calendar, Event


def create_calendar(events, lang="ja"):
    cal = Calendar()

    # Set calendar metadata
    cal.add("prodid", f"-//NAIST Academic Calendar {lang.upper()}//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("x-wr-calname", f"NAIST Academic Calendar {lang.upper()}")
    cal.add("x-wr-timezone", "Asia/Tokyo")

    jst = zoneinfo.ZoneInfo("Asia/Tokyo")

    for event_data in events:
        event = Event()

        start = datetime.strptime(event_data["start"], "%Y-%m-%d").replace(tzinfo=jst)
        end = datetime.strptime(event_data["end"], "%Y-%m-%d").replace(tzinfo=jst)

        event.add("summary", event_data["event"])
        event.add("dtstart", start)
        event.add("dtend", end)
        event.add("dtstamp", datetime.now(jst))

        event_id = f"naist-{lang}-{random.randint(1000, 9999)}"
        event.add("uid", event_id)

        cal.add_component(event)

    return cal


def generate_ics_files(calendar_ja, calendar_en, year: int):
    os.makedirs("data", exist_ok=True)

    ja_cal = create_calendar(calendar_ja, "ja")
    with open(f"data/academic-calendar-{year}-ja.ics", "wb") as f:
        f.write(ja_cal.to_ical())

    en_cal = create_calendar(calendar_en, "en")
    with open(f"data/academic-calendar-{year}-en.ics", "wb") as f:
        f.write(en_cal.to_ical())
