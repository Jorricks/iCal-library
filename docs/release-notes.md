# Release Notes

## Latest Changes

## 0.0.1b0
- 🎨 Update name of package on Pypi
- 📝 Update buttons

## 0.0.1a1
- 📝 Update PyPi package description
- 🔧 Remove auto tagging pipeline

## 🚀 0.0.1a0 Initial release
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
