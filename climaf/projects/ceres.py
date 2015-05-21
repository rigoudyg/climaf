"""

This module declares CERES data organization and specifics, as managed by Sophie T. at CNRM;

**Also declares how to derive CMIP5 variables from the original CERES variables set**

No attributes 

Example of a 'ceres' project dataset declaration ::

 >>> cdef('project','ceres')
 >>> d=ds(variable='rlds',period='198001')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias
from climaf.site_settings import atCNRM

if atCNRM:
    cproject('ceres') 
    url_ceres="/cnrm/vdr/DATA/OBS/netcdf/monthly_mean/ceres/${variable}_CERES-EBAF.nc"
    dataloc(project='ceres', organization='generic', url=[url_ceres])

    # No need to define alias for CERES, which sticks to CMIP5 standards
    ##############################################################################

    #calias("ceres",''    ,'rluscs'  ,filenameVar='rluscs') pas de variable correspondante...?
    #rluscs:="Surface Longwave Flux Up, Monthly Means, Clear-Sky conditions"
	


