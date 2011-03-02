"""
Relative time select filters for tiddlyweb. 

Where a filter is:

    select=modifier:>2011

once could expect either a tiddlywiki timestamp string, a fragment
thereof, or some numbers that end with 'd', 's', 'm', 'h', 'y' (case
insensitive) meaning Days, Seconds, Minutes, Hours, Years. We don't
worry about months. If the trailing letter is there, we translate it
into an absolute time in the past, relative to now.

It's important to note that the translation happens _before_ the > or
< is interpreted. So while select=modified:>1d at first glance reads
as "select those entities with a modified more than one day ago" it
is actually, if we say today is 20110302, "select those entities
with a modified greater than 20110302" (i.e. those thing modified
within the last day).

Install by adding 'tiddlywebplugins.relativetime' to system_plugins
in tiddlywebconfig.py.
"""
from datetime import datetime, timedelta

from tiddlyweb.filters import FilterError
from tiddlyweb.filters.sort import ATTRIBUTE_SORT_KEY, date_to_canonical

def init(config):
    pass


def parse_date(datestring):
    """
    We expect either a tiddlywiki timestamp string,
    a fragment thereof, or some numbers that end with
    'd', 's', 'm', 'h', 'y' (case insensitive) meaning
    Days, Seconds, Minutes, Hours, Years. We don't worry
    about months. If the trailing letter is there, we
    translate it into an absolute time in the past, relative
    to now.
    """
    end = datestring[-1].lower()
    if not end.isdigit():
        datestring = _parse_relative_time(datestring)
    return date_to_canonical(datestring)


def _parse_relative_time(datestring):
    time_type = datestring[-1]
    time_value = int(datestring[0:-1])
    # clearly this can be cleared up
    if time_type == 'y':
        time_type = 'd'
        time_value = time_value * 365
    if time_type == 'd':
        delta = timedelta(days=time_value)
    elif time_type == 's':
        delta = timedelta(seconds=time_value)
    elif time_type == 'm':
        delta = timedelta(minutes=time_value)
    elif time_type == 'h':
        delta = timedelta(hours=time_value)
    else:
        raise FilterError('unknown time type in filter')
    time_object = datetime.utcnow() - delta
    datestring = unicode(time_object.strftime('%Y%m%d%H%M%S'))
    return datestring


# reset ATTRIBUTE_SORT_KEY to local func
ATTRIBUTE_SORT_KEY.update({'modified': parse_date, 'created': parse_date})

