from typing import List, Optional, TYPE_CHECKING

from pendulum import DateTime

from ical_library.base_classes.component import Component
from ical_library.exceptions import MissingRequiredProperty
from ical_library.ical_components.v_event import VEvent
from ical_library.ical_components.v_free_busy import VFreeBusy
from ical_library.ical_components.v_journal import VJournal
from ical_library.ical_components.v_timezone import VTimeZone
from ical_library.ical_components.v_todo import VToDo
from ical_library.ical_properties.pass_properties import CalScale, Method, ProdID, Version

if TYPE_CHECKING:
    from ical_library.timeline import Timeline


class VCalendar(Component):
    """
    This class represents the VCALENDAR component specified in RFC 5545 in '3.6. Calendar Components'.

    The "VCALENDAR" component consists of a sequence of calendar properties and one or more calendar components.
    The calendar properties are attributes that apply to the calendar object as a whole. The calendar components are
    collections of properties that express a particular calendar semantic. For example, the calendar component can
    specify an event, a to-do, a journal entry, time zone information, free/busy time information, or an alarm.

    :param prodid: The ProdID property. Required and must occur exactly once.
    :param version: The Version property. Required and must occur exactly once.
    :param calscale: The CalScale property. Optional, but may occur at most once.
    :param method: The Method property. Optional, but may occur at most once.
    :param events: Optional list of VEvent components. Each component may occur multiple times.
    :param todos: Optional list of VToDo components. Each component may occur multiple times.
    :param journals: Optional list of VJournal components. Each component may occur multiple times.
    :param free_busy_list: Optional list of VFreeBusy components. Each component may occur multiple times.
    :param time_zones: Optional list of VTimeZone components. Each component may occur multiple times.
    """

    def __init__(
        self,
        prodid: Optional[ProdID] = None,
        version: Optional[Version] = None,
        calscale: Optional[CalScale] = None,
        method: Optional[Method] = None,
        events: Optional[List[VEvent]] = None,
        todos: Optional[List[VToDo]] = None,
        journals: Optional[List[VJournal]] = None,
        free_busy_list: Optional[List[VFreeBusy]] = None,
        time_zones: Optional[List[VTimeZone]] = None,
    ):
        super().__init__("VCALENDAR")

        # Required properties, only one occurrence allowed.
        self._prodid: Optional[ProdID] = self.as_parent(prodid)
        self._version: Optional[Version] = self.as_parent(version)

        # Optional properties, must not occur more than once.
        self.calscale: Optional[CalScale] = self.as_parent(calscale)
        self.method: Optional[Method] = self.as_parent(method)

        # These are children Components
        self.events: List[VEvent] = events or []
        self.todos: List[VToDo] = todos or []
        self.journals: List[VJournal] = journals or []
        self.free_busy_list: List[VFreeBusy] = free_busy_list or []
        self.time_zones: List[VTimeZone] = time_zones or []

        # Only the VCalender stores the entire list.
        self._lines: Optional[List[str]] = None

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"VCalendar({self.prodid.value}, {self.version.value})"

    @property
    def prodid(self) -> ProdID:
        """A getter to ensure the required property is set."""
        if self._prodid is None:
            raise MissingRequiredProperty(self, "prodid")
        return self._prodid

    @prodid.setter
    def prodid(self, value: ProdID):
        """A setter to set the required property."""
        self._prodid = value

    @property
    def version(self) -> Version:
        """A getter to ensure the required property is set."""
        if self._version is None:
            raise MissingRequiredProperty(self, "version")
        return self._version

    @version.setter
    def version(self, value: Version):
        """A setter to set the required property."""
        self._version = value

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
    def timeline(self) -> "Timeline":
        """Return a timeline of VEvents from 1970-00-00T00:00:00 to 2100-00-00T00:00:00."""
        from ical_library.timeline import Timeline

        return Timeline(self)

    def get_limited_timeline(self, start: Optional[DateTime], end: Optional[DateTime]) -> "Timeline":
        """
        Return a timeline of VEvents limited by *start* and *end*

        :param start: Only include events in the timeline with a starting date later than this value.
        :param end: Only include events in the timeline with a starting date earlier than this value.
        """
        from ical_library.timeline import Timeline

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
