from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ical_reader import Component


class ComponentContext:
    """
    Component context is used to keep the current Component when Component is used as ContextManager.

    You can use components as context: `#!py3 with Component() as my_component:`.

    If you do this the context stores the Component and whenever a new component or property is created, it will use
    such stored Component as the parent Component.
    """

    _context_managed_component: Optional["Component"] = None
    _previous_context_managed_components: List["Component"] = []

    @classmethod
    def push_context_managed_component(cls, component: "Component"):
        """Set the current context managed component."""
        if cls._context_managed_component:
            cls._previous_context_managed_components.append(cls._context_managed_component)
        cls._context_managed_component = component

    @classmethod
    def pop_context_managed_component(cls) -> Optional["Component"]:
        """Pop the current context managed component."""
        old_component = cls._context_managed_component
        if cls._previous_context_managed_components:
            cls._context_managed_component = cls._previous_context_managed_components.pop()
        else:
            cls._context_managed_component = None
        return old_component

    @classmethod
    def get_current_component(cls) -> Optional["Component"]:
        """Get the current context managed component."""
        return cls._context_managed_component
