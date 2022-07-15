from typing import Dict, Iterator, List, Literal, Optional, Tuple, Union

import pendulum
from dateutil import rrule as base_for_time_periods
from dateutil.rrule import rrule, weekday
from pendulum import Date, DateTime, Duration

from ical_library.base_classes.property import Property
from ical_library.help_modules import dt_utils
from ical_library.help_modules.lru_cache import instance_lru_cache


class RRule(Property):
    """
    The RRULE property defines a rule or repeating pattern for recurring events, to-dos, journal entries, or time zone
    definitions.

    For more in depth restrictions and possibilities we refer you to the `RTFC 5545` section `3.3.10. Recurrence Rule`.
    """

    @property
    @instance_lru_cache()
    def value_as_dict(self) -> Dict[str, str]:
        """
        Parse all recurrence rule parts as a dictionary, so it can be used as an easy lookup.
        :return: A dict mapping of str to str containing all recurrence rule parts.
        """
        all_values = [tuple(key_and_value.split("=")) for key_and_value in self._value.split(";")]
        return {key: value for key, value in all_values}

    @property
    def freq(self) -> str:
        """
        The FREQUENCY rule identifies the type of recurrence rule. Possible values are: SECONDLY, MINUTELY, HOURLY,
        DAILY, WEEKLY, MONTHLY and YEARLY.
        This is the only required field.
        :return: The frequency as a string.
        """
        return self.value_as_dict["FREQ"]

    @property
    def freq_dateutil(self) -> int:
        """
        Return the frequency in the format dateutil expects which is a map of the string to an integer.
        :return: An integer in the range of 0 to 6.
        """
        return getattr(base_for_time_periods, self.freq)

    @property
    def until(self) -> Optional[Union[Date, DateTime]]:
        """
        The UNTIL rule defines a DATE or DATE-TIME value that bounds the recurrence rule in an inclusive manner.
        This is optional but may not occur together with COUNT.
        :return: None or a positive integer.
        """
        if (until_value := self.value_as_dict.get("UNTIL", None)) is not None:
            return dt_utils.parse_date_or_datetime(until_value)
        return None

    @property
    def count(self) -> Optional[int]:
        """
        The COUNT rule defines the number of occurrences at which to range-bound the recurrence.
        This is optional but may not occur together with UNTIL.
        :return: None or a positive integer.
        """
        count_value = self.value_as_dict.get("COUNT", None)
        return int(count_value) if count_value else None

    @property
    def interval(self) -> int:
        """
        The INTERVAL rule contains a positive integer representing at which intervals the recurrence rule repeats.
        :return: A positive integer.
        """
        return int(self.value_as_dict.get("INTERVAL", 1))

    @staticmethod
    def convert_str_to_optional_integer_tuple(value: Optional[str]) -> Optional[Tuple[int, ...]]:
        """
        Converts a string to a Tuple of integers.
        :return: None or a Tuple of integers if the value exists, otherwise None.
        """
        if not value:
            return None
        return tuple(int(item) for item in value.split(","))

    @property
    def by_second(self) -> Optional[Tuple[int, ...]]:
        """
        The BYSECOND rule part specifies a COMMA-separated list of seconds within a minute.
        :return: None or a list of integers in the range of 0 to 60.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYSECOND"))

    @property
    def by_minute(self) -> Optional[Tuple[int, ...]]:
        """
        The BYMINUTE rule part specifies a COMMA-separated list of minutes within an hour.
        :return: None or a list of integers in the range of 0 to 59.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYMINUTE"))

    @property
    def by_hour(self) -> Optional[Tuple[int, ...]]:
        """
        The BYHOUR rule part specifies a COMMA-separated list of hours of the day.
        :return: None or a list of integers in the range of 0 to 23.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYHOUR"))

    def by_day(self) -> Optional[List[Tuple[Optional[int], Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"]]]]:
        """
        The BYDAY rule part specifies a COMMA-separated list of days of the week;
        SU indicates Sunday; MO indicates Monday; TU indicates Tuesday; WE indicates Wednesday;
        TH indicates Thursday; FR indicates Friday; and SA indicates Saturday.

        Each BYDAY value can also be preceded by a positive (+n) or negative (-n) integer.
        If present, this indicates the nth occurrence of a specific day within the MONTHLY or YEARLY "RRULE".

        Example values are SU,TU or +2SU,-3TU

        :return None or a list of tuples of two values. The first value represents possible specified nth occurrence or
        None. The second value the day of the week as a SU, MO, TU, WE, TH, FR or SA.
        """
        value = self.value_as_dict.get("BYDAY")
        if not value:
            return None
        list_of_days: List[Tuple[Optional[int], Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"]]] = []
        for a_day in value.split(","):
            a_day = a_day.strip()
            nth_occurence: Optional[int] = int(a_day[:-2]) if len(a_day) > 2 else None
            day_of_week: str = a_day[-2:]
            if day_of_week not in ("SU", "MO", "TU", "WE", "TH", "FR", "SA"):
                raise ValueError
            list_of_days.append((nth_occurence, day_of_week))  # type: ignore
        return list_of_days

    @property
    def by_day_dateutil(self) -> Optional[Tuple[weekday, ...]]:
        """
        Return the by_day in the format dateutil expects which is a tuple of weekday instance.
        :return: None or a tuple of weekday instances which is a type native to dateutil.
        """
        day_list: List[weekday] = []
        by_day = self.by_day()
        if by_day is None:
            return None
        for optional_nth_occurrence, weekday_str in by_day:
            try:
                if optional_nth_occurrence is not None:
                    day_list.append(getattr(base_for_time_periods, weekday_str)(optional_nth_occurrence))
                else:
                    day_list.append(getattr(base_for_time_periods, weekday_str))
            except Exception as exc:
                raise ValueError(f"{optional_nth_occurrence=}, {weekday_str=}") from exc
        return tuple(day_list)

    @property
    def by_month_day(self) -> Optional[Tuple[int, ...]]:
        """
        The BYMONTHDAY rule part specifies a COMMA-separated list of days of the month.
        For example: -10 represents the tenth to the last day of the month.
        :return: None or a tuple of integers in the range of 1 to 31 or -31 to -1.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYMONTHDAY"))

    @property
    def by_year_day(self) -> Optional[Tuple[int, ...]]:
        """
        The BYYEARDAY rule part specifies a COMMA-separated list of days of the year.
        For example: -1 represents the last day of the year (December 31st).
        :return: None or a tuple of integers in the range of 1 to 366 or -366 to -1.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYYEARDAY"))

    @property
    def by_week_no(self) -> Optional[Tuple[int, ...]]:
        """
        The BYWEEKNO rule part specifies a COMMA-separated list of ordinals specifying weeks of the year.
        For example: 3 represents the third week of the year.
        :return: None or an integer in the range of 1 to 53 or -53 to -1.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYWEEKNO"))

    @property
    def by_month(self) -> Optional[Tuple[int, ...]]:
        """
        The BYMONTH rule part specifies a COMMA-separated list of months of the year.
        :return: None or a list of integers in the range of 1 to 12.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYMONTH"))

    @property
    def by_set_pos(self) -> Optional[Tuple[int, ...]]:
        """
        The BYSETPOS rule part specifies a COMMA-separated list of values that corresponds to the nth occurrence within
        the set of recurrence instances specified by the rule. BYSETPOS operates on a set of recurrence instances in
        one interval of the recurrence rule. For example, in a WEEKLY rule, the interval would be one week A set of
        recurrence instances starts at the beginning of the interval defined by the FREQ rule part.
        :return: None or a list of integers in the range of 1 to 366 or -366 to -1.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYSETPOS"))

    @property
    def wkst(self) -> Optional[str]:
        """
        The WKST rule part specifies the day on which the workweek starts.
        :return: A string that is the value of MO, TU, WE, TH, FR, SA, or SU or None.
        """
        day = self.value_as_dict.get("WKST")
        if not day:
            return None
        if day not in ("SU", "MO", "TU", "WE", "TH", "FR", "SA"):
            raise ValueError(f"{day=} is not in the list of weekdays.")
        return day

    @property
    def wkst_dateutil(self) -> Optional[int]:
        """
        Return the wkst in the format dateutil expects which is an integer. 0 for MO, 1 for TU, 2 for WE, ...
        :return: An integer in the range of 0 to 6 or None.
        """
        day = self.wkst
        return getattr(base_for_time_periods, day) if self.wkst is not None else None

    @property
    def by_easter(self) -> Optional[Tuple[int, ...]]:
        """
        According to dateutil, this is an extension of the RFC specification.. I can't find it. If anyone can, please
        file an issue or a PR to add it here as a reference.

        The BYEASTER rule part specifies the offset from the Easter Sunday.
        :return: None or an integer in the range of 1 to 366 or -366 to -1 or None.
        """
        return self.convert_str_to_optional_integer_tuple(self.value_as_dict.get("BYEASTER"))

    def compute_max_end_date(self, starting_datetime: Union[Date, DateTime], component_duration: Duration) -> DateTime:
        """
        To speed up the computation of the Timelines range, it's good to know the ending of the last recurring event
        of a recurrence property. This does not need to be perfect, it should just be an estimate (so we don't check
        EXDate and such).
        :param starting_datetime: The starting datetime from which we start computing the next occurrences.
        :param component_duration: The duration of the component which has the recurring properties.
        :return: An estimate of the maximum end date across all occurrences. This value should always be at least the
        actual highest recurrence end date
        """
        if self.until:
            return dt_utils.convert_time_object_to_aware_datetime(self.until) + component_duration  # type: ignore
        elif self.count:
            if self.count < 1000:
                *_, last = self.sequence_iterator(starting_datetime=starting_datetime, max_datetime=DateTime.max)
                return dt_utils.convert_time_object_to_aware_datetime(last) + component_duration  # type: ignore
        return DateTime.max

    def sequence_iterator(
        self, starting_datetime: Union[Date, DateTime], max_datetime: Union[Date, DateTime]
    ) -> Iterator[DateTime]:
        """
        Given a starting datetime, we compute dates according to the RRule specification until the end of the sequence
        according to the specification is reached or until we reached the max_datetime.
        :param starting_datetime: The starting datetime from which we start computing the next occurrences.
        :param max_datetime: The maximum datetime. If we reach this datetime, we stop the iteration..
        :return: Yield all datetimes(except itself) in the sequence.
        """
        if type(starting_datetime) != type(max_datetime):
            raise TypeError(f"{type(starting_datetime)=} and {type(max_datetime)=} should be of the same type.")
        if isinstance(starting_datetime, DateTime):
            if (starting_datetime.tz or max_datetime.tz) and (not starting_datetime.tz or not max_datetime.tz):
                raise TypeError(f"The tz info should be consistent: {starting_datetime=}, {max_datetime=}.")
        if not isinstance(starting_datetime, (Date, DateTime)) or not isinstance(max_datetime, (Date, DateTime)):
            raise TypeError(f"{type(starting_datetime)=} and {type(max_datetime)=} should be of Date or DateTime.")
        if starting_datetime >= max_datetime:
            raise ValueError(f"This should not be the case: {starting_datetime=} >= {max_datetime=} .")

        if not (is_datetime_format := isinstance(starting_datetime, DateTime) and isinstance(max_datetime, DateTime)):
            starting_datetime = DateTime(starting_datetime.year, starting_datetime.month, starting_datetime.day)
            max_datetime = DateTime(max_datetime.year, max_datetime.month, max_datetime.day)

        starting_datetime = starting_datetime
        max_datetime = max_datetime
        starting_tz = starting_datetime.tz
        until = self.until
        if until:
            if not isinstance(until, DateTime):
                until = DateTime(until.year, until.month, until.day)
            until = until.replace(tzinfo=None) if starting_tz is None else until.in_timezone(starting_tz)

        keyword_arguments = {
            "until": until,
            "count": self.count,
            "interval": self.interval,
            "bysecond": self.by_second,
            "byminute": self.by_minute,
            "byhour": self.by_hour,
            "byweekday": self.by_day_dateutil,
            "bymonthday": self.by_month_day,
            "byyearday": self.by_year_day,
            "byweekno": self.by_week_no,
            "bymonth": self.by_month,
            "bysetpos": self.by_set_pos,
            "wkst": self.wkst_dateutil,
            "byeaster": self.by_easter,
        }
        no_none_keywords = {key: value for key, value in keyword_arguments.items() if value is not None}
        dt_iterator = rrule(dtstart=starting_datetime, freq=self.freq_dateutil, **no_none_keywords)
        for dt in dt_iterator:
            if dt > max_datetime:
                break
            p_instance = pendulum.instance(dt, tz=None)
            yield p_instance if is_datetime_format else p_instance.date()


# if __name__ == "__main__":
#     r_rule: RRule = RRule(None, "RRULE", None, "FREQ=WEEKLY;UNTIL=20220608T215959Z;BYDAY=FR,MO,TH,TU,WE")
#     for an_item in r_rule.sequence_iterator(
#         DateTime(2022, 5, 1, 12, 13, 14).in_tz("UTC"), DateTime(2022, 6, 8, 12, 13, 14).in_tz("UTC")
#     ):
#         print(an_item)
#
#     r_rule = RRule(None, "RRULE", None, "FREQ=WEEKLY;WKST=MO;COUNT=5;INTERVAL=10;BYDAY=WE")
#     for an_item in r_rule.sequence_iterator(Date(2022, 3, 2), Date(2030, 3, 20)):
#         print(an_item)
