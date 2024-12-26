import argparse

from en import AcademicCalendarEN
from ja import AcademicCalendarJA


def main(year: int):
    if year is None:
        raise ValueError("Year is required")

    AcademicCalendarJA(year).get()
    AcademicCalendarEN(year).get()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y", "--year", type=int, help="The year of the academic calendar"
    )
    main(parser.parse_args().year)
