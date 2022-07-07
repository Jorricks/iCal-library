from typing import Iterator, List, Optional

from pendulum import DateTime, Duration

from ical_reader.base_classes.component import Component
from ical_reader.help_modules import property_utils
from ical_reader.help_modules.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractRecurringComponent, AbstractStartStopComponent
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import _DTBoth, Created, DTStamp, DTStart, LastModified, RecurrenceID
from ical_reader.ical_properties.ints import Sequence
from ical_reader.ical_properties.pass_properties import (
    Attach,
    Categories,
    Class,
    Comment,
    Contact,
    Description,
    RelatedTo,
    RequestStatus,
    Status,
    Summary,
    UID,
    URL,
)
from ical_reader.ical_properties.periods import EXDate, RDate
from ical_reader.ical_properties.rrule import RRule


class VJournal(AbstractStartStopComponent):
    """
    This class represents the VJOURNAL component specified in RFC 5545 in '3.6.3. Journal Component'.

    A "VJOURNAL" calendar component is a grouping of component properties that represent one or more descriptive text
    notes associated with a particular calendar date. The "DTSTART" property is used to specify the calendar date with
    which the journal entry is associated. Generally, it will have a DATE value data type, but it can also be used to
    specify a DATE-TIME value data type. Examples of a journal entry include a daily record of a legislative body or
    a journal entry of individual telephone contacts for the day or an ordered list of accomplishments for the day.
    The "VJOURNAL" calendar component can also be used to associate a document with a calendar date.

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
    :param last_modified: Optional LastModified property. Optional, but may occur at most once.
    :param organizer: The Organizer property. Optional, but may occur at most once.
    :param sequence: The Sequence property. Optional, but may occur at most once.
    :param status: The Status property. Optional, but may occur at most once.
    :param url: The URL property. Optional, but may occur at most once.
    :param recurrence_id: Optional RecurrenceID property. Optional, but may occur at most once.
    :param attach: The Attach property. Optional, but may occur multiple times.
    :param attendee: The Attendee property. Optional, but may occur multiple times.
    :param categories: The Categories property. Optional, but may occur multiple times.
    :param contact: The Contact property. Optional, but may occur multiple times.
    :param description: The Description property. Optional, but may occur multiple times.
    :param related: The RelatedTo property. Optional, but may occur multiple times.
    :param rstatus: The RequestStatus property. Optional, but may occur multiple times.
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
        last_modified: Optional[LastModified] = None,
        organizer: Optional[Organizer] = None,
        sequence: Optional[Sequence] = None,
        status: Optional[Status] = None,
        url: Optional[URL] = None,
        recurrence_id: Optional[RecurrenceID] = None,
        attach: Optional[List[Attach]] = None,
        attendee: Optional[List[Attendee]] = None,
        categories: Optional[List[Categories]] = None,
        contact: Optional[List[Contact]] = None,
        description: Optional[List[Description]] = None,
        related: Optional[List[RelatedTo]] = None,
        rstatus: Optional[List[RequestStatus]] = None,
    ):
        super().__init__(
            name="VJOURNAL",
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
        self.last_modified: Optional[LastModified] = last_modified
        self.organizer: Optional[Organizer] = organizer
        self.sequence: Optional[Sequence] = sequence
        self.status: Optional[Status] = status
        self.url: Optional[URL] = url
        self.recurrence_id: Optional[RecurrenceID] = recurrence_id

        # Optional, may occur more than once
        self.attach: Optional[List[Attach]] = attach
        self.attendee: Optional[List[Attendee]] = attendee
        self.categories: Optional[List[Categories]] = categories
        self.contact: Optional[List[Contact]] = contact
        self.description: Optional[List[Description]] = description
        self.related: Optional[List[RelatedTo]] = related
        self.rstatus: Optional[List[RequestStatus]] = rstatus

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"VJournal({self.start}: {self.summary.value})"

    @property
    def ending(self) -> Optional[_DTBoth]:
        """
        Return the start time of the journal. This is because the Journal does not have a duration.

        Note: This is an abstract method from :class:`AbstractStartStopComponent` that we have to implement.
        """
        return self.dtstart

    def get_duration(self) -> Optional[Duration]:
        """
        Return an empty Duration as a Journal does not have a duration.

        Note: This is an abstract method from :class:`AbstractStartStopComponent` that we have to implement.
        """
        return Duration()

    def expand_component_in_range(self: "VJournal", return_range: Timespan) -> Iterator["VJournal"]:
        """
        Expand this VJournal in range according to its recurring *RDate*, *EXDate* and *RRule* properties.
        :param return_range: The timespan range on which we should return VJournal instances.
        :return: Yield all recurring VJournal instances related to this VJournal in the given *return_range*.
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
            yield VRecurringJournal(original_component_instance=self, start=event_start_time)


class VRecurringJournal(AbstractRecurringComponent, VJournal):
    """
    This class represents VJournal that are recurring.
    Inside the AbstractRecurringComponent class we overwrite specific dunder methods and property methods. This way
    our end users have a very similar interface to an actual VJournal but without us needing to code the exact same
    thing twice.

    :param original_component_instance: The original VJournal instance.
    :param start: The start of this occurrence.
    :param end: The end of this occurrence.
    """

    def __init__(self, original_component_instance: VJournal, start: DateTime):
        super(VJournal, self).__init__("VJOURNAL", original_component_instance)
        self._original = original_component_instance
        self._start = start
        self._end = start

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"RVJournal({self._start}: {self.original.summary.value})"
