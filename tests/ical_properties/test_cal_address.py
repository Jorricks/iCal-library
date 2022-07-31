from ical_library.ical_properties.cal_address import _CalAddress


def test_cal_address():
    ca = _CalAddress(name="ORGANIZER", property_parameters="CN=John Smith", value="mailto:jsmith@example.com")
    assert ca.email == "jsmith@example.com"
    assert ca.persons_name == "John Smith"
