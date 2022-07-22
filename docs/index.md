# iCal-library
<p align="center">
  <a href="https://jorricks.github.io/iCal-library"><img src="ical-library.png" alt="iCal-library" width="600px"></a>
</p>
<p align="center">
    <em>Fast, yet simple, iCalendar reader with excellent recurrence support. <a href="https://www.ietf.org/rfc/rfc5545.txt">RFC 5545</a> compliant.</em>
</p>
<p align="center">
<a href="https://github.com/Jorricks/iCal-library/actions/workflows/validate.yml" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/Jorricks/iCal-library/Validate" alt="GitHub Workflow Test Status">
</a>
<a href="https://codecov.io/gh/Jorricks/iCal-library" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/Jorricks/iCal-library/main" alt="Coverage">
</a>
</p>

---

**Documentation**: [https://jorricks.github.io/iCal-library/](https://jorricks.github.io/iCal-library/)

**Source Code**: [https://github.com/Jorricks/iCal-library](https://github.com/Jorricks/iCal-library)

---

**iCal-library** is a Python library for anyone who wishes to read any iCalendar file.

It is one of the fastest iCalender python library out there and has excellent support for recurring events. Now there is truly no reason to miss an event, ever.

!!! info "This project is under active development."

    You may encounter items on which we can improve, please file an issue if you encounter any issue or create a feature request for any missing feature.

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


## Installation
To use iCal-library, first install it using pip:

<!-- termynal -->
```
$ pip install iCal-library
---> 100%
Installed
```


## Requirements
Python 3.8+

iCal-library uses two major libraries for their date and time utilities:
- [Pendulum](https://github.com/sdispater/pendulum) for its extensions on datetime objects and parsing of durations.
- [Python-Dateutil](https://github.com/dateutil/dateutil) for its RRule support.


## Example
A simple example. Please look [in the docs](https://jorricks.github.io/iCal-library/) for more examples.

```python
from ical_library import client

calendar = client.parse_icalendar_file("/home/user/my_icalendar.ics")
print(calendar.events)
print(calendar.todos)
print(calendar.journals)
print(calendar.free_busy_list)
print(calendar.time_zones)
```


???+ info "During experimentation, it is recommended to use a Python Debugger."

    iCal-library is fully Debugger compliant, meaning it is very easy to use a debugger with this project. It will be much faster to see all the different attributes and functions from inside a Python debugger. If you are unsure whether your IDE supports it, take a look [here](https://wiki.python.org/moin/PythonDebuggingTools) under the sections 'IDEs with Debug Capabilities'.


## Limitations
- Currently, it is not supported to write ICS files. If this is a deal-breaker for you, it should be relatively straight forward to add it, so please consider submitting a PR for this :).
