# Welcome to iCal Reader

**iCal Reader** is a Python library for anyone who wishes to read any iCalendar file.

It is the fastest iCalender python library out there and has excellent support for recurring events. Now there is truly no reason to miss an event, ever.

!!! info "This project is under active development."

    There are many items on which we can improve, please file an issue if you encounter any issue or have a feature request.

# Features
- Easy python interface. It's as simple as '`client.load_ics_file("<my_file>").timeline`' to show all your events of that week.
- Timeline support. Show exactly what is planned for a specific week.
- ***Fully functional*** support for recurring iCal components. E.g. Any recurring event will show up as intended within the timeline interface.
- Very fast parsing due to lazy evaluation of iCal properties.
- Debugger supported. Any issues? Open up a debugger and inspect all values.
- Minimal dependencies. Only `python-dateutil` and `pendulum`.


## Installation
To use iCal Reader, first install it using pip:

<!-- termynal -->
```
$ pip install ical-reader
---> 100%
Installed
```

## Usage
```python
from ical_reader import client

calendar = client.parse_icalendar_file("/home/user/my_icalendar.ics")
print(calendar.events)
print(calendar.todos)
print(calendar.journals)
print(calendar.free_busy_list)
print(calendar.time_zones)
```

When you are in an interactive interpreter, you can always call `help` to get more information about the instance at hand.
```text
>>> help(calendar)
Help on class VCalendar in module ical_reader.ical_components.v_calendar:
class VCalendar(ical_reader.base_classes.component.Component)
 |  VCalendar(name: str, parent: Union[ical_reader.base_classes.component.Component, NoneType], prodid: Union[ical_reader.ical_properties.pass_properties.ProdID, NoneType] = None, version: Union[ical_reader.ical_properties.pass_properties.Version, NoneType] = None, calscale: Union[ical_reader.ical_properties.pass_properties.CalScale, NoneType] = None, method: Union[ical_reader.ical_properties.pass_properties.Method, NoneType] = None, events: Union[List[ical_reader.ical_components.v_event.VEvent], NoneType] = None, todos: Union[List[ical_reader.ical_components.v_todo.VToDo], NoneType] = None, journals: Union[List[ical_reader.ical_components.v_journal.VJournal], NoneType] = None, free_busy_list: Union[List[ical_reader.ical_components.v_free_busy.VFreeBusy], NoneType] = None, time_zones: Union[List[ical_reader.ical_components.v_timezone.VTimeZone], NoneType] = None)
...
```

???+ info "During experimentation, it is recommended to use a Python Debugger."

    iCal Reader is fully Debugger compliant, meaning it is very easy to use a debugger with this project. It will be much faster to see all the different attributes and functions from inside a Python debugger. If you are unsure whether your IDE supports it, take a look [here](https://wiki.python.org/moin/PythonDebuggingTools) under the sections 'IDEs with Debug Capabilities'.

