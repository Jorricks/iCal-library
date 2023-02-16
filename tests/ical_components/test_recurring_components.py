from typing import List

import pendulum
from pendulum import Date, DateTime

from ical_library.help_modules.timespan import Timespan, TimespanWithParent
from ical_library.ical_components import VCalendar


def test_recurrence_with_offset_changes(multi_offset_calendar: VCalendar) -> None:
    """
    This test verifies that calendars that have a recurrence set, correctly handle time zone changes.
    In this case we have Amsterdam time zone which changes from +02:00 to +01:00 at 2022-10-30
    """
    recurring_event = multi_offset_calendar.events[0]
    return_rage = Timespan(DateTime(2022, 10, 1), DateTime(2022, 11, 10))
    components: List[TimespanWithParent] = list(recurring_event.expand_component_in_range(return_rage, []))
    assert components[0].begin == pendulum.parse("2022-10-18T12:00:00+02:00")
    assert components[0].end == pendulum.parse("2022-10-18T17:00:00+02:00")
    assert components[1].begin == pendulum.parse("2022-10-25T12:00:00+02:00")
    assert components[1].end == pendulum.parse("2022-10-25T17:00:00+02:00")
    assert components[2].begin == pendulum.parse("2022-11-01T12:00:00+01:00")
    assert components[2].end == pendulum.parse("2022-11-01T17:00:00+01:00")
    assert components[3].begin == pendulum.parse("2022-11-08T12:00:00+01:00")
    assert components[3].end == pendulum.parse("2022-11-08T17:00:00+01:00")


def test_recurrence_with_dates_includes_intersected_dates(recurring_date_events_calendar: VCalendar) -> None:
    """
    This test verifies that calendars that have a recurrence set on a date, correctly expand in recurring events.
    When a new event occurs exactly on the end of the return range, it should be returned.
    """
    recurring_event = recurring_date_events_calendar.events[0]
    return_rage = Timespan(Date(2023, 3, 4), Date(2023, 3, 8))
    components: List[TimespanWithParent] = list(recurring_event.expand_component_in_range(return_rage, []))
    assert components[0].begin == pendulum.parse("2023-03-08T00:00:00+01:00")
    assert components[0].end == pendulum.parse("2023-03-15T00:00:00+01:00")

    return_rage = Timespan(Date(2023, 3, 4), Date(2023, 5, 31))
    components: List[TimespanWithParent] = list(recurring_event.expand_component_in_range(return_rage, []))
    assert components[1].begin == pendulum.parse("2023-05-31T00:00:00+02:00")
    assert components[1].end == pendulum.parse("2023-06-07T00:00:00+02:00")
