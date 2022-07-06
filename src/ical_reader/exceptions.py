class CalendarParentRelationError(ValueError):
    """Indicate finding the tree root failed as it did not find a VCalendar root."""

    pass


class VEventExpansionFailed(ValueError):
    """Indicate the expansion based on recurring properties failed."""

    pass
