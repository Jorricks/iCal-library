from ical_reader.base_classes.property import Property


class PercentComplete(Property):
    """
    The PERCENT-COMPLETE property is used by an assignee or delegatee of a to-do to convey the percent completion of
    a to-do to the "Organizer".
    """

    def percentage(self) -> int:
        return int(self.value)

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *PERCENTCOMPLETE* but *PERCENT-COMPLETE*."""
        return "PERCENT-COMPLETE"
