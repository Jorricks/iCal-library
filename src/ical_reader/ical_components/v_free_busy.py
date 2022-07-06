from typing import List, Optional

from ical_reader.base_classes.component import Component
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

    :param name:
    :param parent:
    :param dtstamp:
    :param uid:
    :param contact:
    :param dtstart:
    :param dtend:
    :param organizer:
    :param url:
    :param attendee:
    :param comment:
    :param freebusy:
    :param rstatus:
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
        self.dtstamp: Optional[DTStamp] = dtstamp
        self.uid: Optional[UID] = uid

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
