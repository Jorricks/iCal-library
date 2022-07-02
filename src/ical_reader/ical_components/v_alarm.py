from dataclasses import dataclass
from typing import Optional

from ical_reader.base_classes.component import Component
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.pass_properties import Action, Attach
from ical_reader.ical_properties.repeat import Repeat
from ical_reader.ical_properties.trigger import Trigger


@dataclass(repr=False)
class VAlarm(Component):
    """This class represents the VAlarm component specified in RFC 5545 in '3.6.6. Alarm Component'."""

    # @ToDo(jorrick) Check whether all these properties are actually named correctly.
    # @ToDo(jorrick) Either use the get_property_name or remove it. Preferably use it.
    # Required
    action: Optional[Action] = None
    trigger: Optional[Trigger] = None

    # Both optional and may only occur once. But if one occurs, the other also has to occur.
    duration: Optional[ICALDuration] = None
    repeat: Optional[Repeat] = None

    # Optional, may only occur once
    attach: Optional[Attach] = None

    def __repr__(self) -> str:
        return f"VAlarm({self.action.value}: {self.trigger.value})"
