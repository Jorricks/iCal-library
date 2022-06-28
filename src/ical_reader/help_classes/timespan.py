import functools
from dataclasses import dataclass
from typing import Optional, Tuple, Any, Union

from pendulum import DateTime, Date

from ical_reader.ical_utils import dt_utils


@dataclass
@functools.total_ordering
class Timespan:
    begin: DateTime
    end: DateTime

    def __init__(self, begin: Union[Date, DateTime], end: Union[Date, DateTime]):
        self.begin = dt_utils.convert_time_object_to_aware_datetime(begin)
        self.end = dt_utils.convert_time_object_to_aware_datetime(end)

    @property
    def tuple(self) -> Tuple[DateTime, DateTime]:
        return self.begin, self.end

    def get_end_in_same_type(self, time: Union[Date, DateTime]):
        if not isinstance(time, DateTime):
            return Date(self.end.year, self.end.month, self.end.day)
        elif time.tz is None:
            return self.end.replace(tzinfo=None)
        return self.end.in_timezone(time.tz)

    def execute_compare(self, other: "Timespan") -> bool:
        if isinstance(other, Timespan):
            return self.tuple < other.tuple
        else:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Timespan):
            return self.tuple < other.tuple
        else:
            return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Timespan):
            return self.tuple > other.tuple
        else:
            return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Timespan):
            return self.tuple <= other.tuple
        else:
            return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Timespan):
            return self.tuple >= other.tuple
        else:
            return NotImplemented

    def is_included_in(self, other: "Timespan") -> bool:
        return other.begin <= self.begin and self.end < other.end

    def intersects(self, other: "Timespan") -> bool:
        return self.begin <= other.begin < self.end or \
               self.begin <= other.end < self.end or \
               other.begin <= self.begin < other.end or \
               other.begin <= self.end < other.end

    def includes(self, instant: Union[Date, DateTime]) -> bool:
        dt = dt_utils.convert_time_object_to_aware_datetime(instant)
        return self.begin <= dt < self.end


@dataclass
class TimespanWithParent(Timespan):
    parent: Optional["TreeComponent"]

    def __init__(self, parent: Optional["TreeComponent"], begin: Union[Date, DateTime], end: Union[Date, DateTime]):
        super().__init__(begin, end)
        self.parent = parent
