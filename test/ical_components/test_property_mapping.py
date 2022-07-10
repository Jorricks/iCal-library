from ical_reader.ical_components import (
    DayLight,
    Standard,
    VAlarm,
    VCalendar,
    VEvent,
    VFreeBusy,
    VJournal,
    VTimeZone,
    VToDo,
)
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import Completed, Created, DTEnd, DTStamp, DTStart, Due, LastModified, RecurrenceID
from ical_reader.ical_properties.geo import GEO
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import PercentComplete, Priority, Repeat, Sequence
from ical_reader.ical_properties.pass_properties import (
    Action,
    Attach,
    CalScale,
    Categories,
    Class,
    Comment,
    Contact,
    Description,
    Location,
    Method,
    ProdID,
    RelatedTo,
    RequestStatus,
    Resources,
    Status,
    Summary,
    TimeTransparency,
    TZID,
    TZName,
    TZURL,
    UID,
    URL,
    Version,
)
from ical_reader.ical_properties.periods import EXDate, FreeBusyProperty, RDate
from ical_reader.ical_properties.rrule import RRule
from ical_reader.ical_properties.trigger import Trigger
from ical_reader.ical_properties.tz_offset import TZOffsetFrom, TZOffsetTo


def test_get_property_ical_names():
    assert VCalendar.get_property_ical_names() == {"calscale", "prodid", "version", "method"}
    assert VAlarm.get_property_ical_names() == {"attach", "repeat", "trigger", "action", "duration"}


def test_valarm_get_property_mapping():
    assert VAlarm._get_property_mapping() == {
        "ACTION": ("action", Action, False),
        "ATTACH": ("attach", Attach, False),
        "DURATION": ("duration", ICALDuration, False),
        "REPEAT": ("repeat", Repeat, False),
        "TRIGGER": ("trigger", Trigger, False),
    }


def test_vcalendar_get_property_mapping():
    assert VCalendar._get_property_mapping() == {
        "CALSCALE": ("calscale", CalScale, False),
        "METHOD": ("method", Method, False),
        "PRODID": ("prodid", ProdID, False),
        "VERSION": ("version", Version, False),
    }


def test_vevent_get_property_mapping():
    assert VEvent._get_property_mapping() == {
        "ATTACH": ("attach", Attach, True),
        "ATTENDEE": ("attendee", Attendee, True),
        "CATEGORIES": ("categories", Categories, True),
        "CLASS": ("ical_class", Class, False),
        "COMMENT": ("comment", Comment, True),
        "CONTACT": ("contact", Contact, True),
        "CREATED": ("created", Created, False),
        "DESCRIPTION": ("description", Description, False),
        "DTEND": ("dtend", DTEnd, False),
        "DTSTAMP": ("dtstamp", DTStamp, False),
        "DTSTART": ("dtstart", DTStart, False),
        "DURATION": ("duration", ICALDuration, False),
        "EXDATE": ("exdate", EXDate, True),
        "GEO": ("geo", GEO, False),
        "LAST-MODIFIED": ("last_modified", LastModified, False),
        "LOCATION": ("location", Location, False),
        "ORGANIZER": ("organizer", Organizer, False),
        "PRIORITY": ("priority", Priority, False),
        "RDATE": ("rdate", RDate, True),
        "RECURRENCE-ID": ("recurrence_id", RecurrenceID, False),
        "RELATED-TO": ("related", RelatedTo, True),
        "REQUEST-STATUS": ("rstatus", RequestStatus, True),
        "RESOURCES": ("resources", Resources, True),
        "RRULE": ("rrule", RRule, False),
        "SEQUENCE": ("sequence", Sequence, False),
        "STATUS": ("status", Status, False),
        "SUMMARY": ("summary", Summary, False),
        "TRANSP": ("transp", TimeTransparency, False),
        "UID": ("uid", UID, False),
        "URL": ("url", URL, False),
    }


def test_vfreebusy_get_property_mapping():
    assert VFreeBusy._get_property_mapping() == {
        "ATTENDEE": ("attendee", Attendee, True),
        "COMMENT": ("comment", Comment, True),
        "CONTACT": ("contact", Contact, False),
        "DTEND": ("dtend", DTEnd, False),
        "DTSTAMP": ("dtstamp", DTStamp, False),
        "DTSTART": ("dtstart", DTStart, False),
        "FREEBUSY": ("freebusy", FreeBusyProperty, True),
        "ORGANIZER": ("organizer", Organizer, False),
        "REQUEST-STATUS": ("rstatus", RequestStatus, True),
        "UID": ("uid", UID, False),
        "URL": ("url", URL, False),
    }


def test_vjournal_get_property_mapping():
    assert VJournal._get_property_mapping() == {
        "ATTACH": ("attach", Attach, True),
        "ATTENDEE": ("attendee", Attendee, True),
        "CATEGORIES": ("categories", Categories, True),
        "CLASS": ("ical_class", Class, False),
        "COMMENT": ("comment", Comment, True),
        "CONTACT": ("contact", Contact, True),
        "CREATED": ("created", Created, False),
        "DESCRIPTION": ("description", Description, True),
        "DTSTAMP": ("dtstamp", DTStamp, False),
        "DTSTART": ("dtstart", DTStart, False),
        "EXDATE": ("exdate", EXDate, True),
        "LAST-MODIFIED": ("last_modified", LastModified, False),
        "ORGANIZER": ("organizer", Organizer, False),
        "RDATE": ("rdate", RDate, True),
        "RECURRENCE-ID": ("recurrence_id", RecurrenceID, False),
        "RELATED-TO": ("related", RelatedTo, True),
        "REQUEST-STATUS": ("rstatus", RequestStatus, True),
        "RRULE": ("rrule", RRule, False),
        "SEQUENCE": ("sequence", Sequence, False),
        "STATUS": ("status", Status, False),
        "SUMMARY": ("summary", Summary, False),
        "UID": ("uid", UID, False),
        "URL": ("url", URL, False),
    }


def test_vtimezone_get_property_mapping():
    assert VTimeZone._get_property_mapping() == {
        "LAST-MODIFIED": ("last_mod", LastModified, False),
        "TZID": ("tzid", TZID, False),
        "TZURL": ("tzurl", TZURL, False),
    }


def test_vtodo_get_property_mapping():
    assert VToDo._get_property_mapping() == {
        "ATTACH": ("attach", Attach, True),
        "ATTENDEE": ("attendee", Attendee, True),
        "CATEGORIES": ("categories", Categories, True),
        "CLASS": ("ical_class", Class, False),
        "COMMENT": ("comment", Comment, True),
        "COMPLETED": ("completed", Completed, False),
        "CONTACT": ("contact", Contact, True),
        "CREATED": ("created", Created, False),
        "DESCRIPTION": ("description", Description, False),
        "DTSTAMP": ("dtstamp", DTStamp, False),
        "DTSTART": ("dtstart", DTStart, False),
        "DUE": ("due", Due, False),
        "DURATION": ("duration", ICALDuration, False),
        "EXDATE": ("exdate", EXDate, True),
        "GEO": ("geo", GEO, False),
        "LAST-MODIFIED": ("last_modified", LastModified, False),
        "LOCATION": ("location", Location, False),
        "ORGANIZER": ("organizer", Organizer, False),
        "PERCENT-COMPLETE": ("percent", PercentComplete, False),
        "PRIORITY": ("priority", Priority, False),
        "RDATE": ("rdate", RDate, True),
        "RECURRENCE-ID": ("recurrence_id", RecurrenceID, False),
        "RELATED-TO": ("related", RelatedTo, True),
        "REQUEST-STATUS": ("rstatus", RequestStatus, True),
        "RESOURCES": ("resources", Resources, True),
        "RRULE": ("rrule", RRule, False),
        "SEQUENCE": ("sequence", Sequence, False),
        "STATUS": ("status", Status, False),
        "SUMMARY": ("summary", Summary, False),
        "UID": ("uid", UID, False),
        "URL": ("url", URL, False),
    }


def test_daylight_and_get_property_mapping():
    expected = {
        "COMMENT": ("comment", Comment, True),
        "DTSTART": ("dtstart", DTStart, False),
        "RDATE": ("rdate", RDate, True),
        "RRULE": ("rrule", RRule, False),
        "TZNAME": ("tzname", TZName, True),
        "TZOFFSETFROM": ("tzoffsetfrom", TZOffsetFrom, False),
        "TZOFFSETTO": ("tzoffsetto", TZOffsetTo, False),
    }
    assert DayLight._get_property_mapping() == expected
    assert Standard._get_property_mapping() == expected
