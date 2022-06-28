from dataclasses import dataclass
from typing import Optional, List, Iterator

from pendulum import DateTime, Duration

from ical_reader.help_classes.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractStartStopComponent, AbstractRecurringComponent
from ical_reader.ical_properties.cal_address import Organizer, Attendee
from ical_reader.ical_properties.dt import Created, LastModified, RecurrenceID, _DTBoth
from ical_reader.ical_properties.ints import Sequence
from ical_reader.ical_properties.pass_properties import Class, Status, URL, Attach, Categories, Contact, Description, \
    Related, RStatus
from ical_reader.ical_utils import property_utils


@dataclass(repr=False)
class VJournal(AbstractStartStopComponent):
    # Optional, may only occur once
    ical_class: Optional[Class] = None  # As class is a reserved keyword in python, we prefixed it with `ical_`.
    created: Optional[Created] = None
    last_modified: Optional[LastModified] = None
    organizer: Optional[Organizer] = None
    sequence: Optional[Sequence] = None
    status: Optional[Status] = None
    url: Optional[URL] = None
    recurrence_id: Optional[RecurrenceID] = None

    # Optional, may occur more than once
    attach: Optional[List[Attach]] = None
    attendee: Optional[List[Attendee]] = None
    categories: Optional[List[Categories]] = None
    contact: Optional[List[Contact]] = None
    description: Optional[List[Description]] = None
    related: Optional[List[Related]] = None
    rstatus: Optional[List[RStatus]] = None

    def __repr__(self) -> str:
        return f"VJournal({self.start}: {self.summary.value})"

    @property
    def ending(self) -> _DTBoth:
        return self.dtstart

    def get_duration(self) -> Optional[Duration]:
        return Duration()

    def expand_component_in_range(self: "VJournal", return_range: Timespan) -> Iterator["VJournal"]:
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
            yield VRecurringJournal(
                original_component_instance=self,
                start=event_start_time,
                end=event_end_time,
            )


@dataclass(repr=False)
class VRecurringJournal(AbstractRecurringComponent[VJournal], VJournal):
    def __init__(self, original_component_instance: VJournal, start: DateTime, end: DateTime):
        super(VJournal, self).__init__()
        self._parent = original_component_instance
        self._original = original_component_instance
        self._start = start
        self._end = end

    def __repr__(self) -> str:
        return f"RVJournal({self._start}: {self.original.summary.value})"

