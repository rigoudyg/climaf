"""

This module declares reference products on ciclad data organization and specifics, as managed by J. Servonnat at IPSL;

"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias, cfreqs, cdef
from climaf.site_settings import onCiclad

cfreqs('ref_pcmdi', {'monthly':'mo' , 'daily':'day' , 'seasonal':'mo', 'annual_cycle':'mo'})


if onCiclad:
    cproject('ref_pcmdi', ('frequency','annual_cycle'), 'product', 'clim_period')
    cdef('variable',     '*',           project='ref_pcmdi')
    cdef('product',      '*',           project='ref_pcmdi')
    cdef('clim_period',  '*',           project='ref_pcmdi')
    cdef('period',       '1950-2015',   project='ref_pcmdi')
    root="/data/jservon/Evaluation/ReferenceDatasets/PCMDI-MP/obs/*/${frequency}/${variable}/${product}/ac/"
    pattern2=root+"${variable}_*mon_${product}_${clim_period}-clim.nc" 
    dataloc(project='ref_pcmdi', organization='generic', url=pattern2)


