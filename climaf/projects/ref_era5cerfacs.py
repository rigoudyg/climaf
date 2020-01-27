#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This module declares two 'projects' :

  - 'ref_climatos', for the climatological annual cycles and
  - 'ref_ts', for the 'time series' (one variable evolving with time)
    of a set of reference products as managed by J. Servonnat at IPSL.

This archive is available on Ciclad (IPSL), Curie (TGCC) and Ada (IDRIS), and /cnrm and at Cerfacs

The specific attributes are:

  - **product** (default:'*'): name of the observation or reanalysis product (example: ERAI, GPCP...)
  - for climatologies only : **clim_period** : a character string; there is no mechanism of
    period selection (like with 'period')

Default values of the attributes for climatologies (**ref_climato**) :

- product : '*'
- variable : '*'
- period : 'fx'
- frequency : annual_cycle'

It is possible to pass a list of products to 'product' to define an ensemble of
climatologies with eds() as in:

 >>> dat_ens = eds(project='ref_climatos', product=['ERAI','NCEP'],...)


Default values of the attributes for time_series (**ref_era5cerfacs**) :

- product : '*' : necessary so that the C-ESM-EP identifies that it is an observational product and not a model simulation
- period : '1900-2050'
- frequency : 'monthly'

Example of a 'era5cerfacs' project dataset declaration ::

 >>> cdef('project','ref_era5cerfacs')
 >>> d=ds(variable='tas',period='198001'....)



"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import onCiclad, atTGCC, atIDRIS, atCerfacs, atCNRM

root = None

if onCiclad:
    root = "/data/jservon/Evaluation/ReferenceDatasets/"
if atTGCC:
    root = "/ccc/work/cont003/igcmg/igcmg/IGCM/ReferenceDatasets/"
if atIDRIS:
    root = "/workgpfs/rech/psl/rpsl035/IGCM/ReferenceDatasets/"
if atCerfacs:
    root="/data/scratch/globc/dcom/globc_obs/OBS4MIPS_ANA4MIPS_CMOR/Tier1/ERA5/"
if atCNRM:
    root = "/cnrm/est/COMMON/climaf/reference_datasets_from_IPSL/"

cproject('ref_era5cerfacs', ('frequency', 'monthly'), 'product', ('period', '1979-2018'), 'obs_type', 'table',
         separator='%')
cfreqs('ref_era5cerfacs', {'monthly': 'mon', 'daily': 'day'})

cdef('variable', '*', project='ref_era5cerfacs')
cdef('product', 'ERA5', project='ref_era5cerfacs')
cdef('period', '1979-2018', project='ref_era5cerfacs')
cdef('obs_type', 'reanalysis', project='ref_era5cerfacs')
cdef('table', '*', project='ref_era5cerfacs')

# Obs de MOC RAPID (Il a fallu bricoler les donnees d'origine pour la dimension time au debut et unlim)
# dataloc(project="ref_climatos",organization="generic",
#        url='/home/esanchez/data_climaf/${variable}_vertical_unlim.nc')
calias(project='ref_era5cerfacs', variable='moc', fileVariable='stream_function_mar', filenameVar='moc')

if root:
    pattern1 = root + "${variable}_${table}_${obs_type}_${product}_${PERIOD}.nc"
    dataloc(project='ref_era5cerfacs', organization='generic', url=[pattern1])

#calias("ref_era5cerfacs","tas",offset=273.15)