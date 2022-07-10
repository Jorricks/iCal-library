from ical_reader.base_classes.base_class import ICalBaseClass
from ical_reader.base_classes.component import Component
from ical_reader.ical_components import VCalendar
from ical_reader.ical_properties.dt import RecurrenceID


def test_name():
    assert ICalBaseClass(name="ABC", parent=None).name == "ABC"


def test_parent():
    another_component = Component("ANOTHER-COMPONENT", None)
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
