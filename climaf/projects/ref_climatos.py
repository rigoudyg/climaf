"""

This module declares PCMDI reference products on ciclad data organization and specifics, as managed by J. Servonnat at IPSL;

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import onCiclad, atTGCC

cfreqs('ref_climatos', {'monthly':'mo' , 'daily':'day' , 'seasonal':'mo', 'annual_cycle':'mo'})


if onCiclad:
    root="/data/jservon/Evaluation/"
if atTGCC:
    root="/ccc/work/cont003/igcmg/igcmg/IGCM/"

    
cproject('ref_climatos', ('frequency','annual_cycle'), 'product', 'clim_period', ensemble=['product'],separator='%')
cdef('variable',     '*',           project='ref_climatos')
cdef('product',      '*',           project='ref_climatos')
cdef('clim_period',  '*',           project='ref_climatos')
cdef('period',       'fx',          project='ref_climatos')
pattern2=root+"ReferenceDatasets/climatos/*/${frequency}/${variable}/${product}/ac/${variable}_*mon_${product}_${clim_period}-clim.nc" 
dataloc(project='ref_climatos', organization='generic', url=pattern2)


