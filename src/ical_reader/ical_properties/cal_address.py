from typing import Optional

from ical_reader.base_classes.property import Property


class _CalAddress(Property):
    @property
    def persons_name(self) -> Optional[str]:
        """Return the persons name, identified by the CN property parameter."""
        return self.get_property_parameter("CN")

    @property
    def email(self) -> Optional[str]:
        """Return the email if the value starts with `mailto:`. Otherwise return None."""
        if self.value.startswith("mailto:"):
            return self.value[len("mailto:") :]
        return None

    @property
    def cu_type(self) -> str:
        """Return the CUTYPE."""
        return self.get_property_parameter_default("CUTYPE", default="INDIVIDUAL")

    @property
    def member(self) -> Optional[str]:
        """Return the membership property parameter."""
        return self.get_property_parameter("MEMBER")

    @property
    def role(self) -> str:
        """Return the role of the person."""
        return self.get_property_parameter_default("ROLE", default="REQ-PARTICIPANT")

    @property
    def participation_status(self) -> str:
        """Return the participation status, indicating whether the person will be present or not."""
        return self.get_property_parameter_default("PARTSTAT", default="NEEDS-ACTION")


class Attendee(_CalAddress):
    """The ATTENDEE property defines an "Attendee" within a calendar component."""

    pass


class Organizer(_CalAddress):
    """The ORGANIZER property defines the organizer for a calendar component."""

    pass


# if __name__ == "__main__":
#     ca = _CalAddress.create_property_from_str(None, "ORGANIZER;CN=John Smith:mailto:jsmith@example.com")
#     print(ca.email)
#     print(ca.persons_name)
