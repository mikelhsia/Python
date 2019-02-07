import datetime
from dateutil import tz
now = datetime.datetime.now()

time_zone = tz.gettz('Europe/Paris')
now.replace(tzinfo=time_zone)


from dateutil.zoneinfo import get_zonefile_instance
zones = list(get_zonefile_instance().zones)
print(sorted(zones)[:5])
print(len(zones))

# Getting name of the timezone
tz.gettz().tzname(datetime.datetime.now())