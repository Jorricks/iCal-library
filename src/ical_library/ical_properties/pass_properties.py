from ical_library.base_classes.property import Property


class ProdID(Property):
    """The PRODID property specifies the identifier for the product that created the iCalendar object."""

    pass


class Version(Property):
    """
    The VERSION property specifies the identifier corresponding to the highest version number or the minimum and
    maximum range of the iCalendar specification that is required in order to interpret the iCalendar object.
    """

    pass


class CalScale(Property):
    """
    The CALSCALE property defines the calendar scale used for the calendar information specified in the iCalendar
    object.
    """

    pass


class Method(Property):
    """The METHOD property defines the iCalendar object method associated with the calendar object."""

    pass


class Class(Property):
    """The CLASS property defines the access classification for a calendar component."""

    pass


class Description(Property):
    """
    The DESCRIPTION property provides a more complete description of the calendar component than that provided by
    the "SUMMARY" property.
    """

    pass


class Location(Property):
    """The LOCATION property defines the intended venue for the activity defined by a calendar component."""

    pass


class Status(Property):
    """The STATUS property defines the overall status or confirmation for the calendar component."""

    pass


class TimeTransparency(Property):
    """The TRANSP property defines whether an event is transparent to busy time searches."""

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *TIMETRANSPARANCY* but *TRANSP*."""
        return "TRANSP"


class URL(Property):
    """The URL property defines a Uniform Resource Locator (URL) associated with the iCalendar object."""

    pass


class Attach(Property):
    """The ATTACH property provides the capability to associate a document object with a calendar component."""

    pass


class Categories(Property):
    """The CATEGORIES property defines the categories for a calendar component."""

    pass


class Contact(Property):
    """
    The CONTACT property is used to represent contact information or alternately a reference to contact information
    associated with the calendar component.
    """

    pass


class RequestStatus(Property):
    """The REQUEST-STATUS property defines the status code returned for a scheduling request."""

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *REQUESTSTATUS* but *REQUEST-STATUS*."""
        return "REQUEST-STATUS"


class RelatedTo(Property):
    """
    The RELATED-TO property is used to represent a relationship or reference between one calendar component and another.
    """

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *RELATEDTO* but *RELATED-TO*."""
        return "RELATED-TO"


class Resources(Property):
    """
    The RESOURCES property defines the equipment or resources anticipated for an activity specified by a calendar
    component.
    """

    pass


class Action(Property):
    """The ACTION property defines the action to be invoked when an alarm is triggered."""

    pass


class UID(Property):
    """The UID property defines the persistent, globally unique identifier for the calendar component."""

    pass


class Comment(Property):
    """The COMMENT property specifies non-processing information intended to provide a comment to the calendar user."""

    pass


class TZName(Property):
    """The TZNAME property specifies the customary designation for a time zone description."""

    pass


class TZID(Property):
    """
    The TZID property specifies the text value that uniquely identifies the "VTIMEZONE" calendar component in the scope
    of an iCalendar object.
    """

    pass


class TZURL(Property):
    """
    The TZURL property provides a means for a "VTIMEZONE" component to point to a network location that can be used to
    retrieve an up- to-date version of itself.
    """

    pass


class Summary(Property):
    """
    The SUMMARY property defines a short summary or subject for the calendar component.
    """

    pass
