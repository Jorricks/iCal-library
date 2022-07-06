from typing import Dict, Iterator, List, Optional, Tuple, Union

from pendulum import Date, DateTime

from ical_reader.base_classes.component import Component
from ical_reader.help_modules import dt_utils, property_utils
from ical_reader.help_modules.timespan import Timespan
from ical_reader.ical_properties.dt import DTStart, LastModified
from ical_reader.ical_properties.pass_properties import Comment, TZID, TZName, TZURL
from ical_reader.ical_properties.periods import RDate
from ical_reader.ical_properties.rrule import RRule
from ical_reader.ical_properties.tz_offset import TZOffsetFrom, TZOffsetTo


class _TimeOffsetPeriod(Component):
    """
    A _TimeOffsetPeriod representing either a Standard configuration or a Winter configuration.

    :param name:
    :param parent:
    :param dtstart:
    :param tzoffsetto:
    :param tzoffsetfrom:
    :param rrule:
    :param comment:
    :param rdate:
    :param tzname:
    """

    def __init__(
        self,
        name: str,
        parent: Optional[Component],
        dtstart: Optional[DTStart] = None,
        tzoffsetto: Optional[TZOffsetTo] = None,
        tzoffsetfrom: Optional[TZOffsetFrom] = None,
        rrule: Optional[RRule] = None,
        comment: Optional[List[Comment]] = None,
        rdate: Optional[List[RDate]] = None,
        tzname: Optional[List[TZName]] = None,
    ):
        super().__init__(name, parent)
        # Required, must occur only once.
        self.dtstart: Optional[DTStart] = dtstart
        self.tzoffsetto: Optional[TZOffsetTo] = tzoffsetto
        self.tzoffsetfrom: Optional[TZOffsetFrom] = tzoffsetfrom
        # Optional, may only occur once.
        self.rrule: Optional[RRule] = rrule
        # Optional, may occur more than once.
        self.comment: Optional[List[Comment]] = comment
        self.rdate: Optional[List[RDate]] = rdate
        self.tzname: Optional[List[TZName]] = tzname

    def timezone_aware_start(self) -> DateTime:
        """Return a timezone aware start."""
        dt: DateTime = dt_utils.convert_time_object_to_datetime(self.dtstart.datetime_or_date_value)
        return dt.in_timezone(tz=self.tzoffsetfrom.as_timezone_object())

    def get_time_sequence(
        self, max_datetime: Optional[DateTime] = None
    ) -> Iterator[Tuple[DateTime, "_TimeOffsetPeriod"]]:
        """
        Expand the TimeZone start date according to its recurring *RDate* and *RRule* properties.
        :param max_datetime: The maximum datetime value we wish to expand to.
        :return: Yield all the datetime values according to the recurring properties that are lower than *max_datetime*.
        """
        for rtime in property_utils.expand_event_in_range_only_return_first(
            rdate_list=self.rdate or [],
            rrule=self.rrule,
            first_event_start=self.timezone_aware_start(),
            return_range=Timespan(self.dtstart.datetime_or_date_value, max_datetime),
            make_tz_aware=self.tzoffsetfrom.as_timezone_object(),
        ):
            if not isinstance(rtime, DateTime):
                raise TypeError(f"{rtime} was expected to be a DateTime object.")
            yield rtime, self


class DayLight(_TimeOffsetPeriod):
    """A TimeOffsetPeriod representing a DayLight(a.k.a. Advanced Time, Summer Time or Legal Time) configuration."""

    def __init__(self, parent: Optional[Component], **kwargs):
        super().__init__("DAYLIGHT", parent)


class Standard(_TimeOffsetPeriod):
    """A TimeOffsetPeriod representing a Standard(a.k.a. Winter Time) configuration."""

    def __init__(self, parent: Optional[Component], **kwargs):
        super().__init__("STANDARD", parent)


class VTimeZone(Component):
    """
    This class represents the VTIMEZONE component specified in RFC 5545 in '3.6.5. Time Zone Component'.

    If present, the "VTIMEZONE" calendar component defines the set of Standard Time and Daylight Saving Time
    observances (or rules) for a particular time zone for a given interval of time. The "VTIMEZONE" calendar component
    cannot be nested within other calendar components. Multiple "VTIMEZONE" calendar components can exist in an
    iCalendar object. In this situation, each "VTIMEZONE" MUST represent a unique time zone definition. This is
    necessary for some classes of events, such as airline flights, that start in one time zone and end in another.

    :param parent:
    :param tzid:
    :param last_mod:
    :param tzurl:
    :param standardc:
    :param daylightc:
    """

    def __init__(
        self,
        parent: Optional[Component],
        tzid: Optional[TZID] = None,
        last_mod: Optional[LastModified] = None,
        tzurl: Optional[TZURL] = None,
        standardc: Optional[List[Standard]] = None,
        daylightc: Optional[List[DayLight]] = None,
    ):
        super().__init__("VTIMEZONE", parent)

        # Required properties, must occur one.
        self.tzid: Optional[TZID] = tzid
        # Optional properties, may only occur once.
        self.last_mod: Optional[LastModified] = last_mod
        self.tzurl: Optional[TZURL] = tzurl
        # Either one of these components must have at least one record. May occur multiple times.
        self.standardc: List[Standard] = standardc or []
        self.daylightc: List[DayLight] = daylightc or []

        self.__storage_of_results: Dict[DateTime, List[Tuple[DateTime, _TimeOffsetPeriod]]] = {}

    def get_ordered_timezone_overview(self, max_datetime: DateTime) -> List[Tuple[DateTime, _TimeOffsetPeriod]]:
        """
        Expand all TimeOffsetPeriod configuration and return them in an ordered by time fashion.
        :param max_datetime: The maximum datetime value we wish to expand to.
        :return: A sorted list on datetime containing tuples of datetime and offset period where the datetime is
        lower than *max_datetime*.
        """
        if max_datetime in self.__storage_of_results.keys():
            return self.__storage_of_results[max_datetime]
        all_timezones: List[Tuple[Union[DateTime, Date], _TimeOffsetPeriod]] = []
        for a_standard in self.standardc:
            all_timezones.extend(a_standard.get_time_sequence(max_datetime=max_datetime))
        for a_daylight in self.daylightc:
            all_timezones.extend(a_daylight.get_time_sequence(max_datetime=max_datetime))
        sorted_list = sorted(all_timezones, key=lambda tup: tup[0])
        self.__storage_of_results[max_datetime] = sorted_list
        return sorted_list

    def convert_naive_datetime_to_aware(self, dt: DateTime) -> DateTime:
        """
        Convert a naive datetime to an aware datetime using the configuration of this TimeZone object.
        :param dt: The (possibly naive) datetime to convert to this timezone configuration.
        :return: The timezone aware datetime.
        """
        if dt.tzinfo is not None:
            return dt

        dt_object: DateTime
        time_offset_period: _TimeOffsetPeriod
        for i, (dt_object, time_offset_period) in enumerate(self.get_ordered_timezone_overview(DateTime(2100, 1, 1))):
            if i == 0 and dt < dt_object.replace(tzinfo=None):
                return dt.in_timezone(time_offset_period.tzoffsetfrom.as_timezone_object())
            if dt > dt_object.replace(tzinfo=None):
                return dt.in_timezone(time_offset_period.tzoffsetto.as_timezone_object())
        return dt
