import argparse

from en import AcademicCalendarEN
from ja import AcademicCalendarJA


def main(year: int):
    AcademicCalendarJA(year).get()
    AcademicCalendarEN(year).get()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="The year of the academic calendar",
        required=True,
    )
    main(parser.parse_args().year)
