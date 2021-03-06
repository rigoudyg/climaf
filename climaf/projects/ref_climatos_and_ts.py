#!/usr/bin/python
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


Default values of the attributes for time_series (**ref_ts**) :

- product : '*'
- period : '1900-2050'
- frequency : 'monthly'

Example of a 'ref_ts' project dataset declaration ::

 >>> cdef('project','ref_ts')
 >>> d=ds(variable='tas',period='198001'....)



"""

from __future__ import print_function, division, unicode_literals, absolute_import

from env.environment import *
from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from env.site_settings import onCiclad, atTGCC, atIDRIS, atCerfacs, atCNRM

root = None

if onCiclad:
    root = "/data/jservon/Evaluation/ReferenceDatasets/"
if atTGCC:
    root = "/ccc/work/cont003/igcmg/igcmg/IGCM/ReferenceDatasets/"
if atIDRIS:
    root = "/workgpfs/rech/psl/rpsl035/IGCM/ReferenceDatasets/"
if atCerfacs:
    root = "/data/scratch/globc/dcom/CMIP6_TOOLS/ReferenceDatasets/"
if atCNRM:
    root = "/cnrm/est/COMMON/climaf/reference_datasets_from_IPSL/"

cproject('ref_climatos', ('frequency', 'annual_cycle'), 'product', 'clim_period', 'table', 'obs_type',
         ensemble=['product'], separator='%')
cfreqs('ref_climatos', {'monthly': 'mo', 'daily': 'day', 'seasonal': 'mo', 'annual_cycle': 'mo', 'yearly': 'yr'})

cdef('variable', '*', project='ref_climatos')
cdef('product', '*', project='ref_climatos')
cdef('clim_period', '*', project='ref_climatos')
cdef('simulation', 'refproduct', project='ref_climatos')
cdef('period', 'fx', project='ref_climatos')
cdef('table', '*', project='ref_climatos')
cdef('obs_type', '*', project='ref_climatos')

if root:
    pattern1 = root + "climatos/*/${frequency}/${variable}/${product}/ac/" \
                      "${variable}_${table}_${product}_${obs_type}_${clim_period}-clim.nc"
    pattern2 = root + "climatos/*/${frequency}/${variable}/${product}/ac/" \
                      "${variable}_${table}_${product}_${clim_period}-clim.nc"
    patterns = [pattern1, pattern2]
    dataloc(project='ref_climatos', organization='generic', url=patterns)

##########################################################################################


cproject('ref_ts', ('frequency', 'monthly'), ('product', '*'), ('period', '1900-2050'), 'obs_type', 'table',
         ensemble=['product'], separator='%')
cfreqs('ref_ts', {'monthly': 'mo', 'daily': 'day'})

cdef('variable', '*', project='ref_ts')
cdef('product', '*', project='ref_ts')
cdef('simulation', 'refproduct', project='ref_ts')
cdef('period', '1980-2005', project='ref_ts')
cdef('obs_type', '*', project='ref_ts')
cdef('table', '*', project='ref_ts')

calias(project='ref_ts', variable='moc', fileVariable='stream_function_mar', filenameVar='moc')

if root:
    # pattern1=root+"ts/*/${frequency}/${variable}/${variable}_*mon_${product}*_YYYYMM-YYYYMM.nc"
    pattern1 = root + "ts/*/${frequency}/${variable}/${variable}_${table}_${product}_${obs_type}_${PERIOD}.nc"
    dataloc(project='ref_ts', organization='generic', url=[pattern1])
