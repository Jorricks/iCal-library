from typing import List, Optional

from ical_reader.base_classes.component import Component
from ical_reader.exceptions import MissingRequiredProperty
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import DTEnd, DTStamp, DTStart
from ical_reader.ical_properties.pass_properties import Comment, Contact, RequestStatus, UID, URL
from ical_reader.ical_properties.periods import FreeBusyProperty


class VFreeBusy(Component):
    """
    This class represents the VFREEBUSY component specified in RFC 5545 in '3.6.4. Free/Busy Component'.

    A "VFREEBUSY" calendar component is a grouping of component properties that represents either a request for free
    or busy time information, a reply to a request for free or busy time information, or a published set of busy time
    information.

    :param name: The actual name of this component instance. E.g. VEVENT, RRULE, VCUSTOMCOMPONENT.
    :param parent: The Component this item is encapsulated by in the iCalendar data file.
    :param dtstamp: The DTStamp property. Required and must occur exactly once.
    :param uid: The UID property. Required and must occur exactly once.
    :param contact: The Contact property. Optional, but may occur at most once.
    :param dtstart: The DTStart property. Optional, but may occur at most once.
    :param dtend: The DTEnd property. Optional, but may occur at most once.
    :param organizer: The Organizer property. Optional, but may occur at most once.
    :param url: The URL property. Optional, but may occur at most once.
    :param attendee: The Attendee property. Optional, but may occur multiple times.
    :param comment: The Comment property. Optional, but may occur multiple times.
    :param freebusy: The FreeBusyProperty property. Optional, but may occur multiple times.
    :param rstatus: The RequestStatus property. Optional, but may occur multiple times.
    """

    def __init__(
        self,
        parent: Optional[Component],
        dtstamp: Optional[DTStamp] = None,
        uid: Optional[UID] = None,
        contact: Optional[Contact] = None,
        dtstart: Optional[DTStart] = None,
        dtend: Optional[DTEnd] = None,
        organizer: Optional[Organizer] = None,
        url: Optional[URL] = None,
        attendee: Optional[List[Attendee]] = None,
        comment: Optional[List[Comment]] = None,
        freebusy: Optional[List[FreeBusyProperty]] = None,
        rstatus: Optional[List[RequestStatus]] = None,
    ):
        super().__init__("VFREEBUSY", parent)

        # Required
        self._dtstamp: Optional[DTStamp] = dtstamp
        self._uid: Optional[UID] = uid

        # Optional, may only occur once
        self.contact: Optional[Contact] = contact
        self.dtstart: Optional[DTStart] = dtstart
        self.dtend: Optional[DTEnd] = dtend
        self.organizer: Optional[Organizer] = organizer
        self.url: Optional[URL] = url

        # Optional, may occur more than once
        self.attendee: Optional[List[Attendee]] = attendee
        self.comment: Optional[List[Comment]] = comment
        self.freebusy: Optional[List[FreeBusyProperty]] = freebusy
        self.rstatus: Optional[List[RequestStatus]] = rstatus

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"VFreeBusy({self.dtstart.value if self.dtstart else ''}, {self.dtend.value if self.dtend else ''})"

    @property
    def dtstamp(self) -> DTStamp:
        """A getter to ensure the required property is set."""
        if self._dtstamp is None:
            raise MissingRequiredProperty(self, "dtstamp")
        return self._dtstamp

    @dtstamp.setter
    def dtstamp(self, value: DTStamp):
        """A setter to set the required property."""
        self._dtstamp = value

    @property
    def uid(self) -> UID:
        """A getter to ensure the required property is set."""
        if self._uid is None:
            raise MissingRequiredProperty(self, "uid")
        return self._uid

    @uid.setter
    def uid(self, value: UID):
        """A setter to set the required property."""
        self._uid = value
