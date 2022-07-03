from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from pendulum import DateTime

from ical_reader.base_classes.component import Component
from ical_reader.ical_components.v_event import VEvent
from ical_reader.ical_components.v_free_busy import VFreeBusy
from ical_reader.ical_components.v_journal import VJournal
from ical_reader.ical_components.v_timezone import VTimeZone
from ical_reader.ical_components.v_todo import VToDo
from ical_reader.ical_properties.pass_properties import CalScale, Method, ProdID, Version
from ical_reader.timeline import Timeline


@dataclass
class VCalendar(Component):
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
    def children(self) -> Tuple["Component", ...]:
        # @ToDo(jorrick) check if this is required.
        return (
            *self.events,
            *self.todos,
            *self.journals,
            *self.free_busy_list,
            *self.time_zones,
            *[child for list_of_children in self._extra_child_components.values() for child in list_of_children],
        )

    @property
    def calendar_scale(self) -> str:
        """Return the calendar scale according to RFC 5545."""
        return self.calscale.value if self.calscale else "GREGORIAN"

    def get_timezone(self, tzid: str) -> VTimeZone:
        """Get the corresponding VTimeZone object based on the given timezone identifier."""
        for timezone in self.time_zones:
            if timezone.tzid.value == tzid:
                return timezone
        raise ValueError(f"Could not find Timezone with {tzid=}.")

    def get_aware_dt_for_timezone(self, dt: DateTime, tzid: str) -> DateTime:
        """Return the timezone aware DateTime object for a given TimeZone identifier."""
        return self.get_timezone(tzid).convert_naive_datetime_to_aware(dt)

    @property
    def timeline(self) -> Timeline:
        """Return a timeline of VEvents from 1970-00-00T00:00:00 to 2100-00-00T00:00:00."""
        return Timeline(self)

    def get_limited_timeline(self, start: Optional[DateTime], end: Optional[DateTime]) -> Timeline:
        """
        Return a timeline of VEvents limited by *start* and *end*

        :param start: Only include events in the timeline with a starting date later than this value.
        :param end: Only include events in the timeline with a starting date earlier than this value.
        """
        return Timeline(self, start, end)

    def parse_component(self, lines: List[str], line_number: int) -> int:
        """
        Parse a new component in the RAW string list.
        :param lines: A list of all the lines in the iCalendar file.
        :param line_number: The line number at which this component starts.
        :return: The line number at which this component ends.
        """
        self._lines = lines
        return super().parse_component(lines=lines, line_number=line_number)

    def get_original_ical_text(self, start_line: int, end_line: int) -> str:
        """
        Get the original iCAL text for your property from the RAW string list.
        :param start_line: The starting line index for the component you wish to show.
        :param end_line: The ending line index for the component you wish to show.
        :return: The complete string, as it was in the RAW string list, for the component you wish to show.
        """
        lines = self._lines
        if lines is None:
            raise TypeError("We should first parse the component section before calling this function.")
        return "\n".join(line for line in self.tree_root._lines[max(0, start_line) : min(len(lines), end_line)])


if __name__ == "__main__":
    import pprint

    pprint.pprint(VCalendar._get_property_mapping())
    pprint.pprint(VCalendar._get_child_component_mapping())
