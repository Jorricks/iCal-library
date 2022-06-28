from typing import Union

import pendulum
from pendulum import DateTime, Date

from ical_reader.ical_utils import dt_utils
from ical_reader.base_classes.property import Property


class _DTBoth(Property):
    @property
    def datetime_or_date_value(self) -> Union[Date, DateTime]:
        value = dt_utils.parse_date_or_datetime(self.value)
        if isinstance(value, DateTime):
            tz_id = self.get_sub_property("TZID", None)
            if value.tz or not tz_id:
                return value
            return self.parent.tree_root.get_aware_dt_for_timezone(dt=value, tzid=tz_id)
        elif isinstance(value, Date):
            return value
        else:
            raise TypeError(f"Unknown {type(value)=} returned for {value=}.")


class _DTSingular(Property):
    @property
    def datetime(self) -> DateTime:
        value = pendulum.parse(self.value, tz=None)
        tz_id = self.get_sub_property("TZID", None)
        if value.tz or not tz_id:
            return value
        return self.parent.tree_root.get_aware_dt_for_timezone(dt=value, tzid=tz_id)


# Value & TZInfo
class DTStart(_DTBoth):
    pass


# Value & TZInfo
class DTEnd(_DTBoth):
    pass


# Value & TZInfo
class Due(_DTBoth):
    pass


# Value & TZInfo
class RecurrenceID(_DTBoth):
    pass


# Only date-time
class DTStamp(_DTBoth):
    pass


# Only date-time
class Completed(_DTSingular):
    pass


# Only date-time
class Created(_DTSingular):
    pass


# Only date-time
class LastModified(_DTSingular):
    @classmethod
    def get_ical_name_of_class(cls) -> str:
        return "LAST-MODIFIED"
