import requests
from bs4 import BeautifulSoup, NavigableString

from date import parse_date
from util import normalize


class AcademicCalendarEN:
    def __init__(self, year: int = None):
        self.year = year
        self.events = list()
        self.url = f"https://www.naist.jp/en/campuslife/academic_calendar/{year}.html"

    def _get_text_content(self, element):
        texts = []
        for content in element.contents:
            if isinstance(content, NavigableString):
                text = content.strip()
                if text and text != ",":
                    texts.append(text)
            elif content.name == "br":
                continue
            elif content.name == "p":
                p_text = content.get_text(strip=True)
                if p_text:
                    texts.append(p_text)
        return ", ".join(filter(None, texts))

    def get(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find("tbody").find_all("tr")

        for row in rows:
            # Skip semester headers
            if len(row.find_all("th")) == 1 and "rowspan" in row.find("th").attrs:
                continue

            date_cell = row.find("th", class_=None)
            event_cell = row.find("td")

            if date_cell and event_cell:
                date_str = date_cell.get_text(strip=True)
                event = self._get_text_content(event_cell)

                if date_str and event:
                    date = parse_date(date_str, self.year)
                    if date:
                        self.events.append(
                            {
                                "start": date["start"],
                                "end": date["end"],
                                "event": normalize(event),
                            }
                        )
        return self.events
