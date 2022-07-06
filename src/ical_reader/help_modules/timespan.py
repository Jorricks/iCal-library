import functools
from dataclasses import dataclass
from typing import Any, Optional, Tuple, TYPE_CHECKING, Union

from pendulum import Date, DateTime

from ical_reader.help_modules import dt_utils

if TYPE_CHECKING:
    from ical_reader.base_classes.component import Component


@dataclass
@functools.total_ordering
class Timespan:
    """
    Represents a time span with a beginning and end date.

    Contains multiple handy functions when working with a time span like the is_included_in or intersect function.
    """

    begin: DateTime
    end: DateTime

    def __init__(self, begin: Union[Date, DateTime], end: Union[Date, DateTime]):
        """
        Init the Timespan class.

        For simplicity, we immediately convert the variables to timezone aware :class:`pendulum.DateTime` instances.
        :param begin: The beginning of the timespan.
        :param end: The end of the timespan.
        """
        self.begin = dt_utils.convert_time_object_to_aware_datetime(begin)
        self.end = dt_utils.convert_time_object_to_aware_datetime(end)

    @property
    def tuple(self) -> Tuple[DateTime, DateTime]:
        """
        Return the timespan as a tuple.
        :return: The beginning and end in a tuple format.
        """
        return self.begin, self.end

    def get_end_in_same_type(self, time: Union[Date, DateTime]) -> Union[Date, DateTime]:
        """
        Return *self.end* in the same format as *time*.
        :param time: A time format in which we would like to return the *self.end*.
        :return: Return *self.end* in the same format as *time*.
        """
        if not isinstance(time, DateTime):
            return Date(self.end.year, self.end.month, self.end.day)
        elif time.tz is None:  # At this point we know it is a DateTime object.
            return self.end.replace(tzinfo=None)
        return self.end.in_timezone(time.tz)

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
        """
        Check whether the *other* timespan is included within this timespan.
        :param other: Another timespan.
        :return: Boolean whether the *other* timespan is included within this timespan.
        """
        return other.begin <= self.begin and self.end < other.end

    def intersects(self, other: "Timespan") -> bool:
        """
        Check whether the *other* timespan intersects with this timespan.
        :param other: Another timespan.
        :return: boolean whether the *other* timespan intersects with this timespan.
        """
        return (
            self.begin <= other.begin < self.end
            or self.begin <= other.end < self.end
            or other.begin <= self.begin < other.end
            or other.begin <= self.end < other.end
        )

    def includes(self, instant: Union[Date, DateTime]) -> bool:
        """
        Check if the *instant* is included in this timespan.
        :param instant: An instance that represents a moment in time.
        """
        dt = dt_utils.convert_time_object_to_aware_datetime(instant)
        return self.begin <= dt < self.end


@dataclass
class TimespanWithParent(Timespan):
    parent: Optional["Component"]

    def __init__(self, parent: Optional["Component"], begin: Union[Date, DateTime], end: Union[Date, DateTime]):
        """
        Init a Timespan object which represents the length of a specific component.

        For simplicity, we immediately convert the variables to timezone aware :class:`pendulum.DateTime` instances.
        :param parent: The component instance which this timespan represents.
        :param begin: The beginning of the timespan.
        :param end: The end of the timespan.
        """
        super().__init__(begin, end)
        self.parent = parent
