import pendulum

from ical_reader.base_classes.property import Property


class ICALDuration(Property):
    @property
    def duration(self) -> pendulum.Duration:
        parsed_value: pendulum.Duration = pendulum.parse(self.value)
        if not isinstance(parsed_value, pendulum.Duration):
            raise TypeError(f"Invalid value passed for Duration: {self.value=}")
        return parsed_value
