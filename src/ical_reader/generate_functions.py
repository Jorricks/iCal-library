singular = {
    "dtstamp": "DTStamp",
    "uid": "Property",
    "dtstart": "DTStart",
    "ical_class": "Property",
    "created": "Created",
    "description": "Property",
    "geo": "GEO",
    "last_modified": "LastModified",
    "location": "Property",
    "organizer": "Organizer",
    "priority": "Priority",
    "sequence": "Sequence",
    "status": "Property",
    "summary": "Property",
    "transp": "Property",
    "url": "Property",
    "recurrence_id": "Property",
    "rrule": "RRule",
    "dtend": "DTEnd",
    "duration": "Duration",
}

multiple = {
    "attach": "Property",
    "attendee": "Attendee",
    "categories": "Property",
    "comment": "Property",
    "contact": "Property",
    "exdate": "Property",
    "rstatus": "Property",
    "related": "Property",
    "resources": "Property",
    "rdate": "Property",
}


for key, value_type in singular.items():
    print(
        f"""
    @property
    def {key}(self) -> {value_type}:
        tuple_values = self._singular_property_strs.get("{key.upper().replace('_', '-')}")
        return {value_type}(self, *tuple_values) 
""".strip("\n"), end="\n\n")


for key, value_type in multiple.items():
    print(
        f"""
    @property
    def {key}(self) -> List[{value_type}]:
        return [
            {value_type}(self, *tuple_values) 
            for tuple_values in self._property_multiple_strs.get("{key.upper().replace('_', '-')}")
        ]
""".strip("\n"), end="\n\n")






