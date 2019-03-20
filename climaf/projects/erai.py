#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

This module declares ERA Interim data organization and specifics, as managed by Sophie T. at CNRM; see file:///cnrm/amacs/DATA/OBS/netcdf/

**Also declares how to derive CMIP5 variables from the original ERAI variables set (aliasing)**

Attributes are 'grid', and 'frequency'

Various grids are available. Original grid writes as : grid='_'. Other grids write e.g. as : grid ='T42' or grid ='T127'

Example of an 'erai' project dataset declaration ::

 >>> cdef('project','erai')
 >>> d=ds(variable='tas',period='198001',grid='_', frequency='monthly')
 >>> d2=ds(variable='tas',period='198001',grid='T42',frequency='daily')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from climaf.site_settings import atCNRM

if atCNRM:
    cproject('erai',('grid','_'), ('frequency','monthly'))  # no grid writes as '_' , otherwise as e.g. 'T42' or 'T127'

    root="/cnrm/amacs/DATA/OBS/netcdf/${frequency}"
    patmonth1=root+"_mean/erai/erai_???_mm_${variable}${grid}${PERIOD}.nc"   #for original grid
    patmonth2=root+"_mean/erai/erai_???_mm_${variable}.${grid}.${PERIOD}.nc" #for other grids e.g. : grid ='T42' or 'T127'
    patday1=root+"/erai/ei_${variable}${grid}${PERIOD}.nc"   #for original grid
    patday2=root+"/erai/ei_${variable}_${grid}_${PERIOD}.nc" #for other grids e.g.: grid ='T42' or 'T127'
    dataloc(project='erai', organization='generic', url=[patmonth1,patmonth2,patday1,patday2])


    # Defining alias and derived variables for ERAI, together with filenames
    ##############################################################################
    # Valid both for daily and monthly data (to check : energy flux in W for
    # daily and Joules for monthly ????)

    calias("erai",'sic'    ,'ci'  ,filenameVar='CI')
    calias("erai",'tos'    ,'sst' ,filenameVar='SSTK')
    calias("erai",'z'      ,'z'   ,filenameVar='Z')
    calias("erai",'ta'     ,'t'   ,filenameVar='T')
    calias("erai",'ua'     ,'u'   ,filenameVar='U')
    calias("erai",'va'     ,'v'   ,filenameVar='V')
    calias("erai",'hus'    ,'q'   ,filenameVar='Q')
    calias("erai",'prw'    ,'tcw' ,filenameVar='TCW')
    calias("erai",'prc'    ,'cp'  ,filenameVar='CP')
    calias("erai",'prl'    ,'lsp' ,filenameVar='LSP')
    calias("erai",'prsn'   ,'sf'  ,filenameVar='SF')
    calias("erai",'hfss'   ,'sshf',filenameVar='SSHF')
    calias("erai",'hfls'   ,'slhf',filenameVar='SLHF')
    calias("erai",'ps'     ,'msl' ,filenameVar='MSL')
    calias("erai",'clt'    ,'tcc' ,filenameVar='TCC')
    calias("erai",'uas'    ,'u10' ,filenameVar='10U')
    calias("erai",'vas'    ,'v10' ,filenameVar='10V')
    calias("erai",'tas'    ,'t2m' ,filenameVar='2T')
    calias("erai",'das'    ,'d2m' ,filenameVar='2D')
    calias("erai",'rsds'   ,'ssrd',filenameVar='SSRD')
    calias("erai",'rlds'   ,'strd',filenameVar='STRD')
    calias("erai",'rss'    ,'ssr' ,filenameVar='SSR')
    calias("erai",'rls'    ,'str' ,filenameVar='STR')
    calias("erai",'rlut'   ,'ttr' ,filenameVar='TTR')
    calias("erai",'tauu'   ,'ewss',filenameVar='EWSS')
    calias("erai",'tauv'   ,'nsss',filenameVar='NSSS')
    calias("erai",'evspsbl','e'   ,filenameVar='E')
    calias("erai",'tasmax' ,'mx2t',filenameVar='MX2T')
    calias("erai",'tasmin' ,'mn2t',filenameVar='MN2T')
    calias("erai",'mrro'   ,'ro'  ,filenameVar='RO')
    calias("erai",'rsscs'  ,'ssrc',filenameVar='SSRC')
    calias("erai",'rlscs'  ,'strc',filenameVar='STRC')
    calias("erai",'pr','tp',filenameVar='TP')
    #snm est en kg.m-2.s-1 et smlt en "m of water equivalent" , supposement par mois
    calias("erai",'snm', 'smlt', scale=1000./(86400.*30.3),units="kg m-2 s-1", filenameVar='SMLT')

    # Some additional daily fields
    calias("erai",'v850'   ,'v850',filenameVar='V850')
    calias("erai",'u850'   ,'u850',filenameVar='U850')
    calias("erai",'v200'   ,'v200',filenameVar='V200')
    calias("erai",'u200'   ,'u200',filenameVar='U200')
    # For sfcWind, need to define a derived variable, from 10U and 10V
    #calias("erai",'sfcWind','fg10',filenameVar='10FG') #sfcWind:="Near-Surface Wind Speed" et fg10:="10 metre wind gust"
    calias("erai",'hus'    ,'q',filenameVar='Q60')
    #calias("erai",'z500'   ,'z', scale=1./9.81, units="m", filenameVar='Z500')
    calias("erai",'z500'   ,'z'   , filenameVar='Z500')

    # To do : either read specific files for hurs and huss or provide a CliMAF operator
