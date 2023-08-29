#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
CliMAF utilities.
"""

from __future__ import print_function, division, unicode_literals, absolute_import

import copy
from string import Template
from collections import defaultdict
import numpy as np

from env.clogging import clogger, dedent, dedent as cdedent
from env.environment import *


def ranges_to_string(ranges=list(), add=list(), sym=False, sep=" "):
    if not isinstance(add, list):
        add = [add, ]
    if len(ranges) > 0 and not isinstance(ranges[0], list):
        ranges = [ranges, ]
    list_nb = copy.deepcopy(add)
    for (start, stop, step) in ranges:
        list_nb.extend(np.arange(start, stop + step, step))
    if sym:
        list_nb.extend([-val for val in list_nb])
    list_nb = sorted(list(set(list_nb)))
    return sep.join([str(elt) for elt in list_nb])


def turn_list_to_tuple(val):
    if isinstance(val, list):
        return tuple(val)
    else:
        return val


def remove_keys_with_same_values(diclist):
    """Assuming DICLIST is a list of dicts which all have the same set of
    keys, remove in each dict those keys which value is the same
    across all dicts (content of DICLIST is actually changed !).

    Also returns a subdict with those keys which have a common value

    """
    if len(diclist) == 0:
        return []
    #
    # Build 'values': a dict of the set (across DICLIST) of values for each key
    values = { k:set() for k in diclist[0] }
    for dic in diclist:
        for k in values:
            values[k].add(turn_list_to_tuple(dic[k]))
    #
    # Register common values in a dict that will be returned
    common_values_dict = { key : diclist[0][key]
                           for key in values if len(values[key]) == 1 }
    #
    # Withdraw each commmon-value-key in each dict of DICLIST. 
    for dic in diclist :
        for k in common_values_dict.keys():
            dic.pop(k)

    # Warn : on top of returning the dict of common values, DICLIST has been modified 
    return common_values_dict


def cartesian_product_substitute(input_string, skip_keys=list(), **kwargs):

    """Iterate Template.safe_substitute on a list of strings, subtituting
    for those keys in kwargs which have a value of type list, by
    creating the cartesian product of all values in all sets

    Those kwargs of type list are supposed to show as first element 
    the pattern that allowed to derive the other list values, by some 
    logic upstream

    Returns :
    - an augmented list after substitution, 
    - a copy of kwargs where keys with values of type list have been removed
    - a copy of kwargs where keys with values of type list have been replaced 
      by the first list value (i.e. the pattern)

    Example :

    >>> u="aa/${x}/${y}/${z}"
    >>> cartesian_product_substitute(u,x=["*","x","X"],y=["?","y"],z=3)
    ['aa/X/y', 'aa/x/y', 'ab/X', 'ab/x'],
    {'z' : 3 },
    { 'x':'*', 'y':'?' },

    """
    set_kw = [kw for kw in kwargs if isinstance(kwargs[kw], list) and kw not in skip_keys]
    single_kw = list(set(list(kwargs)) - set(set_kw) - set(skip_keys))
    # Deal with substitutions for which there is one possible value
    for kw in single_kw:
        input_string = Template(input_string).safe_substitute({kw: kwargs[kw]})
    # Turn input_string into a set
    input_strings = set([input_string, ])
    # Deal with substitutions for which there is several values possible
    for kw in set_kw:
        new_strings = set()
        for s in input_strings:
            for value in set(kwargs[kw][1:]):
                new_strings.add(Template(s).safe_substitute({kw: value}))
        input_strings = new_strings
    #
    simple_kwargs = kwargs.copy()
    for k in set_kw:
        del simple_kwargs[k]
    #
    kwargs_with_patterns = kwargs.copy()
    for k in set_kw:
        kwargs_with_patterns[k] = kwargs[k][0]
    #
    return list(input_strings), simple_kwargs, kwargs_with_patterns


class Climaf_Classes_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)


class Climaf_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)


class Climaf_Cache_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        dedent(100)

    def __str__(self):
        return repr(self.valeur)


class Climaf_Operator_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        # clogging.dedent(100)

    def __str__(self):
        return repr(self.valeur)


class Climaf_Data_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        # clogging.dedent(100)

    def __str__(self):
        return repr(self.valeur)


class Climaf_Driver_Error(Exception):
    def __init__(self, valeur):
        self.valeur = valeur
        clogger.error(self.__str__())
        cdedent(100)

    def __str__(self):
        return repr(self.valeur)
