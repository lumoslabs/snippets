import datetime

class Pacific_tzinfo(datetime.tzinfo):
    """Implementation of the Pacific timezone.

    Adapted from http://code.google.com/appengine/docs/python/datastore/typesandpropertyclasses.html
    """
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def _FirstSunday(self, dt):
        """First Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        # 2 am on the second Sunday in March
        dst_start = self._FirstSunday(datetime.datetime(dt.year, 3, 8, 2))
        # 1 am on the first Sunday in November
        dst_end = self._FirstSunday(datetime.datetime(dt.year, 11, 1, 1))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)

    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "PST"
        else:
            return "PDT"


TARGET_WEEKDAY = 4 # Friday

def date_for_new_snippet():
    """Return next Friday, unless it is Friday, Saturday, or Sunday"""
    today = datetime.datetime.now(Pacific_tzinfo()).date()
    weekday = today.weekday()
    if (weekday >= TARGET_WEEKDAY):
        aligned = today - datetime.timedelta(days=(today.weekday() - TARGET_WEEKDAY))
    else:
        aligned = today + datetime.timedelta(days=((7 - today.weekday() - TARGET_WEEKDAY)+1))
    return aligned


def date_for_retrieval():
    """Always return the most recent Friday.

    Note that this can be today.
    """
    today = datetime.datetime.now(Pacific_tzinfo()).date()
    if (today.weekday() == TARGET_WEEKDAY):
        return today
    else:
        return today - datetime.timedelta(days=(today.weekday() + TARGET_WEEKDAY - 1))
