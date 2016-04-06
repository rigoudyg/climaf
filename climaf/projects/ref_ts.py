"""

This module declares reference products on ipsl data organization and specifics, as managed by J. Servonnat at IPSL;

Attributes are : ...

Example of an 'ref_ts' project dataset declaration ::

 >>> cdef('project','ref_ts')
 >>> d=ds(variable='tas',period='198001'....)
 >>> d2=ds(variable='tas',period='198001', frequency='daily', ....)

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs
from climaf.site_settings import onCiclad, atTGCC

cfreqs('ref_ts', {'monthly':'mo' , 'daily':'day' })

if onCiclad:
    root="/data/jservon/Evaluation/"
if atTGCC:
    root="/ccc/work/cont003/igcmg/igcmg/IGCM/"
if atIdris:
    root="/workgpfs/rech/psl/rpsl035/IGCM/"

cproject('ref_ts', ('frequency','monthly'), ('product','*'), ('period','1900-2050'))
pattern1=root+"ReferenceDatasets/ts/*/${frequency}/${variable}/${variable}_*mon_${product}*_YYYYMM-YYYYMM.nc"
dataloc(project='ref_ts', organization='generic', url=[pattern1])

