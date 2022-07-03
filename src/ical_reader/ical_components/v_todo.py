from dataclasses import dataclass
from typing import Iterator, List, Optional

from pendulum import DateTime, Duration

from ical_reader.help_classes.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractRecurringComponent, AbstractStartStopComponent
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import _DTBoth, Completed, Created, Due, LastModified, RecurrenceID
from ical_reader.ical_properties.geo import GEO
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import Priority, Sequence
from ical_reader.ical_properties.pass_properties import (
    Attach,
    Categories,
    Class,
    Contact,
    Description,
    Location,
    RelatedTo,
    RequestStatus,
    Resources,
    Status,
    URL,
)
from ical_reader.ical_properties.percentcomplete import PercentComplete
from ical_reader.ical_utils import property_utils


@dataclass(repr=False)
class VToDo(AbstractStartStopComponent):
    """
    This class represents the VTODO component specified in RFC 5545 in '3.6.2. To-Do Component'.

    Note: Not all properties are listed here as some of them are inherited by :class:`AbstractStartStopComponent`.
    """

    # Optional, may only occur once
    ical_class: Optional[Class] = None  # As class is a reserved keyword in python, we prefixed it with `ical_`.
    completed: Optional[Completed] = None
    created: Optional[Created] = None
    description: Optional[Description] = None
    duration: Optional[ICALDuration] = None
    geo: Optional[GEO] = None
    last_modified: Optional[LastModified] = None
    location: Optional[Location] = None
    organizer: Optional[Organizer] = None
    percent: Optional[PercentComplete] = None
    priority: Optional[Priority] = None
    sequence: Optional[Sequence] = None
    status: Optional[Status] = None
    url: Optional[URL] = None
    recurrence_id: Optional[RecurrenceID] = None
    due: Optional[Due] = None

    # Optional, may occur more than once
    attach: Optional[List[Attach]] = None
    attendee: Optional[List[Attendee]] = None
    categories: Optional[List[Categories]] = None
    contact: Optional[List[Contact]] = None
    rstatus: Optional[List[RequestStatus]] = None
    related: Optional[List[RelatedTo]] = None
    resources: Optional[List[Resources]] = None

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"VAlarm({self.start} - {self.end}: {self.summary.value})"

    @property
    def ending(self) -> Optional[_DTBoth]:
        """
        Return the ending of the vtodo.

        Note: This is an abstract method from :class:`AbstractStartStopComponent` that we have to implement.
        """
        return self.due

    def get_duration(self) -> Optional[Duration]:
        """
        Return the duration of the vtodo.

        Note: This is an abstract method from :class:`AbstractStartStopComponent` that we have to implement.
        """
        return self.duration.duration if self.duration else None

    def expand_component_in_range(self: "VToDo", return_range: Timespan) -> Iterator["VToDo"]:
        """
        Expand this VToDo in range according to its recurring *RDate*, *EXDate* and *RRule* properties.
        :param return_range: The timespan range on which we should return VToDo instances.
        :return: Yield all recurring VToDo instances related to this VToDo in the given *return_range*.
        """
        yield self
        iterator = property_utils.expand_component_in_range(
            exdate_list=self.exdate or [],
            rdate_list=self.rdate or [],
            rrule=self.rrule,
            first_event_start=self.start,
            first_event_duration=self.computed_duration,
            return_range=return_range,
            make_tz_aware=None,
        )

        for event_start_time, event_end_time in iterator:
            yield VRecurringToDo(
                original_component_instance=self,
                start=event_start_time,
                end=event_end_time,
            )


@dataclass(repr=False)
class VRecurringToDo(AbstractRecurringComponent, VToDo):
    """
    This class represents VToDo that are recurring.
    Inside the AbstractRecurringComponent class we overwrite specific dunder methods and property methods. This way
     our end users have a very similar interface to an actual VToDo but without us needing to code the exact same
     thing twice.
    """

    def __init__(self, original_component_instance: VToDo, start: DateTime, end: DateTime):
        super(VToDo, self).__init__()
        self._parent = original_component_instance
        self._original = original_component_instance
        self._start = start
        self._end = end

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"RVToDo({self._start} - {self._end}: {self.original.summary.value})"
