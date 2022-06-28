from ical_reader.base_classes.property import Property


class _IntProperty(Property):
    @property
    def int_value(self) -> int:
        return int(self.value)


class Priority(Property):
    pass


class Sequence(Property):
    pass
