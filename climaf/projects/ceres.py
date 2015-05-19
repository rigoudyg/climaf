"""

This module declares CERES data organization and specifics, as managed by Sophie T. at CNRM;

**Also declares how to derive CMIP5 variables from the original CERES variables set**

No attributes 

Example of an 'ceres' project dataset declaration ::

 >>> cdef('project','ceres')
 >>> d=ds(variable='rlds',period='198001')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias

cproject('ceres') 
url_ceres="/cnrm/vdr/DATA/OBS/netcdf/monthly_mean/ceres/${variable}_CERES-EBAF.nc"
dataloc(project='ceres', organization='generic', url=[url_ceres])

# Defining alias and derived variables for CERES, together with filenames
##############################################################################

calias("ceres",'rlds'    ,'rlds'  ,filenameVar='rlds') 
calias("ceres",'rldscs'  ,'rldscs',filenameVar='rldscs')
calias("ceres",'rlus'    ,'rlus'  ,filenameVar='rlus')

#calias("ceres",''    ,'rluscs'  ,filenameVar='rluscs') pas de variable correspondante...?
#rluscs:="Surface Longwave Flux Up, Monthly Means, Clear-Sky conditions"
	
calias("ceres",'rlut'    ,'rlut'  ,filenameVar='rlut') 
calias("ceres",'rlutcs'  ,'rlutcs',filenameVar='rlutcs') 
calias("ceres",'rsds'    ,'rsds'  ,filenameVar='rsds') 
calias("ceres",'rsdscs'  ,'rsdscs',filenameVar='rsdscs') 
calias("ceres",'rsdt'    ,'rsdt'  ,filenameVar='rsdt') 
calias("ceres",'rsus'    ,'rsus'  ,filenameVar='rsus') 
calias("ceres",'rsuscs'  ,'rsuscs',filenameVar='rsuscs') 
calias("ceres",'rsut'    ,'rsut'  ,filenameVar='rsut')
calias("ceres",'rsutcs'  ,'rsutcs',filenameVar='rsutcs')


