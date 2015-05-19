"""

This module declares ERA Interim land data organization and specifics, as managed by Sophie T. at CNRM;

**Also declares how to derive CMIP5 variables from the original ERAI-land variables set**

Attribute is 'grid'

Various grids are available. Original grid writes as : grid='_'. Other grids write e.g. as : grid ='T127'

Example of an 'erai-land' project dataset declaration ::

 >>> cdef('project','erai-land')
 >>> d=ds(variable='snd',period='198001',grid='_')
 >>> d2=ds(variable='snd',period='198001',grid='T127')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias

cproject('erai-land','grid')  # no grid writes as '_' , otherwise as e.g. 'T127'

url_erai_land1="/cnrm/vdr/DATA/OBS/netcdf/monthly_mean/erai-land/erai_???_mm_${variable}${grid}YYYY-YYYY.nc" #for original grid
url_erai_land2="/cnrm/vdr/DATA/OBS/netcdf/monthly_mean/erai-land/erai_???_mm_${variable}.${grid}.YYYY-YYYY.nc" #for other grids write e.g. as : grid='T127'
dataloc(project='erai-land', organization='generic', url=[url_erai_land1,url_erai_land2])


# Defining alias and derived variables for ERAI-land, together with filenames
############################################################################## 

#calias("erai-land",''    ,'asn'  ,filenameVar='ASN') #asn:="Snow albedo" sans dimension mais un commentaire ds '.xls': "snow albedo was deleted." ou "surface snow and ice sublimation flux" en kg.m-2.s-1 ?

#calias("erai-land",'snw'    ,'rsn'  , scale= 'snd',filenameVar='RSN') ?
#rsn=Snow density "kg m**-3"ds .nc
#dans '.xls'
#surface snow amount -snw- en kg.m-2
#ou snowfall flux -prsn- en kg.m-2.s-1 ?

calias("erai-land",'snd' ,'sd'  ,filenameVar='SD')


