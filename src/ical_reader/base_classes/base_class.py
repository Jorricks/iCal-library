class ICalBaseClass:
    """
    This is the base class of all custom classes representing an iCal component or iCal property in our library.

    :class:`Component` and :class:`Property` are the only ones inheriting this class directly, the rest of the classes
    are inheriting from :class:`Component` and :class:`Property` based on whether they represent an iCal component or
    iCal property.
    """

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """
        Return the name of the object as described in the standard.

        For a :class:`Property` this would be the value at the start of the line. Example: a property with the name of
        `ABC;def=ghi:jkl` would be `ABC`.
        For a :class:`Component` this would be the value at the start of the component after BEGIN. Example: a VEvent
        starts with `BEGIN:VEVENT`, hence this function would return `VEVENT`.
        """
        return cls.__name__.upper()
