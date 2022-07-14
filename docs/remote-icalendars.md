# Remote iCalendars
Here are some more in-depth use-cases 

## Integration status.
- Google Calendar: :material-check:. Works with private and public calendars. Also works when you are part of an organisation that does not allow plugins.
- Microsoft Outlook: :material-check:. Requires you to make your calendar public.
- Apple Calendar: :octicons-question-16:. Unable to find any info on how to make calendars public.

## Getting the iCalendar URL for remote calendars.
Before we can actually load in the data of your calendar, we need to get the iCalendar URL.
The steps are different per host, some of them are listed here:

- Google Calendar: ["Getting your secret address in iCal format"](https://support.google.com/calendar/answer/37648?hl=en#zippy=%2Cget-your-calendar-view-only)
- Microsoft Outlook: ["Publish your Calendar"]("https://support.microsoft.com/en-us/office/share-your-calendar-in-outlook-on-the-web-7ecef8ae-139c-40d9-bae2-a23977ee58d5")

!!! info 

    This package is actively tested with Google iCalendars.
    If you have any other calendars and encounter odd behaviour, please file a Github feature request or a Github Issue.

## Reading your iCalendar from a remote place

1. Follow one of the above-mentioned tutorial to get the iCalendar URL.
2. Verify that when you open the URL in your browser, it shows a page or downloads a file that begins with `BEGIN:VCALENDAR`.
3. Use the `client.parse_icalendar_url()` to get it directly.

```python
from ical_library import client

calendar = client.parse_icalendar_url("https://calendar.google.com/calendar/ical/xxxxxx/private-xxxxxx/basic.ics")
print(calendar.events)
```

## Reading your iCalendar from a remote place with rate limiting
To help you avoid doing unnecessary requests to your iCalendar provider, there is a `CacheClient`.
This helps you cache the result on a location on your Hard Drive to avoid the need to fetch it every time you restart
your application.

```python
from pathlib import Path
from pendulum import Duration
from ical_library.cache_client import CacheClient

cache_client = CacheClient(
    url="https://calendar.google.com/calendar/ical/xxxxxx/private-xxxxxx/basic.ics",
    cache_location=Path.home() / "ical-reader-cache",
    cache_ttl=Duration(hours=1),
    verbose=True,
)
calendar = cache_client.get_icalendar()
print(calendar.events)
```


!!! info 

    If you have a production use-case for a 24/7 running service, you might be better of doing the caching/rate-limiting
    in your service. 
