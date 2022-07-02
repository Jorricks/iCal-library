import dataclasses
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from typing import (
    ClassVar,
    Dict,
    get_args,
    get_origin,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TYPE_CHECKING,
    TypeVar,
    Union,
)

from ical_reader.base_classes.base_class import ICalBaseClass
from ical_reader.base_classes.property import Property

if TYPE_CHECKING:
    from ical_reader.ical_components.v_calendar import VCalendar


T = TypeVar("T")


@dataclass(repr=False)
class Component(ICalBaseClass):
    """
    This is the base class for any component (according to the RFC 5545 specification) in ical-reader.

    Inside all components (so also all classes inheriting this class, e.g. VEvent) there are four kind of variables:
    - variables that start with _. These are specific to the class and not directly related to a property or
     component from iCalendar.
    - variables that have a type of List[x] and a default value of List. These are child components/properties of
    the instance. These components/properties may or may not be required to be present in the iCal file.
    - variables that have a type of Optional[List[x]]. These are components/properties of the instance.
    They can be either optional or required and may occur multiple times in the iCal file.
    - variables that have a type of Optional[x] (and not Optional[List[x]]). These are properties of the instance.
    They can be either optional or required, but may only occur once in the iCal file.
    """

    _name: Optional[str] = None
    _parent: Optional["Component"] = None
    _extra_child_components: Dict[str, List["Component"]] = field(default_factory=lambda: defaultdict(list))
    _extra_properties: Dict[str, List[Property]] = field(default_factory=lambda: defaultdict(list))
    _parse_line_start: Optional[int] = 0
    _parse_line_end: Optional[int] = 0

    def __repr__(self):
        properties_as_string = ", ".join([f"{name}={value}" for name, value in self.properties.items()])
        return f"{self.__class__.__name__}({properties_as_string})"

    @property
    def name(self):
        return self._name

    @property
    def extra_child_components(self) -> Dict[str, List["Component"]]:
        return self._extra_child_components

    @property
    def extra_properties(self) -> Dict[str, List[Property]]:
        return self._extra_properties

    @property
    def parent(self) -> Optional["Component"]:
        return self._parent

    def set_parent(self, parent: "Component") -> None:
        if self._parent is not None:
            raise ValueError(f"Can not overwrite the parent of {self} to {parent=}")
        self._parent = parent

    @property
    def tree_root(self) -> "VCalendar":
        from ical_reader.ical_components.v_calendar import VCalendar

        instance = self
        while instance.parent is not None:
            instance = instance.parent
        if not isinstance(instance, VCalendar):
            raise TypeError(f"Invalid TreeRoot as it was of type {type(instance)=} instead of VCalendar.")
        return instance

    @property
    def children(self) -> List["Component"]:
        children = [child for list_of_children in self._extra_child_components.values() for child in list_of_children]
        children.extend(
            item_in_list
            for ical_name, (var_name, var_type, is_list) in self._get_child_component_mapping().items()
            for item_in_list in getattr(self, var_name)
        )
        return children

    def add_child(self, child: "Component") -> None:
        child.set_parent(self)
        child_component_mapping = self._get_child_component_mapping()
        if child._name in child_component_mapping:
            var_name, var_type, is_list = child_component_mapping[child._name]
            getattr(self, var_name).append(child)
            return
        self._extra_child_components[child._name].append(child)

    @property
    def original_ical_text(self) -> str:
        return self.tree_root.get_original_ical_text(self._parse_line_start, self._parse_line_end)

    @classmethod
    @lru_cache()
    def _get_property_attributes(cls) -> Set[str]:
        return {var_name for var_name, var_type, is_list in cls._get_property_mapping_2().values()}

    @staticmethod
    def _extract_ical_class_from_args(var_name: str, a_type: Union[Type[List], type(Union)]) -> Type:
        sub_types: List[Type] = [st for st in get_args(a_type) if not issubclass(get_origin(st) or st, type(None))]
        if len(sub_types) != 1:
            raise TypeError(f"Incorrect number of sub_types to follow here for {var_name=}, {a_type=}, {sub_types=}.")
        return sub_types[0]

    @staticmethod
    def _extract_type_information(
        var_name: str, a_type: Type, is_in_list: bool
    ) -> Optional[Tuple[str, Tuple[str, Optional[Type[ICalBaseClass]], bool]]]:
        if get_origin(a_type) is None:
            if issubclass(a_type, ICalBaseClass):
                return a_type.get_ical_name_of_class(), (var_name, a_type, is_in_list)
            return None
        elif get_origin(a_type) == Union:  # This also covers the Optional case.
            sub_class = Component._extract_ical_class_from_args(var_name, a_type)
            return Component._extract_type_information(var_name, sub_class, is_in_list)
        elif issubclass(get_origin(a_type), List):
            sub_class = Component._extract_ical_class_from_args(var_name, a_type)
            return Component._extract_type_information(var_name, sub_class, True)
        elif get_origin(a_type) == ClassVar:
            return None
        else:
            raise TypeError(f"Unknown type '{a_type}' came by in Component.extract_custom_type.")

    @classmethod
    @lru_cache()
    def _get_var_mapping(cls) -> Mapping[str, Tuple[str, Type[ICalBaseClass], bool]]:
        var_mapping: Dict[str, Tuple[str, Type[ICalBaseClass], bool]] = {}
        for a_field in dataclasses.fields(cls):
            if a_field.name.startswith("_"):
                continue
            result = Component._extract_type_information(a_field.name, a_field.type, False)
            if result is None:
                continue
            ical_name, var_type_info = result
            if issubclass(var_type_info[1], ICalBaseClass):
                var_mapping[ical_name] = var_type_info
        return var_mapping

    @classmethod
    @lru_cache()
    def _get_property_mapping_2(cls) -> Mapping[str, Tuple[str, Type[Property], bool]]:
        return {
            ical_name: var_tuple
            for ical_name, var_tuple in cls._get_var_mapping().items()
            if issubclass(var_tuple[1], Property)
        }

    @classmethod
    @lru_cache()
    def _get_child_component_mapping(cls) -> Mapping[str, Tuple[str, Type["Component"], bool]]:
        return {
            ical_name: var_tuple
            for ical_name, var_tuple in cls._get_var_mapping().items()
            if issubclass(var_tuple[1], Component)
        }

    @property
    def properties(self) -> Dict[str, Union[Property, List[Property]]]:
        standard_properties = {
            var_name: getattr(self, var_name)
            for var_name, var_type, is_list in self._get_property_mapping_2().values()
            if getattr(self, var_name) is not None
        }
        return {**standard_properties, **self._extra_properties}

    def print_tree_structure(self, indent: int = 0):
        print(f"{'  ' * indent} - {self}")
        for child in self.children:
            child.print_tree_structure(indent=indent + 1)

    def parse_property(self, line: str) -> None:
        """
        Parse a line containing a Property definition.

        Credits for the excellent regex parsing string go to @Jan Goyvaerts: https://stackoverflow.com/a/2482067/2277445
        """
        property_mapping = self._get_property_mapping_2()
        result = re.search("([^\r\n;:]+)(;[^\r\n:]+)?:(.*)", line)
        if result is None:
            raise ValueError(f"{result=} should never be None!")
        name, property_parameters, value = result.group(1), result.group(2), result.group(3)
        if name in property_mapping.keys():
            var_name, var_type, is_list = property_mapping[name]
            if is_list:
                property_instance = var_type(
                    parent=self, name=name, property_parameters=property_parameters, value=value
                )
                if getattr(self, var_name) is None:
                    setattr(self, var_name, [property_instance])
                else:
                    current_value: List[Property] = getattr(self, var_name)
                    current_value.append(property_instance)
            else:
                property_instance = var_type(
                    parent=self, name=name, property_parameters=property_parameters, value=value
                )
                setattr(self, var_name, property_instance)
        else:
            pythonic_name = name.lower().replace("-", "_")
            property_instance = Property(parent=self, name=name, property_parameters=property_parameters, value=value)
            self._extra_properties[pythonic_name].append(property_instance)

    def parse_component_section(self, lines: List[str], line_number: int) -> int:
        self._parse_line_start = line_number - 1
        component_mapping = self._get_child_component_mapping()
        while not (current_line := lines[line_number]).startswith("END:"):
            line_number += 1
            if current_line.startswith("BEGIN:"):
                component_name = current_line[len("BEGIN:") :]
                if component_name in component_mapping:
                    var_name, var_type, is_list = component_mapping[component_name]
                    instance: "Component" = var_type()
                else:
                    instance: "Component" = Component()
                instance._name = component_name
                self.add_child(instance)
                line_number = instance.parse_component_section(lines=lines, line_number=line_number)
                continue

            full_line_without_line_breaks = current_line
            while (next_line := lines[line_number]).startswith(" "):
                line_number += 1
                # [1:] so we skip the space indicating a line break.
                full_line_without_line_breaks += next_line[1:]
            self.parse_property(full_line_without_line_breaks)

        if current_line != f"END:{self._name or self.get_ical_name_of_class()}":
            raise ValueError(f"Expected {current_line=} to be equal to END:{self.get_ical_name_of_class()}.")
        self._parse_line_end = line_number + 1
        return line_number + 1
