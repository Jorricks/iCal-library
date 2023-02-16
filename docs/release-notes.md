# Release Notes

## 0.2.2 BugFix release
This is a minor release to solve a critical bug.
It occurred when it is expanding a recurring event with a start date in dates for a range defined by dates.
- 🐛 RRule expansion failing where event.start_date==return_range.start.

## 0.2.1 Documentation update
A minor update to improve documentation:
- 📝 Remove workflow badge
- ⬆️ Add Python 3.11 & 3.12 support

## 0.2.0 Release to improve timezone offset changes support
This release contains some bugfixes and a major improvement to also support timezone offset changes over time.
Thereby, recurring events for timezones that have Daylight saving time now correctly change according to the VTIMEZONE definition.
Furthermore, EXDATE (so excluding a single occurrence from a recurring event) now correctly handles timezones. Previously it did not exclude EXDATE's with a Timezone correctly. This release fixes that.

- ✨ Support offset changes in a sequence of recurring events.
- 🐛 Return only recurring items in Timespan range.
- 🐛 EXDate now takes TZID into account.
- 📝 Make pipeline name more generic.

## 0.1.0 Code structure release
This release mostly contains general improvements to the code base with some minor bugfixes.

- 📝 Add emoji to features docs.
- ✅ Add tests for CalAddress.
- 🐛 Defaultlist gave None when using `.get`.
- 🐛 Function arg date type should match other arg.
- 🐛 Remove unwanted commented code.
- 🐛 Remove unwanted print.
- 🎨 Update name of package on Pypi.
- 📝 Update buttons.

## 0.0.1a1 BugFix release
This release contains some updates to the release process.

- 📝 Update PyPi package description.
- 🔧 Remove auto tagging pipeline.

## 🚀 0.0.1a0 Initial release
The initial release of the package. Some turbulence expected.

- ✅ Easy python interface. It's as simple as '`client.load_ics_file("<my_file>").timeline`' to show all your events of that week.
- 📈 Timeline support. Show exactly what is planned for a specific week.
- 👌 ***Fully functional*** support for recurring iCal components. E.g. Any recurring event will show up as intended within the timeline interface. This includes:
  - Recurring components/events based on RRule.
  - Recurring components/events based on RDate.
  - Excluding components/events based on EXDate.
  - Any combination of the above three.
  - Redefined/changed components/events correctly show the latest version. 
- ⚡️ Very fast parsing due to lazy evaluation of iCal properties.
- ✨ Debugger supported. Any issues? Open up a debugger and inspect all values.
- 🔥 Minimal dependencies. Only `python-dateutil` and `pendulum`.
- 📝 Fully documented code base.
- 🏷️ Fully typed code base.
