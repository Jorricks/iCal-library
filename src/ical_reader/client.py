from pathlib import Path
from typing import Any, List, Union
from urllib import request

from ical_reader.ical_components import VCalendar


def parse_lines_into_calendar(lines: List[str]) -> VCalendar:
    """
    Given the lines of an iCalendar file, return a parsed VCalendar instance.
    :param lines: The lines of the iCalendar file/website.
    :return: a VCalendar with all it's iCalendar components like VEvents, VToDos, VTimeZones etc.
    """
    new_instance = VCalendar()
    if lines[0] != "BEGIN:VCALENDAR":
        raise ValueError(f"This is not a ICalendar as it started with {lines[0]=}.")
    new_instance.parse_component(lines, line_number=1)
    return new_instance


def parse_icalendar_file(file: Union[str, Path]) -> VCalendar:
    """
    Parse an iCalendar file and return a parsed VCalendar instance.
    :param file: A file on the local filesystem that contains the icalendar definition.
    :return: a VCalendar instance with all it's iCalendar components like VEvents, VToDos, VTimeZones etc.
    """
    with open(file, "r") as ical_file:
        return parse_lines_into_calendar([line.strip("\n") for line in ical_file.readlines()])


def parse_icalendar_url(url: str, **kwargs: Any) -> VCalendar:
    """
    Given a URL to an iCalendar file, return a parsed VCalendar instance.
    :param url: The URL to the iCalendar file.
    :param kwargs: Any keyword arguments to pass onto the `urllib.request.urlopen` call.
    :return: a VCalendar instance with all it's iCalendar components like VEvents, VToDos, VTimeZones etc.
    """
    response = request.urlopen(url, **kwargs)
    text = response.read().decode("utf-8")
    lines = text.split("\n")
    return parse_lines_into_calendar(lines)
