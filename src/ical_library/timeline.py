import heapq
from collections import defaultdict
from typing import Dict, Iterator, List, Optional, Tuple, Union

from pendulum import Date, DateTime

from ical_library.base_classes.component import Component
from ical_library.help_modules.lru_cache import instance_lru_cache
from ical_library.help_modules.timespan import Timespan, TimespanWithParent
from ical_library.ical_components import VCalendar, VFreeBusy
from ical_library.ical_components.abstract_components import AbstractComponentWithRecurringProperties


class Timeline:
    """
    This class is a wrapper to make it easy to see what the order of each component based on the start date.

    Inside this class there are multiple methods to iterate over all the components present. However, one should note
    that often the recurrence properties for components specify only a lower bound and will therefore proceed to
    infinity. To prevent us having an infinite list of items to iterate on, we define upper and lower bounds.
    You should set these upper bounds to the absolute minimum start date and absolute maximum end date that you would
    ever need. So if you need to do 10 different queries, this start and end date should range all of these, so it
    doesn't need to compute the list of components in the range over and over again. The functions themselves(e.g.
    :function:`self.includes` and :function:`self.intersects`) help you to limit the exact range you want to return
    components for.

    :param v_calendar: The VCalendar object we are iterating over.
    :param start_date: The minimum ending date of each event that is returned inside this timeline.
    :param end_date: The maximum starting date of each event that is return inside this timeline.
    """

    def __init__(
        self, v_calendar: VCalendar, start_date: Optional[DateTime] = None, end_date: Optional[DateTime] = None
    ):
        self.v_calendar: VCalendar = v_calendar
        self._start_date: DateTime = start_date or DateTime(1970, 1, 1)
        self._end_date: DateTime = end_date or DateTime(2100, 1, 1)

    def __repr__(self) -> str:
        return f"Timeline({self._start_date}, {self._end_date})"

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
    def __get_items_to_exclude_from_recurrence(
        all_components: List[Component],
    ) -> Dict[str, Union[List[Date], List[DateTime]]]:
        """
        Deduplicate recurring components. Sometimes it happens that recurring events are changed and this will cause
        them to both be present as a standard component and in the recurrence.
        :param all_components: The list of all component children of the VCalendar instance.
        :return: A deduplicated list of components.
        """
        start_date_to_timespan_dict: Dict[str, Union[List[Date], List[DateTime]]] = defaultdict(list)
        for component in all_components:
            if isinstance(component, AbstractComponentWithRecurringProperties) and component.recurrence_id is not None:
                start_date_to_timespan_dict[component.uid.value].append(component.recurrence_id.datetime_or_date_value)
        return start_date_to_timespan_dict

    def __explode_recurring_components(self) -> List[TimespanWithParent]:
        """
        Get a de-duplicated list of all components with a start date, including the recurring components. This means
        that we add all child component of the :class:`VCalendar` (except for the :class:`VTimeZone` instances) to a
        list and then add all extra occurrences (as recurring components) according to the recurrence properties:
        :class:`RRule`, :class:`RDate` and :class:`EXDate`.
        :return: A de-duplicated list of all components, including the recurring occurrences of the components.
        """
        list_of_timestamps_with_parents: List[TimespanWithParent] = []
        all_children = self.v_calendar.children
        uid_to_datetime_to_exclude = self.__get_items_to_exclude_from_recurrence(all_children)
        for c in all_children:
            # Do some initial filtering.
            if isinstance(c, AbstractComponentWithRecurringProperties):
                if c.max_recurring_timespan.intersects(self.get_timespan()):
                    values_to_exclude = uid_to_datetime_to_exclude.get(c.uid.value)
                    list_of_timestamps_with_parents.extend(
                        c.expand_component_in_range(self.get_timespan(), values_to_exclude)
                    )
            elif isinstance(c, VFreeBusy):
                if c.timespan.intersects(self.get_timespan()):
                    list_of_timestamps_with_parents.append(c.timespan)
            else:
                # There is no way to extend iana-props or x-props for now. If you feel like implementing this, please
                # let me know and open a PR :).
                pass
        return list_of_timestamps_with_parents

    def iterate(self) -> Iterator[Tuple[TimespanWithParent, Component]]:
        """
        Iterate over the `self.__explode_recurring_components()` in chronological order.

        Implementation detail: Using a heap is faster than sorting if the number of events (n) is much bigger than the
        number of events we extract from the iterator (k). Complexity: O(n + k log n).
        """
        heap: List[TimespanWithParent] = self.__explode_recurring_components()
        heapq.heapify(heap)
        while heap:
            popped: TimespanWithParent = heapq.heappop(heap)
            yield popped, popped.parent

    def includes(self, start: DateTime, stop: DateTime) -> Iterator[Component]:
        """Iterate (in chronological order) over every component that is in the specified timespan."""
        query_timespan = Timespan(start, stop)
        for timespan, event in self.iterate():
            if timespan.is_included_in(query_timespan):
                yield event

    def overlapping(self, start: DateTime, stop: DateTime) -> Iterator[Component]:
        """Iterate (in chronological order) over every component that has an intersection with the timespan."""
        query_timespan = Timespan(start, stop)
        for timespan, event in self.iterate():
            if timespan.intersects(query_timespan):
                yield event

    def start_after(self, instant: DateTime) -> Iterator[Component]:
        """Iterate (in chronological order) on every component larger than instant in chronological order."""
        for timespan, event in self.iterate():
            if timespan.begin > instant:
                yield event

    def at(self, instant: DateTime) -> Iterator[Component]:
        """Iterate (in chronological order) over all component that are occurring during `instant`."""
        for timespan, event in self.iterate():
            if timespan.includes(instant):
                yield event
