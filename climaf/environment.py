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
climaf_projects = dict()

#: Dictionary of aliases dictionaries
climaf_aliases = dict()

#: Dictionary of frequency names dictionaries
climaf_frequencies = dict()

#: Dictionary of realms names dictionaries
climaf_realms = dict()

#: Dictionary of scripts names dictionaries
climaf_scripts = dict()

#: Dictionary of operators names dictionaries
climaf_operators = dict()

#: Dictionary of derived variables names dictionaries
climaf_derived_variables = dict()

#: Dictionary of macros names
climaf_macros = dict()

#: List of known formats
climaf_known_formats = ['nc', 'graph', 'txt']

#: List of graphic formats
climaf_graphic_formats = ['png', 'pdf', 'eps']

#: List of none formats
climaf_none_formats = [None, 'txt']

#: Log directory
logdir = "."


# Tools to deal with variables
def get_variable(variable):
    if variable in globals():
        if variable != "climaf_macros":
            return copy.deepcopy(globals()[variable])
        else:
            return copy.copy(globals()[variable])
    else:
        raise Climaf_Error("Unknown variable %s." % variable)


def change_variable(variable, value):
    if variable in globals():
        globals()[variable] = value
    else:
        raise Climaf_Error("Unknown variable %s." % variable)
