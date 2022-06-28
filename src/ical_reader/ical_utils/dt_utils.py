from typing import Union, Optional

import pendulum
from pendulum import Date, DateTime
from pendulum.tz import get_local_timezone
from pendulum.tz.timezone import Timezone


def parse_date_or_datetime(value: str) -> Union[Date, DateTime]:
    if len(value) == 8:
        return pendulum.Date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    return pendulum.parse(value, tz=None)


def convert_time_object_to_datetime(time_value: Union[Date, DateTime]) -> DateTime:
    if isinstance(time_value, DateTime):
        return time_value
    return DateTime(time_value.year, time_value.month, time_value.day)


def make_datetime_aware(dt: DateTime, tz: Optional[Union[str, Timezone]] = None):
    if dt.tz is not None:
        return dt
    timezone: Timezone = (tz if isinstance(tz, Timezone) else pendulum.timezone(tz)) if tz else get_local_timezone()
    return dt.in_timezone(timezone)


def convert_time_object_to_aware_datetime(
    time_value: Union[Date, DateTime], tz: Optional[Union[str, Timezone]] = None
) -> DateTime:
    dt: DateTime = convert_time_object_to_datetime(time_value)
    return make_datetime_aware(dt, tz)
