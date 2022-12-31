from typing import List

from pendulum import DateTime
from pendulum.tz.zoneinfo.transition import Transition

from ical_library.ical_components import VCalendar, VTimeZone


def filter_transitions(start: DateTime, end: DateTime, transitions: List[Transition]) -> List[Transition]:
    start_epoch = int(start.timestamp())
    end_epoch = int(end.timestamp())
    return [transition for transition in transitions if start_epoch <= transition.at <= end_epoch]


def test_get_ordered_timezone_overview_as_transition(berlin_timezone_calendar: VCalendar):
    """Test that the timezone components are correctly parsed."""
    # For reference material, you can use the transitions that are present in this;
    # berlin = pendulum._safe_timezone("Europe/Berlin")
    berlin_timezone: VTimeZone = berlin_timezone_calendar.get_timezone("Europe/Berlin")
    generated_transitions = berlin_timezone.get_ordered_timezone_overview_as_transition(DateTime(2023, 1, 1))
    year_1970 = filter_transitions(DateTime(1970, 1, 1), DateTime(1971, 1, 1), generated_transitions)
    march_1970_switch = year_1970[0]
    october_1970_switch = year_1970[1]
    assert march_1970_switch.at == 7520400
    assert march_1970_switch.ttype.offset == 7200
    assert march_1970_switch.ttype.is_dst() is True
    assert march_1970_switch.ttype.abbreviation == "CEST"
    assert march_1970_switch.previous is None
    assert october_1970_switch.at == 25664400
    assert october_1970_switch.ttype.offset == 3600
    assert october_1970_switch.ttype.is_dst() is False
    assert october_1970_switch.ttype.abbreviation == "CET"
    assert october_1970_switch.previous.at == 7520400
    assert october_1970_switch.previous.ttype.offset == 7200
    assert october_1970_switch.previous.ttype.is_dst() is True
    assert october_1970_switch.previous.ttype.abbreviation == "CEST"
    assert october_1970_switch.previous.previous is None

    year_2022 = filter_transitions(DateTime(2022, 1, 1), DateTime(2023, 1, 1), generated_transitions)
    march_2022_switch = year_2022[0]
    october_2022_switch = year_2022[1]

    assert march_2022_switch.at == 1648342800
    assert march_2022_switch.ttype.offset == 7200
    assert march_2022_switch.ttype.is_dst() is True
    assert march_2022_switch.ttype.abbreviation == "CEST"

    assert october_2022_switch.at == 1667091600
    assert october_2022_switch.ttype.offset == 3600
    assert october_2022_switch.ttype.is_dst() is False
    assert october_2022_switch.ttype.abbreviation == "CET"


def test_custom_timezone(berlin_timezone_calendar: VCalendar):
    """Test that the offset switches correctly when there is a time change (which is around 2022-03-27)."""
    tz = berlin_timezone_calendar.get_timezone("Europe/Berlin").get_as_timezone_object(DateTime(2023, 1, 1))
    assert DateTime(2022, 1, 1).in_timezone(tz).offset == 3600
    assert DateTime(2022, 4, 1).in_timezone(tz).offset == 7200
