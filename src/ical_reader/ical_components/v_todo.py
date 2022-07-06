from typing import Iterator, List, Optional

from pendulum import DateTime, Duration

from ical_reader.base_classes.component import Component
from ical_reader.help_modules import property_utils
from ical_reader.help_modules.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractRecurringComponent, AbstractStartStopComponent
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import (
    _DTBoth,
    Completed,
    Created,
    DTStamp,
    DTStart,
    Due,
    LastModified,
    RecurrenceID,
)
from ical_reader.ical_properties.geo import GEO
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import PercentComplete, Priority, Sequence
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
    UID,
    URL,
)
from ical_reader.ical_properties.periods import EXDate, RDate
from ical_reader.ical_properties.rrule import RRule


class VToDo(AbstractStartStopComponent):
    """
    This class represents the VTODO component specified in RFC 5545 in '3.6.2. To-Do Component'.

    A "VTODO" calendar component is a grouping of component properties and possibly "VALARM" calendar components that
    represent an action-item or assignment. For example, it can be used to represent an item of work assigned to an
    individual; such as "turn in travel expense today".

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
    :param completed:
    :param created:
    :param description:
    :param duration:
    :param geo:
    :param last_modified:
    :param location:
    :param organizer:
    :param percent:
    :param priority:
    :param sequence:
    :param status:
    :param url:
    :param recurrence_id:
    :param due:
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
        completed: Optional[Completed] = None,
        created: Optional[Created] = None,
        description: Optional[Description] = None,
        duration: Optional[ICALDuration] = None,
        geo: Optional[GEO] = None,
        last_modified: Optional[LastModified] = None,
        location: Optional[Location] = None,
        organizer: Optional[Organizer] = None,
        percent: Optional[PercentComplete] = None,
        priority: Optional[Priority] = None,
        sequence: Optional[Sequence] = None,
        status: Optional[Status] = None,
        url: Optional[URL] = None,
        recurrence_id: Optional[RecurrenceID] = None,
        due: Optional[Due] = None,
        attach: Optional[List[Attach]] = None,
        attendee: Optional[List[Attendee]] = None,
        categories: Optional[List[Categories]] = None,
        contact: Optional[List[Contact]] = None,
        rstatus: Optional[List[RequestStatus]] = None,
        related: Optional[List[RelatedTo]] = None,
        resources: Optional[List[Resources]] = None,
    ):
        super().__init__(
            name="VTODO",
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
        self.completed: Optional[Completed] = completed
        self.created: Optional[Created] = created
        self.description: Optional[Description] = description
        self.duration: Optional[ICALDuration] = duration
        self.geo: Optional[GEO] = geo
        self.last_modified: Optional[LastModified] = last_modified
        self.location: Optional[Location] = location
        self.organizer: Optional[Organizer] = organizer
        self.percent: Optional[PercentComplete] = percent
        self.priority: Optional[Priority] = priority
        self.sequence: Optional[Sequence] = sequence
        self.status: Optional[Status] = status
        self.url: Optional[URL] = url
        self.recurrence_id: Optional[RecurrenceID] = recurrence_id
        self.due: Optional[Due] = due

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


class VRecurringToDo(AbstractRecurringComponent, VToDo):
    """
    This class represents VToDo that are recurring.
    Inside the AbstractRecurringComponent class we overwrite specific dunder methods and property methods. This way
    our end users have a very similar interface to an actual VToDo but without us needing to code the exact same
    thing twice.

    :param original_component_instance: The original VToDo instance.
    :param start: The start of this occurrence.
    :param end: The end of this occurrence.
    """

    def __init__(self, original_component_instance: VToDo, start: DateTime, end: DateTime):
        super(VToDo, self).__init__("VTODO", original_component_instance)
        self._original = original_component_instance
        self._start = start
        self._end = end

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"RVToDo({self._start} - {self._end}: {self.original.summary.value})"
