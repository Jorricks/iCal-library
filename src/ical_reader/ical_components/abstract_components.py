from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, List, Optional, TYPE_CHECKING, TypeVar, Union

from pendulum import Date, DateTime, Duration, Period

from ical_reader.base_classes.calendar_component import CalendarComponent
from ical_reader.base_classes.property import Property
from ical_reader.help_classes.timespan import TimespanWithParent
from ical_reader.ical_properties.dt import _DTBoth, DTStamp, DTStart
from ical_reader.ical_properties.pass_properties import Comment, Summary, UID
from ical_reader.ical_properties.periods import EXDate, RDate
from ical_reader.ical_properties.rrule import RRule
from ical_reader.ical_utils.lru_cache import instance_lru_cache

if TYPE_CHECKING:
    from ical_reader.ical_components.v_event import VEvent  # noqa: F401
    from ical_reader.ical_components.v_journal import VJournal  # noqa: F401
    from ical_reader.ical_components.v_todo import VToDo  # noqa: F401

T = TypeVar(
    "T",
    "VEvent",
    "VToDo",
)


@dataclass(repr=False)
class AbstractStartStopComponent(CalendarComponent, ABC):
    """
    This class helps with Events that have recurring properties luke rrule, rdate and exdate.

    Note: The out one out here is VJournal as these events don't have a duration.
    Therefore,
    """

    # Required
    dtstamp: Optional[DTStamp] = None
    uid: Optional[UID] = None

    # Optional, may only occur once
    dtstart: Optional[DTStart] = None
    rrule: Optional[RRule] = None
    summary: Optional[Summary] = None

    # Optional, may occur more than once
    exdate: Optional[List[EXDate]] = None
    rdate: Optional[List[RDate]] = None
    comment: Optional[List[Comment]] = None

    @property
    @abstractmethod
    def ending(self) -> _DTBoth:
        """As the argument for this is different in each class, we ask this to be implemented."""
        pass

    @abstractmethod
    def get_duration(self) -> Optional[Duration]:
        """As the duration is not present in each of them, we ask this to be implemented."""
        pass

    @staticmethod
    def compare_property_value(own: Property, others: Property) -> bool:
        if not own and others or own and not others:
            return False
        if own and others and own.as_original_string != others.as_original_string:
            return False
        return True

    @staticmethod
    def compare_property_list(own: List[Property], others: List[Property]) -> bool:
        if not own and others or own and not others:
            return False
        if not own and not others:
            return True
        if len(own) != len(others):
            return False
        for i in range(len(own)):
            if own[i].as_original_string != others[i].as_original_string:
                return False
        return True

    def __eq__(self: "AbstractStartStopComponent", other: "AbstractStartStopComponent") -> bool:
        return (
            self.compare_property_value(self.dtstart, other.dtstart)
            and self.compare_property_value(self.ending, other.ending)
            and self.compare_property_value(self.summary, other.summary)
            and self.compare_property_list(self.comment, other.comment)
        )

    @property
    def timespan(self) -> TimespanWithParent:
        if self.start is None or self.end is None:
            raise ValueError(f"{self.start=} and {self.end=} may not be None.")
        return TimespanWithParent(parent=self, begin=self.start, end=self.end)

    @property
    @instance_lru_cache()
    def start(self) -> Union[Date, DateTime]:
        return self.dtstart.datetime_or_date_value

    @property
    @instance_lru_cache()
    def end(self) -> Optional[Union[Date, DateTime]]:
        if self.ending:
            return self.ending.datetime_or_date_value
        elif self.start and self.get_duration():
            return self.start + self.get_duration()
        return None

    @property
    @instance_lru_cache()
    def computed_duration(self: "AbstractStartStopComponent") -> Optional[Duration]:
        if a_duration := self.get_duration():
            return a_duration
        elif self.end and self.start:
            result: Period = self.end - self.start
            return result
        return None


@dataclass(repr=False)
class AbstractRecurringComponent(AbstractStartStopComponent, ABC):
    def __getattribute__(self, name: str) -> Any:
        if name in ("_start", "_end", "_original", "_parent", "start", "end", "original", "parent"):
            return object.__getattribute__(self, name)
        if name in ("_name", "_extra_child_components", "_extra_properties"):
            return object.__getattribute__(self._original, name)
        if name in self._original._get_property_attributes():
            return object.__getattribute__(self._original, name)
        return object.__getattribute__(self, name)

    @property
    def start(self) -> DateTime:
        return self._start

    @property
    def end(self) -> DateTime:
        return self._end

    @property
    def original(self) -> AbstractStartStopComponent:
        return self._original

    @property
    def parent(self) -> "CalendarComponent":
        return self._original._parent
