import pendulum
from pendulum import DateTime

from ical_library.ical_properties.dt import DTStart


def test_dt_both(berlin_timezone_calendar):
    with berlin_timezone_calendar:
        a = DTStart(name="DTSTART", property_parameters="TZID=Europe/Berlin", value="20190307T020000")
    assert a.datetime_or_date_value == DateTime(2019, 3, 7, 2, 0, 0, tzinfo=pendulum.timezone("Europe/Berlin"))
