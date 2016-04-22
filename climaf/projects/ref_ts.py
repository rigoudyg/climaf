"""
This module declares the 'time series' (one variable evolving with time) of a set of reference products as managed by J. Servonnat at IPSL.
This archive is available on Ciclad (IPSL), Curie (TGCC) and Ada (IDRIS)

The specific attributes are:
  - product (default:'*'): name of the observation or reanalysis product (example: ERAI, GPCP...) 

Default values of the attributes:
- product : '*'
- period : '1900-2050'
- frequency : 'monthly'


Example of a 'ref_ts' project dataset declaration ::

 >>> cdef('project','ref_ts')
 >>> d=ds(variable='tas',period='198001'....)

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs
from climaf.site_settings import onCiclad, atTGCC, atIDRIS

cfreqs('ref_ts', {'monthly':'mo' , 'daily':'day' })

if onCiclad:
    root="/data/jservon/Evaluation/"
if atTGCC:
    root="/ccc/work/cont003/igcmg/igcmg/IGCM/"
if atIDRIS:
    root="/workgpfs/rech/psl/rpsl035/IGCM/"

cproject('ref_ts', ('frequency','monthly'), ('product','*'), ('period','1900-2050'))
pattern1=root+"ReferenceDatasets/ts/*/${frequency}/${variable}/${variable}_*mon_${product}*_YYYYMM-YYYYMM.nc"
dataloc(project='ref_ts', organization='generic', url=[pattern1])


