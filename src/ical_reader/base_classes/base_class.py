from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ical_reader.base_classes.component import Component


class ICalBaseClass:
    """
    This is the base class of all custom classes representing an iCal component or iCal property in our library.

    :class:`Component` and :class:`Property` are the only ones inheriting this class directly, the rest of the classes
    are inheriting from :class:`Component` and :class:`Property` based on whether they represent an iCal component or
    iCal property.

    :param name: the actual name of this property or component. E.g. VEVENT, RRULE, VCUSTOMCOMPONENT, CUSTOMPROPERTY.
    :param parent: the parent :class:`Component` instance that contains this :class:`Component` instance.
    """

    def __init__(self, name: str, parent: Optional["Component"]):
        self._name: str = name
        self._parent: Optional["Component"] = parent

    @property
    def parent(self) -> Optional["Component"]:
        """
        Return the parent :class:`Component` that contains this :class:`Component`.
        :return: Return the parent :class:`Component` instance or None in the case there is no parent (for VCalender's).
        """
        return self._parent

    @property
    def name(self) -> str:
        """
        Return the actual name of this property or component. E.g. VEVENT, RRULE, VCUSTOMCOMPONENT, CUSTOMPROPERTY.

        We inherit this class, for the general Property and Component but also for the specific VEvent component and
        the RRule property. Now what do we do with the `x-comp` or `iana-comp` components and `x-prop` and `iana-prop`
        properties? They also have an iCalendar name, e.g. VCUSTOMCOMPONENT. However, we can't specify them beforehand
        as we simply can't cover all cases. Therefore, we use `get_ical_name_of_class` to find and map all of our
        pre-defined Components and Properties but we still specify the name for all custom components. So the rule of
        thumb:
        Use `.name` on instantiated classes while we use `.get_ical_name_of_class()` for non-instantiated classes.
        """
        return self._name

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """
        Return the name of a pre-defined property or pre-defined component. E.g. VEVENT, RRULE, COMPONENT, PROPERTY.

        For a :class:`Property` this would be the value at the start of the line. Example: a property with the name of
        `ABC;def=ghi:jkl` would be `ABC`.
        For a :class:`Component` this would be the value at the start of the component after BEGIN. Example: a VEvent
        starts with `BEGIN:VEVENT`, hence this function would return `VEVENT`.
        """
        return cls.__name__.upper()
