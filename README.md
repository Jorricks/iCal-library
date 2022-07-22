<p align="center">
  <a href="https://jorricks.github.io/iCal-library"><img src="docs/ical-library.png" alt="iCal-library" width="600px"></a>
</p>
<p align="center">
    <em>Fast, yet simple, iCalendar reader with excellent recurrence support. <a href="https://www.ietf.org/rfc/rfc5545.txt">RFC 5545</a> compliant.</em>
</p>
<p align="center">
<a href="https://github.com/Jorricks/iCal-library/actions/workflows/validate.yml" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/Jorricks/iCal-library/Validate" alt="GitHub Workflow Test Status" >
</a>
<a href="https://codecov.io/gh/Jorricks/iCal-library" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/Jorricks/iCal-library/main" alt="Coverage">
</a>
</p>

[//]: # (<a href="https://pypi.org/project/iCal-library" target="_blank">)
[//]: # (    <img src="https://img.shields.io/pypi/v/iCal-library?color=%2334D058&label=pypi%20package" alt="Package version">)
[//]: # (</a>)
[//]: # (<a href="https://pypi.org/project/iCal-library" target="_blank">)
[//]: # (    <img src="https://img.shields.io/pypi/pyversions/iCal-library.svg?color=%2334D058" alt="Supported Python versions">)
[//]: # (</a>)

---

**Documentation**: [https://jorricks.github.io/iCal-library/](https://jorricks.github.io/iCal-library/)

**Source Code**: [https://github.com/Jorricks/iCal-library](https://github.com/Jorricks/iCal-library)


## Features
- Easy python interface. It's as simple as '`client.load_ics_file("<my_file>").timeline`' to show all your events of that week.
- Timeline support. Show exactly what is planned for a specific week.
- ***Fully functional*** support for recurring iCal components. E.g. Any recurring event will show up as intended within the timeline interface. This includes:
  - Recurring components/events based on RRule.
  - Recurring components/events based on RDate.
  - Excluding components/events based on EXDate.
  - Any combination of the above three.
  - Redefined/changed components/events correctly show the latest version. 
- Very fast parsing due to lazy evaluation of iCal properties.
- Debugger supported. Any issues? Open up a debugger and inspect all values.
- Minimal dependencies. Only `python-dateutil` and `pendulum`.
- Fully typed code base.


## Requirements
Python 3.8+

iCal-library uses two major libraries for their date and time utilities:
- [Pendulum](https://github.com/sdispater/pendulum) for its extensions on datetime objects and parsing of durations.
- [Python-Dateutil](https://github.com/dateutil/dateutil) for its RRule support.


## Installation

To use iCal-library, first install it using pip:

    pip install iCal-library


## Example
A simple example. Please look [in the docs](https://jorricks.github.io/iCal-library/) for more examples.

```python3
from ical_library import client

calendar = client.parse_icalendar_file("/home/user/my_icalendar.ics")
print(calendar.events)
print(calendar.todos)
print(calendar.journals)
print(calendar.free_busy_list)
print(calendar.time_zones)
```

Note: iCal-library is fully Debugger compliant, meaning it is very easy to use a debugger with this project. It will be much faster to see all the different attributes and functions from inside a Python debugger. If you are unsure whether your IDE supports it, take a look [here](https://wiki.python.org/moin/PythonDebuggingTools) under the sections 'IDEs with Debug Capabilities'.


## Limitations
- Currently, it is not supported to write ICS files. If this is a deal-breaker for you, it should be relatively straight forward to add it, so please consider submitting a PR for this :). However, this will be added shortly!


##  Why yet another iCalendar library?

I first tried several libraries for iCalendar events. However, none of them supported recurring events as well as they should be. For some libraries my calendar loaded but then didn't show my recurring events, while others simply threw stacktraces trying to load it. Furthermore, I noticed that my calendar (with over 2000 events) took ages to load.
After traversing the code of the other libraries I decided I wanted to build my own. With some key principles:
- Recurring components should be the main priority to get working.
- No strict evaluation that could lead to errors while parsing the file.
- Lazy evaluation for iCalendar properties to speed up the process.

## Ideas for additional features
- Support quoted property parameters containing special characters.
- Support the new Properties for iCalendar (RFC 7986).
- Support CalDev (RFC 4791).

