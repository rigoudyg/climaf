#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CliMAF utilities.
"""

from __future__ import print_function, division, unicode_literals, absolute_import

from string import Template

from env.clogging import clogger, dedent

def remove_keys_with_same_values(diclist) :
    """Assuming DICLIST is a list of dicts which all have the same set of
    keys, remove in each dict those keys which value is the same
    across all dicts.
    Returns a subdict with those keys which have a common value

    """
    if len(diclist) == 0 :
        return []
    #
    values = { k:set() for k in diclist[0] }
    #
    for dic in diclist :
        for k in values:
            if isinstance(dic[k],list) :
                val = tuple(dic[k])
            else :
                val = dic[k]
            values[k].add(val)
    keys_with_common_values = [ k for k in values if len(values[k]) == 1 ]
    #
    common_values_dict=dict()
    for dic in diclist :
        for k in keys_with_common_values:
            common_values_dict[k] = dic.pop(k)
    return common_values_dict


def cartesian_product_substitute(string, skip_keys=list(), **kwargs):

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
    >>> cartesian_product_substitute(u, x=["*","x","X"], y=["?","y"], z=3)
    ['aa/X/y', 'aa/x/y', 'ab/X', 'ab/x'],
    {'z' : 3 },
    { 'x':'*', 'y':'?' },

    """
    set_kw = [ kw for kw in kwargs if isinstance(kw, list)]
    new_strings = set([string])
    for kw in [kw for kw in kwargs if kw not in skip_keys]:
        for s in new_strings.copy() :
            new_strings.remove(s)
            if kw in set_kw:
                for value in set(kwargs[kw][1:]):
                    new_strings.add(Template(s).safe_substitute({kw:value}))
            else:
                value = kwargs[kw]
                new_strings.add(Template(s).safe_substitute({kw:value}))
                
    #
    simple_kwargs = kwargs.copy()
    for k in set_kw :
        simple_kwargs.pop(k)
    #
    kwargs_with_patterns = kwargs.copy()
    for k in set_kw :
        kwargs_with_patterns[k] = kwargs[k][0]
    #
    return(list(new_strings), simple_kwargs, kwargs_with_patterns)


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
