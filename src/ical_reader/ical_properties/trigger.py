from typing import Literal, Union

import pendulum
from pendulum import DateTime, Duration

from ical_reader.base_classes.property import Property


class Trigger(Property):
    @property
    def kind(self) -> Literal["DATE-TIME", "DURATION"]:
        kind_of_value = self.get_sub_property("VALUE")
        return "DATE-TIME" if kind_of_value and kind_of_value == "DATE-TIME" else "DURATION"  # noqa

    def parse_value(self) -> Union[Duration, DateTime]:
        if self.kind == "DURATION":
            parsed_value: Duration = pendulum.parse(self.value)
            if not isinstance(parsed_value, Duration):
                raise TypeError(f"Invalid value passed for Duration: {self.value=}")
            return parsed_value
        else:
            parsed_value: DateTime = pendulum.parse(self.value)
            if not isinstance(parsed_value, DateTime):
                raise TypeError(f"Invalid value passed for DateTime: {self.value=}")
            return parsed_value

    def trigger_relation(self) -> Literal["START", "END"]:
        return "START" if self.get_sub_property("RELATED", "START") == "START" else "END"  # noqa
