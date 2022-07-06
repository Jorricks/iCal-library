from dataclasses import dataclass
from typing import Iterator, List, Optional

from pendulum import DateTime, Duration

from ical_reader.help_modules import property_utils
from ical_reader.help_modules.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractRecurringComponent, AbstractStartStopComponent
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import _DTBoth, Created, DTEnd, LastModified, RecurrenceID
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
    TimeTransparency,
    URL,
)
from ical_reader.ical_properties.rrule import RRule


@dataclass(repr=False)
class VEvent(AbstractStartStopComponent):
    """
    This class represents the VEVENT component specified in RFC 5545 in '3.6.1. Event Component'.

    Note: Not all properties are listed here as some of them are inherited by :class:`AbstractStartStopComponent`.
    """

    # Optional, may only occur once
    ical_class: Optional[Class] = None  # As class is a reserved keyword in python, we prefixed it with `ical_`.
    created: Optional[Created] = None
    description: Optional[Description] = None
    duration: Optional[ICALDuration] = None
    geo: Optional[GEO] = None
    last_modified: Optional[LastModified] = None
    location: Optional[Location] = None
    organizer: Optional[Organizer] = None
    priority: Optional[Priority] = None
    sequence: Optional[Sequence] = None
    status: Optional[Status] = None
    transp: Optional[TimeTransparency] = None
    url: Optional[URL] = None
    recurrence_id: Optional[RecurrenceID] = None
    rrule: Optional[RRule] = None
    dtend: Optional[DTEnd] = None

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
        return f"VEvent({self.start} - {self.end}: {self.summary.value if self.summary else ''})"

    @property
    def ending(self) -> Optional[_DTBoth]:
        """
        Return the ending of the event.

        Note: This is an abstract method from :class:`AbstractStartStopComponent` that we have to implement.
        """
        return self.dtend

    def get_duration(self) -> Optional[Duration]:
        """
        Return the duration of the event.

        Note: This is an abstract method from :class:`AbstractStartStopComponent` that we have to implement.
        """
        return self.duration.duration if self.duration else None

    def expand_component_in_range(self: "VEvent", return_range: Timespan) -> Iterator["VEvent"]:
        """
        Expand this VEvent in range according to its recurring *RDate*, *EXDate* and *RRule* properties.
        :param return_range: The timespan range on which we should return VEvent instances.
        :return: Yield all recurring VEvent instances related to this VEvent in the given *return_range*.
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
            yield VRecurringEvent(
                original_component_instance=self,
                start=event_start_time,
                end=event_end_time,
            )


@dataclass(repr=False)
class VRecurringEvent(AbstractRecurringComponent, VEvent):
    """
    This class represents VEvents that are recurring.
    Inside the AbstractRecurringComponent class we overwrite specific dunder methods and property methods. This way
    our end users have a very similar interface to an actual VEvent but without us needing to code the exact same
    thing twice.
    """

    def __init__(self, original_component_instance: VEvent, start: DateTime, end: DateTime):
        """
        Instantiate a VEvent for a datetime computed by the recurrence rule properties set the VEvent.
        :param original_component_instance: The original VEvent instance.
        :param start: The start of this occurrence.
        :param end: The end of this occurrence.
        """
        super(VEvent, self).__init__()
        self._parent = original_component_instance
        self._original = original_component_instance
        self._start = start
        self._end = end

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"RVEvent({self._start} - {self._end}: {self.original.summary.value if self.original.summary else ''})"
