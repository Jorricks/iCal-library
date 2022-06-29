from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pendulum import DateTime

from ical_reader.base_classes.calendar_component import CalendarComponent
from ical_reader.ical_components.v_event import VEvent
from ical_reader.ical_components.v_free_busy import VFreeBusy
from ical_reader.ical_components.v_journal import VJournal
from ical_reader.ical_components.v_timezone import VTimeZone
from ical_reader.ical_components.v_todo import VToDo
from ical_reader.ical_properties.pass_properties import CalScale, Method, ProdID, Version
from ical_reader.timeline import Timeline


@dataclass
class VCalendar(CalendarComponent):
    """This class represents the VCALENDER component specified in RFC 5545 in '3.6. Calendar Components'."""

    # Required properties, only one occurrence allowed.
    prodid: Optional[ProdID] = None
    version: Optional[Version] = None

    # Optional properties, must not occur more than once.
    calscale: Optional[CalScale] = None
    method: Optional[Method] = None

    # These are Components as well
    events: List[VEvent] = field(default_factory=list)
    todos: List[VToDo] = field(default_factory=list)
    journals: List[VJournal] = field(default_factory=list)
    free_busy_list: List[VFreeBusy] = field(default_factory=list)
    time_zones: List[VTimeZone] = field(default_factory=list)
    _lines: Optional[List[str]] = None

    @property
    def children(self) -> Tuple["CalendarComponent", ...]:
        return (
            *self.events,
            *self.todos,
            *self.journals,
            *self.free_busy_list,
            *self.time_zones,
            *[child for list_of_children in self._extra_child_components.values() for child in list_of_children],
        )

    def add_child(self, child: "CalendarComponent") -> None:
        if isinstance(child, VEvent):
            self.events.append(child)
            child.set_parent(self)
        else:
            super().add_child(child)

    @property
    def calendar_scale(self) -> str:
        return self.calscale.value if self.calscale else "GREGORIAN"

    @property
    def timezones(self) -> List[VTimeZone]:
        return [instance for instance in self.children if isinstance(instance, VTimeZone)]

    def get_timezone(self, tzid: str) -> VTimeZone:
        for timezone in self.timezones:
            if timezone.tzid.value == tzid:
                return timezone
        raise ValueError(f"Could not find Timezone with {tzid=}.")

    def get_aware_dt_for_timezone(self, dt: DateTime, tzid: str) -> DateTime:
        return self.get_timezone(tzid).convert_naive_datetime_to_aware(dt)

    @property
    def current_timezone(self) -> str:
        raise NotImplementedError("Please implement this")

    @property
    def timeline(self) -> Timeline:
        return Timeline(self)

    def get_limited_timeline(self, start: Optional[DateTime], end: Optional[DateTime]) -> Timeline:
        return Timeline(self, start, end)

    def parse_component_section(self, lines: List[str], line_number: int) -> int:
        self._lines = lines
        return super().parse_component_section(lines=lines, line_number=line_number)

    def get_original_ical_text(self, start_line: int, end_line: int) -> str:
        lines = self._lines
        if lines is None:
            raise TypeError("We should first parse the component section before calling this function.")
        return "\n".join(line for line in self.tree_root._lines[max(0, start_line) : min(len(lines), end_line)])


if __name__ == "__main__":
    import pprint

    pprint.pprint(VCalendar._get_property_mapping_2())
    pprint.pprint(VCalendar._get_child_component_mapping())
