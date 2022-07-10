from abc import ABC, abstractmethod
from typing import Any, List, Optional, TYPE_CHECKING, TypeVar, Union

from pendulum import Date, DateTime, Duration, Period

from ical_reader.base_classes.component import Component
from ical_reader.base_classes.property import Property
from ical_reader.exceptions import MissingRequiredProperty
from ical_reader.help_modules.lru_cache import instance_lru_cache
from ical_reader.help_modules.timespan import TimespanWithParent
from ical_reader.ical_properties.dt import _DTBoth, DTStamp, DTStart
from ical_reader.ical_properties.pass_properties import Comment, Summary, UID
from ical_reader.ical_properties.periods import EXDate, RDate
from ical_reader.ical_properties.rrule import RRule

if TYPE_CHECKING:
    from ical_reader.ical_components import VEvent, VJournal, VToDo  # noqa: F401

T = TypeVar(
    "T",
    "VEvent",
    "VToDo",
)


class AbstractStartStopComponent(Component, ABC):
    """
    This class helps avoid code repetition with different :class:`Component` classes.

    This class is inherited by VEvent, VToDo and VJournal as these all have recurring properties like :class:`RRule`,
    :class:`RDate` and :class:`EXDate`. All properties they had in common are part of this class.
    Note: VJournal is the odd one out as these events don't have a duration.

    :param name: The actual name of this component instance. E.g. VEVENT, RRULE, VCUSTOMCOMPONENT.
    :param parent: The Component this item is encapsulated by in the iCalendar data file.
    :param dtstamp: The DTStamp property. Required and must occur exactly once.
    :param uid: The UID property. Required and must occur exactly once.
    :param dtstart: The DTStart property. Optional and may occur at most once.
    :param rrule: The RRule property. Optional and may occur at most once.
    :param summary: The Summary property. Optional and may occur at most once.
    :param exdate: The EXDate property. Optional, but may occur multiple times.
    :param rdate: The RDate property. Optional, but may occur multiple times.
    :param comment: The Comment property. Optional, but may occur multiple times.
    """

    def __init__(
        self,
        name: str,
        parent: Optional[Component],
        dtstamp: Optional[DTStamp] = None,
        uid: Optional[UID] = None,
        dtstart: Optional[DTStart] = None,
        rrule: Optional[RRule] = None,
        summary: Optional[Summary] = None,
        exdate: Optional[List[EXDate]] = None,
        rdate: Optional[List[RDate]] = None,
        comment: Optional[List[Comment]] = None,
    ):
        super().__init__(name, parent)

        # Required
        self._dtstamp: Optional[DTStamp] = dtstamp
        self._uid: Optional[UID] = uid

        # Optional, may only occur once
        self.dtstart: Optional[DTStart] = dtstart
        self.rrule: Optional[RRule] = rrule
        self.summary: Optional[Summary] = summary

        # Optional, may occur more than once
        self.exdate: Optional[List[EXDate]] = exdate
        self.rdate: Optional[List[RDate]] = rdate
        self.comment: Optional[List[Comment]] = comment

    @property
    def dtstamp(self) -> DTStamp:
        """A getter to ensure the required property is set."""
        if self._dtstamp is None:
            raise MissingRequiredProperty(self, "dtstamp")
        return self._dtstamp

    @dtstamp.setter
    def dtstamp(self, value: DTStamp):
        """A setter to set the required property."""
        self._dtstamp = value

    @property
    def uid(self) -> UID:
        """A getter to ensure the required property is set."""
        if self._uid is None:
            raise MissingRequiredProperty(self, "uid")
        return self._uid

    @uid.setter
    def uid(self, value: UID):
        """A setter to set the required property."""
        self._uid = value

    @property
    @abstractmethod
    def ending(self) -> _DTBoth:
        """
        As the argument for this is different in each class, we ask this to be implemented.

        :return: The ending of the :class:`Component`, except for :class:`VJournal` which returns the start.
        """
        pass

    @abstractmethod
    def get_duration(self) -> Optional[Duration]:
        """
        As the duration is not present in each of them, we ask this to be implemented by the subclasses.

        :return: The duration of the :class:`Component`.
        """
        pass

    @staticmethod
    def compare_property_value(own: Property, others: Property) -> bool:
        """
        Compare two properties for whether they are the same.
        :param own: The instance own property.
        :param others: A property of another :class:`Component` instance.
        :return: Boolean of whether they are the same.
        """
        if not own and others or own and not others:
            return False
        if own and others and own.as_original_string != others.as_original_string:
            return False
        return True

    @staticmethod
    def compare_property_list(own: List[Property], others: List[Property]) -> bool:
        """
        Compare a list of two properties for whether they are the same.
        :param own: The list of properties from the :class:`Component` instance itself.
        :param others: A list of properties from the other :class:`Component` instance.
        :return: Boolean of whether they are the same.
        """
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
        """Return whether the current instance and the other instance are the same."""
        if type(self) != type(other):
            return False
        return (
            self.compare_property_value(self.dtstart, other.dtstart)
            and self.compare_property_value(self.ending, other.ending)
            and self.compare_property_value(self.summary, other.summary)
            and self.compare_property_list(self.comment, other.comment)
        )

    @property
    def timespan(self) -> TimespanWithParent:
        """
        Return a timespan as a property representing the start and end of the instance.
        :return: A timespan instance with this class instance as parent.
        """
        if self.start is None or self.end is None:
            raise ValueError(f"{self.start=} and {self.end=} may not be None.")
        return TimespanWithParent(parent=self, begin=self.start, end=self.end)

    @property
    @instance_lru_cache()
    def start(self) -> Optional[Union[Date, DateTime]]:
        """Return the start of this Component as a :class:`Date` or :class:`DateTime` value."""
        return self.dtstart.datetime_or_date_value if self.dtstart else None

    @property
    @instance_lru_cache()
    def end(self) -> Optional[Union[Date, DateTime]]:
        """Return the ending of this Component as a Date or DateTime value."""
        if self.ending:
            return self.ending.datetime_or_date_value
        elif self.start and self.get_duration():
            return self.start + self.get_duration()
        return None

    @property
    @instance_lru_cache()
    def computed_duration(self: "AbstractStartStopComponent") -> Optional[Duration]:
        """Return the duration of this Component as a :class:`Date` or :class:`DateTime` value."""
        if a_duration := self.get_duration():
            return a_duration
        elif self.end and self.start:
            result: Period = self.end - self.start
            return result
        return None


class AbstractRecurringComponent(AbstractStartStopComponent, ABC):
    """
    This class extends :class:`AbstractStartStopComponent` to represent a recurring Component.

    This class is inherited by VRecurringEvent, VRecurringToDo and VRecurringJournal. When we compute the recurrence
    based on the :class:`RRule`, :class:`RDate` and :class:`EXDate` properties, we create new occurrences of that
    specific component. Instead of copying over all Properties (and using a lot of memory), this class overwrites the
    *__getattribute__* function to act like the original component for most attributes except for *start*, *end*,
    *original* and *parent*.
    """

    def __getattribute__(self, name: str) -> Any:
        """
        Overwrite this function to return the originals properties except for *start*, *end*, *original* and *parent*.

        Depending on the attributes *name* we are requesting, we either return its own properties or the original
        components properties. This way we don't need to copy over all the variables.
        :param name: Name of the attribute we are accessing.
        :return: The value of the attribute we are accessing either from the *original* or from this instance itself.
        """
        if name in ("_start", "_end", "_original", "_parent", "start", "end", "original", "parent"):
            return object.__getattribute__(self, name)
        if name in ("_name", "_extra_child_components", "_extra_properties"):
            return object.__getattribute__(self._original, name)
        if name in self._original.get_property_ical_names():
            return object.__getattribute__(self._original, name)
        return object.__getattribute__(self, name)

    @property
    def start(self) -> DateTime:
        """Return the start of this recurring event."""
        return self._start

    @property
    def end(self) -> DateTime:
        """Return the end of this recurring event."""
        return self._end

    @property
    def original(self) -> AbstractStartStopComponent:
        """Return the original component that created this recurring component."""
        return self._original

    @property
    def parent(self) -> Component:
        """Return the parent of the original component."""
        return self._original.parent
