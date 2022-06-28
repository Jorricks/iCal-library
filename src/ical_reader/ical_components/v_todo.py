from dataclasses import dataclass
from typing import Optional, List, Iterator

from pendulum import DateTime, Duration

from ical_reader.help_classes.timespan import Timespan
from ical_reader.ical_components.abstract_components import AbstractStartStopComponent, AbstractRecurringComponent
from ical_reader.ical_properties.cal_address import Organizer, Attendee
from ical_reader.ical_properties.dt import Created, LastModified, RecurrenceID, Due, Completed, _DTBoth
from ical_reader.ical_properties.geo import GEO
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import Priority, Sequence
from ical_reader.ical_properties.pass_properties import Class, Description, Location, Status, URL, Attach, Categories, \
    Contact, RStatus, Related, Resources
from ical_reader.ical_properties.percent import Percent
from ical_reader.ical_utils import property_utils


@dataclass(repr=False)
class VToDo(AbstractStartStopComponent):
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
    percent: Optional[Percent] = None
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
    rstatus: Optional[List[RStatus]] = None
    related: Optional[List[Related]] = None
    resources: Optional[List[Resources]] = None

    def __repr__(self) -> str:
        return f"VAlarm({self.start} - {self.end}: {self.summary.value})"

    @property
    def ending(self) -> _DTBoth:
        return self.due

    def get_duration(self) -> Optional[Duration]:
        return self.duration.duration if self.duration else None

    def expand_component_in_range(self: "VToDo", return_range: Timespan) -> Iterator["VToDo"]:
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
class VRecurringToDo(AbstractRecurringComponent[VToDo], VToDo):
    def __init__(self, original_component_instance: VToDo, start: DateTime, end: DateTime):
        super(VToDo, self).__init__()
        self._parent = original_component_instance
        self._original = original_component_instance
        self._start = start
        self._end = end

    def __repr__(self) -> str:
        return f"RVToDo({self._start} - {self._end}: {self.original.summary.value})"
