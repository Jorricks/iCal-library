from ical_reader.base_classes.component import Component
from ical_reader.base_classes.property import Property
from ical_reader.ical_components import VCalendar, VEvent, VFreeBusy, VJournal, VTimeZone, VToDo
from ical_reader.ical_properties.pass_properties import ProdID, Version


def test_repr(calendar_instance):
    with calendar_instance:
        my_component = Component("MORTHY")
        my_component._extra_properties["prop"].append(Property(name="PROP", property_parameters=None, value="GHI"))
        assert repr(my_component) == "Component(prop=[Property(PROP:GHI)])"


def test_extra_child_components(calendar_instance):
    with calendar_instance:
        with Component("MORTHY", None) as my_component:
            component_1 = Component("RICK", None)
            component_2 = Component("SUMMER", None)
    assert my_component.extra_child_components == {
        "RICK": [component_1],
        "SUMMER": [component_2],
    }


def test_extra_properties(calendar_instance):
    my_component = Component("MORTHY", parent=calendar_instance)
    my_component.parse_property("RICK:SUMMER")
    assert set(my_component.properties.keys()) == {"rick"}
    print(dir(my_component.properties.values()))
    property = list(my_component.properties.values())[0][0]
    assert property.name == "RICK"
    assert property.value == "SUMMER"


def test_parent(calendar_instance):
    some_component = Component("SOME-COMPONENT", calendar_instance)
    assert some_component.parent is calendar_instance
    with calendar_instance:
        a = Property(name="PROP", value="bcdef")
        assert a.parent is calendar_instance


def test_children(calendar_with_all_components_once: VCalendar):
    assert len(calendar_with_all_components_once.children) == 6
    type_of_children = [type(child) for child in calendar_with_all_components_once.children]
    assert type_of_children == [VEvent, VToDo, VJournal, VFreeBusy, VTimeZone, Component]


def test_original_ical_text(calendar_with_all_components_once: VCalendar):
    assert (
        calendar_with_all_components_once.free_busy_list[0].original_ical_text
        == """
BEGIN:VFREEBUSY
UID:19970901T082949Z-FA43EF@example.com
ORGANIZER:mailto:jane_doe@example.com
ATTENDEE:mailto:john_public@example.com
DTSTART:19971015T050000Z
DTEND:19971016T050000Z
DTSTAMP:19970901T083000Z
END:VFREEBUSY
    """.strip()
    )


def test_properties(empty_calendar):
    version_property = Version(name="VERSION", value="1.1")
    empty_calendar.version = version_property
    some_other_property = Property(name="AWESOME", value="VALUE")
    empty_calendar._extra_properties["awesome"].append(some_other_property)
    assert empty_calendar.properties["awesome"] == [some_other_property]
    assert empty_calendar.properties["version"] == version_property
    assert set(empty_calendar.properties.keys()) == {
        "prodid",
        "version",
        "calscale",
        "method",
        "x_wr_caldesc",
        "x_wr_timezone",
        "x_wr_calname",
        "awesome",
    }


def test_print_tree_structure(capsys):
    root = VCalendar(prodid=ProdID(name="A", value="B"), version=Version(name="C", value="D"))
    an_event = VEvent(parent=root)
    a_journal = VJournal(parent=root)
    root.add_child(an_event)
    root.add_child(a_journal)
    root.print_tree_structure()
    captured = capsys.readouterr()
    assert captured.out == " - VCalendar(B, D)\n   - VEvent()\n   - VJournal(None: )\n"
