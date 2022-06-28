from datetime import timedelta
from typing import List

from pendulum import DateTime

from ical_reader.ical_components.v_calendar import VCalendar


def get_calendar(lines: List[str]) -> VCalendar:
    new_instance = VCalendar()
    if lines[0] != "BEGIN:VCALENDAR":
        raise ValueError(f"This is not a ICalendar as it started with {lines[0]=}.")
    new_instance.parse_component_section(lines, line_number=1)
    return new_instance


if __name__ == "__main__":
    from utils import path_finder
    file_contents = open(path_finder.get_root_folder() / "ical_examples" / "ical.cache").readlines()
    # file_contents = open(path_finder.get_root_folder() / "ical_examples" / "example_of_failure.txt").readlines()
    calendar = get_calendar([line.rstrip("\n") for line in file_contents])
    print(type(calendar.events[0]), str(calendar.events[0])[0:1000])
    print(type(calendar.events[0].attendee), calendar.events[0].attendee)
    print(calendar.events[0].attendee[95].persons_name)
    print([e for e in calendar.events if e.rrule is not None])

    from ical_reader.ical_components.v_event import VRecurringEvent
    for t, e in calendar.get_limited_timeline(DateTime.utcnow() - timedelta(days=10), DateTime.utcnow()).iterate():
        if isinstance(e, VRecurringEvent):
            print(e)

"""
from ical_reader import client
from utils import path_finder
file_contents = open(path_finder.get_root_folder() / "ical_examples" / "ical.cache").readlines()
calendar = client.get_calendar([line.rstrip("\n") for line in file_contents])
calendar.timeline
"""