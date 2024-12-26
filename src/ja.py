import requests
from bs4 import BeautifulSoup

from date import parse_date
from ics import generate_ics_files
from util import normalize, output_json


class AcademicCalendarJA:
    def __init__(self, year: int = None):
        self.lang = "ja"
        self.year = year
        self.events = list()
        self.url = "https://www.naist.jp/campuslife/information/calendar.html"
        self.current_date = None
        self.current_events = []

    def _process_events(self):
        if self.current_date and self.current_events:
            date = parse_date(self.current_date, self.year)
            if date:
                self.events.append(
                    {
                        "start": date["start"],
                        "end": date["end"],
                        "event": ", ".join(self.current_events),
                    }
                )
            self.current_events = []

    def get(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find("tbody").find_all("tr")

        for row in rows:
            semester_cell = row.find("th")
            if semester_cell and "rowspan" in semester_cell.attrs:
                continue

            cells = row.find_all("td")

            if len(cells) == 2:
                if self.current_date:
                    self._process_events()

                self.current_date = cells[0].text.strip()
                event = cells[1].text.strip()
                if event:
                    self.current_events = [normalize(event)]

            elif len(cells) == 1 and self.current_date:
                event = cells[0].text.strip()
                if event:
                    self.current_events.append(normalize(event))

        self._process_events()
        output_json(self.events, f"data/{self.year}-{self.lang}.json")
        generate_ics_files(self.events, self.lang, self.year, self.url)
