import datetime

from dateutil.rrule import rrule, MONTHLY, weekday, WE, SU

# RRULE:FREQ=MONTHLY;UNTIL=20220614T215959Z;BYDAY=3WE
r = rrule(
    dtstart=datetime.datetime.utcnow() - datetime.timedelta(weeks=4),
    freq=MONTHLY,
    until=datetime.datetime.now(),
    byweekday=WE(3),
)
for dt in r:
    print(dt)
