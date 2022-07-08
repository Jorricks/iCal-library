from typing import Optional

from ical_reader.base_classes.component import Component
from ical_reader.exceptions import MissingRequiredProperty
from ical_reader.ical_properties.ical_duration import ICALDuration
from ical_reader.ical_properties.ints import Repeat
from ical_reader.ical_properties.pass_properties import Action, Attach
from ical_reader.ical_properties.trigger import Trigger


class VAlarm(Component):
    """
    This class represents the VAlarm component specified in RFC 5545 in '3.6.6. Alarm Component'.

    A "VALARM" calendar component is a grouping of component properties that is a reminder or alarm for an event or a
    to-do. For example, it may be used to define a reminder for a pending event or an overdue to-do.

    :param parent: The Component this item is encapsulated by in the iCalendar data file.
    :param action: The Action property. Required and must occur exactly once.
    :param trigger: The Trigger property. Required and must occur exactly once.
    :param duration: The ICALDuration property. Optional, but may occur at most once. If this item is
        present, repeat may not be present.
    :param repeat: The Repeat property. Optional, but may occur at most once. If this item is
        present, duration may not be present.
    :param attach: The Attach property. Optional, but may occur at most once.
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
        self._action: Optional[Action] = action
        self._trigger: Optional[Trigger] = trigger

        # Both optional and may only occur once. But if one occurs, the other also has to occur.
        self.duration: Optional[ICALDuration] = duration
        self.repeat: Optional[Repeat] = repeat

        # Optional, may only occur once
        self.attach: Optional[Attach] = attach

    def __repr__(self) -> str:
        """Overwrite the repr to create a better representation for the item."""
        return f"VAlarm({self.action.value}: {self.trigger.value})"

    @property
    def action(self) -> Action:
        """A getter to ensure the required property is set."""
        if self._action is None:
            raise MissingRequiredProperty(self, "action")
        return self._action

    @action.setter
    def action(self, value: Action):
        """A setter to set the required property."""
        self._action = value

    @property
    def trigger(self) -> Trigger:
        """Getter that ensures the required property is set."""
        if self._trigger is None:
            raise MissingRequiredProperty(self, "trigger")
        return self._trigger

    @trigger.setter
    def trigger(self, value: Trigger):
        """A setter to set the required property."""
        self._trigger = value
