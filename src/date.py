import calendar
import re
from datetime import datetime, timedelta


def _parse_japanese_date(date: str, year: int):
    pattern = r"(\d+)月(\d+)日"
    matches = re.findall(pattern, date)

    if len(matches) == 1:
        month, day = matches[0]
        month_num = int(month)
        # Add 1 year for months 1-3 (next year)
        actual_year = year + 1 if month_num <= 3 else year
        start = f"{actual_year}-{month_num:02d}-{int(day):02d}"
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)
        return {"start": f"{start}", "end": f"{end_dt.strftime('%Y-%m-%d')}"}
    elif len(matches) == 2:
        start_month, start_day = matches[0]
        end_month, end_day = matches[1]
        start_month_num = int(start_month)
        end_month_num = int(end_month)

        # Handle academic year transition
        start_year = year + 1 if start_month_num <= 3 else year
        end_year = year + 1 if end_month_num <= 3 else year
        end_dt = datetime.strptime(
            f"{end_year}-{end_month_num:02d}-{int(end_day):02d}", "%Y-%m-%d"
        ) + timedelta(days=1)

        return {
            "start": f"{start_year}-{start_month_num:02d}-{int(start_day):02d}",
            "end": f"{end_dt.strftime('%Y-%m-%d')}",
        }
    return None


def _parse_english_date(date: str, year: int):
    range_pattern = r"(\w+) (\d+)(?:st|nd|rd|th).*?-.*?(\w+) (\d+)(?:st|nd|rd|th)"
    single_pattern = r"(\w+) (\d+)(?:st|nd|rd|th)"

    range_match = re.search(range_pattern, date, re.DOTALL)
    if range_match:
        start_month, start_day, end_month, end_day = range_match.groups()
        start_month_num = list(calendar.month_name).index(start_month)
        end_month_num = list(calendar.month_name).index(end_month)

        # Handle academic year transition
        start_year = year + 1 if start_month_num <= 3 else year
        end_year = year + 1 if end_month_num <= 3 else year

        end_date = f"{end_year}-{end_month_num:02d}-{int(end_day):02d}"
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

        return {
            "start": f"{start_year}-{start_month_num:02d}-{int(start_day):02d}",
            "end": end_dt.strftime("%Y-%m-%d"),
        }

    # Single date
    single_match = re.search(single_pattern, date)
    if single_match:
        month_str, day = single_match.groups()
        month_num = list(calendar.month_name).index(month_str)
        if month_num == 0:
            return None

        # Handle academic year transition
        actual_year = year + 1 if month_num <= 3 else year
        start = f"{actual_year}-{month_num:02d}-{int(day):02d}"
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)

        return {"start": start, "end": end_dt.strftime("%Y-%m-%d")}

    return None


def parse_date(date: str, year: int):
    if year is None:
        raise ValueError("Year is not set")

    if date is None:
        return None

    if "月" in date:
        return _parse_japanese_date(date, year)
    else:
        return _parse_english_date(date, year)
