from dataclasses import dataclass
from typing import List, Optional

from ical_reader.base_classes.component import Component
from ical_reader.ical_properties.cal_address import Attendee, Organizer
from ical_reader.ical_properties.dt import DTEnd, DTStamp, DTStart
from ical_reader.ical_properties.pass_properties import Comment, Contact, RStatus, UID, URL
from ical_reader.ical_properties.periods import FreeBusyProperty


@dataclass
class VFreeBusy(Component):
    """This class represents the VFREEBUSY component specified in RFC 5545 in '3.6.4. Free/Busy Component'."""

    # Required
    dtstamp: Optional[DTStamp] = None
    uid: Optional[UID] = None

    # Optional, may only occur once
    contact: Optional[Contact] = None
    dtstart: Optional[DTStart] = None
    dtend: Optional[DTEnd] = None
    organizer: Optional[Organizer] = None
    url: Optional[URL] = None

    # Optional, may occur more than once
    attendee: Optional[List[Attendee]] = None
    comment: Optional[List[Comment]] = None
    freebusy: Optional[List[FreeBusyProperty]] = None
    rstatus: Optional[List[RStatus]] = None
