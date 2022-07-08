from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ical_reader.base_classes.component import Component


class CalendarParentRelationError(ValueError):
    """Indicate finding the tree root failed as it did not find a VCalendar root."""

    pass


class VEventExpansionFailed(ValueError):
    """Indicate the expansion based on recurring properties failed."""

    pass


class MissingRequiredProperty(ValueError):
    """Indicate a required property is not set for a Component."""

    def __init__(self, component: "Component", missing_property_name: str):
        self.component = component
        self.missing_property_name = missing_property_name

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return (
            f"The required property named {self.missing_property_name} was not set for "
            f"{self.component.__class__.__name__}"
        )
