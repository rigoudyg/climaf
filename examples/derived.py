#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" CliMAF - example for derived variables

A derived variable is a new geophysical variable defined by explaining
how to compute it using a script and some other geophysical variable(s)

It can be used to define a CliMAF dataset

"""

# S.Senesi - sept 2014

from __future__ import print_function

# Load Climaf functions and site settings
# This sets logical flags 'onCiclad' and 'atCNRM'
from climaf.api import *

# Set some default values
cdef("project", "example")
cdef("simulation", "AMIPV6ALB2G")
# cdef("period","1980-1981") # Cannto , because datafiles don't have same number of variables for these two years
cdef("period", "1980")

# Define some dataset with a new, virtual, variable (also called
# 'derived') . We call it 'crest' (which stand for Cloud Radiative
# Effect in Shortwave at Top of atmosphere), from all-sky and
# clear-sky sortwave fluxes

# All the other dataset attributes were ste above by cdef()
creShortTop = ds(variable="crest")

# Declare a script that will be used in defining how to derive the new variable
# Actually, this is a standard operator: 'minus' is equivalent to 'sub' (when
# substracting two CliMAF objects) except that is a CliMAF operator)
# cscript('minus','cdo sub ${in_1} ${in_2} ${out}')

# Say how you compute (or derive) variable 'crest' form variables 'rst' and 'rstcs', for all projects
derive('*', 'crest', 'minus', 'rst', 'rstcs')

# Ask for actually compute the variable as a file
my_file = cfile(creShortTop)
print(my_file)

if my_file is None:
    exit(1)
