"""

This module declares NEMO data organization

Attribute are 'grid' and 'table'

Example of an 'NEMO' project dataset declaration ::

 >>> cdef('project','NEMO')
 >>> cdef('frequency','monthly')
 >>> d=ds(variable='uo',period='198001',grid='grid_U',table='table2.3')
 

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from climaf.site_settings import atCNRM

#/cnrm/aster/data1/simulations/SC/Ocean/Origin/Monthly/CPICTL2/CPICTL2_1m_18931201_18931231_grid_U_table2.3.nc
#cnrm/aster/data1/simulations/SC/Ocean/Origin/Monthly/CPICTL2

if atCNRM:
    cproject('NEMO','grid','table',separator='&')

    root="/cnrm/aster/data1/simulations/SC/Ocean/Origin/Monthly/CPICTL2/CPICTL2_"
    #"/cnrm/vdr/DATA/OBS/netcdf/monthly_mean/erai-land/erai_???_mm_${variable}"
    suffix="YYYYMMDD_YYYYMMDD"
    #
    url_nemo1=root+"1d_"+suffix+"_${grid}_${table}.nc"   
    url_nemo2=root+"1m_"+suffix+"_${grid}_${table}.nc"
    url_nemo3="/cnrm/aster/data1/simulations/SC/Ocean/Origin/Monthly/CPICTL2/CPICTL2_1m_18931201_18931231_grid_U_table2.3.nc"

    url_nemo4="/cnrm/aster/data3/aster/chevalli/Monitoring/PRE6/SORTIE/PRE6/PRE6CPLCr2alb/MONITOR/VT/PRE6CPLCr2alb_1m_"+suffix+"_${grid}.nc" #grid='VT'
    url_nemo5="/cnrm/aster/data3/aster/senesi/NO_SAVE/expes/PRE6/PRE6CPLCr2alb/O/PRE6CPLCr2alb_1m_"+suffix+"_${grid}_${table}.nc"
#/cnrm/aster/data3/aster/senesi/NO_SAVE/expes/PRE6/PRE6CPLCr2alb/O/PRE6CPLCr2alb_1m_19981201_19981231_grid_V_table2.3.nc
    
    #
    #dataloc(project='NEMO', organization='generic', url=[url_nemo3])
    dataloc(project='NEMO', organization='generic', url=[url_nemo4,url_nemo5])
