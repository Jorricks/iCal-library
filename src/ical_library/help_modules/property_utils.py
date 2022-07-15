from typing import Iterator, List, Optional, Set, Tuple, Union

from pendulum import Date, DateTime, Duration
from pendulum.tz.timezone import Timezone

from ical_library.help_modules import dt_utils
from ical_library.help_modules.timespan import Timespan
from ical_library.ical_properties.periods import EXDate, RDate
from ical_library.ical_properties.rrule import RRule


def _handle_tz(dt: Union[DateTime, Date], make_tz_aware: Optional[Timezone]) -> Union[DateTime, Date]:
    """
    Small helper function to help with handling timezones.
    It makes the *dt* timezone aware if *make_tz_aware* is specified to be anything but None.
    """
    if make_tz_aware:
        return dt_utils.convert_time_object_to_aware_datetime(dt, make_tz_aware)
    else:
        return dt


def _compute_exdates(
    exdate_list: List[EXDate],
    return_range: Timespan,
    first_event_duration: Duration,
    make_tz_aware: Optional[Timezone],
    starts_to_exclude: Optional[Union[List[Date], List[DateTime]]] = None,
) -> Union[Set[Date], Set[DateTime]]:
    """
    Return a set of Dates or a set of DateTimes that should be excluded based on the EXDate definitions.

    :param exdate_list: The list of EXDate definitions of the component. This defines what dates/datetimes should be
    excluded.
    :param return_range: Returns all DateTimes starts that are within this range.
    :param first_event_duration: The duration of the original component which we should use for the rest of the
    components.
    :param make_tz_aware: If this contains a non-none value, we make all timezone naive DateTimes timezone aware to
    using this Timezone.
    :param starts_to_exclude: List of start Dates or list of start DateTimes of which we already know we should exclude
    them from our recurrence computation (as they have been completely redefined in another element).
    :return: a set of Dates or a set of DateTimes that should be excluded.
    """
    full_list: Union[Set[Date], Set[DateTime]] = set(starts_to_exclude or [])
    for exdate in exdate_list:
        full_list.update(
            _handle_tz(time, make_tz_aware)
            for time in exdate.excluded_date_times
            if return_range.intersects(Timespan(time, time + first_event_duration))  # type: ignore
        )
    return full_list


def _yield_rdate_list(
    rdate_list: List[RDate],
    excluded_times_set: Union[Set[Date], Set[DateTime]],
    first_event_duration: Duration,
    return_range: Timespan,
    make_tz_aware: Optional[Timezone],
) -> Union[Iterator[Tuple[Date, Date]], Iterator[Tuple[DateTime, DateTime]]]:
    """
    Yield a Tuple containing two Dates or yields a tuple containing two DateTimes based on the RDate definitions.

    Note: Instead of the other two functions, this yield a tuple as it might contain a start and end date (or
    start and duration to be more precise) instead of just a start date like the other two. As this duration might be
    different from the original component's duration, we need to always return the start and end date of the component
    here.

    :param rdate_list: The list of RDate definitions of the component. RDate defines a sequence of date/datetimes at
    which the component occurs as well.
    :param excluded_times_set: The set of Dates or a set of DateTimes that should be excluded.
    :param first_event_duration: The duration of the original component which we should use for the rest of the
    components.
    :param return_range: Returns all DateTimes starts that are within this range.
    :param make_tz_aware: If this contains a non-none value, we make all timezone naive DateTimes timezone aware to
    using this Timezone.
    :return: Yields a Tuple containing two Dates or yields a tuple containing two DateTimes representing the full
    duration of the occurrence.
    """
    for rdate in rdate_list:
        rdate_time: Union[DateTime, Date, Tuple[DateTime, DateTime]]
        for rdate_time in rdate.all_values:
            rdate_timespan = Timespan(rdate_time, rdate_time + first_event_duration)
            if not return_range.intersects(rdate_timespan):
                continue
            # Date covers both DateTime and Date. This is because DateTime inherits from Date.
            if isinstance(rdate_time, Date):
                rdate_time = _handle_tz(rdate_time, make_tz_aware=make_tz_aware)
                if return_range.intersects(rdate_timespan) and rdate_time not in excluded_times_set:
                    yield rdate_time, rdate_time + first_event_duration
            elif isinstance(rdate_time, tuple):
                rdate_start = _handle_tz(rdate_time[0], make_tz_aware=make_tz_aware)
                rdate_end = _handle_tz(rdate_time[1], make_tz_aware=make_tz_aware)
                if return_range.intersects(rdate_timespan) and rdate_start not in excluded_times_set:
                    yield rdate_start, rdate_end
            else:
                raise TypeError(f"RDate returned a weird type: {type=}.")


def _yield_rrule_list(
    rrule: Optional[RRule],
    excluded_times_set: Union[Set[Date], Set[DateTime]],
    first_event_start: Union[DateTime, Date],
    first_event_duration: Duration,
    return_range: Timespan,
    make_tz_aware: Optional[Timezone],
) -> Union[Iterator[Date], Iterator[DateTime]]:
    """
    Yield dates or yields DateTimes according to the RRule definition.

    Note: Depending on whether *first_event_start* is a DateTime or a Date, this function also yields in the same
    type.
    :param rrule: The RRule definition of the component.
    :param excluded_times_set: The set of Dates or a set of DateTimes that should be excluded.
    :param first_event_start: The starting point from which we should compute the recurrence.
    :param first_event_duration: The duration of the original component which we should use for the rest of the
    components.
    :param return_range: Returns all DateTimes starts that are within this range.
    :param make_tz_aware: If this contains a non-none value, we make all timezone naive DateTimes timezone aware to
    using this Timezone.
    :return: Yields dates or yields DateTimes for all occurrences of the component specified in the RRule within the
    *return_range*.
    """
    if not rrule:
        return

    iterator = rrule.sequence_iterator(first_event_start, return_range.get_end_in_same_type(first_event_start))
    rrule_time: Union[Date, DateTime]
    for rrule_time in iterator:
        rrule_time = _handle_tz(rrule_time, make_tz_aware=make_tz_aware)
        if not return_range.intersects(Timespan(rrule_time, rrule_time + first_event_duration)):
            continue
        # Date covers both DateTime and Date. This is because DateTime inherits from Date.
        if isinstance(rrule_time, Date):
            if rrule_time not in excluded_times_set:
                yield rrule_time
        else:
            raise TypeError(f"RRule returned a weird type: {type=}")


def expand_event_in_range_only_return_first(
    rdate_list: List[RDate],
    rrule: Optional[RRule],
    first_event_start: Union[DateTime, Date],
    return_range: Timespan,
    make_tz_aware: Optional[Timezone],
) -> Union[Iterator[DateTime], Iterator[Date]]:
    """
    Expand a Component without a duration according to the variables starting from the first_event_start.

    For us to expand events according to the iCalendar specification, we need to keep track of the start times as
    we should not return the same event twice. This is because RDate and RRule might return the same time twice, in
    which case RDate takes priority over RRule.

    :param rdate_list: The list of RDate definitions of the component. RDate defines a sequence of date/datetimes at
    which the component occurs as well
    :param rrule: The RRule definition of the component. RRule specifies a recurring formula from which you can compute
    the sequence of date/datetimes at which the component occurs as well.
    :param first_event_start: The starting point from which we should compute the recurrence.
    :param return_range: Returns all DateTimes starts that are within this range.
    :param make_tz_aware: If this contains a non-none value, we make all timezone naive DateTimes timezone aware to
    using this Timezone.
    :return: an Iterator returning either DateTimes or Dates.
    """
    excluded_times_set: Union[Set[DateTime], Set[Date]] = set()
    iterator = _yield_rdate_list(
        rdate_list=rdate_list,
        excluded_times_set=excluded_times_set,
        first_event_duration=Duration(),
        return_range=return_range,
        make_tz_aware=make_tz_aware,
    )
    rdate: Union[Tuple[Date, Date], Tuple[DateTime, DateTime]]
    for rdate_start, rdate_ending in iterator:
        yield rdate_start

    iterator = _yield_rrule_list(
        rrule=rrule,
        excluded_times_set=set(),
        first_event_start=first_event_start,
        first_event_duration=Duration(),
        return_range=return_range,
        make_tz_aware=make_tz_aware,
    )
    rrule_time: Union[Date, DateTime]
    for rrule_time in iterator:
        yield rrule_time


def expand_component_in_range(
    exdate_list: List[EXDate],
    rdate_list: List[RDate],
    rrule: Optional[RRule],
    first_event_start: Union[DateTime, Date],
    first_event_duration: Duration,
    starts_to_exclude: Union[List[Date], List[DateTime]],
    return_range: Timespan,
    make_tz_aware: Optional[Timezone],
) -> Union[Iterator[Tuple[DateTime, DateTime]], Iterator[Tuple[Date, Date]]]:
    """
    Expand a Component with a duration according to the variables starting from the first_event_start.

    For us to expand events according to the iCalendar specification, we need to keep track of the start times as
    we should not return the same event twice. This is because RDate and RRule might return the same time twice, in
    which case RDate takes priority over RRule. Furthermore, EXDate (which excludes dates from the other sequences)
    takes priority over the other two.

    :param exdate_list: The list of EXDate definitions of the component. This defines what dates/datetimes should be
    excluded.
    :param rdate_list: The list of RDate definitions of the component. RDate defines a sequence of date/datetimes at
    which the component occurs as well.
    :param rrule: The RRule definition of the component. RRule specifies a recurring formula from which you can compute
    the sequence of date/datetimes at which the component occurs as well.
    :param first_event_start: The starting point from which we should compute the recurrence.
    :param first_event_duration: The duration of the original component which we should use for the rest of the
    components.
    :param starts_to_exclude: List of start Dates or list of start DateTimes of which we already know we should exclude
    them from our recurrence computation (as they have been completely redefined in another element).
    :param return_range: Returns all DateTimes starts that are within this range.
    :param make_tz_aware: If this contains a non-none value, we make all timezone naive DateTimes timezone aware to
    using this Timezone.
    :return: an Iterator returning a tuple with two values of either DateTimes or Dates.
    """
    print(f"{starts_to_exclude=}")
    excluded_times_set: Union[Set[DateTime], Set[Date]] = _compute_exdates(
        exdate_list=exdate_list,
        return_range=return_range,
        make_tz_aware=make_tz_aware,
        first_event_duration=first_event_duration,
        starts_to_exclude=starts_to_exclude,
    )

    iterator = _yield_rdate_list(
        rdate_list=rdate_list,
        excluded_times_set=excluded_times_set,
        first_event_duration=first_event_duration,
        return_range=return_range,
        make_tz_aware=make_tz_aware,
    )
    rdate: Union[Tuple[Date, Date], Tuple[DateTime, DateTime]]
    for rdate in iterator:
        yield rdate

    iterator = _yield_rrule_list(
        rrule=rrule,
        excluded_times_set=excluded_times_set,
        first_event_start=first_event_start,
        first_event_duration=first_event_duration,
        return_range=return_range,
        make_tz_aware=make_tz_aware,
    )
    rrule_time: Union[Date, DateTime]
    for rrule_time in iterator:
        yield rrule_time, rrule_time + first_event_duration
