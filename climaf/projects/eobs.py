"""

This module declares the project E-OBS : 
This archive is available on Ciclad (IPSL), Curie (TGCC) and Ada (IDRIS), and /cnrm and at Cerfacs

The specific attributes are:


Default values of the attributes for time_series (**ref_ts**) :

- product : '*'
- period : '1900-2050'
- frequency : 'monthly'

Example of a 'ref_ts' project dataset declaration ::

 >>> cdef('project','ref_ts')
 >>> d=ds(variable='tas',period='198001'....)



"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import onCiclad, atTGCC, atIDRIS,atCerfacs,atCNRM

# -- Create E-OBS CliMAF project
EOBS_pattern = '/bdd/E-OBS/Grid_${grid}/${variable}_${grid}_YYYY-YYYY_v15.0.nc4'
cproject('E-OBS','grid', 'frequency', separator='%')
dataloc(project='E-OBS', organization='generic', url=EOBS_pattern)

# -- Make a 
cdef('frequency', 'daily', project='E-OBS')
cfreqs('E-OBS',{'daily':'day'})

calias('E-OBS', 'tasmin', 'tn')
calias('E-OBS', 'tasmax', 'tx')



