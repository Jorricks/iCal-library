from ical_library.base_classes.base_class import ICalBaseClass
from ical_library.base_classes.component import Component
from ical_library.ical_components import VCalendar
from ical_library.ical_properties.dt import RecurrenceID


def test_name(calendar_instance):
    assert ICalBaseClass(name="ABC", parent=calendar_instance).name == "ABC"


def test_parent(calendar_instance):
    another_component = Component(name="ANOTHER-COMPONENT", parent=calendar_instance)
    assert ICalBaseClass(name="ABC", parent=another_component).parent == another_component


def test_get_ical_name_of_class():
    class SomeRandomClass(ICalBaseClass):
        pass

    assert SomeRandomClass.get_ical_name_of_class() == "SOMERANDOMCLASS"

    class SomeOtherClass(ICalBaseClass):
        pass

    assert SomeOtherClass.get_ical_name_of_class() == "SOMEOTHERCLASS"
    assert VCalendar.get_ical_name_of_class() == "VCALENDAR"
    assert RecurrenceID.get_ical_name_of_class() == "RECURRENCE-ID"
