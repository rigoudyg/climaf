#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""  Basic types and syntax for managing time periods in CLIMAF

"""

# S.Senesi 08/2014 : created

from __future__ import print_function, division, unicode_literals, absolute_import

import re
import datetime
import six
import copy

from climaf.utils import Climaf_Error
from env.clogging import clogger, dedent
from env.environment import *


class cperiod(object):
    """
    A class for handling a pair of datetime objects defining a period.

    Period is defined as [ date1, date2 ]. Resolution for date2 is 1 minute
    Attribute 'pattern' usually provides a more condensed form

    """

    def __init__(self, start, end=None, pattern=None):
        self.fx = False
        if isinstance(start, six.string_types) and start == 'fx':
            self.fx = True
            self.pattern = 'fx'
        else:
            if not isinstance(start, datetime.datetime) or not isinstance(end, datetime.datetime):
                try:
                    # Assuming start and end use Netcdf advanced calendars (e.g. noleap or 360-day)
                    # and trying to carry on anyway with dumb python datetime package
                    start = start._to_real_datetime()
                    end = end._to_real_datetime()
                except:
                    raise Climaf_Period_Error("issue with start or end, %s : %s,\n%s : %s" %
                                              (type(start), str(start), type(end), str(end)))
            if start > end:
                raise Climaf_Period_Error("Period's start (%s) must be before period's end (%s)" %
                                          (repr(start), repr(end)))
            self.start = start
            self.end = end
            if pattern is None:
                self.pattern = self.__repr__()
            else:
                self.pattern = pattern

    #
    def __eq__(self, other):
        test = not other == "*" and isinstance(other, cperiod)
        if test and self.fx != other.fx:
            test = False
        if test and self.pattern != other.pattern:
            test = False
        start_self = getattr(self, "start", None)
        start_other = getattr(other, "start", None)
        if test and start_self != start_other:
            test = False
        end_self = getattr(self, "end", None)
        end_other = getattr(other, "end", None)
        if test and end_self != end_other:
            test = False
        return test

    def __le__(self, other):
        if self.start != other.start:
            return self.start <= other.start
        else:
            return self.end <= other.end

    def __lt__(self, other):
        if self.start != other.start:
            return self.start < other.start
        else:
            return self.end < other.end

    def __ge__(self, other):
        if self.start != other.start:
            return self.start >= other.start
        else:
            return self.end >= other.end

    def __gt__(self, other):
        if self.start != other.start:
            return self.start > other.start
        else:
            return self.end > other.end

    #
    def __hash__(self):
        return hash((self.fx, self.pattern, getattr(self, "start", None), getattr(self, "end", None)))

    #
    def __repr__(self):
        return self.pr()
        # return("%04d%02d%02d%02d%02d-%04d%02d%02d%02d%02d"%(\
        #      self.start.year,self.start.month,self.start.day,self.start.hour,self.start.minute,
        #      self.end.year,self.end.month,self.end.day,self.end.hour,self.end.minute))

    #
    def iso(self):
        """ Return isoformat(start)-isoformat(end), (with inclusive end, and 1 minute accuracy)
        e.g. : 1980-01-01T00:00:00,1980-12-31T23:59:00
        """
        if self.fx:
            raise Climaf_Period_Error("There is no ISO representation for period 'fx'")
        endproxy = self.end - datetime.timedelta(0, 60)  # substract 1 minute
        return "%s,%s" % (self.start.isoformat(), endproxy.isoformat())

    #
    def pr(self):
        if self.fx:
            return 'fx'
        if self.start.minute != 0 or self.start.minute != 0:
            return ("%04d%02d%02d%02d%02d-%04d%02d%02d%02d%02d" % (self.start.year, self.start.month, self.start.day,
                                                                   self.start.hour, self.start.minute, self.end.year,
                                                                   self.end.month, self.end.day, self.end.hour,
                                                                   self.end.minute))
        elif self.start.hour != 0 or self.end.hour != 0:
            return ("%04d%02d%02d%02d-%04d%02d%02d%02d" % (self.start.year, self.start.month, self.start.day,
                                                           self.start.hour, self.end.year, self.end.month, self.end.day,
                                                           self.end.hour))
        elif self.start.day != 1 or self.end.day != 1:
            if self.end.day != 1:
                d = self.end.day - 1
                m = self.end.month
                y = self.end.year
            else:
                end = self.end - datetime.timedelta(1)
                y = end.year
                m = end.month
                d = end.day
            if (self.start.year, self.start.month, self.start.day) == (y, m, d):
                return "%04d%02d%02d" % (y, m, d)
            else:
                return "%04d%02d%02d-%04d%02d%02d" % (self.start.year, self.start.month, self.start.day, y, m, d)
        elif self.start.month != 1 or self.end.month != 1:
            if self.end.month != 1:
                m = self.end.month - 1
                y = self.end.year
            else:
                m = 12
                y = self.end.year - 1
            if self.start.year == y and self.start.month == m:
                return "%04d%02d" % (self.start.year, self.start.month)
            else:
                return "%04d%02d-%04d%02d" % (self.start.year, self.start.month, y, m)
        else:
            if self.start.year != self.end.year - 1:
                return "%04d-%04d" % (self.start.year, self.end.year - 1)
            else:
                return "%04d" % self.start.year

    #
    def hasFullYear(self, year):
        if self.fx:
            raise Climaf_Period_Error("Meaningless for period 'fx'")
        else:
            year = int(year)
            return self.start <= datetime.datetime(year=year, month=1, day=1) and \
                datetime.datetime(year=year + 1, month=1, day=1) <= self.end

    #
    def start_with(self, begin):
        """ If period BEGIN actually begins period SELF, returns the
        complement of BEGIN in SELF; otherwise returns None """
        if self.fx:
            return False
        if self.start == begin.start and self.end >= begin.end:
            return cperiod(begin.end, self.end)

    #
    def is_before(self, candidate):
        """ True if period SELF starts before period CANDIDATE
        """
        if self.fx:
            return False
        return self.start <= candidate.start

    #
    def includes(self, included):
        """ if period self does include period 'included', returns a pair of
        periods which represents the difference """
        if self.fx:
            return False
        # raise Climaf_Period_Error("Meaningless for period 'fx'")
        if self.start <= included.start and included.end <= self.end:
            return cperiod(self.start, included.start), cperiod(included.end, self.end)

    #
    def intersects(self, other):
        """
        Returns the intersection of period self and period 'other' if any
        """
        if other:
            if self.fx and other.fx:
                clogger.warning("Meaningless for period 'fx'")
                return cperiod("fx")
            elif self.fx:
                return cperiod(other.start, other.end)
            elif other.fx:
                return cperiod(self.start, self.start)
            else:
                start = self.start
                if other.start > start:
                    start = other.start
                end = self.end
                if other.end < end:
                    end = other.end
                if start < end:
                    return cperiod(start, end)
        else:
            if self.fx:
                return cperiod("fx")
            else:
                return cperiod(self.start, self.end)


def init_period(dates):
    """
    Init a CliMAF 'period' object

    Args:
      dates (str): must match r'YYYY[MM[DD[HH[MM]]]][(-\|_)YYYY[MM[DD[HH[MM]]]]]' , or
        be 'fx' for fixed fields

    Returns:
      the corresponding CliMAF 'period' object

    When using only YYYY, can omit some Ys (for zeros).
    Cannot handle year 0000

    Examples :

    -  a one-year long period : '1980', or '1980-1980'
    -  a decade : '1980-1989'
    -  first millenium : 1-1000  # Must have leading zeroes if you want to quote a month
    -  first century : 1-100
    -  one month : '198005'
    -  two months : '198003-198004'
    -  one day : '17890714'
    -  the same single day, in a more complicated way : '17890714-17890714'

    CliMAF internally handles date-time values with a 1 minute accurracy; it can provide date
    information to external scripts in two forms; see keywords 'period' and 'period_iso' in
    :py:func:`~climaf.operators.cscript`

    """
    def str_to_date(a_date, end=False):
        if a_date.startswith("-"):
            sign = -1
            a_date = a_date[1:]
        elif a_date.startswith("+"):
            sign = 1
            a_date = a_date[1:]
        else:
            sign = 1
        a_date = a_date.zfill(4)
        year = int(a_date[0:4]) * sign
        month = int(a_date[4:6]) if len(a_date) > 5 else 1
        day = int(a_date[6:8]) if len(a_date) > 7 else 1
        hour = int(a_date[8:10]) if len(a_date) > 9 else 0
        minute = int(a_date[10:12]) if len(a_date) > 11 else 0
        add_day = 0
        add_hour = 0
        add_minute = 0
        if end:
            if len(a_date) < 6:
                year += 1
            elif len(a_date) < 8:
                month += 1
                if month > 12:
                    month = 1
                    year += 1
            elif len(a_date) < 10:
                add_day = 1
            elif len(a_date) < 12:
                add_hour = 1
            else:
                add_minute = 1
        try:
            if year <= 0:
                raise Climaf_Period_Error("Could not yet deal with negative or null years.")
            else:
                rep = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        except:
            raise Climaf_Period_Error(
                "String %s is not a date (%s %s %s %s %s)" % (a_date, year, month, day, hour, minute))
        if end:
            rep += datetime.timedelta(days=add_day, hours=add_hour, minutes=add_minute)
        return rep

    # clogger.debug("analyzing  %s"%dates)
    if isinstance(dates, cperiod):
        return dates
    elif not isinstance(dates, six.string_types):
        raise Climaf_Period_Error("arg is not a string : " + repr(dates))
    else:
        dates = str(dates)
        if dates in ['fx', ]:
            return cperiod('fx')
        else:
            period_regexp = re.compile(r"(?P<start>-?\d+)([-_](?P<end>-?\d+))?")
            period_match = period_regexp.match(dates)
            if period_match:
                start = period_match.groupdict()["start"]
                s = str_to_date(start)
                end = period_match.groupdict()["end"]
                if end is None:
                    e = str_to_date(start, end=True)
                else:
                    e = str_to_date(end, end=True)
                if s < e:
                    return cperiod(s, e, None)
                else:
                    raise Climaf_Period_Error("Must have start (%s) before or equal to end (%s)" % (repr(s), repr(e)))
            else:
                raise Climaf_Period_Error("Could not create a period with string %s" % dates)


def sort_periods_list(periods_list):
    #
    class SortTree(object):
        def __init__(self, el):
            self.pivot = el
            self.smaller = None
            self.larger = None

    #
    def insert(el, tree=None):
        """
        """
        if tree is None:
            return SortTree(el)
        if repr(tree.pivot) == repr(el):
            return tree  # Discard identical periods
        if el.is_before(tree.pivot):
            tree.smaller = insert(el, tree.smaller)
        else:
            tree.larger = insert(el, tree.larger)
        return tree

    #
    def walk(tree):
        if tree is None:
            return []
        rep = walk(tree.smaller)
        rep.append(tree.pivot)
        rep.extend(walk(tree.larger))
        return rep

    #
    if isinstance(periods_list, list) and all([isinstance(elt, cperiod) for elt in periods_list]):
        clist = copy.copy(periods_list)
        sorted_tree = SortTree(clist.pop())
        while clist:
            insert(clist.pop(), sorted_tree)
        return walk(sorted_tree)
    else:
        raise Climaf_Period_Error("Can not deal with something else than a list of cperiod objects.")


def merge_periods(remain_to_merge, already_merged=list(), handle_360_days_year=True):
    """
    Provided with a list of periods (even un-sorted), returns a list of periods 
    where all consecutive periods have been merged.

    Argument 'already_merged' is used only in the underlying recursion, and shouldn't 
    usually be provided

    Argument 'handle_360_days_year' allows to merge consecutive periods which miss 
    only a 31st december,such as in the case with 360-days calendars. It defaults to True

    For dealing with very long list of periods, which do not allow for recursion, we
    proceed with batches of N elements
    """
    if not (isinstance(remain_to_merge, list) and all([isinstance(elt, cperiod) for elt in remain_to_merge])):
        raise Climaf_Period_Error("Can not deal with something else than a list of cperiod objects.")
    else:
        N = 300
        if isinstance(already_merged, list) and len(already_merged) == 0:
            if len(remain_to_merge) < 2:
                return remain_to_merge
            else:
                sorted_remain = sorted(remain_to_merge)
                if len(sorted_remain) <= N:
                    return merge_periods(sorted_remain[1:], [sorted_remain[0]], handle_360_days_year)
                else:
                    # Avoid too much recursion
                    first_batch = merge_periods(sorted_remain[0:N])
                    return merge_periods(sorted_remain[N:], first_batch, handle_360_days_year)
        else:
            if len(remain_to_merge) > 0:
                last = already_merged[-1]
                next_one = remain_to_merge.pop(0)
                # print "last.end=",last.end,"next.start=",next_one.start
                # if (last.end == next_one.start) :
                #    already_merged[-1]=cperiod(last.start,next_one.end)
                if next_one.start <= last.end or (handle_360_days_year and last.end.month == 12 and
                                                  last.end.day == 31 and
                                                  next_one.start.month == 1 and
                                                  next_one.start.day == 1 and
                                                  next_one.start.year == last.end.year + 1):
                    if next_one.end > last.end:
                        # the next period is not entirely included in the
                        # last merged one
                        already_merged[-1] = cperiod(last.start, next_one.end)
                else:
                    # There is no overlap between both periods
                    already_merged.append(next_one)
            #
            if len(remain_to_merge) > 0:
                return merge_periods(remain_to_merge, already_merged, handle_360_days_year)
            else:
                return already_merged


def intersect_periods_list(lperiod1, lperiod2):
    """
    Given two lists of periods, returns a list of the periods representing their intersection

    Algorithm : for each period in l1, compute intersection with all periods in l2,
    and add it in a big list; finally, merge  the big list
    """
    if not(isinstance(lperiod1, list) and [isinstance(elt, cperiod) for elt in lperiod1] and
           isinstance(lperiod2, list) and [isinstance(elt, cperiod) for elt in lperiod2]):
        raise Climaf_Period_Error("Can not deal with something else than list of cperiod objects")
    else:
        big = []
        for p1 in lperiod1:
            for p2 in lperiod2:
                inter = p1.intersects(p2)
                if inter:
                    big.append(inter)
        return merge_periods(big)


def lastyears(period, nyears):
    """
    Returns a period ending at PERIOD's end and which duration is at most NYEARS
    """
    # print "period=",period, 'type=',type(period),'nyears=',nyears
    if isinstance(period, six.string_types):
        period = init_period(period)
    elif not isinstance(period, cperiod):
        raise Climaf_Period_Error("Can not deal with periods that are not string or cperiod objects")
    if not isinstance(nyears, int):
        raise Climaf_Period_Error("nyears must be an integer, not %s" % nyears)
    rep = cperiod(period.start, period.end)
    yend = rep.end.year
    ystart = rep.start.year
    if ystart < yend - nyears:
        s = rep.end
        rep.start = datetime.datetime(year=yend - nyears, month=s.month, day=s.day, hour=s.hour, minute=s.minute)
    return repr(rep)


def firstyears(period, nyears):
    """
    Returns a period beginning at PERIOD's begin and which duration is at most NYEARS
    """
    if isinstance(period, six.string_types):
        period = init_period(period)
    elif not isinstance(period, cperiod):
        raise Climaf_Period_Error("Can not deal with periods that are not string or cperiod objects")
    if not isinstance(nyears, int):
        raise Climaf_Period_Error("nyears must be an integer, not %s" % nyears)
    rep = cperiod(period.start, period.end)
    yend = rep.end.year
    ystart = rep.start.year
    if yend > ystart + nyears:
        s = rep.start
        rep.end = datetime.datetime(year=ystart + nyears, month=s.month, day=s.day, hour=s.hour, minute=s.minute)
    # print "period=",period, 'type=',type(period),'nyears=',nyears
    # print rep
    return repr(rep)


def group_periods(diclist):
    """Assuming DICLIST is a list of dictionnaries which include key
    'period', identifies all dicts which have the same content for the
    other keys, merge the periosd for those dicts and returns the list of 
    dicts with this merge periods

    Used e.g. on 'return_combinations' output of a series of selectGenericFiles
    """
    tempo = dict()
    for dic in diclist:
        aperiod = dic['period']
        if not isinstance(aperiod, cperiod):
            aperiod = init_period(aperiod)
        #
        keys = list(dic.keys())
        keys.remove('period')
        keys.sort()
        tuple_key = tuple([dic[k] for k in keys])
        #
        if tuple_key not in tempo:
            tempo[tuple_key] = dic.copy()
            tempo[tuple_key]['period'] = list()
        tempo[tuple_key]['period'].append(aperiod)
    #
    output = list()
    for key in tempo:
        dic = tempo[key]
        dic['period'] = merge_periods(dic['period'])
        output.append(dic)
    #
    return output


def freq_to_minutes(data_freq):
    """
    Interprets values returned by Panda's infer_freq() , such as '2D', 'H', '6MS'.. 
    Returns duration in minutes (quite arbitrary for months)
    """
    data_freq = data_freq.replace("mon", "MS")
    number = re.findall("^[0-9]*", data_freq)
    if len(number[0]) == 0:
        number = 1
    else:
        number = int(number[0])
    units = re.findall("[A-Z]*$", data_freq)[0]
    scale = {"M": 1, "H": 60, "D": 60 * 24, "MS": 30 * 60 * 24}
    if units in scale:
        return number * scale[units]
    else:
        raise Climaf_Error("Cannot interpret frequency %s, returning O minutes" % data_freq)


class Climaf_Period_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)
