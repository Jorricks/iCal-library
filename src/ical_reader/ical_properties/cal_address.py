from typing import Optional

from ical_reader.base_classes.property import Property


class _CalAddress(Property):
    @property
    def persons_name(self) -> Optional[str]:
        return self.get_property_parameter("CN")

    @property
    def email(self) -> Optional[str]:
        if self.value.startswith("mailto:"):
            return self.value[len("mailto:") :]
        return None

    @property
    def cu_type(self) -> str:
        return self.get_property_parameter_default("CUTYPE", default="INDIVIDUAL")

    @property
    def member(self) -> Optional[str]:
        return self.get_property_parameter("MEMBER")

    @property
    def role(self) -> str:
        return self.get_property_parameter_default("ROLE", default="REQ-PARTICIPANT")

    @property
    def participation_status(self) -> str:
        return self.get_property_parameter_default("PARTSTAT", default="NEEDS-ACTION")


class Attendee(_CalAddress):
    pass


class Organizer(_CalAddress):
    pass


# if __name__ == "__main__":
#     ca = _CalAddress.create_property_from_str(None, "ORGANIZER;CN=John Smith:mailto:jsmith@example.com")
#     print(ca.email)
#     print(ca.persons_name)
