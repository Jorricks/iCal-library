from typing import Optional

from ical_library.base_classes.component import Component
from ical_library.exceptions import MissingRequiredProperty
from ical_library.ical_properties.ical_duration import ICALDuration
from ical_library.ical_properties.ints import Repeat
from ical_library.ical_properties.pass_properties import Action, Attach
from ical_library.ical_properties.trigger import Trigger


class VAlarm(Component):
    """
    This class represents the VAlarm component specified in RFC 5545 in '3.6.6. Alarm Component'.

    A "VALARM" calendar component is a grouping of component properties that is a reminder or alarm for an event or a
    to-do. For example, it may be used to define a reminder for a pending event or an overdue to-do.
    The "VALARM" calendar component MUST only appear within either a "VEVENT" or "VTODO" calendar component

    :param action: The Action property. Required and must occur exactly once.
    :param trigger: The Trigger property. Required and must occur exactly once.
    :param duration: The ICALDuration property. Optional, but may occur at most once. If this item is
        present, repeat may not be present.
    :param repeat: The Repeat property. Optional, but may occur at most once. If this item is
        present, duration may not be present.
    :param attach: The Attach property. Optional, but may occur at most once.
    :param parent: The Component this item is encapsulated by in the iCalendar data file.
    """

    def __init__(
        self,
        action: Optional[Action] = None,
        trigger: Optional[Trigger] = None,
        duration: Optional[ICALDuration] = None,
        repeat: Optional[Repeat] = None,
        attach: Optional[Attach] = None,
        parent: Optional[Component] = None,
    ):
        super().__init__("VALARM", parent=parent)

        # Required
        self._action: Optional[Action] = self.as_parent(action)
        self._trigger: Optional[Trigger] = self.as_parent(trigger)

        # Both optional and may only occur once. But if one occurs, the other also has to occur.
        self.duration: Optional[ICALDuration] = self.as_parent(duration)
        self.repeat: Optional[Repeat] = self.as_parent(repeat)

        # Optional, may only occur once
        self.attach: Optional[Attach] = self.as_parent(attach)

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
