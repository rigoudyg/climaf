#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Example of ensemble definition and handling in CliMAF
# S.Senesi - 05/2015

from __future__ import print_function, division, unicode_literals, absolute_import

from climaf.api import *

# Basic example : superimpose annual time series of tas for various periods of same simulation
############################################################################################

# Define some objects. here, they are datasets for the same simulation but distinct periods
cdef('project', 'example')
cdef('frequency', 'monthly')
cdef('simulation', "AMIPV6ALB2G")
cdef('variable', "tas")
j0 = ds(period="1980")
j1 = ds(period="1981")

# Create an ensemble out of various objects. Similar to dictionnaries
e2 = cens({'1980': j0, '1981': j1})

# You can operate on ensemble with operators that are not ensemble-capable
# Then, CliMAF will simply loop operators on members
# Here, let us compute global average on the ensemble
tas_ga = space_average(e2)

# An 'ensemble-capable' script is a script designed for processing an ensemble
# Such scripts are declared to CLiMAF using keyord ${mmin} for their main input
# They receive the labels/keys if they were declared with keyword ${labels}
# 'curves' is such a script, devoted to plot xy curves
p = curves(tas_ga, title="Surface Temperature global average")
p = curves(tas_ga, title="Surface Temperature global average", X_axis="aligned")
cshow(p)

# Advanced example : create plot panel of various members, add a member, and compute anomalies
###############################################################################################

if atCNRM or onCiclad or onSpirit:
    # Define some default values for using CMIP5 data for various realizations
    cdef("project", "CMIP5")
    cdef("frequency", "monthly")
    cdef("model", "CNRM-CM5")
    cdef("variable", "tas")
    # Create an ensemble of datasets , more easily, with 'eds'; labels are automatic
    ens = eds(experiment="historical", period="1860", simulation=["r1i1p1", "r2i1p1"], table="Amon")
else:
    ens = e2

# You can invoke a non-ensemble-capable script with an ensemble input
# Looping is automatic. The result is also an ensemble
# (additionnaly, each member label is added to the 'title' when looping)
multiplot = plot(ens, title='tas')

# Display all plots separately
cshow(multiplot)

# Assemble all plots in a page and display it
page = cpage(multiplot)
cshow(page)

if atCNRM or onCiclad or onSpirit:
    # Add a member to an ensemble
    member = ds(experiment="historical", period="1860", simulation="r3i1p1", table="Amon")
    ens["r3i1p1"] = member

# Compute ensemble mean thanks to CDO
cscript("ensavg", "cdo ensavg ${mmin} ${out}")
average = ensavg(ens)

# Compute anomalies wrt to ensemble mean
anomalies = minus(ens, average)
cshow(cpage(plot(anomalies, title='tas')))

# BE CAUTIOUS WHEN EXTENDING AN ENSEMBLE
#############################################
# you shouldn't extend an ensemble with the result of some
# operation on the same ensemble : because of the dynamic
# nature of CliMAF objects, this could lead to an INFINITE RECURSION
# You should rather use a copy to create the extended ensemble

myens = cens({'1980': j0, '1981': j1})
eavg = ccdo_ens(myens, operator='ensavg')
extended_ens = myens.copy()
extended_ens['avg'] = eavg
