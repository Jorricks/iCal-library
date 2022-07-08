import os
from pathlib import Path

import pytest

from ical_reader import client
from ical_reader.ical_components.v_calendar import VCalendar


@pytest.fixture
def root_folder() -> Path:
    starting_place = Path(os.getcwd()).resolve()
    folder = starting_place
    while not (folder / ".git").is_dir() and not folder.name == "ical-reader":  # Test on .git folder being present
        folder = folder.parent
        if folder.name == "":
            raise ValueError(f"Could not find the root folder starting from {starting_place=}.")
    return folder.resolve()


@pytest.fixture
def calendar_with_all_components_once(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "test" / "resources" / "iCalendar-with-all-components-once.ics")


@pytest.fixture
def calendar_with_reoccurring_events_once(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "test" / "resources" / "iCalendar-with-reoccurring-events.ics")


@pytest.fixture
def empty_calendar(root_folder: Path) -> VCalendar:
    return client.parse_icalendar_file(root_folder / "test" / "resources" / "iCalender-without-anything.ics")
