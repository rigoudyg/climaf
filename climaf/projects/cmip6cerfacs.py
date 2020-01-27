#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module declares locations for searching data for CMIP6 outputs produced by
libIGCM or Eclis for all frequencies.

Attributes for CMIP6 datasets are : model, experiment, table, realization, grid, version, institute, mip, root

Syntax for these attributes is described in `the CMIP6 DRS document <https://goo.gl/v1drZl>`_

Example for a CMIP6 dataset declaration ::

 >>> tas1pc=ds(project='CMIP6', model='CNRM-CM6-1', experiment='1pctCO2', variable='tas', table='Amon', realization='r3i1p1f2', period='1860-1861')



"""
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef


# Declare CMIP6CERFACS project
cproject('CMIP6CERFACS', 'model', 'simulation', 'institute', 'mip','table', 'realization', 'grid', separator='%')
# --> systematic arguments = simulation, frequency, variable
# -- Set the aliases for the frequency
# cfreqs('PRIMAVERA-cerfacs', {'monthly':'mon', 'yearly':'yr', 'daily':'day'})
# crealms('IGCM_CMIP6', {'atmos':'ATM', 'ocean':'OCE', 'land':'SRF', 'seaice':'ICE' })
# -- Set default values
cdef('institute', 'CNRM-CERFACS', project='CMIP6CERFACS')
cdef('mip', '*', project='CMIP6CERFACS')
cdef('model', '*', project='CMIP6CERFACS')
cdef('simulation', '*', project='CMIP6CERFACS')
cdef('domain', 'global', project='CMIP6CERFACS')
cdef('period', '*', project='CMIP6CERFACS')
cdef('variable', 'tas', project='CMIP6CERFACS')
cdef('table', 'Amon', project='CMIP6CERFACS')
cdef('realization', 'r*i1p1f*', project='CMIP6CERFACS')
cdef('grid', 'g*', project='CMIP6CERFACS')

# -- Specify the pattern
root1 = "/data/scratch/globc/dcom/CMIP6/${mip}/${institute}/${model}/${model}_${simulation}_${realization}/"
pathfiles1 = root1 + "${variable}_${table}_${model}_${simulation}_${realization}_${grid}_${PERIOD}.nc"
root2 = "/data/scratch/globc/dcom/PRIMAVERA/WP6_HIGHRESMIP/${model}_${simulation}_${realization}/"
pathfiles2 = root2 + "${variable}_${table}_${model}_${simulation}_${realization}_${grid}_${PERIOD}.nc"
root3 = "/data/scratch/globc/vrousseau/MODELE/${model}_${simulation}_${realization}/"
pathfiles3 = root3 + "${variable}_${table}_${model}_${simulation}_${realization}_${grid}_${PERIOD}.nc"

# -- call the dataloc CliMAF function
dataloc(project='CMIP6CERFACS', organization='generic', url=[pathfiles1])
dataloc(project='CMIP6CERFACS', organization='generic', url=[pathfiles2])
dataloc(project='CMIP6CERFACS', organization='generic', url=[pathfiles3])

# -- Define alias if necessary
calias("CMIP6CERFACS", "msftmyz", scale=1.e-3)
calias("CMIP6CERFACS", "tos", offset=273.15)
calias("CMIP6CERFACS", "thetao", offset=273.15)
calias("CMIP6CERFACS", "thetaoga", offset=273.15)
calias("CMIP6CERFACS", 'sic', 'siconc', filenameVar='siconc')
calias("CMIP6CERFACS", 'sit', 'sithick', filenameVar='sithick')
calias("CMIP6CERFACS", 'sivolu', 'sivol', filenameVar='sivol')
# Obs de MOC RAPID (Il a fallu bricoler les donnees d'origine pour la dimension time au debut et unlim)
# dataloc(project="ref_climatos",organization="generic",
#        url='/home/esanchez/data_climaf/${variable}_vertical_unlim.nc')
calias(project='ref_climatos', variable='moc', fileVariable='stream_function_mar', filenameVar='moc')
