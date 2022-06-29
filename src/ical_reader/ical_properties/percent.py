from ical_reader.base_classes.property import Property


class Percent(Property):
    def percentage(self) -> int:
        return int(self.value)
