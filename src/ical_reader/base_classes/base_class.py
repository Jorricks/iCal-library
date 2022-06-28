class ICalBaseClass:
    @classmethod
    def get_ical_name_of_class(cls) -> str:
        return cls.__name__.upper()
