from ical_reader.base_classes.property import Property


class _IntProperty(Property):
    """This property class should be inherited. It represents a property that contain just an int as value."""

    @property
    def int_value(self) -> int:
        """Return the value as an int."""
        return int(self.value)


class Priority(_IntProperty):
    """The PRIORITY property represents the relative priority for a calendar component."""

    pass


class Sequence(_IntProperty):
    """
    The SEQUENCE property defines the revision sequence number of the calendar component within a sequence of revisions.
    """

    pass


class Repeat(_IntProperty):
    """The REPEAT property defines the number of times the alarm should be repeated, after the initial trigger."""

    pass
