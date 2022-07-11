# ICal Reader - Fast, yet simple, iCalendar reader with excellent recurrence support

The ICal reader module provides easy access to iCalenders with full support for recurring events, following the [RFC 5545](https://www.ietf.org/rfc/rfc5545.txt), available in Python.


## Installation

ical-reader can be installed from PyPI using pip (note that the package name is different from the importable name)::

    pip install ical-reader


## Quick start
A simple example. Please look into the docs for more examples.
```python3
from ical_reader import client

calendar = client.parse_icalendar_file("/home/user/my_icalendar.ics")
print(calendar.events)
print(calendar.todos)
print(calendar.journals)
print(calendar.free_busy_list)
print(calendar.time_zones)
```

## Features

- Easy python interface. It's as simple as '`client.parse_icalendar_file("<my_file>").timeline`' to show all your events.
- Timeline support. Show exactly what is planned for a specific period.
- ***Fully functional*** support for recurring iCalender components. E.g. Any recurring event will show up as intended within the timeline interface.
- Very fast parsing due to lazy evaluation of iCalender properties.
- Debugger supported. Any issues? Or just wondering what operations are supported? Open up a debugger and inspect all values.
- Minimal dependencies. Only `python-dateutil` and `pendulum`.

#### Limitations
- Currently, it is not supported to write ICS files. If this is a deal-breaker for you, it should be relatively straight forward to add it, so please consider adding a PR for this :).

###  Why yet another iCalendar library?

I first tried several libraries for iCalendar events. However, none of them supported recurring events as well as they should be. For some libraries my calendar loaded but then didn't show my recurring events, while others simply threw stacktraces trying to load it. Furthermore, I noticed that my calendar (with over 2000 events) took ages to load.
After traversing the code of the other libraries I decided I wanted to build my own. With some key principles:
- Recurring components should be the main priority to get working.
- No strict evaluation that could lead to errors while parsing the file.
- Lazy evaluation for iCalendar properties to speed up the process.

## ToDo
- Create badges like python-dateutil.
- Implement timeline functionality for all items instead of just VEvents.
- Fix the timeline & expanding functionality to use intersect.
- Implement a context manager (like Airflow DAGs) for Components.
- Implement support for quoted property parameters.
- Implement support for the new Properties for iCalendar (RFC 7986)

