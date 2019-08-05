#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CliMAF environment tools.
Those variables are used everywhere and should be move to a distinct directory.
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import copy

from climaf.utils import Climaf_Error

# Variables

#: Dictionary of declared projects (type is cproject)
cprojects = dict()

#: Dictionary of aliases dictionaries
aliases = dict()

#: Dictionary of frequency names dictionaries
frequencies = dict()

#: Dictionary of realms names dictionaries
realms = dict()

#: Dictionary of scripts names dictionaries
scripts = dict()

#: Dictionary of operators names dictionaries
operators = dict()

#: Dictionary of derived variables names dictionaries
derived_variables = dict()

#: List of known formats
known_formats = ['nc', 'graph', 'txt']

#: List of graphic formats
graphic_formats = ['png', 'pdf', 'eps']

#: List of none formats
none_formats = [None, 'txt']

#: Log directory
logdir = "."


# Tools to deal with variables
def get_variable(variable):
    if variable in globals():
        return copy.deepcopy(globals()[variable])
    else:
        raise Climaf_Error("Unknown variable %s." % variable)


def change_variable(variable, value):
    if variable in globals():
        globals()[variable] = value
    else:
        raise Climaf_Error("Unknown variable %s." % variable)
