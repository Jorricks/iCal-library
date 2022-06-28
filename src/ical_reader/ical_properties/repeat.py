from ical_reader.base_classes.property import Property


class Repeat(Property):
    def get_int(self):
        return int(self.value)
