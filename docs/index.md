# iCalLibrary
<p align="center">
  <a href="https://jorricks.github.io/ical-reader"><img src="icallibrary.png" alt="iCalLibrary" width="600px"></a>
</p>
<p align="center">
    <em>Fast, yet simple, iCalendar reader&writer with excellent recurrence support. <a href="https://www.ietf.org/rfc/rfc5545.txt">RFC 5545</a> compliant.</em>
</p>
<p align="center">
<a href="https://github.com/Jorricks/ical-reader/actions/workflows/validate.yml" target="_blank">
    <img src="https://github.com/Jorricks/ical-reader/actions/workflows/validate.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/Jorricks/ical-reader" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/Jorricks/ical-reader/main" alt="Coverage">
</a>
</p>

---

**Documentation**: [https://jorricks.github.io/ical-reader/](https://jorricks.github.io/ical-reader/)

**Source Code**: [https://github.com/Jorricks/ical-reader](https://github.com/Jorricks/ical-reader)

---

**iCal Reader** is a Python library for anyone who wishes to read any iCalendar file.

It is one of the fastest iCalender python library out there and has excellent support for recurring events. Now there is truly no reason to miss an event, ever.

!!! info "This project is under active development."

    You may encounter items on which we can improve, please file an issue if you encounter any issue or create a feature request for any missing feature.

## Features
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


## Requirements
Python 3.8+

iCalLibrary uses two major libraries for their date and time utilities:
- [Pendulum](https://github.com/sdispater/pendulum) for its extensions on datetime objects and parsing of durations.
- [Python-Dateutil](https://github.com/dateutil/dateutil) for its RRule support.


## Example
A simple example. Please look [in the docs](https://jorricks.github.io/ical-reader/) for more examples.

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

    iCal Reader is fully Debugger compliant, meaning it is very easy to use a debugger with this project. It will be much faster to see all the different attributes and functions from inside a Python debugger. If you are unsure whether your IDE supports it, take a look [here](https://wiki.python.org/moin/PythonDebuggingTools) under the sections 'IDEs with Debug Capabilities'.


## Limitations
- Currently, it is not supported to write ICS files. If this is a deal-breaker for you, it should be relatively straight forward to add it, so please consider submitting a PR for this :).
