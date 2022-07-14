from typing import Union

import pendulum
from pendulum import Date, DateTime

from ical_library.base_classes.property import Property
from ical_library.help_modules import dt_utils


class _DTBoth(Property):
    """This property class should be inherited. It represents a property that contain a datetime or date as value."""

    @property
    def datetime_or_date_value(self) -> Union[Date, DateTime]:
        """Return the value as a DateTime or Date value taking into account the optional TZID property parameter."""
        value = dt_utils.parse_date_or_datetime(self.value)
        if isinstance(value, DateTime):
            tz_id = self.get_property_parameter("TZID")
            if value.tz or not tz_id:
                return value
            return self.parent.tree_root.get_aware_dt_for_timezone(dt=value, tzid=tz_id)
        elif isinstance(value, Date):
            return value
        else:
            raise TypeError(f"Unknown {type(value)=} returned for {value=}.")


class _DTSingular(Property):
    """This property class should be inherited. It represents a property that can only contain a datetime as value."""

    @property
    def datetime(self) -> DateTime:
        """Return the value as a DateTime value taking into account the optional TZID property parameter."""
        value = pendulum.parse(self.value, tz=None)
        tz_id = self.get_property_parameter("TZID")
        if value.tz or not tz_id:
            return value
        return self.parent.tree_root.get_aware_dt_for_timezone(dt=value, tzid=tz_id)


# Value & TZInfo
class DTStart(_DTBoth):
    """The DTSTART property specifies when the calendar component begins.."""

    pass


# Value & TZInfo
class DTEnd(_DTBoth):
    """The DTEND property specifies the date and time that a calendar component ends."""

    pass


# Value & TZInfo
class Due(_DTBoth):
    """This DUE property defines the date and time that a to-do is expected to be completed.."""

    pass


# Value & TZInfo
class RecurrenceID(_DTBoth):
    """
    The RECURRENCE-ID property is defined as followed.

    This property is used in conjunction with the "UID" and "SEQUENCE" properties to identify a specific instance of
    a recurring "VEVENT", "VTODO", or "VJOURNAL" calendar component. The property value is the original value of the
    "DTSTART" property of the recurrence instance. Value Type: The default value type is DATE-TIME. The value type
    can be set to a DATE value type. This property MUST have the same value type as the "DTSTART" property contained
    within the recurring component. Furthermore, this property MUST be specified as a date with local time if and
    only if the "DTSTART" property contained within the recurring component is specified as a date with local time.
    """

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *LASTMODIFIED* but *LAST-MODIFIED*."""
        return "RECURRENCE-ID"


# Only date-time
class DTStamp(_DTBoth):
    """The DTSTAMP property is defined as followed.

    In the case of an iCalendar object that specifies a "METHOD" property, this property specifies the date and time
    that the instance of the iCalendar object was created. In the case of an iCalendar object that doesn't specify a
    "METHOD" property, this property specifies the date and time that the information associated with the calendar
    component was last revised in the calendar store.
    """

    pass


# Only date-time
class Completed(_DTSingular):
    """The COMPLETED property defines the date and time that a to-do was actually completed."""

    pass


# Only date-time
class Created(_DTSingular):
    """
    The CREATED property defines the date and time that the calendar information was created by the calendar
    user agent in the calendar store.
    """

    pass


# Only date-time
class LastModified(_DTSingular):
    """
    The LAST-MODIFIED property specifies the date and time that the information associated with the calendar component
    was last revised in the calendar store.
    """

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *LASTMODIFIED* but *LAST-MODIFIED*."""
        return "LAST-MODIFIED"
