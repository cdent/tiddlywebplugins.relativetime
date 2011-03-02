
from tiddlywebplugins.relativetime import parse_date
from tiddlyweb.filters import FilterError
from tiddlyweb.model.tiddler import current_timestring, Tiddler
from tiddlyweb.control import filter_tiddlers

import py.test


def test_parse_date():
    """ some of these will fail on some midnights """
    nowstring = current_timestring()
    assert parse_date('2009') == '20090000000000'
    assert parse_date('1d')[0:6] == nowstring[0:6]
    assert parse_date('1h')[0:8] == nowstring[0:8]
    assert parse_date('1m')[0:10] == nowstring[0:10]
    assert parse_date('1s')[0:12] == nowstring[0:12]
    assert int(parse_date('1y')[0:4]) == int(nowstring[0:4]) - 1
    assert py.test.raises(FilterError, "parse_date('1x')")

def test_select():
    # cook some known modified strings in the past
    nowstring = current_timestring()
    now = int(nowstring)
    yearago = str(now - 10000000101)
    dayago = str(now - 1000101)

    tiddlers = []

    tiddler = Tiddler('now')
    tiddler.modified = nowstring
    tiddlers.append(tiddler)

    tiddler = Tiddler('year')
    tiddler.modified = yearago
    tiddlers.append(tiddler)

    tiddler = Tiddler('day')
    tiddler.modified = dayago
    tiddlers.append(tiddler)

    results = list(filter_tiddlers(tiddlers, 'select=modified:<1y'))
    assert len(results) == 1
    assert results[0].title == 'year'

    results = list(filter_tiddlers(tiddlers, 'select=modified:>1y'))
    assert len(results) == 2
    assert sorted(tiddler.title for tiddler in results) == ['day', 'now']

    results = list(filter_tiddlers(tiddlers, 'select=modified:<1d'))
    assert len(results) == 2
    assert sorted(tiddler.title for tiddler in results) == ['day', 'year']

    results = list(filter_tiddlers(tiddlers, 'select=modified:>1m'))
    assert len(results) == 1
    assert results[0].title == 'now'
