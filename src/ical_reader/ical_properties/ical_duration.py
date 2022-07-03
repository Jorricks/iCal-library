import pendulum

from ical_reader.base_classes.property import Property


class ICALDuration(Property):
    """The DURATION property specifies a positive duration of time."""

    @property
    def duration(self) -> pendulum.Duration:
        """Return the value as a parsed pendulum.Duration."""
        parsed_value: pendulum.Duration = pendulum.parse(self.value)
        if not isinstance(parsed_value, pendulum.Duration):
            raise TypeError(f"Invalid value passed for Duration: {self.value=}")
        return parsed_value

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *ICALDURATION* but *DURATION*."""
        return "DURATION"
