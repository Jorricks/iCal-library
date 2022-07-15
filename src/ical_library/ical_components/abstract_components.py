from abc import ABC, abstractmethod
from typing import Any, Iterator, List, Optional, Union

from pendulum import Date, DateTime, Duration, Period

from ical_library.base_classes.component import Component
from ical_library.exceptions import MissingRequiredProperty
from ical_library.help_modules.lru_cache import instance_lru_cache
from ical_library.help_modules.timespan import Timespan, TimespanWithParent
from ical_library.ical_properties.dt import _DTBoth, DTStamp, DTStart, RecurrenceID
from ical_library.ical_properties.pass_properties import Comment, Summary, UID
from ical_library.ical_properties.periods import EXDate, RDate
from ical_library.ical_properties.rrule import RRule


class AbstractComponentWithRecurringProperties(Component, ABC):
    """
    This class helps avoid code repetition with different :class:`Component` classes that have a duration and have
    recurring properties.

    This class is inherited by VEvent, VToDo and VJournal as these all have recurring properties like :class:`RRule`,
    :class:`RDate` and :class:`EXDate`. All properties they had in common are part of this class.
    Note: VJournal is the odd one out as these events don't have a duration.

    :param name: The actual name of this component instance. E.g. VEVENT, RRULE, VCUSTOMCOMPONENT.
    :param dtstamp: The DTStamp property. Required and must occur exactly once.
    :param uid: The UID property. Required and must occur exactly once.
    :param dtstart: The DTStart property. Optional and may occur at most once.
    :param rrule: The RRule property. Optional and may occur at most once.
    :param summary: The Summary property. Optional and may occur at most once.
    :param exdate: The EXDate property. Optional, but may occur multiple times.
    :param rdate: The RDate property. Optional, but may occur multiple times.
    :param comment: The Comment property. Optional, but may occur multiple times.
    :param parent: The Component this item is encapsulated by in the iCalendar data file.
    """

    def __init__(
        self,
        name: str,
        dtstamp: Optional[DTStamp] = None,
        uid: Optional[UID] = None,
        dtstart: Optional[DTStart] = None,
        rrule: Optional[RRule] = None,
        summary: Optional[Summary] = None,
        recurrence_id: Optional[RecurrenceID] = None,
        exdate: Optional[List[EXDate]] = None,
        rdate: Optional[List[RDate]] = None,
        comment: Optional[List[Comment]] = None,
        parent: Optional[Component] = None,
    ):
        super().__init__(name, parent=parent)

        # Required
        self._dtstamp: Optional[DTStamp] = self.as_parent(dtstamp)
        self._uid: Optional[UID] = self.as_parent(uid)

        # Optional, may only occur once
        self.dtstart: Optional[DTStart] = self.as_parent(dtstart)
        self.rrule: Optional[RRule] = self.as_parent(rrule)
        self.summary: Optional[Summary] = self.as_parent(summary)
        self.recurrence_id: Optional[RecurrenceID] = self.as_parent(recurrence_id)

        # Optional, may occur more than once
        self.exdate: Optional[List[EXDate]] = self.as_parent(exdate)
        self.rdate: Optional[List[RDate]] = self.as_parent(rdate)
        self.comment: Optional[List[Comment]] = self.as_parent(comment)

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

    @abstractmethod
    def expand_component_in_range(
        self, return_range: Timespan, starts_to_exclude: Union[List[Date], List[DateTime]]
    ) -> Iterator[TimespanWithParent]:
        """
        Expand this component in range according to its recurring *RDate*, *EXDate* and *RRule* properties.
        :param return_range: The timespan range on which we should return VToDo instances.
        :param starts_to_exclude: List of start Dates or list of start DateTimes of which we already know we should
        exclude them from our recurrence computation (as they have been completely redefined in another element).
        :return: Yield all recurring VToDo instances related to this VToDo in the given *return_range*.
        """
        pass

    def __eq__(
        self: "AbstractComponentWithRecurringProperties", other: "AbstractComponentWithRecurringProperties"
    ) -> bool:
        """Return whether the current instance and the other instance are the same."""
        if type(self) != type(other):
            return False
        return (
            self.dtstart == other.dtstart
            and self.ending == other.ending
            and self.summary == other.summary
            and self.comment == other.comment
        )

    @property
    def timespan(self) -> Optional[TimespanWithParent]:
        """
        Return a timespan as a property representing the start and end of the instance.
        :return: A timespan instance with this class instance as parent.
        """
        if self.start is None:
            return None
        if self.end is None:
            TimespanWithParent(parent=self, begin=self.start, end=self.start)
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
    def computed_duration(self: "AbstractComponentWithRecurringProperties") -> Optional[Duration]:
        """Return the duration of this Component as a :class:`Date` or :class:`DateTime` value."""
        if a_duration := self.get_duration():
            return a_duration
        elif self.end and self.start:
            result: Period = self.end - self.start
            return result
        return None

    @property
    @instance_lru_cache()
    def max_recurring_timespan(self) -> Optional[Timespan]:
        if not self.start or not self.computed_duration:
            return None
        if not self.rrule and not self.rdate:
            return self.timespan
        max_dt: DateTime = DateTime.min
        if self.rdate:
            max_dt = max(max_dt, max([rdate.compute_max_end_date(self.computed_duration) for rdate in self.rdate]))
        if self.rrule:
            max_dt = max(max_dt, self.rrule.compute_max_end_date(self.start, self.computed_duration))
        if max_dt != DateTime.min:
            return Timespan(self.start, max_dt)
        return None


class AbstractRecurrence(AbstractComponentWithRecurringProperties, ABC):
    """
    This class extends :class:`AbstractComponentWithRecurringProperties` to represent a recurring Component.

    This class is inherited by VRecurringEvent, VRecurringToDo and VRecurringJournal. When we compute the recurrence
    based on the :class:`RRule`, :class:`RDate` and :class:`EXDate` properties, we create new occurrences of that
    specific component. Instead of copying over all Properties (and using a lot of memory), this class overwrites the
    *__getattribute__* function to act like the original component for most attributes except for *start*, *end*,
    *original* and *parent*.
    """

    def __getattribute__(self, var_name: str) -> Any:
        """
        Overwrite this function to return the originals properties except for *start*, *end*, *original* and *parent*.

        Depending on the attributes *name* we are requesting, we either return its own properties or the original
        components properties. This way we don't need to copy over all the variables.
        :param var_name: Name of the attribute we are accessing.
        :return: The value of the attribute we are accessing either from the *original* or from this instance itself.
        """
        if var_name in ("_start", "_end", "_original", "_parent", "start", "end", "original", "parent"):
            return object.__getattribute__(self, var_name)
        if var_name in ("_name", "_extra_child_components", "_extra_properties"):
            return object.__getattribute__(self._original, var_name)
        if var_name in self._original.get_property_ical_names():
            return object.__getattribute__(self._original, var_name)
        return object.__getattribute__(self, var_name)

    def __setattr__(self, key: str, value: Any) -> None:
        """Overwrite the custom __setattr__ from Components to set it back to the standard behavior."""
        object.__setattr__(self, key, value)

    @property
    def start(self) -> DateTime:
        """Return the start of this recurring event."""
        return self._start

    @property
    def end(self) -> DateTime:
        """Return the end of this recurring event."""
        return self._end

    @property
    def original(self) -> AbstractComponentWithRecurringProperties:
        """Return the original component that created this recurring component."""
        return self._original

    @property
    def parent(self) -> Component:
        """Return the parent of the original component."""
        return self._original.parent
