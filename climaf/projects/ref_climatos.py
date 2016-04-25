"""

This module declares the climatological annual cycles of a set of reference products as managed by J. Servonnat at IPSL.
This archive is available on Ciclad (IPSL), Curie (TGCC) and Ada (IDRIS)

The specific attributes are:
  - product (default:'*'): name of the observation or reanalysis product (example: ERAI, GPCP...)
  - clim_period : a character string; there is no mechanism of period selection (like with 'period')

Default values of the attributes:
- product : '*'
- variable : '*'
- period : 'fx'
- frequency : annual_cycle'

It is possible to pass a list of products to 'product' to define an ensemble with eds() as following:
dat_ens = eds(project='ref_climatos', product=['ERAI','NCEP'],...)

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import onCiclad, atTGCC, atIDRIS

cfreqs('ref_climatos', {'monthly':'mo' , 'daily':'day' , 'seasonal':'mo', 'annual_cycle':'mo'})


if onCiclad:
    root="/data/jservon/Evaluation/"
if atTGCC:
    root="/ccc/work/cont003/igcmg/igcmg/IGCM/"
if atIDRIS:
    root="/workgpfs/rech/psl/rpsl035/IGCM/"
    
cproject('ref_climatos', ('frequency','annual_cycle'), 'product', 'clim_period', ensemble=['product'],separator='%')
cdef('variable'    , '*'            , project='ref_climatos')
cdef('product'     , '*'            , project='ref_climatos')
cdef('clim_period' , '*'            , project='ref_climatos')
cdef('simulation'  , 'refproduct'   , project='ref_climatos')
cdef('period'      , 'fx'           , project='ref_climatos')
pattern2=root+"ReferenceDatasets/climatos/*/${frequency}/${variable}/${product}/ac/${variable}_*mon_${product}_${clim_period}-clim.nc" 
dataloc(project='ref_climatos', organization='generic', url=pattern2)


