from typing import Iterator, List, Optional, Union

from pendulum import Date, DateTime, Duration

from ical_library.base_classes.component import Component
from ical_library.help_modules import property_utils
from ical_library.help_modules.timespan import Timespan, TimespanWithParent
from ical_library.ical_components.abstract_components import (
    AbstractComponentWithRecurringProperties,
    AbstractRecurrence,
)
from ical_library.ical_components.v_alarm import VAlarm
from ical_library.ical_properties.cal_address import Attendee, Organizer
from ical_library.ical_properties.dt import _DTBoth, Created, DTEnd, DTStamp, DTStart, LastModified, RecurrenceID
from ical_library.ical_properties.geo import GEO
from ical_library.ical_properties.ical_duration import ICALDuration
from ical_library.ical_properties.ints import Priority, Sequence
from ical_library.ical_properties.pass_properties import (
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
from ical_library.ical_properties.periods import EXDate, RDate
from ical_library.ical_properties.rrule import RRule


class VEvent(AbstractComponentWithRecurringProperties):
    """
    This class represents the VEVENT component specified in RFC 5545 in '3.6.1. Event Component'.

    A "VEVENT" calendar component is a grouping of component properties, possibly including "VALARM" calendar
    components, that represents a scheduled amount of time on a calendar. For example, it can be an activity; such as
    a one-hour long, department meeting from 8:00 AM to 9:00 AM, tomorrow. Generally, an event will take up time on an
    individual calendar. Hence, the event will appear as an opaque interval in a search for busy time. Alternately,
    the event can have its Time Transparency set to "TRANSPARENT" in order to prevent blocking of the event in
    searches for busy time.

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
    :param ical_class: Optional Class property. Optional, but may occur at most once.
    :param created: The Created property. Optional, but may occur at most once.
    :param description: The Description property. Optional, but may occur at most once.
    :param duration: The ICALDuration property. Optional, but may occur at most once.
    :param geo: The GEO property. Optional, but may occur at most once.
    :param last_modified: Optional LastModified property. Optional, but may occur at most once.
    :param location: The Location property. Optional, but may occur at most once.
    :param organizer: The Organizer property. Optional, but may occur at most once.
    :param priority: The Priority property. Optional, but may occur at most once.
    :param sequence: The Sequence property. Optional, but may occur at most once.
    :param status: The Status property. Optional, but may occur at most once.
    :param transp: The TimeTransparency property. Optional, but may occur at most once.
    :param url: The URL property. Optional, but may occur at most once.
    :param recurrence_id: Optional RecurrenceID property. Optional, but may occur at most once.
    :param dtend: The DTEnd property. Optional, but may occur at most once.
    :param attach: The Attach property. Optional, but may occur multiple times.
    :param attendee: The Attendee property. Optional, but may occur multiple times.
    :param categories: The Categories property. Optional, but may occur multiple times.
    :param contact: The Contact property. Optional, but may occur multiple times.
    :param rstatus: The RequestStatus property. Optional, but may occur multiple times.
    :param related: The RelatedTo property. Optional, but may occur multiple times.
    :param resources: The Resources property. Optional, but may occur multiple times.
    """

    def __init__(
        self,
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
        alarms: Optional[List[VAlarm]] = None,
        parent: Optional[Component] = None,
    ):
        super().__init__(
            name="VEVENT",
            dtstamp=dtstamp,
            uid=uid,
            dtstart=dtstart,
            rrule=rrule,
            summary=summary,
            recurrence_id=recurrence_id,
            exdate=exdate,
            rdate=rdate,
            comment=comment,
            parent=parent,
        )

        # Optional, may only occur once
        # As class is a reserved keyword in python, we prefixed it with `ical_`.
        self.ical_class: Optional[Class] = self.as_parent(ical_class)
        self.created: Optional[Created] = self.as_parent(created)
        self.description: Optional[Description] = self.as_parent(description)
        self.duration: Optional[ICALDuration] = self.as_parent(duration)
        self.geo: Optional[GEO] = self.as_parent(geo)
        self.last_modified: Optional[LastModified] = self.as_parent(last_modified)
        self.location: Optional[Location] = self.as_parent(location)
        self.organizer: Optional[Organizer] = self.as_parent(organizer)
        self.priority: Optional[Priority] = self.as_parent(priority)
        self.sequence: Optional[Sequence] = self.as_parent(sequence)
        self.status: Optional[Status] = self.as_parent(status)
        self.transp: Optional[TimeTransparency] = self.as_parent(transp)
        self.url: Optional[URL] = self.as_parent(url)
        self.dtend: Optional[DTEnd] = self.as_parent(dtend)

        # Optional, may occur more than once
        self.attach: Optional[List[Attach]] = self.as_parent(attach)
        self.attendee: Optional[List[Attendee]] = self.as_parent(attendee)
        self.categories: Optional[List[Categories]] = self.as_parent(categories)
        self.contact: Optional[List[Contact]] = self.as_parent(contact)
        self.rstatus: Optional[List[RequestStatus]] = self.as_parent(rstatus)
        self.related: Optional[List[RelatedTo]] = self.as_parent(related)
        self.resources: Optional[List[Resources]] = self.as_parent(resources)

        # This is a child component
        self.alarms: List[VAlarm] = alarms or []

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        if self.dtstart and self.dtend:
            return f"VEvent({self.start} - {self.end}: {self.summary.value if self.summary else ''})"
        else:
            return f"VEvent({self.summary.value if self.summary else ''})"

    @property
    def ending(self) -> Optional[_DTBoth]:
        """
        Return the ending of the event.

        Note: This is an abstract method from :class:`AbstractComponentWithRecurringProperties` we have to implement.
        """
        return self.dtend

    def get_duration(self) -> Optional[Duration]:
        """
        Return the duration of the event.

        Note: This is an abstract method from :class:`AbstractComponentWithRecurringProperties` we have to implement.
        """
        return self.duration.duration if self.duration else None

    def expand_component_in_range(
        self, return_range: Timespan, starts_to_exclude: Union[List[Date], List[DateTime]]
    ) -> Iterator[TimespanWithParent]:
        """
        Expand this VEvent in range according to its recurring *RDate*, *EXDate* and *RRule* properties.
        :param return_range: The timespan range on which we should return VEvent instances.
        :param starts_to_exclude: List of start Dates or list of start DateTimes of which we already know we should
        exclude them from our recurrence computation (as they have been completely redefined in another element).
        :return: Yield all recurring VEvent instances related to this VEvent in the given *return_range*.
        """
        yield self.timespan
        starts_to_exclude.append(self.start)

        start = self.start
        duration = self.computed_duration
        if not start or not duration:
            return None

        iterator = property_utils.expand_component_in_range(
            exdate_list=self.exdate or [],
            rdate_list=self.rdate or [],
            rrule=self.rrule,
            first_event_start=start,
            first_event_duration=duration,
            starts_to_exclude=starts_to_exclude,
            return_range=return_range,
            make_tz_aware=None,
        )

        for event_start_time, event_end_time in iterator:
            yield VRecurringEvent(
                original_component_instance=self,
                start=event_start_time,
                end=event_end_time,
            ).timespan


class VRecurringEvent(AbstractRecurrence, VEvent):
    """
    This class represents VEvents that are recurring.
    Inside the AbstractRecurrence class we overwrite specific dunder methods and property methods.
    This way our end users have a very similar interface to an actual VEvent but without us needing to code the exact
    same thing twice.

    :param original_component_instance: The original VEvent instance.
    :param start: The start of this occurrence.
    :param end: The end of this occurrence.
    """

    def __init__(self, original_component_instance: VEvent, start: DateTime, end: DateTime):
        self._original = original_component_instance
        self._start = start
        self._end = end
        super(VEvent, self).__init__("VEVENT", parent=original_component_instance)

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"RVEvent({self._start} - {self._end}: {self.original.summary.value if self.original.summary else ''})"
