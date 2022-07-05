from typing import Dict, Optional, TYPE_CHECKING

from ical_reader.base_classes.base_class import ICalBaseClass
from ical_reader.ical_utils.lru_cache import instance_lru_cache

if TYPE_CHECKING:
    from ical_reader.base_classes.component import Component


class Property(ICalBaseClass):
    """
    This is the base class for any property (according to the RFC 5545 specification) in ical-reader.

    A property always exists of three parts:
    - The name of the property
    - The property parameters, this is optional and does not need to be present
    - The value of the property

    A line containing a property typically has the following format:
    PROPERTY-NAME;parameterKey=parameterValue,anotherParameterKey=anotherValue:actual-value
    """

    def __init__(self, parent: "Component", name: str, property_parameters: Optional[str], value: Optional[str]):
        """
        Instantiate a Property class.
        :param parent: Instance of the :class:`Component` it is a part of.
        :param name: The properties name, e.g. `RRULE`.
        :param property_parameters: The property parameters for this definition.
        :param value: The value of the property.
        """
        self._parent: "Component" = parent
        self._name: str = name
        self._property_parameters: Optional[str] = property_parameters
        self._value: Optional[str] = value

    @property
    def parent(self) -> "Component":
        """Return the instance of the :class:`Component` it is a part of."""
        return self._parent

    @property
    def name(self) -> str:
        """Return the name of the property."""
        return self._name

    @property
    @instance_lru_cache()
    def property_parameters(self) -> Dict[str, str]:
        """
        Return (and cache) all the property's parameters as a dictionary of strings.

        Note: When the instance is collected by the garbage collection, the cache is automatically deleted as well.

        :return: all the property's parameters as a dictionary of strings
        """
        property_parameters_str = self._property_parameters or ""
        return {
            key_and_value.split("=")[0]: key_and_value.split("=")[1]
            for key_and_value in property_parameters_str.split(",")
            if key_and_value.count("=") == 1
        }

    def has_property_parameter(self, key: str) -> Optional[bool]:
        """
        Return whether this property has a property parameter with a specific *key*.

        :param key: What key to search for.
        :return: boolean whether this property has a property parameter with a specific *key*.
        """
        return key in self.property_parameters

    def get_property_parameter(self, key: str) -> Optional[str]:
        """
        Get a property parameter's value with a specific key.

        :param key: The identifier of the property parameter.
        :return: The requested property parameter, or if that is not present, the default value.
        """
        return self.property_parameters.get(key, None)

    def get_property_parameter_default(self, key: str, default: str) -> str:
        """
        Get a property parameter's value with a specific key, where the default may not be None.

        :param key: The identifier of the property parameter.
        :param default: A value to return when the property parameter is not present, which may not be None.
        :return: The requested property parameter, or if that is not present, the default value.
        """
        return self.property_parameters.get(key, default)

    @property
    def value(self) -> Optional[str]:
        """Return the value of this property."""
        return self._value

    @property
    def as_original_string(self) -> str:
        """
        Return the iCalendar representation of the parameter.
        :return: the iCalendar string representation.
        """
        add_subs = f";{self._property_parameters.strip(';')}" if self._property_parameters else ""
        return f"{self._name}{add_subs}:{self._value}"
