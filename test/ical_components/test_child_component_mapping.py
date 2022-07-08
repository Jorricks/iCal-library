import pytest

from ical_reader.ical_components.v_alarm import VAlarm
from ical_reader.ical_components.v_calendar import VCalendar
from ical_reader.ical_components.v_event import VEvent
from ical_reader.ical_components.v_free_busy import VFreeBusy
from ical_reader.ical_components.v_journal import VJournal
from ical_reader.ical_components.v_timezone import DayLight, Standard, VTimeZone
from ical_reader.ical_components.v_todo import VToDo


def test_get_child_component_mapping_with_children():
    assert VCalendar._get_child_component_mapping() == {
        "VEVENT": ("events", VEvent, True),
        "VFREEBUSY": ("free_busy_list", VFreeBusy, True),
        "VJOURNAL": ("journals", VJournal, True),
        "VTIMEZONE": ("time_zones", VTimeZone, True),
        "VTODO": ("todos", VToDo, True),
    }

    assert VTimeZone._get_child_component_mapping() == {
        "DAYLIGHT": ("daylightc", DayLight, True),
        "STANDARD": ("standardc", Standard, True),
    }

    assert VEvent._get_child_component_mapping() == {
        "VALARM": ("alarms", VAlarm, True),
    }

    assert VToDo._get_child_component_mapping() == {
        "VALARM": ("alarms", VAlarm, True),
    }


@pytest.mark.parametrize("a_type", [VFreeBusy, VJournal, DayLight, Standard, VAlarm])
def test_get_child_component_mapping_without_children(a_type):
    assert a_type._get_child_component_mapping() == {}
