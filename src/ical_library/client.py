import re
from pathlib import Path
from typing import Any, List, Union
from urllib import request

from ical_library.ical_components import VCalendar


def parse_lines_into_calendar(raw_text: str) -> VCalendar:
    """
    Given the lines of an iCalendar file, return a parsed VCalendar instance.
    :param raw_text: The raw text of the iCalendar file/website.
    :return: a VCalendar with all it's iCalendar components like VEvents, VToDos, VTimeZones etc.
    """
    lines: List[str] = []
    for line in re.split(r"\n", raw_text):
        line_content = re.sub(r"^\n|^\r|\n$|\r$", "", line)
        if len(line_content) > 0:
            lines.append(line_content)
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
        return parse_lines_into_calendar(ical_file.read())


def parse_icalendar_url(url: str, **kwargs: Any) -> VCalendar:
    """
    Given a URL to an iCalendar file, return a parsed VCalendar instance.
    :param url: The URL to the iCalendar file.
    :param kwargs: Any keyword arguments to pass onto the `urllib.request.urlopen` call.
    :return: a VCalendar instance with all it's iCalendar components like VEvents, VToDos, VTimeZones etc.
    """
    response = request.urlopen(url, **kwargs)
    text = response.read().decode("utf-8")
    return parse_lines_into_calendar(text)
