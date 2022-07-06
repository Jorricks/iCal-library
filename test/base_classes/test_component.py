from ical_reader.base_classes.component import Component
from ical_reader.base_classes.property import Property
from ical_reader.ical_components.v_calendar import VCalendar
from ical_reader.ical_components.v_event import VEvent


def test_repr():
    my_component = Component("MORTHY", None)
    my_component._extra_properties["prop"].append(Property(my_component, "PROP", None, "GHI"))
    assert repr(my_component) == "Component(prop=[Property(PROP:GHI)])"


def test_extra_child_components():
    my_component = Component("MORTHY", None)
    component_1 = Component("RICK", None)
    component_2 = Component("SUMMER", None)
    my_component.add_child(component_1)
    my_component.add_child(component_2)
    assert my_component.extra_child_components == {
        "RICK": [component_1],
        "SUMMER": [component_2],
    }


def test_extra_properties():
    my_component = Component("MORTHY", None)
    my_component.parse_property("RICK:SUMMER")
    assert set(my_component.properties.keys()) == {"RICK"}
    print(dir(my_component.properties.values()))
    property = list(my_component.properties.values())[0][0]
    assert property.name == "RICK"
    assert property.value == "SUMMER"


def test_parent():
    root_component = Component("ROOT-COMPONENT", None)
    some_component = Component("SOME-COMPONENT", root_component)
    assert some_component.parent == root_component


def test_children():
    root_component = VCalendar(parent=None)
    an_event = VEvent(parent=root_component)
    some_component = Component("SOME-COMPONENT", root_component)
    root_component.add_child(an_event)
    root_component.add_child(some_component)
    assert len(root_component.children) == 2
    assert root_component.children == (an_event, some_component)
