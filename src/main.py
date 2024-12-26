import argparse

from en import AcademicCalendarEN
from ics import generate_ics_files
from ja import AcademicCalendarJA


def main(year: int):
    if year is None:
        raise ValueError("Year is required")

    ja = AcademicCalendarJA(year)
    en = AcademicCalendarEN(year)
    generate_ics_files(ja.get(), en.get(), year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y", "--year", type=int, help="The year of the academic calendar"
    )
    main(parser.parse_args().year)
