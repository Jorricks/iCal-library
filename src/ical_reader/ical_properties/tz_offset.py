from pendulum.tz.timezone import FixedTimezone

from ical_reader.base_classes.property import Property


class _TZOffset(Property):
    def parse_value_as_seconds(self) -> int:
        plus_or_minus = self.value[0]
        hour = int(self.value[1:3])
        minute = int(self.value[3:5])
        seconds = int(self.value[5:7]) if len(self.value) > 6 else 0
        summed = seconds + 60 * (minute + 60 * hour)
        return summed if plus_or_minus == "+" else 0 - summed

    def as_timezone_object(self) -> FixedTimezone:
        return FixedTimezone(self.parse_value_as_seconds())


class TZOffsetTo(_TZOffset):
    pass


class TZOffsetFrom(_TZOffset):
    pass
