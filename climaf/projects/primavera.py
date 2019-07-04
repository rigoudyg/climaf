#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CMIP6 outputs produced by
libIGCM or Eclis for all frequencies.

Attributes for CMIP6 datasets are : model, experiment, table, realization, grid, version, institute, mip, root

Syntax for these attributes is described in `the CMIP6 DRS document <https://goo.gl/v1drZl>`_

Example for a CMIP6 dataset declaration ::

 >>> tas1pc=ds(project='CMIP6', model='CNRM-CM6-1', experiment='1pctCO2', variable='tas', table='Amon', realization='r3i1p1f2', period='1860-1861')

"""

import os
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import atTGCC, onCiclad, onSpip, atCNRM, atCerfacs

# Declare PRIMAVERA project
cproject('PRIMAVERA', 'model', 'simulation', 'table', 'realization', 'grid', separator='%')
# --> systematic arguments = simulation, frequency, variable
# -- Set the aliases for the frequency
# cfreqs('PRIMAVERA-cerfacs', {'monthly':'mon', 'yearly':'yr', 'daily':'day'})
# crealms('IGCM_CMIP6', {'atmos':'ATM', 'ocean':'OCE', 'land':'SRF', 'seaice':'ICE' })
# -- Set default values
cdef('model', '*', project='PRIMAVERA')
cdef('simulation', '*', project='PRIMAVERA')
cdef('domain', 'global', project='PRIMAVERA')
cdef('period', '*', project='PRIMAVERA')
cdef('variable', 'tas', project='PRIMAVERA')
cdef('table', 'Amon', project='PRIMAVERA')
cdef('realization', 'r*i1p1f*', project='PRIMAVERA')
cdef('grid', 'g*', project='PRIMAVERA')

# -- Specify the pattern
root = "/data/scratch/globc/dcom/PRIMAVERA/WP6_HIGHRESMIP/${model}_${simulation}_${realization}/"
pathfiles = root + "${variable}_${table}_${model}_${simulation}_${realization}_${grid}_${PERIOD}.nc"

# -- call the dataloc CliMAF function
dataloc(project='PRIMAVERA', organization='generic', url=[pathfiles])

# -- Define alias if necessary
calias("PRIMAVERA", "msftmyz", scale=1.e-3)
calias("PRIMAVERA", "tos", offset=273.15)
calias("PRIMAVERA", "thetao", offset=273.15)
calias("PRIMAVERA", "thetaoga", offset=273.15)
calias("PRIMAVERA", 'sic', 'siconc', filenameVar='siconc')
calias("PRIMAVERA", 'sit', 'sithick', filenameVar='sithick')
calias("PRIMAVERA", 'sivolu', 'siu', filenameVar='siu')

# Obs de MOC RAPID (Il a fallu bricoler les donnees d'origine pour la dimension time au debut et unlim)
# dataloc(project="ref_climatos",organization="generic", url='/home/esanchez/data_climaf/${variable}_vertical_unlim.nc')
calias(project='ref_climatos', variable='moc', fileVariable='stream_function_mar', filenameVar='moc')
