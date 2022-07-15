from typing import List, Optional

from ical_library.base_classes.component import Component
from ical_library.exceptions import MissingRequiredProperty
from ical_library.help_modules.timespan import TimespanWithParent
from ical_library.ical_properties.cal_address import Attendee, Organizer
from ical_library.ical_properties.dt import DTEnd, DTStamp, DTStart
from ical_library.ical_properties.pass_properties import Comment, Contact, RequestStatus, UID, URL
from ical_library.ical_properties.periods import FreeBusyProperty


class VFreeBusy(Component):
    """
    This class represents the VFREEBUSY component specified in RFC 5545 in '3.6.4. Free/Busy Component'.

    A "VFREEBUSY" calendar component is a grouping of component properties that represents either a request for free
    or busy time information, a reply to a request for free or busy time information, or a published set of busy time
    information.

    :param name: The actual name of this component instance. E.g. VEVENT, RRULE, VCUSTOMCOMPONENT.
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
    :param parent: The Component this item is encapsulated by in the iCalendar data file.
    """

    def __init__(
        self,
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
        parent: Optional[Component] = None,
    ):
        super().__init__("VFREEBUSY", parent=parent)

        # Required
        self._dtstamp: Optional[DTStamp] = self.as_parent(dtstamp)
        self._uid: Optional[UID] = self.as_parent(uid)

        # Optional, may only occur once
        self.contact: Optional[Contact] = self.as_parent(contact)
        self.dtstart: Optional[DTStart] = self.as_parent(dtstart)
        self.dtend: Optional[DTEnd] = self.as_parent(dtend)
        self.organizer: Optional[Organizer] = self.as_parent(organizer)
        self.url: Optional[URL] = self.as_parent(url)

        # Optional, may occur more than once
        self.attendee: Optional[List[Attendee]] = self.as_parent(attendee)
        self.comment: Optional[List[Comment]] = self.as_parent(comment)
        self.freebusy: Optional[List[FreeBusyProperty]] = self.as_parent(freebusy)
        self.rstatus: Optional[List[RequestStatus]] = self.as_parent(rstatus)

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

    @property
    def timespan(self) -> Optional[TimespanWithParent]:
        start = self.dtstart.datetime_or_date_value if self.dtstart else None
        end = self.dtend.datetime_or_date_value if self.dtend else None
        if start is None:
            return None
        if end is None:
            TimespanWithParent(parent=self, begin=start, end=start)
        return TimespanWithParent(parent=self, begin=start, end=end)
