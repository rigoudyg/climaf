#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import *

# Define a dataset, using a built-in pre-defined datafile location
##################################################################
dg = ds(project="example", frequency="monthly", simulation="AMIPV6ALB2G", variable="tas", period="1980-1981")

# Average it over space
#########################################################
ta = space_average(dg)

cshow(curves(ta, title="AMIPV6"))
