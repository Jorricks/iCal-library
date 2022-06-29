from typing import Dict, Iterator, List, Optional, Tuple, Union

import pendulum
from dateutil import rrule as base_for_time_periods
from dateutil.rrule import rrule, weekday
from pendulum import Date, DateTime

from ical_reader.base_classes.calendar_component import CalendarComponent
from ical_reader.base_classes.property import Property
from ical_reader.ical_utils import dt_utils
from ical_reader.ical_utils.lru_cache import instance_lru_cache


class RRule(Property):
    def __init__(self, parent: CalendarComponent, name: str, sub_properties: str, value: str):
        super().__init__(parent=parent, name=name, sub_properties=sub_properties, value=value)

    @property
    @instance_lru_cache()
    def dict(self) -> Dict[str, str]:
        return dict([tuple(key_and_value.split("=")) for key_and_value in self._value.split(";")])

    @property
    def freq(self) -> int:
        """0 for MO, 1 for TU, 2 for WE, ..."""
        return getattr(base_for_time_periods, self.dict["FREQ"])

    @property
    def until(self) -> Optional[Union[Date, DateTime]]:
        if (until_value := self.dict.get("UNTIL", None)) is not None:
            return dt_utils.parse_date_or_datetime(until_value)
        return None

    @property
    def count(self) -> Optional[int]:
        count_value = self.dict.get("COUNT", None)
        return int(count_value) if count_value else None

    @property
    def interval(self) -> int:
        return int(self.dict.get("INTERVAL", 1))

    @staticmethod
    def convert_str_to_optional_integer_tuple(value: Optional[str]) -> Optional[Tuple[int, ...]]:
        if not value:
            return None
        return tuple(int(item) for item in value.split(","))

    @property
    def by_second(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYSECOND"))

    @property
    def by_minute(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYMINUTE"))

    @property
    def by_hour(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYHOUR"))

    @property
    def by_day(self) -> Optional[Union[Tuple[int, ...], Tuple[weekday, ...]]]:
        """Note: To prevent confusion, this was renamed to byweekday in dateutil.rrule."""
        day_list: List[
            weekday,
        ] = []
        value = self.dict.get("BYDAY")
        if not value:
            return None
        for a_day in value.split(","):
            if a_day[-2:] not in ("SU", "MO", "TU", "WE", "TH", "FR", "SA"):
                raise ValueError
            if len(a_day) > 2:
                day_list.append(getattr(base_for_time_periods, a_day[-2:])(int(a_day[0:-2])))
            else:
                day_list.append(getattr(base_for_time_periods, a_day))
        return tuple(day_list)

    @property
    def by_month_day(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYMONTHDAY"))

    @property
    def by_year_day(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYYEARDAY"))

    @property
    def by_week_no(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYWEEKNO"))

    @property
    def by_month(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYMONTH"))

    @property
    def by_set_pos(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYSETPOS"))

    @property
    def wkst(self) -> Optional[int]:
        day = self.dict.get("WKST")
        if not day:
            return None
        if day[-2:] not in ("SU", "MO", "TU", "WE", "TH", "FR", "SA"):
            raise ValueError(f"{day[-2:]=} is not in the list of weekdays.")
        if len(day) != 2:
            print(f"WARNING! We have a unique WKST: {day=}.")
        return getattr(base_for_time_periods, day)

    @property
    def by_easter(self) -> Optional[Tuple[int, ...]]:
        return self.convert_str_to_optional_integer_tuple(self.dict.get("BYEASTER"))

    def sequence_iterator(
        self, starting_datetime: Union[Date, DateTime], max_datetime: Union[Date, DateTime]
    ) -> Iterator[DateTime]:
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
            "byweekday": self.by_day,
            "bymonthday": self.by_month_day,
            "byyearday": self.by_year_day,
            "byweekno": self.by_week_no,
            "bymonth": self.by_month,
            "bysetpos": self.by_set_pos,
            "wkst": self.wkst,
            "byeaster": self.by_easter,
        }
        no_none_keywords = {key: value for key, value in keyword_arguments.items() if value is not None}
        dt_iterator = rrule(dtstart=starting_datetime, freq=self.freq, **no_none_keywords)
        for dt in dt_iterator:
            if dt > max_datetime:
                break
            p_instance = pendulum.instance(dt, tz=None)
            yield p_instance if is_datetime_format else p_instance.date()


# if __name__ == "__main__":
#     r_rule = RRule.create_property_from_str(None, "RRULE:FREQ=WEEKLY;UNTIL=20220608T215959Z;BYDAY=FR,MO,TH,TU,WE")
#     for an_item in r_rule.sequence_iterator(
#         DateTime(2022, 5, 1, 12, 13, 14).in_tz("UTC"), DateTime(2022, 6, 8, 12, 13, 14).in_tz("UTC")
#     ):
#         print(an_item)
#
#     r_rule = RRule.create_property_from_str(None, "RRULE:FREQ=WEEKLY;WKST=MO;COUNT=5;INTERVAL=10;BYDAY=WE")
#     for an_item in r_rule.sequence_iterator(Date(2022, 3, 2), Date(2030, 3, 20)):
#         print(an_item)
