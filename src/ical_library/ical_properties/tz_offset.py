from pendulum.tz.timezone import FixedTimezone

from ical_library.base_classes.property import Property


class _TZOffset(Property):
    """
    Helper class to represent a UTC offset. This class should be inherited.

    Add functions to parse the value as a fixed timezone offset.
    """

    def parse_value_as_seconds(self) -> int:
        """Parse the value as seconds difference from UTC."""
        plus_or_minus = self.value[0]
        hour = int(self.value[1:3])
        minute = int(self.value[3:5])
        seconds = int(self.value[5:7]) if len(self.value) > 6 else 0
        summed = seconds + 60 * (minute + 60 * hour)
        return summed if plus_or_minus == "+" else 0 - summed

    def as_timezone_object(self) -> FixedTimezone:
        """Return the value of the property as a fixed timezone offset."""
        return FixedTimezone(self.parse_value_as_seconds())


class TZOffsetTo(_TZOffset):
    """The TZOFFSETTO property specifies the offset that is in use prior to this time zone observance."""

    pass


class TZOffsetFrom(_TZOffset):
    """The TZOFFSETFROM property specifies the offset that is in use prior to this time zone observance."""

    pass
