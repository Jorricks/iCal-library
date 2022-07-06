from typing import Optional

from ical_reader.base_classes.component import Component
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import Repeat
from ical_reader.ical_properties.pass_properties import Action, Attach
from ical_reader.ical_properties.trigger import Trigger


class VAlarm(Component):
    """
    This class represents the VAlarm component specified in RFC 5545 in '3.6.6. Alarm Component'.

    A "VALARM" calendar component is a grouping of component properties that is a reminder or alarm for an event or a
    to-do. For example, it may be used to define a reminder for a pending event or an overdue to-do.

    :param parent:
    :param action:
    :param trigger:
    :param duration:
    :param repeat:
    :param attach:
    """

    def __init__(
        self,
        parent: Optional[Component],
        action: Optional[Action] = None,
        trigger: Optional[Trigger] = None,
        duration: Optional[ICALDuration] = None,
        repeat: Optional[Repeat] = None,
        attach: Optional[Attach] = None,
    ):
        super().__init__("VALARM", parent)

        # Required
        self.action: Optional[Action] = action
        self.trigger: Optional[Trigger] = trigger

        # Both optional and may only occur once. But if one occurs, the other also has to occur.
        self.duration: Optional[ICALDuration] = duration
        self.repeat: Optional[Repeat] = repeat

        # Optional, may only occur once
        self.attach: Optional[Attach] = attach

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"VAlarm({self.action.value}: {self.trigger.value})"
