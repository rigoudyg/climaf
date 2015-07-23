"""

This module declares CERES data organization and specifics, as managed by Sophie T. at CNRM; see file:///cnrm/vdr/DATA/OBS/netcdf/

No attributes in addition to standard ones; and 'simulation' is not used

Version of dataset is implicitly the latest, through symbolic links managed by Sophie. Please
complain to climaf at cnrm dot fr if this does not fit the needs

Example of a 'ceres' project dataset declaration ::

 >>> d=ds('project='ceres, variable='rlds',period='198001',domain=[40.,60.,-10.,+20.])

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
	


