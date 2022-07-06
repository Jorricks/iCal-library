import heapq
from collections import defaultdict
from typing import Iterator, List, Mapping, Optional, Tuple, TYPE_CHECKING

from pendulum import DateTime

from ical_reader.help_modules.lru_cache import instance_lru_cache
from ical_reader.help_modules.timespan import Timespan, TimespanWithParent
from ical_reader.ical_components.v_event import VEvent

if TYPE_CHECKING:
    from ical_reader.ical_components.v_calendar import VCalendar


class Timeline:
    """
    This class is a wrapper to make it easy to see what the order of each component based on the start date.

    Inside this class there are multiple methods to iterate over all the components present. However, one should note
    that often the recurrence properties for components specify only a lower bound and will therefore proceed to
    infinity. To prevent us having an infinite list of items to iterate on, we define upper and lower bounds.
    You should set these upper bounds to the absolute minimum start date and absolute maximum end date that you would
    ever need. So if you need to do 10 different queries, this start and end date should range all of these, so it
    doesn't need to compute the list of components in the range over and over again. The functions themselves(e.g.
    :function:`self.includes` and :function:`self.intersects`) help you  to limit the exact range you want to return
    components for.
    """

    def __init__(
        self, v_calendar: "VCalendar", start_date: Optional[DateTime] = None, end_date: Optional[DateTime] = None
    ):
        """
        Instantiate the Timeline class.
        :param v_calendar: The VCalendar object we are iterating over.
        :param start_date: The
        :param end_date:
        """
        self.v_calendar: VCalendar = v_calendar
        self._start_date: DateTime = start_date or DateTime(1970, 1, 1)
        self._end_date: DateTime = end_date or DateTime(2100, 1, 1)

    # @ToDo improve upon the time filtering here by using intersect.
    # @ToDo also allow ToDo & Journal expansions.
    # @ToDo inside the RRule, compute an estimated end_date so we can skip many right away.

    @property
    def start_date(self) -> DateTime:
        """Return the start date of the timeline. No event should end before this value."""
        return self._start_date

    @start_date.setter
    def start_date(self, value) -> None:
        """Set the start date of the timeline."""
        self._start_date = value
        self.get_timespan.cache_clear()

    @property
    def end_date(self) -> DateTime:
        """Return the end date of the timeline. No event should start before this value."""
        return self._end_date

    @end_date.setter
    def end_date(self, value) -> None:
        """Set the end date of the timeline."""
        self._end_date = value
        self.get_timespan.cache_clear()

    @instance_lru_cache()
    def get_timespan(self) -> Timespan:
        """Return the start and end date as a Timespan."""
        return Timespan(self.start_date, self.end_date)

    @staticmethod
    def de_duplicate_events(list_of_events: List[VEvent]) -> List[VEvent]:
        """
        Deduplicate recurring components. Sometimes it happens that recurring events are changed and this will cause
        them to both be present as a standard component and in the recurrence.
        :param list_of_events: The list of all components that we should deduplicate.
        :return: A deduplicated list of components.
        """
        event_dict: Mapping[Tuple[Tuple[DateTime, DateTime], str], List[VEvent]] = defaultdict(list)
        for event in list_of_events:
            event_dict[(event.timespan.tuple, event.summary.value if event.summary else "")].append(event)
        for keys, events in event_dict.items():
            if len(events) == 1:
                continue
            for i, event_a in list(enumerate(events)):
                if event_a.recurrence_id is not None:
                    del events[i]
        return [event for event_list in event_dict.values() for event in event_list]

    def explode_recurring_events(self) -> List[VEvent]:
        """
        Get a de-duplicated list of all components, including the recurring components. This means that we add all
        child component of the :class:`VCalendar` (except for the :class:`VTimeZone` instances) to a list and then add
        all extra occurrences (as recurring components) according to the recurrence properties: :class:`RRule`,
        :class:`RDate` and :class:`EXDate`.
        :return: A de-duplicated list of all components, including the recurring occurrences of the components.
        """
        list_of_v_events: List[VEvent] = []
        for e in self.v_calendar.events:
            # Do some initial filtering.
            if not e.start or not e.end:
                continue
            intersects = e.timespan.intersects(self.get_timespan())
            if not (intersects or e.rrule or e.rdate):
                continue

            list_of_v_events.extend(e.expand_component_in_range(self.get_timespan()))
        return self.de_duplicate_events(list_of_v_events)

    def iterate(self) -> Iterator[Tuple[TimespanWithParent, VEvent]]:
        """Iterate over the `self.explode_recurring_events()` in chronological order."""
        # Using a heap is faster than sorting if the number of events (n) is
        # much bigger than the number of events we extract from the iterator (k).
        # Complexity: O(n + k log n).
        heap: List[TimespanWithParent] = [e.timespan for e in self.explode_recurring_events()]
        heapq.heapify(heap)
        while heap:
            popped = heapq.heappop(heap)
            if not isinstance(popped.parent, VEvent):
                raise TypeError("Expected only VEvents here!")
            yield popped, popped.parent

    def includes(self, start: DateTime, stop: DateTime) -> Iterator[VEvent]:
        """Iterate (in chronological order) over every event that is in the specified timespan."""
        query_timespan = Timespan(start, stop)
        for timespan, event in self.iterate():
            if timespan.is_included_in(query_timespan):
                yield event

    def overlapping(self, start: DateTime, stop: DateTime) -> Iterator[VEvent]:
        """Iterate (in chronological order) over every event that has an intersection with the timespan."""
        query_timespan = Timespan(start, stop)
        for timespan, event in self.iterate():
            if timespan.intersects(query_timespan):
                yield event

    def start_after(self, instant: DateTime) -> Iterator[VEvent]:
        """Iterate (in chronological order) on every event larger than instant in chronological order."""
        for timespan, event in self.iterate():
            if timespan.begin > instant:
                yield event

    def at(self, instant: DateTime) -> Iterator[VEvent]:
        """Iterate (in chronological order) over all events that are occurring during `instant`."""
        for timespan, event in self.iterate():
            if timespan.includes(instant):
                yield event
