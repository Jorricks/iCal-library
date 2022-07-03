from typing import Optional, Union

import pendulum
from pendulum import Date, DateTime
from pendulum.tz import get_local_timezone
from pendulum.tz.timezone import Timezone


# @ToDo(jorrick) add doc strings here.
def parse_date_or_datetime(value: str) -> Union[Date, DateTime]:
    """Parse a string into a pendulum.Date or pendulum.Datetime."""
    if len(value) == 8:
        return pendulum.Date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
    return pendulum.parse(value, tz=None)


def convert_time_object_to_datetime(time_value: Union[Date, DateTime]) -> DateTime:
    """Convert the argument to a pendulum.DateTime object whether it's a pendulum.Date or a pendulum.DateTime."""
    if isinstance(time_value, DateTime):
        return time_value
    return DateTime(time_value.year, time_value.month, time_value.day)


def make_datetime_aware(dt: DateTime, tz: Optional[Union[str, Timezone]] = None):
    """
    Make a pendulum.DateTime timezone aware.

    When it already has a timezone, it doesn't change the timezone. If it doesn't, it will add the timezone.
    """
    if dt.tz is not None:
        return dt
    timezone: Timezone = (tz if isinstance(tz, Timezone) else pendulum.timezone(tz)) if tz else get_local_timezone()
    return dt.in_timezone(timezone)


def convert_time_object_to_aware_datetime(
    time_value: Union[Date, DateTime], tz: Optional[Union[str, Timezone]] = None
) -> DateTime:
    """Convert a time pendulum.Date or pendulum.DateTime to a timezone aware pendulum.DateTime."""
    dt: DateTime = convert_time_object_to_datetime(time_value)
    return make_datetime_aware(dt, tz)
