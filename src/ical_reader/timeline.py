import heapq
from collections import defaultdict
from typing import Iterator, List, Mapping, Optional, Tuple, TYPE_CHECKING

from pendulum import DateTime

from ical_reader.help_classes.timespan import Timespan, TimespanWithParent
from ical_reader.ical_components.v_event import VEvent
from ical_reader.ical_utils.lru_cache import instance_lru_cache

if TYPE_CHECKING:
    from ical_reader.ical_components.v_calendar import VCalendar


class Timeline:
    def __init__(
        self, v_calendar: "VCalendar", start_date: Optional[DateTime] = None, end_date: Optional[DateTime] = None
    ):
        self.v_calendar: VCalendar = v_calendar
        self._start_date: DateTime = start_date or DateTime(1970, 1, 1)
        self._end_date: DateTime = end_date or DateTime(2100, 1, 1)

    # @ToDo(jorrick) also allow ToDo & Journal expansions.
    # @ToDo(jorrick) inside the RRule, compute an estimated end_date so we can skip many right away.

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value
        self.get_timespan.cache_clear()

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value
        self.get_timespan.cache_clear()

    @instance_lru_cache()
    def get_timespan(self):
        return Timespan(self.start_date, self.end_date)

    @staticmethod
    def de_duplicate_events(list_of_events: List[VEvent]) -> List[VEvent]:
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
