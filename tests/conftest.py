import os
from pathlib import Path

import pytest

from ical_library import client
from ical_library.ical_components import VCalendar
from ical_library.ical_properties import ProdID


@pytest.fixture
def root_folder() -> Path:
    starting_place = Path(os.getcwd()).resolve()
    folder = starting_place
    while not (folder / ".git").is_dir() and not folder.name.lower() == "iCal-library":
        folder = folder.parent
        if folder.name == "":
            raise ValueError(f"Could not find the root folder starting from {starting_place=}.")
    return folder.resolve()


@pytest.fixture
def calendar_instance() -> VCalendar:
    return VCalendar(
        prodid=ProdID("-//Google Inc//Google Calendar 70.9054//EN"),
    )


@pytest.fixture
def calendar_with_all_components_once(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "tests" / "resources" / "iCalendar-with-all-components-once.ics")


@pytest.fixture
def calendar_with_reoccurring_events_once(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "tests" / "resources" / "iCalendar-with-reoccurring-events.ics")


@pytest.fixture
def empty_calendar(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "tests" / "resources" / "iCalender-without-anything.ics")


@pytest.fixture
def berlin_timezone_calendar(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "tests" / "resources" / "iCalendar-with-berlin-timezone.ics")


@pytest.fixture
def multi_offset_calendar(root_folder: Path) -> VCalendar:
    filename = "iCalendar-with-recurring-event-multiple-timezone-offsets.ics"
    return client.parse_icalendar_file(root_folder / "tests" / "resources" / filename)
