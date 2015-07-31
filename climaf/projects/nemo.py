"""

This module declares NEMO data organization, where VT-files (netcdf file with
mean values of vt, vs, ut, us for heat and salt transport) are defined

Attribute are 'grid' and 'table'

Example of an 'NEMO' project dataset declaration ::

 >>> cdef('project','NEMO')
 >>> cdef('frequency','monthly')
 >>> d=ds(variable='uo',period='198001',grid='grid_U',table='table2.3')
 >>> d2=ds(variable='vozous',period='198001',grid='VT')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from climaf.site_settings import atCNRM

if atCNRM:
    cproject('NEMO','grid','table',separator='&')

    root1="/cnrm/aster/data3/aster/senesi/NO_SAVE/expes/PRE6/PRE6CPLCr2alb/O/PRE6CPLCr2alb_1m_"
    root2="/cnrm/aster/data3/aster/chevalli/Monitoring/PRE6/SORTIE/PRE6/PRE6CPLCr2alb/MONITOR/VT/PRE6CPLCr2alb_1m_"
    suffix="YYYYMMDD_YYYYMMDD"

    url_nemo1=root1+suffix+"_${grid}_${table}.nc"
    url_nemo2=root2+suffix+"_${grid}.nc"   #grid='VT'
   
    dataloc(project='NEMO', organization='generic', url=[url_nemo1,url_nemo2])
