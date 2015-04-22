"""
Access observation datasets organized 'a la CAMI' at CNRM, at /cnrm/aster/data1/UTILS/cami/V1.7/climlinks/

Example ::

    >>> pr_gpcp=ds(project='CAMIOBS', experiment='GPCP2.5d', variable='pr', period='1979-1980')


"""

from climaf.dataloc import dataloc
from climaf.classes import cproject, calias

cproject("CAMIOBS" , separator="_")

# Root directory for obs data organized 'a la CAMI' on CNRM's Lustre file system.
CAMIOBS_root="/cnrm/aster/data1/UTILS/cami/V1.7/climlinks/"

# Pattern for matching CAMI obs data files and their directory. 
# We choose to use facet 'model' to carry the observation source
CAMIOBS_pattern="${experiment}/${variable}_1m_YYYYMM_YYYYMM_${experiment}.nc"

# Declare the CAMIOBS pattern to be associated with a project we name OBS_CAMI
dataloc(project="CAMIOBS", organization="generic", 
        url=[CAMIOBS_root+CAMIOBS_pattern])

# From here, you can define your dataset using these files. 
# You need only to define the facets useful w.r.t. the patterns
# i.e. here : model and variable
#pr_gpcp=ds(project="CAMIOBS", experiment="GPCP2.5d", variable="pr", period="1979-1980")
