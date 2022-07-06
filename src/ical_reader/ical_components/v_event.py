from typing import Iterator, List, Optional

from pendulum import DateTime, Duration

from ical_reader.base_classes.component import Component
from ical_reader.help_modules import property_utils
from ical_reader.help_modules.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractRecurringComponent, AbstractStartStopComponent
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import _DTBoth, Created, DTEnd, DTStamp, DTStart, LastModified, RecurrenceID
from ical_reader.ical_properties.geo import GEO
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import Priority, Sequence
from ical_reader.ical_properties.pass_properties import (
    Attach,
    Categories,
    Class,
    Comment,
    Contact,
    Description,
    Location,
    RelatedTo,
    RequestStatus,
    Resources,
    Status,
    Summary,
    TimeTransparency,
    UID,
    URL,
)
from ical_reader.ical_properties.periods import EXDate, RDate
from ical_reader.ical_properties.rrule import RRule


class VEvent(AbstractStartStopComponent):
    """
    This class represents the VEVENT component specified in RFC 5545 in '3.6.1. Event Component'.

    A "VEVENT" calendar component is a grouping of component properties, possibly including "VALARM" calendar
    components, that represents a scheduled amount of time on a calendar. For example, it can be an activity; such as
    a one-hour long, department meeting from 8:00 AM to 9:00 AM, tomorrow. Generally, an event will take up time on an
    individual calendar. Hence, the event will appear as an opaque interval in a search for busy time. Alternately,
    the event can have its Time Transparency set to "TRANSPARENT" in order to prevent blocking of the event in
    searches for busy time.

    :param name:
    :param parent:
    :param dtstamp:
    :param uid:
    :param dtstart:
    :param rrule:
    :param summary:
    :param exdate:
    :param rdate:
    :param comment:
    :param ical_class:
    :param created:
    :param description:
    :param duration:
    :param geo:
    :param last_modified:
    :param location:
    :param organizer:
    :param priority:
    :param sequence:
    :param status:
    :param transp:
    :param url:
    :param recurrence_id:
    :param dtend:
    :param attach:
    :param attendee:
    :param categories:
    :param contact:
    :param rstatus:
    :param related:
    :param resources:
    """

    def __init__(
        self,
        parent: Optional[Component],
        dtstamp: Optional[DTStamp] = None,
        uid: Optional[UID] = None,
        dtstart: Optional[DTStart] = None,
        rrule: Optional[RRule] = None,
        summary: Optional[Summary] = None,
        exdate: Optional[List[EXDate]] = None,
        rdate: Optional[List[RDate]] = None,
        comment: Optional[List[Comment]] = None,
        ical_class: Optional[Class] = None,
        created: Optional[Created] = None,
        description: Optional[Description] = None,
        duration: Optional[ICALDuration] = None,
        geo: Optional[GEO] = None,
        last_modified: Optional[LastModified] = None,
        location: Optional[Location] = None,
        organizer: Optional[Organizer] = None,
        priority: Optional[Priority] = None,
        sequence: Optional[Sequence] = None,
        status: Optional[Status] = None,
        transp: Optional[TimeTransparency] = None,
        url: Optional[URL] = None,
        recurrence_id: Optional[RecurrenceID] = None,
        dtend: Optional[DTEnd] = None,
        attach: Optional[List[Attach]] = None,
        attendee: Optional[List[Attendee]] = None,
        categories: Optional[List[Categories]] = None,
        contact: Optional[List[Contact]] = None,
        rstatus: Optional[List[RequestStatus]] = None,
        related: Optional[List[RelatedTo]] = None,
        resources: Optional[List[Resources]] = None,
    ):
        super().__init__(
            name="VEVENT",
            parent=parent,
            dtstamp=dtstamp,
            uid=uid,
            dtstart=dtstart,
            rrule=rrule,
            summary=summary,
            exdate=exdate,
            rdate=rdate,
            comment=comment,
        )

        # Optional, may only occur once
        # As class is a reserved keyword in python, we prefixed it with `ical_`.
        self.ical_class: Optional[Class] = ical_class
        self.created: Optional[Created] = created
        self.description: Optional[Description] = description
        self.duration: Optional[ICALDuration] = duration
        self.geo: Optional[GEO] = geo
        self.last_modified: Optional[LastModified] = last_modified
        self.location: Optional[Location] = location
        self.organizer: Optional[Organizer] = organizer
        self.priority: Optional[Priority] = priority
        self.sequence: Optional[Sequence] = sequence
        self.status: Optional[Status] = status
        self.transp: Optional[TimeTransparency] = transp
        self.url: Optional[URL] = url
        self.recurrence_id: Optional[RecurrenceID] = recurrence_id
        self.dtend: Optional[DTEnd] = dtend

        # Optional, may occur more than once
        self.attach: Optional[List[Attach]] = attach
        self.attendee: Optional[List[Attendee]] = attendee
        self.categories: Optional[List[Categories]] = categories
        self.contact: Optional[List[Contact]] = contact
        self.rstatus: Optional[List[RequestStatus]] = rstatus
        self.related: Optional[List[RelatedTo]] = related
        self.resources: Optional[List[Resources]] = resources

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        if self.dtstart and self.dtend:
            return f"VEvent({self.start} - {self.end}: {self.summary.value if self.summary else ''})"
        else:
            return "VEvent()"

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


class VRecurringEvent(AbstractRecurringComponent, VEvent):
    """
    This class represents VEvents that are recurring.
    Inside the AbstractRecurringComponent class we overwrite specific dunder methods and property methods. This way
    our end users have a very similar interface to an actual VEvent but without us needing to code the exact same
    thing twice.

    :param original_component_instance: The original VEvent instance.
    :param start: The start of this occurrence.
    :param end: The end of this occurrence.
    """

    def __init__(self, original_component_instance: VEvent, start: DateTime, end: DateTime):
        super(VEvent, self).__init__("VEVENT", original_component_instance)
        self._original = original_component_instance
        self._start = start
        self._end = end

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"RVEvent({self._start} - {self._end}: {self.original.summary.value if self.original.summary else ''})"
