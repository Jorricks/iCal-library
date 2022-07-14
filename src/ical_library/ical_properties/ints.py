from ical_library.base_classes.property import Property


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


class PercentComplete(_IntProperty):
    """
    The PERCENT-COMPLETE property is used by an assignee or delegatee of a to-do to convey the percent completion of
    a to-do to the "Organizer".
    """

    @property
    def percentage(self) -> int:
        return self.int_value

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *PERCENTCOMPLETE* but *PERCENT-COMPLETE*."""
        return "PERCENT-COMPLETE"
