"""

This module declares reference products on ipsl data organization and specifics, as managed by J. Servonnat at IPSL;

**Also declares how to derive CMIP5 variables from the original ERAI variables set (aliasing)**

Attributes are 'grid', and 'frequency'

Various grids are available. Original grid writes as : grid='_'. Other grids write e.g. as : grid ='T42' or grid ='T127'

Example of an 'ref_ipsl' project dataset declaration ::

 >>> cdef('project','ref_ipsl')
 >>> d=ds(variable='tas',period='198001',grid='_', frequency='monthly')
 >>> d2=ds(variable='tas',period='198001',grid='144142',frequency='daily')

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs
from climaf.site_settings import onCiclad

cfreqs('ref_ipsl', {'monthly':'mo' , 'daily':'day' })

if onCiclad:
    cproject('ref_ipsl', ('frequency','monthly'), ('product','*'), ('period','1900-2050'))

    root="/data/jservon/Evaluation/ReferenceDatasets/*/${frequency}/${variable}/"
    pattern1=root+"${variable}_*mon_${product}*_YYYYMM-YYYYMM.nc"
    dataloc(project='ref_ipsl', organization='generic', url=[pattern1])

