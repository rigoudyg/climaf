#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This module declares ERA Interim land data organization and specifics, as managed by Sophie T. at CNRM;
see file:///cnrm/amacs/DATA/OBS/netcdf/

**Also declares how to derive CMIP5 variables from the original ERAI-land variables set**

Attribute is 'grid'

Various grids are available. Original grid writes as : grid='_'. Other grids write e.g. as : grid ='T127'

Most variables for ERAI-LAND have no CMIP5 counterpart : only CIMP5
'snd' is aliased to ERAI-LAND 'sd'; see doc for the other, original,
ERAI-LAND variables

Example of an 'erai_land' project dataset declaration ::

 >>> cdef('project','erai-land')
 >>> d=ds(variable='snd',period='198001',grid='_')
 >>> d2=ds(variable='snd',period='198001',grid='T127')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from env.site_settings import atCNRM

if atCNRM:
    cproject('erai-land', 'grid')  # no grid writes as '_' , otherwise as e.g. 'T127'

    root = "/cnrm/amacs/DATA/OBS/netcdf/monthly_mean/erai-land/erai_???_mm_${variable}"
    suffix = "${PERIOD}.nc"
    #
    url_erai_land1 = root + "${grid}" + suffix  # for original grid
    url_erai_land2 = root + ".${grid}." + suffix  # for other grids write e.g. as : grid='T127'
    #
    dataloc(project='erai-land', organization='generic', url=[url_erai_land1, url_erai_land2])

    # Defining alias and derived variables for ERAI-land, together with filenames
    ##############################################################################

    # asn:="Snow albedo" sans dimension
    # calias("erai-land",''    ,'asn'  ,filenameVar='ASN')

    # calias("erai-land",'snw'    ,'rsn'  , scale= 'snd',filenameVar='RSN') ?
    # rsn=Snow density "kg m**-3"ds .nc

    calias("erai-land", 'snd', 'sd', filenameVar='SD')
