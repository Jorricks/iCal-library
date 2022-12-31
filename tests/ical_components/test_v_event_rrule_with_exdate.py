import pendulum
from pendulum import DateTime

from ical_library.help_modules.timespan import Timespan
from ical_library.ical_components import VCalendar
from ical_library.timeline import Timeline


def test_vevent_with_exdate(calendar_exdate: VCalendar):
    timeline: Timeline = calendar_exdate.get_limited_timeline(
        DateTime(2022, 12, 27).in_tz("Europe/Amsterdam"), DateTime(2022, 12, 31).in_tz("Europe/Amsterdam")
    )
    all_events = list(timeline.iterate())
    assert len(all_events) == 2
    assert all_events[0][0] == Timespan(
        pendulum.parse("2022-12-27T11:15:00+01:00"), pendulum.parse("2022-12-27T11:45:00+01:00")
    )
    assert all_events[1][0] == Timespan(
        pendulum.parse("2022-12-29T11:15:00+01:00"), pendulum.parse("2022-12-29T11:45:00+01:00")
    )
