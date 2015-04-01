"""
Standard site settings for working with CliMAF.

Currently tuned for dealing with CMIP5 data access a CNRM or IPSL

"""

import os
from climaf.api import dataloc

atCNRM=False
onCiclad=False
urls_CMIP5=None

# Declare locations for searching data for all projects,experiment and
# frequencies, and that data located in dirs listed in urls_CMIP5_CNRM
# and urls_CMIP5_Ciclad is organized as 'CMIP5_DRS'
if os.path.exists('/cnrm'):
    # Declare a list of root directories for CNRM-CM CMIP5 data on CNRM's Lustre file system.
    urls_CMIP5=["/cnrm/aster/data2/ESG/data1", "/cnrm/aster/data2/ESG/data2", "/cnrm/aster/data2/ESG/data5",
                "/cnrm/aster/data4/ESG/data6", "/cnrm/aster/data4/ESG/data7", "/cnrm/aster/data4/ESG/data8"]
    atCNRM=True
    
else :
    if os.path.exists('/prodigfs') :
        # Declare a list of root directories for CMIP5 data on IPLS's Ciclad file system
        urls_CMIP5=["/prodigfs/esg"]
        onCiclad=True

if urls_CMIP5 :
    # Next command will lead to explore all directories in 'url' for searching data for a CliMAF
    # dataset (by function ds) except if a more specific dataloc entry matches the arguments to 'ds'
    dataloc(project="CMIP5", organization="CMIP5_DRS", url=urls_CMIP5)


