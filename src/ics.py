import os
import random
import zoneinfo
from datetime import datetime

from icalendar import Calendar, Event


def _create_calendar(events, lang, url):
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
        event.add("url", url)
        event.add("description", f"{event_data["event"]}\n{url}")

        event_id = f"naist-{lang}-{random.randint(1000, 9999)}"
        event.add("uid", event_id)

        cal.add_component(event)

    return cal


def generate_ics_files(event, lang: str, year: int, url: str):
    os.makedirs("data", exist_ok=True)

    cal = _create_calendar(event, lang, url)
    with open(f"data/academic-calendar-{year}-{lang}.ics", "wb") as f:
        f.write(cal.to_ical())
