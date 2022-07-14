from typing import Literal, Union

import pendulum
from pendulum import DateTime, Duration

from ical_library.base_classes.property import Property


class Trigger(Property):
    """The TRIGGER property specifies when an alarm will trigger."""

    @property
    def kind(self) -> Literal["DATE-TIME", "DURATION"]:
        """Return the type of the property value."""
        kind_of_value = self.get_property_parameter("VALUE")
        return "DATE-TIME" if kind_of_value and kind_of_value == "DATE-TIME" else "DURATION"  # noqa

    def parse_value(self) -> Union[Duration, DateTime]:
        """Parse the value of this property based on the VALUE property parameter."""
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
        """Get the trigger relation, whether the duration should be relative to the start or the end of a component."""
        return "START" if self.get_property_parameter_default("RELATED", "START") == "START" else "END"  # noqa
